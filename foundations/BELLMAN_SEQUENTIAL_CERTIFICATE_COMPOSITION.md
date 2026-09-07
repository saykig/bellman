# Bellman: sequential decision-certificate composition

**7 September 2026. Additive mathematical construction and bounded exact reference.**
Source baseline: `b1266137f824dc65e614722f1f0592846b915262` on main, the merge of repaired PR4 head `efba25bc3a52535e331fe21fe364f394029c853c`. Their file trees agree; no intervening mathematical change was found. Earlier editions, proofs, reviews, results, manifests, and archive gaps remain historical records.

This module establishes when local calculation guarantees warrant an entire executable policy, and what new evidence or replanning changes. It gives constructive lower-optimum and upper-policy certificates, checked residual composition, a pathwise telescoping argument, and restricted model-transfer and conditioning rules. Established finite dynamic programming suffices. This is not a new substrate edition, general solver, risk guarantee, or Writ integration.

## 1. Subject, information, and timing

Fix a finite horizon \(H\). A node \(h=(a_0,o_1,\ldots,a_{t-1},o_t)\) is the **observed** history available just before decision \(t\). The root is the empty history. Own past actions are observable; hidden state, an unobserved model label, and future observations are not. Distinct histories are not merged merely because a current posterior or value happens to agree.

At a decision node a nonempty finite menu \(A(h)\) is supplied. A STOP action pays its signed cost \(c(h,a)\) and ends the episode. A continuing action pays signed cost \(c(h,a)\), then emits \(o\) with the supplied rational law \(p(o\mid h,a)\); its child is \(hao\). Every row is nonnegative and sums to one. At a terminal node, including every node at depth \(H\), pay \(g(h)\) once and terminate. The reference prohibits simultaneous nonzero terminal costs and a decision menu to avoid double counting. There are no decisions after stopping and no acquisition decision at zero remaining horizon.

All costs use the same declared loss unit, are finite, and may be negative. A finite tree makes every total cost bounded. Already-paid costs are absent from continuation costs. This criterion is **expected additive total cost**, not a tail, pathwise harm, robust, or legitimacy criterion.

A deterministic policy \(\pi\) is one total table \(h\mapsto a\in A(h)\). The reference requires a legal response on every structurally supplied decision history, including zero-probability children. This is stronger than checking only the policy's on-support nodes and supports subsequent model comparisons on a common union of histories. No private randomization is used or needed for the present claims. Finitely many such total tables exist; conditional on the supplied known model they define a unique path law. A finite menu has an attaining deterministic optimum by backward induction.

**Support distinction.** A zero-probability child may have a supplied hypothetical completion law/cost and a legal fallback action. These numbers do not become a posterior under the original model. Only positive-mass histories have conditional expectations under its actual root law. Counterfactual completed-node values may be checked algebraically but must not be reported as an original zero-mass conditional answer. A transferred policy must cover histories possible under either model and its actual loss on them must be counted.

The subject contains its name, horizon, unit, premise labels, ordered histories, full action menus, every cost, and every observation probability. It is not an unspecified MDP identified by a root value. The recipient independently supplies its intended subject and executable policy when consuming a certificate. A changed horizon remains a different subject even if early stopping makes numerical values unchanged.

### Deriving node quantities from a hidden law

In a static hidden-state observation model with known prior \(b_0(\theta)\), at a positive-probability observed history \(h\),
\[
 \Lambda_h(\theta)=\prod_{k=0}^{t-1}K_{h_k}(o_{k+1}\mid\theta,a_k),
 \qquad b_h(\theta)=\frac{b_0(\theta)\Lambda_h(\theta)}
 {\sum_{\vartheta}b_0(\vartheta)\Lambda_h(\vartheta)}.
\tag{S1}
\]
Here the past actions are those of the same legal deterministic history rule, and the likelihood is a chronological product of the controlled conditional kernels. This chain rule does not assume independent observations. It is not the observational likelihood obtained by conditioning on the event that an adaptive policy selected the whole action sequence; that selection can itself reveal observations and change normalization. The conditional observation kernel is \(K_h(o\mid\theta,a)\), so
\[
 p(o\mid h,a)=\sum_\theta b_h(\theta)K_h(o\mid\theta,a),
 \quad
 b_{hao}(\theta)=\frac{b_h(\theta)K_h(o\mid\theta,a)}
 {p(o\mid h,a)}
\tag{S2}
\]
only at positive denominator. A terminal decision has conditional cost
\(c(h,a)=\sum_\theta b_h(\theta)L_h(a,\theta)\); an observation can instead have a supplied fee. More general random immediate costs are replaced by their conditional means for this expected additive criterion. The required prediction and cost laws must come from one chronologically consistent **controlled** model. An observational joint law does not, merely by conditioning on selected actions, supply an intervention model.

