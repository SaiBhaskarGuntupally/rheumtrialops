-- One row per study with operational portfolio, accrual, funding, milestone, and quality metrics.

with studies as (
    select * from {{ ref('stg_studies') }}
),

subject_metrics as (
    select
        study_id,
        count(*) as total_subjects_screened,
        count(*) filter (
            where subject_status in ('Enrolled', 'Active', 'Completed', 'Withdrawn', 'Lost to Follow-Up')
        ) as total_subjects_enrolled,
        count(*) filter (where subject_status = 'Active') as total_subjects_active,
        count(*) filter (where subject_status = 'Completed') as total_subjects_completed,
        count(*) filter (where subject_status = 'Withdrawn') as total_subjects_withdrawn
    from {{ ref('stg_subjects') }}
    group by study_id
),

grant_metrics as (
    select
        study_id,
        count(*) as total_grants,
        sum(funding_amount) as total_funding_amount,
        sum(case when is_awarded then funding_amount else 0 end) as awarded_funding_amount,
        count(*) filter (
            where jit_required = true
              and (jit_status is null or jit_status = '' or jit_status in ('Pending', 'Not Required'))
        ) as pending_jit_count
    from {{ ref('stg_grants') }}
    group by study_id
),

milestone_metrics as (
    select
        study_id,
        count(*) as total_milestones,
        count(*) filter (where is_delayed) as delayed_milestone_count,
        count(*) filter (where milestone_status = 'Completed') as completed_milestone_count
    from {{ ref('stg_milestones') }}
    group by study_id
),

quality_metrics as (
    select
        study_id,
        count(*) as data_quality_issue_count
    from {{ ref('mart_data_quality_summary') }}
    group by study_id
)

select
    s.study_id,
    s.nct_id,
    s.protocol_id,
    s.study_title,
    s.principal_investigator,
    s.condition_area,
    s.study_type,
    s.study_status,
    s.intervention_type,
    s.target_accrual,
    s.activation_date,
    s.target_completion_date,
    s.study_duration_days,
    s.is_active_study,
    coalesce(sm.total_subjects_screened, 0) as total_subjects_screened,
    coalesce(sm.total_subjects_enrolled, 0) as total_subjects_enrolled,
    coalesce(sm.total_subjects_active, 0) as total_subjects_active,
    coalesce(sm.total_subjects_completed, 0) as total_subjects_completed,
    coalesce(sm.total_subjects_withdrawn, 0) as total_subjects_withdrawn,
    round(coalesce(sm.total_subjects_enrolled, 0)::numeric / nullif(s.target_accrual, 0), 4) as accrual_rate,
    coalesce(gm.total_grants, 0) as total_grants,
    coalesce(gm.total_funding_amount, 0) as total_funding_amount,
    coalesce(gm.awarded_funding_amount, 0) as awarded_funding_amount,
    coalesce(gm.pending_jit_count, 0) as pending_jit_count,
    coalesce(mm.total_milestones, 0) as total_milestones,
    coalesce(mm.delayed_milestone_count, 0) as delayed_milestone_count,
    coalesce(mm.completed_milestone_count, 0) as completed_milestone_count,
    coalesce(qm.data_quality_issue_count, 0) as data_quality_issue_count
from studies s
left join subject_metrics sm on s.study_id = sm.study_id
left join grant_metrics gm on s.study_id = gm.study_id
left join milestone_metrics mm on s.study_id = mm.study_id
left join quality_metrics qm on s.study_id = qm.study_id
