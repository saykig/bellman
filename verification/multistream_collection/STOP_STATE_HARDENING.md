# PR #14 final stopping-state revision hardening

**7 September 2026. Additive acceptance repair; no new mathematical stage.**

Reviewed pre-repair head: `32c40894904837cbf16692dca6ec3bfb03322a76`.
Current main: `fc45c4fff0f2958450f7073b46b67b92cb306bb3`.

The mathematical companion, original PR #14 result, and first acceptance-hardening result remain
unchanged. This final repair concerns only the provenance disposition of an identical transcript
whose stopping-state field changes.

## Reproduction

An empty `round-robin-to-registry-budget` request with `stopped=False` and an otherwise identical
request with `stopped=True` both pass structural `CollectionRequest` validation. Their collection
digests differ because `stopped` is part of the subject payload. At the reviewed head the classifier
nevertheless returned `same-transcript-recalculation-no-new-evidence` because its same-transcript
branch checked lineage but omitted stopping state. Full collection replay separately and correctly
rejected the toggled request as `mismatched stopping status or rule`.

## Repair and boundary

For an identical transcript, ordinary recalculation now requires both unchanged lineage and
unchanged stopping state. A stopping-state-only change returns `provenance-changed-new-claim`.

The strict-prefix append branch is unchanged. In particular, a correctly replayed successor may
move from `stopped=False` to `stopped=True` when it has the same record identity, a genuinely new
revision identity, and the exact predecessor digest. The classifier records provenance only; full
replay remains authoritative about whether the transcript and final stopping state obey the
built-in rule.

Targeted R4 controls require:

- an identical stopping state to retain ordinary recalculation;
- a stopping-state-only toggle to receive `provenance-changed-new-claim`;
- producer and receiver replay to reject the inconsistent toggle;
- a valid five-to-six-event `round-robin-stop-at-6` successor to replay as stopped and retain
  `append-only-transcript-extension`.

The complete acceptance route reruns R1–R4, M1–M8, scalar PR #12, current family and persistent
checks, current history/version identities, exact PR #12 and inherited PR #10 replay, and negative
controls normally and with `-O`. The hosted result is recorded separately in
`stop_state_hardening_results.json`; the earlier `acceptance_hardening_results.json` remains frozen
and is checked against its original source commit.

## Preserved identities and limits

| File | SHA-256 |
|---|---|
| `foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md` | `be495f29011479adab2736bfbe8f3c3e513403fa48c4886652e8137256d1ccbc` |
| `verification/multistream_collection/results.json` | `2b80b11c691be1c297e71bd2c7016c837a3584389748d42ec06c377bf2da7a93` |
| `verification/multistream_collection/acceptance_hardening_results.json` | `68d500c54a3a4c2848aa365d144eadd182d0b41da84aa34adcf4f29a04e9f357` |

This repair does not change the coverage theorem, affine-box theorem, M1–M8 values, resource
profile, sampling assumptions, or full replay semantics. It adds no adaptive allocation, dynamic
registry, missingness correction, optimization, sequential-control composition, Writ/Decision Lab
change, language migration, formalization, experiment reopening, or release.