Conditional independence is not needed for a fully supplied history tree. It is needed to replace history-dependent \(K_h\) by repeated draws from one stationary channel in B13. For a simple failure of posterior-only prediction, let \(\theta\) be an independent fair bit and let reports satisfy \(X_2=X_1\), with \(X_1\) fair. After either first report the posterior over \(\theta\) is still \(1/2\), but \(P(X_2=0\mid X_1=0)=1\) and \(P(X_2=0\mid X_1=1)=0\). The old posterior alone cannot supply the next-observation law.

For a separate adaptive-selection control, let the prior be fair, let the first report satisfy P(X=0|theta=0)=3/4 and P(X=0|theta=1)=1/4, and choose the next action LEFT exactly when X=0. On that history the correct posterior P(theta=1|X=0)=1/4. But P(X=0|theta, selected LEFT)=1 for either theta; multiplying these selected-action conditional probabilities by the original prior would incorrectly return 1/2. The chronological likelihood in (S1) retains 3/4 versus 1/4 and gives the correct 1/4. No future information is supplied to the earlier decision.

The checker validates finite probability arithmetic, coverage, and declared information keys. It does not empirically establish that a supplied label really is observable, that a controlled model is correct, or that a loss unit represents warranted preferences. Those remain substantive premises.

## 2. Whole-policy certificate: two different bounds

Let \(V(h)\) denote the optimal expected remaining cost and \(J^\pi(h)\) that of the supplied policy. Define the action backup on a table \(w\) by
\[
 Q_w(h,a)=
 \begin{cases}
 c(h,a),&a\text{ stops},\\
 c(h,a)+\sum_o p(o\mid h,a)w(hao),&a\text{ continues}.
 \end{cases}
\]
Then \(V(h)=\min_a Q_V(h,a)\), \(J^\pi(h)=Q_{J^\pi}(h,\pi(h))\), with \(V=J^\pi=g\) at terminal nodes.

**Package.** Supply the exact subject, the complete executable policy, and two exact rational node tables \(L,U\). Check:
\[
 L(h)\le g(h)\le U(h) \quad\text{at every terminal node};
\tag{S3}
\]
\[
 L(h)\le Q_L(h,a)\quad\text{for EVERY }a\in A(h),
 \qquad U(h)\ge Q_U(h,\pi(h))
 \quad\text{at every decision node}.
\tag{S4}
\]
The lower table concerns the optimum over the entire declared policy class. The upper table concerns one named executable policy. They need not be tight.

**Theorem and proof.** At terminals (S3) establishes \(L\le V\) and \(J^\pi\le U\). Induct backward. If \(L\le V\) at children, nonnegative probabilities give \(Q_L(h,a)\le Q_V(h,a)\) for each action. By (S4), \(L(h)\le\min_a Q_V(h,a)=V(h)\). If \(J^\pi\le U\) at children, policy evaluation gives \(J^\pi(h)\le Q_U(h,\pi(h))\le U(h)\). STOP has no continuation term. Therefore
\[
 L(\varnothing)\le V(\varnothing)\le J^\pi(\varnothing)
 \le U(\varnothing),\qquad
 0\le J^\pi-V\le U(\varnothing)-L(\varnothing).
\tag{S5}
\]
Checking only the selected action in the first inequality proves nothing about better competitors. A lower bound does not supply a policy; a policy value does not supply an optimum. A matching valid lower and upper bound proves the supplied policy is optimal. A nonzero gap is a bound, not automatically an attained regret.

