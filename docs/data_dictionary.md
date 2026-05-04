# Data Dictionary

This dictionary documents the synthetic source tables and dashboard-ready mart outputs used by RheumTrialOps.

## Source Tables

### studies

| Column | Description |
| --- | --- |
| `study_id` | Synthetic study identifier. |
| `nct_id` | Synthetic NCT-style identifier. |
| `protocol_id` | Synthetic rheumatology protocol identifier. |
| `study_title` | Rheumatology-themed study title. |
| `principal_investigator` | Synthetic investigator name. |
| `condition_area` | Rheumatology or chronic disease condition area. |
| `study_type` | Interventional, observational, registry, or pragmatic trial. |
| `study_status` | Operational study status. |
| `intervention_type` | Care delivery or intervention category. |
| `target_accrual` | Target number of enrolled subjects. |
| `activation_date` | Synthetic study activation date. |
| `target_completion_date` | Synthetic planned completion date. |

### subjects

| Column | Description |
| --- | --- |
| `subject_id` | Synthetic subject identifier. |
| `study_id` | Linked study identifier. |
| `screening_date` | Synthetic screening date. |
| `enrollment_date` | Synthetic enrollment date. |
| `study_arm` | Synthetic study arm. |
| `subject_status` | Screening, enrollment, completion, withdrawal, or follow-up status. |
| `eligibility_status` | Eligible, ineligible, or pending review. |
| `withdrawal_reason` | Synthetic withdrawal reason where applicable. |

### grants

| Column | Description |
| --- | --- |
| `grant_id` | Synthetic grant identifier. |
| `study_id` | Linked study identifier. |
| `sponsor_name` | Synthetic sponsor/funding source category. |
| `funding_amount` | Synthetic funding amount. |
| `submission_date` | Synthetic grant submission date. |
| `submission_status` | Draft, submitted, under review, JIT requested, awarded, or not funded. |
| `jit_required` | Whether JIT activity is required. |
| `jit_status` | JIT status. |
| `award_status` | Award outcome status. |

### milestones

| Column | Description |
| --- | --- |
| `milestone_id` | Synthetic milestone identifier. |
| `study_id` | Linked study identifier. |
| `milestone_type` | Milestone category. |
| `planned_date` | Planned milestone date. |
| `actual_date` | Actual milestone date when available. |
| `milestone_status` | Not started, in progress, completed, or delayed. |
| `days_delayed` | Difference between actual and planned date when available. |

## Mart Outputs

### research_portfolio_summary

One row per study with study metadata, accrual counts, funding totals, JIT counts, milestone counts, and data quality issue counts.

Key columns:

- Study identifiers and metadata: `study_id`, `nct_id`, `protocol_id`, `study_title`, `principal_investigator`, `condition_area`, `study_type`, `study_status`, `intervention_type`
- Timeline and target fields: `target_accrual`, `activation_date`, `target_completion_date`, `study_duration_days`, `is_active_study`
- Subject metrics: `total_subjects_screened`, `total_subjects_enrolled`, `total_subjects_active`, `total_subjects_completed`, `total_subjects_withdrawn`, `accrual_rate`
- Grant metrics: `total_grants`, `total_funding_amount`, `awarded_funding_amount`, `pending_jit_count`
- Milestone and quality metrics: `total_milestones`, `delayed_milestone_count`, `completed_milestone_count`, `data_quality_issue_count`

### subject_accrual

Monthly subject accrual by study and study arm, including screened, enrolled, active, completed, withdrawn, ineligible, and data quality issue counts.

Key columns:

- Study grouping: `study_id`, `protocol_id`, `study_title`, `condition_area`, `intervention_type`
- Accrual grouping: `enrollment_month`, `study_arm`
- Counts: `screened_count`, `enrolled_count`, `active_count`, `completed_count`, `withdrawn_count`, `ineligible_count`
- Quality counts: `invalid_enrollment_date_count`, `enrolled_ineligible_count`, `withdrawn_missing_reason_count`

### grant_jit_tracking

One row per grant with sponsor, funding, submission, JIT, award fields, validation flags, and operational status.

Key columns:

- Grant and study identifiers: `grant_id`, `study_id`, `protocol_id`, `study_title`
- Grant details: `sponsor_name`, `funding_amount`, `submission_date`, `submission_status`, `award_status`, `is_awarded`
- JIT details: `jit_required`, `jit_status`, `is_jit_status_invalid`
- Validation and status: `is_funding_amount_invalid`, `grant_operational_status`

### milestone_delay_summary

One row per milestone with planned and actual dates, delay fields, validation flags, and milestone risk level.

Key columns:

- Milestone and study identifiers: `milestone_id`, `study_id`, `protocol_id`, `study_title`
- Milestone details: `milestone_type`, `planned_date`, `actual_date`, `milestone_status`, `days_delayed`
- Validation and risk: `is_completed_missing_actual_date`, `is_delayed`, `milestone_risk_level`

### data_quality_summary

One row per failed validation rule with source table, record identifier, rule name, severity, and issue description.

Key columns:

- Issue identifier: `issue_id`
- Study context: `study_id`, `protocol_id`, `study_title`
- Source context: `source_table`, `record_id`
- Rule details: `rule_name`, `issue_severity`, `issue_description`

### study_risk_score

One row per study with accrual progress, JIT count, delayed milestone count, data quality counts, days to completion, risk score, risk level, and reason summary.

Key columns:

- Study context: `study_id`, `protocol_id`, `study_title`, `condition_area`, `study_status`
- Accrual and operations inputs: `target_accrual`, `total_subjects_enrolled`, `accrual_rate`, `pending_jit_count`, `delayed_milestone_count`
- Quality and timeline inputs: `high_severity_dq_count`, `total_dq_issue_count`, `days_to_completion`
- Score outputs: `risk_score`, `risk_level`, `risk_reason_summary`
