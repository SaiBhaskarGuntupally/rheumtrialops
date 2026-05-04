-- Milestone tracking with delay and missing completion date risk labels.

with milestones as (
    select * from {{ ref('stg_milestones') }}
),

studies as (
    select * from {{ ref('stg_studies') }}
)

select
    m.milestone_id,
    m.study_id,
    s.protocol_id,
    s.study_title,
    m.milestone_type,
    m.planned_date,
    m.actual_date,
    m.milestone_status,
    m.days_delayed,
    m.is_completed_missing_actual_date,
    m.is_delayed,
    case
        when m.is_completed_missing_actual_date then 'High'
        when m.days_delayed >= 30 then 'High'
        when m.days_delayed between 1 and 29 then 'Medium'
        when m.milestone_status = 'Delayed' then 'Medium'
        else 'Low'
    end as milestone_risk_level
from milestones m
left join studies s on m.study_id = s.study_id
