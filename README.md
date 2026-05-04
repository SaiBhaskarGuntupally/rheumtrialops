# RheumTrialOps

Clinical Research Operations Analytics for Rheumatology Studies

## Live Dashboard

The dashboard is deployed on Streamlit Cloud: [https://rheumtrialops.streamlit.app/](https://rheumtrialops.streamlit.app/)

The live app is the easiest way to review the final dashboard. The local setup steps are included later for anyone who wants to inspect the full data pipeline.

## What to Read First

For the quickest understanding of the project, start with:

- [Project Story and Design Tradeoffs](docs/project_story_and_tradeoffs.md): why I built this, what I considered, and why I chose this approach.
- [Architecture](docs/architecture.md): how the data moves from synthetic CSVs to PostgreSQL, dbt, exports, and Streamlit.
- [Clinical Research Workflow Mapping](docs/clinical_research_mapping.md): how the project relates to REDCap, OnCore/CTMS, HURON-style workflows, and investigator reporting without claiming direct integration.

For technical reference, use [Data Dictionary](docs/data_dictionary.md) and [PostgreSQL/dbt Setup](docs/setup_postgres_dbt.md).

## Project Overview

RheumTrialOps is a lightweight clinical research operations analytics prototype built with public or synthetic rheumatology study metadata and fully synthetic operational data. It tracks study portfolio status, subject accrual, grant/JIT activity, study milestones, data quality validation, and rule-based operational risk scoring.

The project is organized around rheumatology and chronic disease research themes such as rheumatoid arthritis, gout, osteoporosis, lupus, inflammatory arthritis, telemedicine follow-up, technology-enabled care delivery, infection prevention, polypharmacy monitoring, and chronic inflammatory disease.

## Why This Project Was Built

This project was built to demonstrate how healthcare data engineering, reporting, SQL modeling, validation, and dashboarding skills can translate into clinical research operations workflows.

It emphasizes transferable skills: SQL modeling, dbt transformations, data validation, dashboarding, study accrual tracking, grant/JIT visibility, milestone monitoring, and operational risk scoring.

## Architecture

The project uses a simple analytics flow:

Synthetic/public study metadata and synthetic operational data move into PostgreSQL raw tables.

PostgreSQL raw tables feed dbt staging models.

dbt staging models feed dbt mart models.

The mart outputs are exported as CSV files.

The Streamlit dashboard reads those CSV files and is deployed on Streamlit Cloud.

## Data Model

Source tables:

- studies: synthetic protocol and portfolio metadata.
- subjects: synthetic screening, enrollment, eligibility, and disposition records.
- grants: synthetic sponsor, submission, award, funding, and JIT records.
- milestones: synthetic study timeline and milestone records.

Main mart outputs:

- research portfolio summary: one row per study with portfolio, accrual, funding, milestone, and quality metrics.
- subject accrual: monthly subject accrual by study and study arm.
- grant JIT tracking: grant status, funding, award, and JIT tracking.
- milestone delay summary: milestone delay and risk tracking.
- data quality summary: one row per failed validation rule.
- study risk score: transparent rule-based operational risk score by study.

## Dashboard Pages

- **Research Portfolio Overview**: portfolio KPIs, study status, condition areas, funding, risk distribution, and operational takeaway text.
- **Subject Accrual & Study Progress**: screening and enrollment KPIs, accrual trends, study-arm enrollment, and studies below accrual target.
- **Grants, Milestones & Data Quality**: grant/JIT tracking, funding by sponsor, delayed milestones, high-severity quality issues, and high-risk study tables.

## Data Quality Rules

Example validation rules include:

- Enrollment date before screening date.
- Enrolled subject marked ineligible.
- Withdrawn subject missing withdrawal reason.
- Target completion date before activation date.
- Funding amount below zero.
- JIT required but missing or invalid JIT status.
- Completed milestone missing actual date.

Intentional bad records are preserved so the dashboard can show validation and monitoring workflows.

## Rule-Based Risk Score

This is a transparent operational risk score using accrual progress, pending JIT items, delayed milestones, high-severity data quality issues, and approaching completion timelines. It is intended for operational review, not clinical prediction.

## Clinical Research Platform Mapping

RheumTrialOps uses clinical research platforms as workflow context only. REDCap-style workflows are represented through synthetic subject and enrollment records. OnCore and CTMS-style workflows are represented through study status, milestones, accrual, and risk scoring. HURON-style research administration is represented through synthetic grant status, JIT tracking, and funding visibility. Investigator reporting is represented through the Streamlit dashboard pages. Data quality oversight is represented through dbt tests and the validation summary.

## Tech Stack

- Python
- PostgreSQL
- dbt
- Streamlit
- pandas
- Plotly
- SQL

## What This Project Does Not Claim

"This project does not use real patient data, real UAB data, or direct access to REDCap, OnCore, HURON, PowerTrials, or CTMS systems. It uses public or synthetic study metadata and fully synthetic operational data to demonstrate transferable data modeling, validation, workflow monitoring, and reporting skills for clinical research operations."

## How to Run Locally

The live dashboard is available at [https://rheumtrialops.streamlit.app/](https://rheumtrialops.streamlit.app/). These local steps are only needed if you want to regenerate the data, run the PostgreSQL/dbt pipeline, or inspect the project end to end.

Install dependencies:

    pip install -r requirements.txt
    pip install sqlalchemy psycopg2-binary dbt-postgres

Generate synthetic raw data:

    python src/generate_data.py

Create PostgreSQL schemas and raw tables, then load CSVs:

    psql -U postgres -d rheumtrialops -f sql/01_create_schema.sql
    psql -U postgres -d rheumtrialops -f sql/02_create_raw_tables.sql
    python src/load_to_postgres.py

Run dbt:

    cd dbt_rheumtrialops
    dbt run
    dbt test
    cd ..

Export marts and launch the dashboard:

    python src/export_marts_to_csv.py
    streamlit run app.py

## Project Summary

This project demonstrates the ability to translate healthcare data engineering skills into clinical research operations reporting, including study tracking, subject accrual monitoring, grant/JIT visibility, data quality validation, and investigator-facing dashboards.
