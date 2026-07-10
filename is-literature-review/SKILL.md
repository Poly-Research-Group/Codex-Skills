---
name: is-literature-review
description: Conduct Information Systems literature-review work: dynamically derive project-specific search keywords from the user's research idea, ask for approval before searching, scout recent ten-year papers in a defined elite IS journal basket, screen results, and synthesize papers into matrices with IV/DV/moderator/mediator/control measures separated. Use for literature review, literature search, related work, paper synthesis, source screening, research gap mapping, construct/measures extraction, and manuscript positioning.
---

# IS Literature Review Skill

## Purpose

Use this skill to support rigorous Information Systems literature review work by combining two tasks:

1. **Literature scout**: convert a user-provided project idea into a transparent, approved search strategy and then identify relevant papers within the configured journal and time scope.
2. **Paper synthesis**: extract and compare papers using matrices that separate constructs, operational measures, independent variables, dependent variables, moderators, mediators/mechanisms, and controls.

The skill should adapt to very different research topics. Do not rely on a predefined topic list or static keyword bank. Generate search terms only from the user's project idea, the user's revisions, and terms discovered in verified papers.

## Non-negotiable operating rules

1. **Ask for the project idea if absent.** If the user has not provided a project idea, ask for a concise description before proposing keywords.
2. **Do not conduct the literature search before approval.** First propose search facets, candidate keywords, query strings, journal/year filters, and inclusion/exclusion criteria. Then explicitly ask whether the user approves, wants revisions, or wants a narrower/broader search.
3. **No predefined research keywords.** Do not insert hard-coded topic terms from other projects. Use only terms grounded in the current project idea or user-provided terms.
4. **Default outlet scope is fixed.** Unless the user explicitly changes it, search only the configured elite IS journal basket listed below.
5. **Default time scope is recent ten years.** Use a rolling ten-year window ending on the search date. If the database only supports publication-year filtering, use the closest calendar-year approximation and document it.
6. **Preserve provenance.** Record the database/source, exact query string, date searched, journal filter, year/date filter, result count, and screening decision for each source.
7. **Do not fabricate citations.** Use APA 7th only when bibliographic details are verified. If metadata are incomplete, use a placeholder and mark it as unverified.
8. **Separate evidence from interpretation.** When synthesizing papers, distinguish what the paper states from your interpretation of relevance to the user's project.
9. **Mark confidence.** Identify whether extraction is based on full text, abstract only, metadata only, or user-provided notes.
10. **Prefer concise, decision-useful outputs.** The user should be able to approve a search strategy, revise terms, screen papers, or write a literature review section from the outputs.

## Default journal basket

Restrict literature scouting to these journals unless the user explicitly authorizes additional outlets:

- Decision Sciences
- Decision Support Systems
- European Journal of Information Systems
- Information & Management
- Information Systems Journal
- Information Systems Research
- International Journal of Information Management
- Journal of Information Technology
- Journal of Management Information Systems
- Journal of Strategic Information Systems
- Journal of the Association for Information Systems
- Management Science
- MIS Quarterly
- Information & Organization

Use exact journal-title filters where possible. Account for database title variants, punctuation variants, and ampersand variants, but do not expand the outlet basket without approval.

## Default publication window

Use the rolling ten years ending on the search date. If today's date is available, calculate the exact start date. If only year filtering is available, use the nearest inclusive publication-year range and state that the range is an approximation.

Reporting format:

```text
Search window: [YYYY-MM-DD] to [YYYY-MM-DD].
Database year-filter approximation: [YYYY-YYYY] inclusive, if exact date filtering is unavailable.
Note: final screening should exclude papers outside the exact rolling ten-year window if publication dates are available.
```

## Workflow

### Phase 0: Intake

If the user gives only a broad request such as "do a literature review," ask for the project idea before proposing keywords. Ask only for what is needed to begin:

