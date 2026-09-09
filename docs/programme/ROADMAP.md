# Bellman Programme Roadmap

**Status:** living programme-steering document. This is not a frozen theorem, experiment result, or mathematical authority. Update it when evidence changes the best route.

**Current snapshot:** merged PR #22 and causal PR #21 form the frozen v0.0.7 mathematical
release at `2cd6fd7432efccaacc734fd235549a564ddbff48`. Their results retain their bounded,
author-reviewed standing. The later FSD and AFY cases add empirical observations and bounded
prediction comparisons with explicit identification and transfer limits. [Current acceptance](../../verification/beliefs_acceptance/README.md)
preserves and checks both checkpoints; it establishes neither a causal-to-strategic bridge nor
empirical validation of equilibrium consistency.

The governing North Star remains [Bellman North Star](../../foundations/BELLMAN_NORTH_STAR.md):

> **Make consequential decision-making mathematically inspectable, cumulative, and correctable.**

Bellman should become progressively better at saying what a decision problem means mathematically, what follows under its assumptions, what can be reused or combined, what must be rechecked after change, and where the guarantee stops.

The next bounded capability is now a [measurement-to-decision menu](../../research/measurement_decision/README.md):
finite supplied-prior Bayesian loss plus observation costs, with a no-measurement
baseline and one persistent hidden state. Two stipulated cases use the existing
exact observation engine. Informative signals can have zero decision value; a
conditional-response report can help while utility information helps more. This
does not identify human priors, calibrate report noise or resolve robust ambiguity.
The stopping gate is exact menu selection and independently checked conditional
claims; empirical adoption awaits a warranted channel, utility scale and costs.
No additional empirical fitting or product transfer follows automatically.
[Current additive acceptance](../../verification/measurement_acceptance/README.md)
preserves the completed AFY edition and replays its inherited checks.

## 1. How to read this roadmap

This is a **capability roadmap, not a checklist of fields to complete**. A line may be skipped, reordered, simplified, or closed if established mathematics already settles it, a counterexample kills the proposed route, or engineering/domain work reveals a better frontier.

Progress does **not** require mathematical novelty. A known theorem becomes useful Bellman mathematics when its object, assumptions, operation, guarantee, composition rule, failure boundary, and provenance are made explicit enough to check and reuse.

The programme should change course when the evidence warrants it. Changing course is not drifting from the North Star if the change improves our ability to make decision reasoning inspectable, cumulative, and correctable.

## 2. Named capability snapshot

Earlier versions gave percentage-complete estimates for a first finite core and for the wider
programme. Those estimates had no justified fixed denominator. Replacing them with named earned
capabilities and outstanding obligations is a measurement clarification, not a claim that progress
was lost. The earlier wording remains preserved in Git history.

### First finite executable chain

The bounded chain from exact model compatibility through sequential guarantees, persistent-model
uncertainty, one complete family-aware continuation splice, and the first admissible statistical-
rectangle composition now has explicit mathematical constructions and exact reference checks.

Earned so far:

1. exact compatible-model fibres versus outer enclosures;
2. finite rational compatibility, identification, and checked decision certificates;
3. whole-policy sequential certificates and regret composition;
4. target revalidation after explicit model or policy change;
5. accumulation of compatible certificates and checked policy selection;
6. one implementable policy across persistent whole-episode model families;
7. explicit support-filtered continuation without hidden model switching or fabricated model weights;
8. a complete single-cut family-aware replanning certificate with separate root-cap and exact-policy-change warrants.
9. an exact bridge from an admissible two-parameter statistical rectangle to persistent sequential
   corner models for whole-policy deterministic loss and regret.
10. exact unsafe-history hitting probability, persistent-family robust safety caps, and deterministic
    expected-loss/regret selection within one fixed robust-feasible policy class, including an
    admissible statistical-corner composition.
11. exact one-stage finite adjustment under supplied causal premises, exact binary response-type
    point/partial identification, and same-causal-fibre deterministic action certification.
12. conditional identification of one two-stage adapted deterministic regime, with a separate
    stronger-support warrant for constructing and checking the complete 32-policy Bellman subject.
