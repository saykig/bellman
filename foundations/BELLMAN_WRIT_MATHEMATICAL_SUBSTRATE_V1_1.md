# Bellman/Writ — Mathematical Substrate v1.1

**Date:** 6 September 2026  
**Status:** Focused amendment of the foundation synthesis and proposed mathematical contract; not an experiment, preregistration, software architecture, or claim of completed implementation.  
**Source edition:** v1, 6 September 2026. The original v1 bytes are preserved; its SHA-256 is recorded below.  
**Engineering boundary:** Existing Build 1 may continue unchanged in parallel. This amendment is not an additional implementation gate.

> **Programme:** Make consequential decision-making mathematically inspectable, cumulative, and correctable.
>
> **First capability:** Know exactly what information a representation must preserve for specified future decisions.

## Executive assembly

The foundation is a collection of **mathematical objects and conditional guarantees with explicit rules for composition**. Its basic reusable unit is not a recommendation, a probability, or a summary alone. It is a result together with the model, assumptions, question, information access, derivation, and limits that make that result valid.

The accumulated mathematics supports seven connected components:

1. Joint probability models and evidence operations.
2. Information states, admissible policies, and sequential decision evaluation.
3. Query-relative representations and exact abstraction.
4. Approximation certificates for values, policies, and decision margins.
5. Information comparison and dependence-aware evidence reuse.
6. Explicit model uncertainty and its decision criterion.
7. A distinct causal interface for intervention claims.

Assumption tracking, result provenance, and correction apply across all seven. They do not replace their mathematics. The causal interface is conditional: it is required when a claim concerns interventions, not imposed on every probability calculation. Strategy, institutional authority, and collective preference aggregation do not acquire a mathematical treatment merely by appearing in the programme's long-term vocabulary. [N; P §§2–9; E §§3–5]

The central discipline is:

> **Before a result becomes an input to another decision, establish that its guarantee covers the new question, information context, and permitted operation. Otherwise preserve the limitation rather than silently supply the missing mathematics.**

This document assembles that discipline into usable mathematical specifications. The component selection and record conventions are proposed synthesis. The equations and guarantees are inherited from the supplied audits or explicitly identified elementary consequences. No claim is made that this collection is a new calculus, universally minimal, or already implemented.

**Summary of the amended guarantee.** An exact compatible-model fiber is not its outer enclosure: an empty sound outer intersection rules out an original joint model, but a nonempty one proves only feasibility of the relaxation. For the coupling certificate in §6, use finite nonempty state/action/observation spaces, a common known prior, stationary conditionally independent observations, common terminal losses \(0\le L\le L_{\max}<\infty\), a common fee \(0\le c<\infty\), integers \(H\ge0\), \(0\le h\le H\), and finite nonnegative error allowances. Policies must be executable on every history possible in any covered model or the surrogate. Under the uniform channel bound \(d_s\ge0\), \(e_h=(L_{\max}+hc)\min\{1,hd_s\}\) bounds value error; a separately justified whole-policy suboptimality \(\eta_h\ge0\) gives regret at most \(2e_h+\eta_h\). For positive horizons only, a computed STOP/OBSERVE margin is certified by excluding zero from its interval with radius \(e_h+\xi_{R,h}+\xi_{O,h}\), where the two additional nonnegative finite bounds concern the computed STOP value and forced-observation optimum. No conditional expression is evaluated on an `NA` branch. Statistical coverage is separate. Build 1's exact signed-loss calculations do not automatically receive this narrower approximation guarantee. [REV §§3–5; §§4, 6, 14 below]

### v1.1 change log and assessment of the review

| Finding | Assessment on its merits | Focused amendment |
|---|---|---|
| Exact fiber versus outer set | A consequential cross-section ambiguity. Nonempty outer feasibility implying original compatibility is a false inference; the exact-set rule is not refuted. | Separate the sets in §§2, 5, 8, 10 and 12; include the fixed rational counterexample. |
| Approximation domains and support | The nonnegative-loss theorem remains valid. Its summary omitted the lower bound; several displayed expressions left predicates implicit. | Restore domains and positive-support sums at use sites, including this summary and §13. |
| Off-support transferred policy | Clarification of the existing common-implementable-policy premise, not a counterexample to policy transfer. | Require a legal total response on covered histories without inventing a surrogate posterior. |
| Computed margins | The exact-surrogate theorem is valid. The proposed numerical bridge is a useful strengthening; ignoring certified numerical error would be invalid. | Separate model, forced-observation optimization/evaluation, whole-policy, and coverage errors in §6. |
| Decoder existence and randomization | Precision improvements, not refutations of semantic factorization or of declared randomization. | Distinguish semantic sufficiency, executable decoding, and applicability; clarify randomized policy measurability. |
| Readiness and Build 1 mapping | An implementation correspondence requested here, not an additional theorem or feature gate. | Add compact annotations, the existing one-observation mapping, and a bounded check record in §14. |

The seven components, eleven composition rules, theorem-level content, and inherited stopping dispositions are retained. The review's other fixed cases confirm already-present qualifications, rather than establish new deficiencies. Established mathematics is sufficient for this foundation-building; novelty is not a condition for continuing Build 1. [REV §§2–6]

---

## 1. Inherited knowledge and binding boundaries

| Inherited record | What enters the foundation |
|---|---|
| KL5 Stage R | Its registered primary search had 64 equal-`C_*` sequentially separating pairs, earliest horizon two; the mandatory informative quarter-grid interior restriction had none. `KL5_STOP_DEGENERATE` remains final. No main lane or synthesis ran. |
| KL6 V2 | At fixed prior, losses, and cost, distinct strictly interior models can share `C_*` but require opposite strict STOP/OBSERVE decisions. One-step answer agreement is not a sequential certificate. |
| KL6 reconstruction closure | On the original eighth-grid, original prior/loss family, and horizon five, `S04=(C_*,Z_5)` identifies the labeled channel. Its sufficiency is not genuine compression. `KL6_STOP_THEORY_ALREADY_SETTLES` and `KL6_STOP_STANDARD` remain final. |
| Post-KL6 frontier audit | Exact task-relative abstraction and bounded-error alternatives already have adequate mathematical foundations. `FRONTIER_STOP_EXISTING_THEORY_SUFFICES` remains final for the attempted observation-compression research continuation. |
| Next-axis audit | Dependence-aware information comparison is an additional foundation. `NEXT_AXIS_FOUNDATION_ONLY` selected evidence dependence without authorizing another experiment. |

These are inherited conclusions, not computations repeated here. The exposed eighth-grid remains post-hoc development evidence, not a blind replication domain. The KL6 injectivity theorem remains scoped to its stated domain; it is not a universal impossibility theorem for compression. [K §§1, 4–8; P §1; E §1]

**Operational consequence:** `C_*` and `S04` are historical mathematical lessons, not proposed default data structures. Full-model retention is an acceptable baseline when it is needed. Compression is optional; validity is not.

---

## 2. The unit of consequential decision knowledge

### 2.1 A result is a conditional statement

Use the following organizing form, not a mandatory universal serialization:

\[
\mathcal A;\quad F\in\operatorname{Fibre}(s,B);\quad q\in\mathcal Q
\quad\Longrightarrow\quad
\mathcal G_q\bigl(F,d_q(s,B)\bigr).
\tag{1}
\]

Here:

- \(F\) is a model of the appropriate type: probabilistic, dynamic, causal, or another explicitly supported type.
- \(s\) is the retained representation; \(B\) is declared side information available to the recipient.
- \(\operatorname{Fibre}(s,B)\) is the exact set satisfying the representation and original declared constraints, defined in (10). Realized-model claims require justified membership; an inconsistent or unestablished fiber cannot supply an existence witness by vacuous truth.
- A separate sound outer enclosure \(\mathcal U^+(s,B)\) satisfies \(\operatorname{Fibre}(s,B)\subseteq\mathcal U^+(s,B)\). A uniform theorem over that larger set is sufficient for actual fiber members, not proof that the fiber is nonempty or that the enclosure is exact. Without a `+`, a declared \(\mathcal U\) below denotes an exact stated uncertainty set, not an unlabeled relaxation.
- \(\mathcal A\) states the assumptions required by the particular operation and theorem.
- \(q\) is a fully specified downstream query; \(\mathcal Q\) is the family actually covered.
- \(d_q\) is an available decoder, computation, or implementable policy. It cannot secretly consult the discarded original model.
- \(\mathcal G_q\) states the exact equality, inequality, action guarantee, or policy guarantee that follows.

A query includes its horizon, losses and units, feasible actions, information availability, uncertainty criterion, and requested output. When reuse involves auxiliary evidence, the permissible **joint informational contexts** must also be specified. These quantifiers may be written separately rather than hidden in \(q\). A policy returned by \(d_q\) may use later observations only as they become available. It must be defined and executable on all covered histories, not just histories with positive surrogate probability (§4). Semantic factorization of an answer through a representation, an available executable decoder, and a warrant for this application's premises are separate obligations (§5).

Equation (1) is the shared accounting pattern from the audits. It does not reduce interventions to conditioning, uncertainty sets to probability distributions, or all guarantees to one numerical score. [P §§2, 5, 9; E §§2, 7]

### 2.2 Seven obligations for every component

Following the North Star, each reusable component needs an **object**, **assumptions**, **operation**, **guarantee**, **composition rule**, **failure boundary**, and **provenance**. [N]

A theorem establishes an implication. A calculation establishes an instance under its inputs. Empirical evidence may support a modeling assumption. These are different warrants. Neither a correct proof nor an exact calculation proves that an external situation satisfies its model.

For example, “the policy has regret at most \(\rho\)” is incomplete until it identifies the loss, horizon, comparison policy class, true-model class, information available to the policy, and source of the bound. “The source is reliable” cannot replace those fields with a single unsupported number.

### 2.3 Semantic primitives

| Primitive | Mathematical content | Distinction that must not be erased |
|---|---|---|
| Variables and domains | State, observations, actions, time indices, outcome spaces, units, and identity maps | A matching name is not proof of a matching variable, population, time, or regime. |
| Model | Joint law, conditional factors/kernels, or a mechanism-indexed causal family | A marginal law is not a joint law; an observational law is not an intervention law. |
| Information | Observed history, signal/statistic, and information available at each date | Potential future evidence is not current evidence. |
| Decision task | Feasible actions/policies, loss and acquisition cost, horizon, and objective | Probabilistic uncertainty does not determine preferences or authority. |
| Model uncertainty | A known model, distribution over models, or constrained set of models with update semantics | A set is not a prior; a fixed unknown model is not a changing adversary. |
| Representation map | Encoder, statistic, stochastic transformation, abstraction map, decoder, and policy lift | Fewer fields do not establish genuine information loss. |
| Query and result | Posterior, expectation, value, action set, policy, comparison, or bound | Value accuracy, common optimal action, and complete-policy regret are different outputs. |
| Guarantee | Quantified equality/inequality with assumptions, scope, metric, and error budget | Mathematical error, statistical coverage, and substantive model adequacy are different claims. |
| Dependency record | Sources, assumptions, model versions, theorem references, computations, and prior results used | Derivation ancestry is not itself statistical independence or causal structure. |

