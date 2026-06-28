# DID / Event-Study Design Memo

## Treatment structure

- Treatment variable:
- Treated units:
- Control units:
- Treatment-assignment level:
- Treatment timing:
- Staggered or common timing:
- Pre-periods:
- Post-periods:

## Assumptions

- Parallel trends rationale:
- No anticipation rationale:
- Stable composition:
- No spillover/interference, or how exposure is handled:

## Required diagnostics

- Treatment timing table.
- Outcome trends by treatment group before treatment.
- `estat trendplots` after `didregress`/`xtdidregress` where applicable.
- `estat ptrends` where applicable.
- `estat granger`/event-time leads for anticipation.
- `estat bdecomp` or heterogeneous DID route when staggered timing is present.
- Placebo timing and alternative window checks.

## Reporting

- ATET estimate.
- Event-time plot.
- Pretrend p-value or visual assessment.
- Group/time FE and cluster level.
- Number of treated/control units and observations.
