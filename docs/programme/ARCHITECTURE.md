# Bellman–Writ Mathematical Transfer Architecture

**Status:** living architecture and transfer-boundary document. This is not a mathematical theorem and does not supersede frozen foundations or verification evidence.

The programme North Star is [Bellman North Star](../../foundations/BELLMAN_NORTH_STAR.md). The current capability sequence and open mathematical frontier are tracked in [`ROADMAP.md`](ROADMAP.md).

## 1. System relationship

Bellman, Decision Lab, and Writ have different responsibilities but are intended to converge on one interoperable mathematical substrate over time.

### Bellman — mathematical authority

Bellman defines and hardens:

- mathematical subjects and object identity;
- assumptions and applicability premises;
- permitted operations and queries;
- guarantees and certificates;
- composition, transfer, accumulation, conditioning, and revision rules;
- failure boundaries and distinctions such as incompatible / unknown / unfinished;
- provenance obligations for mathematical claims.

Bellman is not merely documentation for engineering. Mature Bellman mathematics is expected to become executable semantics.

### Decision Lab — bounded computational test bench

Decision Lab is a replaceable environment for small exact computational components. Its role is to:

- accept explicitly specified mathematical subjects;
- produce candidate answers or certificates;
- independently check the candidate against the intended subject;
- expose failures in mathematical or implementation boundaries;
- provide a simpler comparison path for Writ integration.

Decision Lab is not the whole engineering roadmap, not the permanent product boundary, and not the mathematical ceiling.

### Writ — durable executable decision provenance

Writ owns the infrastructure needed to make stable mathematical semantics usable over time:

- source and exact-passage provenance;
- explicit modelling choices and mappings from evidence to mathematical inputs;
- versioned decision cases and revisions;
- execution records and checked-result handoff;
- applicability reassessment when support or use changes;
- separation of mathematical status, evidentiary applicability, human disposition, and authority to act;
- cumulative reuse without silently carrying forward stale conclusions.

Writ should progressively embody Bellman semantics where the transfer gate is met. It should not merely store Bellman filenames or theorem summaries.

### Domain stress environments

War, security, global affairs, biology, science, procurement, or other consequential domains are stress environments for the transferable decision structure. They should reveal missing mathematics and engineering rather than weaken the substrate to fit narrative complexity.

## 2. The four layers that must remain distinct

A trustworthy implementation should keep at least these four layers separate.

1. **Evidence / source layer** — what was observed, asserted, measured, or supplied, with provenance.
2. **Model / mathematical subject layer** — the explicit assumptions, states, constraints, losses, information structure, causal claims, and decision query.
3. **Checked mathematical result layer** — what follows conditionally from that exact subject and query.
4. **Human / institutional decision layer** — whether to accept assumptions, adopt a recommendation, exercise authority, or act.

A successful checker at layer 3 does not establish truth at layer 1 or 2 and does not grant authority at layer 4.

## 3. Transfer maturity model

A Bellman capability can move through the following maturity levels.

| Level | Meaning | Required evidence |
|---|---|---|
| **M0 — mathematical proposal** | Object or theorem is under active construction. | Definitions, premises, derivation or counterexample. |
| **M1 — bounded checked reference** | A finite construction has explicit checks and failure controls. | Exact reference, negative controls, preserved provenance. |
| **M2 — stable semantic contract** | Subject, operation, guarantee, and failure boundary are stable enough to specify independently of one implementation. | Adversarial review, exact interfaces, clear unsupported cases. |
| **M3 — engineering adapter** | Writ/Decision Lab can execute and freshly check the contract without changing its meaning. | Pinned/verified execution, byte/identity preservation, stale-use refusal. |
| **M4 — reusable cross-case capability** | A second independently authored case can use the contract without editing the engine. | Handoff/revision test, simpler-workflow comparison, no case-specific hidden assumptions. |
| **M5 — domain stress-tested** | The capability survives consequential real-world instantiation under explicit empirical premises. | Domain evidence, model criticism, applicability review, failure reports. |

Movement is not automatic. A mathematically interesting result can remain M1 indefinitely if no engineering workflow needs it.

## 4. Current transfer snapshot

This table is intentionally conservative.

