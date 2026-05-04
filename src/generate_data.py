"""Generate synthetic RheumTrialOps source CSV data.

This script creates only synthetic operational research records for a
rheumatology-focused analytics prototype. It does not use real patient data,
real institutional data, or live source-system access.
"""

from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from faker import Faker
except ImportError:  # pragma: no cover - exercised only when Faker is absent
    Faker = None


SEED = 42
ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "data" / "raw"

random.seed(SEED)
np.random.seed(SEED)
fake = Faker() if Faker else None
if fake:
    Faker.seed(SEED)


CONDITION_AREAS = [
    "rheumatoid arthritis",
    "gout",
    "osteoporosis",
    "lupus",
    "inflammatory arthritis",
    "telemedicine follow-up",
    "technology-enabled care delivery",
    "infection prevention",
    "polypharmacy monitoring",
    "chronic inflammatory disease",
]

STUDY_THEMES = [
    "Remote Monitoring for {condition}",
    "Care Coordination in {condition}",
    "Medication Safety for {condition}",
    "Patient Education Strategies for {condition}",
    "Digital Workflow for {condition}",
    "Telemedicine Follow-Up in {condition}",
    "Comparative Effectiveness in {condition}",
    "Infection Prevention Among Patients With {condition}",
    "Polypharmacy Monitoring for {condition}",
    "Pragmatic Care Delivery for {condition}",
]

PI_FIRST_NAMES = [
    "Avery",
    "Jordan",
    "Morgan",
    "Taylor",
    "Riley",
    "Casey",
    "Parker",
    "Quinn",
    "Reese",
    "Drew",
]
PI_LAST_NAMES = [
    "Mitchell",
    "Patel",
    "Nguyen",
    "Robinson",
    "Carter",
    "Garcia",
    "Bennett",
    "Kim",
    "Morgan",
    "Davis",
]


def random_date(start: date, end: date) -> date:
    """Return a random date between start and end, inclusive."""
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def format_date(value: date | pd.Timestamp | None) -> str | None:
    """Format dates for CSV export as YYYY-MM-DD."""
    if value is None or pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        value = value.date()
    return value.isoformat()


def maybe_pi_name() -> str:
    if fake:
        return fake.name()
    return f"{random.choice(PI_FIRST_NAMES)} {random.choice(PI_LAST_NAMES)}"


def make_study_title(condition: str) -> str:
    return random.choice(STUDY_THEMES).format(condition=condition.title())


def generate_studies() -> tuple[pd.DataFrame, list[dict[str, object]]]:
    """Studies describe synthetic protocol-level portfolio metadata."""
    statuses = ["Active", "Completed", "Pending Activation", "Suspended", "Closed to Accrual"]
    study_types = ["Interventional", "Observational", "Registry", "Pragmatic Trial"]
    intervention_types = [
        "Telemedicine",
        "In-Person Care",
        "Digital Workflow",
        "Medication Management",
        "Care Coordination",
        "Patient Education",
    ]
    bad_count = random.randint(3, 5)
    bad_indexes = set(random.sample(range(100), bad_count))
    rows = []

    for index in range(100):
        activation = random_date(date(2022, 1, 1), date(2025, 12, 31))
        if index in bad_indexes:
            completion = activation - timedelta(days=random.randint(15, 180))
        else:
            completion = activation + timedelta(days=random.randint(180, 900))

        year = random.randint(2022, 2025)
        condition = random.choice(CONDITION_AREAS)
        rows.append(
            {
                "study_id": f"STUDY{index + 1:03d}",
                "nct_id": f"NCT{random.randint(0, 99999999):08d}",
                "protocol_id": f"RHEUM-{year}-{index + 1:03d}",
                "study_title": make_study_title(condition),
                "principal_investigator": maybe_pi_name(),
                "condition_area": condition,
                "study_type": random.choice(study_types),
                "study_status": random.choice(statuses),
                "intervention_type": random.choice(intervention_types),
                "target_accrual": random.randint(40, 300),
                "activation_date": activation,
                "target_completion_date": completion,
            }
        )

    return pd.DataFrame(rows), [
        {
            "table_name": "studies",
            "row_count": 100,
            "intentional_bad_record_type": "target_completion_date before activation_date",
            "intentional_bad_record_count": bad_count,
        }
    ]


