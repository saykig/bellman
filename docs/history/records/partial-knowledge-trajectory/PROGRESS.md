# Research progress ledger

Entries reconstructed on 18 September 2026 from the retained records. Research
dates come from those records, not inferred file timestamps. Same-day ordering
follows explicit predecessor/successor statements. No research was rerun in this
preservation pass.

## R01 — 17 September: reassess the mathematical foundations

**Question:** how should partial knowledge combine, and how should causal mechanisms
and interventions be represented? Compared information/valuation algebras,
local-to-global compatibility and compositional causal models.

**Outcome:** use complementary established theories, not a new universal algebra.
Selected finite acyclic causal modules with relational uncertainty over complete
mechanism choices. Derived extension, gluing, intervention and outer-approximation
results; later distinguished scalar ranges from complete query signatures.

**Evidence:** written proofs; exact finite enumeration; selected Lean lemmas.
These do not establish novelty, empirical adequacy or general strategic applications.
**History:** repository initially appeared empty; existing main was recovered and
historical artifacts preserved. Milestones: `e3cb988`, `7602659`, `e3a6a92`.

**Recover:** [original September 17 log](../../../../research/foundations/history/RESEARCH_LOG.md),
[initial audit](../../../../research/foundations/history/2026-09-17-initial-audit.md),
[repository inspection](../../../../research/foundations/history/2026-09-17-repository-inspection.md),
[note](../../../../research/foundations/manuscript/RESEARCH_NOTE.md),
[claim standing](../../../../research/foundations/CURRENT_STATE.md),
[rejected routes](../../../../research/foundations/REJECTED.md).

**Then-next question:** which dependencies must a representation retain under later
composition? R02 reconsidered this emphasis; it did not invalidate R01's results.

## R02 — 17 September: clarify revision and provenance

**Question:** what must be retained when named premises are added or withdrawn,
or a named mechanism is replaced? This is a related branch of the foundations
question, not a completed general theory of revision.

**Outcome:** an anonymous current-model family cannot implement every named
withdrawal. Two independent warrants can support the same present conclusion but
respond differently to withdrawal. Mechanism versions and intervention interfaces
also matter. Selected a bounded provenance-sensitive experiment.

**Evidence:** written arguments and executed small probes, including the recorded
32/0/20 interface counts. The larger 96-record experiment was specified and its
runner prepared, **not executed**. Its practical value and quotient size remain open.
**Git at the time:** uncommitted at `e3a6a92`; preserved by R06.

**Recover:** [recommendation](../../../../research/clarification_2026_09_17/RECOMMENDATION.md),
[current state and recovery map](../../../../research/clarification_2026_09_17/CURRENT_STATE.md),
[translation/proofs](../../../../research/clarification_2026_09_17/TRANSLATION.md),
[actual probe results](../../../../research/clarification_2026_09_17/probe-results.json),
[unexecuted next specification](../../../../research/clarification_2026_09_17/EXPERIMENT_SPEC.md).

**Still open:** this revision experiment was not completed by the later strategic
research. The trajectory branches here; later work must not be described as having
settled named revision in general.

## R03 — 18 September: shared information budgets and active incentives

**Question:** combine supplied information–incentive components without spending
the same information budget independently in each component; include disclosure.
External source notes and an audit were inspected and hashed.

**Outcome:** information-cost profiles, joint attainability, a six-branch expected
joint-vulnerability formula, and a solved disclosure benchmark. Separate expected
maxima and separate credible punishments can give wrong answers. A partial
certificate requires one continuation that deters all eligible sender types.

**Evidence:** analytical Theorems A–G; original-cell optimization and payoff checks;
50 tree identities and exact certificate arithmetic; narrow Lean checks of maximum
and threshold identities. The full equilibrium and entropy theory were not formalized.
The binary benchmark's controlled fine ≈.09018 and disclosure penalty 1 are specific
to that game and cannot be compared as identical objects with R04's numbers.
**Git at the time:** uncommitted at `e3a6a92`; preserved by R06.

**Recover:** [log](../../../../research/information_incentives_2026_09_18/RESEARCH_LOG.md),
[note](../../../../research/information_incentives_2026_09_18/manuscript/RESEARCH_NOTE.md),
[standing](../../../../research/information_incentives_2026_09_18/CURRENT_STATE.md),
[input identities](../../../../research/information_incentives_2026_09_18/sources/INPUT_MANIFEST.json),
[rejected routes](../../../../research/information_incentives_2026_09_18/REJECTED.md).

**Then-next:** a three-state robust partial-certificate frontier, pursued in R04.

## R04 — 18 September: partial certificates and the perfect-gate obstruction

