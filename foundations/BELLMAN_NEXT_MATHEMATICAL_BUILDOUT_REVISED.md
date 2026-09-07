# Bellman build-out: finite joint-law and conditional-decision certificate completion

**Date:** 7 September 2026. **Status:** Additive mathematical revision and small exact research reference. This is not a new substrate edition, a production solver, or a Writ integration. Substrate v1.1 and the original build-out remain unchanged historical inputs.

**Result.** The finite rational construction from B4–B8 now has explicit subjects, original-membership checks, conditional transformations, primal/dual certificate rules, a bounded producer, and a consumer that does not depend on that producer. The existing example yields attained posterior extrema **4/7 and 8/11**, with independently checked matching duals, and a uniform action-risk difference upper bound **−1/7**. Changed-loss, tie, incompatibility, relaxed-membership, and impossible-event controls retain distinct meanings. The proposed sharper conditioning inequality is accepted after two algebraic proof checks; old B15 remains valid.

## 1. Review adjudication before revision

The governing instruction is the supplied build-out completion prompt, explicitly adopted by the user. The adversarial review, its original source, and its results are evidence to evaluate, not authority to invent errors or expand the task.

| Finding | Classification and mathematical assessment | Treatment |
|---|---|---|
| R1: solver-facing certificates | Constructive completion. B4–B8's reductions and Farkas signs are valid; an attained value is not an extremum and a solver flag is not a proof. | §§2–6 specify and exercise the receiver's exact checks. |
| R2: exact arithmetic | Premise clarification. Finite spaces alone do not give exact operations on arbitrary real input encodings. | Rational reference profile; exact integer comparisons and elimination. B21 remains symbolic unless its numerical enclosure is justified, §9. |
| R3: integrated construction/revision | Constructive completion. B29's arithmetic is correct but its full producer/consumer chain was incomplete. | Existing model, reviewer duals, action certificate, changed query, ties, and alternatives worked through in §§6–7. |
| R4: extension maturity | Premise/scope clarification. Tail, causal, and strategic material has differing maturity; none is refuted by lacking a common implementation. | Explicit maturity table and inherited premises, §9. No additional extension engine. |
| R5: missing original author checks | Evidence limitation at the review's time. It did not show the author's results false. The actual originals are now recovered. | Original author outputs reproduce byte-for-byte; reviewer observations reproduce separately. Public portability and original-source identity are distinguished, §10. |
| Optional stronger conditioning inequality | Optional strengthening, not correction of false B15. | Accepted in §8 with the review's overlap proof, an independently derived event-set proof, and the fixed sharp case. |
| Review's “archive still needed” statement | Historical evidence limitation, not a mathematical finding. PR #3 was subsequently opened and was unmerged at initial inspection. It was merged externally while this completion was underway; archival packaging starts from main containing that archive. | Keep review bytes unchanged; ledger records the chronology rather than silently rewriting the review. |

No central theorem is retracted. This revision adds constructive contracts and point-of-use qualifications; it does not re-open KL5/KL6 or propose another grid.

## 2. Exact mathematical subject and input contract

Let the ordered atoms be `Ω=(ω₁,…,ω_n)`, with each atom an ordered assignment to declared variables. Labels denote supplied meanings, populations, regimes, and observation events; matching text does not prove that those meanings describe reality.

The linear analysis domain is

\[
P^+=\{x\in\mathbb R^n:x\ge0,\ Ax=b,\ Cx\le d\},
\tag{C1}
\]

with an explicit row `1ᵀx=1`. All displayed rows and right-hand sides are part of the subject. The **original** domain is either exactly `P=P⁺`, or

\[
P=\{x\in P^+:H_1(x),\ldots,H_k(x)\}.
\tag{C2}
\]

When constraints `H` are present, `P⁺` is a labeled outer relaxation, never relabeled as an exact original fiber. In the reference, `H` may be finite rational polynomial equalities or non-strict inequalities evaluated at a supplied rational point. That earns exact **point-membership checking**, not nonlinear optimization or a general proof of nonemptiness. Containment is sound here because the relaxation only drops explicitly retained conjuncts. Arbitrary maps between unrelated relaxations require a separate containment argument and are outside this reference.

A query includes:

