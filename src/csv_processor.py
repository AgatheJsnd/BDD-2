"""
Module de lecture et traitement du fichier CSV
"""
import pandas as pd
from typing import List, Dict


class CSVProcessor:
    """Classe pour lire et traiter le fichier CSV des conversations clients"""

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.data = None

    def load_data(self) -> pd.DataFrame:
        """Charge le fichier CSV"""
        try:
            self.data = pd.read_csv(self.csv_path, encoding="utf-8")
            print(f"OK - CSV charge : {len(self.data)} conversations")
            return self.data
        except Exception as e:
            print(f"ERREUR - Chargement du CSV : {e}")
            return None

    def get_conversations(self) -> List[Dict]:
        """Retourne la liste des conversations sous forme de dictionnaires"""
        if self.data is None:
            self.load_data()

        conversations = []
        for _, row in self.data.iterrows():
            conversations.append({
                "client_id": row["ID"],
                "date": row["Date"],
                "duration": row["Duration"],
                "language": row["Language"],
                "length": row["Length"],
                "transcription": row["Transcription"],
            })

        return conversations

    def get_conversation_by_id(self, client_id: str) -> Dict:
        """Recupere une conversation specifique par ID"""
        if self.data is None:
            self.load_data()

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