Coverage is explicit: all terminal conditions, all action rows for the lower proof, and the selected legal action and its continuation for the upper proof. This reference checks the entire completed tree. A weaker checker could restrict upper coverage to policy-reachable nodes, but then transfer or replanning would need a new coverage argument.

The consumer performs finite arithmetic and inequality checking; it does not call the producer. The producer separately computes backward optimal values and a policy evaluation. An independent forward complete-path sum and enumeration of eight small policies cross-check the main example. Producer and consumer share schema and Fraction arithmetic; different code paths do not imply independent authorship or formal proof.

## 3. Residual hardening of B16

Let \(v(h)\) be a supplied approximate value table. Let \(r(h),z(h)\) be nonnegative claimed residual and greediness allowances. The receiver actually checks:
\[
 |v(h)-g(h)|\le r(h),\quad z(h)=0
 \quad\text{at terminals};
\tag{S6}
\]
\[
 |v(h)-\min_a Q_v(h,a)|\le r(h),\qquad
 Q_v(h,\pi(h))-\min_a Q_v(h,a)\le z(h)
\tag{S7}
\]
at decision nodes. The same table, model, actions, and policy must be used on both sides. An allowance field is not evidence that these inequalities hold.

Define two nonnegative error tables. At terminals \(E_V=E_\pi=r\). At decision nodes write \(P_a E=\sum_o p(o\mid h,a)E(hao)\) for continuing actions and zero for STOP:
\[
 E_V(h)=r(h)+\max_a P_a E_V,\qquad
 E_\pi(h)=r(h)+z(h)+P_{\pi(h)}E_\pi.
\tag{S8}
\]
Then
\[
 |v(h)-V(h)|\le E_V(h),\qquad
 |v(h)-J^\pi(h)|\le E_\pi(h).
\tag{S9}
\]

**Proof.** Terminal claims are (S6). The elementary inequalities
\(|Pf-Pg|\le P|f-g|\) and
\(|\min_a u_a-\min_a w_a|\le\max_a|u_a-w_a|\)
bound the optimum backup discrepancy by \(\max_a P_a E_V\). Add the checked residual. For the selected action, (S7) implies
\(-r(h)\le Q_v(h,\pi(h))-v(h)\le r(h)+z(h)\).
Add the expectation of child policy error to obtain the second recursion. These finite inductions prove (S9) without treating approximate values as exact.

Moreover \(L=v-E_V\) and \(U=v+E_\pi\) satisfy (S3)–(S4). For example \(v-r\le\min_a Q_v\) and \(E_V-r\ge P_aE_V\) for every action imply \(v-E_V\le Q_{v-E_V}(h,a)\). Similarly \(v+r+z\ge Q_v(h,\pi(h))\) implies \(v+E_\pi\ge Q_{v+E_\pi}(h,\pi(h))\). Thus the residual routine constructs an ordinary independently checkable package, with regret radius \(E_V(\varnothing)+E_\pi(\varnothing)\).

If \(r(h)\le r_t\) and \(z(h)\le z_t\) uniformly at depth \(t\), then
\[
 E_V(h)\le\sum_{k=t}^H r_k,\quad
 E_\pi(h)\le\sum_{k=t}^H r_k+\sum_{k=t}^{H-1}z_k.
\]
Consequently B16's \(2\sum r_k+\sum z_k\) is valid under these checked premises. Early stopping only shortens propagation. Terminal residuals remain essential, including a zero-horizon problem. Sampled-node residuals or a policy greedy for another backup do not establish this uniform result.

The nonuniform construction (S8) can be sharper: it propagates optimum uncertainty over all actions but policy uncertainty along the actual policy. This is an established finite induction specialized into a receiver-checkable construction, with no novelty claim.

## 4. Root decisions do not substitute for a complete policy

From a valid package, each optimal forced-root-action value obeys
\[
 Q_L(\varnothing,a)\le Q^*(\varnothing,a)\le Q_U(\varnothing,a).
\tag{S10}
\]
For the upper inequality, follow action \(a\), then the supplied total policy; this is one legal member of the forced-action class. The policy need not be optimal there.