- the complete model subject: variable and atom order, every original constraint, every dropped conjunct, and modeling-premise labels;
- an event label and its indicator vector `v∈{0,1}ⁿ`;
- a rational numerator `u`, with `u_i=0` outside the event for conditional queries;
- whether the query is conditional, and whether its minimum or maximum is requested;
- action labels, their loss rows and unit, where a decision is requested;
- the named requested quantity and its information context.

For conditional tasks the answer is `Q(x)=uᵀx/(vᵀx)` on the **eligible** original domain `P_e={x∈P:vᵀx>0}`. For unconditional tasks it is `uᵀx`, with the event set to the whole space. Finitely many losses `L_a(ω)` have a common meaning and unit. For an action comparison, the numerator is exactly `v_i(L_a(ω_i)−L_b(ω_i))`. The code constructs it from the declared losses; it is not an unrelated number supplied under an action label.

The reference accepts integers, integer/fraction strings, and exact `Fraction` inputs through constructors; booleans, binary floats, decimal strings, invalid denominators, and coefficients beyond the declared input limit are rejected. Constructors normalize rational values. Equality and ordering use integer/rational arithmetic, not a tolerance. Dimensions and normalization are checked. The small profile permits at most eight atoms, sixteen original linear rows, eight actions, and bounded finite polynomial point predicates; the transformation has at most nine variables. These are reference-resource limits, not Bellman's mathematical ceiling.

Certificates embed the full normalized `Task`. `consume(expected, certificate)` compares it with the independently supplied intended task before checking any proof. A byte digest is useful archival identity, not a substitute for that match or for arithmetic. Even a merely equivalent reordering is rejected until explicitly rebound and rechecked; no semantic equivalence service is claimed.

## 3. Witness and certificate contracts

Write a linear system generally as `Z={z≥0:Ez=f,Gz≤h}` and maximize the signed objective `rᵀz`. Minimization of a query uses `r` equal to its negative; the final bound is negated. All certificate vectors are exact rationals with checked dimensions.

### 3.1 Feasibility and attainment

A primal witness `z` must satisfy every equation, inequality, and nonnegativity constraint. If it is a transformed conditional point, inverse recovery in §4 must succeed. Then check every original dropped predicate on the recovered `x`.

- Passing only the analysis-domain tests proves an **outer feasible point** and an **outer attained query value**.
- Passing all original constraints proves an **original-model witness** and, if the event mass is positive, an **original attained query value**.
- Neither statement says that this value is an extremum or that the original model is the actual world.

The reference returns `original_attained` or `outer_attained_only`, with the recovered point and computed value. A zero-objective unconditional task can be used solely to record compatibility. Feasibility and attainment are separate facts even when the checker obtains both from one point.

### 3.2 Upper and lower bounds: independently checkable inequalities

An upper certificate supplies free `y`, nonnegative `zeta`, and claimed scalar `U`. The checker verifies

\[
\zeta\ge0,\qquad E^Ty+G^T\zeta\ge r,\qquad
U=f^Ty+h^T\zeta.
\tag{C3}
\]

For every feasible nonnegative `z`,

\[
r^Tz\le z^T(E^Ty+G^T\zeta)
=f^Ty+\zeta^TGz\le f^Ty+h^T\zeta=U.
\tag{C4}
\]

The first inequality needs `z≥0`; the last needs `zeta≥0`. This is the complete weak-duality checking proof. Apply it to `−r` with upper bound `U_-` to obtain the lower bound `−U_-`. A dual point need not be optimal to give a valid bound. A feasible primal point need not attain that bound.

A bound alone leaves nonemptiness unestablished. The code labels it `bound_only_nonemptiness_unestablished`; decision certification separately requires an eligible original witness. Over a sound outer set, the same bound is sufficient for its original members but may be conservative.

### 3.3 Exact optimum and identification

A primal witness and a checked dual satisfying `rᵀz=U` prove an attained maximum over the analysis set by (C4). If the recovered point is an original member, they also prove that **same exact original maximum**, even when the bound was obtained over a larger relaxation. This is a useful consequence of matching an original attainment with an outer bound. Without original membership the code reports only `outer_optimum_only`.

Two such certificates establish the exact original minimum and maximum, hence the smallest interval enclosure `[L,U]`. They do not generally show that every interior value is attainable when original nonlinear constraints make the domain disconnected. For the exact linear domain, the eligible domain is convex and the ratio is continuous, so its scalar image is an interval; attained extrema then give the full attainable interval. For example, `x₀+x₁=1`, `x₀x₁=0`, and query `x₀` have exact extrema 0 and 1 but attainable set `{0,1}`. The reference checks this distinction. If `L=U` and an eligible original witness exists, the query is identified. If two original eligible witnesses have different values, they prove nonidentification without needing optimality. Variation or an optimum attained only in a relaxation does not establish original variation. A pair of nonmatching upper/lower bounds is an enclosure, not the exact range.