| Capability | Mathematical standing | Engineering standing |
|---|---|---|
| Finite exact compatibility / decision certificates | M2 | Decision Lab provides an executable slice; Writ's bounded derived-decision-case integration is the current transfer experiment. |
| Sequential whole-policy certificates | M2 candidate | No general Writ integration yet. |
| Certificate transport / revalidation | M2 candidate | No general Writ integration yet. |
| Certificate accumulation / policy selection | M1–M2 | Research reference only. |
| Persistent model-family certificates | M1–M2 | Research reference only. |
| Family-aware replanning | M1–M2 | Bounded checked research reference; no general Writ integration. |
| Anytime-valid Bernoulli data-to-decision bridge | M1 | Acceptance-hardened research reference; not implemented as Writ or Decision Lab semantics. |
| Controlled fixed-registry multistream collection | M1 | Reviewed and acceptance-hardened bounded reference; no engineering adapter. |
| Statistical rectangle to sequential corner models | M1 | Reviewed bounded composition; at most two parameters/four corners under a pathwise multi-affine warrant, with no engineering adapter. |
| Statistical learning / coverage beyond the bounded Bernoulli profile | Foundation only | Outcome filtering, within-row dependence, drift, missingness, adaptive allocation and broader model learning are not implemented. |
| Unsafe-set reachability / constrained deterministic selection | M1 | Reviewed and merged bounded reference; exact first-hit probability, persistent-family cap, and admissible statistical-corner composition, with no engineering adapter. |
| Resource constraints / tail and dynamic risk | Foundation only | Not implemented. |
| Finite causal identification / one-stage decision certification | M1 | Merged bounded exact adjustment and binary response-type reference; supplied causal premises are not empirically validated and no engineering adapter exists. |
| Two-stage longitudinal causal policy / sequential bridge | M1 | Reviewed and merged bounded exact policy g-formula and full-support completed-subject composition; no engineering adapter. |
| Longitudinal causal kernel fibres / persistent decisions | M1 candidate | Bounded exact saturated continuous fibre and query-specific deterministic corner reduction under review; no engineering adapter. |
| Plural objectives / strategy | Foundation only | Not implemented. |

Do not infer that later mathematical modules should be rushed into Writ. The purpose of this table is to prevent engineering from claiming semantics that have not stabilized.

### Statistical, corner-family, and unsafe-reachability boundary

The bounded research references keep six interfaces separate:

1. a fixed registry and complete append-only event transcript under explicit rowwise IID Bernoulli
   fixed-parameter premises and a built-in history-only rule;
2. one checked outward rational all-prefix interval for each identified stream;
3. a fixed-allocation union-bound certificate for simultaneous membership in the retained
   parameter rectangle;
4. an exact static finite-action affine comparison conditional on membership in that rectangle.
5. when explicitly requested, a separate pathwise multi-affine warrant and persistent family of
   completed sequential corner models for whole-policy deterministic loss and regret.
6. when explicitly requested, a further unsafe-history declaration and first-hit receiver for exact
   modelwise reachability, robust safety caps, and deterministic selection within one fixed robust-
   feasible policy class.

The controlled reference additionally binds registry order, distinct physical-event identities,
global and local indices, rule/stopping state, revision lineage, fixed stream allocations, and
cross-stream premise. Its checker can replay the supplied bytes and verify exact binomial-tail,
union-bound, and affine-box arithmetic. It cannot reveal concealed discarded outcomes or verify
physical independence, completeness, representativeness, absence of drift, or legitimacy of the
decision inputs. Cross-stream independence is unnecessary for simultaneous coverage but cannot be
silently inferred for joint-event or conditional next-draw queries. A changed transcript or
coverage specification gets a new claim; a changed loss table gets a new decision claim without
pretending the same data are a fresh sample.

These are M1 research-reference results. No adapter, database record, Decision Lab build, or Writ
workflow is added here. Promotion would require a stable independent contract, concrete workflow,
fresh checking, revision/applicability semantics, and the acceptance evidence in section 7.

The fifth interface is not implied by rectangle validity. It additionally binds statistical-stream
identities to transition-parameter identities, requires parameter-independent costs and a fixed
completed skeleton, and checks that no parameter occurs in two transition factors on one complete
path. Its corner subjects have no probabilities of their own. A repeated-parameter subject such as
`p(1-p)` remains a valid sequential model but must use a different optimization method. Coverage
failure probability, loss/regret quantities, and outward-enclosure precision remain distinct
checked fields. Any changed data revision, mapping, transition law, loss table, policy class, or
query creates a new composition claim rather than inheriting an earlier corner result.

The sixth interface does not infer an unsafe event from a loss table. Its receiver binds an
identified subset of the completed observable histories, recomputes an absorbing reachability
recurrence, and requires equality with an independent first-hit path sum. Absorption is a
calculation device and does not rewrite the sequential model. For persistent families, every model
identity and the one common policy remain visible and unweighted. Constrained comparison uses one
fixed robust-feasible deterministic class in every model; it does not let the comparator change its
feasibility class by hidden model identity.

