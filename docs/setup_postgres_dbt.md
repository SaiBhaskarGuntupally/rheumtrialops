# RheumTrialOps PostgreSQL and dbt Setup

This project uses local PostgreSQL for raw CSV storage and `dbt-postgres` for staging transformations.

## 1. Install Python dependencies

From the project root:

```powershell
pip install pandas sqlalchemy psycopg2-binary dbt-postgres
```

## 2. Create the PostgreSQL database

Run this from a terminal with PostgreSQL command-line tools available:

```powershell
createdb -U postgres rheumtrialops
```

If your local PostgreSQL user or password is different, use those credentials instead.

## 3. Set environment variables

The loader defaults to a beginner-friendly local setup:

- `POSTGRES_HOST=localhost`
- `POSTGRES_PORT=5432`
- `POSTGRES_DB=rheumtrialops`
- `POSTGRES_USER=postgres`
- `POSTGRES_PASSWORD=postgres`

To set them explicitly in PowerShell:

```powershell
$env:POSTGRES_HOST = "localhost"
$env:POSTGRES_PORT = "5432"
$env:POSTGRES_DB = "rheumtrialops"
$env:POSTGRES_USER = "postgres"
$env:POSTGRES_PASSWORD = "postgres"
```

## 4. Create schemas and raw tables

From the project root:

```powershell
psql -U postgres -d rheumtrialops -f sql/01_create_schema.sql
psql -U postgres -d rheumtrialops -f sql/02_create_raw_tables.sql
```

These scripts create:

- `raw`
- `staging`
- `marts`

The `marts` schema is reserved for later tasks.

## 5. Load raw CSV files into PostgreSQL

Make sure the raw CSV files exist under `data/raw/`, then run:

```powershell
python src/load_to_postgres.py
```

The loader truncates and reloads:

- `raw.studies`
- `raw.subjects`
- `raw.grants`
- `raw.milestones`

Intentional bad records are preserved for later validation and risk scoring work.

## 6. Configure the dbt profile

Create or update this file:

```text
%USERPROFILE%\.dbt\profiles.yml
```

Use:

```yaml
rheumtrialops:
  target: dev
  outputs:
    dev:
      type: postgres
      host: "{{ env_var('POSTGRES_HOST', 'localhost') }}"
      user: "{{ env_var('POSTGRES_USER', 'postgres') }}"
      password: "{{ env_var('POSTGRES_PASSWORD', 'postgres') }}"
      port: "{{ env_var('POSTGRES_PORT', '5432') | int }}"
      dbname: "{{ env_var('POSTGRES_DB', 'rheumtrialops') }}"
      schema: staging
      threads: 4
```

Adjust `user`, `password`, `host`, or `port` if your PostgreSQL setup differs.

## 7. Run dbt

From the dbt project folder:

```powershell
cd dbt_rheumtrialops
dbt debug
dbt run
dbt test
```

The staging models read from `raw` and create cleaned views in the configured dbt schema.

## Troubleshooting

### `createdb` or `psql` is not recognized

PostgreSQL command-line tools may not be on your `PATH`. Reopen your terminal after installing PostgreSQL, or run the commands from PostgreSQL's `bin` directory.

### Password authentication failed

The default password in this project is `postgres`, but your local PostgreSQL installation may use a different password. Update `POSTGRES_PASSWORD` and `profiles.yml`.

### Database does not exist

Create it first:

```powershell
createdb -U postgres rheumtrialops
```

### `ModuleNotFoundError: sqlalchemy` or `psycopg2`

Install the loader dependencies:

```powershell
pip install sqlalchemy psycopg2-binary pandas
```

### `dbt debug` cannot find profile

Confirm that `profiles.yml` exists at:

```text
%USERPROFILE%\.dbt\profiles.yml
```

Also confirm the profile name is exactly `rheumtrialops`.

### dbt relation `raw.studies` does not exist

Run the schema scripts and loader before `dbt run`:

```powershell
psql -U postgres -d rheumtrialops -f sql/01_create_schema.sql
psql -U postgres -d rheumtrialops -f sql/02_create_raw_tables.sql
python src/load_to_postgres.py
```