13. an exact continuous saturated completion fibre for missing binary second-stage outcome rows,
    with query-specific corner reduction and distinct common-optimal, model-dependent, and robust
    deterministic decisions.

### Wider Bellman mathematical programme

Outstanding areas remain explicit rather than compressed into a percentage: statistical learning
beyond the first IID Bernoulli bridge; adaptive sampling, dependence, drift, missingness and model
criticism; resource/operational constraints and tail/dynamic risk beyond the first unsafe-set
primitive; causal transport, time-varying intervention semantics, and wider identification;
richer structural transport; scalable
optimization; plural objectives; strategic actors; and selected formal verification.

## 3. Completed and hardened capability chain

| Capability | Standing | Main mathematical record | What it earns |
|---|---|---|---|
| Working substrate | FOUNDATION | [`BELLMAN_WRIT_MATHEMATICAL_SUBSTRATE_V1_1.md`](../../foundations/BELLMAN_WRIT_MATHEMATICAL_SUBSTRATE_V1_1.md) | Seven-component working foundation and composition discipline. Not finished Bellman mathematics. |
| Exact joint-law compatibility and decision certificates | HARDENED | [`BELLMAN_NEXT_MATHEMATICAL_BUILDOUT_REVISED.md`](../../foundations/BELLMAN_NEXT_MATHEMATICAL_BUILDOUT_REVISED.md) | Exact/outer separation, witnesses, bounds, infeasibility certificates, conditional queries, checked finite decisions. |
| Sequential whole-policy guarantees | HARDENED | [`BELLMAN_SEQUENTIAL_CERTIFICATE_COMPOSITION.md`](../../foundations/BELLMAN_SEQUENTIAL_CERTIFICATE_COMPOSITION.md) | Nodewise inequalities become whole-policy bounds; conditioning and replanning boundaries are explicit. |
| Certificate transport and revalidation | HARDENED | [`BELLMAN_CERTIFICATE_TRANSPORT_AND_REVALIDATION.md`](../../foundations/BELLMAN_CERTIFICATE_TRANSPORT_AND_REVALIDATION.md) | A changed model or policy gets a new checked guarantee rather than inheriting an old label. |
| Certificate accumulation and policy selection | HARDENED | [`BELLMAN_CERTIFICATE_ACCUMULATION_AND_POLICY_SELECTION.md`](../../foundations/BELLMAN_CERTIFICATE_ACCUMULATION_AND_POLICY_SELECTION.md) | Compatible checked results can strengthen one another; different-policy selection creates and checks a new policy. |
| Persistent model families | HARDENED | [`BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md`](../../foundations/BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md) | One accessible policy is evaluated across alternative whole-episode models; loss, regret, model identity, support, and criteria remain distinct. |
| Family-aware replanning and root guarantees | HARDENED | [`BELLMAN_FAMILY_REPLANNING_AND_ROOT_GUARANTEES.md`](../../foundations/BELLMAN_FAMILY_REPLANNING_AND_ROOT_GUARANTEES.md) | One complete continuation splice produces checked modelwise certificates; conditional preference, cap preservation, and exact policy change remain separate. |
| Anytime-valid Bernoulli data-to-decision bridge | HARDENED | [`BELLMAN_ANYTIME_VALID_DATA_TO_DECISION.md`](../../foundations/BELLMAN_ANYTIME_VALID_DATA_TO_DECISION.md) | One complete IID Bernoulli prefix yields checked all-time outward coverage and exact static decisions; PR #12 aligns producer/receiver support and historical replay. |
| Controlled multistream collection | HARDENED | [`BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md`](../../foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md) | Fixed-registry adaptive collection retains rowwise all-prefix coverage, exact simultaneous rectangles, and checked static affine decisions; PR #14 closes subject/revision acceptance findings. |
| Statistical rectangles to sequential corner models | HARDENED | [`BELLMAN_STATISTICAL_RECTANGLES_TO_CORNER_MODEL_GUARANTEES.md`](../../foundations/BELLMAN_STATISTICAL_RECTANGLES_TO_CORNER_MODEL_GUARANTEES.md) | Under a pathwise multi-affine warrant, continuous rectangle uncertainty for deterministic whole-policy loss and regret is represented exactly by the finite persistent corner family. |
| Unsafe-set reachability and constrained selection | HARDENED | [`BELLMAN_UNSAFE_SET_REACHABILITY_AND_CONSTRAINED_SELECTION.md`](../../foundations/BELLMAN_UNSAFE_SET_REACHABILITY_AND_CONSTRAINED_SELECTION.md) | Exact first-hit probability, unweighted persistent-family safety caps, and deterministic selection within one fixed robust-feasible class. |
| Finite causal identification and one-stage decisions | HARDENED | [`BELLMAN_FINITE_CAUSAL_IDENTIFICATION_AND_DECISION_CERTIFICATION.md`](../../foundations/BELLMAN_FINITE_CAUSAL_IDENTIFICATION_AND_DECISION_CERTIFICATION.md) | Exact adjustment under supplied premises, exact response-type point/partial identification, and paired same-fibre one-stage action certification. |
| Two-stage longitudinal causal policy and sequential bridge | HARDENED | [`BELLMAN_TWO_STAGE_LONGITUDINAL_CAUSAL_POLICY_AND_SEQUENTIAL_BRIDGE.md`](../../foundations/BELLMAN_TWO_STAGE_LONGITUDINAL_CAUSAL_POLICY_AND_SEQUENTIAL_BRIDGE.md) | Policy-specific g-formula identification remains distinct from the stronger support required to identify every transition of the complete Bellman subject. |
| Longitudinal causal kernel fibres and persistent decisions | HARDENED | [`BELLMAN_LONGITUDINAL_CAUSAL_KERNEL_FIBRES_AND_PERSISTENT_DECISIONS.md`](../../foundations/BELLMAN_LONGITUDINAL_CAUSAL_KERNEL_FIBRES_AND_PERSISTENT_DECISIONS.md) | Missing second-stage binary outcome rows form an exact saturated continuous fibre; proved multi-affine deterministic queries reduce to corners without identifying the finite family with the fibre. |