def generate_subjects(studies: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, object]]]:
    """Subjects contain synthetic screening, enrollment, and disposition data."""
    study_activations = dict(zip(studies["study_id"], studies["activation_date"]))
    study_arms = ["Telemedicine", "In-Person", "Standard Care", "Enhanced Care", "Digital Review", "Control"]
    statuses = ["Screened", "Enrolled", "Active", "Completed", "Withdrawn", "Lost to Follow-Up"]
    eligibility = ["Eligible", "Ineligible", "Pending Review"]
    withdrawal_reasons = [
        "Adverse Event",
        "Lost Contact",
        "Patient Choice",
        "Protocol Deviation",
        "Transportation Barrier",
        "None",
    ]

    bad_enrollment_count = random.randint(10, 15)
    bad_enrollment_indexes = set(random.sample(range(500), bad_enrollment_count))
    remaining = [idx for idx in range(500) if idx not in bad_enrollment_indexes]
    missing_withdrawal_indexes = set(random.sample(remaining, 10))
    remaining = [idx for idx in remaining if idx not in missing_withdrawal_indexes]
    ineligible_enrolled_indexes = set(random.sample(remaining, 8))

    rows = []
    study_ids = list(studies["study_id"])
    for index in range(500):
        study_id = random.choice(study_ids)
        activation = study_activations[study_id]
        screening = activation + timedelta(days=random.randint(1, 540))
        if index in bad_enrollment_indexes:
            enrollment = screening - timedelta(days=random.randint(1, 45))
        else:
            enrollment = screening + timedelta(days=random.randint(0, 45))

        subject_status = random.choice(statuses)
        eligibility_status = random.choice(eligibility)
        withdrawal_reason = "None"

        if subject_status == "Withdrawn":
            withdrawal_reason = random.choice(withdrawal_reasons[:-1])
        elif random.random() < 0.08:
            withdrawal_reason = random.choice(withdrawal_reasons)

        if index in missing_withdrawal_indexes:
            subject_status = "Withdrawn"
            withdrawal_reason = None

        if index in ineligible_enrolled_indexes:
            subject_status = "Enrolled"
            eligibility_status = "Ineligible"
        elif subject_status == "Enrolled" and eligibility_status == "Ineligible":
            eligibility_status = random.choice(["Eligible", "Pending Review"])

        rows.append(
            {
                "subject_id": f"SUBJ{index + 1:04d}",
                "study_id": study_id,
                "screening_date": screening,
                "enrollment_date": enrollment,
                "study_arm": random.choice(study_arms),
                "subject_status": subject_status,
                "eligibility_status": eligibility_status,
                "withdrawal_reason": withdrawal_reason,
            }
        )

    return pd.DataFrame(rows), [
        {
            "table_name": "subjects",
            "row_count": 500,
            "intentional_bad_record_type": "enrollment_date before screening_date",
            "intentional_bad_record_count": bad_enrollment_count,
        },
        {
            "table_name": "subjects",
            "row_count": 500,
            "intentional_bad_record_type": "withdrawn subject missing withdrawal_reason",
            "intentional_bad_record_count": 10,
        },
        {
            "table_name": "subjects",
            "row_count": 500,
            "intentional_bad_record_type": "enrolled subject marked Ineligible",
            "intentional_bad_record_count": 8,
        },
    ]


def generate_grants(studies: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, object]]]:
    """Grants represent synthetic submissions, JIT activity, and award outcomes."""
    sponsors = [
        "NIH",
        "Rheumatology Research Foundation",
        "American College of Rheumatology",
        "PCORI",
        "VA Research",
        "Internal Pilot Funding",
        "Foundation Award",
    ]
    submission_statuses = ["Draft", "Submitted", "Under Review", "JIT Requested", "Awarded", "Not Funded"]
    jit_statuses = ["Not Required", "Pending", "Submitted", "Complete"]
    award_statuses = ["Pending", "Awarded", "Not Funded"]

    negative_funding_count = random.randint(5, 8)
    bad_jit_count = random.randint(8, 12)
    negative_indexes = set(random.sample(range(60), negative_funding_count))
    remaining = [idx for idx in range(60) if idx not in negative_indexes]
    bad_jit_indexes = set(random.sample(remaining, bad_jit_count))

    rows = []
    study_ids = list(studies["study_id"])
    for index in range(60):
        amount = random.randint(25_000, 1_500_000)
        if index in negative_indexes:
            amount = -random.randint(1_000, 250_000)

        jit_required = random.choice([True, False])
        jit_status = random.choice(jit_statuses)
        submission_status = random.choice(submission_statuses)
        if jit_required:
            jit_status = random.choice(["Pending", "Submitted", "Complete"])
        else:
            jit_status = "Not Required"
        if index in bad_jit_indexes:
            jit_required = True
            jit_status = random.choice([None, "Not Required"])
            submission_status = random.choice(["JIT Requested", "Under Review", "Submitted"])

        rows.append(
            {
                "grant_id": f"GRANT{index + 1:03d}",
                "study_id": random.choice(study_ids),
                "sponsor_name": random.choice(sponsors),
                "funding_amount": amount,
                "submission_date": random_date(date(2021, 1, 1), date(2026, 4, 30)),
                "submission_status": submission_status,
                "jit_required": jit_required,
                "jit_status": jit_status,
                "award_status": random.choice(award_statuses),
            }
        )

    return pd.DataFrame(rows), [
        {
            "table_name": "grants",
            "row_count": 60,
            "intentional_bad_record_type": "negative funding_amount",
            "intentional_bad_record_count": negative_funding_count,
        },
        {
            "table_name": "grants",
            "row_count": 60,
            "intentional_bad_record_type": "jit_required True with missing or Not Required jit_status",
            "intentional_bad_record_count": bad_jit_count,
        },
    ]


