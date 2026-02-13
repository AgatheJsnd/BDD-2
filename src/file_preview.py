import json
import os
import sys
from pathlib import Path

import pandas as pd


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
        return pd.DataFrame({"text": lines})
    return pd.read_csv(file_path, encoding="utf-8", sep=None, engine="python")


def to_native_number(val):
    if pd.isna(val):
        return None
    try:
        return float(val)
    except Exception:
        return None


def main():
    if len(sys.argv) < 2:
        raise ValueError("Missing file path argument")

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = read_source_file(file_path)
    if df is None:
        df = pd.DataFrame()

    row_count = int(len(df))
    column_count = int(len(df.columns))
    columns = [str(c) for c in df.columns]

    missing_by_column = []
    if column_count > 0:
        for col in df.columns:
            missing = int(df[col].isna().sum())
            missing_by_column.append({"column": str(col), "missing": missing})
        missing_by_column.sort(key=lambda x: x["missing"], reverse=True)

    numeric_metrics = []
    if row_count > 0:
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        for col in numeric_cols[:10]:
            series = df[col].dropna()
            if series.empty:
                continue
            numeric_metrics.append(
                {
                    "column": str(col),
                    "count": int(series.count()),
                    "min": to_native_number(series.min()),
                    "max": to_native_number(series.max()),
                    "mean": to_native_number(series.mean()),
                }
            )

    top_categories = []
    if row_count > 0:
        cat_cols = df.select_dtypes(include=["object", "category", "bool", "string"]).columns.tolist()
        for col in cat_cols[:8]:
            vc = df[col].astype(str).replace("nan", pd.NA).dropna().value_counts().head(8)
            values = [{"name": str(k), "count": int(v)} for k, v in vc.items()]
            if values:
                top_categories.append({"column": str(col), "values": values})

    preview_rows = []
    if row_count > 0:
        preview = df.head(5).fillna("").astype(str).to_dict(orient="records")
        preview_rows = preview

    payload = {
        "file_name": os.path.basename(file_path),
        "row_count": row_count,
        "column_count": column_count,
        "columns": columns,
        "missing_by_column": missing_by_column[:12],
        "numeric_metrics": numeric_metrics,
        "top_categories": top_categories,
        "preview_rows": preview_rows,
    }
    print(json.dumps(payload, ensure_ascii=True))


if __name__ == "__main__":
    main()