A strict root certificate for \(a\) follows if its upper bound is less than **every** competitor's lower bound. A singleton action menu is forced availability, not evidence of a positive comparison gap. If every interval is a singleton, exact minimization preserves all minimizing actions. Overlapping intervals merely leave the sign uncertified. They neither prove a tie nor disprove a unique optimum.

A common optimal root action may require different model-specific optimal continuations. It therefore does not by itself give a common optimal whole policy. The package must name the actual continuation, including off-support behavior. Likewise \(|V_F-V_G|\) alone supplies no loss bound for transferring the optimizer of \(G\): action cost rows \((0,1)\) and \((1,0)\) have the same optimum zero but transferring an optimizer incurs regret one.

For computed action estimates \(\widetilde Q_a\) with individually justified errors \(\epsilon_a\), a sufficient comparison is \(\widetilde Q_a+\epsilon_a<\widetilde Q_b-\epsilon_b\) for every other \(b\). If these errors are composed from model and calculation contributions, each component needs its own applicable proof. An interval crossing zero is not exact equality. At zero remaining horizon a terminal cost has no forced-observation optimum or observation margin.

## 5. Model error and calculation error: the precise join

For two models on one common total history-policy class \(\Pi\), assume
\[
 |J_F(\rho)-J_G(\rho)|\le e_*\quad\forall\rho\in\Pi,
 \qquad |J_F(\pi)-J_G(\pi)|\le e_\pi
\tag{S11}
\]
for the named candidate. If a nominal package proves \(L_G\le V_G\) and \(J_G(\pi)\le U_G\), then
\[
 J_F(\pi)-V_F
 \le (U_G-L_G)+e_\pi+e_*.
\tag{S12}
\]
Indeed the policy inequality gives \(J_F(\pi)\le U_G+e_\pi\). Taking infima in the uniform comparison gives \(V_F\ge V_G-e_*\ge L_G-e_*\). Subtract. The usual \(2e+\eta\) is the special case \(e_\pi=e_*=e\), \(U_G-L_G=\eta\). If \(\eta\) already came from checked residual/evaluation bounds, adding those residuals again double counts calculation error.

If only a lifted/restricted policy class is compared, retain B3's benchmark-coverage premise \(\inf_{\rho\in\Pi_{\mathrm{lift}}}J_F(\rho)\le V_F+\beta\) and add \(\beta\). The same minimization and triangle argument proves the extension. Value closeness or a model-specific inaccessible decoder does not establish (S11) or coverage.

### B13 audited: when a channel bound becomes a trajectory bound

For B13 retain a static hidden state with **common prior**, the same stationary channel repeated conditionally independently under each model, a common total history policy, common signed terminal loss range \([\ell,u]\), common nonnegative per-observation fee \(c\), and at most \(h\) observations. Suppose rowwise channel TV is at most \(d\in[0,1]\).

Couple the hidden state identically. Conditional on it, independently maximally couple each of the \(h\) potential report pairs. Each pair agrees with probability at least \(1-d\); hence no report mismatch has probability at least \((1-d)^h\). If all reports agree, the same deterministic history policy chooses the same actions and stopping time. Total realized costs lie in \([\ell,u+hc]\). Thus
\[
 |J_F(\pi)-J_G(\pi)|
 \le (u-\ell+hc)[1-(1-d)^h]=e_h.
\tag{S13}
\]
Unused reports after stopping may be pre-sampled. Shifting every terminal loss by \(-\ell\) changes neither decisions nor regret. At \(h=0\) the model discrepancy is zero, but no observation comparison exists. Forced-first-observation optima inherit the bound only for \(h\ge1\) by minimizing over the common forced-action subclass. Model-specific terminal losses, differing priors/fees, undefined off-support policies, or dependence not represented by the channel are outside this proof.

**Dependence counterexample.** On two reports, \(P(00)=P(11)=1/2\), while \(Q(01)=Q(10)=1/2\). Both one-date marginals are fair, giving marginal discrepancy zero. The cost \(1\{X_1=X_2\}\) has expectations one and zero. The product bound with \(d=0\) is false if marginal agreement is substituted for its conditional-independence premise. In contrast, independent fair reports versus independent reports with zero-probability parameter \(3/4\) have two-report TV \(5/16\), below \(1-(3/4)^2=7/16\). The failure is the unsupported join, not B13.

