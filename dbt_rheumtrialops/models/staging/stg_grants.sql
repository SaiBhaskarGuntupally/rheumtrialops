with source as (
    select * from raw.grants
)

select
    trim(grant_id) as grant_id,
    trim(study_id) as study_id,
    trim(sponsor_name) as sponsor_name,
    funding_amount::numeric as funding_amount,
    submission_date::date as submission_date,
    trim(submission_status) as submission_status,
    jit_required::boolean as jit_required,
    nullif(trim(jit_status), '') as jit_status,
    trim(award_status) as award_status,
    (funding_amount::numeric < 0) as is_funding_amount_invalid,
    (
        jit_required = true
        and (
            jit_status is null
            or trim(jit_status) = ''
            or trim(jit_status) = 'Not Required'
        )
    ) as is_jit_status_invalid,
    trim(award_status) = 'Awarded' as is_awarded
from source
