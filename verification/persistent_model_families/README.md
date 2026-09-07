# Persistent model-family verification

[Mathematical contract and proofs](../../foundations/BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md).

Run from the repository root with the existing Python runtime:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verification/persistent_model_families/run_checks.py
```

The runner executes the new fixed checks normally and with `-O`, compares exact observations, invokes
the unchanged certificate-accumulation/preservation runner, verifies PR7's merge tree against its
reviewed head, and checks every file in the pinned base. Historical files must remain byte-identical;
only README and the two cumulative ledgers may have append-only additions.

`families.py` imports the existing PR7 and ordinary certificate consumers. It provides three
separate interfaces: a bound for one named policy across an ordered persistent family; exact choice
from a checked deterministic policy matrix; and an unweighted positive-prefix family query. Full
choice coverage is independently enumerated and capped at 64 policies. A larger full-class request
is `unfinished`, while a separately valid named-policy bound remains available.

`checks.py` fixes F1–F8 and uses a separate forward path evaluator for exact arithmetic checks. It
also covers model/certificate identity, support, criterion, unit, coverage, exact proof types,
large derived rationals, immutable inputs, empty-support conditioning, zero-horizon and one-model
reductions. All relevant candidate producers are disabled during final receiver checks.

`results.json` records the actual GitHub Actions runtime, counts, exclusions/refusals, timings,
executed-source hashes, base/head identities, and inherited preservation results. Fixed executions
are not formal verification, independent authorship, statistical coverage, or validation of supplied
model/access/loss premises. The reference supports deterministic policies only and makes no Bayesian,
randomized-optimum, rectangularity, dynamic-consistency, Writ, or Decision Lab claim.
