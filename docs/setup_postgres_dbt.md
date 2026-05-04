# PostgreSQL and dbt Setup

The live dashboard is available here:

[https://rheumtrialops.streamlit.app/](https://rheumtrialops.streamlit.app/)

Most readers can start with the live dashboard first. This setup note is for anyone who wants to run the full local pipeline from synthetic CSV files through PostgreSQL, dbt, exported mart files, and the Streamlit app.

## Install the Python Packages

From the project folder, install the packages used by the loader and dbt:

    pip install pandas sqlalchemy psycopg2-binary dbt-postgres

The dashboard itself uses the packages listed in requirements.txt.

## Create the Local PostgreSQL Database

This project expects a local database named rheumtrialops.

    createdb -U postgres rheumtrialops

If your PostgreSQL username is different, use your own username in the command.

## Set the Database Connection Values

The Python loader already has local defaults:

- host: localhost
- port: 5432
- database: rheumtrialops
- user: postgres
- password: postgres

If your local setup is different, set the values in PowerShell before running the loader:

    $env:POSTGRES_HOST = "localhost"
    $env:POSTGRES_PORT = "5432"
    $env:POSTGRES_DB = "rheumtrialops"
    $env:POSTGRES_USER = "postgres"
    $env:POSTGRES_PASSWORD = "postgres"

## Create the Schemas and Raw Tables

Run these from the project folder:

    psql -U postgres -d rheumtrialops -f sql/01_create_schema.sql
    psql -U postgres -d rheumtrialops -f sql/02_create_raw_tables.sql

The SQL files create the raw, staging, and marts schemas. The raw schema stores the CSV-loaded source records. The staging and marts schemas are used by dbt.

## Load the Raw CSV Files

Generate the synthetic data first if the CSV files are not already present:

    python src/generate_data.py

Then load the raw tables:

    python src/load_to_postgres.py

The loader truncates and reloads the raw studies, subjects, grants, and milestones tables. The intentional bad records are kept because the data quality dashboard depends on them.

## Configure dbt

dbt needs a profile file in your user folder:

    %USERPROFILE%\.dbt\profiles.yml

Use this profile as a starting point:

    rheumtrialops:
      target: dev
      outputs:
        dev:
          type: postgres
          host: localhost
          user: postgres
          password: postgres
          port: 5432
          dbname: rheumtrialops
          schema: staging
          threads: 4

Change the user, password, host, or port if your PostgreSQL setup uses different values.

## Run dbt

From the dbt project folder:

    cd dbt_rheumtrialops
    dbt debug
    dbt run
    dbt test
    cd ..

dbt builds the staging and mart models and runs the validation tests.

## Export the Mart Files

After dbt finishes, export the reporting tables:

    python src/export_marts_to_csv.py

The exported files are written under outputs/streamlit and outputs/powerbi.

## Run the Dashboard Locally

The deployed version is usually easier to review, but the local app can be started with:

    streamlit run app.py

## Common Local Issues

If createdb or psql is not recognized, PostgreSQL command-line tools are probably not on your system path. Reopen the terminal after installing PostgreSQL, or run the commands from the PostgreSQL bin folder.

If password authentication fails, update the password in the environment variable and in the dbt profile.

If dbt cannot find the profile, confirm that profiles.yml exists under your user .dbt folder and that the profile name is rheumtrialops.

If dbt says a raw table does not exist, run the schema SQL files and the Python loader before running dbt.

If Python cannot find sqlalchemy or psycopg2, reinstall the loader dependencies:

    pip install sqlalchemy psycopg2-binary pandas
