# Clinical Research Workflow Mapping

RheumTrialOps does not connect to clinical research platforms. I used those platforms only as workflow context so the project could focus on the type of reporting that often surrounds study operations.

For REDCap-style workflows, the project uses synthetic subject records. These records include screening dates, enrollment dates, eligibility status, subject status, study arm, and withdrawal reason. The point is not to recreate REDCap. The point is to show how subject-level operational data can be checked and summarized after capture.

For OnCore or CTMS-style workflows, the project uses study status, target accrual, milestones, delayed milestones, and study-level risk scoring. This gives the dashboard a study tracking view without claiming to reproduce a real CTMS.

For HURON-style research administration workflows, the project uses synthetic grant records. These include sponsor name, funding amount, submission status, award status, JIT required flag, and JIT status. This gives the dashboard a way to show grant and JIT visibility without using real grant administration data.

For investigator reporting, the Streamlit dashboard gives three practical views: portfolio overview, subject accrual and study progress, and grants, milestones, and data quality. These are the kinds of views that can help a team quickly see progress and exceptions.

For data quality oversight, the dbt models and dashboard keep bad records visible instead of hiding them. The project flags issues such as invalid enrollment dates, missing withdrawal reasons, negative funding amounts, invalid JIT status, and completed milestones without actual dates.

The boundary is important: this project does not use real patient data, real UAB data, or direct access to REDCap, OnCore, HURON, PowerTrials, or CTMS systems. It is a synthetic analytics prototype built to show transferable data modeling, validation, workflow monitoring, and reporting skills.
