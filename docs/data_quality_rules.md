# Data Quality Rules

The data quality layer preserves bad records and flags them for operations reporting. These rules are designed for a synthetic dashboard prototype and should not be interpreted as clinical adjudication.

| Source | Rule Name | Severity | Logic | Why It Matters |
| --- | --- | --- | --- | --- |
| `studies` | Invalid Study Timeline | High | `target_completion_date < activation_date` | Study completion dates before activation indicate invalid timeline metadata and can distort timeline reporting. |
| `subjects` | Invalid Enrollment Timeline | High | `enrollment_date < screening_date` | Enrollment before screening is an operational data integrity issue and should be reviewed before accrual reporting. |
| `subjects` | Enrolled Ineligible Subject | High | `subject_status in ('Enrolled', 'Active') and eligibility_status = 'Ineligible'` | Ineligible enrolled or active subjects require review in study operations reporting. |
| `subjects` | Missing Withdrawal Reason | Medium | `subject_status = 'Withdrawn' and withdrawal_reason is null, blank, or 'None'` | Withdrawal reason completeness supports retention analysis and operational follow-up. |
| `grants` | Invalid Funding Amount | High | `funding_amount < 0` | Negative funding amounts distort financial reporting and award tracking. |
| `grants` | Invalid JIT Status | Medium | `jit_required = true and jit_status is null, blank, or 'Not Required'` | Required JIT activity should have a meaningful status for grant operations tracking. |
| `milestones` | Completed Milestone Missing Actual Date | High | `milestone_status = 'Completed' and actual_date is null` | Completed milestones need actual dates for timeline, delay, and closeout reporting. |

## Reporting Output

These rules feed `mart_data_quality_summary`, where each failed rule becomes one dashboard-ready issue row. A single source record can create multiple issue rows if it fails multiple rules.
