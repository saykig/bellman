# Current acceptance: mathematical release plus human-data checkpoint

This additive entrypoint supersedes the v0.0.7 wrapper **for the expanded current tree**.
The previous wrapper, result and mathematical evidence remain unchanged and are replayed at
v0.0.7 in an ephemeral detached snapshot. This is not a new release or a weaker historical gate.

```sh
python -m pip install -r research/empirical_trust_2016/requirements.txt
PYTHONDONTWRITEBYTECODE=1 python verification/empirical_acceptance/acceptance.py --recompute --verify-retained
```

It checks:

- every frozen file from the release and empirical checkpoint ae7acb7, with explicit living
  guidance/CI exceptions and an explicit additions list;
- the original v0.0.7 combined strategic/causal acceptance at its exact commit;
- live strategic and causal component checks in normal and optimized modes;
- retained empirical source identities, producer-disabled arithmetic receiving, 14 rejection
  controls, intended-use revision replay and its 3 rejection controls;
- optional fresh statistical fitting with pinned packages, normal/-O equality on one host,
  comparison to retained numbers within 1e-11 across hosts, and independent receiving of
  the fresh predictions. Runtime metadata is reported, not required to be byte-identical.

`--strategic`, `--causal`, `--history` retain the old workflow obligations and add empirical
receiving without requiring the statistical stack. Full `--recompute` requires the empirical
requirements (which also include SymPy). The history route needs only the standard library.

[completion-results.json](completion-results.json) binds this wrapper and current guidance to a committed source edition.
The earlier empirical [checkpoint receipt](../../research/empirical_trust_2016/checkpoint-validation.json)
continues to describe its own source commit, including its then-outstanding combined gate.
That historical statement is not rewritten. Use this guide for current execution.

Passing these checks establishes scoped computational conformance and preservation, not a
population finding, randomization audit, external peer review or formal verification. The
source-bound [research review](../../research/empirical_trust_2016/REVIEW_20260909.md) records the
statistical limitations. The stronger experiment recommendation remains research ahead.

The [first aggregate receipt](results.json) is preserved at 4685278. The completion receipt
also binds the [requirement audit](../../research/empirical_trust_2016/COMPLETION_AUDIT_20260909.md).
Its analytical design illustration is not a fitted empirical model or a new formal-verification claim.
