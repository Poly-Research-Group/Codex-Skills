# Research-Design Intake Questionnaire

Use this questionnaire before preparing archival empirical data. The goal is to build the dataset around the research design rather than around available columns.

## 1. Research context

- What is the working project title?
- What empirical context, platform, organization, industry, or market does the study examine?
- What focal phenomenon motivates the study?
- What is the main research question?
- What theoretical lenses or literature streams guide the study?
- Is the intended claim causal, associational, descriptive, predictive, or exploratory?

## 2. Hypotheses or focal empirical relationships

For each hypothesis or empirical relationship, specify:

- Hypothesis ID, such as H1, H2a, H2b.
- Hypothesis statement.
- Expected sign or pattern.
- Dependent construct and intended measure.
- Key independent construct, treatment, or event and intended measure.
- Moderator, mediator, or mechanism if any.
- The temporal order implied by the theory.

## 3. Unit of analysis and time structure

- What should one row in the final analysis dataset represent?
- Is the dataset cross-sectional, panel, repeated cross-sectional, event-time, cohort-time, transaction-level, or session-level?
- What is the time grain: minute, session, day, week, month, quarter, year, or none?
- What is the observation window?
- What are the unit identifiers and time identifiers?

## 4. Data sources and merge logic

For each raw data source, specify:

- File, table, API, or database name.
- Source owner or collection method.
- Coverage start/end dates.
- Unit and time grain in the raw source.
- Available ID, timestamp, category, group, treatment, and outcome columns.
- Expected merge keys with other sources.
- Known limitations, missingness, measurement error, or access restrictions.

## 5. Variable roles

List all candidate variables by role:

- Dependent variables.
- Key independent variables, treatment indicators, or event variables.
- Moderators.
- Mediators or mechanisms.
- Candidate controls.
- Fixed effects.
- Clustering dimensions.
- Sample restriction variables.
- Variables for descriptive tables only.

## 6. Timing and control-variable logic

- Which controls are measured before the treatment/key independent variable?
- Which variables are contemporaneous?
- Which variables may be post-treatment mediators or mechanisms?
- Which variables may mechanically overlap with the dependent variable?
- Which variables are likely to be absorbed by fixed effects?
- Which variables should be excluded from the main model but retained for robustness or mechanism analysis?

## 7. Sample frame and transformations

- What units and time periods are eligible for the study?
- What exclusion rules are theoretically motivated?
- What exclusion rules are data-quality motivated?
- Are lags, leads, event-time indicators, baseline windows, or rolling measures needed?
- Should variables be logged, inverse-hyperbolic-sine transformed, winsorized, trimmed, standardized, or aggregated?
- How should zeros, negative values, and structural missingness be handled?

## 8. Manuscript-facing outputs

- Which variables should appear in the main descriptive statistics table?
- Are grouped or decomposed descriptive statistics needed?
- What variable names and descriptions should appear in the manuscript table?
- Should the table report a common N row or variable-specific N?
- What output formats are needed: CSV, Markdown, LaTeX, Excel, or all?