### 3.4 Infeasibility and impossible conditioning

An infeasibility certificate supplies free `y` and nonnegative `zeta` such that

\[
E^Ty+G^T\zeta\ge0,\qquad f^Ty+h^T\zeta<0.
\tag{C5}
\]

A feasible `z` would yield `0≤zᵀ(Eᵀy+Gᵀzeta)≤fᵀy+hᵀzeta<0`. Thus the **analyzed** system is empty. Empty sound outer sets exclude the original set as well. A sign-reversed vector is not this certificate.

For transformed constraints, (C5) proves **no eligible original model**; it does not by itself distinguish an empty original domain from an impossible event within a nonempty domain. Add an original unconditional witness to establish the latter. `impossible_event` checks both ingredients and then returns `impossible_conditioning`. No posterior or conditional action set is produced on that branch.

### 3.5 No conclusion from missing computation

An invalid certificate is rejected; this does not prove the negation of its desired conclusion. A stopped search, budget exhaustion, or absence of a found vertex/certificate is `unfinished`, not infeasibility, nonidentification, a tie, or an optimum. A valid mathematical implication with an assumed empirical premise remains conditional; exact arithmetic supplies no empirical warrant for that premise.

## 4. Conditional transformation, support, and inverse

For `x∈P⁺` with `vᵀx>0`, put `t=1/(vᵀx)` and `w=tx`. The transformed **linear analysis** system is

\[
w\ge0,\ t\ge0,\quad Aw-bt=0,\quad Cw-dt\le0,
\quad v^Tw=1.
\tag{C6}
\]

The transformed objective is `(u,0)ᵀ(w,t)`. The normalization row gives `1ᵀw=t`; since `w≥0` and `vᵀw=1`, necessarily `t≥1>0`. Recover `x=w/t`. It satisfies all original **linear** constraints, normalization, and `vᵀx=1/t>0`; the objective equals the conditional query. Additional original predicates must still be checked at this recovered point. This is a bijection on the eligible linear domain, with explicit inverse—not a correspondence up to a zero-scale limiting point.

This specializes standard linear-fractional optimization to normalized joint laws. General fractional programs can admit zero-scaling points that represent limits; our normalization excludes them. The underlying established source is [Boyd and Vandenberghe, §4.3.2](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf). The sign checks and normalization-specific inverse above are explicit derivations.

The transformed domain can be unbounded in `t` when event probabilities approach zero. This is not an unbounded query: `u` vanishes outside the event, so `uᵀw` lies between the finite minimum and maximum of `u_i` over event atoms, because the event coordinates sum to one. A nonempty finite-dimensional polyhedron with a bounded linear optimum attains it. This standard LP fact justifies an exact optimizing procedure, but a recipient still receives and checks matching witnesses. No lower event-probability bound is needed for this exact transformation. Such a bound matters for stability under perturbations (§8).

## 5. Small reference procedure and decision outputs

### 5.1 Producer versus consumer

`joint_law.py` provides normalized model/task constructors, the exact transform/inverse, original point membership, bound/Farkas/optimality consumption, action checks, and a small proposal procedure. It imports no Decision Lab code.

`propose(task,max_bases)` selects a linearly independent subset of equality rows by exact Gaussian elimination. It appends original inequalities and the `−I` nonnegativity inequalities. For each choice of enough active inequalities to make a square full-rank system, it:

1. solves for a candidate primal point exactly and checks all original analysis rows;
2. solves the transposed active system for dual multipliers;
3. requires nonnegative multipliers on all active inequalities;
4. expands equality multipliers back to the supplied row order and drops the nonnegativity multipliers into the dual dominance slack;
5. sends the resulting primal/dual pair through `consume` and returns only if it passes.

This construction includes active nonnegativity constraints; it is not limited to the review helper's selected original `C` rows. A nondegenerate support is not assumed. At a successful return, correctness comes from the checked pair, not a claim that every vertex was enumerated.