`HARDENED` here means: the bounded construction has survived targeted adversarial review and exact reference checks within its stated profile. It does **not** mean universal correctness, empirical validity, formal verification, scalability, or final engineering acceptance.

## 4. Current frontier

### Integrated component — sequential credibility with a shared consistency witness

The [sequential credibility companion](../../foundations/BELLMAN_SEQUENTIAL_CREDIBILITY_UNDER_UNCERTAINTY.md)
connects all four strategic directions through one query: continuation deviation gains under
uncertainty, with selective evidence, explicit remembered information, and bond/monitoring rules.
The preliminary exact reference checks one supplied profile across a finite persistent game family
and all information sets. Its assessment-relative result remains frozen. The additive
[consistency theorem](../../foundations/BELLMAN_SEQUENTIAL_CREDIBILITY_CONSISTENCY_ADDENDUM.md)
now supplies the missing constructive bridge: a common rational power-perturbation witness must
generate every model's assessed beliefs simultaneously. At epsilon=0, independent exact
polynomial and full-continuation checks establish modelwise sequential equilibrium with a shared
consistency witness. Positive epsilon yields only a consistent continuation-gain bound.

The original four-model/20-information-set fixture now has a checked common witness. Two exact
counterexamples distinguish local assessed rationality from consistency, and individual model
consistency from a shared sequence. The [research audit](../../reviews/SEQUENTIAL_CREDIBILITY_RESEARCH_REVIEW_2026_09_08.md)
inspects Dilmé's power-sequence theorem, robust/evidence/abstraction results, GTE-sequential,
Gambit and OpenSpiel; SymPy is used for independent exact polynomial receiving. This is a
supplied-witness procedure, not a complete existence decision or equilibrium search. Failure of a
bounded witness is not a global impossibility. Ambiguity preferences and participation remain
separate from modelwise incentives; stipulated monitoring is not empirical evidence.

