# RheumTrialOps Mart Logic

The mart layer converts cleaned staging models into dashboard-ready reporting tables. These models do not remove intentional data quality issues. They preserve records and expose operational flags for reporting.

## mart_research_portfolio_summary

Use case: executive and operations portfolio overview.

Grain: one row per study.

This mart combines study metadata with subject accrual, grant funding, JIT activity, milestone progress, and data quality issue counts. It supports dashboard views such as active study counts, accrual performance, funding totals, delayed milestones, and studies with data quality concerns.

## mart_subject_accrual

Use case: monthly accrual tracking.

Grain: one row per study, enrollment month, and study arm.

This mart groups subjects by enrollment month using `enrollment_date`, with `screening_date` as the fallback when enrollment date is missing. Invalid enrollment timelines remain visible through count fields.

## mart_grant_jit_tracking

Use case: grant pipeline, award, funding, and JIT monitoring.

Grain: one row per grant.

This mart joins grant records to study metadata and adds `grant_operational_status` labels for awarded, JIT pending, under review, not funded, and other grants.

## mart_milestone_delay_summary

Use case: study timeline and milestone delay monitoring.

Grain: one row per milestone.

This mart exposes planned and actual milestone dates, delay flags, missing completion date flags, and a simple `milestone_risk_level`.

## mart_data_quality_summary

Use case: data quality dashboard and issue drill-through.

Grain: one row per failed validation rule.

This mart converts staging flags into issue rows with rule names, severity, descriptions, source tables, and record identifiers. A single record can appear more than once if it fails more than one rule.

## mart_study_risk_score

Use case: operational prioritization.

Grain: one row per study.

This mart uses portfolio metrics and data quality counts to create a rule-based score from 0 to 100. It supports dashboard sorting and filtering by risk level and risk reasons.