Under the fifth interface's no-repeat-per-parameter path warrant, first-hit probabilities are also
multi-affine and their rectangle maxima occur at the same completed corners. Statistical coverage
failure `alpha`, conditional model-implied unsafe reachability `delta`, and numerical enclosure
precision remain typed and separate even when two numbers coincide. A checked cap establishes no
empirical model validity, normative adequacy of the unsafe declaration, or authority to act. A
repeated same-path parameter invalidates only the corner warrant; unsafe reachability at each fixed
model remains a valid query for another optimization method.

### One-stage causal identification boundary

The causal reference introduces a separate model-layer interface; it does not reinterpret the six
statistical/sequential interfaces above. Its adjustment route binds an exact observational
`P(A,Y,Z)`, population and variable coding, the adjustment set, and explicit identities for
consistency, exchangeability, pre-action status, and intervention meaning. The receiver checks
support and exact adjustment arithmetic. A successful result is conditional on those premises;
positivity failure means an observational conditional is unavailable, not that the causal model is
incompatible or the effect absent.

Its second route maps an exact binary observational `P(A,Y)` into the eight deterministic
`(A_nat,Y0,Y1)` response types under observed consistency and a small typed equality restriction
library. The receiver completely enumerates the bounded exact fibre, distinguishes point/partial
identification from incompatibility and unsupported nonlinear restrictions, and retains attaining
witnesses. An explicitly requested dropped-restriction analysis is an outer result only.

One-stage action certification evaluates every paired risk difference on the same response-type
law. It cannot subtract marginal extrema attained by different causal witnesses. Observation,
causal premise, restriction, coding, cost, loss, and query revisions all create new claims. This M1
result does not discover causal structure, validate premises, transport between populations,
define time-varying interventions, compose with sequential or unsafe-set models, or authorize an
action. Its one-stage intervention marginals do not supply the history-conditioned kernels needed
by an adaptive second-stage policy.

### Two-stage longitudinal causal bridge boundary

The bounded longitudinal interface binds one complete exact `P(A1,L1,A2,Y)`, population, binary
coding, temporal order, consistency/intervention/first- and second-stage exchangeability,
adaptation and no-interference premise identities, a complete deterministic history policy, and an
exact cost/loss table. A matching premise identity is not empirical evidence for its truth, and
the first profile permits no population transport.

Policy-specific receiving checks support only for the chosen first action and chosen second action
at each positive-probability regime history. An intermediate history with zero regime mass needs no
action conditional for that policy. In contrast, construction of Bellman's complete subject
requires positive support for both first actions, both intermediate values below each first action,
and both second actions at every resulting history. The API preserves an identified policy while
returning `policy-identified-full-subject-not-supported` for the invalid broader bridge.

With full support, the adapter constructs the existing 21-node completed observable-history
subject rather than defining a parallel planner. It retains all 32 policies, including distinct
off-root completions. The receiver reconstructs every transition, checks retained certificates
through the existing sequential consumer, and independently matches complete-path distributions,
signed costs, and the complete minimizing set to the longitudinal g-formula.

Two fully supported causal worlds can have the same static `do(A2)` outcome marginals for both
actions while making opposite `L1`-adapted policies optimal. One-stage intervention results are
therefore not accepted as longitudinal transition rows. This M1 result does not implement
transport, statistical estimation, safety composition, causal discovery, empirical premise
validation, or authority to act. Each would require its own typed composition warrant.

### Longitudinal causal kernel-fibre boundary

The bounded partial longitudinal interface begins only when both root actions and every
intermediate history have positive observational support. It retains each supported second-stage
outcome row exactly and maps every unsupported binary row to one explicitly ordered coordinate in
`[0,1]`. The resulting continuous Cartesian fibre is exact only under the supplied saturated
no-cross-row-restriction profile. A request carrying monotonicity, shared structural errors,
cross-world coupling, parametric structure, or another stronger restriction is unsupported; the
architecture does not silently drop it and promote a possible outer relaxation to an exact fibre.

For fixed deterministic policies, terminal outcome probabilities, expected additive loss, and
pairwise same-completion differences are multi-affine in the missing-row coordinates. A distinct
finite corner family is therefore an exact extremal representation for those query classes and
their complete-class common-optimal, minimax-loss, and same-model-regret consequences. It is not
the continuous fibre and is not reusable for arbitrary nonlinear causal queries. The exact
`q(1-q)` midpoint control makes that boundary executable.

