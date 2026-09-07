# Bellman mathematical build-out — adversarial review

**Reviewed:** 7 September 2026.  
**Disposition:** Retain the mathematical development. Complete its certificate contracts and evidence package before treating its collection of constructions as implemented or jointly validated. No central displayed result was refuted in this review under its stated, appropriately matched premises. The next mathematical work is constructive completion, not a search for novelty or a wholesale restart.

## 1. Source and review boundary

The reviewed source is the complete uploaded `Pasted markdown(20260907-031855).md`, titled **Bellman: next mathematical build-out from Substrate v1.1**. Its SHA-256 is:

`af631b49c3e411c57dbbc7baa145bdcc337e26f0ac2eebf7fa508ba840111a2e`

It describes itself as an additive development draft, not a replacement v1.2. That status should remain explicit. It preserves the older experiment closures rather than claiming to have rerun them.

The mounted v1.1 has SHA-256:

`91f535d7010fa3bb4e4e1fdab6a1cebd3643f97666e5ba32240c81f264a8597e`

This matches the build-out's declared base. I also checked the bytes and lengths of all eight input entries in the available `BELLMAN_WRIT_NEXT_STEP_PACKET.zip` against its manifest. This establishes the identities of those available inputs, not what occurred in the author's workspace.

The author's message reports 18 check groups under Python 3.9.6. The actual new check script, `checks.json`, and standalone `CHECKS.md` were not recovered from the supplied files, mounted directories, available input archives, or targeted Project/conversation searches. The pasted check summary is available. Accordingly:

- The original 18-pass execution remains author-reported.
- Particular check claims such as the original Farkas vector, the residual bound `63/80`, and local regret `7/64` cannot be exactly replayed without their actual inputs and source.
- This is not evidence that those calculations are false.
- Python 3.9.6 is not, by itself, a mathematical defect. This work is not the separately versioned Build 1 runtime.

I wrote and executed a **new** standard-library reviewer harness under CPython 3.13.5. Nineteen groups passed normally and with `-O`, with identical group observations. One group checks archive integrity; eighteen contain mathematical example or contract checks. This is not 38 independent experiments, not a replay of the author's 18 groups, not a production test suite, and not formal verification. Exact vertex enumeration and policy enumeration were used only on fixed audit instances, not as a new research grid.

The harness and its outputs accompany this review. Source material was not changed. No repository write, push, merge, or production implementation was performed.

## 2. Overall mathematical judgment

This is a substantive improvement over a catalogue of theorem names. In particular, it supplies:

1. Explicit feasibility and infeasibility witnesses for a linear joint-law profile.
2. A valid fractional transformation for conditional questions.
3. Constructive finite representations and simulators, with appropriate limitations.
4. A signed-loss extension of the inherited coupling bound.
5. Valid Bellman-residual and local-disadvantage routes to whole-policy guarantees.
6. A correctly scoped persistent-model robust formulation and confidence-sequence construction.

The document generally distinguishes an implication from evidence that its premises hold. It is also careful about outer sets, causal versus observational quantities, optimizer output versus a certificate, and private versus observable randomization.

The main reservations are about **how far the constructive and validation claims have been earned**, not a discovered contradiction in these main formulas. Several sections reduce a problem to a finite optimization or equality test; that is legitimate constructive mathematics. It is not yet an executable, independently checked implementation of that reduction. The draft itself partly acknowledges this distinction; the next revision should make it systematic.

## 3. Priority findings and required treatment

### R1 — Finish the solver-facing certificate contracts

**Classification:** Constructive completion / verification coverage gap, not refutation of B4–B8 or B11.

Sections 4 and 6 correctly explain that a feasible point gives existence and a dual certificate can establish a bound. But the report does not completely specify, for its principal operation, what a receiver receives and checks for each outcome. “Solve two LPs” is a valid reduction; it is not the complete checkable mathematical interface the programme is trying to build.

For the finite joint-law profile, distinguish at least:

- A point satisfying the original constraints: a compatibility witness.
- A valid theorem-of-alternatives certificate: inconsistency of the stated linear constraints.
- A feasible query value: an attained value, not necessarily an extremum.
- A dual upper or lower bound: a certified enclosure, not necessarily attained.
- Matching primal and dual values: an attained exact optimum for that query.
- No checked witness or bound: no conclusion supplied by that computation.

Bind each certificate to the exact variable order, constraints, any relaxation map, conditioning event, query, action meaning, and guarantee type. This is mathematical subject matching; it does not require inventing a universal data schema.

For a concrete upper-bound contract, let

\[
\mathcal P=\{p\ge0:Ap=b,\ Cp\le d\}.
\]

Given free `y` and nonnegative `z`, check

\[
A^Ty+C^Tz\ge r.
\]

Then every feasible `p` satisfies

\[
r^Tp\le b^Ty+d^Tz.
\]

The proof is multiplication by nonnegative `p` followed by the original constraints. A lower bound is obtained by applying this construction to `−r` and negating its upper bound. Equality with an original feasible point certifies the extremum. A numerical status flag or small floating-point residual is not a replacement for these inequalities.

B5's infeasibility certificate is correct: the signs in its displayed contradiction are consistent. The review generated another exact Farkas witness for the binary triangle and rejected its sign-reversed version. This is a new reviewer witness, not the unavailable author's vector with objective `−1/2`.

### R2 — State the arithmetic domain of each constructive procedure

**Classification:** Missing executable-domain qualification; not a reason to restrict Bellman's mathematical theory to rationals.

Section 5.1 correctly requires terminating exact evaluators and decidable output equality. That discipline should also accompany the exact LP, partition, residual, and contextual-equality procedures. Finite state spaces do not by themselves specify how arbitrary real coefficients are represented or compared exactly.

For a first executable certificate profile, finite rational input data and rational primal/dual certificates are a clean choice. A symbolic or validated-interval profile can be added with its own rules. Keep the broader real-valued theorems as mathematics; do not silently advertise arbitrary-real exact computation.

B21 introduces logarithms and square roots. Its formula is mathematically valid under the IID categorical assumptions, but ordinary rational arithmetic does not evaluate those radii exactly. A future numerical procedure should supply a justified outward upper radius, or preserve a symbolic radius with an adequate checking method. Inward rounding may shrink the set and lose the stated coverage implication.

This is not a failure of B21 or a claim that all future calculations must use `Fraction`. It is the same distinction the substrate already makes between exact mathematical values and certified computed quantities.

### R3 — Complete the principal mathematical chain, including reuse and revision

**Classification:** Incomplete integration demonstration, not a false individual formula.

Section 15 is a useful integrated example, and its arithmetic is correct. It connects an exact prior family, a likelihood, conditioning, and an identified action despite an unidentified posterior. It does not yet demonstrate a complete certificate-producing and certificate-consuming operation, or the dependency reassessment proposed in §3.

The review went one step further: it constructed the example as an exact joint-law polytope, transformed the conditional query, enumerated its fixed vertices with rational Gaussian elimination, and checked primal/dual certificates for both extrema. It also certified the strict action comparison and supplied changed-loss and tie controls.

That is the natural next mathematical module to finish. It need not become a general compatibility engine. Its initial domain can explicitly be finite rational **linear joint-law constraints**, with other constraints preserved as outside that exact profile or as a labeled relaxation requiring an additional original-membership check.

The corrective example should distinguish a changed question from an invalid old calculation. Keep old premises and conclusions inspectable; refuse unsupported new reuse. It should also distinguish intersecting jointly asserted constraints from retaining competing models as alternatives. Disagreement does not make both conditional records useless.

The directed hyperedges in §3 are an abstract way to represent multi-premise derivations, not a reason to choose a hypergraph database. If an executable reassessment procedure is later specified, distinguish reachability from support: a cycle of mutually dependent claims is not an independent proof. An alternative derivation restores support only when its own premises and proof obligations remain warranted.

### R4 — Separate foundational extensions from the next implementation commitment

