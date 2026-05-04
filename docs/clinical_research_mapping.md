# Clinical Research Workflow Mapping

RheumTrialOps is a synthetic clinical research operations analytics prototype. It demonstrates reporting patterns that can be useful around clinical research workflows without claiming direct integration with research administration or clinical trial platforms.

| Workflow Area | Prototype Mapping | Notes |
| --- | --- | --- |
| REDCap-style data capture | Synthetic subject, screening, enrollment, eligibility, and withdrawal records | Demonstrates how subject-level operational data can be modeled and validated. |
| OnCore/CTMS-style study tracking | Study status, target accrual, milestones, delayed milestones, and risk score | Demonstrates study portfolio and timeline monitoring concepts. |
| HURON-style research administration | Grant submission status, JIT tracking, funding amount, and award status | Demonstrates grant and research administration visibility concepts. |
| Investigator reporting | Streamlit dashboard pages for portfolio, accrual, grants, milestones, quality, and risk | Demonstrates dashboard communication for study teams and operational stakeholders. |
| Data quality oversight | dbt tests, staging validation flags, and `data_quality_summary` issue rows | Demonstrates transparent validation logic and issue drill-through. |

## Important Boundary

The project does not connect to REDCap, OnCore, HURON, PowerTrials, CTMS systems, or any institutional source system. It uses fully synthetic operational data to demonstrate transferable analytics engineering and reporting skills.