Every completion is a persistent whole-episode alternative and receives the same complete policy;
hidden completion-indexed policy vectors and cross-completion regret subtraction reject. For one
or two missing rows, the unchanged four-member persistent-family receiver independently reproduces
the decision results. Three or four rows create eight or sixteen corners, so the new bounded
receiver records the old checker's four-model limit and performs the exact local matrix check
without rewriting historical machinery. This is an interface-size mismatch, not a solver
bottleneck.

The `k=0` case delegates to the merged longitudinal bridge and must reproduce its subject, all 32
policy values/distributions, and minimizing set exactly. Earlier-stage positivity gaps remain
`outside-second-stage-kernel-fibre-profile`; they are not fabricated, declared incompatible, or
allowed to erase a narrower policy result. Observation, support pattern, population, coding,
timing, premise, completion profile, row order, loss, policy catalogue, fibre, corner family, and
query revisions all create new claims. This M1 candidate does not establish a general SCM fibre,
transport, estimation, unsafe-set composition, randomized control, premise validity, or authority
to act.

## 5. Stable interface principles

### Language-neutral mathematical contracts

The enduring interface should be mathematical, not tied to Python, Julia, Rust, Lean, TypeScript, or a bespoke DSL. Implementations may change while exact subject and certificate semantics remain stable.

Where exact rationals are part of the contract, serialization must preserve them exactly rather than route them through floating-point normalization.

### Producer and checker remain separate roles

A producer may use heuristics, floating search, optimization libraries, or expensive algorithms to find a candidate. A checker must verify the claimed result against the independently intended subject.

A producer's `optimal`, `feasible`, or `success` label is never itself a guarantee.

### New revision means new claim

A changed source, mapping, model, loss, policy, query, information structure, or criterion may leave an old theorem historically correct while making it inapplicable to the new use. Engineering should construct or revalidate the successor claim instead of editing history.

### Composition is an operation, not a database join

Two valid records are not automatically composable. Bellman's composition rules determine whether values, models, policies, certificates, or evidence can be combined. Graph structure or dependency metadata cannot substitute for those rules.

## 6. Language and tool triggers

The current reference stack is not permanent.

### Python — current research reference

Use Python while it remains the simplest way to express small exact constructions, counterexamples, and receiver checks. Do not treat present Python references as the product ceiling.

### Julia / JuMP — optimization trigger

Evaluate Julia/JuMP or another established mathematical optimization route when:

- explicit optimization models become larger than comfortable handwritten search;
- robust, constrained, occupancy, or matrix problems require a real modeling system;
- exact or certifiable solver integration can materially reduce bespoke code.

Do not migrate existing stable modules solely for cleaner syntax.

### Rust — durable checker trigger

Evaluate a small Rust checker when:

- Writ depends operationally on Bellman certificates;
- independent exact checking becomes a durable infrastructure requirement;
- stronger value/type isolation would materially reduce implementation risk.

Rust would normally be a checker/runtime choice, not the default language for mathematical discovery.

### Lean — formal theorem trigger

Evaluate Lean when:

- a theorem is stable;
- many later guarantees depend on it;
- a proof bug would propagate widely;
- the theorem is narrow enough to formalize without freezing an unstable research interface.

The sequential certificate soundness core is a current candidate for a narrow feasibility study. Formalization should remain selective.

## 7. Engineering acceptance test

A transferred Bellman capability should not be considered earned merely because a command returns the expected answer for one fixture.

A strong acceptance test is:

1. author a case using the published contract;
2. bind all source/model assumptions explicitly;
3. execute and freshly check the mathematical result;
4. hand the portable case/result to a separate recipient process;
5. revise one supported input or modelling assumption;
6. correctly distinguish reusable mathematics from required applicability reassessment;
7. produce a new checked result when the mathematical subject changes;
8. preserve the old result under its old assumptions;
9. compare the workflow with a competent notebook/script using the same mathematical checker;
10. retain the Writ layer only if its provenance, revision, and handoff safeguards justify the added complexity.

## 8. Architecture redirect rules

Change this architecture when evidence shows a better boundary.

Examples:

- If Decision Lab duplicates Writ without providing an independent test-bench benefit, simplify or absorb it.
- If a stable Bellman semantic contract needs a stronger checker, replace the implementation without changing the mathematical meaning.
- If Writ needs a mathematical primitive that Bellman has not specified, send the question upstream rather than inventing a product-level guarantee.
- If a mathematical component never earns a downstream use, do not build infrastructure merely to make every Bellman file executable.
- If a domain case reveals that the current subject omits information, causality, constraints, strategic behavior, or authority needed for the decision, revise the mathematical problem rather than hiding those omissions in metadata.

Repository boundaries are implementation conveniences, not doctrine. The long-run target is an interoperable substrate in which stable Bellman mathematics can be executed, checked, revised, and accumulated through Writ.