```text
Please provide a 3-6 sentence project idea, including the focal phenomenon, likely context, candidate actors/unit of analysis, and the outcome or puzzle you care about. I will then propose search keywords and ask for your approval before searching.
```

If the user already gave a project idea, infer provisional facets from it and proceed to Phase 1.

### Phase 1: Dynamic keyword and query proposal

Create a search proposal from the project idea. Do not search yet.

Produce the following sections:

1. **Project interpretation**: restate the research idea in 2-4 sentences and identify any ambiguity.
2. **Search facets**: derive terms from the idea using these generic categories:
   - focal phenomenon or technology
   - actors or unit of analysis
   - mechanism/process
   - outcome/consequence
   - context/domain
   - theory-adjacent terms if clearly implied
   - method/data terms only if they help retrieval
3. **Candidate keyword bank**: group exact phrases, synonyms, broader terms, and narrower terms. Every keyword must be traceable to the project idea or user-provided terms.
4. **Query strategy**: provide at least three database-ready search strings:
   - precision query: narrower, high-relevance terms
   - recall query: broader, adjacent terms
   - mechanism/theory query: terms that capture the underlying process, not merely the surface context
5. **Journal and year filters**: list the default journal basket and rolling ten-year window.
6. **Inclusion/exclusion criteria**: specify what will count as relevant, borderline, or excluded.
7. **Approval request**: stop and ask the user to approve or revise the search plan.

Approval request template:

```text
Please approve, revise, or narrow this search plan. I will not conduct the literature search until you confirm the keyword/query strategy and scope.
```

If the user explicitly says "search now" or has already approved a specific strategy, proceed to Phase 2.

### Phase 2: Literature search execution

After approval, conduct the search using available scholarly databases, web search, library search, or user-provided bibliographic exports. Prefer sources that provide reliable metadata and publication venue information.

Search execution requirements:

- Apply the approved keyword/query strategy.
- Apply the default journal basket unless the user approved changes.
- Apply the rolling ten-year window or documented year approximation.
- Save exact queries and filters in the search log.
- Deduplicate results by DOI first, then title/year/author match.
- Do not include papers from outside the journal basket unless they are clearly marked as "outside-scope background" and the user approved such additions.
- Do not treat search snippets as sufficient evidence for synthesis. Use full text when available; otherwise mark extraction as abstract-only or metadata-only.

Search log fields:

| Field | Description |
|---|---|
| Search date | Date the query was run |
| Database/source | Web of Science, Scopus, AIS eLibrary, Google Scholar, journal website, Semantic Scholar, library database, etc. |
| Query ID | Short identifier such as Q1-precision |
| Exact query | Full query string exactly as run |
| Journal filter | Exact journal names or source-title filters used |
| Year/date filter | Rolling window or year approximation |
| Result count | Number of raw results |
| Notes | Limitations, query syntax constraints, database issues |

### Phase 3: Screening and role classification

Screen retrieved results in two steps:

1. **Title/abstract screening**: classify each paper as include, exclude, or borderline.
2. **Full-text/metadata verification**: verify journal, publication date, article type, and relevance.

Default inclusion criteria:

- Published in one of the configured journals within the recent ten-year window.
- Addresses the focal phenomenon, context, mechanism, outcome, or closely related theoretical/process logic from the approved search strategy.
- Uses empirical, conceptual, review, or theory-building approaches relevant to IS scholarship.

Default exclusion criteria:

- Outside the configured journal basket.
- Outside the recent ten-year publication window.
- Purely technical or computational with no IS, organizational, behavioral, platform, economic, or managerial relevance, unless the user explicitly wants technical background.
- Editorial, preface, book review, teaching case, or commentary unless the user asks for it or it is central to theory framing.
- Duplicate record.

Classify included papers into one or more roles:

- Core phenomenon paper
- Theoretical foundation
- Mechanism/process paper
- Contextual analog
- Measurement precedent
- Methodological precedent
- Boundary-condition paper
- Contradictory/tension-building paper
- Review/synthesis paper