The reference examines at most 25,000 active bases, with smaller user budgets allowed. Each system has at most nine variables and finite rational arithmetic. It terminates in finitely many arithmetic operations within that bound; no wall-time or efficient general-purpose solver guarantee is claimed. Without a checked pair it returns `unfinished`. In particular it is **not a complete infeasibility oracle**: supplied exact Farkas vectors are checked directly through (C5). A different solver may produce rational candidates through precisely the same interface. This combination is a bounded reference and an explicit solver/certificate interface, not a production solver platform.

The consumer never calls proposal or optimization code. Checks exercise it with `propose` disabled. This separates calculation paths; both are authored in this task and share Python rational arithmetic, so this is not independent authorship or machine-checked formal verification.

### 5.2 Common action, uniform strictness, and a complete minimizing set

For original eligible models, let `R_a(x)` be the conditional risk. For every competitor `b≠a`, a checked bound

\[
\sup_{x\in P_e}\bigl(R_a(x)-R_b(x)\bigr)\le U_{ab}\le0
\tag{C7}
\]

certifies that `a` is common optimal, provided an eligible original witness is available. If all bounds are strictly negative, `a` is uniformly strictly better than every other action and the full minimizing set is `{a}` throughout the family. Exclude self-comparisons. For a single-action menu there are no competitors and the singleton minimizing set is immediate; “strict against other actions” then has only its vacuous comparative meaning, not a numerical positive gap.

A bound equal to zero may indicate a true tie, slack certification, or both. To prove an actual tie, evaluate a feasible original witness and show equal minimal risks there. To prove a fixed complete minimizing set `S` over the family, require `S` nonempty, certify equality of each selected action with a representative using **both** signed bounds, and certify that the representative strictly beats every outside action. `fixed_minimizing_set` implements this sufficient uniform rule. It does not infer a full minimizing set from common optimality alone.

If a matching original optimizer gives `max(R_a−R_b)>0`, that witness refutes common optimality of `a`. An outer-only positive optimizer cannot do so. Different pairwise extrema must not be assembled into an alleged single attainable risk vector.

## 6. Existing integrated example: inputs → witnesses → bounds → action

Use exactly the original atom order

`(theta=0,not-e), (theta=0,e), (theta=1,not-e), (theta=1,e)`.

The prior parameter is in `[1/4,2/5]`, with the original channel `P(e|theta=0)=1/5`, `P(e|theta=1)=4/5`. The equivalent original linear constraints are

\[
A=\begin{pmatrix}1&1&1&1\\-1&4&0&0\\0&0&-4&1\end{pmatrix},\quad b=(1,0,0)^T,
\quad C=\begin{pmatrix}0&0&-1&-1\\0&0&1&1\end{pmatrix},\quad d=(-1/4,2/5)^T.
\tag{C8}
\]

Take `v=(0,1,0,1)` and `u=(0,0,0,1)`. Two original-model witnesses are

\[
x_L=(3/5,3/20,1/20,1/5),\qquad x_U=(12/25,3/25,2/25,8/25).
\tag{C9}
\]

Their positive event masses are `7/20` and `11/25`. They satisfy all original constraints; no relaxation is used. Forward transformation yields the reviewer points

\[
z_L=(12/7,3/7,1/7,4/7,20/7),\quad
z_U=(12/11,3/11,2/11,8/11,25/11).
\tag{C10}
\]

The transformed matrices are the original rows with columns `−b`, `−d`, followed by the event equality:

\[
E=\begin{pmatrix}1&1&1&1&-1\\-1&4&0&0&0\\0&0&-4&1&0\\0&1&0&1&0\end{pmatrix},\quad f=(0,0,0,1)^T,
\quad G=\begin{pmatrix}0&0&-1&-1&1/4\\0&0&1&1&-2/5\end{pmatrix},\quad h=(0,0)^T.
\tag{C11}
\]

For `r=(0,0,0,1,0)`, the review's upper dual is

`y_U=(-8/55,-8/55,3/55,8/11)`, `zeta_U=(0,4/11)`.

For `−r`, its dual is

`y_-=(4/35,4/35,-3/35,-4/7)`, `zeta_-=(16/35,0)`.

Direct multiplication gives `Eᵀy_U+Gᵀzeta_U=r` and `Eᵀy_-+Gᵀzeta_-=-r`. Their bounds are `8/11` and `−4/7`; their primal values match at (C10). Thus **4/7 and 8/11 are attained exact extrema**, not just endpoint guesses or safe bounds. They certify posterior nonidentification. As a separate distinction, the feasible prior `1/3` attains `2/3`; the simple event-equality dual gives the loose upper bound 1. Pairing them does not certify an optimum, and the checker rejects that claim.

