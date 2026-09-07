# Bellman: next mathematical build-out from Substrate v1.1

**Status:** Mathematical development draft, 7 September 2026. An additive companion to v1.1, not a replacement edition or a software acceptance report.

**Main conclusion.** v1.1 already has substantial exact mathematics. Its largest immediate deficit is the distance between a semantic criterion and a constructed, checkable instance. The next layer should supply finite compatibility witnesses, constructive representations, executable information simulators, certified optimization, and stronger sequential composition. A richer treatment of consequential decisions additionally needs statistical learning, constraints and tail risk, causal identification, and—when other decision-makers become endogenous—preferences and incentives. None requires a novelty claim.

This document develops those additions rather than merely listing topics. Results below are elementary derivations or finite specializations of established mathematics. They are not asserted to be new theorems. Small calculations accompany the development; they are illustrative conformance checks, not empirical research or a revival of a stopped experiment.

## 1. Scope, source authority, and preservation

The controlling request is to take v1.1 as the base, assess its mathematical maturity, deepen composition, and begin a progressively richer mathematical substrate. The packet's `RUN_THIS_NEXT_*` documents propose different assignments: a current-code review and a convergence decision constrained to one engineering capability. Those are reference documents, not instructions executed here. In particular, their restriction against expanding the substrate does not constrain this explicit mathematical expansion.

The original v1.1 and all packet inputs remain unchanged. Its historical KL5/KL6 and frontier stopping dispositions remain inherited records with their original scope. Its references to unavailable earlier audits and past test runs are source-reported, not independently reproduced here. The PR reports are unnecessary to these mathematical derivations; no current Writ code or PR acceptance is inferred from them. This work does not select an implementation architecture.

The base used is `inputs/BELLMAN_WRIT_MATHEMATICAL_SUBSTRATE_V1_1.md`, SHA-256 `91f535d7010fa3bb4e4e1fdab6a1cebd3643f97666e5ba32240c81f264a8597e`. The companion North Star supplies the seven obligations: object, assumptions, operation, guarantee, composition, failure boundary, and provenance.

Throughout, spaces are finite unless explicitly stated, action menus are nonempty, horizons are finite, costs are bounded, and all compared policies have legal total implementations on the union of covered history supports. Probability kernels are normalized. `TV` means half the L1 distance. Undefined conditioning remains undefined; a legal action on a zero-probability history does not manufacture a posterior. All exact-fiber claims require a nonempty exact fiber or an existence witness; an outer enclosure is labeled separately.

## 2. What v1.1 has, and what is missing

These are overlapping maturity dimensions, not a ranking of entire components. A component can contain a computable formula, a nonconstructive characterization, and an organizing convention.

| v1.1 location | Mathematics already present | Remaining gap | Development here |
|---|---|---|---|
| §§2, 10.1, 10.11, 11 | Conditional-result pattern and dependency distinctions | Mostly organizing principles; no general procedure deciding applicability or revision | Typed partial contracts and explicit proof obligations, §3 |
| §3 | Bayes, finite elimination, qualified fusion | Global compatibility is defined, not generally constructed; dependence may be unknown | Joint-law LP, witnesses, conditional extrema, §4 |
| §4 | Explicit stopping recurrence and known-model information state | General controlled dynamics and state construction are not fully instantiated | Constructive abstraction and persistent model-state update, §§5, 9 |
| §5, equations (11)–(12) | Fiber constancy and common-minimizer characterizations | Semantic existence need not supply a decoder; no universal efficient discovery procedure | Finite query quotient, backward partitions, separation certificates, §5 |
| §6 | Coupling, regret, margins, AIS theorem interface | Error radii assumed supplied; signed losses excluded from coupling; solver certificates not constructed | Span bound, Bellman residuals and local regret, §§7–8 |
| §7 | Blackwell simulation, deficiency, contextual sufficiency | Simulator optimization and finite contextual checks not instantiated | Explicit LP and polynomial equality checks, §6 |
| §8 | Robust objectives, half-range optimum, model persistence | Arbitrary extrema and nonrectangular planning have no generic constructive method | Finite policy-matrix LP; exact whole-model semantics, §9 |
| §9 | Intervention-indexed preservation | Principally an interface; does not identify effects from data | Finite adjustment and response-type bounds, §12 |
| §10.2 | Exact versus outer compatibility | No test supplying an original-model witness | §4 |
| §§10.4–10.6 | Exact substitution, scalar Lipschitz and simulation error rules | Policy-lift coverage and adaptive sequential error need explicit derivation | §§3, 7–8 |
| §§10.7–10.9 | Context and temporal identity safeguards | Conditioning amplification and contextual checking remain underdeveloped | §§6–7, 9 |
| §10.10 | Fixed finite union bound | No data-to-model construction valid under repeated inspection | A simple confidence sequence and decision bridge, §10 |
| §12, final boundary | Expected loss does not imply harm or authority guarantees | No tail-risk, constrained, plural-objective, or incentive mathematics | §§11–13 |

**Three important distinctions.** The finite stopping recurrence is already constructive once its inputs are available. The general fiber criterion is exact mathematics without a general effective decoder. Provenance and semantic alignment are mostly organizing conventions: attaching more formal notation does not by itself establish real-world variable identity or empirical adequacy.

## 3. Make composition a typed partial operation

### 3.1 Contract and composition rule

Represent a mathematical operation as a partial map `f:D→Y` with a contract

\[
A(x)\Longrightarrow [x\in D\ \land\ R_f(x,f(x))].
\tag{B1}
\]

The type of `x` includes the model class, information schedule, units, feasible policy class, and query—not merely a data format. A second operation `g` needs predicate `B(y)`. To compose, prove

\[
A(x)\land R_f(x,y)\Longrightarrow B(y).
\tag{B2}
\]

