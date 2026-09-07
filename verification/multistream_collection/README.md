# Controlled multistream collection verification

[Mathematical contract and proofs](../../foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md).

Run the current acceptance entry point from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verification/multistream_collection/run_checks.py
```

The runner executes the repaired current PR #12 scalar checks and the new M1–M8 checks normally
and with `-O`. It separately verifies preserved PR #12 source/result identities and runs PR #12's
unchanged historical acceptance program at repaired head
`5017122500450c8f7f890474f7232b9c94d3a3fb` in a disposable clone whose `origin/main` is bound to
the required historical base `2e8d99cdcf289eabb63df15086eaa68251a359f1`. That historical program in
turn executes its complete pinned PR #10 preservation chain. Current live additions are checked
by the new runner's exact allowlist; they are not fed to PR #12's obsolete hardening-only path
scope.

`reference.py` separates collection replay, rowwise scalar evidence, simultaneous coverage, and
static decision certificates. A collection binds a fixed ordered stream registry, source and
protocol identities, fixed alpha allocation, a built-in nonanticipative rule, global/local event
indices, unique physical-event identities, an append-only transcript, and stopping/revision
status. The receiver reconstructs every prefix. It cannot diagnose concealed outcome filtering or
validate the declared physical sampling premise.

Each row is projected into the unchanged PR #12 scalar receiver. The multistream receiver accepts
identified scalar rows in arbitrary presentation order, rejects missing/duplicate/mismatched
rows, recomputes the rectangle, and applies only the finite union bound. No cross-stream
independence is assumed for coverage and no adaptive-count binomial conditioning is used.

The decision receiver independently recomputes all signed rational affine-risk differences at
the appropriate rectangle endpoints, the complete common and strict action sets, explicit strict
margins, intended-action regret, and an optional loss-unit cap. It supports population expected
risk. Conditional fresh-draw risk requires a separately bound sufficient premise. Nonlinear joint
events are unsupported by marginal Bernoulli parameters and reject.

The finite request profile is four streams, 128 observations per stream, 512 transcript events,
four actions, and 64 requested precision bits. Producers and receivers return the same typed
`unfinished`/`resource-refusal` before expensive work for a valid out-of-profile request.
Malformed or mathematically false evidence rejects; a checked empty action set is a substantive
noncertification.

The exact M1–M8 controls include scalar reduction, the two prescribed rectangles, full adaptive
path enumeration, the adaptive-count counterexample, omission/copying, allocation and identity
mutations, perfect cross-row dependence, producer-disabled hand-authored evidence, full corner
enumeration, coarse valid witnesses, boundary/refusal behavior, large derived rational
coordinates, immutability, and stale or unfinished evidence. These fixed calculations do not
establish empirical IID sampling, absence of drift/missingness, formal verification, optimized
collection, Writ/Decision Lab integration, or authority to act.
