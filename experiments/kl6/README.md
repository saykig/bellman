# Kahneman Lab Experiment 6

**Status:** closed analytically.

- Referee verdict: `KL6_STOP_THEORY_ALREADY_SETTLES`
- Programme disposition: `KL6_STOP_STANDARD`
- Decisive scoped finding: `STOP-RECONSTRUCTION`

## What KL6 established

KL6 did not execute the originally proposed exhaustive Stage R or Stage M. The replacement audit closed the registered question analytically.

For the original informative eighth-grid domain at horizon 5, with context `B=(p,L,c)` fixed:

```text
C_*(B,k) = C_*(B,k')
and
Z_5(B,k) = Z_5(B,k')

imply

k = k'.
```

Equivalently, `S04=(C_*,Z_5)` and the labeled observation kernel induce the same conditional partition on the registered domain.

Therefore:

- **P-SUFF is true**, because S04 reconstructs the labeled kernel and therefore preserves the registered downstream decision targets.
- **P-COMP is false**, because no distinct-kernel equal-S04 pair exists on that domain.
- S04 does **not** demonstrate genuine compression.

The same audit also establishes that `C_*` alone is too weak for bounded sequential decisions. Distinct strictly interior models can share prior, loss, cost, and `C_*` while producing opposite strict root STOP/OBSERVE decisions. This is compatible with standard belief-state/Bellman theory: the known observation model remains part of the continuation dynamics even when posterior belief is a sufficient history state within one fixed model.

## Scope limits

The injectivity result is finite-domain and registered-scope specific. It does not prove:

- that every exact decision-preserving representation reconstructs the full model;
- that no task-relative compression exists;
- that every other finite grid behaves the same way;
- that shorter-horizon summaries are injective;
- or that approximate representations cannot preserve decisions with certified error.

Those stronger claims are not KL6 results.

## Closure rule

Do not reopen KL5 or KL6 by adding a new grid, cost, loss family, horizon, smoother kernel, representation ladder, parallel lane, or holdout merely to rescue S04. Such work would be a different research question.

No KL7 follows automatically from this branch.

## Post-KL6 frontier audit

A subsequent literature-grounded mathematical frontier audit ended with:

`FRONTIER_STOP_EXISTING_THEORY_SUFFICES`

It found that bounded optimal-value error, bounded surrogate-policy regret, exact abstraction under appropriate conditions, and approximate decision-preservation guarantees already belong to established mathematical territory. The KL6 finite-horizon coupling argument itself supplies bounded optimal-value error, bounded regret for an implementable surrogate-model policy, and exact root STOP/OBSERVE preservation outside a certified margin interval.

The surviving bounded question, if later useful, is economic rather than foundational: after fixing the query family and criterion, identify the smallest, cheapest, or efficiently discoverable representation achieving the desired guarantee.

That question is one possible proving-ground direction, not the default roadmap.

## Source identity

The binding KL6 replacement was supplied as `RUN_THIS_NEXT_KAHNEMAN_LAB_6_OBSERVATION_MODEL_SUFFICIENCY_V2(2).md` with SHA-256:

`31a4fb8bfcfbb7e9c4753866628c7784bf769d560d6716e21e878d22bf3d47f2`

The exact source bytes are not migrated into this repository in this consolidation. This README is a ledger record of the binding closure, not a rewritten substitute for the frozen source artifact.
