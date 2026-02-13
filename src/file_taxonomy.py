import json
import os
import sys
from pathlib import Path

import pandas as pd

try:
    from src.tag_extractor import extract_all_tags
except Exception:
    from tag_extractor import extract_all_tags


def read_source_file(file_path: str) -> pd.DataFrame:
    ext = Path(file_path).suffix.lower()
    if ext == ".csv":
        try:
            return pd.read_csv(file_path, encoding="utf-8", sep=None, engine="python")
        except Exception:
            return pd.read_csv(file_path, encoding="utf-8")
    if ext in {".xlsx", ".xls"}:
        return pd.read_excel(file_path)
    if ext == ".json":
        try:
            return pd.read_json(file_path)
        except ValueError:
            return pd.read_json(file_path, lines=True)
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        return pd.DataFrame({"Transcription": lines})
    return pd.read_csv(file_path, encoding="utf-8", sep=None, engine="python")


def normalize_col(col: str) -> str:
    return str(col).strip().lower().replace(" ", "_")


def pick_column(df: pd.DataFrame, candidates):
    normalized = {normalize_col(c): c for c in df.columns}
    for c in candidates:
        if c in normalized:
            return normalized[c]
    return None


def has_meaningful_value(value):
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, list):
        return len(value) > 0
    return True


def clean_tags(tags):
    out = {}
    for key, value in (tags or {}).items():
        if key in {"cleaned_text", "centres_interet", "timing"}:
            continue
        if has_meaningful_value(value):
            out[key] = value
    return out


def main():
    if len(sys.argv) < 2:
        raise ValueError("Missing file path argument")
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = read_source_file(file_path)
    if df is None or df.empty:
        print(json.dumps({"taxonomy_rows": []}, ensure_ascii=True))
        return

    transcription_col = pick_column(
        df,
        ["transcription", "transcript", "texte", "text", "message", "conversation", "notes", "contenu"],
    )
    if transcription_col is None:
        # fallback: first string-like column
        for col in df.columns:
            if df[col].dtype == "object":
                transcription_col = col
                break

    if transcription_col is None:
        print(json.dumps({"taxonomy_rows": []}, ensure_ascii=True))
        return

    client_col = pick_column(df, ["client", "client_name", "nom", "name", "fullname"])
    id_col = pick_column(df, ["id", "client_id", "customer_id", "uid", "uuid"])

    rows = []
    for idx, row in df.iterrows():
        text = row.get(transcription_col, "")
        text = "" if pd.isna(text) else str(text)
        if not text.strip():
            continue

        tags = clean_tags(extract_all_tags(text))
        if not tags:
            continue

        client_name = None
        if client_col is not None:
            raw_client = row.get(client_col, "")
            if not pd.isna(raw_client):
                client_name = str(raw_client).strip() or None
        if not client_name:
            client_name = f"Client {idx + 1}"

        client_id = None
        if id_col is not None:
            raw_id = row.get(id_col, "")
            if not pd.isna(raw_id):
                client_id = str(raw_id).strip() or None

        rows.append(
            {
                "row_index": int(idx + 1),
                "client": client_name,
                "client_id": client_id,
                "tags": tags,
            }
        )

    print(json.dumps({"taxonomy_rows": rows}, ensure_ascii=True))


if __name__ == "__main__":
    main()