**Question:** solve an explicit three-state two-receiver game with a shared budget,
common gate/fine and a partial certificate; examine valid composition boundaries.

**Outcome:** noisy-gate frontier and a distinct perfect-gate regime when an eligible
type becomes impossible. Established a scalar-profile result not specific to KL,
upper-image composition with retained interfaces, and counterexamples to arbitrary
convexification and unrestricted multi-sender belief choices. The game differs
from R03; optimality is only over the declared symmetric binary gates.

**Evidence:** written proofs; 36 original-cell comparisons, 200 sampled laws,
304 continuation checks, 72 finite feasibility queries and six narrow Lean lemmas.
SLSQP failed on nonsmooth total variation; the appropriate LP replaced that check.
**Prior-art reassessment:** close signaling/communication and set-optimization work
already contains the common-payoff logic and algebra; novelty remains unestablished.
**Git at the time:** uncommitted at `e3a6a92`; preserved by R06.

**Recover:** [log](../../../../research/partial_certificate_frontier_2026_09_18/RESEARCH_LOG.md),
[note](../../../../research/partial_certificate_frontier_2026_09_18/manuscript/RESEARCH_NOTE.md),
[standing](../../../../research/partial_certificate_frontier_2026_09_18/CURRENT_STATE.md),
[source audit](../../../../research/partial_certificate_frontier_2026_09_18/sources/AUDIT.md),
[rejected routes](../../../../research/partial_certificate_frontier_2026_09_18/REJECTED.md).

**Then-next:** explain the discontinuity with asymmetric priors and overlapping
certificates, before further network/multiple-sender expansion. Pursued in R05.

## R05 — 18 September: classify disclosure discontinuities

**Question:** first vary only prior/gate/budget with fixed payoffs and costs; then
classify full-parameter boundaries. Are support and equilibrium changes exhaustive?

**Outcome:** exact information-only criterion in the full KL family (Theorem I),
exact phase criterion within the payoff family (F), and a regular-region theorem
from established parametric optimization (R). Support loss can be masked. A discrete
source catalogue supplies another jump mechanism without posterior-support change.
Separate examples isolate incentive thresholds and loss of deterrent equilibrium
branches. Optimizing the gate removes the supplied-perfect-gate jump in this family.

**Evidence:** analytical proofs and counterexamples, 56 original-cell optimization
comparisons and exact rational checks. One unsuccessful solver status is retained.
Lean derives the fixed-information E12 threshold from utilities, including operations
and a full-support wrapper; it does not prove the global continuity theorem.
**Commits:** `26d3415`, `ad16961`, pushed to main.

**Recover:** [log](../../../../research/disclosure_boundaries_2026_09_18/RESEARCH_LOG.md),
[note](../../../../research/disclosure_boundaries_2026_09_18/manuscript/RESEARCH_NOTE.md),
[audit](../../../../research/disclosure_boundaries_2026_09_18/AUDIT.md),
[rejections](../../../../research/disclosure_boundaries_2026_09_18/REJECTED_APPROACHES.md),
[Lean scope](../../../../research/disclosure_boundaries_2026_09_18/lean/README.md).

**Open next question:** can a nontrivial continuation switch survive joint gate
optimization? This remains a proposal, not a result or automatically active goal.

## R06 — 18 September: consolidate the trajectory for recovery

**User request:** keep the whole research trajectory in one ledger area, including
the record begun September 17, so earlier work can be revisited and corrected.

Located R01's original log and the research-purpose statement. Reconstructed R01–R05
from retained logs/status notes, indexed decisions and recovery dependencies, and
inventoried exact bytes. Preserved the 60 previously untracked artifacts of R02–R04
and the existing research-purpose statement without rewriting them. Their original
“uncommitted” statements remain historically accurate; this is the later preservation
event. Git identifies this event under the commit subject **Preserve prior research
phases and consolidate the research trajectory ledgers**.

No mathematical claim was newly proved or revalidated in this pass. No unexecuted
experiment was run. External source files remain outside the repository where
previous manifests say so; hashes alone do not recover those bytes.

## R07a — 18 September: activate endogenous-gate recovery research

Explicit active goal, starting from `5661f9e`, following R05's open question.
The [new bounded investigation](../../../../research/optimized_gate_recovery_2026_09_18/README.md)
first rejects a fixed-fine continuation switch in the inherited full-information,
fixed-support public model. A candidate fixed-payoff information-only obstruction
uses a sender observing certificate eligibility rather than the exact state;
the user explicitly authorized analysing both and labelling that change.
Analytical development begun; computation and final theorem audit pending at this
milestone. No claim of refuting strong persistence, minimality or novelty.
