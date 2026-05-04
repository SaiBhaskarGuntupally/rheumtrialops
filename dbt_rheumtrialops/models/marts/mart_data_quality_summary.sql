-- One row per failed data quality rule. Intentional bad records remain visible.

with studies as (
    select * from {{ ref('stg_studies') }}
),

subjects as (
    select * from {{ ref('stg_subjects') }}
),

grants as (
    select * from {{ ref('stg_grants') }}
),

milestones as (
    select * from {{ ref('stg_milestones') }}
)

select
    concat('studies-', s.study_id, '-01') as issue_id,
    s.study_id,
    s.protocol_id,
    s.study_title,
    'studies' as source_table,
    s.study_id as record_id,
    'Invalid Study Timeline' as rule_name,
    'High' as issue_severity,
    'Target completion date is before activation date.' as issue_description
from studies s
where s.is_completion_date_invalid

union all

select
    concat('subjects-', subj.subject_id, '-01') as issue_id,
    subj.study_id,
    s.protocol_id,
    s.study_title,
    'subjects' as source_table,
    subj.subject_id as record_id,
    'Invalid Enrollment Timeline' as rule_name,
    'High' as issue_severity,
    'Enrollment date is before screening date.' as issue_description
from subjects subj
left join studies s on subj.study_id = s.study_id
where subj.is_enrollment_date_invalid

union all

select
    concat('subjects-', subj.subject_id, '-02') as issue_id,
    subj.study_id,
    s.protocol_id,
    s.study_title,
    'subjects' as source_table,
    subj.subject_id as record_id,
    'Enrolled Ineligible Subject' as rule_name,
    'High' as issue_severity,
    'Subject is enrolled or active while marked ineligible.' as issue_description
from subjects subj
left join studies s on subj.study_id = s.study_id
where subj.is_enrolled_ineligible

union all

select
    concat('subjects-', subj.subject_id, '-03') as issue_id,
    subj.study_id,
    s.protocol_id,
    s.study_title,
    'subjects' as source_table,
    subj.subject_id as record_id,
    'Missing Withdrawal Reason' as rule_name,
    'Medium' as issue_severity,
    'Withdrawn subject is missing a usable withdrawal reason.' as issue_description
from subjects subj
left join studies s on subj.study_id = s.study_id
where subj.is_withdrawn_missing_reason

union all

select
    concat('grants-', g.grant_id, '-01') as issue_id,
    g.study_id,
    s.protocol_id,
    s.study_title,
    'grants' as source_table,
    g.grant_id as record_id,
    'Invalid Funding Amount' as rule_name,
    'High' as issue_severity,
    'Funding amount is negative.' as issue_description
from grants g
left join studies s on g.study_id = s.study_id
where g.is_funding_amount_invalid

union all

select
    concat('grants-', g.grant_id, '-02') as issue_id,
    g.study_id,
    s.protocol_id,
    s.study_title,
    'grants' as source_table,
    g.grant_id as record_id,
    'Invalid JIT Status' as rule_name,
    'Medium' as issue_severity,
    'JIT is required but the JIT status is missing or marked Not Required.' as issue_description
from grants g
left join studies s on g.study_id = s.study_id
where g.is_jit_status_invalid

union all

select
    concat('milestones-', m.milestone_id, '-01') as issue_id,
    m.study_id,
    s.protocol_id,
    s.study_title,
    'milestones' as source_table,
    m.milestone_id as record_id,
    'Completed Milestone Missing Actual Date' as rule_name,
    'High' as issue_severity,
    'Milestone is completed but actual date is missing.' as issue_description
from milestones m
left join studies s on m.study_id = s.study_id
where m.is_completed_missing_actual_date