The table is a proposed organization of the existing objects, not a new ontology claiming to formalize every consequential judgment.

### 2.4 Initial mathematical scope

The explicit computational semantics below start with finite state/action/observation spaces, finite horizons, bounded losses, and one decision-maker. Randomized policies are permitted only where their randomization and information access are specified. Some cited foundations cover broader spaces or discounted horizons; those extensions retain their own hypotheses rather than entering automatically.

No initial-prior grid, kernel grid, selected loss table, or new experimental domain is prescribed. “Finite” is a mathematical scope condition, not an instruction to enumerate another space.

---

## 3. Component I — Joint probability and evidence operations

### Objects and assumptions

The object is a joint law for the payoff-relevant state \(\theta\) and evidence variables \(E_1,\ldots,E_m\), or a justified set of such laws. A numerical prior, likelihood, dependence restriction, and source-to-variable interpretation must be supplied or remain explicitly uncertain.

A report's existence, a report's assertion, and the underlying event are different possible variables. Treating a textual assertion as a measurement of the state requires an explicit modeling step. Provenance identifies the source of that step; it does not automatically validate it.

### Operations and guarantees

**Conditioning.** For an observed event \(e\) with positive model probability,

\[
P_F(\theta\mid e)
=\frac{\mu_F(\theta)P_F(e_1,\ldots,e_m\mid\theta)}
{\sum_{\vartheta}\mu_F(\vartheta)P_F(e_1,\ldots,e_m\mid\vartheta)}.
\tag{2}
\]

Replacing the joint likelihood by a product of separate likelihoods requires the corresponding joint conditional-independence assumption. Distinct source identifiers do not supply it. [E §3.1]

**Elimination.** In a specified factorization, sum over discarded internal variables and retain the resulting factor on the variables through which later calculations connect. In schematic finite form,

\[
\psi_{\mathrm{boundary}}(b)
=\sum_{u}\prod_{j\in J}\psi_j(b,u).
\tag{3}
\]

This is valid when the remaining factors connect to the eliminated region only through the retained boundary. It preserves the quantities obtainable by subsequently combining those factors and summing. A proportional factor may suffice for a particular normalized posterior; the proportionality constant cannot be discarded when an evidence probability, posterior weighting over model identities, or another scale-sensitive query requires it. This last restriction follows directly from the difference between a normalized ratio and an unnormalized likelihood. [E §3.1; elementary specialization]

**Common-information fusion.** When two analyses use \((C,U)\) and \((C,V)\), share a prior, and satisfy \(U\perp V\mid(\theta,C)\),

\[
P(\theta\mid C,U,V)
\propto
\frac{P(\theta\mid C,U)P(\theta\mid C,V)}{P(\theta\mid C)}.
\tag{4}
\]

Apply this on the relevant positive support. The denominator removes duplicated **shared information**, not necessarily just a duplicated initial prior. Residual dependence invalidates the formula even when the overlap is correctly identified. [E §3.2]

### Composition and failure

Evidence can be combined when its variable identities, observation events, and joint dependence assumptions admit one consistent model. If only marginals are known, preserve a set of compatible joint laws rather than select independence for convenience. In finite spaces, supplied marginal constraints define a set such as

\[
\mathcal J=\{P:P(E_i\mid\theta)=P_i(E_i\mid\theta)\text{ for every }i\}.
\tag{5}
\]

Inference then ranges over compatible laws with positive probability for the observed event. Other dependence restrictions may require additional, non-linear constraints. [E §3.3]

Reusing a deterministic derivative of evidence already conditioned on supplies no additional information by itself. Likewise, provenance labels saying “common source” do not fix a numerical dependence structure: an unrestricted latent source can encode the entire report vector and leave all joint laws possible. [E §§3.2–3.3; the deterministic-derivative statement follows from conditioning on a function of existing data]

**Failure boundaries:** impossible conditioning event; unidentified dependence; inconsistent factors; duplicated evidence treated as independent; a dropped factor needed by a new query; or approximate loopy inference presented as exact. The remedy is a narrower guarantee, an explicit compatible-law set, or a blocked operation—not a fabricated probability.

**Provenance:** record the joint model/factorization, actual shared evidence, independence assumptions, support conditions, and each marginalization or update. Established foundations are Bayes conditioning, sum-product inference, common-information fusion, and credal/joint-law analysis. [E §§3.1–3.3; references E:A3–A6]

---

## 4. Component II — Information, policies, and sequential decisions

### Objects and assumptions

A deterministic policy selects a feasible action measurably with respect to the information \(\mathcal I_t\) available at date \(t\). A randomized policy instead supplies a history-measurable probability distribution over feasible actions, or uses an explicitly allowed private random seed with actions measurable with respect to \(\mathcal I_t\) augmented by that seed. Specify the seed's independence and what any model-selecting adversary can observe; private randomization is not automatically available in every decision criterion. With perfect recall, \(\mathcal I_t\subseteq\mathcal I_{t+1}\). Any memory restriction must instead be declared in the policy class.

**Common implementability includes support.** A transferred policy, its update procedure, and any lift must give a legal executable response at every history possible under any covered model, including histories impossible under the surrogate, and continue legally thereafter until termination. A predeclared feasible off-support response may complete the policy; it is not a surrogate posterior or a claim of conditional optimality. Alternatively, prove the requisite support inclusion so that the surrogate procedure is defined on all such histories. Include the surrogate's own possible histories when comparing policies across models. An unmodeled crash, missing branch, or refusal has no certified bounded policy loss. This makes the existing implementability premise explicit; it does not request a transferred-policy feature in Build 1. [REV Finding 3]

Let \(J_F^h(\pi)\) be expected future loss, including acquisition costs, for a common implementable policy \(\pi\) and horizon \(h\). Define

\[
V_F^h=\min_{\pi\in\Pi_h}J_F^h(\pi),
\qquad
\Pi_{F,h}^{*}=\operatorname*{argmin}_{\pi\in\Pi_h}J_F^h(\pi).
\tag{6}
\]

Minima here use a nonempty finite policy class, or an explicitly justified setting in which an optimum exists. A model-informed oracle may choose a different history rule in each model for the regret benchmark; the recipient’s actual chosen rule must be available from its retained information. Already-paid costs are not continuation costs. Preferences, feasibility constraints, and the uncertainty criterion are inputs to this problem; they are not inferred from probability alone. [K §2; P §§2.3, 5.3; E §5.1]

### Operations and guarantees

**Known-model history compression.** A statistic \(z_t\) may replace history when it determines the conditional immediate-loss and future-information quantities required by the permitted continuation problem. It must have an available update rule. In the known POMDP case, the posterior over the appropriate hidden state is the standard information state; its computation still uses the known model. [P §§2.1, 3.1]

**Bellman evaluation.** The already-established static-state stopping model provides a complete explicit baseline. Use finite nonempty state, terminal-action, and observation alphabets; a normalized nonnegative prior \(b\); a nonnegative row-normalized channel \(K\); finite terminal losses \(L(a,\theta)\); a finite fee \(c\ge0\); and integers \(H\ge0\), \(0\le h\le H\). Exact evaluation here permits signed losses; the approximation profile in §6 is narrower. Repeated draws, when permitted, are conditionally independent from that same stationary channel. The terminal action menu is unchanged, observations do not change the state, and fees and losses use the same declared unit. Then

\[
m_x(b)=\sum_\theta b(\theta)K(x\mid\theta),
\qquad
b_x(\theta)=\frac{b(\theta)K(x\mid\theta)}{m_x(b)}\quad\text{only if }m_x(b)>0,
\tag{7}
\]

\[
R(b)=\min_a\sum_\theta b(\theta)L(a,\theta),
\qquad V^0(b)=R(b),
\]

\[
O^h(b)=c+\sum_{x:m_x(b)>0}m_x(b)V^{h-1}(b_x),
\qquad
V^h(b)=\min\{R(b),O^h(b)\},\qquad 1\le h\le H.
\tag{8}
\]

Retain all terminal minimizers and all STOP/OBSERVE minimizers. At \(h=0\), STOP is forced, \(V^0=R\), and \(O^0=\mathrm{NA}\); no observation margin is defined. Forced termination is not a demonstrated strict preference. At \(m_x(b)=0\), the posterior, conditional losses, and conditional minimizers are `NA`, not ties. Omit that branch from every posterior-dependent sum: do not evaluate `0 * NA`. Its unnormalized contribution to an expectation is zero. A legal off-support policy response under the preceding premise does not change these conditional-answer semantics. [K §2; P §6]

**Value of information.** Under the same model and unchanged terminal action menu,

\[
v(b)=R(b)-\sum_{x:m_x(b)>0}m_x(b)R(b_x)
\]

is the one-step value before acquisition cost. The sequential comparison satisfies the elementary identity

\[
R(b)-O^h(b)
=[v(b)-c]+\sum_{x:m_x(b)>0}m_x(b)\bigl[R(b_x)-V^{h-1}(b_x)\bigr],\qquad 1\le h\le H.
\tag{9}
\]

It follows by adding and subtracting the expected posterior terminal risk. Nonpositive one-step net value does not eliminate the additional continuation benefit. This is the precise obstruction illustrated by the inherited equal-`C_*` separation. [K §§2, 5; algebraic consequence of (8)]

### Composition and failure

A continuation value can enter a Bellman backup only when it belongs to the same continuation model, remaining horizon, units, feasible actions, and accessible information state. An answer about \(V^h\) at one horizon is not a certificate for all earlier or later horizons. A root answer is not a complete conditional policy tree.

With dependent future reports, a posterior over \(\theta\) alone may omit information needed to predict those reports. A larger sufficient state or the full relevant history is then required. Merely keeping the same numerical posterior cannot import the conditionally independent model of (7)–(8). [P §§2, 6.7; E §§3.1, 3.4]

**Failure boundaries:** omitted model inputs; future information used prematurely; changed cost or action menu; inaccessible policy update; belief state lacking predictive sufficiency; or a fixed-model Bellman recursion applied to the wrong ambiguity semantics.

