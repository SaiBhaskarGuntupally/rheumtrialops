from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


APP_ROOT = Path(__file__).resolve().parent
DATA_DIR = APP_ROOT / "outputs" / "streamlit"

DATA_FILES = {
    "portfolio": "research_portfolio_summary.csv",
    "accrual": "subject_accrual.csv",
    "grants": "grant_jit_tracking.csv",
    "milestones": "milestone_delay_summary.csv",
    "quality": "data_quality_summary.csv",
    "risk": "study_risk_score.csv",
}

COLORS = {
    "active_primary": "#2E86AB",
    "completed": "#A8DADC",
    "at_risk_high": "#E63946",
    "pending_medium": "#F4A261",
    "low_risk_good": "#57CC99",
    "suspended_neutral": "#C9C9C9",
    "target_benchmark": "#C9C9C9",
    "digital_workflow": "#7209B7",
    "background": "#F8F9FA",
    "card": "#FFFFFF",
    "high_row": "#FFE5E5",
    "medium_row": "#FFF3E0",
}

RISK_COLOR_MAP = {
    "High": COLORS["at_risk_high"],
    "Medium": COLORS["pending_medium"],
    "Low": COLORS["low_risk_good"],
}

STATUS_COLOR_MAP = {
    "Active": COLORS["active_primary"],
    "Completed": COLORS["completed"],
    "Pending Activation": COLORS["pending_medium"],
    "Suspended": COLORS["suspended_neutral"],
    "Closed to Accrual": COLORS["low_risk_good"],
}

GRANT_STATUS_COLOR_MAP = {
    "Awarded": COLORS["low_risk_good"],
    "JIT Pending": COLORS["pending_medium"],
    "Under Review": COLORS["active_primary"],
    "Not Funded": COLORS["at_risk_high"],
    "Other": COLORS["suspended_neutral"],
}

SUBJECT_STATUS_COLOR_MAP = {
    "Active": COLORS["active_primary"],
    "Completed": COLORS["completed"],
    "Withdrawn": COLORS["pending_medium"],
    "Ineligible": COLORS["at_risk_high"],
}

SEVERITY_COLOR_MAP = {
    "High": COLORS["at_risk_high"],
    "Medium": COLORS["pending_medium"],
    "Low": COLORS["suspended_neutral"],
}

DISCLAIMER = (
    "This project does not use real patient data, real UAB data, or direct access to "
    "REDCap, OnCore, HURON, PowerTrials, or CTMS systems. It uses public or synthetic "
    "study metadata and fully synthetic operational data to demonstrate transferable "
    "data modeling, validation, workflow monitoring, and reporting skills for clinical "
    "research operations."
)


