-- Monthly subject accrual by study and study arm. Invalid records are grouped and flagged, not removed.

with subjects as (
    select * from {{ ref('stg_subjects') }}
),

studies as (
    select * from {{ ref('stg_studies') }}
)

select
    s.study_id,
    st.protocol_id,
    st.study_title,
    st.condition_area,
    st.intervention_type,
    date_trunc('month', coalesce(s.enrollment_date, s.screening_date))::date as enrollment_month,
    s.study_arm,
    count(*) as screened_count,
    count(*) filter (
        where s.subject_status in ('Enrolled', 'Active', 'Completed', 'Withdrawn', 'Lost to Follow-Up')
    ) as enrolled_count,
    count(*) filter (where s.subject_status = 'Active') as active_count,
    count(*) filter (where s.subject_status = 'Completed') as completed_count,
    count(*) filter (where s.subject_status = 'Withdrawn') as withdrawn_count,
    count(*) filter (where s.eligibility_status = 'Ineligible') as ineligible_count,
    count(*) filter (where s.is_enrollment_date_invalid) as invalid_enrollment_date_count,
    count(*) filter (where s.is_enrolled_ineligible) as enrolled_ineligible_count,
    count(*) filter (where s.is_withdrawn_missing_reason) as withdrawn_missing_reason_count
from subjects s
left join studies st on s.study_id = st.study_id
group by
    s.study_id,
    st.protocol_id,
    st.study_title,
    st.condition_area,
    st.intervention_type,
    date_trunc('month', coalesce(s.enrollment_date, s.screening_date))::date,
    s.study_arm
