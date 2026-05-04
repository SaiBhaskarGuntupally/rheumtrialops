"""Load RheumTrialOps synthetic CSV files into PostgreSQL raw tables.

The loader truncates and reloads raw tables without correcting intentional bad
records. Those records are part of the analytics validation workflow.
"""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd

try:
    from sqlalchemy import create_engine, text
except ImportError as exc:  # pragma: no cover - depends on local environment
    raise SystemExit(
        "Missing dependency: sqlalchemy. Install local dependencies with:\n"
        "  pip install sqlalchemy psycopg2-binary pandas"
    ) from exc


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"

TABLE_CONFIG = {
    "studies": {
        "file": "studies.csv",
        "date_columns": ["activation_date", "target_completion_date"],
    },
    "subjects": {
        "file": "subjects.csv",
        "date_columns": ["screening_date", "enrollment_date"],
    },
    "grants": {
        "file": "grants.csv",
        "date_columns": ["submission_date"],
    },
    "milestones": {
        "file": "milestones.csv",
        "date_columns": ["planned_date", "actual_date"],
    },
}


def get_connection_url() -> str:
    """Build a PostgreSQL connection URL from environment variables."""
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "rheumtrialops")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = quote_plus(os.getenv("POSTGRES_PASSWORD", "postgres"))
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def read_csv_for_table(table_name: str, config: dict[str, object]) -> pd.DataFrame:
    """Read one raw CSV and normalize blank values for PostgreSQL loading."""
    csv_path = RAW_DIR / str(config["file"])
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing input file: {csv_path}")

    df = pd.read_csv(csv_path, keep_default_na=True)
    for column in config["date_columns"]:
        df[column] = pd.to_datetime(df[column], errors="coerce").dt.date

    if table_name == "grants":
        df["jit_required"] = (
            df["jit_required"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({"true": True, "false": False})
        )

    return df.where(pd.notnull(df), None)


def main() -> None:
    engine = create_engine(get_connection_url())

    with engine.begin() as connection:
        for table_name, config in TABLE_CONFIG.items():
            df = read_csv_for_table(table_name, config)

            connection.execute(text(f"truncate table raw.{table_name};"))
            df.to_sql(
                table_name,
                con=connection,
                schema="raw",
                if_exists="append",
                index=False,
                method="multi",
            )

            loaded_count = connection.execute(
                text(f"select count(*) from raw.{table_name};")
            ).scalar_one()
            print(f"Loaded raw.{table_name}: {loaded_count} rows")

    print("Raw CSV load complete.")


if __name__ == "__main__":
    main()
