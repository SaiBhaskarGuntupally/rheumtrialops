-- Create analytics schemas for the RheumTrialOps prototype.
-- raw: CSV-loaded source tables
-- staging: cleaned dbt staging models
-- marts: reserved for future dashboard-ready models

create schema if not exists raw;
create schema if not exists staging;
create schema if not exists marts;
