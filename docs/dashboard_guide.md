# Dashboard Guide

The Streamlit dashboard reads CSV files from `outputs/streamlit/` and does not require a live database connection.

## Global Filters

The sidebar includes filters for:

- Condition area
- Study status
- Intervention type
- Risk level

Filters apply across pages where the selected studies are present.

## Research Portfolio Overview

This page supports portfolio-level review.

Key decisions supported:

- Which condition areas and study statuses dominate the portfolio?
- How many studies are active or high risk?
- How much funding is tracked?
- How many JIT items and delayed milestones need attention?
- Which studies have the highest operational risk scores?

## Subject Accrual & Study Progress

This page supports accrual monitoring.

Key decisions supported:

- Which studies are below accrual targets?
- How does monthly enrollment trend over time?
- Which study arms are enrolling subjects?
- How many invalid enrollment timeline issues are visible?
- Which studies may need recruitment or operational review?

## Grants, Milestones & Data Quality

This page supports operational follow-up across grants, timelines, and validation.

Key decisions supported:

- Which grants are awarded, under review, not funded, or JIT pending?
- Which sponsors account for the largest funding totals?
- Which milestone types are delayed?
- Which high-severity data quality issues should be reviewed?
- Which high-risk studies and delayed milestones need drill-through attention?