Then substitution proves the composite guarantee. This is an ordinary contract/implication rule, not a proposed universal proof language. A finite checker can verify a supplied stochastic matrix, arithmetic identity, or partition. It cannot thereby decide whether two source reports concern the same real event.

Each application therefore carries two separate items: a mathematical proof or check of the conditional result, and the warrant for its actual premises. Store unresolved premises as unresolved; never turn failure to prove a premise into proof of its negation.

### 3.2 Policy lifts require benchmark coverage

Suppose an abstraction has lift `L:barΠ→Π` and

\[
|J_F(L\bar\pi)-\bar J(\bar\pi)|\le e\quad\forall\bar\pi.
\]

This alone does **not** bound regret against all of `Π`: the abstraction might omit every good original policy. An additional benchmark condition is

\[
\inf_{\bar\pi}J_F(L\bar\pi)\le V_F+\beta.
\]

For an `η`-optimal abstract policy, inserting the abstract optimum and the lifted-class optimum gives

\[
J_F(L\widehat\pi)-V_F\le 2e+\eta+\beta.
\tag{B3}
\]

**Proof.** Uniform error bounds the returned lifted cost above by the abstract optimum plus `η+e`, and bounds that optimum above by the infimum lifted cost plus `e`. Apply benchmark coverage. With exact abstraction and optimal lift coverage, `e=β=0`.

For two abstractions, compose lifts in order, prove the analogous cost comparison and benchmark coverage at each interface, then apply (B3). Do not add the two final regret claims without this bridge. A total executable composite lift must respect the recipient's actual information at each date.

**Provenance/correction extension.** Let assumptions be nodes and derivations be directed hyperedges from all their required premises to a conclusion. A changed assumption marks descendants for reassessment. An alternative unaffected derivation can still warrant the same conclusion. Reachability detects potentially affected derivations, not mathematical falsity; shared ancestry still says nothing by itself about statistical independence. This is a useful finite bookkeeping operation, not a general theory of belief revision.

## 4. Construct compatibility, identification, and evidence joins

### 4.1 Exact finite joint-law profile

Let `Ω` enumerate assignments to all variables needed for a proposed join. Put one mass `p_ω` on each assignment. Normalization, supplied marginals, support restrictions, and linear moment bounds yield

\[
\mathcal P=\{p\ge0:Ap=b,\ Cp\le d\},
\tag{B4}
\]

including `1ᵀp=1` among the equalities. This is the **exact** set only if these are all original constraints. Dropping independence, rank, stationarity, or mechanism constraints generally produces an outer polytope instead. Conditional independence with unknown factors is generally polynomial, not linear.

**Procedure.** Build the constraint matrices; find a feasible point or infeasibility certificate; check it against the original constraints. For rational data, rational witnesses permit exact verification. Solver termination without a checked witness is an unresolved computation, not a compatibility theorem.

A useful infeasibility certificate is a pair `(y,z)` satisfying

\[
z\ge0,\quad A^Ty+C^Tz\ge0,\quad b^Ty+d^Tz<0.
\tag{B5}
\]

Indeed, any feasible `p` would imply
`0≤pᵀ(Aᵀy+Cᵀz)≤bᵀy+dᵀz<0`, a contradiction. Existence of such certificates for infeasible linear systems is the finite theorem of alternatives. LP duality also supplies checked upper/lower bounds and optimality gaps. These established foundations are covered in [Boyd and Vandenberghe, chapters 4–5](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf). Subsequent formulas here explicitly derive the Bellman-specific uses rather than assume arbitrary fibers are convex.

**Decisive incompatibility example.** Binary `X,Y,Z` have individually consistent pair marginals: each pair is uniform over its two unequal assignments. Thus every singleton is fair, yet all three pairs are required to disagree almost surely. For each binary triple,
`1{X≠Y}+1{Y≠Z}+1{X≠Z}≤2`.
The specified marginals require expected sum 3. Matching all overlaps therefore does not establish a joint model. The inequality is an inspectable separating certificate.

### 4.2 A positive gluing theorem

Given consistent `P(X,Y)` and `P(Y,Z)`, define for `p(y)>0`

\[
p(x,y,z)=p(x,y)p(y,z)/p(y),
\tag{B6}
\]

and zero mass when `p(y)=0`. Summing over `x` or `z` recovers the supplied marginals. Thus a joint extension exists. It enforces `X⊥Z|Y`; it is one extension, not a conclusion that reality has that independence. A query varying across other extensions remains unidentified.

For a tree of clusters satisfying the running-intersection property, attach each child using its conditional distribution on variables outside the separator. Induction proves normalization and preservation of every cluster marginal. This gives a constructive existence result for that tree pattern. Extra cross-cluster or cyclic constraints must still be checked; the triangle example shows why.

### 4.3 Query bounds and conditional identification

For a linear query `rᵀp`, solve its minimum and maximum over (B4). If both checked bounds coincide, the scalar is identified. If two feasible points give different values, they certify nonidentification. A nonzero **relaxed** range is not such a certificate for a smaller original fiber.

For event `e`, let `v_ω=1{ω∈e}` and `u_ω=1{ω∈e}f(ω)`. A conditional expectation is

\[
Q(p)=u^Tp/(v^Tp),\quad v^Tp>0.
\]

Use `t=1/(vᵀp)` and `w=tp`. Its exact transformed feasible set is

\[
w\ge0,\quad Aw=bt,\quad Cw\le dt,\quad v^Tw=1,\quad t\ge0.
\tag{B7}
\]

Because normalization implies `1ᵀw=t`, feasibility forces `t>0`; recover `p=w/t`. The objective is `uᵀw`. This bijection proves that two LPs compute the conditional extrema for this finite polytope. First check that some original model gives `e` positive mass. This transformation is not applicable unchanged to arbitrary nonlinear fibers.

**Decision-relative identification.** To certify a fixed action `a` is optimal under every `p∈P`, it suffices and is necessary to have

