with source as (
    select * from raw.studies
)

select
    trim(study_id) as study_id,
    trim(nct_id) as nct_id,
    trim(protocol_id) as protocol_id,
    trim(study_title) as study_title,
    trim(principal_investigator) as principal_investigator,
    trim(condition_area) as condition_area,
    trim(study_type) as study_type,
    trim(study_status) as study_status,
    trim(intervention_type) as intervention_type,
    target_accrual::integer as target_accrual,
    activation_date::date as activation_date,
    target_completion_date::date as target_completion_date,
    (target_completion_date::date - activation_date::date) as study_duration_days,
    (target_completion_date::date < activation_date::date) as is_completion_date_invalid,
    trim(study_status) in ('Active', 'Pending Activation', 'Closed to Accrual') as is_active_study
from source