The [public-tag reduction](../../foundations/BELLMAN_PUBLIC_TAG_HISTORY_REDUCTION.md) now earns
one specified many-to-one history reduction: positive public copies of the same continuation game,
with identical supplied strategy and assessment, may be erased while preserving every continuation
gain and common consistency in both directions. The 127-node source reduces to 63 nodes. This is
assessment-specific; public randomization can coordinate non-invariant strategies, and equal
payoffs cannot justify transporting changed off-path likelihoods. Both shortcuts have exact
counterexamples. [Current reproduction](../../verification/beliefs_acceptance/README.md)
checks the new reduction and replays unchanged earlier components at their retained identities.

The [diagnostic erasure obstruction](../../foundations/BELLMAN_DIAGNOSTIC_HISTORY_ERASURE_OBSTRUCTION.md)
resolves the next question negatively for a concrete class beyond identical copies. Exact equality
of every local continuation value and individual model consistency do not preserve ONE common
sequence after discarding diagnostic information from both players. The necessary target ratios
3/5 and 5/3 contradict each other for arbitrary sequences. Retaining the sender's information
permits a restricted receiver-only reduction, with its full assessment induced by the witness.
The [author review](../../reviews/DIAGNOSTIC_HISTORY_ERASURE_REVIEW_2026_09_08.md) distinguishes
this consistency-existence obstruction from a rejected bounded witness and from equilibrium
nonexistence. [Current acceptance](../../verification/beliefs_acceptance/README.md) checks it
and preserves/replays all earlier evidence.

The next useful representation gate is a specified broader strategy class with explicit coverage
of deviations spanning the erased observation AND likelihood sufficiency across all models.
Inspect the established MSI/USI conditions first; their single-game equilibrium-payoff results
must not become arbitrary specified-belief/shared-sequence transport claims. Preserve sender
likelihood distinctions and signal-conditioned mechanism rules unless a new proof licenses their
removal. General quotient search, approximate off-path consistency and all-equilibria transport
remain unearned. Generic continuous receiving also remains unimplemented; do not mechanically
build both directions or infer causal-to-game identification.

### Merged result — Longitudinal causal kernel fibres and persistent decisions

Merged PR #21 extends PR #20’s point-identified policy and full-support subject boundary.
Its bounded result addresses the missing-support question:

> When first-stage/intermediate causal kernels are identified but binary second-stage outcome rows
> lack positivity, which complete causal subjects, policy values, and deterministic decisions are
> identified under an explicit saturated completion profile?

The [bounded construction](../../foundations/BELLMAN_LONGITUDINAL_CAUSAL_KERNEL_FIBRES_AND_PERSISTENT_DECISIONS.md)
keeps each unsupported outcome row as one named coordinate in an exact continuous `[0,1]^k` fibre,
for at most four rows. Policy outcome probabilities, additive losses, and pairwise policy
differences are multi-affine, so their extrema and the derived common-optimal, minimax-loss, and
same-model-regret queries are checked exactly on at most 16 corners. The corner family is not the
continuous fibre and has no warrant for arbitrary nonlinear queries.

All 32 complete policies remain one-policy-across-hidden-completions objects. A common minimizer is
causal decision identification across the fibre; minimax selection when no common optimum exists
is a separately supplied robust criterion. Stronger cross-row restrictions are unsupported rather
than silently discarded, and first-stage/intermediate gaps remain outside this profile. The causal
premises remain supplied, not empirically validated. No transport, estimation, unsafe-set
composition, authority, or Writ/Decision Lab capability is claimed.

## Empirical proving ground — current evidence-led gate

The [FSD3661 case](../../research/empirical_trust_2016/README.md) reproduces eight published
means and retains a prespecified retrospective history comparison with session holdout. Its
primary uncertainty is inconclusive; it does not estimate utility or validate shared off-path
consistency. A [review](../../research/empirical_trust_2016/REVIEW_20260909.md) and exact
observational-extension argument explain why prediction does not identify an untested
feedback intervention. Retention, refinement or redirection must follow evidence, not sunk effort.