### Phase 4: Paper synthesis extraction

For each included paper, extract the following. Use "not reported" or "not available from abstract" rather than guessing.

#### Bibliographic and positioning fields

- Full citation, APA 7th when verified
- DOI or stable URL when available
- Journal
- Publication year and online publication date if relevant
- Paper role in the review
- Research question/objective
- Phenomenon/context
- Theory/theoretical lens
- Unit of analysis
- Data source/sample/time window
- Method/model/analytic approach
- Identification logic or validity strategy

#### Variable and measures fields

Separate variable roles clearly. For each role, capture both construct names and operational measures.

- Independent variable construct(s)
- Independent variable measure(s)/operationalization
- Dependent variable construct(s)
- Dependent variable measure(s)/operationalization
- Moderator construct(s)
- Moderator measure(s)/operationalization
- Mediator/mechanism construct(s)
- Mediator/mechanism measure(s)/operationalization
- Control variable construct(s)
- Control variable measure(s)/operationalization
- Level of measurement and unit of analysis alignment
- Data source for measures

Use mediator/mechanism rather than forcing a variable into mediator status if the paper theorizes a process but does not empirically test mediation.

#### Findings and contribution fields

- Main findings by relationship, not just a general summary
- Supported/non-supported hypotheses or propositions when available
- Boundary conditions
- Theoretical contribution
- Empirical/methodological contribution
- Practical/platform/managerial implications
- Limitations stated by authors
- Additional limitations or cautions
- Relevance to current project
- Open questions or literature gaps
- Extraction confidence: full text / abstract only / metadata only / user notes

### Phase 5: Cross-paper synthesis

After paper-level extraction, produce a synthesis across papers:

1. **Literature stream map**

| Stream | Representative papers | Core question | Dominant theory/lens | Typical method/data | Key IVs | Key DVs | Moderators/mediators | What is established | What remains unresolved | Relevance to project |
|---|---|---|---|---|---|---|---|---|---|---|

2. **Construct and measures map**

| Construct | Variable role(s) | Representative measures | Data source | Common unit of analysis | Papers using it | Measurement concerns | Relevance to project |
|---|---|---|---|---|---|---|---|

3. **Gap and positioning memo**

Write a concise memo that distinguishes:

- empirical gap: what has not been tested
- theoretical gap: what mechanism or boundary condition is underdeveloped
- contextual gap: what setting, technology, platform, actor, or institutional context remains underexamined
- methodological gap: what design, data, identification, or measurement opportunity remains
- contribution risk: where the proposed study may look incremental unless sharpened

4. **Manuscript-oriented paragraph skeleton**

Provide draftable literature-review logic in this order:

- what the stream has established
- where the stream remains limited
- why this limitation matters theoretically
- how the current project addresses it

Do not produce polished manuscript paragraphs unless the user asks; first provide the synthesis logic and evidence base.

## Output templates

Use the assets in this skill when a file/template is requested:

- `assets/search_strategy_template.md`
- `assets/search_approval_form.md`
- `assets/search_log_template.csv`
- `assets/screening_matrix_template.csv`
- `assets/paper_synthesis_matrix_template.csv`
- `assets/variable_measure_matrix_template.csv`
- `assets/literature_stream_matrix_template.csv`
- `assets/construct_measures_matrix_template.csv`
- `assets/positioning_memo_template.md`
- `references/elite_is_journal_scope.md`

## Quality checks before finalizing any literature-review output

Before giving the final answer, verify:

- Did I ask for approval before executing search?
- Are all keywords grounded in the user's project idea or approved revisions?
- Did I restrict the search to the journal basket and recent ten-year window unless the user approved otherwise?
- Did I record query provenance and screening criteria?
- Did I separate IV, DV, moderator, mediator/mechanism, and control variables?
- Did I distinguish constructs from operational measures?
- Did I mark whether evidence comes from full text, abstract, metadata, or user notes?
- Did I avoid invented citations and unsupported claims?
