with source as (
    select * from raw.subjects
)

select
    trim(subject_id) as subject_id,
    trim(study_id) as study_id,
    screening_date::date as screening_date,
    enrollment_date::date as enrollment_date,
    trim(study_arm) as study_arm,
    trim(subject_status) as subject_status,
    trim(eligibility_status) as eligibility_status,
    nullif(trim(withdrawal_reason), '') as withdrawal_reason,
    (enrollment_date::date < screening_date::date) as is_enrollment_date_invalid,
    (
        trim(subject_status) in ('Enrolled', 'Active')
        and trim(eligibility_status) = 'Ineligible'
    ) as is_enrolled_ineligible,
    (
        trim(subject_status) = 'Withdrawn'
        and (
            withdrawal_reason is null
            or trim(withdrawal_reason) = ''
            or trim(withdrawal_reason) = 'None'
        )
    ) as is_withdrawn_missing_reason
from source