Under zero-one losses, action 1 minus action 0 has numerator `(0,1,0,−1)` and conditional difference `w1−w3=1−2w3`. Combining twice the lower-query dual with the event equality gives

`y_D=(8/35,8/35,−6/35,−1/7)`, `zeta_D=(32/35,0)`.

Its checked upper bound is **−1/7**, attained at `x_L`. Together with the eligible original witness this certifies action 1 uniquely throughout the original family, with guaranteed risk gap at least `1/7`. The generated certificate and this independently checked reviewer-derived calculation agree.

### Changed question and tie controls

Changing the false-positive loss from 1 to 2 changes the difference to `2w1−w3=2−3w3`. Its exact range is `[−2/11,2/7]`, attained at the same respective endpoint models. At `x_L`, action 0 is better; at `x_U`, action 1 is better. No common action follows. The old certificate is rejected under the new loss subject; its original conditional statement is still true.

Changing only the prior family to `[1/5,2/5]` gives posterior range `[1/2,8/11]` and maximum zero-one risk difference 0. Action 1 remains common optimal. At prior `1/5`, both actions minimize; elsewhere action 1 is strictly better. Uniform strictness and a constant complete minimizing set are therefore not established. A separate same-model constant-loss control exercises the full-set checker with two tied minimizing actions and a strictly worse third action.

These are the already posed model and requested changed-query controls, not a new parameter-grid search.

## 7. Joining, original constraints, impossible events, and revision

### Incompatible triangle

For ordered binary triples, impose normalization and all three pairwise disagreements with probability one. With equality rows `(1,1{X≠Y},1{Y≠Z},1{X≠Z})`, the reviewer vector `y=(2,−1,−1,−1)` gives `Aᵀy≥0` and `bᵀy=−1`. This is an exact infeasibility certificate. Its sign reversal is rejected. An empty or budget-limited proposal run is never used as a replacement proof.

### Compatible join and nonunique dependence

The review's literal pair laws are

`P(X,Y)=[[3/8,1/8],[1/8,3/8]]`,
`P(Y,Z)=[[1/3,1/6],[1/6,1/3]]`.

Both have `P(Y)=(1/2,1/2)`. Define `p(x,y,z)=p(x,y)p(y,z)/p(y)`. The exact point checker verifies normalization and every supplied pair-marginal row. A zero-mass separator cell is assigned zero joint mass and is never divided by its mass. This constructs one compatible extension. It does not identify the true dependence or prove uniqueness; the reviewer also preserves the two fair-pair extensions with different `P(X=Z)` values.

### Missing independence

Fair binary marginals alone admit both the uniform joint `(1/4,1/4,1/4,1/4)` and `(1/2,0,0,1/2)`. If the original subject also requires independence `x00*x11−x01*x10=0`, the second point fails original membership. Optimizing `x00` over the linear relaxation attains `1/2`, while the independent original joint has `x00=1/4`. The former is only an outer optimum; it cannot prove original nonidentification or compatibility by itself. The uniform point does establish original compatibility. For the marginal query `x00+x01`, an outer bound `1/2` matched by this original point establishes the exact original value `1/2` without solving nonlinear optimization.

### Impossible event in a nonempty family

Take `x0+x1=1`, `x1=0`, and event `{1}`. `(1,0)` is an original witness. The transformed equalities are `(w0+w1−t=0,w1=0,w1=1)`. Multipliers `(0,1,−1)` give zero left vector and bound `−1`. The event is impossible throughout this nonempty family. A posterior and conditional action set are undefined; no arbitrary legal response on an impossible history is relabeled conditional optimality.

### Keep dependencies with the statement

A certificate retains its model subject, original predicates and any relaxation, event, query, loss/action table, and computed proof vectors. Reuse under a changed premise requires checking against the new intended subject. A differing subject triggers reassessment, not retroactive falsity. Even if a forged label is rebound to the new task, the new arithmetic must pass; a forged larger objective with old duals is rejected.

Competing explanations are retained as alternatives. The integrated endpoint models separately give valid conditional answers. If instead their two distinct prior equalities are **jointly asserted**, the equality multipliers selecting `p=1/4` minus `p=2/5` give contradiction `−3/20`. The conjunction is inconsistent; the alternative family is not. A second proof restores support only if its own premises are warranted. No dependency-graph infrastructure or circular self-support is introduced.