def generate_milestones(studies: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, object]]]:
    """Milestones track synthetic protocol operations dates and delays."""
    milestone_types = [
        "IRB Submission",
        "IRB Approval",
        "Study Activation",
        "First Subject Enrolled",
        "Enrollment Target 50%",
        "JIT Submission",
        "Data Lock",
        "Final Report",
    ]
    statuses = ["Not Started", "In Progress", "Completed", "Delayed"]
    missing_completed_count = random.randint(8, 12)
    missing_completed_indexes = set(random.sample(range(150), missing_completed_count))

    rows = []
    study_ids = list(studies["study_id"])
    for index in range(150):
        planned = random_date(date(2022, 1, 1), date(2026, 12, 31))
        status = random.choice(statuses)
        actual = None

        if status == "Completed":
            actual = planned + timedelta(days=random.randint(-30, 90))
        elif status == "Delayed":
            actual = planned + timedelta(days=random.randint(1, 180))
        elif random.random() < 0.15:
            actual = planned + timedelta(days=random.randint(-15, 45))

        if index in missing_completed_indexes:
            status = "Completed"
            actual = None

        days_delayed = None
        if actual is not None:
            days_delayed = (actual - planned).days

        rows.append(
            {
                "milestone_id": f"MILE{index + 1:03d}",
                "study_id": random.choice(study_ids),
                "milestone_type": random.choice(milestone_types),
                "planned_date": planned,
                "actual_date": actual,
                "milestone_status": status,
                "days_delayed": days_delayed,
            }
        )

    return pd.DataFrame(rows), [
        {
            "table_name": "milestones",
            "row_count": 150,
            "intentional_bad_record_type": "Completed milestone missing actual_date",
            "intentional_bad_record_count": missing_completed_count,
        },
        {
            "table_name": "milestones",
            "row_count": 150,
            "intentional_bad_record_type": "Delayed milestone with positive days_delayed",
            "intentional_bad_record_count": int((pd.DataFrame(rows)["days_delayed"] > 0).sum()),
        },
    ]


def write_csv(df: pd.DataFrame, filename: str) -> None:
    date_columns = [column for column in df.columns if column.endswith("_date")]
    export_df = df.copy()
    for column in date_columns:
        export_df[column] = export_df[column].apply(format_date)

    output_path = RAW_DIR / filename
    export_df.to_csv(output_path, index=False)
    print(f"Generated {output_path} ({len(export_df)} rows)")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    studies, studies_summary = generate_studies()
    subjects, subjects_summary = generate_subjects(studies)
    grants, grants_summary = generate_grants(studies)
    milestones, milestones_summary = generate_milestones(studies)

    write_csv(studies, "studies.csv")
    write_csv(subjects, "subjects.csv")
    write_csv(grants, "grants.csv")
    write_csv(milestones, "milestones.csv")

    summary = pd.DataFrame(
        studies_summary
        + subjects_summary
        + grants_summary
        + milestones_summary
    )
    output_path = RAW_DIR / "data_generation_summary.csv"
    summary.to_csv(output_path, index=False)
    print(f"Generated {output_path} ({len(summary)} rows)")
    print("Synthetic RheumTrialOps data generation complete.")


if __name__ == "__main__":
    main()
