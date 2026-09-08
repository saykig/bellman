# Finite causal identification verification

[Mathematical contract and proofs](../../foundations/BELLMAN_FINITE_CAUSAL_IDENTIFICATION_AND_DECISION_CERTIFICATION.md).

Run the complete current and historical acceptance entry point from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verification/finite_causal_identification/run_checks.py
```

`reference.py` contains two separate exact routes. The adjustment route accepts a complete rational
`P(A,Y,Z)`, explicit population and variable identities, and named consistency, exchangeability,
pre-action, intervention, and adjustment-set premises. Its receiver independently reconstructs the
required support and complete binary intervention law. A missing supported treatment cell is
`positivity-failure-for-adjustment`, not causal incompatibility.

The response-type route uses exactly the eight `(A_nat,Y0,Y1)` types. Observed consistency and the
small typed library of monotonicity or exact linear-equality restrictions form an equality-simplex
fibre. Complete rational vertex enumeration decides bounded compatibility and every linear
intervention/risk/difference extremum. The receiver enumerates zero sets independently and requires
the complete vertex list and exact attaining witnesses. Unsupported nonlinear factorization is not
silently linearized; an explicitly requested dropped-restriction result is labeled outer-only.

Decision certification maximizes each action difference on one shared response-type law. It does
not subtract risk extrema attained by different causal witnesses. Fixed cases include the exact
Simpson reversal, positivity failure, exact partial and point identification, decision
identification despite nonpoint causal probabilities, opposite model-dependent action witnesses,
incompatibility, unsupported/outer distinctions, forged claims, stale subject bindings, malformed
inputs, direct independent vertex enumeration, and producer-disabled receiving.

The runner executes these checks normally and with `-O`, runs inherited current Bellman packages,
checks the history/release manifest, preserves every merged PR #17 base file except the declared
living pointers and workflow delegation, and replays the entire PR #17 acceptance chain from its
exact merge in an isolated clone. `results.json` is a compact source-bound execution record and does
not rewrite prior evidence.

This is conditional one-stage causal mathematics, not causal discovery, empirical premise
validation, sequential treatment, transport, graph search, safety integration, Writ/Decision Lab
integration, formal verification, or authority to act. The complete eight-type enumeration did not
reach a solver or language trigger.
