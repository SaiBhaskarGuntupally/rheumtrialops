-- Raw tables mirror the synthetic CSV files created from src/generate_data.py.
-- These tables intentionally preserve known data quality issues for later tests.

create table if not exists raw.studies (
    study_id text primary key,
    nct_id text,
    protocol_id text,
    study_title text,
    principal_investigator text,
    condition_area text,
    study_type text,
    study_status text,
    intervention_type text,
    target_accrual integer,
    activation_date date,
    target_completion_date date
);

create table if not exists raw.subjects (
    subject_id text primary key,
    study_id text,
    screening_date date,
    enrollment_date date,
    study_arm text,
    subject_status text,
    eligibility_status text,
    withdrawal_reason text
);

create table if not exists raw.grants (
    grant_id text primary key,
    study_id text,
    sponsor_name text,
    funding_amount numeric,
    submission_date date,
    submission_status text,
    jit_required boolean,
    jit_status text,
    award_status text
);

create table if not exists raw.milestones (
    milestone_id text primary key,
    study_id text,
    milestone_type text,
    planned_date date,
    actual_date date,
    milestone_status text,
    days_delayed integer
);