**Classification:** Scope / maturity clarification, not mathematical rejection.

Sections 11–13 introduce constraints, tail risk, causal identification, plural preferences, and game-theoretic interfaces. These are not all at the same stage. For example:

- The finite CVaR calculation is explicit and handles atoms correctly.
- The section expressly leaves dynamic risk consistency for later formalization.
- The adjustment formula is constructive given a valid causal graph and a supplied law; it does not validate that graph or eliminate statistical uncertainty in estimated inputs.
- Nash and correlated-equilibrium inequalities specify different concepts. They are not evidence of a strategic-decision engine or of actual behavior.

Preserve useful material as scoped extensions rather than making every field mandatory in the next build. In particular, no return to game-theory implementation follows from including §13; that would need an explicit subsequent direction decision. This keeps mathematics open without generating another four-lane execution programme.

### R5 — Preserve the actual verification source, not only its summary

**Classification:** Reproducibility / archival completion gap.

The reported checks are sensibly qualified. They still do not establish the claimed general procedures by their count. The coverage allocation example checks a finite sum, not statistical coverage empirically. A single transformed feasible point checks the coordinate transformation, not the extremum over its domain. An identity-to-noisy zero-deficiency example does not exercise positive deficiency or failure of exact simulation.

The new reviewer harness includes nonzero deficiency, negative controls, exact upper/lower certificates, zero-probability conditioning, ties, changed losses, nonzero transferred-policy regret, nonzero approximate-greedy regret, and fixed-model versus stagewise model selection. These strengthen example coverage without becoming a general proof.

Archive the author's original script, literal inputs, compact outputs, and runtime record when available. Do not reconstruct missing source and call it original. The user's returned task explicitly reports no branch, commit, or push; mathematical delivery and repository publication therefore remain separate outcomes. Finish the previously requested archival PR using the genuine artifacts, without rewriting old source versions or making a local-only deliverable the final archive.

## 4. An optional mathematical improvement found during review

### A sharper version of B15, with no stronger probability premises

**Classification:** Reviewer-derived strengthening of a valid conservative bound. No novelty claim. Not a correction of a false theorem.

The draft proves

\[
\operatorname{TV}(P(\cdot\mid e),Q(\cdot\mid e))\le\min(1,2\varepsilon/\kappa)
\]

when both event masses are positive, `TV(P,Q)≤ε`, and `P(e)≥κ>0`. This is valid.

In the same finite setting, a stronger inequality is

\[
\operatorname{TV}(P(\cdot\mid e),Q(\cdot\mid e))
\le \min\left(1,\frac{\operatorname{TV}(P,Q)}{\max\{P(e),Q(e)\}}\right)
\le\min(1,\varepsilon/\kappa).
\tag{R1}
\]

**Proof.** Put `a=P(e)`, `b=Q(e)` and `Δ=TV(P,Q)`. By symmetry assume `a≤b`. Write the restricted L1 discrepancy as `D_e=Σ_{ω∈e}|P_ω−Q_ω|`. The discrepancy outside `e` is at least `b−a`, so

\[
D_e\le2\Delta-(b-a).
\]

The common unnormalized mass inside the event consequently satisfies

\[
\sum_{\omega\in e}\min(P_\omega,Q_\omega)
=\frac{a+b-D_e}{2}\ge b-\Delta.
\]

Since `a≤b`, the normalized common mass is at least

\[
\sum_{\omega\in e}\min(P_\omega/a,Q_\omega/b)
\ge\frac1b\sum_{\omega\in e}\min(P_\omega,Q_\omega)
\ge1-\Delta/b.
\]

Total variation of two normalized distributions is one minus their common mass. This proves the first inequality, with the trivial bound 1 added. The second uses `max(a,b)≥P(e)≥κ` and `Δ≤ε`.

Positivity of `Q(e)` remains necessary for its conditional law to exist; it follows from `ε<κ` when not already supplied. If neither positive mass is established, no conditional certificate follows.

