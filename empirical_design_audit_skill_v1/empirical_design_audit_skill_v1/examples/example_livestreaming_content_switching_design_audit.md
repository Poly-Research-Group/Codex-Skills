# Example: Design Audit for a Livestreaming Content-Switching Study

This example illustrates how the design-audit skill should reason. It is not a template to copy mechanically.

## Research context

A livestreaming platform study examines whether entrant creators' movement into a content category changes incumbent creators' viewer flows. The theoretical logic separates direct viewer-flow spillovers from indirect category-visibility spillovers.

## Unit of analysis

One row represents an incumbent creator-session. The audit must verify that the row key, such as `(incumbent_creator_id, session_id, entrant_event_id)` or the project-specific equivalent, is unique. If multiple entrant events can affect the same incumbent-session, the audit must determine whether the data intentionally aggregate entrants or accidentally duplicate incumbent-session rows.

## Treatment/event construction

The event is an entrant creator switching from another category into the incumbent's category. Treatment timing must be based on category at `t-1` and `t`, not on later viewer outcomes. The audit should verify treated sessions, comparison sessions, pre/post windows, repeated switches, overlapping events, and whether exact switch timing is observed or only interval-coded.

## Outcomes

Direct and indirect net viewer-flow outcomes are directional flow measures. Because the outcomes are constructed from viewer IDs across adjacent sessions, the audit must verify that the mapping uses only the allowed pre/post window and does not create future-information leakage.

## Controls

Reasonable controls may include lagged incumbent viewership, baseline or lagged creator popularity, content similarity between source and destination categories, mature-content indicator, and time-period indicators. The audit should flag current visibility, post-switch ranking, or post-switch engagement as possible mechanisms or bad controls if they are downstream of the entrant switch.

## Fixed effects and clustering

Potential fixed effects include incumbent creator, category, and session/time fixed effects. The audit must check whether the treatment varies within these dimensions and whether category-by-time shocks or streamer-level serial correlation imply particular clustering choices.

## Identification threats

Major threats include endogenous switching timing, category-level concurrent shocks, unobserved exact switch timing, algorithmic ranking confounding, interference across creators, viewer-level dependence, source coverage restrictions, and sensitivity to event-window length.

## Robustness seed plan

Potential robustness checks include alternative event windows, alternative flow transformations, untransformed outcomes, high-similarity category subsamples, exclusion of overlapping events, placebo switch times, and alternative clustering levels.