The [AFY 2024 challenge](../../research/beliefs_2024/README.md) now executes that changed-incentive
comparison. A source-only fit and prespecified retrospective validation precede High-T/Low-R
scoring. The primary linear-utility comparison is inconclusive, and a simpler history/report
baseline predicts better. Utility sensitivities and feasible shared-prior alternatives change
the direction. The [identification audit](../../research/beliefs_2024/IDENTIFICATION_AUDIT.md)
therefore supports bounded model criticism, not psychological identification or an empirical
sequential-equilibrium claim. Exact rational value residuals and 600 prior-bound certificates
remain separate from numerical fitting and session uncertainty.

The author edition is hash-bound and raw rows remain external. Archive licensing was inspected,
but author/archive byte equivalence remains unverified. After-action reports may be used only
with their actual timing. Current unconditional reports do not identify reactions to deviations.
The most informative next observation is a pre-choice forecast of the opponent's response to a
specified deviation at a cooperative history. It needs a separately justified study design;
there is no automatic 2019 expansion or authority to collect new data.

Decision Lab/Writ's current exact contracts do not receive this statistical comparison. The
[portable gap](../../research/beliefs_2024/TRANSFER.md) preserves source/query identity and rejects
changed mechanism-use or report-timing claims without a cross-repository adapter.
[Current acceptance](../../verification/beliefs_acceptance/README.md) preserves/replays v0.0.7 and
FSD evidence and separately checks the new empirical computation. Statistical adequacy, causal
applicability and human disposition remain distinct from arithmetic receiving.

## 5. Default mathematical frontier after the current chain

These are **default priorities, not mandatory order**.

### A. Statistical learning and time-uniform coverage

Current Bellman models are supplied. The first bounded bridge from data constructs uncertainty sets
while preserving repeated-inspection guarantees.

Earned in the current reference:

- one complete ordered binary-data prefix under an explicit IID Bernoulli fixed-parameter premise;
- exact-binomial tail inversion with a summable all-time allocation for every real parameter;
- outward rational brackets checked independently from their bisection producer;
- separation of coverage alpha, deterministic precision, and loss-unit regret;
- exact static finite-action guarantees that remain valid on the simultaneous coverage event,
  including at data-dependent stopping times.
- controlled adaptive selection among a fixed finite registry, with exact next-unused local
  indexing, transcript replay, fixed per-stream alpha allocation, and arbitrary cross-row
  dependence consistent with each row's all-prefix premise;
- simultaneous rectangular coverage at realized local counts without conditioning on those
  counts, plus exact signed affine decisions over the retained rectangle.
- exact whole-policy expected-loss and modelwise-regret reduction from a checked rectangle to its
  corner family under the pathwise multi-affine admissibility condition, with complete tiny
  deterministic minimax-loss/minimax-regret comparison.

Still needed when promised by a future capability:

- outcome-dependent omission, concealed missingness, adaptive alpha allocation, or dynamically
  created streams;
- arbitrary within-row dependence, drift, misspecification, and broader selection handling;
- multivariate, channel-row, continuous, or structured model learning;
- empirical model criticism and applicability review;
- sequential statistical composition when a parameter can reappear along one path, or when
  parameter/corner growth requires an established optimization route instead of finite corners.

Existing foundation: §10 of [`BELLMAN_NEXT_MATHEMATICAL_BUILDOUT.md`](../../foundations/BELLMAN_NEXT_MATHEMATICAL_BUILDOUT.md). The exact-binomial reference is a narrower constructive specialization; it does not replace the unchanged categorical Hoeffding theorem or implement a sharper modern confidence-sequence boundary.

### B. Constraints, reachability, and tail/dynamic risk

Expected loss is not sufficient for many consequential decisions.

Earned in the active bounded reference:

- exact probability of ever visiting an identified unsafe observable history under one complete
  deterministic policy;
- maximum reachability across an unweighted persistent whole-episode family using the same policy;
- exact deterministic minimax expected loss and same-model regret within one fixed robust-feasible
  class, with FULL/subset empty-class distinctions;
- exact statistical-rectangle reduction to corner reachability under the inherited pathwise
  multi-affine warrant; and
- explicit separation of statistical coverage failure from model-implied harm probability.

Still needed when a future task promises it:

- resource and operational constraints;
- occupancy or equivalent finite constructions;
- CVaR/tail-risk queries where specified;
- a clear distinction between terminal risk criteria and recursively time-consistent risk criteria;
- preservation obligations for any abstraction used under constraints.
- randomized constrained feasibility and larger constrained optimization where justified;
- empirical criticism of supplied transition models and normative/applicability review of unsafe
  declarations.

Existing foundation: §11 of the build-out.

### C. Causal identification and partial identification

Needed when the decision question concerns interventions rather than predictions under an exogenous model.

Earned in the active bounded reference:

- checked finite adjustment/identification under supplied causal premises;
- support and positivity checks;
- partial-identification bounds through finite response-type or other justified representations;
- action-risk comparisons even when full intervention laws are not identified;
- exact same-fibre action differences, common minimizing sets, and opposite causal witnesses; and
- explicit separation between mathematical identification and substantive correctness of the causal assumptions.
- exact policy-specific two-stage g-formula identification under supplied longitudinal premises;
- explicit separation of policy support from support for every structural subject transition; and
- full-support construction of the completed two-stage subject with exact equality across all 32
  causal and Bellman policy values and minimizing sets.
- exact saturated completion of up to four unsupported binary second-stage outcome rows;
- exact policy distribution/loss intervals and same-completion pairwise comparisons through
  query-specific multi-affine corner reduction; and
- separate common-optimal causal decisions, model-dependent decisions, and robust minimax-loss or
  same-model-regret criteria across one fixed hidden completion.

Still needed beyond the bounded causal-to-sequential bridge:

- missing first-stage or intermediate causal kernels and stronger cross-row longitudinal
  restrictions beyond the saturated second-stage profile;
- causal-kernel-family composition with unsafe-set reachability;
- statistical estimation and coverage for longitudinal causal rows;
- transport or regime-stability premises between distinct observational and deployment populations;
- more than two stages and wider time-varying intervention semantics;
- wider supported causal restrictions, covariates, actions, and outcomes; and
- empirical criticism of supplied causal premises.

Existing foundation: §12 of the build-out.

### D. Structural transport beyond identical skeletons

Current transport deliberately requires the same completed observable-history skeleton. A later capability may need justified maps between different representations, action sets, information structures, or state descriptions.

Do not add a generic mapper merely to broaden the interface. A structural lift is earned only when a concrete downstream reuse problem requires it and comparator/policy coverage can be proved.

### E. Randomized and richer robust policies

PR #8's full policy comparison is deterministic. Randomization can matter for minimax or constrained decisions.

Possible later targets:

- finite private mixtures over complete policies;
- explicit adversary information/timing assumptions;
- exact finite minimax-loss or minimax-regret certificates;
- rectangular robust dynamic programming only when rectangularity is actually part of the model;
- Bayesian persistent-model updates only when a prior and likelihood model are supplied.

Do not silently replace persistent whole-episode uncertainty with rowwise rectangular uncertainty.

### F. Plural objectives and strategic actors

These become necessary when Bellman stops modelling one decision-maker facing exogenous uncertainty.

Earned strategic slice: supplied-profile full-continuation checks across a finite game family,
with an independently checked common off-path consistency witness. The four directions of
uncertainty, disclosure, remembered history and commitment/monitoring share this exact subject.
No ambiguity-sensitive equilibrium, complete equilibrium search or mechanism optimum follows.

Possible later targets:

- Pareto/nondominance and explicit preference-family interfaces;
- declared aggregation or bargaining rules rather than invented scalar weights;
- finite game/equilibrium or obedience checks;
- incentive compatibility when reports/actions respond strategically.

Existing foundation: §13 of the build-out.

## 6. Cross-cutting obligations

These can become active alongside any frontier when a concrete threshold is reached.

### Scalability and optimization

The current Python references deliberately favour inspectability over scale. Introduce stronger optimization machinery when handwritten search or enumeration becomes the actual blocker.

**Reminder trigger:** when Bellman needs substantially larger exact optimization, evaluate **Julia/JuMP and established exact/verified solver routes** before expanding bespoke Python search.

### Durable independent checking