For general supplied history trees a conditional mismatch bound at **every common matched history** can replace independence: recursively couple the next law, conditional on agreement so far, with failure at most \(d_t\). Induction gives agreement probability at least \(\prod_t(1-d_t)\). A common realized total-cost range then gives a bound of that range times \(1-\prod_t(1-d_t)\). Unconditional one-date marginals do not give these conditional bounds. If costs differ on agreeing paths, add a separately justified bound for that discrepancy; do not import (S13) unchanged.

B14's value comparison remains valid on accessible full histories with a common completed skeleton, bounded stage-cost discrepancies and row TV discrepancies. Its split into stage error, continuation value error, and TV times continuation span is the same triangle argument as the inherited proof. It is a value comparison; whole-policy transfer still needs (S11), (S12), or a direct checked policy residual. No general partially observed abstraction theorem is imported without a sufficient observable update and benchmark coverage.

## 6. Conditioning is a new scope, not a free rescaling

Let \(P,Q\) be trajectory laws on the same space, and let \(e\) be the **same event** with masses \(a,b>0\). Write \(\Delta=\mathrm{TV}(P,Q)\). C12–C13 survive:
\[
 \mathrm{TV}(P(\cdot\mid e),Q(\cdot\mid e))
 \le \min(1,\Delta/\max(a,b)).
\tag{S14}
\]
Proof: assume \(a\le b\). On the event subset \(A\) where normalized \(Q\) exceeds normalized \(P\), conditional TV is \(\delta=Q(A)/b-P(A)/a\). Therefore
\(b\delta=Q(A)-(b/a)P(A)\le Q(A)-P(A)\le\Delta\).
This proves the stronger bound directly. The overlap derivation in the revised build-out gives the same inequality. With a common conditional loss of span \(D\), the expectation discrepancy is at most \(D\) times the radius. A bound \(\Delta\le\epsilon\) and \(a\ge\kappa\) imply radius at most \(\min(1,\epsilon/\kappa)\); positivity of \(b\) remains required (or follows from \(\epsilon<\kappa\)).

When \(e\) is a decision-generated history, the pre-observation policy must be the same for the two laws or there must be a separate comparison for the different policies. A channel/model discrepancy proved for one common policy cannot be reused after silently changing the action that generates the event. Even with the same prefix, a new continuation needs its own policy/model comparison and support. For a single known model the already-checked nodewise package supplies conditional continuation bounds at positive-mass histories under the unchanged continuation; a root-only expected bound need not do so.

In the fixed rare-event case
\(P=(1/100,0,99/100)\), \(Q=(0,1/100,99/100)\), and \(e=\{1,2\}\),
joint TV is \(1/100\) while conditional TV is one. Similarly a bounded nonnegative loss \(1_e\) has expectation \(1/100\) but conditional expectation one. A small unconditional *expected* error therefore need not be small after an event. A bound only on a signed mean is weaker still: cancellations can mask large conditional discrepancies.

If \(Q(e)=0\), its conditional quantity remains undefined. A legal fallback action may make an ex ante transferred policy total and bounded, but it does not define \(Q(\cdot\mid e)\). In a family, discard zero-likelihood members only under an explicitly declared conditioning rule; a list of models supplies no Bayesian weights.

## 7. Replanning and B17: one comparator, actual occupancy

For a legal executed policy \(\pi\) in a fixed subject, define at decision histories
\[
 d(h)=Q_V(h,\pi(h))-V(h)\ge0,
\tag{S15}
\]
where \(V\) is the same exact optimal continuation table throughout. The checker verifies its terminal equality and every Bellman minimum rather than trusting an “optimum” field.

Sum (S15) along a trajectory until termination. For continuing actions replace conditional next \(V\) by the actual next \(V\) inside expectation using the tower property; intermediate values cancel. At a terminal \(V=g\), while STOP already includes its last cost and has zero continuation. This proves
\[
 J^\pi(\varnothing)-V(\varnothing)
 =\mathbb E_\pi\!\sum_{\text{visited decision }h}d(h).
\tag{S16}
\]
The law in this expectation is the actual law induced by the actually executed policy. If \(d(h)\le\beta_t\) at every covered depth-\(t\) history, regret is at most \(\sum_t\beta_t\). Node-dependent allowances can be weighted by actual occupancy. It is not generally correct to add conditional regrets without their visit probabilities.