**Provenance:** retain the policy class, information schedule, terminal/observation cost definitions, model, and calculation or theorem used. Exact rational arithmetic supports exact claims for finite rational instances. A numerical approximation needs its own error treatment; apparent numerical equality does not certify an exact tie. [K §§2, 8.2]

---

## 5. Component III — Representations and exact preservation

### Objects and assumptions

A model representation is an encoder \(S\), retained payload \(s=S(F)\), side information \(B\), and available decoding/update mechanisms. Its exact compatible fiber is

\[
\operatorname{Fibre}(s,B)=\{F\in\mathfrak F:S(F)=s,\ B(F)=B\}.
\tag{10}
\]

Here \(\mathfrak F\) includes the original declared model constraints. A sound outer enclosure obeys \(\operatorname{Fibre}(s,B)\subseteq\mathcal U^+(s,B)\); it may contain models that do not produce the payload or satisfy the original constraints. Its nonemptiness alone is not evidence of exact compatibility (§10.2). Do not define a fiber by the enclosure and thereby erase that distinction.

History compression, model compression, and observation compression remain different types of map. A result about one cannot be used as a theorem about another without a bridge establishing the missing premises. [P §2]

### Operations and guarantees

**Exact query preservation.** A mathematical answer map satisfying

\[
d_q(S(F),B)=Q_q(F)
\tag{11}
\]

exists on the realized representation image exactly when \(Q_q\) is constant on each **exact** fiber. This is semantic factorization, not by itself an effectively computable or receiver-available decoder. In a finite explicitly given domain, a lookup can construct such a decoder, with its own representation and computational cost. In general, retain three separate warrants: semantic sufficiency, a specified executable decoder for the claimed use, and evidence that its premises apply. An explicit finite rule or a theorem with instantiated premises can provide the warrant; no general automated theorem prover is required. [P §5.1; REV Finding 5]

Constancy over a sound outer enclosure is sufficient for constancy on its nonempty exact fiber, but is not necessary. A separating pair in the enclosure refutes the outer-set claim only, unless the pair is shown to satisfy the original fiber constraints. Claims of exact query-quotient equality or minimal retained information concern the exact domain, not an unlabeled relaxation.

**Common action versus complete answer.** A representation permits one universally optimal action when

\[
\bigcap_{F\in\operatorname{Fibre}(s,B)}A_q^*(F)\ne\varnothing.
\tag{12}
\]

This is an existence criterion on a nonempty exact fiber, with the same feasible action meaning throughout. An intersection over an outer enclosure supplies a sufficient, possibly more restrictive certificate; its emptiness does not alone disprove a common optimum on the fiber. Preserving the full minimizing set requires those sets to be equal. Preserving a whole policy requires a common implementable policy on the covered history supports (§4), not merely common root actions supported by different inaccessible continuation plans. Existence of such a policy and provision of an executable selection remain distinct. [P §§2.3, 5.1]

**Structural exact abstraction.** For a finite-horizon fully observed MDP with a common action set and state map \(\phi\), suppose terminal costs factor through \(\phi\), and for every relevant state/action/date,

\[
g_t(x,a)=\bar g_t(\phi(x),a),
\]

