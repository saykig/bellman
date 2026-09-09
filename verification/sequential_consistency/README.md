# Shared consistency under uncertainty

This additive reference implements the sufficient shared-witness theorem in the
[consistency addendum](../../foundations/BELLMAN_SEQUENTIAL_CREDIBILITY_CONSISTENCY_ADDENDUM.md).
The [preliminary assessment-relative reference](../sequential_credibility/README.md),
its original subject/certificate and all historical evidence remain byte-for-byte unchanged.

## Query and earned capability

Given one common behavioral profile, model-specific assessments, a rational power
witness and a separately requested epsilon, check every limiting posterior jointly
and every conditional **full-continuation** incentive. One witness covers all models
and all information sets. At epsilon=0 a pass establishes modelwise sequential
equilibrium with shared consistency, conditional on the supplied games. At positive
epsilon the output is a consistent assessment with a continuation-gain bound.

`valuation_producer.py` traverses leading coefficients and orders. The independent
`consistency_receiver.py` reconstructs complete normalized prefix polynomials using
SymPy `Poly` over `QQ`, then computes exact zero limits by trailing coefficients.
It calls the unchanged old path-based incentive receiver. Both producers are absent
in the isolated receiving test. Structural validation and runtime libraries are
shared trusted infrastructure; this is not formal verification or external peer review.

The witness must specify every zero-profile action and no positive-profile action,
with positive canonical rational coefficient and integer order in 1..32. Chance laws
are never trembled. An information set with no chance-reachable node is unsupported;
a chance-impossible node within an otherwise reachable set receives belief zero.

## Reproduce

Use Python 3.9 or later and the pinned dependencies. For example, from repository root:

```sh
python3 -m venv /tmp/bellman-consistency-env
/tmp/bellman-consistency-env/bin/python -m pip install -r verification/sequential_consistency/requirements.txt
PYTHONDONTWRITEBYTECODE=1 /tmp/bellman-consistency-env/bin/python verification/sequential_consistency/run_checks.py --verify-retained
```

To receive the retained warrant without constructing candidates:

```sh
PYTHONDONTWRITEBYTECODE=1 /tmp/bellman-consistency-env/bin/python verification/sequential_consistency/consistency_receiver.py verification/sequential_credibility/example_subject.json verification/sequential_consistency/example_warrant.json 0
```

`run_checks.py` is read-only: it compares normal and optimized checks, replays the
original retained credibility checks in an exact temporary draft snapshot, preserves all tracked draft/base files except
the three living steering documents, and resolves new source hashes against their
recorded Git commit. The old manifest includes the old living documents, so running
its `--verify-retained` directly against today's updated documents correctly fails;
the snapshot replay preserves that historical identity rather than bypassing it.
`results.json` binds source and exact observations; the warrant
is checked against its own digest inside that observation. No old results are updated.
The older causal and historical suites are not transitively rerun: no implementation
dependency on them is introduced or changed. The original runner also checks the
merged PR #20 base byte-for-byte.

## Decisive boundaries

The J/K counterexample passes the original incentive checker but violates an exact
posterior identity for every perturbation sequence. A separate two-prior example has
individual modelwise consistency witnesses but provably no shared sequence. Those
are analytical impossibilities, independently exercised with exact symbolic identities.
A failed candidate alone produces `witness-limit-mismatch`, never global inconsistency.

The integrated fixture checks 80 model/information-set queries. Different orders,
nonunit coefficients, fully mixed profiles, chance zeros, complete witness renaming,
memory loss, bond/fee revisions, recipient-controlled tolerances and forged certificates
are exercised. Three positive rational perturbation sizes provide additional path
arithmetic evidence; the theorem supplies the limiting guarantee.

No complete equilibrium search, complete rational-witness existence decision, generic
continuous-uncertainty certificate, general history quotient, truth-leaning equilibrium,
ambiguity-sensitive equilibrium, mechanism optimum, or empirical prediction is implemented.
See the [research audit](../../reviews/SEQUENTIAL_CREDIBILITY_RESEARCH_REVIEW_2026_09_08.md)
for source inspection, library dispositions and the next gate.
