# Bellman Programme Roadmap

**Status:** living programme-steering document. This is not a frozen theorem, experiment result, or mathematical authority. Update it when evidence changes the best route.

**Current snapshot:** 7 September 2026, based on `main` after merge of PR #8 (`81eec793094bde8bb26fc88c3f4d6a99ef3ffdfe`).

The governing North Star remains [Bellman North Star](foundations/BELLMAN_NORTH_STAR.md):

> **Make consequential decision-making mathematically inspectable, cumulative, and correctable.**

Bellman should become progressively better at saying what a decision problem means mathematically, what follows under its assumptions, what can be reused or combined, what must be rechecked after change, and where the guarantee stops.

## 1. How to read this roadmap

This is a **capability roadmap, not a checklist of fields to complete**. A line may be skipped, reordered, simplified, or closed if established mathematics already settles it, a counterexample kills the proposed route, or engineering/domain work reveals a better frontier.

Progress does **not** require mathematical novelty. A known theorem becomes useful Bellman mathematics when its object, assumptions, operation, guarantee, composition rule, failure boundary, and provenance are made explicit enough to check and reuse.

The programme should change course when the evidence warrants it. Changing course is not drifting from the North Star if the change improves our ability to make decision reasoning inspectable, cumulative, and correctable.

## 2. Progress snapshot

Two different notions of progress matter.

### First finite executable core

**Planning estimate: roughly 75–80% of the first bounded finite core is now constructed and hardened.** This is not a scientific completion metric. It means that the core chain from exact model compatibility through sequential decision guarantees and persistent model uncertainty now has concrete mathematical constructions and exact reference checks.

Earned so far:

1. exact compatible-model fibres versus outer enclosures;
2. finite rational compatibility, identification, and checked decision certificates;
3. whole-policy sequential certificates and regret composition;
4. target revalidation after explicit model or policy change;
5. accumulation of compatible certificates and checked policy selection;
6. one implementable policy across persistent whole-episode model families;
7. explicit support-filtered continuation without hidden model switching or fabricated model weights.

The largest missing piece in this first finite chain is now **family-aware replanning and preservation/reassessment of root guarantees after a continuation changes**.

### Full Bellman mathematical programme

**Planning estimate: roughly 35–45% has been made comparably constructive.** Large mathematical areas remain intentionally open: statistical learning and coverage, harm/resource constraints and risk, causal identification, richer structural transport, scalable optimization, plural objectives, strategic actors, and selected formal verification.

This lower percentage is expected. The programme is intentionally much larger than the first executable core.

## 3. Completed and hardened capability chain

| Capability | Standing | Main mathematical record | What it earns |
|---|---|---|---|
| Working substrate | FOUNDATION | [`BELLMAN_WRIT_MATHEMATICAL_SUBSTRATE_V1_1.md`](foundations/BELLMAN_WRIT_MATHEMATICAL_SUBSTRATE_V1_1.md) | Seven-component working foundation and composition discipline. Not finished Bellman mathematics. |
| Exact joint-law compatibility and decision certificates | HARDENED | [`BELLMAN_NEXT_MATHEMATICAL_BUILDOUT_REVISED.md`](foundations/BELLMAN_NEXT_MATHEMATICAL_BUILDOUT_REVISED.md) | Exact/outer separation, witnesses, bounds, infeasibility certificates, conditional queries, checked finite decisions. |
| Sequential whole-policy guarantees | HARDENED | [`BELLMAN_SEQUENTIAL_CERTIFICATE_COMPOSITION.md`](foundations/BELLMAN_SEQUENTIAL_CERTIFICATE_COMPOSITION.md) | Nodewise inequalities become whole-policy bounds; conditioning and replanning boundaries are explicit. |
| Certificate transport and revalidation | HARDENED | [`BELLMAN_CERTIFICATE_TRANSPORT_AND_REVALIDATION.md`](foundations/BELLMAN_CERTIFICATE_TRANSPORT_AND_REVALIDATION.md) | A changed model or policy gets a new checked guarantee rather than inheriting an old label. |
| Certificate accumulation and policy selection | HARDENED | [`BELLMAN_CERTIFICATE_ACCUMULATION_AND_POLICY_SELECTION.md`](foundations/BELLMAN_CERTIFICATE_ACCUMULATION_AND_POLICY_SELECTION.md) | Compatible checked results can strengthen one another; different-policy selection creates and checks a new policy. |
| Persistent model families | HARDENED | [`BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md`](foundations/BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md) | One accessible policy is evaluated across alternative whole-episode models; loss, regret, model identity, support, and criteria remain distinct. |

`HARDENED` here means: the bounded construction has survived targeted adversarial review and exact reference checks within its stated profile. It does **not** mean universal correctness, empirical validity, formal verification, scalability, or final engineering acceptance.

## 4. Current frontier

### NEXT — Family-aware replanning and root-guarantee preservation

The immediate mathematical question is:

> After observing information and replacing a continuation policy, what exactly can still be guaranteed about the revised whole plan across the persistent model family?

The next construction should:

- build the actual revised total policy;
- retain the original family and model identities;
- propagate the continuation change through each model using that model's own reach probability;
- distinguish a better conditional bound from a better actual policy;
- distinguish failure to establish preservation from proved violation;
- prevent zero-likelihood conditional exclusions from silently deleting models from an ex-ante family claim;
- produce a new receiver-checkable root guarantee for the revised policy.

A successful result closes another gap in the first finite executable chain. A failure or counterexample should redirect the construction rather than be patched around.

## 5. Default mathematical frontier after the current chain

These are **default priorities, not mandatory order**.

### A. Statistical learning and time-uniform coverage

Current Bellman models are supplied. The next major bridge to evidence is to construct uncertainty sets from data while preserving repeated-inspection guarantees.

Needed:

- explicit sampling/data-generating assumptions;
- time-uniform confidence sets or other valid sequential uncertainty constructions;
- separation of statistical coverage probability from decision loss/regret;
- data-dependent stopping without invalidating the stated coverage;
- explicit handling of adaptive sampling, dependence, drift, missingness, and misspecification when those become part of the promised capability.

Existing foundation: §10 of [`BELLMAN_NEXT_MATHEMATICAL_BUILDOUT.md`](foundations/BELLMAN_NEXT_MATHEMATICAL_BUILDOUT.md).

### B. Constraints, reachability, and tail/dynamic risk

Expected loss is not sufficient for many consequential decisions.

Needed when the task requires it:

- resource and operational constraints;
- unsafe-set reachability/hitting probabilities;
- occupancy or equivalent finite constructions;
- CVaR/tail-risk queries where specified;
- a clear distinction between terminal risk criteria and recursively time-consistent risk criteria;
- preservation obligations for any abstraction used under constraints.

Existing foundation: §11 of the build-out.

### C. Causal identification and partial identification

Needed when the decision question concerns interventions rather than predictions under an exogenous model.

Default bounded targets:

- checked finite adjustment/identification under supplied causal premises;
- support and positivity checks;
- partial-identification bounds through finite response-type or other justified representations;
- action-risk comparisons even when full intervention laws are not identified;
- explicit separation between mathematical identification and substantive correctness of the causal assumptions.

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

Possible targets:

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