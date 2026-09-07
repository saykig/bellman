# v0.0.5 — Persistent model-family certificates and family-aware replanning

Historical period: 2026-09-07

Historical finalization: 2026-09-07T15:50:56-04:00

Tagged commit: `2e8d99cdcf289eabb63df15086eaa68251a359f1`

Git tree: `65f95c850d63e10a7a3f78f9c1d3c6b322f0d08d`

Standing: Bounded family-level policy and one-splice replanning guarantees completed.

Publication note: This historical checkpoint was indexed and published later. Its target commit and
tree—not the GitHub publication timestamp—are the authority for its historical date and state.

## Question

Bellman asked how to retain alternative whole-episode models without inventing weights or allowing
hidden model switches, certify one accessible policy across every family member, distinguish
several robust selection criteria, and replan one subtree without losing an established root bound.

## What we tried

The persistent-family module checked a single total deterministic policy member by member and then
aggregated paired bounds. Separate exact matrices represented common modelwise optimality,
deterministic minimax loss, deterministic minimax regret, and best-in-subset claims. Conditioning
filtered only positive-prefix members. The replanning module spliced one complete continuation
policy, propagated signed ancestor corrections using baseline path mass, and checked submitted-cap,
exact-change, conditional-preference, and candidate-class warrants separately.

## What worked

One implementable policy can be certified across a finite persistent family without averaging the
models. Positive-prefix continuation can retain supported members while explicitly recording
zero-mass exclusions. A complete single-subtree splice can preserve an ex-ante root cap in every
fixed member, including members excluded from the conditional comparison, and can separately
establish exact policy change and candidate-class properties where evidence suffices.

## What failed or was falsified

Nodewise selection of a different favorable model is not a certificate for a persistent family.
Common optimality, minimax loss, minimax regret, and restricted candidate optimality are not
interchangeable. A conditional preference among positive-mass members does not erase zero-mass
members from the root guarantee, and submitted upper-bound improvement is not automatically exact
policy improvement. Overlapping replacement effects cannot be added without a valid composition
argument.

## What stopped or closed

The reference stopped at finite families, deterministic policies, and one subtree splice. It added
no prior, model learner, randomized-policy optimum, optimizer, rectangularization, dynamic-
consistency theorem, generic transport, new language, or external integration.

## What survived

Persistent whole-episode identity, one accessible total policy, paired memberwise certificates,
criterion-specific selection, support-filtered conditional scope, baseline occupancy, and explicit
root-versus-conditional obligations became the standing family discipline.

## Verification and evidence

- [Persistent-family construction](https://github.com/saykig/bellman/blob/2e8d99cdcf289eabb63df15086eaa68251a359f1/foundations/BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md) and [result](https://github.com/saykig/bellman/blob/2e8d99cdcf289eabb63df15086eaa68251a359f1/verification/persistent_model_families/results.json)
- [Family-replanning construction](https://github.com/saykig/bellman/blob/2e8d99cdcf289eabb63df15086eaa68251a359f1/foundations/BELLMAN_FAMILY_REPLANNING_AND_ROOT_GUARANTEES.md) and [result](https://github.com/saykig/bellman/blob/2e8d99cdcf289eabb63df15086eaa68251a359f1/verification/family_replanning/results.json)
- Merged evidence: [PR #8](https://github.com/saykig/bellman/pull/8) and [PR #10](https://github.com/saykig/bellman/pull/10); [PR #9](https://github.com/saykig/bellman/pull/9) and [PR #11](https://github.com/saykig/bellman/pull/11) supplied living programme context, not additional frozen mathematics.

## Known gaps

The proofs and fixed checks were finite and shared arithmetic/authorship. They did not validate the
supplied model family, information access, objectives, or authority. Bayesian weights, randomized
policies, scalable computation, multiple replans, and dynamic-consistency conditions remained out
of scope. A narrowly scoped formalization feasibility question was noted but not started.

## Direction after this milestone

The programme next tested a statistical-to-decision join: an anytime-valid uncertainty set from an
explicit sampling premise, followed by a separate exact action certificate, while keeping coverage
error and loss regret distinct.
