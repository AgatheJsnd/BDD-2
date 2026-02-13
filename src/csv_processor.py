"""
Module de lecture et traitement du fichier CSV
"""
import pandas as pd
from typing import List, Dict
from pathlib import Path


class CSVProcessor:
    """Classe pour lire et traiter le fichier CSV des conversations clients"""

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.data = None

    @staticmethod
    def _normalize_colname(col: str) -> str:
        return str(col).strip().lower().replace(" ", "_")

    def _read_source_file(self) -> pd.DataFrame:
        """Charge plusieurs formats de fichiers en DataFrame."""
        ext = Path(self.csv_path).suffix.lower()

        if ext == ".csv":
            try:
                return pd.read_csv(self.csv_path, encoding="utf-8", sep=None, engine="python")
            except Exception:
                return pd.read_csv(self.csv_path, encoding="utf-8")

        if ext in {".xlsx", ".xls"}:
            return pd.read_excel(self.csv_path)

        if ext == ".json":
            try:
                return pd.read_json(self.csv_path)
            except ValueError:
                # JSON lines
                return pd.read_json(self.csv_path, lines=True)

        if ext == ".txt":
            with open(self.csv_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            return pd.DataFrame({"Transcription": lines})

        raise ValueError(f"Format non supporte: {ext}")

    def _find_first_existing_column(self, columns_map: Dict[str, str], candidates: List[str]) -> str:
        for candidate in candidates:
            col = columns_map.get(candidate)
            if col is not None:
                return col
        return None

    def _standardize_schema(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """Mappe des colonnes variées vers le schéma attendu."""
        if raw_df is None or raw_df.empty:
            return pd.DataFrame(columns=["ID", "Date", "Duration", "Language", "Length", "Transcription"])

        df = raw_df.copy()
        normalized_to_original = {self._normalize_colname(col): col for col in df.columns}

        id_col = self._find_first_existing_column(normalized_to_original, [
            "id", "client_id", "customer_id", "user_id", "uid", "uuid"
        ])
        date_col = self._find_first_existing_column(normalized_to_original, [
            "date", "created_at", "timestamp", "datetime", "date_rdv"
        ])
        duration_col = self._find_first_existing_column(normalized_to_original, [
            "duration", "duree", "duration_seconds", "time_spent"
        ])
        language_col = self._find_first_existing_column(normalized_to_original, [
            "language", "langue", "lang"
        ])
        length_col = self._find_first_existing_column(normalized_to_original, [
            "length", "taille", "size", "conversation_length"
        ])
        transcription_col = self._find_first_existing_column(normalized_to_original, [
            "transcription", "transcript", "texte", "text", "message", "conversation", "notes", "contenu"
        ])

        # Fallback transcription: première colonne textuelle exploitable.
        if transcription_col is None:
            text_candidates = []
            for col in df.columns:
                series = df[col]
                if series.dtype == "object" and not series.dropna().empty:
                    text_candidates.append(col)
            if text_candidates:
                transcription_col = text_candidates[0]

        if transcription_col is None:
            raise ValueError("Aucune colonne texte exploitable pour la transcription n'a ete trouvee.")

        out = pd.DataFrame()
        out["ID"] = df[id_col] if id_col else [f"ROW-{idx + 1}" for idx in range(len(df))]
        out["Date"] = df[date_col] if date_col else ""
        out["Duration"] = df[duration_col] if duration_col else ""
        out["Language"] = df[language_col] if language_col else "FR"
        out["Length"] = df[length_col] if length_col else "medium"
        out["Transcription"] = df[transcription_col].fillna("").astype(str)
        return out

    def load_data(self) -> pd.DataFrame:
        """Charge le fichier CSV"""
        try:
            raw_data = self._read_source_file()
            self.data = self._standardize_schema(raw_data)
            print(f"OK - CSV charge : {len(self.data)} conversations")
            return self.data
        except Exception as e:
            print(f"ERREUR - Chargement du CSV : {e}")
            self.data = pd.DataFrame(columns=["ID", "Date", "Duration", "Language", "Length", "Transcription"])
            return None

    def get_conversations(self) -> List[Dict]:
        """Retourne la liste des conversations sous forme de dictionnaires"""
        if self.data is None:
            self.load_data()
        if self.data is None or self.data.empty:
            return []

        conversations = []
        transcription_col = "Transcription"

        for _, row in self.data.iterrows():
            conversations.append({
                "client_id": row["ID"],
                "date": row["Date"] if pd.notna(row["Date"]) else "",
                "duration": row["Duration"] if pd.notna(row["Duration"]) else "",
                "language": row["Language"] if pd.notna(row["Language"]) else "FR",
                "length": row["Length"] if pd.notna(row["Length"]) else "medium",
                "transcription": row[transcription_col] if pd.notna(row[transcription_col]) else "",
            })

        return conversations

    def get_conversation_by_id(self, client_id: str) -> Dict:
        """Recupere une conversation specifique par ID"""
        if self.data is None:
            self.load_data()
        if self.data is None or self.data.empty:
            return None

        row = self.data[self.data["ID"] == client_id]
        if not row.empty:
            row = row.iloc[0]
            return {
                "client_id": row["ID"],
                "date": row["Date"],
                "duration": row["Duration"],
                "language": row["Language"],
                "length": row["Length"],
                "transcription": row["Transcription"],
            }
        return None