**Sharp fixed example.** Let the first three atoms constitute `e`, and set

\[
P=(1/10,3/20,0,3/4),\qquad Q=(0,3/20,1/10,3/4).
\]

Both event masses are `1/4`, joint TV is `1/10`, and conditional TV is `2/5`. The draft's radius is `4/5`; R1 gives the attained `2/5`. The factor 1 is therefore sharp for this profile.

A conditional loss expectation with common span `D` can use `D min(1,ε/κ)` under these same hypotheses. This does not establish a policy-transfer or changed-model guarantee without that guarantee's other premises. Nor does it remove rare-event instability: setting the event mass equal to the discrepancy still permits conditional TV 1.

This result is suitable for separate proof adjudication and, if retained, a new explicitly attributed revision. Do not silently overwrite B15 in the frozen draft or present a tighter bound as evidence that B15 was wrong.

## 5. Exact constructive verification of the integrated example

Use atom order

`(theta=0,not-e), (theta=0,e), (theta=1,not-e), (theta=1,e)`.

For joint mass vector `x`, the source example is exactly represented by

\[
\mathbf1^Tx=1,\quad -x_0+4x_1=0,\quad -4x_2+x_3=0,
\]

\[
x\ge0,\qquad 1/4\le x_2+x_3\le2/5.
\]

Condition on `e` and put `w=x/P(e)`, `t=1/P(e)`. In variable order `(w0,w1,w2,w3,t)`, use equalities

\[
\widetilde A=
\begin{pmatrix}
1&1&1&1&-1\\
-1&4&0&0&0\\
0&0&-4&1&0\\
0&1&0&1&0
\end{pmatrix},\quad
\widetilde b=(0,0,0,1)^T,
\]

and inequalities

\[
\widetilde C=
\begin{pmatrix}
0&0&-1&-1&1/4\\
0&0&1&1&-2/5
\end{pmatrix},\quad \widetilde d=(0,0)^T.
\]

All five variables are nonnegative. Normalization and the event equation force `t>0`, so inverse recovery is valid; this avoids a zero-scaling issue present in more general fractional formulations.

The reviewer finds exactly two vertices:

\[
(12/7,3/7,1/7,4/7,20/7),\qquad
(12/11,3/11,2/11,8/11,25/11).
\]

The posterior query is `w3`. Its exact bounds are `4/7` and `8/11`. The compact output supplies the independently checked dual vectors. For the upper bound `8/11` they are

`y=(-8/55,-8/55,3/55,8/11)`, `z=(0,4/11)`.

For the upper bound `−4/7` on the negative query they are

`y=(4/35,4/35,-3/35,-4/7)`, `z=(16/35,0)`.

These give feasible upper-bound inequalities and match feasible vertex values. Thus the review establishes extrema rather than only checking the source's two endpoint substitutions.

For zero-one prediction loss, action 1 minus action 0 has conditional risk `w1−w3`. Its checked upper bound is `−1/7`; action 1 is therefore strictly optimal throughout the family.

Two important negative controls pass:

- Changing the false-positive loss from 1 to 2 gives endpoint risk differences `2/7` and `−2/11`. Different admissible models then favor different actions. The original result is not false; the new query is outside its old guarantee.
- Enlarging the prior family to include `p=1/5` yields a tie at that endpoint. The common-optimal-action claim survives, but the uniform strictness claim does not.

When the conditioning event is impossible throughout a nonempty family, the transformed constraints are infeasible; the review does not manufacture a conditional answer.

## 6. Formula-by-formula disposition

