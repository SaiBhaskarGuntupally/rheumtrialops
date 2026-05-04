-- Rule-based operational risk score for dashboard prioritization.

with portfolio as (
    select * from {{ ref('mart_research_portfolio_summary') }}
),

quality as (
    select
        study_id,
        count(*) filter (where issue_severity = 'High') as high_severity_dq_count,
        count(*) as total_dq_issue_count
    from {{ ref('mart_data_quality_summary') }}
    group by study_id
),

score_inputs as (
    select
        p.study_id,
        p.protocol_id,
        p.study_title,
        p.condition_area,
        p.study_status,
        p.target_accrual,
        p.total_subjects_enrolled,
        coalesce(p.accrual_rate, 0) as accrual_rate,
        p.pending_jit_count,
        p.delayed_milestone_count,
        coalesce(q.high_severity_dq_count, 0) as high_severity_dq_count,
        coalesce(q.total_dq_issue_count, 0) as total_dq_issue_count,
        (p.target_completion_date - current_date) as days_to_completion
    from portfolio p
    left join quality q on p.study_id = q.study_id
),

scored as (
    select
        *,
        least(
            100,
            case
                when accrual_rate < 0.50 then 40
                when accrual_rate >= 0.50 and accrual_rate < 0.70 then 25
                else 0
            end
            + case when pending_jit_count > 0 then 20 else 0 end
            + case when delayed_milestone_count > 0 then 20 else 0 end
            + case when high_severity_dq_count > 0 then 20 else 0 end
            + case when total_dq_issue_count > 3 then 10 else 0 end
            + case when days_to_completion <= 90 and accrual_rate < 0.80 then 15 else 0 end
        ) as risk_score
    from score_inputs
)

select
    study_id,
    protocol_id,
    study_title,
    condition_area,
    study_status,
    target_accrual,
    total_subjects_enrolled,
    accrual_rate,
    pending_jit_count,
    delayed_milestone_count,
    high_severity_dq_count,
    total_dq_issue_count,
    days_to_completion,
    risk_score,
    case
        when risk_score >= 70 then 'High'
        when risk_score >= 35 and risk_score < 70 then 'Medium'
        else 'Low'
    end as risk_level,
    concat_ws(
        '; ',
        case when accrual_rate < 0.70 then 'Low accrual' end,
        case when pending_jit_count > 0 then 'Pending JIT' end,
        case when delayed_milestone_count > 0 then 'Delayed milestones' end,
        case when high_severity_dq_count > 0 then 'High-severity data quality issues' end,
        case when days_to_completion <= 90 and accrual_rate < 0.80 then 'Completion date approaching' end
    ) as risk_reason_summary
from scored
