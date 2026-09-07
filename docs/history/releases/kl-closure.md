# v0.0.1 — Kahneman Lab experimental and closure arc

Historical period: 2026-09-02 through 2026-09-06

Historical finalization: 2026-09-06T19:28:32-04:00

Tagged commit: `145dbb17d928ccbe36b6a3454f979fd7dbeb963c`

Git tree: `127e106e54b8c34a32496191fbfcd88867a254da`

Standing: Closed experimental arc with scoped positive findings, falsified shortcuts, and explicit stop dispositions.

Publication note: This historical checkpoint was indexed and published later. Its target commit and
tree—not the GitHub publication timestamp—are the authority for its historical date and state.

## Question

Bellman tested which information summaries preserve specified decisions, whether common uncertainty
or information scores predict decision value and stability, and whether one-step decision answers
could serve as a sufficient certificate for bounded sequential decisions.

## What we tried

KL4 ran four preregistered finite exact lanes: mutual information versus decision value, uncertainty
width versus action stability, query-relative summary quotients, and finite-horizon stopping. KL5's
registered Stage R exhaustively searched its primary and mandatory interior grids for models equal
under increasingly strong one-step certificates but separated by later STOP/OBSERVE decisions. KL6
then audited the proposed `S04=(C_*,Z_5)` representation on its registered eighth-grid domain and
compared the remaining frontier with established theory.

## What worked

KL4 produced scoped counterexamples showing that mutual-information rankings need not match
decision-value rankings, probability-width rankings need not match decision stability, sufficiency
is relative to a specified query family, and entropy or one-step value alone does not determine a
finite-horizon stopping decision. KL5 found 64 primary equal-`C_*` separating pairs, with the first
separation at horizon two. KL6 proved that `S04` preserves the registered targets on its domain.

## What failed or was falsified

The candidate shortcuts were not general decision guarantees. KL5's mandatory informative
quarter-grid interior gate found no separating `C_*` pair among 144 candidate models, so its main
lane did not open. KL6 showed that `S04` worked there only because it reconstructed the labeled
observation kernel; it was not genuine compression. The claim that bounded-error
decision-preserving representations were an open foundational frontier did not survive the later
theory audit.

## What stopped or closed

KL5 stopped at Stage R with `KL5_STOP_DEGENERATE`. KL6 closed with
`KL6_STOP_THEORY_ALREADY_SETTLES` / `KL6_STOP_STANDARD`. The observation-compression continuation
closed with `FRONTIER_STOP_EXISTING_THEORY_SUFFICES`; no automatic KL7 or grid expansion was
authorized. Earlier KL2 D0/D1 architecture claims and KL3v2's distinct preparation method remained
retired rather than being rescued by these experiments.

## What survived

Decision sufficiency survived as a property relative to an explicit query family. Exact
counterexamples, complete minimizing sets, support/`NA` distinctions, and closure rules remained
useful. A bounded economic question—finding the smallest or cheapest representation for a fixed
query and guarantee—remained available, but not as the default roadmap.

## Verification and evidence

- [KL4 preregistration](https://github.com/saykig/bellman/blob/145dbb17d928ccbe36b6a3454f979fd7dbeb963c/experiments/kl4/RUN_THIS_NEXT_KAHNEMAN_LAB_4_PARALLEL.md) and [frozen synthesis](https://github.com/saykig/bellman/blob/145dbb17d928ccbe36b6a3454f979fd7dbeb963c/experiments/kl4/kahneman_lab_4S_parallel_synthesis.md)
- [KL5 preregistration](https://github.com/saykig/bellman/blob/145dbb17d928ccbe36b6a3454f979fd7dbeb963c/experiments/kl5/RUN_THIS_NEXT_KAHNEMAN_LAB_5_SEQUENTIAL_SUFFICIENCY.md) and [Stage R report](https://github.com/saykig/bellman/blob/145dbb17d928ccbe36b6a3454f979fd7dbeb963c/experiments/kl5/kahneman_lab_5R_replication_gate.md)
- [KL6 closure and source-identity record](https://github.com/saykig/bellman/blob/145dbb17d928ccbe36b6a3454f979fd7dbeb963c/experiments/kl6/README.md)
- Merged evidence: [PR #1](https://github.com/saykig/bellman/pull/1) and [PR #2](https://github.com/saykig/bellman/pull/2)

## Known gaps

KL2 and KL3 canonical source identities were unresolved. The exact binding KL6 replacement bytes,
reported as SHA-256 `31a4fb8bfcfbb7e9c4753866628c7784bf769d560d6716e21e878d22bf3d47f2`,
were not migrated; the committed KL6 README is a status record, not a substitute original. The
finite grids and exact checks do not establish unrestricted empirical or mathematical claims.

## Direction after this milestone

The programme redirected from inventing a new observation-compression object toward assembling and
making established decision mathematics explicit, composable, and inspectable. Closed experimental
branches remained available as negative evidence, not as instructions to reopen them.
