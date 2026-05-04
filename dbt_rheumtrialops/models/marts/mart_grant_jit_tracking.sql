-- Grant, award, and JIT tracking with operational status labels.

with grants as (
    select * from {{ ref('stg_grants') }}
),

studies as (
    select * from {{ ref('stg_studies') }}
)

select
    g.grant_id,
    g.study_id,
    s.protocol_id,
    s.study_title,
    g.sponsor_name,
    g.funding_amount,
    g.submission_date,
    g.submission_status,
    g.jit_required,
    g.jit_status,
    g.award_status,
    g.is_awarded,
    g.is_funding_amount_invalid,
    g.is_jit_status_invalid,
    case
        when g.is_awarded then 'Awarded'
        when g.jit_required = true
          and (g.jit_status is null or g.jit_status = '' or g.jit_status in ('Pending', 'Not Required'))
            then 'JIT Pending'
        when g.submission_status in ('Under Review', 'Submitted', 'JIT Requested') then 'Under Review'
        when g.award_status = 'Not Funded' then 'Not Funded'
        else 'Other'
    end as grant_operational_status
from grants g
left join studies s on g.study_id = s.study_id