\[
\max_{p\in\mathcal P}(r_a-r_b)^Tp\le0\quad\forall b.
\tag{B8}
\]

It is uniformly strictly optimal when all these maxima are negative for `b≠a`. This can succeed when individual action risks vary. Complete minimizing sets require additional equality and strict-exclusion checks; one common optimal action is a weaker output.

**Failure/cost boundary.** The assignment table grows exponentially with variable count. Finite LP constructibility is not a scalability claim. Polynomial constraints may require certified global methods; a local optimum is insufficient. A feasible original model establishes compatibility, not real-world membership. Provenance includes every equality, inequality, omitted constraint, and verified witness.

## 5. Construct representations rather than assert sufficiency

### 5.1 Finite query quotient

For explicitly enumerated finite model class `F₁,…,F_n` and finite query family `q₁,…,q_k` with supplied terminating exact evaluators and decidable equality of their outputs, compute each complete requested answer and form

\[
F_i\sim F_j\iff (Q_{q_1}(F_i),\ldots,Q_{q_k}(F_i))
=(Q_{q_1}(F_j),\ldots,Q_{q_k}(F_j)).
\tag{B9}
\]

The equivalence class is the coarsest deterministic model representation preserving those answers. **Proof:** any sufficient encoder must separate models with different answer vectors; equal vectors admit the common lookup decoder. Include full argmin sets in the vector when those are requested. If the query is only common-action selection, use intersections of optimal sets instead; that is a different design problem and need not define this equivalence relation.

This closes a constructive gap for explicit finite domains with those evaluators, at the cost of computing all answers. Query names alone do not supply an evaluation algorithm. Report decoder size as well as payload size. It is an answer table, not evidence of a discovered structural compression. Infinite domains and arbitrary real-valued predicates are outside this algorithm.

### 5.2 Backward state partitions for finite-horizon MDPs

For known finite time-dependent MDP data `g_t(x,a),P_t(y|x,a)` and terminal loss `g_T`, first partition terminal states by `g_T(x)`. Given partition `P_{t+1}`, partition states at time `t` by the signature

\[
\left(A_t(x),\ (g_t(x,a))_a,
\left(\sum_{y\in C}P_t(y\mid x,a)\right)_{a,C\in\mathscr P_{t+1}}\right).
\tag{B10}
\]

Action names and availability must match inside a class. Choose any representative's signature for the abstract model. Backward induction shows that each abstract action value, optimal value, and optimizing action set agrees with the original at that date. An optimal abstract policy lifts through the observed class map.