| Draft item | Review disposition and boundary |
|---|---|
| B1–B2, typed contracts | Valid implication/substitution rule. Applicability is not automatically decidable from this notation. |
| B3, lift regret | Valid with uniform cost comparison and benchmark coverage. The review confirms that omitting coverage can leave error zero but regret 100. |
| B4–B5, joint-law profile and Farkas | Valid for the stated linear system. A nonlinear original constraint cannot be silently dropped and still call the result exact. |
| B6, positive gluing | Valid with matching separator marginals, normalized nonnegative inputs, and zero-support handling. It establishes one extension, not the true dependence law or uniqueness. |
| B7, conditional LP | Valid in this normalized probability profile. Positivity and inverse recovery are justified; actual extrema need certificates or another exact method. |
| B8, common action | Valid over the nonempty exact set with the same query and actions. Strict comparisons exclude the action's comparison with itself. Outer certificates are sufficient, not necessary. |
| B9, finite quotient | Correct coarsest deterministic answer-preserving quotient for supplied finite evaluators and decidable equality. Not structural compression discovery. |
| B10, backward partition | Correct finite structural abstraction. It is not the coarsest value-only quotient. Supply an exact numeric/equality profile for executable claims. |
| B11, deficiency LP | Correct epigraph formulation with a state-independent stochastic simulator. A feasible simulator proves an upper bound, not optimal deficiency. |
| B12, context equality | Correct on positive `(x,z)` support; that support implies positive `(y,z)` mass. A fitted law is not a universal model-family certificate. |
| B13, signed stopping bound | Valid under common prior, stationary conditionally independent channels, common fee/losses, and total policies. Forced-observation values apply only at positive horizon. The explicit zero-horizon bound concerns stop-only costs. |
| B14, controlled value bound | Correct fully observed induction. Do not import a partially observed or whole-policy guarantee without its additional premises. |
| B15, conditioning | Valid but conservative. Optional R1 above improves its constant under the same premises. |
| B16, residual certificate | Correct for the same model and the same backup-greedy policy, with terminal residual included. Approximate-greedy error is additional. |
| B17, regret telescoping | Correct under the actual policy trajectory and exact optimal continuation for the same task, with matched terminal cost. Unrelated local value differences cannot be added. |
| B18, robust policy mixture | Correct with the complete feasible policy menu, stated perfect recall, and a private seed hidden from Nature when it selects the fixed model. |
| B19, rectangular DP | Correct in its explicitly rectangular, fully observed, compact nonempty uncertainty profile and move order. Not equivalent to fixed-model ambiguity in general. |
| B20, persistent-model filter | Correct Bayes update for the supplied transition/observation model. All actually informative observations must be represented in the history/kernel. |
| B21–B22, confidence sequence | Correct union-of-Hoeffding construction for a fixed finite IID categorical model and stated alpha allocation. It is frequentist simultaneous coverage, not a posterior probability of the model. |
| B23–B24, constraints/occupancies | Correct fully observed flow construction with a consistent time/terminal convention. Hidden path indicators cannot be exposed to a partially observed controller. |
| B25, CVaR | Correct optimization definition, including atoms and the mean at alpha=0. Static terminal CVaR and nested conditional risk are not the same objective. |
| B26, adjustment | Correct conditional on a valid adjustment set, causal assumptions, positivity, and the appropriate observational law. Estimation uncertainty is a separate layer. |
| Response-type bounds, §12.2 | Correct for the declared unrestricted joint mixture; independent-noise restrictions can be nonlinear. Attained counterexamples must satisfy original causal constraints. |
| Pareto argument, §13.1 | Correct for strictly positive weights. Selecting weights or authority is not provided by efficiency. |
| B27–B28, equilibria | Correct defining inequalities for their distinct information and randomization concepts. Finite formulas are not a general exact equilibrium solver for arbitrary real inputs. |
| B29, integrated example | Correct. Exact original-model witnesses and primal/dual bounds were additionally constructed in this review. |

This is a mathematical reading and fixed-example audit, not formal proof validation of all general results. Retain premises at point of use rather than pretending an already stated premise was absent.

## 7. Review execution and source cross-checks

The new `reviewer_checks.py` uses rational arithmetic, exact Gaussian elimination, bounded vertex enumeration, and independent fixed-policy evaluation. It imports no Writ or Decision Lab runtime and does not implement a production LP solver.

Selected executed coverage:

