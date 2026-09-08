# Unsafe-set reachability verification

[Mathematical contract and proofs](../../foundations/BELLMAN_UNSAFE_SET_REACHABILITY_AND_CONSTRAINED_SELECTION.md).

Run the complete current and historical acceptance entry point from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verification/unsafe_set_reachability/run_checks.py
```

`reference.py` computes the exact probability that one complete deterministic policy ever enters
an explicitly identified set of completed observable histories. Unsafe histories become absorbing
only inside this recurrence. The supplied sequential subject is not rewritten. The receiver
recomputes every node value and requires equality with an independent forward first-hit expansion.
It binds the exact subject/model identity, policy, unsafe set, root probability, and optional cap.

The persistent-family route retains every model identity, uses no model weights, and accepts only
one common accessible policy. The selection route reuses the existing exact whole-policy cost
matrix, checks a separate reachability matrix, forms one fixed robust-feasible deterministic class,
and computes constrained minimax expected loss and same-model constrained regret. Empty FULL and
subset catalogues receive different, bounded conclusions.

The statistical route first runs the PR #16 receiver for statistical evidence, exact
stream-to-transition mapping, pathwise multi-affine admissibility, and completed corner-family
construction. Only then does it check corner reachability. A `17 × 17` rational interior audit is
supporting evidence; the first-hit multi-affinity proof establishes the continuous rectangle
result. Repeated same-path use of a parameter returns an invalid corner-reachability warrant while
leaving the sequential problem valid for another optimization method.

The fixed cases cover transient unsafe histories, unsafe-node double counting, expected loss versus
reachability, strict/relaxed caps with different policy winners, safe and unsafe persistent-family
members, zero-probability branches, signed costs, early STOP, hidden-model policy rejection,
FULL/subset empty classes, one and two statistical parameters, the interaction `p(1-q)`, mutually
exclusive reuse, loose rectangles, malformed mappings, stale subjects, producer-disabled receiving,
and the exact `p(1-p)` interior failure. A separate equal-number control gives both statistical
coverage failure and unsafe reachability the value `1/20` and rejects merging or adding them as one
untyped risk quantity.

The runner executes the new checks normally and with `-O`, exercises inherited current components,
replays PR #16's complete acceptance chain at its exact merge in an isolated clone, checks frozen
prerequisite identities, verifies base preservation and affected Markdown links, and compares
normal/optimized results. `results.json` is the compact source-bound result record; it does not
rewrite prior evidence.

The result is conditional mathematics. Statistical IID/completeness premises, empirical model
validity, and normative adequacy of the unsafe set are supplied rather than established. It makes
no randomized-policy, CVaR, dynamic-risk, authority, Writ/Decision Lab, language-migration, or
formal-verification claim. The bounded exact enumeration did not reach a solver/language trigger.
