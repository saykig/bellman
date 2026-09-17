# Selective Lean feasibility evaluation

Run from this directory:

```sh
lean Compatibility.lean
```

The project-local `lean-toolchain` pins Lean 4.33.1. No global configuration,
Mathlib installation or Lake dependency download is required if that toolchain
is installed. Reproduction otherwise requires installing the pinned toolchain.

Status: elaborated and checked successfully on 2026-09-17. The source prints
its axiom dependencies; the compact evaluation receipt records them.

- `extension_iff_join_exact`: T1 for two bags with common separator, arbitrary
  types. It proves existence of an exact global relation iff the natural join
  recovers both projections. It does not formalize the arbitrary-family version.
- `overlap_implies_exact`: T2 for arbitrary types, by explicit witnesses.
- `equality_cycle_impossible`: the logical core of X1.
- `relation_in_rectangle`: the inclusion core of T4.
- `replacement_commutes_with_ownership`: T3(b)'s assembly identity for a disjoint
  sum of owners and arbitrary factor values; no DAG or probability semantics.

The first four declarations report no axiom dependencies. The functional equality
in the last uses function extensionality through Lean's standard `Quot.sound`.
There are no custom axioms, `sorry`, `admit`, `native_decide`, or external solver
certificates. This trusts Lean's kernel/toolchain, not empirical causal premises.

Verdict: formalizing the relational core is cheap and useful. Do not describe the
full stochastic theorem as machine verified. Next formal step, if this interface
is reused, would be finite DAG normalization and marginal evaluation in Mathlib;
that is unnecessary for the present bounded research conclusion. It would require
an explicit finite graph/kernel encoding and a larger dependency footprint.
