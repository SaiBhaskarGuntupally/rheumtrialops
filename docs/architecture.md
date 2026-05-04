# Architecture

RheumTrialOps uses a simple analytics flow. I kept the architecture small because the point of the project is the research operations reporting layer, not a heavy engineering platform.

The flow is:

Synthetic study and operations data moves into PostgreSQL raw tables.

PostgreSQL raw tables feed dbt staging models.

dbt staging models feed dbt mart models.

dbt mart models are exported as CSV files.

The Streamlit dashboard reads those CSV files.

The dashboard is deployed on Streamlit Cloud at:

[https://rheumtrialops.streamlit.app/](https://rheumtrialops.streamlit.app/)

## How the Layers Work

The Python data generation script creates the synthetic source CSVs for studies, subjects, grants, and milestones. The data is rheumatology-themed and includes intentional data quality issues so the validation layer has real examples to surface.

The raw PostgreSQL schema stores the CSV-loaded source records with very little transformation. I wanted this layer to preserve the input data, including the known bad records.

The dbt staging layer cleans up basic field formats and adds validation flags. This is where the project checks for issues such as invalid enrollment timelines or completed milestones without actual dates.

The dbt mart layer turns the staged records into reporting tables. These marts support portfolio summaries, accrual tracking, grant and JIT visibility, milestone delay monitoring, data quality review, and study risk scoring.

The export script writes the mart outputs to CSV files for Streamlit and Power BI. The Streamlit dashboard uses the exported CSV files only, so the deployed app does not need a live database connection.

The local PostgreSQL and dbt pipeline remains in the repository so the full data flow can still be reviewed from source data through final dashboard output.
