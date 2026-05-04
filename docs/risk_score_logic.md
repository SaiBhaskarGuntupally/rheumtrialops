# Study Risk Score Logic

`mart_study_risk_score` creates a rule-based operational risk score for dashboard prioritization.

This is a transparent rules-based score for operational review. It does not predict clinical outcomes, trial success, patient risk, or sponsor decisions.

## Score Inputs

| Condition | Points |
| --- | ---: |
| Accrual rate below 0.50 | 40 |
| Accrual rate from 0.50 to below 0.70 | 25 |
| Pending JIT count greater than 0 | 20 |
| Delayed milestone count greater than 0 | 20 |
| High-severity data quality issue count greater than 0 | 20 |
| Total data quality issue count greater than 3 | 10 |
| Completion date within 90 days and accrual rate below 0.80 | 15 |

The final score is capped at 100.

## Risk Levels

| Risk Level | Score Range |
| --- | --- |
| High | `risk_score >= 70` |
| Medium | `risk_score >= 35 and risk_score < 70` |
| Low | `risk_score < 35` |

## Reason Summary

`risk_reason_summary` combines readable reasons for the score:

- Low accrual
- Pending JIT
- Delayed milestones
- High-severity data quality issues
- Completion date approaching

The field supports operational prioritization, dashboard filtering, and study drill-through views.
