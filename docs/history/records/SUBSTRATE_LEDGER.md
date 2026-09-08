# Substrate Ledger

This is the cumulative index of Bellman's mathematical foundation. Frozen documents remain historical statements under their own assumptions. A frozen draft is not a claim that its mathematics is finished or independently verified. Existing experiment artifacts and the Mathematical Archive Ledger are preserved unchanged.

## Foundation sequence

| Record | Contribution and standing | Durable source |
|---|---|---|
| v1, 6 September 2026 | First seven-component mathematical substrate: joint probability/evidence, information and sequential decisions, representations, approximation/regret, information comparison, model uncertainty, and a separate causal interface. | Exact original source unavailable in this archival pass. Its existence and content are described by the exact review and v1.1; no reconstructed v1 file is supplied. |
| Adversarial review | Retained the central conditional mathematics and recommended focused clarification. Main issues: exact fibers versus outer enclosures; explicit loss, fee, horizon, and support premises; off-support policy execution; numerical error in computed margins; semantic decoder existence versus constructibility; and precise engineering correspondence. | [Frozen exact review](../../../reviews/BELLMAN_SUBSTRATE_V1_ADVERSARIAL_REVIEW.md) |
| v1.1, 6 September 2026 | Focused amendment: separates exact and outer sets; restores nonnegative-loss coupling premises; requires total executable transferred policies; separates model, optimization/evaluation, and coverage errors; clarifies decoders and existing Build 1 scope. **Working foundation, not finished Bellman mathematics.** | [Frozen exact v1.1](../../../foundations/BELLMAN_WRIT_MATHEMATICAL_SUBSTRATE_V1_1.md) |
| Initial next mathematical build-out, 7 September 2026 | Completed additive development draft, frozen before repository packaging. Distinguishes conventions, exact characterizations, and constructive procedures; develops compatibility witnesses, representation/simulation procedures, signed-loss and sequential bounds, persistent uncertainty, and scoped extensions. No novelty requirement or claim of formal proof-library completion. | [Frozen exact build-out](../../../foundations/BELLMAN_NEXT_MATHEMATICAL_BUILDOUT.md) |

The [North Star](../../../foundations/BELLMAN_NORTH_STAR.md) remains: **Make consequential decision-making mathematically inspectable, cumulative, and correctable.** Its first capability is to know exactly what information a representation must preserve for specified future decisions.

## Continuing mathematical programme

Active work includes constructive exact compatibility and identification; discoverable task-relative representations; dependence-aware and online information comparison; conditioning and sequential error composition; solver certificates; persistent robust/Bayesian uncertainty; statistical model learning and time-uniform coverage; constraints, reachability, and tail risk; causal identification; and, where required, multiple objectives and strategic incentives.

The build-out specifies bounded finite procedures and short derivations for these gaps, while identifying what remains an interface or further formalization. More general partial observation, nonlinear model constraints, adaptive data collection, dynamic risk consistency, causal transport, and equilibrium selection remain open development areas. These are not automatic new experiments or selected engineering builds. Historical KL4/KL5/KL6 conclusions and stopping dispositions remain unchanged.

## Verification evidence

- The exact review reports 20 fixed test methods under Python 3.13.5. Its original `fixed_checks.py`, `fixed_check_results.json`, and companion execution/source records were not located. Those claims remain source-reported; this PR neither recreates nor claims to rerun that harness. See [historical verification status](../../../verification/substrate_v1/README.md).
- v1.1 §14.3 reports its own bounded conformance calculations. Its original local harness is also unavailable; those are not this archive's executions.
- The completed build-out's [frozen results](../../../verification/substrate_buildout/checks.json) and [check summary](../../../verification/substrate_buildout/CHECKS.md) record 18 passing illustrative groups under Python 3.9.6: 17 mathematical groups and packet-input integrity. These are example calculations, not independent formal verification, statistical experiments, or production acceptance tests.
- The [portable replay](../../../verification/substrate_buildout/checks.py) retains the mathematical calculation block unchanged. It replaces machine-specific packet access with the archive manifest, checks all six frozen artifacts, and compares the 17 mathematical results with the frozen record. See its [replay notes](../../../verification/substrate_buildout/README.md). It is explicitly not the missing v1 review harness.

