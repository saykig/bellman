# Kahneman Lab Experiment 5

**Status:** stopped at Stage R with `KL5_STOP_DEGENERATE`. Main Lanes A–D and synthesis were not run.

**Title:** Sequential Sufficiency: Replication, Quotients, and Falsification

## Frozen artifact manifest

| Role | File | SHA-256 |
|---|---|---|
| Preregistration | `RUN_THIS_NEXT_KAHNEMAN_LAB_5_SEQUENTIAL_SUFFICIENCY.md` | `43bf13e830d72fac72a36f18197b68d3e9465c8692ff9e69370512f88d7636d1` |
| Stage R report | `kahneman_lab_5R_replication_gate.md` | `4cd74eef7b2dc6cf8340876aaaba4cdbd90f3010df710d61b0f21440e8effe94` |

## Registered Stage R result

Stage R executed the frozen primary and mandatory informative-interior gates with exact rational arithmetic and two deterministic verification paths.

- Primary strongest-certificate (`C_*`) gate: **64** distinct separating pairs.
- Smallest separating horizon: **2**.
- First primary `C_*` pair: **P0100/P0106**.
- Mandatory informative-interior `C_*` gate: **0** separating pairs among 144 equal-`C_*` candidate pairs.
- Frozen verdict: `KL5_STOP_DEGENERATE`.

Under the preregistration, this verdict stops KL5 before Lanes A–D. It means the registered separation failed the specific informative-interior robustness tier in this finite design; it does **not** establish that boundary or degenerate kernels are globally necessary.

## Post-hoc audit — not a KL5 result

A later exploratory finer-grid audit found strictly interior equal-certificate models with different sequential decisions, suggesting that the registered interior failure may be sensitive to the coarse quarter-spaced kernel grid. This was not preregistered, does not alter the frozen KL5 verdict, and must be independently preregistered and replicated before being treated as a finding.

Any correction to a frozen artifact must be a separately versioned record. Do not edit the preregistration or Stage R report in place.