## 8. Accepted conditioning strengthening, independently proof-checked

Let finite probability laws `P,Q` share the same event `e`, with positive masses `a=P(e), b=Q(e)` and `Delta=TV(P,Q)`, where `TV` is half the L1 distance. Then

\[
TV(P(\cdot\mid e),Q(\cdot\mid e))
\le\min\left(1,\frac{\Delta}{\max(a,b)}\right).
\tag{C12}
\]

If `Delta≤epsilon` and `P(e)≥kappa>0`, this implies `min(1,epsilon/kappa)`. Positive `Q(e)` remains required; `epsilon<kappa` is sufficient to establish it when it is not separately supplied.

**Check of the review's overlap proof.** Assume `a≤b` by symmetry. Restricted L1 discrepancy is at most `2Delta−(b−a)` because outside-event L1 is at least `b−a`. Hence unnormalized common mass within the event is at least `b−Delta`. For each event atom, `min(P_i/a,Q_i/b)≥min(P_i,Q_i)/b`. Summing gives normalized common mass at least `1−Delta/b`. Total variation is one minus common mass. The proof uses no independence or equal-mass assumption. If `Delta>b`, the bound is replaced by the trivial bound 1; negative intermediate overlap lower bounds cause no invalid inference.

**Independent event-set proof.** Again let `a≤b`. Define `A⊆e` by the atoms where `Q_i/b>P_i/a`. Its normalized probability difference is exactly the conditional TV, say `delta`. Then

\[
b\delta=Q(A)-(b/a)P(A)\le Q(A)-P(A)\le\Delta,
\tag{C13}
\]

because `b/a≥1` and every event's probability difference is at most TV. This derives (C12) without using the overlap calculation.

For the review's fixed sharp case `P=(1/10,3/20,0,3/4)`, `Q=(0,3/20,1/10,3/4)`, and first three atoms as `e`, both masses are `1/4`, joint TV is `1/10`, and conditional TV is `2/5`. The new radius is the attained `2/5`; old B15 gives the valid conservative `4/5`. A smaller universal factor than 1 fails this example. Unequal event masses and the rare-event case with conditional TV 1 are also checked. This is an accepted reviewer-derived strengthening with no novelty claim and no alteration to the frozen B15 text.

A common conditional loss with span `D` inherits expectation error at most `D min(1,epsilon/kappa)`. It does not establish a whole-policy guarantee without that theorem's model, lift, support, and benchmark premises.

## 9. Point-of-use qualifications for the retained wider mathematics

- **B9–B12 and exact checks:** Rational costs/kernels and exact finite evaluators give decidable equality for the reference's partitions, residuals, and contextual identities. General real-valued statements remain mathematics; arbitrary-real exact algorithms are not promised.
- **B13:** Common prior, stationary conditionally independent channels, common bounded signed terminal losses and nonnegative fee, and common total policies remain required. The forced-observation optimum exists only at positive horizon. Horizon zero has stop-only comparison; it supplies no observation margin.
- **B3 and B14:** Policy transfer retains the benchmark-coverage term. Closeness of optimal values alone does not certify an implementable policy. B14 is the stated fully observed backup argument; partial observation needs an accessible recursively valid information state.
- **B16–B17:** Residuals must be checked against the actual specified model/backup, terminal value, and the policy greedy for that same backup (plus any stated approximate-greediness error). The telescoping costs use the actual policy trajectory and matching exact optimum. Unrelated local values cannot be summed into regret.
- **B20:** The supplied history/kernel must include all informative observations; averaging away a persistent model label does not implement learning about it.
- **B21–B22:** The radius containing `log` and `sqrt` is an exact symbolic real theorem under fixed finite IID sampling assumptions. An implemented radius must be a certified upper enclosure of that exact radius, or an equivalent justified guarantee; this reference supplies no transcendental evaluator. If `r_hat≥r`, the implemented confidence set encloses the theorem's set, preserving its coverage implication. Inward rounding can exclude a point on the original coverage event, as the reviewer control demonstrates. Simultaneous frequentist coverage is not a posterior probability that a selected model is true, and it is not a loss-valued error budget.
- **Causal claims:** Exact adjustment arithmetic establishes its implication under a valid causal model, adjustment set, and positive support. It does not validate those assumptions empirically or remove estimation uncertainty.