- Eight packet byte identities and the declared v1.1 base.
- Triangle incompatibility and exact Farkas sign check.
- Positive gluing and two extensions with different downstream answers.
- A false original-membership witness created by dropping independence.
- Exact conditional extrema, positive scaling/inverse, dual witnesses, and forged-certificate refusal.
- Common action, strictness, changed loss, tie, and impossible-conditioning controls.
- Nonzero deficiency `1/2` with a matching universal lower-bound argument.
- Thirty-eight complete deterministic stopping policies on one fixed two-observation signed-loss instance.
- Off-support legal completion and strictly positive transferred regret `1/200` within its bound.
- The optional sharp conditioning bound, including equal and unequal event masses.
- Structural abstraction on one three-state finite MDP and 512 deterministic Markov plans for that fixed problem.
- Controlled value transfer, residual bounds, and exact regret telescoping.
- A separate positive approximate-greedy regret control: regret `1/10`, bound `1/5`.
- Private robust mixing, fixed-model versus rectangular cost, and persistent versus resampled observations.
- The first-100 alpha allocation identity and a generic inward-rounding counterexample.
- CVaR atom handling, constrained randomized feasibility, and observational versus interventional probabilities in a supplied causal model.

These are correlated, deliberately selected audit checks, not statistical sample sizes. The Python test count does not measure the number of theorems established.

### Primary-source spot checks

The review inspected the relevant primary-source material, not the entirety of each source:

- **Boyd and Vandenberghe, _Convex Optimization_:** §4.3.2 (printed p.151) for the fractional transformation; the theorem-of-alternatives/duality material for context. The displayed Bellman-specific inequalities were also checked algebraically. Source: `https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf`.
- **Givan, Dean, and Greig, _Equivalence Notions and Model Minimization in Markov Decision Processes_:** theorem 7 and §4.2 for structural quotient preservation and partition refinement. The finite-horizon specialization was checked by backward induction, not attributed verbatim to the paper. Source: `https://cs.brown.edu/people/tdean/publications/archive/GivanetalAIJ-03.pdf`.
- **Rockafellar and Uryasev, _Conditional Value-at-Risk for General Loss Distributions_:** the general-distribution minimization formulation and treatment of atoms. Source: `https://sites.math.washington.edu/~rtr/papers/rtr187-CVaR2.pdf`.
- **Pearl, _The Mathematics of Causal Inference_:** Definition 3 and equation (8), in parsed source text. The attempted PDF screenshot failed, so no visual inspection of its causal diagram is claimed. Source: `https://ftp.cs.ucla.edu/pub/stat_ser/r416-reprint.pdf`.
- **Subramanian et al. (2022), approximate information states:** official JMLR abstract for the distinction between a recursively valid information state and arbitrary hidden-state compression. No full-paper re-audit in this turn. Source: `https://jmlr.org/papers/v23/20-1165.html`.
- **Howard et al., confidence sequences:** author arXiv record and abstract for the time-uniform guarantee concept. B21–B22 use the draft's elementary allocation argument, not an implementation of their sharper boundaries. Source: `https://arxiv.org/abs/1810.08240`.

No full fresh proof audit of Hoeffding's original publication, Iyengar's full article, or the cited game-theory textbook is claimed. The finite statements actually used were checked from their displayed assumptions and algebra; uncertainty about wider source scope must not be replaced with an invented literature gap.

## 8. Recommended next disposition

Keep v1.1 unchanged and preserve this draft as an additive development artifact. A focused follow-up should adjudicate R1–R5, consider the optional sharper conditioning proof, and finish the finite joint-law / conditional-action certificate module. It should incorporate the exact example and failure controls already supplied rather than launch another grid or commission four new audits.

Bellman's broader mathematics remains active. This selects one immediate construction; it does not make the current Python implementation a ceiling. The next engineering integration should implement a reviewed mathematical operation, not automatically all topics named in this draft.

The archival stage is still needed: genuine source/check files, compact results, this review, and an honest ledger entry belong in the Bellman repository. Publication is not mathematical acceptance. Preserve the user's no-merge boundary and the original frozen artifacts.
