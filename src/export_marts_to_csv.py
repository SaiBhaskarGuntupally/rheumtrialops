"""Export RheumTrialOps dbt mart tables to CSV files for BI tools.

Exports are written to both outputs/streamlit and outputs/powerbi so later
dashboard work can use the same curated mart outputs.
"""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd

try:
    from sqlalchemy import create_engine
except ImportError as exc:  # pragma: no cover - depends on local environment
    raise SystemExit(
        "Missing dependency: sqlalchemy. Install local dependencies with:\n"
        "  pip install sqlalchemy psycopg2-binary pandas"
    ) from exc


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIRS = [
    ROOT_DIR / "outputs" / "streamlit",
    ROOT_DIR / "outputs" / "powerbi",
]

MART_EXPORTS = {
    "mart_research_portfolio_summary": "research_portfolio_summary.csv",
    "mart_subject_accrual": "subject_accrual.csv",
    "mart_grant_jit_tracking": "grant_jit_tracking.csv",
    "mart_milestone_delay_summary": "milestone_delay_summary.csv",
    "mart_data_quality_summary": "data_quality_summary.csv",
    "mart_study_risk_score": "study_risk_score.csv",
}


def get_connection_url() -> str:
    """Build a PostgreSQL connection URL from environment variables."""
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "rheumtrialops")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = quote_plus(os.getenv("POSTGRES_PASSWORD", "postgres"))
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def main() -> None:
    for output_dir in OUTPUT_DIRS:
        output_dir.mkdir(parents=True, exist_ok=True)

    engine = create_engine(get_connection_url())

    for table_name, file_name in MART_EXPORTS.items():
        query = f"select * from marts.{table_name};"
        df = pd.read_sql_query(query, engine)

        for output_dir in OUTPUT_DIRS:
            output_path = output_dir / file_name
            df.to_csv(output_path, index=False)

        print(f"Exported marts.{table_name}: {len(df)} rows to {file_name}")

    print("Mart CSV export complete.")


if __name__ == "__main__":
    main()