| Retained extension | Actual maturity after this completion |
|---|---|
| Finite constraints and occupancies | Defined constructive fully observed flow mathematics, not implemented by this module. |
| Finite static CVaR | Explicit definition and fixed arithmetic checks, including atoms; not a dynamic risk engine. |
| Dynamic risk consistency | Further formalization remains necessary. |
| Causal adjustment / response types | Conditional constructions under specified causal assumptions; general nonlinear original constraints and transport remain outside this reference. |
| Multiple objectives and strategy | Preference/equilibrium interfaces and defining inequalities, not an implemented strategic solver or warranted prediction of behavior. |

These qualifications keep the wider programme open. No game-theory implementation, new experiment, or Decision Lab restriction follows from completing this one module.

## 10. Exact execution evidence and preservation

| Evidence | Identity and actual treatment | Result and limit |
|---|---|---|
| Original author source and literal inputs | Recovered actual `checks.py`, SHA-256 `1721ef813e7604ad79267888c36f1797c5e901f3fe535f0cc61578642105a46f`; literals are embedded in that source. Replayed an exact source copy in a separate workspace. | 18 original groups passed on Python 3.9.6. Both original `checks.json` and `CHECKS.md` reproduced byte-for-byte, including the `63/80` residual bound and `7/64` local regret. Original files were not overwritten. |
| Original reviewer source/results | Exact supplied harness SHA-256 `55c9fb770e1959c9be3d65ee517fb628b25e940148194e414027043b63aa9486`; supplied results report Python 3.13.5. | Exact harness replay on Python 3.9.6: 19 passed, 0 failed, 0 not run, normally and with `-O`. All group observations equal the supplied results; runtime metadata intentionally differs. |
| New completion module | `joint_law.py`, `module_checks.py`, and `module_results.json`, with actual identities in the completion manifest. | 19 fixed cases passed normally and with `-O`; observations and retained certificates agree across modes. Includes negative controls and separate producer-disabled consumption. This is new evidence, not the original 18 groups. |
| Historical substrate-v1 review harness | Still not recovered; distinct from the build-out reviewer harness supplied here. | No claimed replay. Earlier archival gaps are not silently resolved by similarly named new files. |

The original author source contains a machine-specific private absolute path. Its exact bytes remain preserved locally and its actual digest is recorded; the public archive retains the existing explicitly portable replay whose mathematical calculation block is identical. It is not misrepresented as that original byte-identical source. Original author compact results and summary are already preserved exactly. Original build-out review source/results and this review are archived exactly. ZIPs used solely to reproduce packet-integrity checks, temporary output duplicates, caches, and local paths are excluded.

The preserved source code, archived inputs, and compact evidence identify what ran. Fresh normal/optimized replay files are reduced to a replay record recording their observed counts, source identities, and group-equality comparison with the retained original results; they are not duplicated as two large logs. The exact reviewer harness run directly in the repository without the optional packet ZIP reports its 18 mathematical groups and one explicit `NOT_RUN` integrity group. Full 19-group replay was performed with the original packet in a temporary workspace; the ZIP is not needed for the mathematics and is not committed.

Actual command forms and outcomes are listed in the verification README and replay record. No toolchain was installed or globally reconfigured. There were no failing executed author, reviewer, or module checks in this completion; deliberate bad-certificate controls passed by refusing invalid claims. Tests verify these finite instances and checking rules, not all general theorems or empirical coverage. Both proof arguments in §8 are independently checked algebraic paths within this task, not independent authors or a formal theorem prover.

## 11. Completed scope and remaining obligations

This completion earns a precise finite rational linear joint-law → eligible conditional query → checked decision-certificate construction, with exact examples and reusable checker source. Bounds and matching original witnesses are sufficient for the claimed conclusions. Feasibility of a relaxation, partial optimization, and assumed substantive premises remain explicitly weaker results.

Remaining obligations are general infeasibility-certificate discovery beyond supplied witnesses, scalable optimization and resource guarantees, full nonlinear original-domain optimization, certified numerical confidence radii, broader temporal/causal/risk constructions, and external proof/implementation review. None is needed to disguise this bounded completion as a universal platform. The reference is not an accepted Writ integration, and present executable slices do not determine Bellman's mathematical scope.

Publication preserves the original v1.1 and build-out, appends this revision and evidence, and retains historical KL material without modification. A PR is an archival publication for review, not mathematical acceptance or authorization to merge.