st.set_page_config(
    page_title="RheumTrialOps",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {COLORS["background"]};
    }}
    section[data-testid="stSidebar"] {{
        background-color: #FFFFFF;
    }}
    .metric-card {{
        background: {COLORS["card"]};
        border-radius: 8px;
        border-left: 4px solid {COLORS["active_primary"]};
        padding: 0.85rem 0.95rem;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.06);
        min-height: 86px;
    }}
    .metric-card.high {{
        border-left-color: {COLORS["at_risk_high"]};
    }}
    .metric-card.pending {{
        border-left-color: {COLORS["pending_medium"]};
    }}
    .metric-label {{
        color: #536471;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }}
    .metric-value {{
        color: #111827;
        font-size: 1.55rem;
        font-weight: 700;
        line-height: 1.15;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_csvs() -> dict[str, pd.DataFrame]:
    missing = [
        file_name
        for file_name in DATA_FILES.values()
        if not (DATA_DIR / file_name).exists()
    ]
    if missing:
        missing_list = "\n".join(f"- outputs/streamlit/{name}" for name in missing)
        st.error(
            "The dashboard cannot load because these exported mart CSV files are missing:\n\n"
            f"{missing_list}\n\nRun `python src/export_marts_to_csv.py` after `dbt run`."
        )
        st.stop()

    data = {}
    for key, file_name in DATA_FILES.items():
        data[key] = pd.read_csv(DATA_DIR / file_name)

    for df in data.values():
        for column in df.columns:
            if column.endswith("_date") or column.endswith("_month"):
                df[column] = pd.to_datetime(df[column], errors="coerce")

    return data


def has_columns(df: pd.DataFrame, columns: Iterable[str]) -> bool:
    return all(column in df.columns for column in columns)


def safe_sum(df: pd.DataFrame, column: str) -> float:
    if column not in df.columns or df.empty:
        return 0
    return pd.to_numeric(df[column], errors="coerce").fillna(0).sum()


def safe_mean(df: pd.DataFrame, column: str) -> float:
    if column not in df.columns or df.empty:
        return 0
    values = pd.to_numeric(df[column], errors="coerce").dropna()
    return float(values.mean()) if not values.empty else 0


def money(value: float) -> str:
    return f"${value:,.0f}"


def pct(value: float) -> str:
    return f"{value:.1%}"


def metric_card(label: str, value: str | int | float, variant: str = "primary") -> None:
    variant_class = variant if variant in {"high", "pending"} else ""
    st.markdown(
        f"""
        <div class="metric-card {variant_class}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def truncate_label(value: object, max_length: int = 25) -> str:
    text = "" if pd.isna(value) else str(value)
    return text if len(text) <= max_length else f"{text[: max_length - 3]}..."


def condition_category(condition_area: object) -> str:
    text = str(condition_area).lower()
    if "digital" in text or "technology" in text:
        return "Digital Workflow"
    if "telemedicine" in text:
        return "Telemedicine"
    if "gout" in text:
        return "Gout"
    if "rheumatoid" in text or "arthritis" in text or "lupus" in text:
        return "Rheumatology/Inflammatory"
    if "osteoporosis" in text or "metabolic" in text:
        return "Metabolic"
    return "Other"


def actual_accrual_category(accrual_rate: object) -> str:
    rate = pd.to_numeric(pd.Series([accrual_rate]), errors="coerce").fillna(0).iloc[0]
    if rate < 0.5:
        return "Actual Enrollment <50%"
    if rate <= 0.8:
        return "Actual Enrollment 50-80%"
    return "Actual Enrollment >80%"


def apply_plotly_style(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        font=dict(family="Inter, sans-serif", size=12),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(t=40, b=40, l=20, r=20),
        legend_title_text="",
    )
    return fig


def risk_row_style(row: pd.Series) -> list[str]:
    risk_level = row.get("risk_level", "")
    if risk_level == "High":
        return [f"background-color: {COLORS['high_row']}"] * len(row)
    if risk_level == "Medium":
        return [f"background-color: {COLORS['medium_row']}"] * len(row)
    return [""] * len(row)


def severity_row_style(row: pd.Series) -> list[str]:
    severity = row.get("issue_severity", "")
    if severity == "High":
        return [f"background-color: {COLORS['high_row']}"] * len(row)
    if severity == "Medium":
        return [f"background-color: {COLORS['medium_row']}"] * len(row)
    return [""] * len(row)


def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
    orientation: str = "v",
    color_discrete_map: dict[str, str] | None = None,
) -> None:
    if df.empty or not has_columns(df, [x, y]):
        st.info(f"Not enough data to show {title.lower()}.")
        return
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        orientation=orientation,
        color_discrete_map=color_discrete_map,
    )
    if color is None:
        fig.update_traces(marker_color=COLORS["active_primary"])
    fig.update_xaxes(tickangle=0)
    apply_plotly_style(fig)
    st.plotly_chart(fig, width="stretch")


def pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str,
    color_discrete_map: dict[str, str] | None = None,
) -> None:
    if df.empty or not has_columns(df, [names, values]):
        st.info(f"Not enough data to show {title.lower()}.")
        return
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        hole=0.45,
        color=names,
        color_discrete_map=color_discrete_map,
    )
    apply_plotly_style(fig)
    st.plotly_chart(fig, width="stretch")


def filter_by_studies(df: pd.DataFrame, selected_studies: set[str]) -> pd.DataFrame:
    if "study_id" not in df.columns or not selected_studies:
        return df.iloc[0:0] if "study_id" in df.columns else df
    return df[df["study_id"].isin(selected_studies)].copy()


def sidebar_filters(portfolio: pd.DataFrame, risk: pd.DataFrame) -> tuple[dict[str, list[str]], set[str]]:
    st.sidebar.header("Filters")

    merged = portfolio.copy()
    if has_columns(risk, ["study_id", "risk_level"]):
        merged = merged.merge(risk[["study_id", "risk_level"]], on="study_id", how="left")
    elif "risk_level" not in merged.columns:
        merged["risk_level"] = "Unknown"

    filter_columns = {
        "condition_area": "Condition Area",
        "study_status": "Study Status",
        "intervention_type": "Intervention Type",
        "risk_level": "Risk Level",
    }

    selections: dict[str, list[str]] = {}
    filtered = merged.copy()
    for column, label in filter_columns.items():
        if column not in merged.columns:
            selections[column] = []
            continue
        options = sorted(value for value in merged[column].dropna().unique())
        default = options
        selections[column] = st.sidebar.multiselect(label, options, default=default)
        if selections[column]:
            filtered = filtered[filtered[column].isin(selections[column])]
        else:
            filtered = filtered.iloc[0:0]

    st.sidebar.divider()
    st.sidebar.caption(DISCLAIMER)
    return selections, set(filtered["study_id"]) if "study_id" in filtered.columns else set()


def studies_with_risk(portfolio: pd.DataFrame, risk: pd.DataFrame) -> pd.DataFrame:
    if has_columns(risk, ["study_id", "risk_score", "risk_level", "risk_reason_summary"]):
        return portfolio.merge(
            risk[["study_id", "risk_score", "risk_level", "risk_reason_summary"]],
            on="study_id",
            how="left",
        )
    return portfolio.copy()


def page_portfolio(portfolio: pd.DataFrame, grants: pd.DataFrame, milestones: pd.DataFrame, quality: pd.DataFrame, risk: pd.DataFrame) -> None:
    st.header("Research Portfolio Overview")
    portfolio_risk = studies_with_risk(portfolio, risk)

    kpi_cols = st.columns(7)
    with kpi_cols[0]:
        metric_card("Total studies", len(portfolio))
    with kpi_cols[1]:
        metric_card("Active studies", int(safe_sum(portfolio, "is_active_study")))
    with kpi_cols[2]:
        metric_card("Enrolled subjects", f"{int(safe_sum(portfolio, 'total_subjects_enrolled')):,}")
    with kpi_cols[3]:
        metric_card("Funding tracked", money(safe_sum(portfolio, "total_funding_amount")))
    with kpi_cols[4]:
        high_risk = int((risk.get("risk_level", pd.Series(dtype=str)) == "High").sum()) if not risk.empty else 0
        metric_card("High-risk studies", high_risk, variant="high")
    with kpi_cols[5]:
        metric_card("Pending JIT items", int(safe_sum(portfolio, "pending_jit_count")), variant="pending")
    with kpi_cols[6]:
        metric_card("Delayed milestones", int(safe_sum(portfolio, "delayed_milestone_count")))

    left, right = st.columns(2)
    with left:
        if "condition_area" in portfolio.columns:
            condition_counts = portfolio["condition_area"].value_counts().reset_index()
            condition_counts.columns = ["condition_area", "study_count"]
            condition_counts["clinical_category"] = condition_counts["condition_area"].apply(condition_category)
            condition_color_map = {
                "Gout": COLORS["at_risk_high"],
                "Rheumatology/Inflammatory": COLORS["pending_medium"],
                "Telemedicine": COLORS["active_primary"],
                "Digital Workflow": COLORS["digital_workflow"],
                "Metabolic": COLORS["low_risk_good"],
                "Other": COLORS["suspended_neutral"],
            }
            bar_chart(
                condition_counts,
                "condition_area",
                "study_count",
                "Studies by Condition Area",
                color="clinical_category",
                color_discrete_map=condition_color_map,
            )
        if "sponsor_name" in grants.columns:
            sponsor_funding = grants.groupby("sponsor_name", as_index=False)["funding_amount"].sum()
            bar_chart(sponsor_funding, "sponsor_name", "funding_amount", "Funding by Sponsor")
    with right:
        if "study_status" in portfolio.columns:
            status_counts = portfolio["study_status"].value_counts().reset_index()
            status_counts.columns = ["study_status", "study_count"]
            pie_chart(status_counts, "study_status", "study_count", "Studies by Study Status", STATUS_COLOR_MAP)
        if "risk_level" in risk.columns:
            risk_counts = risk["risk_level"].value_counts().reset_index()
            risk_counts.columns = ["risk_level", "study_count"]
            pie_chart(risk_counts, "risk_level", "study_count", "Risk Level Distribution", RISK_COLOR_MAP)

    if has_columns(portfolio_risk, ["study_title", "risk_score"]):
        top_risk = portfolio_risk.sort_values("risk_score", ascending=False).head(10)
        top_risk = top_risk.copy()
        top_risk["study_title_short"] = top_risk["study_title"].apply(truncate_label)
        bar_chart(top_risk, "risk_score", "study_title_short", "Top 10 Studies by Risk Score", orientation="h")

    st.subheader("Operational Takeaway")
    largest_condition = "not available"
    if "condition_area" in portfolio.columns and not portfolio.empty:
        largest_condition = portfolio["condition_area"].value_counts().idxmax()
    high_risk_count = int((risk.get("risk_level", pd.Series(dtype=str)) == "High").sum()) if not risk.empty else 0
    pending_jit = int(safe_sum(portfolio, "pending_jit_count"))
    dq_count = len(quality)
    st.write(
        f"The filtered portfolio includes **{high_risk_count} high-risk studies**. "
        f"The largest condition area is **{largest_condition}**. "
        f"There are **{pending_jit} pending JIT items** and **{dq_count} data quality issues** visible for review."
    )


def page_accrual(portfolio: pd.DataFrame, accrual: pd.DataFrame, risk: pd.DataFrame) -> None:
    st.header("Subject Accrual & Study Progress")
    portfolio_risk = studies_with_risk(portfolio, risk)

    kpi_cols = st.columns(6)
    with kpi_cols[0]:
        metric_card("Screened subjects", f"{int(safe_sum(portfolio, 'total_subjects_screened')):,}")
    with kpi_cols[1]:
        metric_card("Enrolled subjects", f"{int(safe_sum(portfolio, 'total_subjects_enrolled')):,}")
    with kpi_cols[2]:
        metric_card("Avg. accrual rate", pct(safe_mean(portfolio, "accrual_rate")))
    with kpi_cols[3]:
        below_50 = int((pd.to_numeric(portfolio.get("accrual_rate", pd.Series(dtype=float)), errors="coerce") < 0.5).sum())
        metric_card("Studies below 50%", below_50, variant="high")
    with kpi_cols[4]:
        metric_card("Withdrawn subjects", f"{int(safe_sum(portfolio, 'total_subjects_withdrawn')):,}")
    with kpi_cols[5]:
        metric_card("Invalid timelines", f"{int(safe_sum(accrual, 'invalid_enrollment_date_count')):,}", variant="pending")

    target_cols = ["study_title", "target_accrual", "total_subjects_enrolled"]
    if has_columns(portfolio_risk, target_cols):
        top = portfolio_risk.sort_values("target_accrual", ascending=False).head(15)
        top = top.copy()
        top["study_title_short"] = top["study_title"].apply(truncate_label)
        accrual_rates = top["accrual_rate"] if "accrual_rate" in top.columns else pd.Series(0, index=top.index)
        top["actual_metric"] = accrual_rates.apply(actual_accrual_category)
        target_df = top[["study_title_short", "target_accrual"]].rename(columns={"target_accrual": "subjects"})
        target_df["metric"] = "Target Accrual"
        actual_df = top[["study_title_short", "total_subjects_enrolled", "actual_metric"]].rename(
            columns={"total_subjects_enrolled": "subjects", "actual_metric": "metric"}
        )
        long_df = pd.concat([target_df, actual_df], ignore_index=True)
        accrual_color_map = {
            "Target Accrual": COLORS["target_benchmark"],
            "Actual Enrollment <50%": COLORS["at_risk_high"],
            "Actual Enrollment 50-80%": COLORS["pending_medium"],
            "Actual Enrollment >80%": COLORS["low_risk_good"],
        }
        fig = px.bar(
            long_df,
            x="study_title_short",
            y="subjects",
            color="metric",
            barmode="group",
            title="Target Accrual vs Actual Enrollment, Top 15",
            color_discrete_map=accrual_color_map,
        )
        fig.update_xaxes(title_text="Study", tickangle=0)
        fig.update_yaxes(title_text="Subjects")
        apply_plotly_style(fig)
        st.plotly_chart(fig, width="stretch")

    left, right = st.columns(2)
    with left:
        if has_columns(accrual, ["enrollment_month", "enrolled_count"]):
            trend = accrual.groupby("enrollment_month", as_index=False)["enrolled_count"].sum().sort_values("enrollment_month")
            fig = px.line(trend, x="enrollment_month", y="enrolled_count", markers=True, title="Monthly Enrollment Trend")
            fig.update_traces(
                line=dict(color=COLORS["active_primary"], width=2.5),
                fill="tozeroy",
                fillcolor="rgba(46,134,171,0.1)",
                marker=dict(color=COLORS["active_primary"]),
            )
            apply_plotly_style(fig)
            st.plotly_chart(fig, width="stretch")
        if "study_arm" in accrual.columns:
            arm = accrual.groupby("study_arm", as_index=False)["enrolled_count"].sum()
            bar_chart(arm, "study_arm", "enrolled_count", "Enrollment by Study Arm")
    with right:
        status_values = {
            "Active": safe_sum(accrual, "active_count"),
            "Completed": safe_sum(accrual, "completed_count"),
            "Withdrawn": safe_sum(accrual, "withdrawn_count"),
            "Ineligible": safe_sum(accrual, "ineligible_count"),
        }
        status_df = pd.DataFrame({"status": status_values.keys(), "count": status_values.values()})
        pie_chart(status_df, "status", "count", "Subject Status Breakdown", SUBJECT_STATUS_COLOR_MAP)

    st.subheader("Studies Below Accrual Target")
    table_cols = [
        "study_id",
        "protocol_id",
        "study_title",
        "condition_area",
        "target_accrual",
        "total_subjects_enrolled",
        "accrual_rate",
        "risk_level",
    ]
    if has_columns(portfolio_risk, table_cols):
        table = portfolio_risk[portfolio_risk["total_subjects_enrolled"] < portfolio_risk["target_accrual"]][table_cols]
        table = table.sort_values("accrual_rate").reset_index(drop=True)
        st.dataframe(
            table.style.apply(risk_row_style, axis=1),
            width="stretch",
            column_config={
                "accrual_rate": st.column_config.ProgressColumn(
                    "Accrual Rate",
                    format="%.2f",
                    min_value=0,
                    max_value=1,
                )
            },
        )
    else:
        st.info("Accrual target table columns are not available.")


def page_grants_milestones_quality(grants: pd.DataFrame, milestones: pd.DataFrame, quality: pd.DataFrame, risk: pd.DataFrame) -> None:
    st.header("Grants, Milestones & Data Quality")

    kpi_cols = st.columns(6)
    with kpi_cols[0]:
        metric_card("Total grants", len(grants))
    with kpi_cols[1]:
        metric_card("Total funding", money(safe_sum(grants, "funding_amount")))
    with kpi_cols[2]:
        awarded = safe_sum(grants[grants["is_awarded"] == True] if "is_awarded" in grants.columns else grants.iloc[0:0], "funding_amount")
        metric_card("Awarded funding", money(awarded))
    with kpi_cols[3]:
        pending_jit = int(((grants.get("jit_required", pd.Series(dtype=bool)) == True) & (grants.get("jit_status", pd.Series(dtype=str)).isna() | grants.get("jit_status", pd.Series(dtype=str)).isin(["", "Pending", "Not Required"]))).sum()) if not grants.empty else 0
        metric_card("Pending JIT items", pending_jit, variant="pending")
    with kpi_cols[4]:
        metric_card("Delayed milestones", int((milestones.get("is_delayed", pd.Series(dtype=bool)) == True).sum()) if not milestones.empty else 0, variant="pending")
    with kpi_cols[5]:
        high_dq = int((quality.get("issue_severity", pd.Series(dtype=str)) == "High").sum()) if not quality.empty else 0
        metric_card("High severity DQ", high_dq, variant="high")

    left, right = st.columns(2)
    with left:
        if "grant_operational_status" in grants.columns:
            grant_status = grants["grant_operational_status"].value_counts().reset_index()
            grant_status.columns = ["grant_operational_status", "grant_count"]
            pie_chart(
                grant_status,
                "grant_operational_status",
                "grant_count",
                "Grant Operational Status",
                GRANT_STATUS_COLOR_MAP,
            )
        if "milestone_type" in milestones.columns:
            if "is_delayed" in milestones.columns:
                delayed = milestones[milestones["is_delayed"] == True]
                delayed_by_type = delayed["milestone_type"].value_counts().reset_index()
                delayed_by_type.columns = ["milestone_type", "delayed_count"]
                bar_chart(delayed_by_type, "milestone_type", "delayed_count", "Delayed Milestones by Type")
            else:
                st.info("Delayed milestone flag is not available.")
        if "rule_name" in quality.columns:
            rule_counts = quality.groupby("rule_name", as_index=False).size().rename(columns={"size": "issue_count"})
            if "issue_severity" in quality.columns:
                rule_counts = rule_counts.merge(
                    quality[["rule_name", "issue_severity"]].drop_duplicates("rule_name"),
                    on="rule_name",
                    how="left",
                )
            else:
                rule_counts["issue_severity"] = "Low"
            bar_chart(
                rule_counts,
                "rule_name",
                "issue_count",
                "Data Quality Issues by Rule",
                color="issue_severity",
                color_discrete_map=SEVERITY_COLOR_MAP,
            )
    with right:
        if "sponsor_name" in grants.columns:
            sponsor = grants.groupby("sponsor_name", as_index=False)["funding_amount"].sum()
            bar_chart(sponsor, "sponsor_name", "funding_amount", "Funding by Sponsor")
        if "issue_severity" in quality.columns:
            severity = quality["issue_severity"].value_counts().reset_index()
            severity.columns = ["issue_severity", "issue_count"]
            pie_chart(severity, "issue_severity", "issue_count", "Data Quality Issues by Severity", SEVERITY_COLOR_MAP)

    st.subheader("Open / High Severity Data Quality Issues")
    if not quality.empty and "issue_severity" in quality.columns:
        issue_table = quality[quality["issue_severity"] == "High"].copy()
        st.dataframe(issue_table.head(100).style.apply(severity_row_style, axis=1), width="stretch")
    else:
        st.info("No data quality issues available for the current filters.")

    st.subheader("High-Risk Studies")
    if not risk.empty and "risk_level" in risk.columns:
        high_risk_table = risk[risk["risk_level"] == "High"].sort_values("risk_score", ascending=False)
        st.dataframe(high_risk_table.style.apply(risk_row_style, axis=1), width="stretch")
    else:
        st.info("Risk score data is not available.")

    st.subheader("Delayed Milestones")
    if not milestones.empty and "is_delayed" in milestones.columns:
        delayed_table = milestones[milestones["is_delayed"] == True].sort_values("days_delayed", ascending=False, na_position="last")
        st.dataframe(delayed_table.head(100), width="stretch", hide_index=True)
    else:
        st.info("No delayed milestone data is available.")


def main() -> None:
    st.title("RheumTrialOps")
    st.caption("Clinical Research Operations Analytics for Rheumatology Studies")

    data = load_csvs()
    selections, selected_studies = sidebar_filters(data["portfolio"], data["risk"])

    portfolio = filter_by_studies(data["portfolio"], selected_studies)
    accrual = filter_by_studies(data["accrual"], selected_studies)
    grants = filter_by_studies(data["grants"], selected_studies)
    milestones = filter_by_studies(data["milestones"], selected_studies)
    quality = filter_by_studies(data["quality"], selected_studies)
    risk = filter_by_studies(data["risk"], selected_studies)

    page = st.sidebar.radio(
        "Dashboard Page",
        [
            "Research Portfolio Overview",
            "Subject Accrual & Study Progress",
            "Grants, Milestones & Data Quality",
        ],
    )

    if page == "Research Portfolio Overview":
        page_portfolio(portfolio, grants, milestones, quality, risk)
    elif page == "Subject Accrual & Study Progress":
        page_accrual(portfolio, accrual, risk)
    else:
        page_grants_milestones_quality(grants, milestones, quality, risk)

    st.divider()
    st.caption(DISCLAIMER)


if __name__ == "__main__":
    main()
