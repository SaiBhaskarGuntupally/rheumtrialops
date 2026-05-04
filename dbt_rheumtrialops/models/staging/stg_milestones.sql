with source as (
    select * from raw.milestones
)

select
    trim(milestone_id) as milestone_id,
    trim(study_id) as study_id,
    trim(milestone_type) as milestone_type,
    planned_date::date as planned_date,
    actual_date::date as actual_date,
    trim(milestone_status) as milestone_status,
    days_delayed::integer as days_delayed,
    (
        trim(milestone_status) = 'Completed'
        and actual_date is null
    ) as is_completed_missing_actual_date,
    (
        trim(milestone_status) = 'Delayed'
        or coalesce(days_delayed, 0) > 0
    ) as is_delayed,
    (actual_date::date - planned_date::date) as days_from_planned_to_actual
from source
