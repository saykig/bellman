# Current PR #22 reproduction: diagnostic history erasure

From repository root with Python 3.12 and pinned dependencies:

```sh
python -m pip install -r verification/sequential_consistency/requirements.txt
PYTHONDONTWRITEBYTECODE=1 python verification/diagnostic_erasure/acceptance.py --verify-retained
```

Default acceptance runs the new ordinary/optimized checks and inherited strategic,
causal and history obligations. `--strategic`, `--causal`, `--history` select one
workflow obligation; causal/history modes do not need SymPy. Earlier runners remain
correct at their frozen commits, not as direct current-tree entrypoints.

The [foundation](../../foundations/BELLMAN_DIAGNOSTIC_HISTORY_ERASURE_OBSTRUCTION.md)
proves an obstruction for a specified binary diagnostic/disclosure reduction: both
models separately support the reduced assessment, but the required common ratios
3/5 and 5/3 cannot both be limits. All local continuation values agree. The proof
handles arbitrary sequences; rejecting one power witness would not establish this.
The nearest checked repair retains sender information, merging only the receiver's
sets and inducing the full new belief from a common witness.

`example_case.json` contains three full subjects, source and repair common warrants,
individual target warrants, target incentives and an obstruction pair. The independent
`receive_case.receive(case, expected_identity, expected_query=QUERY)` requires the
recipient's intended identities separately. It recognizes the full bounded game class
before checking the odds obstruction, receives positive claims through the existing
polynomial/path receivers, and compares every local pure action value. No arbitrary
game solver, partition search or global outcome-distribution transport is implemented.

`checks.py` reproduces the retained candidate, exercises decisive rejection controls,
checks exact linear equations independently through SymPy, and performs receiving in
a temporary deployment containing no candidate producers. The symbolic linear solution
corroborates arithmetic; only the foundation's limiting-odds argument proves absence
of arbitrary consistency sequences. Later-guess and monitoring controls are elementary
arithmetic checks, not a new mechanism-game interface. The existing coordination and
integrated bond game are inherited unchanged.

Before replay, `acceptance.py` compares EVERY earlier tracked file to
`5ea19f214ec89536f47fe20cfa5a4d62222b2598`, except three living documents and three
workflow entrypoints explicitly listed in its source. Additions have an exact allowlist.
Mutation and unregistered-release controls must fail. Inherited acceptance runs in a
detached temporary clone at that commit, recursively checking earlier preserved sources.
No frozen result, review, mathematical edition or source manifest is overwritten.

`results.json` binds all new sources, retained example, living guidance and workflow
entrypoints to the exact source commit and their SHA-256 bytes. It records fresh
observations and excludes itself to avoid circular hashing. Required inherited checks
are actual replay, not an inference from CI labels. Ordinary/optimized equality is
conformance evidence, not formal verification or empirical validation.
