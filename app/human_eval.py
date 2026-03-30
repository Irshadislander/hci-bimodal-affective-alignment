"""Human evaluation template helpers for the Day 7 prototype."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

try:  # pragma: no cover - optional dependency
    import pandas as pd
except Exception:  # pragma: no cover - keep the prototype runnable without pandas
    pd = None  # type: ignore[assignment]


HUMAN_EVAL_COLUMNS = [
    "case_id",
    "user_text",
    "text_top_emotion",
    "face_top_emotion",
    "fused_top_emotion",
    "response",
    "empathy_rating",
    "social_presence_rating",
    "trust_rating",
    "notes",
]

BASE_DIR = Path(__file__).resolve().parents[1]
EXPERIMENTS_DIR = BASE_DIR / "experiments"
HUMAN_EVAL_TEMPLATE_PATH = EXPERIMENTS_DIR / "human_eval_template.csv"


def _table_rows(table: Any) -> list[dict[str, Any]]:
    """Convert a table-like object into a list of row dictionaries."""

    if pd is not None and isinstance(table, pd.DataFrame):
        return table.to_dict(orient="records")
    if isinstance(table, list):
        return [dict(row) for row in table]
    if hasattr(table, "to_dict"):
        try:
            return list(table.to_dict(orient="records"))
        except Exception:
            pass
    if hasattr(table, "records"):
        return [dict(row) for row in table.records]
    return [dict(row) for row in table]


def _build_table(rows: list[dict[str, Any]]) -> object:
    """Build a display-friendly table object from row dictionaries."""

    if pd is not None:
        return pd.DataFrame(rows, columns=HUMAN_EVAL_COLUMNS)
    return rows


def _save_table(table: object, path: str | Path) -> str:
    """Save a table-like object to CSV and return the written path."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if pd is not None and isinstance(table, pd.DataFrame):
        table.to_csv(output_path, index=False)
        return str(output_path)

    rows = _table_rows(table)
    if rows:
        fieldnames = [column for column in HUMAN_EVAL_COLUMNS if column in rows[0]]
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        output_path.write_text("", encoding="utf-8")
    return str(output_path)


def make_human_eval_template(cases_df: Any) -> object:
    """Create a blank human-evaluation template from a case table.

    Ratings are intentionally left empty so a reviewer can fill them in later.
    """

    rows = []
    for index, case in enumerate(_table_rows(cases_df), start=1):
        rows.append(
            {
                "case_id": case.get("case_id", index),
                "user_text": case.get("user_text", ""),
                "text_top_emotion": case.get("text_top_emotion", ""),
                "face_top_emotion": case.get("face_top_emotion", ""),
                "fused_top_emotion": case.get("fused_top_emotion", ""),
                "response": case.get("response", case.get("empathetic_response", "")),
                "empathy_rating": "",
                "social_presence_rating": "",
                "trust_rating": "",
                "notes": "",
            }
        )
    return _build_table(rows)


def save_human_eval_template(df: object, path: str) -> str:
    """Save a human evaluation template to CSV and return the file path."""

    return _save_table(df, path)