\[
\sum_{y:\phi(y)=z'}P_t(y\mid x,a)
=\bar P_t(z'\mid\phi(x),a).
\tag{13}
\]

Backward induction gives \(V_t(x)=\bar V_t(\phi(x))\), and an abstract optimal policy lifts to an optimal original policy. Transitions within the abstract classes can genuinely differ. Thus exact preservation need not reconstruct the full underlying dynamics. Applying this principle to partial observation additionally requires an accessible information-state map and valid filtering/policy lift. [P §§3.1, 4.2]

Value-equivalence methods preserve specified Bellman tests rather than every transition entry. Their sufficiency depends on covering the continuation functions actually used. Agreement on a present test collection is not enough if subsequent backups or minimization leave that collection. [P §§3.2, 4.3]

### Composition and failure

An abstraction may feed a decision calculation when the query and policy lift lie within the abstraction theorem's scope. It may feed another abstraction only with compatible maps and preserved intermediate premises; §10 states the composition rules.

**Failure boundaries:** finite-domain injectivity mislabeled as compression; an answer table mislabeled as a discovered structural interface; all necessary model information hidden in the decoder; or a guarantee silently extended to new rewards, interventions, auxiliary evidence, or conditional histories.

Full-model retention, full predictive retention, exact task abstraction, and exact action agreement are distinct regimes. None must be called “compression” to be useful. The closed KL6 result belongs specifically to the model-identifying regime. [K §4.8; P §§4, 10]

**Provenance:** identify the encoder, side information, domain, decoder, query family, and constructive theorem or exact sufficiency argument. Keep semantic information loss separate from storage size, runtime, and the difficulty of discovering the representation.

---

## 6. Component IV — Approximation, regret, and certified margins

### Objects and assumptions

An approximate representation retains a surrogate, a valid decoder or policy lift, an explicit metric/error bound, and the model class over which that bound holds. Error budgets have units and query scopes. They are not confidence probabilities.

**Domain of the coupling certificate (14)–(19b).** Use the finite nonempty alphabets and static, stationary conditionally independent observation model of §4, a common known prior, the same feasible terminal actions, common terminal losses \(0\le L(a,\theta)\le L_{\max}<\infty\), and a common fee \(0\le c<\infty\). Let \(H\in\mathbb N_0\), \(h\in\{0,\ldots,H\}\), and \(0\le d_s<\infty\). Every policy compared must be executable on the union of the covered models' and surrogate's possible histories as specified in §4; the common class must include legal extensions of the compared optimal policies. All approximation and optimization error allowances below are finite and nonnegative. These conditions do not follow merely from an input being valid for Build 1. The common surrogate channel must satisfy

\[
\sup_\theta\operatorname{TV}\bigl(K_F(\cdot\mid\theta),\widehat K_s(\cdot\mid\theta)\bigr)
\le d_s
\quad\text{for every }F\in\operatorname{Fibre}(s,B),
\tag{14}
\]

with \(\operatorname{TV}(P,Q)=\tfrac12\sum_x|P(x)-Q(x)|\). The retained information must justify the uniform bound and the actual model's membership; a different undisclosed decoder for each original model does not qualify. The bound may instead be established over a stated sound \(\mathcal U^+(s,B)\), with every outer member satisfying this same profile and policies executable over that coverage as well. This gives a conservative sufficient certificate for fiber members, not an existence witness or minimal-error claim. [P §§6.1–6.2]

**Fixed domain check.** The review's signed-loss example has prior \((1/2,1/2)\), \(c=0\), \(L=[[-99,1],[1,-99]]\), and binary channels \(k=(0,1)\), \(k'=(1/100,99/100)\). Their one-observation optimal values are \(-99,-98\), differing by \(1\). Their channel distance is \(1/100\); using only the upper bound \(L_{\max}=1\) would incorrectly assert error at most \(1/100\). The omitted premise is \(L\ge0\), not a failure of the stated theorem. Likewise, \(L_{\max}=1,h=1,c=-2,d=1/10\) would give a negative printed bound; such a fee is outside the profile. No signed-loss coupling extension or approximate solver is added here. [REV Finding 2]

### Operations and guarantees

Set

\[
e_h(s)=(L_{\max}+hc)\min\{1,h d_s\},\qquad h\in\{0,\ldots,H\}.
\tag{15}
\]

Under the stated nonnegative bounded-loss and finite nonnegative-fee domain, the inherited coupling argument gives, for every common history policy defined on the covered supports and every integer \(0\le h\le H\),

\[
|J_F^h(\pi)-J_{\widehat F_s}^h(\pi)|\le e_h(s).
\tag{16}
\]

Consequently,

\[
\begin{aligned}
|V_F^h-V_{\widehat F_s}^h|&\le e_h(s) &&(0\le h\le H),\\
|O_F^h-O_{\widehat F_s}^h|&\le e_h(s) &&(1\le h\le H).
\end{aligned}
\tag{17}
\]

The second line minimizes over policies **forced to observe initially**, a different subset from the unrestricted stopping-policy class. It is undefined at \(h=0\). For \(h\in\{0,\ldots,H\}\), if the implemented total surrogate policy has a separately justified \(0\le\eta_h<\infty\) satisfying \(J_{\widehat F_s}^h(\widehat\pi_s)-V_{\widehat F_s}^h\le\eta_h\), its **whole-policy** regret in every covered fiber member is bounded by

\[
J_F^h(\widehat\pi_s)-V_F^h\le 2e_h(s)+\eta_h.
\tag{18}
\]

These consequences use uniform policy comparisons, not just closeness of two optimal values. Their proof couples potential observation strings (and permitted private randomness), bounds the mismatch probability by \(\min\{1,hd_s\}\), and uses the total loss range \([0,L_{\max}+hc]\). Taking minima over the same class proves (17); inserting both surrogate policy value and surrogate optimum in the regret difference proves (18), with its separate \(\eta_h\) term. [P §§6.2–6.4]

**Fixed support check.** In the review's example, the surrogate never emits `x1`; the covered channel emits it with probability \(1/100\) in state 1 and zero in state 0. At prior \(1/2\), its actual mass is \(1/200\). The surrogate posterior remains `NA`. A predeclared feasible response may extend the surrogate policy without changing its nominal value, but its loss on this event is included in \(J_F^h\). Neither a fabricated belief nor an unmodeled crash supplies that response. The claim is ex ante policy loss, not conditional optimality on this event. [REV Finding 3]

For integer \(1\le h\le H\), under the same domain and uniform bound, use the **exact** surrogate forced-observation optimum and the shared exact STOP risk: \(\widehat\Gamma_h=R-O_{\widehat F_s}^h\). Then

\[
\widehat\Gamma_h>e_h \implies \text{strict OBSERVE in every compatible model},
\]

\[
\widehat\Gamma_h<-e_h \implies \text{strict STOP in every compatible model}.
\tag{19}
\]

An interval containing zero supplies no strict-action certificate. It does not establish an actual tie. Equation (19) uses exact surrogate mathematical values, not unqualified solver output. [P §6.5]

**Computed comparison and separate error sources.** Still for \(1\le h\le H\), suppose finite \(\xi_{R,h},\xi_{O,h}\ge0\) are actually justified for computed numbers:

\[
|\widetilde R_h-R|\le\xi_{R,h},\qquad
|\widetilde O_h-O_{\widehat F_s}^h|\le\xi_{O,h}.
\tag{19a}
\]

Let \(\widetilde\Gamma_h=\widetilde R_h-\widetilde O_h\) and \(\Gamma_h(F)=R-O_F^h\). Adding and subtracting the exact surrogate values, then applying (17) and the triangle inequality, gives

\[
|\widetilde\Gamma_h-\Gamma_h(F)|
\le\xi_{R,h}+\xi_{O,h}+e_h=:\delta_h.
\tag{19b}
\]

Certify strict OBSERVE only if \(\widetilde\Gamma_h>\delta_h\), or strict STOP only if \(\widetilde\Gamma_h<-\delta_h\). Otherwise no strict sign is certified. Exact rational evaluation of these two optima has \(\xi_{R,h}=\xi_{O,h}=0\). For a general finite action menu with separately justified total action-value errors, sum the two relevant errors when comparing actions; a uniform finite \(e\ge0\) makes a unique true-action gap greater than \(2e\) sufficient. This does not establish tie preservation.

The error roles must remain distinct:

- \(e_h\) bounds **model approximation** over the stated covered set.
- \(\xi_{O,h}\) bounds error against the **forced-observation optimum**. For example, if a legal forced-observation policy has certified nominal suboptimality \(\eta_{O,h}\ge0\) and its evaluated cost has error \(\epsilon_{O,h}\ge0\), both finite, then \(\xi_{O,h}=\eta_{O,h}+\epsilon_{O,h}\) is conservative by another triangle inequality. Without such certificates, no optimizer/evaluation error bound is available.
- \(\eta_h\) in (18) bounds **unrestricted whole-policy suboptimality**. An optimal policy may stop without evaluating observation; its \(\eta_h\) supplies no automatic bound on an uncomputed forced-observation optimum.
- Statistical coverage concerns a separate model-membership event and is composed in §10.10, not added to a loss-valued radius.

**Fixed margin check.** With zero model error, true margin \(-1/1000\), computed margin \(1/1000\), and certified numerical allowance \(1/500\), the comparison interval is \([-1/1000,3/1000]\). Ignoring numerical error would wrongly certify OBSERVE; (19b) certifies neither sign. These are review/conformance quantities, not an added approximate solver. [REV Finding 4]

**Partially observed generalization.** Approximate information states supply a separate established route using recursively updated information states, immediate-loss error, and next-state prediction error. Under that theorem's instantiated uniform conditions, take finite integer \(T\ge1\), dates \(t=1,\ldots,T\), a supplied finite bounded stage-loss range as required by the AIS theorem, and finite nonnegative \(\epsilon_t\), \(\delta_t\), and continuation-function bounds \(\rho_{\mathcal G}(\widehat V_{t+1})\). Conditional quantities are required only where the relevant history is possible; the lifted policy must still be executable on all covered histories. This separate AIS theorem does not relax the nonnegative-loss domain of the coupling certificate. Its finite-horizon error recursion has the form

\[
\alpha_t=\epsilon_t+
\rho_{\mathcal G}(\widehat V_{t+1})\delta_t+\alpha_{t+1},
\qquad\alpha_{T+1}=0,
\tag{20}
\]

with value/action-value error \(\alpha_t\) and lifted-policy loss bounded by \(2\alpha_t\). Here \(\delta_t\) bounds predictions in the declared integral probability metric and \(\rho_{\mathcal G}\) controls the relevant continuation function. An application must establish the actual update, prediction, continuation-function, and policy-lifting premises; keeping the recursion alone is not a certificate. For model-description compression, the premises must hold uniformly over its compatible models. [P §3.3; reference P:R6, Definition 7 and Theorem 9]

### Composition and failure

Uniform errors may be propagated through compatible operations using §10. A root expectation bound does not survive arbitrary conditioning unchanged: rare histories can enlarge discrepancies and produce different posteriors. Nor does root action agreement certify a complete policy tree. [P §§6.5, 6.7]

**Failure boundaries:** a violated loss/fee/horizon domain; a distance not controlling the relevant continuation functions; nonuniform error over the claimed coverage set; an off-support policy gap; an unavailable decoder; unjustified optimizer/evaluation accuracy; or an error budget too large to support the requested claim. A valid but vacuous bound should remain visible as such. A failure of an outer-set certificate need not refute a tighter fiber-specific guarantee.

**Provenance:** retain the metric convention, error proof, model-membership warrant, surrogate, policy class, numerical/planning error, and covered histories/horizons. A statistical coverage statement for model membership is an additional claim, not a consequence of (14)–(20). [P §§6, 9.2]

---

## 7. Component V — Information comparison and dependence-aware reuse

### Objects and assumptions

There are two related but different objects: experiments compared as information resources, and signals that coexist on a specified joint probability space. Their timing and acquisition costs must be explicit.

### Operations and guarantees

**Blackwell comparison and deficiency.** An experiment \(E\) can simulate \(G\) when a state-independent stochastic transformation \(T\) maps its conditional observation laws to those of \(G\). Approximate simulation uses

\[
\delta(E,G)=\inf_T\sup_\theta
\operatorname{TV}(TP_\theta,Q_\theta).
\tag{21}
\]

For finite experiments, \(0\le\delta(E,G)\le1\). With losses \(0\le L\le1\), the same prior, and executable available decision rules, the corresponding optimal risks satisfy

\[
R_E^*\le R_G^*+\delta(E,G).
\tag{22}
\]

A loss range \(0\le L\le L_{\max}<\infty\), with \(L_{\max}\ge0\), scales the error term by \(L_{\max}\). These are information-resource comparisons; different acquisition costs or decision restrictions require a matching comparison. A transform of an entire final signal string need not be available early enough for a sequential stopping policy. Sequential transfer requires an appropriately nonanticipative simulator. [P §8]

**Joining evidence.** Seeing \(X\) together with \(Z\) means using their joint information, \(\sigma(X)\vee\sigma(Z)\). It does not mean multiplying marginal likelihoods. For a deterministic coarsening \(Y=f(X)\), posterior preservation in a specified context requires

\[
P(\theta\mid X,Z)=P(\theta\mid Y,Z)\quad\text{almost surely},
\tag{23}
\]

equivalently \(\theta\perp X\mid(Y,Z)\). Sufficiency before receiving \(Z\) does not establish (23). [E §§3.4, 3.7]

**Universal correlated contexts.** The adopted static reveal-or-refine result characterizes dominance under every decision problem and every correlated auxiliary signal on the common underlying space: each realization of the dominant signal must either reveal the payoff-relevant state or determine the other signal. This is dominance in attainable decision value, not equality of labeled policy trees. [E §3.5; E:A1]

For finite deterministic coarsening, the audit's exact specialization is especially usable: (23) holds for every auxiliary signal precisely when every positive-probability \(Y\)-cell either fixes \(\theta\) or fixes \(X\), almost surely. A discarded distinction in an unresolved cell can otherwise matter after combination. [E §3.6]

The dynamic extension recorded in the audit applies date by date to exogenous cumulative signals and nonanticipative actions. Its cited May 2026 author-manuscript status and exogenous-information scope are retained. It is not an unrestricted controlled-sensing or intervention theorem, and is not necessary for the basic finite static coarsening result. [E §§3.5–3.7; E:A2]

### Composition and failure

Every reuse guarantee must distinguish isolated use, a specified joint context, a declared restricted context family, and arbitrary correlated auxiliary information. A guarantee for the first is not a guarantee for the last. A model-description certificate must establish the required relation in its compatible **joint** models; naming a signal-comparison theorem does not supply their unknown coupling.

**Failure boundaries:** an unspecified joint law; standalone sufficiency used after new correlated evidence; a noncausal simulator used online; utility depending on a variable omitted from the payoff-relevant state; or dominance promoted to exact decisions without justification.

**Provenance:** identify the information sources and their transformations, the joint context, timing, comparison theorem, and exact guarantee type. The key cumulative gain is a rule for **safe combination**, not merely another rule for safe summarization. [E §7]

---

## 8. Component VI — Model uncertainty and robust decisions

### Objects and assumptions

Use either a known \(F\), a distribution \(\nu\) over models, or a nonempty set \(\mathcal U\). State whether the model remains fixed, is learned about, or may change according to a specified adversary. The admissible policy must use only the information supplied to the recipient.

### Operations and guarantees

The following objectives must remain different:

\[
\begin{array}{ll}
\text{Known model:}&\displaystyle \inf_\pi J_F(\pi),\\[2mm]
\text{Bayesian model uncertainty:}&\displaystyle \inf_\pi\int J_F(\pi)\,\nu(dF),\\[2mm]
\text{Fixed-model robust loss:}&\displaystyle \inf_\pi\sup_{F\in\mathcal U}J_F(\pi),\\[2mm]
\text{Minimax regret:}&\displaystyle \inf_\pi\sup_{F\in\mathcal U}[J_F(\pi)-V_F].
\end{array}
\tag{24}
\]

An interval or a list of plausible models does not select one of these criteria. The model-specific oracle \(V_F\) makes regret different from worst-case loss. If \(\mathcal U^+\) is used in place of an exact \(\mathcal U\), with the same legal policy class and defined finite losses, its robust-loss or regret objective is conservative for that smaller set, not necessarily its exact optimum. Policy randomization and Nature's knowledge of it must remain explicit (§4). [P §9.3; E §5.1]

**Answer identification.** Evaluate a defined query across a nonempty **exact** compatible set. A constant answer is identified. Otherwise report the set or a labeled sound enclosure of possible answers. If only an outer enclosure was evaluated, variation there is not proof of variation on the original set. For any nonempty exact set \(\mathcal U\) and real scalar query \(Q\) bounded above and below on it, the optimal unrestricted scalar approximation has error half its range:

\[
\inf_v\sup_{F\in\mathcal U}|Q(F)-v|
=\frac{\sup_{F\in\mathcal U}Q(F)-\inf_{F\in\mathcal U}Q(F)}2.
\tag{25}
\]

For the original representation problem use \(\mathcal U=\operatorname{Fibre}(s,B)\). Equation (25) follows because no scalar is less than half the query range from both extremes (or their limiting sequences), and the midpoint achieves that bound. Thus a finite tolerance \(\varepsilon\ge0\) is achievable as an unrestricted scalar answer exactly when the fiber's range width is at most \(2\varepsilon\). This is a semantic minimum; a usable algorithm for the extrema or midpoint is a separate obligation.

The same identity is mathematically valid with a nonempty outer \(\mathcal U^+\) on which \(Q\) is defined and bounded, but then it minimizes error for the **relaxed** problem only. Its midpoint bound is sufficient, possibly conservative, for actual fiber members. It need not be the fiber's minimal error, and failure of an outer tolerance is not impossibility on the fiber. No range formula here applies to an empty set. This does not provide a cheap optimizer or a surrogate simultaneously realizing several query midpoints. A common action may still be identified without identifying the entire model or all values; use (12). [P §5; REV Finding 1]

**Uncertainty geometry.** Upper expectations of all linear outcome losses depend on the closed convex hull of a set of outcome distributions. At the policy level, preserve the relevant functional of the whole vectors \((J_F(\pi))_{\pi\in\Pi}\), or the distinct regret vectors \((J_F(\pi)-V_F)_{\pi\in\Pi}\). Independently convexifying local transition rows is not the same operation. [E §5.2]

### Composition and failure

A model chosen once for the episode must remain the same model in all factors of its trajectory law:

\[
\int\prod_t P_F(o_t\mid h_{t-1},a_t)\,\nu(dF)
\ne
\prod_t\int P_F(o_t\mid h_{t-1},a_t)\,\nu(dF)
\quad\text{in general}.
\tag{26}
\]

Bayesian learning must retain the information needed to update model identity. Set-based learning must preserve which global models remain possible and the stipulated updating semantics. Conditioning a set of probability laws means conditioning its eligible members, not inventing posterior weights over them. [E §5.3; P §9.3]

Robust Bellman methods can be used only under their applicable uncertainty and temporal-consistency conditions. Allowing an independent worst-case model at each node may be a conservative relaxation, but it changes a fixed-model problem unless an equivalence theorem applies. No claim is made that all nonrectangular uncertainty is intractable. [E §§5.3–5.4]

**Failure boundaries:** empty compatible set; fabricated model weights; independently combined local ranges that admit impossible global models; a minimax-loss answer relabeled as minimax regret; or changed uncertainty timing.

**Provenance:** preserve the origin and constraints of the uncertainty set/distribution, its update rule, the objective, model persistence, and the exact theorem supporting any dynamic decomposition.

---

## 9. Component VII — A distinct causal interface

### Objects and assumptions

A causal claim requires a mechanism model, permitted interventions, or a causal identification result under stated assumptions. For a recursive structural causal model,

\[
V_i=f_i(V_{\operatorname{pa}(i)},U_i),
\]

interventions replace mechanisms. The relevant object is the family \(\{P_F^{\operatorname{do}(i)}:i\in\mathcal I\}\), not just an observational distribution. [E §4.1]

### Operations and guarantees

For an outcome map \(\tau\) and permitted-intervention map \(\omega\), exact preservation requires an appropriate causal transformation satisfying

\[
\tau_\#P_{F_L}^{\operatorname{do}(i)}
=P_{F_H}^{\operatorname{do}(\omega(i))}
\quad\text{for the covered interventions}.
\tag{27}
\]

If losses and intervention costs also factor through these maps, expected intervention losses agree. An onto action map covering the permitted high-level menu permits optimal-value equality and lifting of an optimizer. With instead a finite uniform total-variation allowance \(d\ge0\), common losses \(0\le L\le L_{\max}<\infty\) with \(L_{\max}\ge0\), and exactly matched finite intervention costs and action coverage, the corresponding action-risk error is at most \(L_{\max}d\) and lifted-optimizer regret at most \(2L_{\max}d\). These are the specialization and qualifications already stated in the next-axis audit. [E §§4.2–4.3]

### Composition and failure

Causal transformations compose only with compatible outcome/intervention maps, costs, and intervention domains. An observational model cannot enter (27) by substituting conditioning for intervention. Adaptive intervention policies require preservation of the relevant policy-induced laws and information access, not an unsupported extrapolation from a few atomic interventions. [E §§4.3–4.4]

**Failure boundaries:** unrepresented confounding or mechanisms required by the chosen identification theorem; changed intervention semantics; unmatched costs or available actions; or observational equivalence used as causal equivalence. Failure to identify a complete intervention distribution does not automatically mean no action is identifiable.

**Provenance:** causal assumptions, regime/environment, data and identification argument, interventions, abstraction maps, and policy-lifting conditions. Transport to another environment additionally needs the specified restrictions on which mechanisms change. [E §§4.4–4.6]

This component provides a boundary and a conditional interface. It does not assert that a general causal-policy solver, a new identification theorem, or a full sequential causal-abstraction implementation has been earned.

---

## 10. Composition rules

This is the connective part of the substrate. The following rules assemble the supplied guarantees. Where a rule goes beyond a source's displayed formulation, its elementary justification is included. None claims a novel composition theorem.

### 10.1 Match meanings and discharge the next operation's premises

Before substituting an output for an input, match the variable/state identities, units, prior or information state, model regime, permitted actions, horizon, uncertainty criterion, and output type that the next operation actually requires. A supplied map can establish a valid correspondence; matching labels cannot.

If an operation proves \(\Gamma_1\) under \(\mathcal A_1\), and the next requires \(B_2\), composition needs \(\Gamma_1\) and the other available premises to imply \(B_2\). Simply having two individually valid results is insufficient.

**Example of a prohibited substitution:** an accurately estimated optimal value is not a transferred policy with low regret. Equations (16)–(18) supply the additional policy comparison needed for that particular conversion. [P §§2.3, 6.4]

### 10.2 Require a compatible global model—not merely compatible descriptions

For records defined on different local views, let \(r_i(F)\) be the restriction of a proposed global model to the variables and assumptions of record \(i\). In (28), each \(\mathcal U_i\) is the **exact** local constraint set (the exact fiber where that is the source of the constraint), not an outer enclosure. Define

\[
\mathcal U_{\mathrm{joint}}
=\{F:r_i(F)\in\mathcal U_i\ \forall i,
\text{ and }F\text{ satisfies the declared joining assumptions}\}.
\tag{28}
\]

The result may be used jointly only with justified nonemptiness of this exact set and the required guarantee over its relevant members. An actual member, or another valid existence proof, establishes original-model compatibility; it establishes neither a unique answer nor real-world membership.

If \(\mathcal U_i\subseteq\mathcal U_i^+\) is justified for every record, replacing the local sets in (28) by their outer enclosures while keeping the declared joining assumptions defines \(\mathcal U_{\mathrm{joint}}^+\), and

\[
\mathcal U_{\mathrm{joint}}\subseteq\mathcal U_{\mathrm{joint}}^+.
\tag{28a}
\]

An **empty outer intersection** therefore proves that the original joint set is empty, conditional on those enclosure and joining premises. A **nonempty outer intersection** proves only feasibility of the relaxation. Its points need not satisfy any original fiber constraints; it is not an original-model compatibility witness. Exact nonemptiness requires such a witness or an existence proof. Uniform outer-set guarantees remain sufficient for actual members, but neither supply those members nor justify vacuous action certification. If joining constraints are also relaxed, their own sound-enclosure implication must be established.

**Fixed rational counterexample.** Let the exact constraints be \(\mathcal U_A=\{1/4\}\) and \(\mathcal U_B=\{3/4\}\), for the same parameter \(p\). Sound outer sets are \(\mathcal U_A^+=\{1/4,1/2\}\) and \(\mathcal U_B^+=\{1/2,3/4\}\). The exact intersection is empty; the outer intersection is \(\{1/2\}\). Its sole point satisfies neither original singleton constraint. The enclosures are sound, but inferring original compatibility from their overlap is false. [REV Finding 1]

When two constraints refer to the same model and both are warranted, intersection is appropriate. When they describe unresolved alternative explanations, intersection may incorrectly erase the alternatives; retain the alternatives instead. Marginal consistency alone is not permission to choose an arbitrary dependence structure. This is an application of the compatible-joint-law and fiber semantics, not a separate calculus. [E §§2, 3.1–3.3; P §5]

### 10.3 Restrict scope safely; do not enlarge it silently

A uniform guarantee over \(\mathcal U\times\mathcal Q\times\mathcal Z\) remains valid over nonempty model subsets and smaller covered query/context families, with the same meanings. This follows by restricting a universal quantifier.

The reverse directions do not follow. Enlarging the model set, loss family, future evidence family, action menu, or horizon needs another applicable guarantee. Restricting an outer enclosure is sound only when the new enclosure still demonstrably contains the original admissible set; arbitrarily deleting inconvenient outer members is not a sound refinement. A guarantee **through** \(H\) includes its declared smaller horizons; a guarantee only **at** \(H\) need not. Preserving one minimizing set is not preserving all point-horizon queries.

A pure model-set restriction for the same scalar query cannot widen its exact range. **Observing new evidence is not merely this operation:** conditioning changes the query and may change uncertainty in other ways. Do not infer that every posterior interval must narrow. [P §§5, 6.7, 10; elementary quantifier and range consequences]

### 10.4 Exact transformations compose with explicit decoders and lifts

If \(s_1=S_1(F)\), \(s_2=T(s_1)\), and an available decoder satisfies

\[
d_2(T(s_1))=d_1(s_1)=Q(F)
\]

throughout the covered domain, then \(T\circ S_1\) preserves \(Q\). The equation supplies the proof. Knowing that each transformation preserves *some* query is insufficient when the queries differ.

For state or causal abstractions, compose the state/outcome maps and action/intervention maps only when the intermediate domains and lifting requirements match. Applying the preserved distribution or transition identities twice proves the composite identity. Policy lifts must remain executable at each date on the union of possible covered histories, including any surrogate-impossible histories. A formal composite map alone does not establish an available implementation. [P §§4.2–4.3; E §§4.2–4.3; elementary substitution]

### 10.5 Propagate approximation in the correct metric and units

For finite real scalar intermediates, finite \(e_1,e_2\ge0\), and a finite Lipschitz constant \(L_f\ge0\), suppose

\[
|y-\widehat y|\le e_1,
\qquad
|\widehat z-f(\widehat y)|\le e_2,
\]

and \(f\) is \(L_f\)-Lipschitz on the relevant domain. Then

\[
|\widehat z-f(y)|\le e_2+L_f e_1.
\tag{29}
\]

The proof is the triangle inequality plus the Lipschitz bound. Additive error without a multiplier is valid only for a matching nonexpansive transformation, such as identity in the same units. Division by an uncontrolled small probability is not such a transformation; this is one reason conditioning needs special treatment.

For model approximations \(F_0,F_1,F_2\) at the same finite integer horizon (when sequential), use finite nonnegative \(e_1,e_2\), a nonempty common whole-policy class executable on all covered supports, and existing comparison optima. If that class satisfies

\[
\sup_\pi|J_{F_0}(\pi)-J_{F_1}(\pi)|\le e_1,
\quad
\sup_\pi|J_{F_1}(\pi)-J_{F_2}(\pi)|\le e_2,
\]

then the policy-value error from \(F_0\) to \(F_2\) is at most \(e_1+e_2\). For a separately justified finite \(\eta\ge0\), an \(\eta\)-optimal final policy has original-model regret at most

\[
2(e_1+e_2)+\eta.
\tag{30}
\]

This follows by the triangle inequality and the optimizer comparison used in (18). With different policy spaces, an analogous claim requires lifts and coverage of the comparison optima; it does not follow from notation alone.

These are conditional error rules, not a new numerical solver. If their policy-value premises are obtained using (14)–(18), that profile’s nonnegative bounded losses, finite nonnegative fees, integer horizons, and support conditions must first hold. For computed STOP/OBSERVE values, apply the separate optimum/evaluation error accounting in (19a)–(19b), not the whole-policy eta allowance. Local regret numbers cannot generally be added and called whole-policy regret without the relevant dynamic argument. Likewise, two “within \(\varepsilon\)” relationships do not compose into another “within \(\varepsilon\)” relationship. [P §§5.4, 6.4, 9.4; elementary consequences]

### 10.6 Compose information simulators with timing intact

For probability laws on compatible finite alphabets and state-independent stochastic transforms with nonnegative normalized rows, composing simulators preserves exact simulation. All stated approximate-simulation allowances are finite and nonnegative. For approximate simulation, total variation contracts under stochastic transformation, so

\[
\operatorname{TV}(T_2T_1P,R)
\le\operatorname{TV}(T_1P,Q)+\operatorname{TV}(T_2Q,R).
\tag{31}
\]

Taking the corresponding uniform bounds provides an additive directed-simulation error. Contraction follows by expanding the finite sums and using nonnegative transition weights whose rows sum to one. This is an elementary specialization of the simulation view in P §8.

A sequence of online simulators remains online only when each uses currently available information. A final-string simulator that looks into the future fails this composition requirement even if its distributional identity is exact.

### 10.7 Joining evidence requires a contextual guarantee

Preservation of \(P(\theta\mid X)\) does not license replacing \(X\) after a new correlated \(Z\) arrives. The joined operation needs (23), its decision-relative counterpart, or another theorem covering the actual joint context. Universal-context reuse needs the stronger conditions in §7.

The two inputs must refer to the same underlying source events where evidence overlaps. Source identifiers can help find that overlap, but the posterior fusion rule additionally needs actual shared-information and residual-independence conditions. No compositional law permits “more citations” to become independent probability factors. [E §§3.2, 3.4–3.7]

### 10.8 Preserve temporal model identity

An episode-level model or dependence assumption cannot change halfway through a derivation without an explicit model transition. Different local conclusions supported by different models may not be spliced into one trajectory as though one model supported them all.

Rectangular uncertainty may be an intentional alternative model, with its own guarantee. It is not a default joining rule for fixed-model ambiguity. The same restriction applies to assembling coordinate-wise bounds: extrema attained under different models need not form one attainable joint vector. Sound enclosing intervals may still be reported, labeled as enclosures. [E §5; P §§5.2, 9.3]

### 10.9 Keep conditioning separate from restriction and approximation

For model-set Bayesian conditioning on \(e\), the eligible conditional laws are

\[
\mathcal U\mid e
=\{P_F(\cdot\mid e):F\in\mathcal U,\ P_F(e)>0\},
\tag{32}
\]

under that explicitly chosen updating semantics, with \(\mathcal U\) the exact stated set. Starting instead from a sound \(\mathcal U^+\) gives a sound enclosure of these defined conditional laws, not necessarily the exact updated fiber. A positive-probability event in an outer member does not prove that it is possible in an original member. Conditional expressions with zero mass remain `NA` and are not evaluated. A distribution over models additionally requires posterior reweighting by likelihood; a bare set supplies no such weights.

The original value/regret certificate remains an ex ante statement unless it explicitly covers conditional histories. Replanning after an observed history requires a valid updated information state and an applicable continuation certificate. Continuing to execute a previously certified whole policy is not the same operation as replacing it with a newly optimized conditional policy. [P §§6.4, 6.7, 9.3; E §3.3]

### 10.10 Compose statistical coverage separately from mathematical error

If result \(i\) has a deterministic guarantee on an event \(E_i\), and valid coverage satisfies \(P(E_i)\ge1-\alpha_i\), then for a fixed finite set of such events on the same sampling space, with \(0\le\alpha_i\le1\),

\[
P\left(\bigcap_iE_i\right)\ge1-\sum_i\alpha_i.
\tag{33}
\]

This is the union bound; it requires no independence. On that joint event, the deterministic error guarantees may be composed using their own applicable rules. Multiplying coverage probabilities requires further independence conditions. Repeated adaptive use must have coverage valid for that use, not a repeatedly reused fixed-sample assertion.

Thus \(\varepsilon\) or \(\rho\) measures error in the promised answer or policy, while \(\alpha\) measures failure of a separately justified coverage event. Neither is a generic confidence score for the entire decision. [P §9.2; elementary probability consequence]

### 10.11 Carry dependencies through every composition

Every composite result inherits the premises actually used by each step, including model identity, source dependence, loss scale, decoder, and theorem scope. Record any further assumptions introduced at the join. A successful computation cannot erase an unresolved modeling premise.

This is the proposed provenance rule derived from the North Star's seven obligations. It is bookkeeping for conditional mathematics, not a new belief-revision theorem. [N; P §9; E §7]

---

## 11. Provenance, revision, and correction

### 11.1 Keep different dependency structures separate

Use a derivation-dependency relation to record which premises and earlier results support a conclusion. Separately preserve the statistical dependence structure of evidence and, where applicable, the causal mechanism structure.

An arrow meaning “this result used that source” does not mean “these random variables are conditionally independent.” An arrow meaning “this variable causes that variable” is different again. Conflating the three makes composition unsound even if every source is traceable. This distinction is a proposed organizing convention implementing the separate mathematical structures in §§3, 7, and 9.

### 11.2 Minimum provenance attached to a result

Record the exact statement and scope; model and data versions; formal assumptions and their warrants; query and loss units; theorem or derivation; decoder/policy identity when relevant; numerical and statistical error components; dependencies; and the result's validation status.

Distinguish **assumed**, **supported empirically**, **derived analytically**, **computed exactly on a specified instance/domain**, and **numerically bounded**. Record published versus manuscript sources as described in the supplied audits. An exact computation is not an independent experiment; a theorem citation is not evidence that an application's assumptions hold. [K §§1, 8–9; P §9; E §1]

These are provenance distinctions, not a mandatory database schema. A content hash identifies bytes. It does not prove mathematical truth, semantic equivalence, or that two evidence items are independent.

### 11.3 Correction is scoped reassessment, not automatic erasure

When an input changes, identify the results whose derivations used it. Their **reuse status** must be reassessed. An old theorem of the form \(\mathcal A\Rightarrow\Gamma\) may remain correct even when new evidence defeats an application of \(\mathcal A\). Conversely, a proof or arithmetic error may require correcting the mathematical result itself.

The proposed correction rule is:

> Preserve the historical statement and its old premises; identify the changed dependency; suspend unsupported current reuse; then restore, narrow, or replace the guarantee only with a valid justification.

Reassessment does not imply that the old numerical answer is necessarily false. It means its previous warrant no longer automatically establishes the new claim. Results not depending on the changed item are not invalidated by association. Model revisions, preference revisions, and newly available evidence are different changes and may trigger different mathematics. [N; P §§9.2–9.4; proposed synthesis convention]

An empirical outcome can become new evidence under an observation model. One favorable outcome does not prove the decision rule optimal, and an unfavorable outcome does not alone refute an expected-loss guarantee. The guarantee concerns its stated probabilistic or worst-case target, not every realized outcome.

### 11.4 Historical stopping decisions remain part of provenance

Corrections do not convert post-hoc evidence into preregistered evidence or revive a closed experiment. KL5, KL6, and the two frontier-audit dispositions remain recorded with their original scopes. This substrate adopts their mathematical consequences without substituting a new success criterion. [K §§1, 8; P §11; E §7]

---

## 12. Failure conditions and the answer permitted by each

The following distinctions are proposed reporting semantics. They should not collapse into one generic “low confidence” label.

| Condition | What may honestly be concluded |
|---|---|
| Undefined variables, missing loss/criterion, or unspecified information access | The decision query is not yet fully defined. No unique optimal answer follows. |
| Empty exact compatible set, or a proved-empty sound outer joint enclosure | The original retained constraints are inconsistent within the declared class, conditional on the enclosure premises where used. Do not certify an action by vacuous truth. |
| Nonempty outer enclosure without an exact witness or existence proof | Only the relaxation is feasible; original-model compatibility and real-world membership remain unestablished. |
| Conditioning event impossible in all compatible models | The update is undefined within that class; the evidence or model assumptions require reassessment. |
| Event possible in only some models | Conditional answers require the declared model-update semantics; not every old model contributes a conditional posterior. |
| Multiple answers attained in the exact compatible set | The query is not identified from retained information. Variation seen only in an outer enclosure need not be attainable in the original set. Report labeled bounds; do not silently select a model. |
| No common optimal policy, but a declared robust criterion exists | A robust or minimax-regret compromise may be computed under that criterion. It is not optimal in every model merely because it is robust. |
| Certified interval crosses a decision boundary | No strict decision is certified by that interval, including all applicable model and computed-value errors. This is not proof of an exact tie. |
| Exact equality of competing costs | A mathematical tie: preserve all minimizers. Any selected tie-break is an additional rule. |
| Guarantee valid but error bound exceeds useful tolerance | The certificate is too weak for that use, not necessarily mathematically false. |
| Missing dependence or joint extension | Fusion or combined reuse is not justified; retain the compatible-law uncertainty or block the join. |
| Changed query, context, cost, horizon, policy access, or regime | The old guarantee is outside its established scope unless a transport/composition argument applies. |
| Unsupported posterior, unavailable decoder/lift, off-support policy gap, or causal intervention conversion | A required operation has no established warrant. A legal predeclared response is distinct from an undefined posterior; an unmodeled crash/refusal is not a certified policy. |
| Verification disagreement, arithmetic error, or proof gap | The affected result is unverified or erroneous; this is not evidence for a negative mathematical proposition. |
| Full model reconstructed by the representation | Valid model retention may remain; the claim of genuine compression is not established. |
| Source/model revision affects a premise | Suspend unsupported current reuse and reassess the dependent result; retain its historical conditional statement. |

The underlying distinctions come from support-sensitive conditioning, query identification, minimizing-set semantics, representation guarantees, and the inherited integrity rules. [K §§2, 8; P §§2, 5–6, 9; E §§3–5]

No expected-value or regret guarantee alone establishes a bound on every possible harm, a tail probability, legal authorization, or the legitimacy of a loss function. Such claims require their own query and premises. They are not added by the word “consequential.”

---

## 13. The first coherent reusable record

A concrete mathematical record can be small while still exposing its obligations. The following is a **symbolic instantiation of already-adopted guarantees**, not a new example search or proposed summary.

| Obligation | Bounded sequential-policy certificate |
|---|---|
| Object | A retained surrogate observation model and an implementable stopping policy. |
| Assumptions | Finite nonempty state/action/observation alphabets; static state; common known prior; common losses \(0\le L\le L_{\max}<\infty\); finite fee \(c\ge0\); stationary conditionally independent observations; integer \(H\ge0\), \(0\le h\le H\); justified actual-model membership in the exact fiber, with any sound outer enclosure separately labeled. |
| Retained information | Surrogate \(\widehat K\), context \(B\), finite uniform channel allowance \(d\ge0\), and a policy/update/lift executable on every covered history, including a predeclared legal response where surrogate conditioning is undefined. The original model is not an undisclosed decoder input. |
| Operation | Evaluate the surrogate policy/optimum and apply the uniform policy-transfer bound. |
| Guarantee | For each covered integer \(0\le h\le H\), value error at most \(e_h\) and whole-policy regret at most \(2e_h+\eta_h\) for justified finite \(\eta_h\ge0\). Only for \(h\ge1\), use (19) for exact optima, or (19b) with finite \(\xi_{R,h},\xi_{O,h}\ge0\) for computed values. At zero horizon STOP is forced. Statistical coverage is separate. |
| Composition | Reuse only with matched context and policy access; accumulate compatible approximation errors; require a new dependence/conditioning argument after adding evidence not already covered. |
| Failure | Unmet profile domain or stationarity/independence; changed loss/prior/cost; hidden model-specific decoding; off-support execution gap; unsupported conditional reuse; unproved numerical error or vacuous comparison interval. |
| Provenance | Source of compatible-model membership, the coupling proof, surrogate and policy versions, planning/numerical error, and every reused input certificate. |

Equations (14)–(19b), under their explicit domains, supply the mathematics. The record merely makes its obligations available for inspection. Every posterior-dependent sum omits zero-mass branches; no operation on `NA` is implied.

For evidence fusion, substitute a joint-law/factor object and equations (2)–(5). For causal decisions, substitute the intervention-indexed object and equation (27). Do not keep the same guarantee while changing the mathematical object underneath it.

### What makes the collection cumulative

The supported flow is:

```text
specified evidence and modeling assumptions
    -> compatible joint model or model set
    -> justified conditioning and available information
    -> explicit decision query and admissible policies
    -> exact evaluation or a certified abstraction/approximation
    -> result with its guarantee and permitted reuse context
    -> further composition only through applicable rules
    -> dependency-aware reassessment when a premise changes
```

Not every record must traverse every step. A theorem can be retained before any empirical instantiation. A source record can remain outside a numerical model until its interpretation is justified. A decision result can be stored without pretending that the actual decision-maker adopted it. These are different kinds of consequential decision knowledge.

---

## 14. Boundary with Writ engineering and with the larger programme

Bellman supplies the meanings and conditional guarantees in this document. Writ's role, as specified in the North Star, is to make those meanings executable, checkable, versioned, and reusable without silently changing them. This document imposes mathematical obligations, not a choice of repository structure, programming language, data store, or user interface. No current repository implementation was inspected or certified. [N]

A successful encoding must preserve what its operation actually requires: variable identities, joint-model constraints, information timing, losses, admissible policies, guarantee scope, complete minimizing sets when requested, and proof dependencies. Distinguish arithmetic correctness, formal premise applicability, and empirical model adequacy. A profile-specific checker can verify its declared input rules and arithmetic without deciding arbitrary theorem premises or real-world truth. No general solver or automated theorem prover is required or asserted to exist. [REV §5; B1 §§2–6]

### 14.1 Readiness correspondence—not an added gate

| Kind of statement | What is explicit here | What an implementation may claim |
|---|---|---|
| Finite mathematical rules | Positive-support conditioning (2), finite sums (3)–(4) under their premises, Bellman rules (7)–(9), set/range rules (10)–(12), (25), (28), and elementary error rules (15)–(19b), (29)–(33). | Each can be evaluated for an explicitly supplied finite instance when its inputs and premises are available. This does not assert an algorithm for obtaining an arbitrary fiber, error certificate, or joint model. Build 1 instantiates only the subset in §14.2. |
| General theorem applications | Exact abstraction/value equivalence, approximate information states, information-comparison results, robust decomposition, and causal transformations. | Require the actual maps, model class, action/policy coverage, dependence/timing, and other theorem-specific premises. A citation or a recurrence alone is not an executable instance or a checked theorem application. |
| Proposed conventions | Result/dependency records, correction and reuse-status rules, and reporting distinctions in §§2, 10.11–12. | Working conventions for recording conditional mathematics, not new theorems, implemented graph infrastructure, or guarantees that a workflow exists. |

### 14.2 Existing `finite-one-observation.v1` only

The supplied Build 1 packet is used solely for this correspondence. Its mathematical instance has a supplied finite known prior and channel, finite **signed rational** terminal losses, the same nonempty action menu after every observation, and one optional observation with a fixed finite rational fee \(c\ge0\) in the declared loss unit. Its existing label, dimension, rational-spelling, byte, and resource limits remain unchanged. No repeated-observation, robust, causal, fusion, approximation, or off-support transferred-policy functionality is added. [B1 §§3–5]

| Existing profile field or operation | Mathematical correspondence |
|---|---|
| `model.json`: `states`, `outcomes`, `prior`, `likelihood` | Variable orders, initial \(b\), and state-row/outcome-column \(K\) in (7). `query.state_order` must match. |
| `query.json`: `actions`, `losses`, `loss_unit`, `cost` | The permitted \(a\), finite signed \(L\), exact unit label, and supplied \(c\ge0\) in (8) at \(h=1\). Unit identity is not empirical preference validation or unit conversion. |
| `prior_risks`, `current_risk`, `current_argmin` | \(\sum_\theta b(\theta)L(a,\theta)\), \(R\), and every terminal minimizer. |
| `branches`: mass and conditional fields | \(m_x\), \(b_x\), action risks, minimum, and all minimizers when \(m_x>0\). At zero mass all four conditional fields are JSON `null`, corresponding to mathematical `NA`; they are not empty sets or ties. |
| `observed_risk`, `evsi`, `net_value` | \(R_1=\sum_{x:m_x>0}m_xR(b_x)\), \(v=R-R_1\), and \(v-c\), respectively. `observed_risk` excludes cost and is not generally \(V^1\). |
| `acquisition_risks`, `acquisition_argmin` | `act_now` has risk \(R\); `observe_once` has risk \(O^1=R_1+c\). Keep every minimizer; \(V^1\) is their minimum, not an additional claimed output field. These names do not assert an arbitrary sequential stopping theorem. |
| Separate checker and `check_and_load` | Direct joint-mass identities and the existing finite \(X\to A\) policy check establish the one-observation arithmetic. Fresh whole-answer checking binds the result to the consumer's independently supplied intended original input bytes. Hash agreement alone is insufficient. |

The exact joint-mass rule is \(J[x,a]=\sum_\theta b(\theta)K(x\mid\theta)L(a,\theta)\); for \(m_x>0\), dividing by \(m_x\) gives the conditional risk. Minimizing over all deterministic functions \(X\to A\) gives the same \(R_1\), because the chosen action at one outcome imposes no constraint on another. A randomized terminal rule cannot improve this known-model linear optimum; this is not a restriction on every robust policy class. Arbitrary actions on impossible branches in that reference calculation make zero joint contribution, not conditional-optimality claims. [B1 §§3, 6]

Build 1 checks exact supplied inputs and answers. It does **not** validate real-world source reliability, empirical model truth, cross-question sufficiency, causal assumptions, all seven components, or a general formal proof. In particular, valid signed-loss inputs do not automatically satisfy §6's coupling premises. `check_and_load` need not verify every theorem discussed in this document. Existing `input_mismatch`, `computation_mismatch`, and `out_of_scope` behavior is retained; no approximate fallback is introduced. [B1 §§5, 8]

### 14.3 Fixed handoff and checks actually rerun

The existing F01 fixture has \(p=P(s1)=1/4\), \(k=(0,1/2)\), \(L=[[0,1],[1,0]]\), and \(c=0\). It gives \(R=1/4\), masses \((7/8,1/8)\), state-1 posteriors \((1/7,1)\), branch minimizers \(\{a0\},\{a1\}\), \(R_1=1/8\), EVSI \(1/8\), and unique acquisition minimizer `observe_once`. Permitted reuse is fresh checking of the whole answer against the same intended original bytes. [B1 §§4–5, 7]

The existing F10 change sets \(c=1/8\): \(O^1=R=1/4\), net value zero, and **both** acquisition alternatives minimize. The F01 result must not be consumed under those changed question bytes: the required status is `input_mismatch`, while fresh checking under F01's original bytes remains legitimate. Forging a matching header does not validate the old net value or acquisition set; the required arithmetic check detects those discrepancies. F02's channel change raises EVSI to \(1/4\); F03→F05 changes the current minimizer from `a0` to `a1`; F12's action restriction makes EVSI zero. These are existing Build 1 definitions, not new parameter cases. [B1 §§7–9]

For this amendment, a small local exact-`Fraction` harness was written and run under **CPython 3.13.5**. It is not the review's `fixed_checks.py`, Build 1 production code, a consumer integration test, or independent formal verification. The two calculation paths share their author, literal inputs, and rational library. Recorded coverage:

| Rerun | Result and scope |
|---|---|
| Existing F01–F12 | All 12 agree between normalized posterior calculation and separately written joint-mass calculation, including all returned mathematical fields and minimizing sets. The latter also evaluated the existing **68** deterministic one-observation reference policies. Required zero-mass `null` fields, F07 terminal ties, F10 acquisition tie, and F09 exact risk gap \(1/1000000000000000001\) were checked. |
| C01: exact/outer rational sets | The §10.2 exact intersection is empty and the outer intersection is \(\{1/2\}\). For the same exact set \(\{1/4\}\), query \(Q(p)=p\) has minimum scalar error zero; its outer set \(\{1/4,1/2\}\) has half-range \(1/8\). |
| C02–C05: approximation premise checks | Recomputed the signed-loss values \(-99,-98\), the invalid negative-fee expression \(-1/10\), surrogate-impossible event mass \(1/200\), and the computed-margin interval \([-1/1000,3/1000]\). They confirm why the clarified premises are necessary, not that production software enforces them. |
| C06–C09: existing safeguards | Rechecked review fusion quantities \(24/25\) versus \(72/73\), residual-dependence quantities \(6/7\) versus \(12/13\), fixed-model versus resampled two-ones probabilities \(1/2\) versus \(1/4\), private-randomization worst loss \(1/2\) versus deterministic loss 1, and the distinction between equal minima, common minimizers, and equal minimizing sets. |
| C10: handoff primitives only | For literal Build 1 input specimens, checked that changing cost or whitespace changes the input digest; an unchanged input digest does not validate tampered EVSI. These scalar/byte checks are not tests of the actual `check_and_load` API or production refusal paths. |

All 12 fixture comparisons and **ten named targeted check groups** passed. No model grid, closed KL search, new experiment, or production implementation was run. The review's companion harness/results were not retrieved as executable source; its reported 20 test methods, 38 horizon-two policies, and historical two-model checks are **not** claimed as rerun. No external publication proof was independently re-audited. Build 1's full parser, mutation, process, consumer, resource-limit, and comparison acceptance tests remain the responsibility of that unchanged build. The statuses in the handoff paragraph are specified behavior, not production results observed here.

The existing Build 1 may proceed in parallel without waiting for this document or satisfying the other components. No Build 2, new execution profile, or follow-on experiment is selected.


The first substrate does **not** yet supply a unified treatment of strategic equilibrium, multiple decision-makers with incompatible objectives, institutional authority, contested natural-language interpretation, endogenous incentives to report, or automatic causal discovery. Nor does it establish the smallest representation or inexpensive verification for every problem. These are boundaries of the present specification, not a new research agenda or authorization for another experiment.

**The foundation earned is narrower and usable:** probability and joint evidence; admissible sequential decisions; exact task-relative preservation; bounded-error policy transfer; dependence-aware information reuse; explicit uncertainty semantics; and a separate intervention interface, all carried by conditional, source-traceable guarantees.

This is the first assembly of the accumulated foundations. It is not a claim that mathematical knowledge alone determines which consequential decisions ought to be made.

---

## Source inventory and attribution

### Supplied sources used for this synthesis

The four source records below are retained from v1; their mounted byte digests were rechecked for this amendment and match. The suffixes are upload filenames, not new mathematical versions. Their literature attributions are retained, not represented as a fresh full-text literature or proof audit.

**[V1] Source substrate.** `BELLMAN_WRIT_MATHEMATICAL_SUBSTRATE_V1.md`, read in full. SHA-256 before and after amendment:

`af60646d0118dce72abc65d7440a4faf9e8ed305ca6ffefc00775cc84204bc22`

Those bytes were not edited. The review refers to an upload named `BELLMAN_WRIT_MATHEMATICAL_SUBSTRATE_V1(1).md` with this same digest. This v1.1 is a separate complete file, retaining v1's section and main equation numbering; new subsidiary labels do not renumber the originals.

**[REV] Adversarial review.** `BELLMAN_SUBSTRATE_V1_REVIEW(1).md`, read in full. SHA-256:

`b8b221715462e05dda5d8ac4a6aa6990e34909dc64bf0e60f181e775067ac309`

Findings 1–5, confirmed edge cases in §4, and engineering correspondence in §§5–6 are assessed in the change log and amended at their points of use. Its report of a 20-method harness is source-reported, not adopted as this amendment's execution record.

**[SUM] Accompanying summary.** `Pasted markdown(20260907-012508).md`, read in full from its saved text. Its approximation summary's omitted lower loss bound is corrected by this document's executive summary and §§6, 13. The old summary is not rewritten or represented as already corrected.

**[B1] Existing engineering boundary.** `RUN_THIS_NEXT_WRIT_ENGINEERING_BUILD_1(1).md`, “Exact decision-query computation, checking, and consumption,” prepared 6 September 2026, read in full from its saved text. Only §§3–9 and the existing F01–F12 definitions inform the correspondence and fixed checks; the packet's implementation instructions are not executed here. No Build 1 scope or acceptance rule is changed.

SUM and B1 were read as retrieved text; no original-byte digest was established for them, and no reconstructed-text digest is substituted. They are identified by filename, title/date where given, and sections. The review companion files `fixed_checks.py`, `fixed_check_results.json`, `fixed_check_log.txt`, and `source_manifest.json` were not rerun. The only new execution record is the bounded one in §14.3.

**[N] Bellman North Star.** Supplied filename:

`BELLMAN_NORTH_STAR(1).md`

SHA-256:

`e2f1f7180fdf05dcd5a1f899b0e2acaf5a64d2e2a0a64c0a6e6679239f8f6b46`

Role: programme, seven component obligations, and mathematical/engineering relationship.

**[K] Kahneman Lab Experiment 6 — V2: Adversarial mathematical audit and terminal theory-closure protocol.** Supplied filename:

`RUN_THIS_NEXT_KAHNEMAN_LAB_6_OBSERVATION_MODEL_SUFFICIENCY_V2(1)(1)(1).md`

SHA-256:

`31a4fb8bfcfbb7e9c4753866628c7784bf769d560d6716e21e878d22bf3d47f2`

Role: binding closure, exact stopping semantics, scoped reconstruction, coupling proof, and research-provenance distinctions.

**[P] Kahneman Lab — Post-KL6 Mathematical Frontier Audit.** Supplied filename:

`KAHNEMAN_LAB_POST_KL6_MATHEMATICAL_FRONTIER_AUDIT(1)(1)(1).md`

SHA-256:

`6a01ca1e81da1d6ea1bc5899f20ebe8380c997693b17fff006719d6f357669bd`

Role: exact/approximate representation foundations, policy/value distinctions, model fibers, error/regret/margin specialization, and ambiguity boundaries.

**[E] Kahneman Lab — Next Mathematical Axis Audit.** Supplied filename:

`KAHNEMAN_LAB_NEXT_MATHEMATICAL_AXIS_AUDIT(1)(1)(1).md`

SHA-256:

`b044e4b38df0d385d8a32af688a62ac0ea794f08f3c709743d7105680eecc010`

Role: joint evidence, common-information fusion, dependence-aware reuse, causal-interface qualifications, uncertainty geometry, and the foundation-only outcome.

### Principal established foundations, as attributed in those sources

- **Known-model partial observation:** Kaelbling, Littman, and Cassandra (1998), “Planning and Acting in Partially Observable Stochastic Domains.” DOI `10.1016/S0004-3702(98)00023-X`. [P:R1; K:P1]
- **Exact abstraction:** Givan, Dean, and Greig (2003), “Equivalence Notions and Model Minimization in Markov Decision Processes.” DOI `10.1016/S0004-3702(02)00376-4`. Poupart and Boutilier (2002), “Value-Directed Compression of POMDPs.” [P:R2, R18]
- **Value equivalence:** Grimm et al. (2020), “The Value Equivalence Principle for Model-Based Reinforcement Learning,” arXiv `2011.03506`; Grimm et al. (2021), “Proper Value Equivalence,” arXiv `2106.10316`. Their distinct theorem scopes remain as recorded in P. [P:R4–R5]
- **Approximate information states:** Subramanian, Sinha, Seraj, and Mahajan (2022), “Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems,” *JMLR* 23(12): 1–83. [P:R6]
- **Experiment comparison:** Blackwell (1953), “Equivalent Comparisons of Experiments,” DOI `10.1214/aoms/1177729032`; Le Cam (1964), “Sufficiency and Approximate Sufficiency,” DOI `10.1214/aoms/1177700372`; van Rooyen and Williamson (2014), “Le Cam meets LeCun: Deficiency and Generic Feature Learning,” arXiv `1402.4884`. Original-source access and normalization qualifications are retained from P. [P:R8–R9]
- **Factorization and fusion:** Kschischang, Frey, and Loeliger (2001), “Factor Graphs and the Sum-Product Algorithm,” DOI `10.1109/18.910572`; Dagan and Ahmed (2021), “Factor Graphs for Heterogeneous Bayesian Decentralized Data Fusion,” DOI `10.23919/FUSION49465.2021.9626865`. [E:A3–A4]
- **Dependence-aware signal comparison:** Brooks, Frankel, and Kamenica (2024), “Comparisons of Signals,” DOI `10.1257/aer.20230430`; Whitmeyer and Williams, *Strong Dominance for Dynamic Signals*, author manuscript arXiv `2407.16648v2`, 17 May 2026, as reviewed in E. [E:A1–A2]
- **Credal/dependence uncertainty:** Cozman (2000), “Credal Networks,” DOI `10.1016/S0004-3702(00)00029-1`; de Oliveira, Ishii, and Lin, *Robust Aggregation of Correlated Information*, reviewed manuscript arXiv `2106.00088v2`. [E:A5–A6]
- **Robust dynamic semantics:** Iyengar (2005), “Robust Dynamic Programming,” DOI `10.1287/moor.1040.0129`; Epstein and Schneider (2003), “Recursive Multiple-Priors,” read with Wakai's (2007) correction as specified in E. [P:R16; E:C1–C2]
- **Causal transformations:** Rubenstein et al. (2017), “Causal Consistency of Structural Equation Models,” arXiv `1707.00819`; Beckers and Halpern (2019), “Abstracting Causal Models,” DOI `10.1609/aaai.v33i01.33012678`; Beckers, Eberhardt, and Halpern (2020), “Approximate Causal Abstractions,” *PMLR* 115: 606–615. [E:B1–B3]

**Attribution boundary:** the seven-component organization, reporting distinctions, and correction conventions remain proposed synthesis. Equations (9), (19a)–(19b), (28)–(33), and the outer-set implications make elementary conditional consequences explicit; they are not experimental findings or novelty claims. The other theorem-level statements retain their stated scopes. The amendment clarifies applicability rather than refuting the existing bounded-loss, policy-transfer, or factorization theorems. Historical KL5/KL6 proofs and searches were not rerun; only §14.3's fixed conformance checks were performed. No new search space, component, approximate solver, infrastructure, experiment, or expanded Build 1 is introduced.

**Disposition:** retain the amended foundation; preserve every original stopping disposition; continue the existing Build 1 in parallel. This document selects no follow-on experiment or Build 2.