## Executable engineering relationship

The first executable Bellman slice is `finite-one-observation.v1` in [`saykig/writ-decision-lab`](https://github.com/saykig/writ-decision-lab). Its [Build 1 specification](https://github.com/saykig/writ-decision-lab/blob/cd8016eda9ccf17ccda4cdb2c37b22f72660bf76/SPEC.md) supplies exact finite rational model/query semantics, signed terminal losses, one optional observation, and all minimizing sets. The [review PR #1](https://github.com/saykig/writ-decision-lab/pull/1) was open at archival inspection, with head `cd8016eda9ccf17ccda4cdb2c37b22f72660bf76`; later reported local repairs are not certified here.

That implementation does not define Bellman's mathematical ceiling. Writ is the engineering/provenance infrastructure intended to progressively embody stable mathematics. Separate implementations may support interface development; permanent repository separation is not a doctrine. Mathematical development may continue beyond current engineering, while an implementation must not claim guarantees outside its specified scope.

## Source identity and archival gaps

The [small source manifest](../../../foundations/SOURCE_MANIFEST.json) records SHA-256 and byte counts for exact artifacts actually obtained. The v1.1, review, and North Star identities match those recorded in the supplied substrate/packet. The completed build-out and its compact results are copied byte-for-byte from the finished mathematical task.

Not included as exact originals: v1; the historical review harness/results and companion log/manifest; v1.1's local conformance harness. No placeholder document or new test script is passed off as any of these. Original upstream audit documents referenced inside the frozen sources are not newly archived by this PR. Packet wrappers, engineering review reports, ZIPs, duplicate copies, local paths, caches, and disposable outputs are excluded. The historical source references inside frozen documents remain historical references; this ledger provides their repository mapping without rewriting their bytes.

## Focused constructive completion — 7 September 2026

The [build-out adversarial review](../../../reviews/BELLMAN_BUILDOUT_ADVERSARIAL_REVIEW.md) identified constructive gaps, numerical-domain premises, maturity overstatement, and evidence limitations. The [additive revision](../../../foundations/BELLMAN_NEXT_MATHEMATICAL_BUILDOUT_REVISED.md) assesses R1–R5 individually; it does not reject a central theorem merely because construction or evidence was incomplete.

The completion supplies precise finite rational compatibility, conditional identification, and decision certificates: full subjects, primal witnesses, dual/Farkas checking, support/inverse checks, and a bounded reference producer with explicit unfinished outcomes. It distinguishes attainable answers from bounds, outer from original feasibility, and assumed premises from checked certificates. Two algebraic proof paths support the sharper conditioning bound, while frozen B15 remains unchanged. Exact fixed cases exercise these constructions; general scalability, nonlinear optimization, certified transcendental radii, and broader temporal/causal/risk mathematics remain active.

Definitions and theorem derivations, fixed-instance execution, and production engineering acceptance remain separate. See [verification](../../../verification/joint_law_completion/README.md) and [source identities](../../../foundations/BUILDOUT_COMPLETION_MANIFEST.json). Author results were recovered and reproduced exactly; reviewer replay passed 19 groups with the temporary packet, and the new module passed 19 fixed cases in normal and optimized modes. The public reviewer replay explicitly skips packet integrity without the excluded ZIP. Earlier missing substrate-v1 originals remain missing.

PR #3 established the first clean substrate archive and was merged externally during this completion. This additive record branches from that existing main history; no old mathematical or KL artifact is rewritten. The external Decision Lab relationship and Bellman's wider mathematical programme remain as stated above. No Writ integration or KL5/KL6 reopening is undertaken.

## PR4 reference-boundary repair — 7 September 2026

Starting from `81fbcc4d503275f091c8c31588ac02d3abf14466`, exact-input witness paths, caller-owned mutable original constraints, and single-action validation shortcuts were independently reproduced and repaired. These are executable premise-enforcement defects; the existing mathematical derivations remain unchanged. The active reference now checks exact witness types, snapshots nested subjects, and validates complete tasks before conclusions. [Additive repair evidence](../../../verification/pr4_repair/README.md) records 13 targeted groups and retention of all 19 existing cases normally and optimized, with no general solver or formal-verification claim. Historical manifests and results resolve against their original commit.

The finish prompt reports recovered v1 and historical review-harness artifacts, but its referenced ZIP/source bytes were inaccessible in this execution. [Recovery status](../../../verification/pr4_repair/recovery_status.json) records the five supplied expected hashes separately from actual verification (not performed). No recovered file or historical rerun is claimed. Earlier unavailable-at-the-time entries remain unchanged; the separate v1.1 conformance harness remains unresolved. The supplied North Star duplicate matched the canonical bytes and was excluded.

## Sequential certificate composition — 7 September 2026

The [additive construction](../../../foundations/BELLMAN_SEQUENTIAL_CERTIFICATE_COMPOSITION.md) proves receiver-checkable optimum lower and policy upper bounds on finite observable-history trees, constructs them from checked residual/greediness allowances, and specifies model-transfer, conditioning, and replanning joins. It retains B13–B17 under explicit premises and preserves counterexamples to marginal-only product bounds, value-only policy transfer, unrelated local regret addition, and nodewise switching of persistent models. Fixed complete-path and policy-enumeration checks are distinguished from the analytical proofs and assumed model/access premises. [Current verification](../../../verification/sequential_certificates/README.md) includes PR4 preservation checks. Historical archive gaps remain unchanged; no recovery pass or closed experiment is reopened. This completes one bounded module, not Bellman's mathematical programme.

## Certificate transport and revalidation — 7 September 2026

The [additive construction](../../../foundations/BELLMAN_CERTIFICATE_TRANSPORT_AND_REVALIDATION.md) derives target certificates from checked source bounds on the same completed observable-history skeleton. It proves lower/upper correction recurrences and pointwise extremality only within the old-table anchors, distinguishes ordinary target validity from transport provenance, and binds conditioning to a target-induced positive prefix probability. Comparator change, union-support fallback, and overlapping-replan cases retain the necessary composition boundaries. [New fixed evidence](../../../verification/certificate_transport/README.md) is separate from PR5 and reviewer-reported runs. PR5 merged before this work; its reviewed tree is unchanged in the pinned main base. No historical theorem, result, experiment, or archive-gap record is rewritten. Scalable procedures, richer mathematics and future justified engineering remain active beyond this bounded module.

## Certificate accumulation — 7 September 2026

The [additive construction](../../../foundations/BELLMAN_CERTIFICATE_ACCUMULATION_AND_POLICY_SELECTION.md) proves same-subject/same-policy max-lower/min-upper closure and table laws, plus separately checked policy selection. Actual dominance requires checked exact policy values; loose-bound selection does not suffice. Retained warrants tighten a restored-subject round trip without changing PR6. New fixed evidence and preservation runs remain distinct from historical/reviewer records. The broader programme continues beyond this finite module.

## Persistent model-family certificates — 7 September 2026

The [additive construction](../../../foundations/BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md) retains alternative models as fixed whole-episode members and certifies one accessible total policy member by member before paired aggregation. Separate exact matrix checks distinguish common modelwise optimality, deterministic minimum worst loss, deterministic minimum worst regret, and best-in-subset claims. Positive-prefix continuation retains only supported members with explicit zero-mass exclusions and no inferred weights. [Fixed exact evidence](../../../verification/persistent_model_families/README.md) preserves PR7 and the inherited checks. The PR5 certificate-soundness theorem is now a candidate for a later narrowly scoped Lean feasibility check; no formalization work or toolchain is started here.

## Family-aware replanning and root guarantees — 7 September 2026

The [additive construction](../../../foundations/BELLMAN_FAMILY_REPLANNING_AND_ROOT_GUARANTEES.md) derives one ordinary certificate after a complete single-subtree policy splice in every fixed model. Signed ancestor corrections use the baseline path mass; root cost and paired-regret caps retain every model, including zero-mass conditional exclusions. Submitted-certificate preservation, conditional preference, exact policy change, and candidate-class optimality remain separate warrants. [Fixed exact evidence](../../../verification/family_replanning/README.md) preserves PR8 and the inherited execution chain. This bounded reference adds no solver, model weights, rectangularization, dynamic-consistency claim, Writ/Decision Lab change, or reopened experiment.

## Anytime-valid Bernoulli data-to-decision bridge — 7 September 2026

The [additive construction](../../../foundations/BELLMAN_ANYTIME_VALID_DATA_TO_DECISION.md) proves a
summably allocated exact-binomial interval covers one fixed real Bernoulli parameter at every
inspection with probability at least `1-alpha`, under the explicitly supplied IID premise. Exact
rational root brackets are checked independently from bisection and enlarged outward. A separate
static decision certificate checks all affine risk differences and named-action regret over that
retained interval. [Fixed exact evidence](../../../verification/statistical_decision_bridge/README.md)
includes repeated-inspection arithmetic, dependence and revision controls, an existing joint-law
cross-check, producer-disabled receiving, and the complete inherited PR #10 preservation chain.
Sampling validity, adaptive collection, drift, causal meaning, empirical usefulness, authority,
and Writ/Decision Lab integration remain separate and unestablished.

## PR12 acceptance hardening — 7 September 2026

The reviewed statistical companion and original result record remain frozen. A reproduced
execution mismatch allowed hand-authored, mathematically valid certificates beyond the public
128-observation, four-action, and 64-requested-precision profile to bypass producer refusal through
receiver entry points. The [additive hardening](../../../verification/statistical_decision_bridge/ACCEPTANCE_HARDENING.md)
applies that request profile before receiver tail or risk arithmetic and preserves resource refusal
as `unfinished`, not invalidity. Current statistical, family-replanning, and persistent-family
checks run normally and optimized; PR #10's complete historical chain still runs unchanged at its
pinned merge. The probability and affine-decision proofs, large derived proof coordinates, and
historical result bytes are unchanged. This is acceptance maintenance, not a new mathematical
stage or an engineering transfer.

## Controlled multistream collection and static decisions — 7 September 2026

The [additive construction](../../../foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md) composes
PR #12's scalar all-prefix intervals over a fixed finite registry. A checked built-in collector
reveals each selected stream's next unused event; the receiver replays global/local indices and
applies a fixed-allocation union bound. The random-count conclusion follows from simultaneous
prefix-event inclusion, not from a generally false conditional-binomial claim, and it does not
require cross-row independence. Exact signed affine population risks are then checked over the
retained rectangle, while conditional fresh-draw and marginal-only joint-event queries retain
their extra-premise boundaries. [Fixed exact evidence](../../../verification/multistream_collection/README.md)
includes scalar reduction, complete adaptive-path and rectangle-corner checks, filtering and
dependence counterexamples, producer-disabled receiving, finite refusal semantics, and PR #12's
complete historical acceptance replay at its original base. This is a bounded research reference,
not empirical sampling validation, an optimized bandit, sequential control, or a Writ/Decision Lab
transfer.

## PR14 acceptance hardening and current-main synchronization — 7 September 2026

The [additive repair](../../../verification/multistream_collection/ACCEPTANCE_HARDENING.md)
reproduces and closes two public-constructor subject-erasure paths: unregistered allocation keys
and unregistered affine coefficients must reject before registry-order canonicalization. It also
binds record, revision, and predecessor lineage in collection-revision classification. The
mathematical companion and original result record retain their reviewed SHA-256 identities, while
a separate hardening result records current code. PR #13's moved history records, migration
manifest, classification, and root cleanup remain in force; PR #15's versioned historical releases
and lightweight-tag checks are preserved. Findings and substrate records permit only append-only
entries after their frozen migrated prefixes. Current and historical acceptance retain the PR #12
and inherited PR #10 replay boundaries. No mathematical stage, GitHub Release, Writ/Decision Lab
integration, or language migration is added.

## Statistical rectangle to sequential corner-model guarantees — 7 September 2026

The [additive construction](../../../foundations/BELLMAN_STATISTICAL_RECTANGLES_TO_CORNER_MODEL_GUARANTEES.md)
composes PR #14's checked simultaneous outward rectangle with PR #8's persistent whole-episode
family semantics. A pathwise no-repeat condition makes every fixed deterministic policy cost
multi-affine, so expected-loss and covered-class modelwise-regret extrema are exactly attained by
the at most four corners. The [bounded receiver](../../../verification/statistical_corner_models/README.md)
checks explicit stream-to-transition mapping, reconstructs completed corner subjects, invokes the
unchanged persistent-family consumer, and cross-checks exact forward paths and complete tiny policy
selection. It preserves all prior result and version identities through pinned PR #14/PR #12/PR
#10 replay.

The `p(1-p)` construction records the sharp boundary: repeated use of one uncertain parameter on
one path can move the maximum into the interior. Such a subject is not impossible; this particular
corner warrant is invalid. More than two parameters is separately `unfinished` in the executable
profile. No empirical premise validation, randomized policy, continuous optimizer, Writ/Decision
Lab transfer, language migration, dynamic risk, causal result, or formal proof is claimed.

## Unsafe-set reachability and constrained deterministic selection — 8 September 2026

The [additive companion](../../../foundations/BELLMAN_UNSAFE_SET_REACHABILITY_AND_CONSTRAINED_SELECTION.md)
adds one bounded risk/constraint object without changing the expected-additive sequential substrate.
For an identified unsafe-history set, one complete deterministic policy's exact ever-hit
probability is computed by backward absorption and independently checked by disjoint first-hit
paths. Persistent-family aggregation keeps model identities and one common policy. Exact finite
selection filters one fixed robust-feasible class before minimax loss and same-model regret
comparisons; FULL and subset empty classes retain different conclusions.

The statistical adapter invokes the existing rectangle/mapping/admissibility receiver before any
safety conclusion. Under the inherited pathwise condition, first-hit probabilities are
multi-affine and their maxima occur at the completed corners. Statistical coverage failure,
model-implied harm probability, and numerical precision remain distinct. The [bounded exact
evidence](../../../verification/unsafe_set_reachability/README.md) preserves PR #16 and the full
historical replay chain. Resource constraints, tail distributions/CVaR, dynamically consistent
risk, randomized feasibility, larger optimization, empirical model/unsafe-set validity, authority,
formalization, and Writ/Decision Lab transfer remain open.

## Finite causal intervention identification and decisions — 8 September 2026

The [additive construction](../../../foundations/BELLMAN_FINITE_CAUSAL_IDENTIFICATION_AND_DECISION_CERTIFICATION.md)
makes the build-out's causal interface executable in two deliberately small profiles. Exact finite
adjustment remains conditional on supplied consistency, exchangeability, pre-action, adjustment-
set, and positivity premises; the checker does not infer those premises from observational bytes.
The response-type route uses the eight binary `(A_nat,Y0,Y1)` masses, observed consistency, and a
typed monotonicity/equality restriction library. Complete rational vertex enumeration establishes
exact compatibility, point/partial intervention bounds, and attaining witnesses; unsupported
nonlinear assumptions and explicit outer relaxations keep different statuses.

Paired one-stage action-risk maxima preserve one common causal model. The fixed evidence includes
the exact Simpson reversal, a positivity failure, 16-vertex partial identification with ranges
`[1/4,3/4]`, point-identifying calibrations, a uniformly identified action despite nonpoint causal
probabilities, opposite model-dependent action witnesses, and a supported inconsistent fibre. The
receiver independently reconstructs adjustment arithmetic and enumerates the full response-type
fibre with producers disabled. All prior artifacts and the PR #17 historical chain remain frozen.
Transport, time-varying intervention semantics, sequential exchangeability, adaptive-policy
support, broader causal restrictions, and empirical premise criticism remain open before any
causal-to-sequential composition.

## Two-stage longitudinal causal policy and sequential bridge — 8 September 2026

The [additive construction](../../../foundations/BELLMAN_TWO_STAGE_LONGITUDINAL_CAUSAL_POLICY_AND_SEQUENTIAL_BRIDGE.md)
adds the first conditional bridge from a fully identified longitudinal causal law to Bellman's
existing sequential subject. It uses an exact 16-cell binary `P(A1,L1,A2,Y)` and names population,
coding, temporal order, consistency/intervention, sequential-exchangeability, adaptation, and
no-interference premises. A complete policy retains actions at all four structural second-stage
histories even though only two follow its chosen root.

The policy receiver requires support only for the policy's selected actions at positive regime
histories. Full-subject construction separately requires every first action, intermediate value,
and second action to be supported. With that warrant, the adapter constructs the existing 21-node
subject and checks all 32 policies through the unchanged sequential certificate consumer and
independent path enumeration. Causal and Bellman distributions, values, and complete minimizing
sets agree exactly.

The preserved two-world counterexample holds both static `do(A2)` outcome marginals fixed at
`1/2` while reversing the optimal `L1`-adapted policy, so the merged one-stage causal output is not
silently reused as a transition kernel. The [exact verification](../../../verification/longitudinal_causal_policy/README.md)
binds observation, population, coding, timing, premises, policies, loss, subject, catalogue, and
queries, and receives retained evidence with producers disabled. Longitudinal causal fibres under
missing support, transport, safety/persistent-family composition, broader stages, empirical
premise validation, formalization, and engineering transfer remain open. Enumeration stayed at 32
policies; no solver or language trigger was reached.

## Longitudinal causal kernel fibres and persistent decisions — 8 September 2026

The [additive construction](../../../foundations/BELLMAN_LONGITUDINAL_CAUSAL_KERNEL_FIBRES_AND_PERSISTENT_DECISIONS.md)
extends the merged two-stage bridge without changing its point-identified semantics. Under positive
first-action and intermediate-history support, supported second-stage outcome rows remain fixed and
each unsupported binary row becomes one explicitly ordered `[0,1]` coordinate under a saturated
no-cross-row-restriction profile. This Cartesian product is exact only for that declared
interventional-kernel interface; stronger cross-row SCM assumptions are unsupported rather than
silently dropped.

Policy risk, exact additive loss, and same-completion pairwise differences are multi-affine, so a
separate finite corner family exactly represents extrema and the derived deterministic common,
minimax-loss, and same-model-regret queries. It is not the continuous fibre. A `q(1-q)` control
records the decisive arbitrary-nonlinear-query boundary. The one-gap, changed-cost, two-gap, and
zero-gap controls distinguish point policies, partial policies, model-dependent decisions, common
decisions, and separately supplied robust choices while retaining all off-root policy identities.

The [exact verification](../../../verification/longitudinal_causal_kernel_fibres/README.md)
independently reconstructs up to four missing rows, 16 corners, 32 policies, and 512 exact policy
values. The historical persistent receiver is reused for at most four corners; its model limit is
exposed rather than modified for larger bounded cases. PR #20 collapses exactly at dimension zero,
earlier-stage support failures are not fabricated, and retained evidence is checked with candidate
producers disabled. No empirical premise validation, transport, estimation, safety composition,
randomized policy, engineering transfer, solver, formalization, or language trigger is claimed.
