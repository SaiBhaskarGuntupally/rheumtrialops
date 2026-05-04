# Project Story and Design Tradeoffs

## Why I Built This Project

I built RheumTrialOps because I wanted to make my healthcare data experience easier to connect with clinical research operations work.

Most of my background is around healthcare reporting, SQL, Python, dashboards, validation, reconciliation, and building datasets that other people can use for decisions. That experience is useful, but clinical research has its own language and workflow. Study status, subject accrual, grant/JIT tracking, milestones, protocol timelines, and data quality exceptions are not always visible in a generic healthcare dashboard.

So I wanted to build something that showed I had spent time thinking about those workflows. I did not want to claim direct access to systems I have not administered. I wanted the project to say something more practical: I may not be coming from a clinical research systems administrator role, but I understand the kind of reporting layer those teams need, and I can build clean data models and dashboards around that layer.

That is where RheumTrialOps came from.

## The Gap I Was Trying to Bridge

The gap was not really technical. I already had experience with databases, transformations, dashboards, validation rules, and healthcare-style reporting. The gap was domain-specific.

Clinical research operations uses tools and workflows such as REDCap, OnCore, HURON, PowerTrials, and CTMS platforms. I did not want to overstate my experience with those systems. At the same time, I wanted to show that I understand the data questions around them:

- Which studies are active or delayed?
- Are subjects being screened and enrolled?
- Are studies falling behind their accrual targets?
- Are grant or JIT items pending?
- Are milestone dates missing or delayed?
- Are there data quality issues that should be reviewed?

Those are the questions I tried to model. I focused on the part of the work that fits my strengths: taking operational data, organizing it, validating it, and turning it into reporting outputs that are easy to review.

## Options I Considered

I considered a few different project directions before choosing the final one.

One option was to build a REDCap-style form application. That would have shown subject-level data capture, but it would have pushed the project toward form design and data entry. I was more interested in what happens after data is captured: how records are cleaned, validated, summarized, and reported.

Another option was to build something that looked like a study management system. I decided against that because it would be unrealistic without access to real system workflows, permissions, and configuration details. I did not want the project to look like I was copying or recreating a platform I had not directly worked in.

I also thought about building a generic healthcare dashboard. That would have been easier, but it would not have addressed the research operations gap. A general dashboard can show charts and KPIs, but it does not show much understanding of study accrual, JIT tracking, or milestone monitoring.

A prediction model was another possible direction. I decided not to use that approach because this project does not have real historical outcomes data, and the goal was not to predict clinical or study outcomes. For this use case, a simple rule-based risk score is easier to explain and more appropriate.

I also considered making the architecture much heavier, with orchestration, containers, and more deployment tooling. That would have shown more engineering tools, but it would also have distracted from the main point. For this project, I wanted the data model, validation rules, and dashboard to be the center of attention.

In the end, I chose a focused clinical research operations analytics layer. It was the most honest and useful direction for what I wanted to demonstrate.

## Why I Chose This Architecture

I chose a simple pipeline on purpose:

1. Python creates synthetic source data.
2. PostgreSQL stores the raw tables.
3. dbt builds staging and mart models.
4. CSV exports feed the dashboard.
5. Streamlit presents the final reporting views.

This setup gave me enough structure to show real analytics engineering work without making the project unnecessarily complicated. Raw data stays separate from cleaned staging models. Staging models stay separate from dashboard-ready marts. The dashboard does not depend on a live database connection, which makes it easier to run and review.

I could have added more tools, but I did not think that would improve the story. The important question was whether the project could show clear data modeling, visible validation issues, and useful operational reporting. This architecture was enough for that.

## Why I Used Rheumatology as the Theme

I used rheumatology because it gave the project a specific clinical research setting instead of making it feel generic.

Rheumatology and chronic disease studies often involve follow-up, medication monitoring, patient education, telemedicine visits, care coordination, and long-term disease management. Those themes work well for operational reporting because they naturally connect to subject accrual, milestones, grant activity, and study progress.

The project includes themes such as rheumatoid arthritis, gout, osteoporosis, lupus, inflammatory arthritis, telemedicine follow-up, technology-enabled care delivery, and chronic disease management. These are only used to create a realistic context. The project does not represent any specific real study.

## Data Source Decisions

I wanted the data to feel realistic, but I also wanted the project to be safe to share.