When Writ begins relying on Bellman certificates as infrastructure rather than research fixtures, evaluate a small hardened checker whose job is only to verify claims.

**Reminder trigger:** evaluate **Rust with exact rational arithmetic** when durable independent certificate checking becomes a production requirement.

### Formal proof

Fixed checks are not proof assistants. Formalization becomes worthwhile when a theorem has stabilized and many later guarantees depend on it.

**Current candidate:** the PR5 sequential certificate soundness core is mature enough for a **narrow Lean feasibility study**, not a wholesale Bellman rewrite.

**Reminder trigger:** evaluate **Lean** for selected stable foundational theorems; do not formalize rapidly changing research objects simply for prestige.

### Continuous or infinite extensions

Do not pretend finite formulas automatically extend. Measure-theoretic kernels, conditional distributions, measurable selection, functional analysis, or other machinery should enter only when a real continuous/infinite capability is promised.

## 7. Closed or constrained directions

- **KL5/KL6 observation-model compression branch:** closed. Do not reopen with new grids or summaries absent a genuinely new mathematical question.
- **Novelty hunting:** not a programme objective.
- **Universal Bellman DSL:** not justified. Data structure and language follow stable mathematics.
- **General graph infrastructure:** not justified by the mathematics alone.
- **Automatic scalarization of contested objectives:** prohibited without a supplied preference rule.
- **Hidden model oracle:** never an implementable policy unless model identity is genuinely observed.
- **Outer enclosure as exact fibre:** never silently promote.
- **Unresolved computation as mathematical impossibility:** keep `unfinished`/unknown distinct.

## 8. Definition of done for a Bellman component

A bounded mathematical component is ready to retain when it has, at minimum:

1. a precise mathematical subject and typed premises;
2. a clear operation/query;
3. an explicit guarantee;
4. a composition/reuse rule;
5. explicit failure and unsupported boundaries;
6. constructive or checkable finite procedure where claimed;
7. adversarial counterexamples to tempting invalid joins;
8. exact fixed checks that exercise both accepted and rejected cases;
9. a receiver/checker path that does not trust the producer's conclusion;
10. honest provenance and preserved historical evidence;
11. explicit limits: what remains assumed, unproved, unimplemented, or unscaled.

Formal proof, production engineering, empirical model validation, and domain usefulness are **separate gates** unless the component explicitly promises them.

## 9. When to redirect the roadmap

Redirect rather than defend the current plan when any of the following occurs:

- a counterexample invalidates the proposed guarantee;
- established mathematics already supplies the needed result more cleanly;
- the proposed object adds machinery without improving any downstream decision capability;
- Writ/domain work exposes a missing primitive that is more important than the scheduled frontier;
- the current implementation language or solver prevents the mathematical operation from being expressed or checked faithfully;
- repeated tasks show that a supposedly separate mathematical component should instead be a composition rule among existing objects.

A redirect should update this file with the evidence and preserve the superseded route in history rather than rewriting old results.

## 10. Engineering-transfer gate

Bellman mathematics should progressively become executable Writ semantics, but not every mathematical artifact should be implemented immediately.

A mathematical component is a candidate for transfer when:

1. its subject, assumptions, operation, guarantee, and failure boundary are stable enough to specify;
2. a concrete Writ workflow needs that capability;
3. the engineering representation preserves the distinctions the mathematics requires;
4. a checker can reject stale, mismatched, unsupported, or false claims;
5. the integration is compared with a competent simpler workflow;
6. the implementation does not claim empirical truth, human approval, or authority merely because the calculation checks.

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the Bellman–Decision Lab–Writ relationship and transfer maturity model.

## 11. Programme success condition

Bellman is not complete when every topic above has a file.

It is succeeding when a growing class of consequential decision problems can be expressed so that another person or program can determine:

- what evidence and assumptions the decision depends on;
- what the mathematical model actually permits;
- what the checked calculation establishes;
- which conclusions survive combination, observation, or revision;
- which conclusions must be reassessed;
- where uncertainty, incompatibility, nonidentification, or unfinished computation remains;
- and how later evidence or corrected assumptions propagate through the decision record.

That is the roadmap's connection to the North Star.
