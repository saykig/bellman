# Sequential certificates, transport, and accumulation

Historical period: 2026-09-07

Historical finalization: 2026-09-07T13:21:21-04:00

Tagged commit: `9761cd0ce99be6fb6b2dcddc89951960a4a0df34`

Git tree: `15c4e5f2c9cfaab947f2c2954f017863bd4ea5c8`

Standing: Three bounded exact construction modules completed with inherited preservation checks.

## Question

Bellman asked when nodewise exact evidence proves a whole-policy guarantee, how such a guarantee can
be revalidated after an explicit model or policy revision, and when several certificates can be
combined or used to select a policy without overstating what their bounds establish.

## What we tried

The sequential module derived separate optimum-lower and named-policy-upper tables by backward
induction and residual/greediness propagation. Transport constructed target bounds on the same
completed history skeleton using signed lower/upper corrections and target support. Accumulation
took pointwise maximum lower bounds and minimum same-policy upper bounds, then treated policy
selection as a separate warrant requiring exact values or independently sufficient evidence.

## What worked

The constructions yield receiver-checkable finite rational whole-policy regret bounds, exact
conditioning and replanning joins under their premises, target-model revalidation, and valid
same-subject/same-policy certificate closure. Fixed examples independently enumerate tiny policies
or sum complete paths, including the exact `5/8` regret case. Current runners preserved the earlier
joint-law/repair evidence and compared normal with optimized execution.

## What failed or was falsified

Root actions do not substitute for complete policies. Marginal-only product bounds, value-only
policy transfer, unrelated local regret addition, candidate-only agreement, and sums of overlapping
predecessor edits do not establish the corresponding sequential claims. Loose bounds alone cannot
prove actual dominance between different policies; direct revalidation and transport envelopes have
no universal tightness ordering.

## What stopped or closed

No closed KL experiment was reopened. The modules stopped at finite completed observable-history
trees and explicitly did not claim scalable optimization, an efficiency advantage, independent
authorship, empirical validity, or a Writ/Decision Lab integration.

## What survived

Separate optimum and policy bounds, total accessible policies, signed exact costs, support-aware
conditioning, explicit comparator coverage, target provenance, and same-policy accumulation became
the reusable certificate discipline. Persistent whole-episode model identity remained the next
unresolved composition target.

## Verification and evidence

- [Sequential construction](https://github.com/saykig/bellman/blob/9761cd0ce99be6fb6b2dcddc89951960a4a0df34/foundations/BELLMAN_SEQUENTIAL_CERTIFICATE_COMPOSITION.md) and [result](https://github.com/saykig/bellman/blob/9761cd0ce99be6fb6b2dcddc89951960a4a0df34/verification/sequential_certificates/results.json)
- [Transport construction](https://github.com/saykig/bellman/blob/9761cd0ce99be6fb6b2dcddc89951960a4a0df34/foundations/BELLMAN_CERTIFICATE_TRANSPORT_AND_REVALIDATION.md) and [result](https://github.com/saykig/bellman/blob/9761cd0ce99be6fb6b2dcddc89951960a4a0df34/verification/certificate_transport/results.json)
- [Accumulation construction](https://github.com/saykig/bellman/blob/9761cd0ce99be6fb6b2dcddc89951960a4a0df34/foundations/BELLMAN_CERTIFICATE_ACCUMULATION_AND_POLICY_SELECTION.md) and [result](https://github.com/saykig/bellman/blob/9761cd0ce99be6fb6b2dcddc89951960a4a0df34/verification/certificate_accumulation/results.json)
- Merged evidence: [PR #5](https://github.com/saykig/bellman/pull/5), [PR #6](https://github.com/saykig/bellman/pull/6), and [PR #7](https://github.com/saykig/bellman/pull/7)

## Known gaps

The references were intentionally limited to small finite trees (including bounded horizons, nodes,
actions, outcomes, and optional enumeration). They shared Python `Fraction` arithmetic and
authorship; alternate calculation paths were not independent proof. No unavailable legacy harness
or packet was claimed rerun, and the executions did not validate model, access, loss, or control
premises.

## Direction after this milestone

The programme next retained uncertainty over fixed whole-episode model families and asked for one
implementable policy and later replanning guarantees without switching models node by node.