Public sources such as ClinicalTrials.gov and NIH RePORTER are useful references because they show how studies and grants are described publicly. They helped shape the kind of metadata that made sense for the project.

But I made the operational data synthetic. That includes subject records, enrollment dates, grant/JIT status, milestone dates, and data quality issues. I made that choice because using real operational data would create privacy, HIPAA, compliance, and institutional data concerns. Synthetic data also let me create known bad records on purpose, which made the data quality dashboard more meaningful.

The goal was not to reproduce real clinical trial operations. The goal was to build a safe project that shows how I would structure, validate, and report on research operations-style data.

Reference sources:

- [ClinicalTrials.gov API](https://clinicaltrials.gov/data-api/api)
- [NIH RePORTER API](https://api.reporter.nih.gov/)
- [REDCap](https://project-redcap.org/)
- [OnCore / CTMS context](https://www.advarra.com/)

## Why I Kept the Data Model Small

I kept the source model to four tables:

- studies
- subjects
- grants
- milestones

That was intentional. These four tables cover the main reporting story I wanted:

- portfolio visibility through studies
- accrual tracking through subjects
- funding and JIT tracking through grants
- timeline monitoring through milestones

I could have added staff effort, protocol calendars, billing information, or detailed form-level data. I decided not to include those in this version because they would make the project harder to follow. A smaller model made the project easier to review and kept the focus on the core clinical research operations questions.

## Why I Used dbt

I used dbt because I wanted the transformation logic to be easy to inspect.

The raw tables hold the source records. The staging models clean field formats and add validation flags. The mart models turn those fields into reporting tables for portfolio summaries, accrual tracking, grants, milestones, data quality, and risk scoring.

That separation matters. It makes it clear where the data starts, where it gets standardized, and where it becomes dashboard-ready. It also makes the validation logic easier to review. I did not want to hide bad records or remove them from the dataset. I wanted them to stay visible because data quality issues are part of the reporting story.

## Why I Used Streamlit

I used Streamlit because I wanted the dashboard to be easy to open and review.

Power BI or Tableau would also work for this kind of project, but they add extra friction for someone who just wants to see what the project does. Streamlit lets the dashboard run in a browser and read from exported CSV files. That means the app does not need a live database connection.

For this project, that was the right tradeoff. The dashboard is deployed at [https://rheumtrialops.streamlit.app/](https://rheumtrialops.streamlit.app/), so someone can review the result directly before deciding whether they want to look through the code or run the pipeline locally. The dashboard is lightweight, but it still shows the important views: portfolio overview, subject accrual, grant/JIT tracking, milestones, data quality issues, and study risk.

## Why the Risk Score Is Rule-Based

I made the risk score rule-based because I wanted it to be explainable.

The score is based on simple operational signals: low accrual, pending JIT items, delayed milestones, high-severity data quality issues, and approaching completion dates. Those are the kinds of things a research operations team might want to review.

I did not want the score to look like it was predicting outcomes. It is not a clinical prediction tool, and it is not meant to say whether a study will succeed or fail. It is only a way to sort studies by operational attention.

## What This Project Shows

This project shows how I approach a domain that is adjacent to my existing experience but not exactly the same. I tried to keep the scope realistic, the data safe, and the reporting layer clear.

It demonstrates:

- clinical research operations reporting mindset
- SQL data modeling
- dbt transformations
- data quality validation
- synthetic data generation
- dashboard design
- subject accrual tracking
- grant/JIT visibility
- milestone monitoring
- operational risk scoring
- ability to learn unfamiliar workflows without overstating direct system experience

## What This Project Does Not Claim

This project does not use real patient data, real UAB data, or direct access to REDCap, OnCore, HURON, PowerTrials, or CTMS systems. It uses public or synthetic study metadata and fully synthetic operational data to demonstrate transferable data modeling, validation, workflow monitoring, and reporting skills for clinical research operations.

It is not a replacement for any clinical research platform. It is not a production clinical system. It is not a clinical decision support tool. It does not make patient-level predictions.

## Final Reflection

My main goal was to build something practical and honest. I did not want to make the project bigger just for the sake of adding tools. I wanted RheumTrialOps to focus on the reporting work that matters in research operations: clean data, visible progress, clear exceptions, and dashboards that make it easier to see where attention is needed.
