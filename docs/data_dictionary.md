# Data Dictionary

This file explains the main data used in RheumTrialOps. I kept the model intentionally small so the project is easy to review.

## Source Data

The source layer has four main files.

Studies contains one record per synthetic study. It includes the study identifier, NCT-style identifier, protocol identifier, study title, principal investigator, condition area, study type, study status, intervention type, target accrual, activation date, and target completion date.

Subjects contains one record per synthetic subject. It includes the subject identifier, linked study identifier, screening date, enrollment date, study arm, subject status, eligibility status, and withdrawal reason.

Grants contains one record per synthetic grant or funding record. It includes the grant identifier, linked study identifier, sponsor name, funding amount, submission date, submission status, JIT required flag, JIT status, and award status.

Milestones contains one record per synthetic study milestone. It includes the milestone identifier, linked study identifier, milestone type, planned date, actual date, milestone status, and days delayed.

## Reporting Outputs

The dbt mart layer creates six reporting outputs.

Research portfolio summary is the main study-level table. It combines study metadata with accrual counts, funding totals, JIT counts, milestone counts, and data quality issue counts.

Subject accrual summarizes screening and enrollment activity by study, month, and study arm. It also keeps counts of invalid enrollment timelines, enrolled ineligible subjects, and missing withdrawal reasons.

Grant JIT tracking keeps one row per grant. It includes sponsor, funding amount, submission status, JIT status, award status, validation flags, and a simple operational status label.

Milestone delay summary keeps one row per milestone. It includes planned and actual dates, milestone status, delay fields, missing actual date flags, and a milestone risk level.

Data quality summary turns validation flags into issue rows. Each row shows the study, source table, source record, rule name, issue severity, and a short issue description.

Study risk score keeps one row per study. It combines accrual progress, pending JIT count, delayed milestone count, high-severity data quality count, total data quality issue count, days to completion, final risk score, risk level, and reason summary.

## Why These Fields Matter

The studies data gives portfolio visibility.

The subjects data supports screening and accrual tracking.

The grants data supports funding and JIT visibility.

The milestones data supports timeline monitoring.

The quality and risk outputs make exceptions easier to find instead of burying them in raw data.

Together, these tables support the dashboard views without making the project larger than it needs to be.