If a replanner supplies a different action at each observed history, its realized deterministic history rule is a new policy. Apply (S16) to that rule and the same comparator; checking each actually available choice against \(V\) permits composition. Zero regret under unrelated local models or horizons is not such a disadvantage. With an arbitrary table \(w\), telescoping instead includes terminal correction \(g-w\), and its local differences need not be nonnegative or correspond to optimal regret. Checking \(w=V\), or separately bounding its residuals, is essential.

A single continuation replacement below positive history \(h\), with unchanged prefix and no other policy changes, obeys the further identity
\[
 J^{\pi'}-J^\pi
 =P_{\mathrm{common\ prefix}}(h)
   [J^{\pi'}(h)-J^\pi(h)].
\tag{S17}
\]
Partition trajectories into those reaching \(h\) and those not; the latter costs and all prefix costs agree, proving the identity. This identity explains both conditional importance and ex ante weighting. Multiple replacements require the actual final policy law, as in (S16), rather than a sum of unrelated predecessor certificates.

Changing the model, permitted information, losses, or horizon leaves the old conditional theorem historically true, but does not establish the new executed-policy claim. Recheck the affected subject and local inequalities. Ordinary observation within the unchanged tree needs no new empirical model merely to evaluate its positive-support node; replacing the model after learning is a separate operation.

## 8. Persistent model identity and common access

For a supplied finite family \(F_i\), evaluate one recipient-available total policy \(\pi\) under each member throughout the trajectory. Valid modelwise packages give
\(J_{F_i}(\pi)-V_{F_i}\le\gamma_i\).
These are modelwise regret bounds. They do not prove minimax optimality of \(\pi\), provide weights over \(i\), or allow an oracle to choose a different continuation from the hidden model label.

The inherited example is decisive: model A has two-date costs \((0,1)\), model B has \((1,0)\), with no informative observation or choice. Fixed-model total cost is one in either. Independently selecting the worst row at each date gives two and enlarges the trajectory family. That is a different adversarial model, not a computation of the old one.

For the access control, cost rows \((0,1)\) and \((1,0)\) permit zero model-specific optimal loss, but no common deterministic action has zero in both. The executable check enumerates the two *same* available policies and obtains modelwise vectors \((0,1),(1,0)\); an extra model-keyed history is rejected. A common mandatory root “continue” would not resolve this inaccessible continuation choice. No robust-planning or randomization solver is added.

## 9. Fixed worked certificate and failure controls

The main tree has \(H=2\). At root STOP costs \(3/4\). GO costs \(1/8\) and reveals L or R, each with probability \(1/2\). At L, action costs are \(a:0,b:1/2\); at R they are \(a:1,b:1/4\). These continuation actions stop.

Optimal values in node order (root,L,R) are \((1/4,0,1/4)\). The policy GO, then b at L and a at R, has costs \((7/8,1/2,1)\). These lower/upper tables satisfy every local inequality, yielding exact regret \(5/8\). Independent path sums are
\[
 \tfrac12(1/8+1/2)+\tfrac12(1/8+1)=7/8.
\]
Enumeration of all eight legal total policies gives optimum \(1/4\). The root GO action is optimal with the optimal continuation, yet this candidate policy costs more than STOP. Its bound interval for forced GO is \([1/4,7/8]\), which overlaps exact STOP \(3/4\): the package alone certifies no strict root sign. This is intentional.

Using the exact optimal value table with residuals zero and greediness allowances \((0,1/2,3/4)\) constructs the same \(5/8\) regret radius. Zero greediness allowances for that bad policy are rejected. Changing only the root approximate value to \(3/8\) requires root residual \(1/8\); understating it as zero is rejected. A separate approximate-greedy policy STOP, with values \((3/4,1,1)\) and residuals \((0,1,3/4)\), has actual regret \(1/2\) and valid certificate radius \(7/8\). Terminal residuals are exercised separately.

For off-support completion change nominal GO probabilities to \((1,0)\), actual to \((99/100,1/100)\), and use a at both children. Its nominal cost is \(1/8\), actual cost \(27/200\), actual regret \(3/400\); loss on the rare fallback branch contributes \(1/100\). A policy omitting R is rejected even nominally. Its nominal posterior at R remains undefined. Enumeration over the common eight policies computes uniform model error \(e=1/100\), nominal gap zero, and valid transfer radius \(1/50\); this radius is conservative, not attained regret.

Each rejection has an accepted control: checked versus understated residual; matched versus wrong backup policy; current versus stale costs/horizon; complete versus inaccessible continuation; new versus predecessor policy; positive versus zero event support; legal fallback versus missing branch; exact rational versus float/Boolean proof inputs; immutable snapshots versus intentional new subjects. Exact tied costs \((-1,-1)\) retain both minimizers; an overlapping interval remains uncertified; zero horizon returns terminal status. Large derived Fraction tables beyond 500 bits remain valid when inequalities hold.

## 10. Constructibility, execution, and limits

The reference profile has horizon at most four, at most 64 nodes, at most four actions per node and four observations per action. Input costs/probabilities accept exact integers or Fraction values with a 256-bit coefficient cap; bool and float values are rejected. Proof tables accept only exact Fractions and have no inherited input-coefficient cap. Nested history, row, action, node, premise, policy, and certificate containers are detached into immutable values; labels/premises are strings. Ordinary deliberate revisions produce new subjects. This is not protection against malicious interpreter memory manipulation.

Backward construction and consumption use finite loops and exact sums. Full policy enumeration, used only as a tiny independent check, is capped at 4096 policies; exceeding this is unfinished enumeration, not infeasibility. All comparison routines validate the intended subject before returning, including terminal and single-action cases. The algebraic helper is internal. The checker never calls the candidate-producing optimizer.

The analytical proofs are (S3)–(S17), with the premises stated above. Fixed tests support specified finite arithmetic and failure paths; they do not establish universal implementation correctness, formal theorem verification, independence of authorship, or empirical model validity. The source/check functions share Python Fraction arithmetic and schema. The forward path evaluator avoids the backup function; whole policy enumeration is a separate finite calculation. No hidden solver, sampling experiment, downloaded toolchain, or recovery ZIP is needed.

See [reference and commands](../verification/sequential_certificates/README.md) and its compact result record for the actually executed runtime, normal/optimized comparisons, current PR4 preservation checks, and exact source identities. Execution is on GitHub-hosted Actions using its existing Python runtime; the minimal read-only workflow exists to reproduce the bounded checks. Prior historical check counts remain attributed to their runs. The supplied REVIEW_RECORD describes an earlier CPython 3.13.5 read-only review; it does not substitute for the current execution.

### Disposition of inherited arguments

| Input | Disposition here |
|---|---|
| v1.1 §§4–6, 8, 10–12 | Retain known-model information/timing, total support coverage, typed error roles, fixed model identity, and scoped revision. Make the sequential package constructive. |
| B3 | Retain benchmark coverage for restricted policy lifts; it cannot be omitted from transfer. |
| B13 | Proof survives under common prior, stationary conditionally independent channel, common signed-loss span/fee, horizon, and total-policy premises. Marginal-only substitution is refuted by the two-report counterexample. |
| B14 | Retain fully observable/accessible history backup comparison and its premises. It alone is not policy regret. |
| B15 and C12–C13 | Old factor-two bound remains valid; use the proved stronger common-event positive-mass bound. Zero-mass conditioning remains undefined. |
| B16 | Retain with checked terminal and backup residuals and same-backup greediness. (S8) gives a constructive nonuniform specialization. |
| B17 | Retain exact same-comparator telescoping under the actually executed trajectory law; add explicit replacement identity and invalid-join controls. |

The task closes this bounded construction, not Bellman's programme. Scalable solvers, general nonlinear constraints, richer partial-observation abstractions, statistical model learning, tail/dynamic risk, causal or strategic engines, formal proof libraries, and interoperability implementations remain separate obligations. None is implemented, revived, or ruled out by this module.