This is a finite constructive sufficient abstraction. It can distinguish states whose optimum happens to agree, so do **not** call it the coarsest value-only quotient. For stationary structural equivalence, iterative splitting until stability constructs the corresponding bisimulation partition. The established model-minimization foundation is [Givan, Dean, and Greig (2003)](https://cs.brown.edu/people/tdean/publications/archive/GivanetalAIJ-03.pdf); (B10) states the specific backward finite-horizon construction used here.

**Genuine compression example.** States `x₁,x₂` have identical action costs. Under a fixed action, their transition rows over `x₁,x₂,z` are `(1/2,0,1/2)` and `(0,1/2,1/2)`. Their probabilities of classes `{x₁,x₂}` and `{z}` agree, while the labeled rows differ. If the terminal loss is constant on `{x₁,x₂}` and all other actions satisfy the same class-sum property, merging is exact and does not reconstruct the original rows.

**Boundary.** A hidden-state partition is not automatically an accessible history statistic. In partial observation one must construct a recursively updatable information state, preserve its controlled prediction law, and supply the policy lift. Unknown models also require uniform preservation or a richer state carrying model identity.

### 5.3 Closure under future calculations

Value tests must cover the continuation functions a backup actually uses. For a declared collection `V_{t+1}`, require equality of `g_t+P_t v` for every admitted action and `v∈V_{t+1}`, then include the pointwise minima in `V_t`. Repeat to the root. Without this closure, equality on a linear basis or a few sample value functions may fail after minimization. Constructing the closure can approach the full problem size; that is an honest outcome.

**Certificate.** Return the partition/encoder, class signatures, abstract data, decoder or update, and exact equality checks. A separating signature diagnoses structural failure, but need not refute weaker value preservation.

## 6. Construct information comparisons and contextual checks

### 6.1 Finite deficiency as an LP

Given row-stochastic experiments `E_{θx}` and `G_{θy}`, choose a row-stochastic simulator `T_{xy}` and minimize `d` subject to

\[
u_{\theta y}\ge\pm\left(\sum_xE_{\theta x}T_{xy}-G_{\theta y}\right),
\quad u_{\theta y}\ge0,\quad \tfrac12\sum_yu_{\theta y}\le d\quad\forall\theta.
\tag{B11}
\]

This is exactly v1.1's finite TV-deficiency optimization: at fixed `T`, the smallest slack sum equals its rowwise L1 discrepancy. A feasible solution constructs an executable simulator and certified upper bound. A checked lower bound is required to call it optimal or to prove no zero-error simulator exists. When `d=0`, composing `T` with any `G` decision rule yields its exact `E` implementation. With loss span `D`, fixed-rule risks differ by at most `Dd`; hence the optimal-risk comparison follows by taking the infimum over target rules. Acquisition fees still need separate accounting.

No new literature claim is needed for this LP reduction: it follows directly from v1.1 equation (21) and the absolute-value epigraph.

### 6.2 Specified contextual sufficiency is checkable

For deterministic `Y=f(X)` and a **supplied joint law** `p(θ,x,z)`, test on each positive `(x,z)` cell

\[
p(\theta,x,z)\,p(y,z)=p(\theta,y,z)\,p(x,z),\quad y=f(x),\quad\forall\theta.
\tag{B12}
\]

Division by the two positive masses gives equality of the posteriors. Thus these exact finite equalities test v1.1 equation (23), without evaluating a zero-mass posterior. For a joint-model fiber, the identities must hold throughout it; checking one fitted joint law is insufficient. Violations in genuine fiber members give counterexamples. Unknown dependence does not become known through this check.

**Failure example.** Let `θ` and `X` be independent fair bits, let `Y` be constant, and set `Z=θ XOR X`. Isolated `X` and `Y` are equally uninformative about `θ`; `(X,Z)` reveals `θ`, while `(Y,Z)` does not. Under zero-one prediction loss their joined risks are respectively 0 and `1/2`.

### 6.3 Online simulation needs sequential kernels

An online simulator at time `t` may use only the source observations available by `t`, past simulated observations, and permitted private randomization. Composition remains nonanticipative because substituting those functions never introduces later observations. To transfer adaptive controlled policies, require simulation of the relevant controlled observation law for **every allowed past action/history**, not only a passive final-string experiment. A final-time garbling is insufficient.

Store the kernel, timing, randomness assumptions, rowwise residuals, joint context, and any optimizer certificate. The operation fails when those objects are absent even if an abstract dominance statement is true.

## 7. Strengthen approximation and conditioning composition

### 7.1 Signed-loss and sharper stopping bound

Retain v1.1's static state, common prior, stationary conditionally independent observation channels, nonnegative common fee `c`, horizon `h`, and total common policy class. Replace `0≤L≤L_max` with

\[
\ell\le L(a,\theta)\le u,\qquad D=u-\ell\ge0.
\]

If channel TV is uniformly at most `d`, put `d̄=min(1,d)` and

\[
e_h^{\mathrm{span}}=(D+hc)\,[1-(1-\bar d)^h],\quad e_0^{\mathrm{span}}=0.
\tag{B13}
\]

Then every common policy has absolute ex ante cost discrepancy at most `e_h^span`; optimal and forced-first-observation values inherit it, and an `η`-optimal surrogate policy has regret at most `2e_h^span+η`.

**Proof.** Couple the common hidden state exactly. Conditional on it, independently maximally couple each of the `h` potential observations and couple the private policy seed identically. Probability of at least one mismatch is at most `1-(1-d̄)^h`. With no mismatch the policy path and cost agree. All costs lie in `[ℓ,u+hc]`, a range of length `D+hc`. Bound the expectation difference by range times mismatch probability, then apply the same infimum and optimizer argument as v1.1. Early stopping causes no problem because unused potential observations can still be coupled. The bound is no larger than `(D+hc)min(1,hd)`.

Equivalently, shifting terminal losses by `−ℓ` shifts every policy cost by the same constant, preserving choices and regret. This closes the signed-loss gap mathematically; it does not claim an approximate Build 1 implementation.

**Check.** The base's signed-loss example has `ℓ=−99,u=1,D=100,h=1,c=0,d=1/100`. Bound (B13) is 1, exactly the stated value difference between `−99` and `−98`. Using the upper endpoint alone would give the false bound `1/100`.

### 7.2 General controlled finite-horizon comparison

For two fully observed models on the same states/actions, with stage discrepancy `|g_t−ĝ_t|≤ε_t`, row TV discrepancy `≤δ_t`, terminal discrepancy `≤ε_T`, and bounded surrogate optimum `V̂_{t+1}`, define

\[
\alpha_T=\epsilon_T,\qquad
\alpha_t=\epsilon_t+\delta_t\operatorname{span}(\widehat V_{t+1})+\alpha_{t+1}.
\tag{B14}
\]

Then action values and optimal values at `t` differ by at most `α_t`.

**Proof.** Split the difference into stage error, expectation of `V_{t+1}−V̂_{t+1}`, and `(P_t−P̂_t)V̂_{t+1}`. The first two terms are bounded by `ε_t` and `α_{t+1}`. Centering a function at its minimum proves `|Pf−Qf|≤span(f)TV(P,Q)`. Finally `|min f−min g|≤max|f−g|`. This elementary fully observed derivation complements the broader [approximate information-state framework](https://jmlr.org/papers/v23/20-1165.html); it does not import that framework's partial-observation conclusions without its update hypotheses.

For whole-policy regret, either compare every policy using uniform continuation-span bounds and then apply (B3), or derive the lifted policy's Bellman residual as in §8. Closeness of optimal values alone remains insufficient.

### 7.3 Conditioning is quantitatively unstable

Let `P,Q` be laws on the same finite space with `TV(P,Q)≤ε`. For a common event `e`, assume both masses are positive and `P(e)≥κ>0`. Then

\[
\operatorname{TV}(P(\cdot\mid e),Q(\cdot\mid e))
\le\min(1,2\epsilon/\kappa).
\tag{B15}
\]

**Proof.** For any `A⊆e`, write `p=P(e),q=Q(e)` and add/subtract `Q(A)/p`:
`|P(A)/p−Q(A)/q|≤|P(A)−Q(A)|/p+(Q(A)/q)|q−p|/p≤2ε/p`.
Take the supremum. This conservative bound is not claimed sharp. If positivity of `Q(e)` is not already established, `ε<κ` suffices because `Q(e)≥κ−ε`.

Thus a conditional bounded-loss certificate has radius at most `D min(1,2ε/κ)`. Ex ante control without an event-mass lower bound cannot give a uniformly small conditional certificate.

**Check.** `P(e,θ=0)=1/100`, `Q(e,θ=1)=1/100`, and both put `99/100` on the same outside atom. Ex ante TV is `1/100`; conditional TV is 1. This is not an approximation failure—it is a failure to preserve the scope of the guarantee.

## 8. Turn local computation into whole-policy certificates

### 8.1 Bellman residuals

For a known finite MDP let `T_t v(x)=min_a[g_t(x,a)+P_t v(x,a)]`. Suppose an available approximate value table `ṽ_t` satisfies

\[
\|\widetilde v_T-g_T\|_\infty\le r_T,
\qquad\|\widetilde v_t-T_t\widetilde v_{t+1}\|_\infty\le r_t.
\]

Let `π_t` be greedy for this **same** backup. Nonexpansiveness of expectation and minimization proves, by induction, both

\[
\|\widetilde v_t-V_t^*\|_\infty\le\sum_{k=t}^T r_k,
\quad
\|\widetilde v_t-J_t^\pi\|_\infty\le\sum_{k=t}^T r_k.
\]

Hence

\[
J_t^\pi-V_t^*\le2\sum_{k=t}^T r_k.
\tag{B16}
\]

For `ζ_t`-greedy action selection relative to the backup, add `Σζ_t`. Residuals against approximate model backups first certify the surrogate problem; model transfer still requires its own bound. Checking residuals only on sampled states is not uniform certification unless coverage of all relevant states is established.

### 8.2 A direct local-regret identity

For any policy in a known model with exact optimal continuation, define its conditional Bellman disadvantage

\[
d_t(h_t)=\mathbb E[g_t+V_{t+1}^*\mid h_t,\pi_t]-V_t^*(h_t)\ge0.
\]

Telescoping conditional expectations yields

\[
J^\pi-V_0^*=\mathbb E_\pi\sum_{t=0}^{T-1}d_t(H_t).
\tag{B17}
\]

Therefore uniformly established `d_t≤β_t` implies regret `≤Σβ_t`. This is the missing justification for adding **local** decision errors: they must be Bellman disadvantages against the same continuation optimum under the actual trajectory law. Differences between unrelated root optimum values do not qualify.

For stopping, add an absorbing post-stop state with zero subsequent cost so the telescoping proof applies unchanged. If replanning replaces a certified policy, re-establish local disadvantages for the replanned choices; the old ex ante certificate does not transfer automatically.

**Practical certificate outputs.** Return feasible policy, checked lower bound on the optimum, checked policy-cost upper bound, and their gap. In finite rational trees these can be exact; in larger numerical problems certified intervals can suffice. An optimizer's status flag alone is not a mathematical error allowance.

## 9. Preserve model uncertainty while making it solvable

### 9.1 Exact finite fixed-model robust planning

Let `F₁,…,F_m` be fully specified episode-level models, and `π₁,…,π_n` enumerate all legal deterministic history policies for a fixed finite horizon. Evaluate the cost matrix `C_ij=J_{F_i}(π_j)` using the same model throughout each trajectory. A policy can sample one full plan privately before the episode, using `λ∈Δ_n`; Nature knows `λ` but not its sampled realization.

Then fixed-model minimax loss is exactly

\[
\min_{\lambda,v}v\quad\text{s.t.}\quad C\lambda\le v\mathbf1,
\quad\lambda\ge0,\quad\mathbf1^T\lambda=1.
\tag{B18}
\]

This follows directly because expected costs under a private mixture are linear and the worst of finitely many models is their maximum. For minimax regret replace `C_ij` by `C_ij−min_k C_ik`. The complete deterministic history-policy list covers permitted behavioral randomization by pre-sampling the required independent action choices, under perfect recall and the stipulated seed access. Restricted memory or observable randomization changes that claim.

**Check.** Cost rows `(0,1)` and `(1,0)` have deterministic worst loss 1. A private half-half mixture has worst loss `1/2`; averaging the two model constraints proves no mixture can do better. If Nature sees the sampled plan before choosing its model, the value returns to 1.

This procedure is finite and exact but potentially enormous. It resolves constructibility for finitely listed models, not efficient general nonrectangular planning. Unlisted model families need a justified robust optimization oracle or other exact representation.

### 9.2 Why rectangularization changes the task

Consider two dates, no actions or informative observations, and one model selected once. Model A produces costs `(0,1)`; B produces `(1,0)`. Each trajectory has total cost 1, so fixed-model worst cost is 1. An adversary permitted to choose the first-date cost from B and the second-date cost from A obtains 2. Local rowwise maximization has silently enlarged the trajectory set.

For a deliberately rectangular fully observed model with independently selectable transition sets `U_t(x,a)`, compactness, and Nature moving after the current action, backward optimization gives

\[
V_t(x)=\min_a\left[g_t(x,a)+\max_{p\in U_t(x,a)}p^TV_{t+1}\right].
\tag{B19}
\]

Induction works because each chosen conditional continuation can be pasted into one admissible strategy of Nature. That pasting property is exactly what the fixed-model example lacks. [Iyengar (2005)](https://pubsonline.informs.org/doi/abs/10.1287/moor.1040.0129) is the established robust-DP foundation; only the finite rectangular specialization above is used here. The accessed publisher abstract confirms the scope; this is not a fresh audit of its full proof.

### 9.3 Bayesian persistence has a constructive state

With prior on a static model label `M` and hidden state `S_t`, keep
`b_t(m,s)=P(M=m,S_t=s|H_t)`. If model `m` has transition `P_m(s'|s,a)` and observation kernel `O_m(o|s',a)`, then

\[
b_{t+1}(m,s')\propto O_m(o_{t+1}\mid s',a_t)
\sum_sP_m(s'\mid s,a_t)b_t(m,s).
\tag{B20}
\]

Normalize only on positive predictive mass. This is Bayes applied to the augmented state, and yields a known-model belief process over `(M,S)`. Averaging the model kernels once and forgetting `M` generally loses the dependence and learning induced by persistence. A set of models supplies no prior over `M`; it cannot use (B20) without that additional input.

## 10. Add a statistical layer that survives repeated inspection

v1.1 conditions on supplied numerical models. To learn those models and keep checking decisions as data arrive, add explicitly time-uniform coverage. For an elementary finite profile, let `X₁,X₂,…` be IID categorical observations with `K` cells and true cell probabilities `p_j`. Define

\[
r_n=\sqrt{\frac{\log(2Kn(n+1)/\alpha)}{2n}},\quad
\mathcal C_n=\{p\in\Delta_K:|p_j-\widehat p_{n,j}|\le r_n\ \forall j\},
\quad0<\alpha<1.
\tag{B21}
\]

The two-sided bounded-variable concentration inequality of [Hoeffding (1963)](https://www.tandfonline.com/doi/abs/10.1080/01621459.1963.10500830) gives each cell/time failure probability at most `α/[Kn(n+1)]`. Summing over cells and all positive integers, using `Σ1/[n(n+1)]=1`, proves

\[
P(p\in\mathcal C_n\text{ for every }n\ge1)\ge1-\alpha.
\tag{B22}
\]

This simple construction is conservative. The established confidence-sequence literature supplies sharper methods under explicit assumptions; see [Howard et al., Time-uniform, nonparametric, nonasymptotic confidence sequences](https://arxiv.org/abs/1810.08240). This document uses the displayed elementary allocation rather than claim one of that paper's sharper boundaries has been implemented.

**Decision bridge.** If, for every `p∈C_n`, a selected policy has regret at most `ρ_n`, that certificate holds simultaneously at every inspection on the event in (B22). It remains valid at a data-dependent stopping time. Keep `ρ_n` in loss units and `α` as coverage failure probability. Do not add them.

For a finite channel with controlled access to labeled state rows, construct simultaneous row regions with a declared allocation of `α`. A valid row-sampling model is essential: hidden states do not magically supply labeled observations, and adaptive selection needs an appropriate sequential sampling argument. IID model drift, selection bias, missingness, and misspecified likelihoods are outside (B21).

This addition earns data-to-uncertainty-set construction and repeated inspection, but does not prove substantive model adequacy. Record the sampling design, observations used, cell definitions, allocation, and model assumptions. Event/time guarantees for a new environment need new support.

## 11. Add constraints, reachability, and tail risk

### 11.1 Expected loss is not enough for every task

Keep the decision criterion explicit. A consequential task may require

\[
\min_\pi E[C^\pi]\quad\text{subject to}\quad
P(\text{hit unsafe set by }T)\le\beta,
\quad E[D_k^\pi]\le b_k.
\tag{B23}
\]

These are different queries from minimizing expected terminal loss. A constraint is a supplied normative or operational requirement; probability theory does not choose its threshold.

For a fully observed finite MDP with stage constraints, occupancy masses `x_t(s,a)` satisfy

\[
\sum_a x_0(s,a)=\mu(s),\qquad
\sum_a x_{t+1}(s',a)=\sum_{s,a}x_t(s,a)P_t(s'\mid s,a),\quad x\ge0.
\tag{B24}
\]

Expected cumulative costs and resource constraints are linear in `x`. Recover `π_t(a|s)=x_t(s,a)/Σ_bx_t(s,b)` at positive occupancy; choose any legal action otherwise. Flow induction proves that this policy realizes the masses. Randomization may be necessary for constrained feasibility, even though it cannot improve an unconstrained known-model linear terminal optimum.

To handle hitting probability, augment the state with a bit recording whether the unsafe set has been visited. Terminal probability of bit 1 is then linear in terminal occupancy. This is a constructive finite path-property representation. Under partial observation the bit may itself be hidden, requiring beliefs or histories; the displayed fully observed LP cannot simply be reused.

**Composition requirement.** An abstraction used here must preserve the unsafe-set indicator, resource quantities, and relevant transition/history structure. Preserving only an expected-loss optimum does not preserve constraints. Separate failure probabilities for multiple hazards can be union-bounded, but doing so need not be exact and does not imply independence.

### 11.2 Tail objectives

For a specified finite loss distribution `Z` and `0≤α<1`, use

\[
\operatorname{CVaR}_\alpha(Z)=\min_{\tau\in\mathbb R}
\left[\tau+\frac{E[(Z-\tau)_+]}{1-\alpha}\right].
\tag{B25}
\]

Auxiliary slacks linearize this expression for finite fixed-probability scenarios. This is the established [Rockafellar–Uryasev formulation for general loss distributions](https://sites.math.washington.edu/~rtr/papers/rtr187-CVaR2.pdf), not a guarantee that arbitrary policy optimization with policy-dependent probabilities is convex. It handles atoms through the optimization definition, avoiding a naive conditional expectation at a quantile. At `α=0`, the displayed formula reduces to the mean.

**Check.** Action A costs 100 with probability `1/100`, otherwise 0; action B always costs 2. Expected loss favors A (`1<2`), while `CVaR_0.95(A)=20` and `CVaR_0.95(B)=2`. A representation retaining only means loses this distinction.

For sequential decisions, a terminal CVaR objective and a nested sequence of conditional risk operators are generally different criteria. To earn recursive risk planning, specify conditional monotone, translation-equivariant operators and the associated consistency/uncertainty structure, then derive the nesting. Do not relabel the ordinary expectation Bellman equation as a risk-sensitive theorem. This part remains an explicitly scoped next formalization, not a completed general risk calculus.

## 12. Make the causal interface partly constructive

### 12.1 Finite identified intervention risks

Take a supplied causal DAG and a valid pre-treatment adjustment set `Z` for action variable `A` and outcome `Y`. With consistency and positivity `P(A=a|Z=z)>0` for every relevant `z`,

\[
P(Y=y\mid\operatorname{do}(A=a))
=\sum_zP(Y=y\mid A=a,Z=z)P(Z=z).
\tag{B26}
\]

The back-door criterion is a sufficient graphical warrant: no descendants of treatment and all paths entering treatment blocked. The source foundation is [Pearl, The Mathematics of Causal Inference](https://ftp.cs.ucla.edu/pub/stat_ser/r416-reprint.pdf), equation (8). Given a finite accepted graph and distribution, checking the graphical criterion, support, and finite sums is constructive. The graph's substantive correctness is a separate assumption.

For declared loss `L(a,y)` and intervention cost `c(a)`, compute
`r(a)=c(a)+Σ_y L(a,y)P(y|do(a))`, then its minimizing set. **Derivation:** adjustment identifies each required outcome mass, and expectation is a finite weighted sum. Uniform intervention-law approximation in TV converts to action-risk error by the loss span; matched action coverage then gives the optimizer bound from §3.

This does not identify adaptive treatment strategies, counterfactual joint outcomes, or transport between environments. Those require their own sequential exchangeability/mechanism and support conditions. Exact causal abstraction also requires intervention-map coverage, as emphasized by [Beckers, Eberhardt, and Halpern](https://proceedings.mlr.press/v115/beckers20a.html).

### 12.2 Partial identification when point identification fails

For a finite SCM domain, enumerate permitted deterministic response types `r`, each specifying the required structural responses. Let `w_r` be their unknown population masses. Observed distributions imply linear constraints `Aw=b` because each type deterministically generates its corresponding observable event under the stated regime. A given intervention risk is `cᵀw`. Bound it using §4.

This is exact for the declared unrestricted joint response-type mixture. Independent exogenous noises or other structural restrictions can add nonlinear constraints; dropping them yields an outer bound, not the original causal fiber. Type enumeration can be exponential. Feasible witness types must respect the original causal assumptions before they establish nonidentification.

Action comparison can still succeed with intervals: solve the risk **difference** maxima as in (B8), preserving common-model coupling. Comparing independently attained marginal interval endpoints can be needlessly conservative. Nonidentification of a full intervention law does not itself imply nonidentification of the best action.

## 13. Add plural objectives and strategy when the problem requires them

### 13.1 Multiple objectives

Retain a vector of stakeholder or objective costs `J(π)=(J₁(π),…,J_k(π))`. Define domination by componentwise improvement with at least one strict improvement. The nondominated set is mathematically defined without inventing interpersonal weights. To select one answer, supply weights, lexicographic order, constraints, a bargaining rule, or another declared preference structure.

For positive weights, a weighted-sum minimizer is Pareto efficient: a dominating vector would have strictly smaller weighted sum. The converse fails without appropriate convexity/support assumptions. Thus a scalar representation can discard distinctions that later changes in preferences require. If a family of weight vectors is allowed, representation preservation must quantify over that family. Institutional authority and legitimacy remain inputs to the decision process; an optimum cannot establish them.

### 13.2 Endogenous other decision-makers

When another agent chooses actions or reports in response to incentives, replace an exogenous channel by a game. In a finite game with losses `L_i(a_i,a_{-i})`, a mixed Nash profile `σ` must satisfy

\[
E_\sigma L_i(A)\le E_{\sigma_{-i}}L_i(a_i',A_{-i})
\quad\forall i,a_i'.
\tag{B27}
\]

Checking a supplied profile is finite; finding one in general is a separate problem and does not imply uniqueness or selection. A two-player zero-sum finite game has an LP construction analogous to (B18). General-sum equilibrium constraints involve coupled products and need different methods.

For a joint recommendation distribution `q(a)`, correlated-equilibrium obedience is the finite linear system

\[
\sum_{a_{-i}}q(a_i,a_{-i})
[L_i(a_i,a_{-i})-L_i(a_i',a_{-i})]\le0
\quad\forall i,a_i,a_i'.
\tag{B28}
\]

This follows by multiplying the conditional no-beneficial-deviation inequality by the recommendation probability; zero-probability recommendations impose a vacuous constraint without requiring a posterior. It supplies a constructive feasibility profile once payoffs, recommendation access, and the equilibrium concept are specified. It does not describe play without a behavioral warrant.

For type-dependent reports, truthful reporting additionally needs incentive constraints of the form
`E[u_i(g(t_i,t_{−i}),t_i)|t_i]≥E[u_i(g(t_i',t_{−i}),t_i)|t_i]`, with the prior, information, outcome rule, and any transfers specified. A fixed source-reliability number cannot replace these premises.

These are elementary defining inequalities, included to earn a bounded interface—not a claim of a completed theory of institutions, strategic learning, or truthful communication. Established background for equilibrium computation and mechanism design is [Algorithmic Game Theory, chapters 3 and 9](https://www.cs.cmu.edu/~sandholm/cs15-892F13/algorithmic-game-theory.pdf). Preferences, equilibrium selection, participation, and incentives require separate records and empirical support.

## 14. Which additional structures are necessary, and in what order?

“Necessary” is relative to the next promised capability. No theorem makes every mathematical field mandatory for every decision.

| Capability to earn | Structure needed | What this draft earns | What remains |
|---|---|---|---|
| Check finite joins and uncertainty answers | Convex polytopes, dual certificates, fractional optimization | Explicit witness/bound procedures, §§4, 9 | Scalable exact treatment of nonlinear constraints |
| Find reusable decision representations | Equivalence relations, partitions, stochastic kernels, Bellman closure | Finite quotient and structural abstraction procedures, §5 | General efficient minimal sufficient representation discovery |
| Reuse approximations through time | Couplings, spans, nonexpansive operators, residuals | Signed-loss, conditioning, and sequential bounds, §§7–8 | Certified partial-observation applications with learned states |
| Update conclusions while collecting data | Concentration and time-uniform confidence sets | A finite IID construction and simultaneous decision bridge, §10 | Adaptive designs, dependence, drift, model criticism |
| Constrain harms and resources | Occupancy measures, reachability, risk functionals | Finite constraint and tail-risk interfaces, §11 | Full dynamic risk consistency and robust safety planning |
| Compare interventions | Causal identification and partial identification | Finite adjustment and response-type bounds, §12 | Sequential policies, transport, richer causal abstractions |
| Respect contested objectives | Partial orders and multicriteria optimization | Pareto and preference-family interface, §13 | Justified choice of aggregation and authority |
| Model responsive actors and reports | Game theory and incentive compatibility | Finite equilibrium/obedience checks, §13 | Equilibrium selection, learning, mechanism implementation |

The first three rows deepen the existing substrate immediately. The next three become necessary as Bellman promises learned models, harm constraints, and interventions. The final two become necessary when objectives and behavior cease to be those of one decision-maker facing exogenous uncertainty.

Measure-theoretic kernels, regular conditional distributions, measurable selection, and functional analysis become necessary for genuine continuous/infinite extensions; finite formulas do not acquire those guarantees automatically. Entropy, optimal transport, category theory, temporal logic, and sophisticated proof assistants may be useful for specified future problems, but none should be added solely as a unifying vocabulary. The finite constructions here already make substantial progress.

## 15. An integrated calculation

Let `θ∈{0,1}`, with unknown prior parameter `p=P(θ=1)∈[1/4,2/5]`. A supplied signal channel has `P(e|θ=1)=4/5` and `P(e|θ=0)=1/5`. Terminal actions predict `θ`, with zero-one loss. Treat this interval and channel as the exact declared model family for this example; any endpoint supplies a compatibility witness.

The event mass is `(1+3p)/5`, bounded below by `7/20`, so conditioning is defined throughout the family. Its posterior is

\[
q(p)=P(\theta=1\mid e)=\frac{4p}{1+3p},\qquad
q(p)\in[4/7,8/11].
\tag{B29}
\]

The derivative `4/(1+3p)^2` is positive, so the endpoints are attained extrema. Equivalently, the affine joint-mass constraints and conditional query admit §4's fractional optimization. The two endpoint witnesses establish that the posterior is not point identified.

Nevertheless, action 1 has conditional loss `1−q`, while action 0 has loss `q`. Their loss difference favoring action 1 is `2q−1≥1/7>0`. The **complete** optimal-action set is therefore `{1}` throughout the family. This is an identified decision with an unidentified probability, exactly the distinction the substrate should preserve.

If the interval is instead only a sound outer enclosure of a separately defined exact fiber, the same uniform action guarantee remains sufficient for its members. The differing endpoint posteriors then establish only outer variation unless both endpoints belong to the exact fiber; exact compatibility must still be established separately. If an interval comes from §10's sampling construction, its statistical coverage accompanies the action guarantee as a separate event, under the stated data-generating assumptions.

This certificate applies after the specified signal, for the specified losses and terminal choice. It does not decide whether acquiring the signal was worthwhile, whether further observations should be acquired, or whether a changed misclassification penalty preserves action 1. A representation may retain this action certificate for the exact covered query; a new query may need the posterior range or full family again.

## 16. Disposition of all eleven composition rules

| v1.1 rule | Assessment and next treatment |
|---|---|
| 10.1 Premise matching | Deserves formalization as typed partial contracts; §3 supplies a finite check/application distinction. |
| 10.2 Global compatibility | Highest-priority constructive gap; §4 supplies exact witnesses, separators, and a gluing theorem. |
| 10.3 Scope restriction | Universal-quantifier restriction is already adequate mathematics. Preserve nonemptiness and distinguish observation from restriction; no more elaborate calculus is needed. |
| 10.4 Exact transformations | Substitution is adequate; benchmark and policy-lift coverage deserve explicit treatment, supplied in §§3, 5. |
| 10.5 Approximation | Deserves deeper sequential derivation and solver certification; §§7–8 provide spans, residuals, and local-regret telescoping. |
| 10.6 Simulators | TV contraction is adequate; §6 supplies construction and the controlled online scope condition. |
| 10.7 Evidence context | Needs executable context checks, not just dominance vocabulary; §6 supplies them and a counterexample. |
| 10.8 Model identity | Deserves constructive persistent-model planning and a pasting argument; §9 supplies both. |
| 10.9 Conditioning | Needs quantitative amplification and constructive conditional bounds; §§4, 7 provide them. |
| 10.10 Coverage | Fixed finite union bound is adequate in its scope; §10 adds a data-to-model sequence valid under repeated inspection. |
| 10.11 Dependencies | Remains mostly a recording convention; §3 adds finite reassessment propagation without mistaking it for a truth or independence theorem. |

## 17. Concrete next mathematical work and evidence status

This draft completes an initial build-out: it supplies objects, finite procedures, assumptions, short proofs, and failure boundaries for the most immediate gaps. The next refinement should package four mathematical units with independent review:

1. **Compatibility and identified action:** (B4)–(B8), original-constraint witnesses, conditional extrema, and strict versus non-strict action certificates.
2. **Constructed representation and simulation:** (B9)–(B12), decoder/lift availability, timing, and counterexamples to enlarged contexts.
3. **Certified sequential choice:** (B13)–(B17), signed losses, support completion, conditioning, checked residuals, and replanning.
4. **Persistent uncertainty and empirical membership:** (B18)–(B22), exact policy mixtures, adversary timing, model-state filtering, and time-uniform statistical scope.

Each unit should be reviewed by checking its proof hypotheses, a positive witness, a decisive failed premise, and its boundary cases. Large parameter sweeps would not substitute for this work. Extension modules in §§11–13 can mature according to an actual decision need rather than an arbitrary demand to implement everything together.

**Validation status.** The companion `CHECKS.md` and `checks.json` record the small computations actually executed. They check arithmetic examples and one finite instance of residual/abstraction composition; they are not independent formal verification of every displayed proposition. The analytic proofs above remain reviewable derivations. External sources were consulted for the named established foundations; no claim is made to have re-audited every source theorem. Neither historical Bellman experiments nor Writ production tests were rerun.

**Preserved boundary.** A theorem about a supplied decision model establishes a conditional decision guarantee. It does not itself establish the model's truth, the legitimacy of its preferences, or authority to act. The useful expansion is to give each of those questions an explicit mathematical interface where justified, without pretending that one optimum answers them all.
