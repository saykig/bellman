# Bellman research history

[GitHub Releases](https://github.com/saykig/bellman/releases) are the preferred human-readable
timeline of Bellman's meaningful research-state transitions. Canonical release-note text is
committed in [`releases/`](releases/), and the exact commit, tree, note, and selected artifact
identities are bound in [`releases/manifest.json`](releases/manifest.json).

The detailed cumulative records remain in [`records/`](records/). Frozen experiments, mathematical
documents, reviews, source manifests, and result records remain authoritative in their existing
locations; release notes only summarize and navigate them. A release publication date may be later
than the underlying research. “Historical finalization” below means the timestamp supported by the
tagged commit, not the date on which GitHub metadata was created.

| Research milestone | Historical date | Standing | Release/tag | Main evidence |
| --- | --- | --- | --- | --- |
| Kahneman Lab experimental and closure arc | 2026-09-06 | Closed with surviving scoped findings and explicit failed branches | `research/kl-closure` | [KL4–KL6 note](releases/kl-closure.md) |
| Mathematical substrate v1.1 and initial build-out | 2026-09-06 | Working foundation; continuing programme | `research/substrate-v1.1` | [Substrate note](releases/substrate-v1.1.md) |
| Finite joint-law completion and exact-reference repair | 2026-09-07 | Bounded construction completed and repaired | `research/joint-law-certificates` | [Joint-law note](releases/joint-law-certificates.md) |
| Sequential certificates, transport, and accumulation | 2026-09-07 | Three bounded constructive modules completed | `research/sequential-certificates` | [Sequential note](releases/sequential-certificates.md) |
| Persistent model families and family-aware replanning | 2026-09-07 | Bounded family-level guarantees completed | `research/persistent-model-families` | [Persistent-family note](releases/persistent-model-families.md) |
| Anytime-valid data-to-decision bridge | 2026-09-07 | Bounded bridge completed; support/CI boundary repaired | `research/anytime-data-decision` | [Anytime note](releases/anytime-data-decision.md) |

The four moved records preserve their prior substantive text, with only relocation-required links
repaired: [findings](records/FINDINGS_LEDGER.md), [retired mathematics](records/MATH_ARCHIVE_LEDGER.md),
[substrate](records/SUBSTRATE_LEDGER.md), and [legacy-source status](records/LEGACY_ARCHIVE_STATUS.md).
The [classification audit](records/CLASSIFICATION.md) records how every section was treated during
the move without turning this page into another cumulative ledger.
