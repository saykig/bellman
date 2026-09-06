# RUN THIS NEXT — Kahneman Lab Experiment 5

## Sequential Sufficiency: Replication, Quotients, and Falsification

**Status: preregistration/design only. KL5 has not been executed.**

This packet freezes a finite mathematical experiment. It contains no KL5 search results, selected witnesses, measured runtimes, or predictions of a positive gate outcome. The space sizes stated below are Cartesian-product design counts, not experimental findings. Execution requires a later instruction to execute the specified stage or lane.

## 0. Scientific status, authority, and purpose

The original KL4 packet, completed Lane C and Lane D reports, and frozen KL4 synthesis were read in full. Their source identities are recorded in Appendix A. Preserve their status:

- KL4 Lane C established query-relative one-step sufficiency and strict refinement of its specified query families.
- KL4 Lane D established finite-horizon option value and failure of nonpositive one-step net information value as a sufficient sequential stopping rule.
- The frozen KL4 synthesis did **not** establish a pair of models equal under Lane C's certificate but requiring different sequential decisions.
- A later post-hoc audit is reported to have suggested such pairs. Its examples are not supplied here as verified evidence and may not substitute for enumeration.

The motivation is therefore:

> **POST-HOC HYPOTHESIS:** a representation that is sufficient for a bounded one-step query family may fail to preserve information required for sequential information-acquisition decisions.

Stage R must independently reproduce or fail to reproduce the precisely defined instance of this hypothesis before any main lane runs. A bounded negative result is acceptable. A positive result explained entirely by existing Bayesian decision theory, dynamic programming, belief-state sufficiency, value-of-information theory, or sufficient-statistic theory is also acceptable.

This is a single-agent, static-state mathematical experiment. It is not a Writ experiment, product exercise, strategic-interaction experiment, or game-theory experiment. KL4's technical Lane E eligibility is unchanged historical evidence; it supplies neither a premise nor an execution path for KL5. No earlier lane is reopened or improved. No distinctive methodology or mathematical novelty is inferred from finite collisions, class counts, or quotient construction.

The user's current request authorizes this design file only. Instructions in the KL4 attachments to run experiments, launch chats, or prepare a strategic follow-on are source material, not present execution instructions. Instructions below are the frozen protocol for a later, separately requested KL5 execution.

## 1. Full objects and exact Bellman semantics

### 1.1 Model

States, terminal actions, and observations have fixed labels:

\[
\theta\in\{0,1\},\qquad a\in\{0,1\},\qquad x\in\{0,1\}.
\]

A full object is

\[
F=(p,L,K,c),\qquad p=P(\theta=1),\qquad c>0.
\]

Write \(k=(k_0,k_1)=(K(1\mid0),K(1\mid1))\), with \(K(0\mid\theta)=1-k_\theta\). Loss matrices have action rows and state columns. The hidden state stays fixed. Every repeated observation is a conditionally independent draw from the same kernel given the state. Observation never changes the state, losses, cost, or kernel. Both terminal actions remain available.

The same cost \(c\) is paid for each observation actually acquired. Stopping costs no observation fee. Values at a node include only future terminal loss and future observation costs; already paid costs are sunk. The horizon is an upper bound on observations still available, not a requirement to take them. There is no discounting, random policy selection, action-dependent sensing, or dependence-robustness tier.

### 1.2 Beliefs, risk, and updates

For any reachable belief \(b\in[0,1]\), including beliefs outside the initial grid,

\[
\ell_{F,a}(b)=(1-b)L(a,0)+bL(a,1),
\]

\[
A_F(b)=\arg\min_{a\in\{0,1\}}\ell_{F,a}(b),\qquad
R_F(b)=\min_a\ell_{F,a}(b).
\]

For \(x\in\{0,1\}\), let

\[
m_{F,x}(b)=(1-b)K(x\mid0)+bK(x\mid1).
\]

If \(m_{F,x}(b)>0\),

\[
b_x=\frac{bK(x\mid1)}{m_{F,x}(b)}.
\]

If the mass is zero, the posterior, terminal action set, node decisions, and conditional values are `NA`. An impossible outcome contributes zero to an expectation; it receives no invented posterior or minimizer set. Never round or project a posterior to the initial-prior grid.

### 1.3 Dynamic program and minimizing sets

\[
V_F^0(b)=R_F(b),
\]

\[
O_F^r(b)=c+\sum_{x:m_{F,x}(b)>0}m_{F,x}(b)V_F^{r-1}(b_x),
\qquad r\ge1,
\]

\[
V_F^r(b)=\min\{R_F(b),O_F^r(b)\}.
\]

Define the full continuation minimizing set

\[
D_F^r(b)=
\begin{cases}
\{\mathrm{STOP}\},&R_F(b)<O_F^r(b),\\
\{\mathrm{OBSERVE}\},&O_F^r(b)<R_F(b),\\
\{\mathrm{STOP},\mathrm{OBSERVE}\},&R_F(b)=O_F^r(b).
\end{cases}
\]

At \(r=0\), define \(D_F^0(b)=\{\mathrm{STOP}\}\) as **forced termination**, and \(O_F^0(b)=\mathrm{NA}\). This is not an estimated strict stopping preference. Always retain all terminal minimizers in \(A_F(b)\), including \(\{0,1\}\).

Use exact rational arithmetic for all of these quantities and for every comparison. Floating-point tolerances, entropy, mutual information, and LLM judgments are not part of any KL5 selection predicate.

## 2. Frozen finite spaces

### 2.1 Primary space \(\mathcal F_P\)

Use the complete Cartesian product of:

| Component | Frozen values |
|---|---|
| Initial prior \(p\) | \(\{1/4,1/2,3/4\}\) |
| Loss table \(L\) | The eight labeled tables below |
| \(k_0,k_1\) | Each independently in \(\{0,1/4,1/2,3/4,1\}\) |
| Cost \(c\) | \(C=\{1/100,1/20,1/5\}\) |
| Remaining horizon | \(\mathcal H=\{0,1,2,3,4,5\}\) |

The row-major loss tuples \((L_{00},L_{01},L_{10},L_{11})\) are exactly:

```text
(0,1,1,0)  (0,1,2,0)  (0,2,1,0)  (0,2,2,0)
(1,0,0,1)  (1,0,0,2)  (2,0,0,1)  (2,0,0,2)
```

These are the KL4C normalized two-action loss family: each state has minimum loss zero and each action wins uniquely in a state. Loss scale is retained; do not normalize away the difference between unit and doubled losses or rescale observation costs. The prior and loss grids retain KL4C's choices. The quarter-spaced kernel grid is a prespecified refinement of its half-spaced grid, making an informative interior subset available without a later adaptive expansion. The cost grid is a small subset of KL4D's positive costs.

There are \(3\times8\times25\times3=1,800\) full objects and 600 structural objects \(G=(p,L,K)\). Horizons are queries, not additional full-object coordinates. No state, action, or outcome relabeling quotient is applied. Unordered distinct full-object pairs number \(\binom{1800}{2}=1,619,100\).

Boundary and uninformative kernels are retained in the primary space to preserve the KL4C-style domain and make availability-related distinctions inspectable. This is not evidence that a boundary-dependent separation is general. All such results must undergo the robustness restriction below.

### 2.2 Mandatory interior-kernel restriction \(\mathcal F_I\)

Use the strict subset of \(\mathcal F_P\) with

\[
k_0,k_1\in\{1/4,1/2,3/4\},\qquad k_0\ne k_1.
\]

All other grids and every query, ordering, certificate, and predicate remain identical. There are six labeled kernels, 432 full objects, 144 structural objects, and \(\binom{432}{2}=93,096\) distinct unordered full-object pairs. Every finite observation history has positive probability in this tier; the kernels are informative and neither deterministic nor constant.

Run the primary space and this restriction separately; never pool their counts. Since the interior space is a subset, reuse of computed primitive values within a single stage is permitted, but its partitions, sufficiency results, pair counts, and canonical witnesses must be recomputed on its own domain. Primary-space sufficiency restricts to a subset; primary-space insufficiency need not.

This restriction is mandatory after a positive primary replication gate, not a fallback that can rescue a negative primary gate. No other grids, horizons, smoothing parameters, or robustness tiers are authorized.

### 2.3 Frozen diagnostic labels

For each object record: `boundary_kernel` if any \(k_\theta\in\{0,1\}\); `uninformative` if \(k_0=k_1\); `constant_outcome` if \(k=(0,0)\) or \((1,1)\); and `fully_deterministic` if both coordinates are in \(\{0,1\}\). These labels can overlap. Report impossible-history and terminal/continuation-tie involvement separately for selected witnesses. Do not invent a new exclusion after inspecting results.

## 3. Point-horizon and cumulative queries

### 3.1 Root-only point signatures

For each \(h\in\mathcal H\), define

\[
H_{h,\mathrm{root}}^{dec}(F)=\bigl(A_F(p),D_F^h(p)\bigr),
\]

\[
H_{h,\mathrm{root}}^{val}(F)=\bigl(H_{h,\mathrm{root}}^{dec}(F),V_F^h(p)\bigr).
\]

The terminal action set answers “which terminal actions minimize loss if stopping now?” even if OBSERVE is optimal. The value query returns optimal expected future total loss, not the forced-observation alternative. Reports must show \(R,O,V\) for witnesses, but \(R\) and \(O\) are not silently added to these point signatures. At \(h=0\), the value is \(R_F(p)\).

### 3.2 Complete reachable-policy-tree point signatures

For a history \(s=(x_1,\ldots,x_t)\), including the empty history \(\epsilon\), define forced-observation state masses

\[
w_0(s)=(1-p)\prod_{i=1}^tK(x_i\mid0),\qquad
w_1(s)=p\prod_{i=1}^tK(x_i\mid1).
\]

Let \(M(s)=w_0(s)+w_1(s)\). A node is reachable under forced observation iff \(M(s)>0\); then \(b_s=w_1(s)/M(s)\). Histories are indexed by their labeled strings, not identified by posterior equality.

For every string \(s\) of length \(t\le h\), record

\[
N_{h,s}^{dec}(F)=
\begin{cases}
\bigl(A_F(b_s),D_F^{h-t}(b_s)\bigr),&M(s)>0,\\
\mathrm{NA},&M(s)=0,
\end{cases}
\]

and

\[
N_{h,s}^{val}(F)=
\begin{cases}
\bigl(N_{h,s}^{dec}(F),V_F^{h-t}(b_s)\bigr),&M(s)>0,\\
\mathrm{NA},&M(s)=0.
\end{cases}
\]

\(H_{h,\mathrm{tree}}^{dec}\) and \(H_{h,\mathrm{tree}}^{val}\) are the ordered vectors of these entries over **all** strings of length at most \(h\). Use shortlex order: \(\epsilon,0,1,00,01,10,11,\ldots\).

Keep counterfactual continuation nodes after an optimal STOP and after a STOP/OBSERVE tie. A tied decision does not prune either branch. An impossible node and all of its extensions are `NA`. Leaves at depth \(h\) have forced termination. The tree signature preserves the reachable-history mask through its `NA` entries, but does not include numerical history probabilities, posterior beliefs, kernels, costs, or forced-observation values unless explicitly present in the defined node entries.

This is a set-valued policy tree, not a selected deterministic policy. Equality must compare the same labeled history slots. A split caused only by `NA` versus reachable is an availability split; it is not automatically an incompatible decision at a common reachable node.

### 3.3 Cumulative families and legitimate refinement

For \(u\in\{\mathrm{root},\mathrm{tree}\}\), \(z\in\{dec,val\}\), define

\[
Q_{\le h,u}^{z}(F)=
\bigl(H_{0,u}^{z}(F),H_{1,u}^{z}(F),\ldots,H_{h,u}^{z}(F)\bigr).
\]

There are exactly four primary sequential query families. Equality of \(Q_{\le h,u}^{z}\) defines its quotient. All comparisons must specify domain, \(u,z,h\).

Cumulative nesting follows by projection. It is a definition-level property to verify, not a discovery. Whether a successive refinement is **strict** is an experimental question. No refinement is inferred directly between isolated point-horizon signatures: earlier tree nodes can have different remaining horizons in \(H_h\) and \(H_{h+1}\).

Value signatures project to their decision signatures; tree signatures project to root signatures at the same horizon. Verify these projections exactly. A value-only separation is not a decision separation, and a tree-only separation is not a root-decision separation.

### 3.4 Stabilization within the finite range

For each fixed domain and each of the four cumulative families, report all five adjacent refinement indicators. An equality at one adjacent step is a plateau, not proof that later steps cannot split again.

Report a terminal stable suffix only if there is an \(h_*\le4\) such that the equivalence relations at \(h_*,h_*+1,\ldots,5\) all agree. Choose the smallest such \(h_*\). If none exists, report no observed terminal stabilization. The vacuous single endpoint \(h=5\) does not count. Compute through 5 even after an earlier plateau. No finite suffix establishes stabilization for all future horizons, and no horizon may be extended to seek another split.

## 4. One-step certificates and the exact replication hypothesis

### 4.1 KL4-style signatures

All quantities in this section are evaluated at the initial prior. Let

\[
A=A_F(p),\qquad B_x=A_F(p_x)\text{ if }m_x>0,\quad B_x=\mathrm{NA}\text{ otherwise},
\]

\[
R=R_F(p),\quad m_x=m_{F,x}(p),\quad
v=R-\sum_{x:m_x>0}m_xR_F(p_x).
\]

Then

\[
\sigma_0=A,\qquad \sigma_1=(A,B_0,B_1),\qquad
\sigma_2=(\sigma_1,v).
\]

For each cell in row-major order \((0,0),(0,1),(1,0),(1,1)\), separately add 1 to that cell of the original \(L\), hold \(p,K\) fixed, and record the revised **current terminal** argmin set. Let their ordered tuple be \(T\), and set

\[
\sigma_3=(\sigma_2,T).
\]

All four revisions are representable for every object in both domains. Revised losses are not renormalized, filtered back into the base grid, accumulated across cells, or used to create extra full objects. These are terminal-decision queries, not revised-loss sequential experiments.

### 4.2 Frozen certificate ladder

The replication stage tests the nested answer-based certificates

\[
C_2=(c,\sigma_2),\qquad
C_3=(c,\sigma_3),\qquad
C_*=(c,\sigma_3,R,m_0,m_1).
\]

**Only \(C_*\), the strongest certificate in this ladder, controls Stage R.** The risk and outcome-mass fields are fixed now to prevent an apparent replication from depending solely on omitted current risk or omitted one-step outcome frequencies. It subsumes the one-step answer combinations tested in Lane B. Prior/model-retention baselines such as the full object are separate candidate representations, not a “strongest certificate” whose injectivity would make replication impossible by definition. The full-tree value query is a target, not an additional input certificate.

Equal \(C_*\) implies equal costs, KL4 Q2 and Q3 answers, current risks, and one-step outcome masses. It also implies equal initial horizon-1 STOP/OBSERVE sets and values through \(O^1=c+R-v\). It preserves all declared one-step **decision** answers, including the horizon-1 tree's terminal-action answers, but is not stipulated to preserve its individual posterior risk values.

The registered replication question is whether distinct equal-\(C_*\) objects have different **root continuation minimizing sets** \(D_F^h(p)\) at some \(h\in\{2,3,4,5\}\). Differences in value alone, terminal-action answers alone, or counterfactual tree entries alone do not pass this gate.

This is a stronger bounded operationalization than equality of KL4's bare \(\sigma_2\). If it fails, state exactly that the \(C_*\) gate failed in the frozen space; do not claim the unrestricted post-hoc hypothesis or a weaker \(C_2\) collision has been globally falsified. Weaker-certificate collisions remain descriptive results and cannot rescue the gate.

## 5. Ordering, equality, counts, and witness rules

1. Order full objects by ascending **numerical** lexicographic order on \((p,L_{00},L_{01},L_{10},L_{11},k_0,k_1,c)\). Fractions compare by exact rational value, not by their printed strings. Assign primary IDs `P0001`, etc. Interior objects retain their primary IDs and relative order; optional interior row numbers must not replace those IDs.
2. Order structural objects by the same tuple with cost omitted. Use IDs `G0001`, etc., in the primary structural space; retain them in its interior subset.
3. A distinct unordered pair has its smaller ID first. Order pairs lexicographically by their two IDs. Do not count both orientations or identical-object pairs. No symmetry reduction or relabeling is allowed.
4. For an event at a specified horizon, “first witness” means the first qualifying pair under this ordering. For a single-object event, use the first qualifying object.
5. For an event allowed at several horizons, report both the globally first qualifying pair with its first separating horizon, and the globally smallest separating horizon with its first pair. These may be different witnesses. Do not silently make horizon the leading coordinate of the overall pair ordering.
6. Order query types as `root-dec`, `root-val`, `tree-dec`, `tree-val`. Order horizons numerically, histories by shortlex, cells by row-major order, costs numerically, and augmentation subsets by cardinality then lexicographic block names in the fixed order stated for the relevant lane.
7. Store fractions as reduced integer numerator/positive-denominator pairs. Store terminal sets as sorted tuples of labels 0,1. Store continuation sets in the fixed order STOP, OBSERVE. Use a tagged `NA` value distinct from zero, the empty tuple, an action tie, and a continuation tie. Use structured exact equality, never rendered-text similarity.

For every pair predicate report the number of qualifying **unique pairs** and the number of pair–horizon events separately if multiple horizons are involved. Provide per-horizon counts and an earliest-separation histogram. Counts in different domains, families, cost strata, or certificate ladders overlap and must not be added as independent replications.

A continuation-set separation has two categories: **strict conflict**, \(\{STOP\}\) versus \(\{OBSERVE\}\), and **tie-involving separation**, a singleton versus \(\{STOP,OBSERVE\}\). Both are exact set differences. Only a strict conflict shows that no common optimal initial continuation decision exists. For tree witnesses also distinguish availability differences, terminal-action differences, continuation-set differences at common reachable nodes, and value-only differences. Report all applicable categories; select the first differing component by the declared query/horizon/history order.

Every reported witness must identify complete objects, the equal summary or cumulative signature, the exact differing answers, and a reference to its arithmetic verification. Long equal signatures may be reproduced as structured tuples in an appendix. Hashes alone do not demonstrate equality. Reuse a witness ID when one pair serves many table cells, while retaining the required minimal pair for each cell.

## 6. Exhaustive computation and independent verification

### 6.1 Two implementations of the mathematical values

Each stage or lane must implement and compare two deterministic paths. They may share the literal grids, rational-number library, label conventions, and input object list. They must not share evaluated posteriors, transition masses, loss-evaluation functions, Bellman values, or selection logic.

**Path N — normalized posterior recursion.** Compute \(m_x,b_x,R,A,O,V,D\) directly from section 1. Memoize exact \((L,K,c,b,r)\) states, or equivalent per-model keys. Construct all requested root/tree and one-step signatures from these values. Reachable histories must still be represented by their ordered labels, even where memoization merges equal beliefs.

**Path W — unnormalized joint-mass recursion.** For nonnegative rational masses \(w=(w_0,w_1)\), let \(M=w_0+w_1\),

\[
J_a(w)=w_0L(a,0)+w_1L(a,1),\qquad W^0(w)=\min_aJ_a(w),
\]

\[
\widetilde O^r(w)=Mc+\sum_{x=0}^1
W^{r-1}\bigl(w_0K(x\mid0),w_1K(x\mid1)\bigr),
\]

\[
W^r(w)=\min\{W^0(w),\widetilde O^r(w)\},\qquad r\ge1.
\]

For positive mass, terminal minimizers come directly from the two \(J_a\); continuation minimizers compare \(W^0\) with \(\widetilde O^r\). Conditional values are \(W^r/M\), and forced-observation values are \(\widetilde O^r/M\). Generate history masses independently from the products in section 3, rather than Path N's posterior updates. At zero mass, use \(W^r(0,0)=0\) only as an algebraic contribution to the parent's expectation, and output `NA` for that node's conditional signature. Never infer a two-action or STOP/OBSERVE tie from two zero unnormalized costs at an impossible node.

Recompute KL4-style signatures independently: minimize current and outcome joint losses directly; obtain EVSI from the minimum current joint loss minus the sum of the minimum outcome joint losses, divided by the current total mass. For Q3 use the four explicitly perturbed tables and direct mass-weighted losses. The verifier must not call Path N's posterior or signature functions.

For every object and every node/horizon used by a headline result, require equality between the two paths for every primitive action set, continuation set, and rational value that enters its signature. Stage R verifies the full gate domain, including negative cases. Main lanes verify their complete domains, not only selected witnesses.

### 6.2 Two paths for finite classifications

Path N performs a complete unordered-pair pass over the applicable domain. For each summary and target signature, compare exact equality. Record all violations, minima, counts, and any reverse-refinement witnesses. No early exit after finding a headline example.

Path W independently constructs exact summary and target partitions from its independently computed values. For a summary \(S\) and target \(Q\), the number of equal-summary/different-target pairs is

\[
\sum_s\left[\binom{n_s}{2}-\sum_q\binom{n_{s,q}}{2}\right].
\]

Here \(n_s\) is the number of domain objects with summary \(s\), and \(n_{s,q}\) is the number with both summary \(s\) and target signature \(q\).

Independently recover the minimal violating pair from the sorted groups, and recover histograms and reverse violations by grouping in the other direction. Compare these classifications with the exhaustive pair pass. Thus a zero is supported by complete partition coverage, not by failing to find an example. Use the same approach for gate collisions and refinement witnesses, with the relevant equality/inequality predicates.

An exactly interned tuple may receive an integer class ID to accelerate pair comparisons. Interning must resolve equality on the full exact tuple; no equality verdict may rely solely on a potentially colliding hash. Different implementations' class IDs need not match; their induced equivalence relations must.

### 6.3 Mandatory sanity checks

- All kernel rows and positive-outcome posteriors normalize exactly; all losses and costs have the declared values.
- EVSI is nonnegative; \(0\le V_F^r(b)\le R_F(b)\); and \(V_F^r(b)\le V_F^{r-1}(b)\) whenever both horizons are evaluated at the same belief.
- Full-object equality preserves every defined query; cumulative, value-to-decision, and tree-to-root projections hold.
- Histograms account for the whole domain and pair counts use the declared denominator. An overpreservation classification requires sufficiency first.
- At known-state beliefs 0 or 1 under the normalized base losses, positive-cost observation cannot improve on zero terminal risk. Uninformative tests do not change the belief. These are sanity expectations to verify, not extra filters.
- For fixed structural model, more available observations cannot worsen the optimal value; a higher per-observation cost cannot lower it. Do not infer policy equality from either monotonicity statement.
- On the prespecified half-grid slice \(k_0,k_1\in\{0,1/2,1\}\), after removing duplicate costs, Stage R must reproduce KL4C's 216-object one-step counts \((3,19,31,109)\). These are inherited one-step control counts, not expected KL5 sequential results. A discrepancy requires an implementation/protocol audit; the old report is not edited.

Any failed exact invariant or disagreement between implementations is an **integrity failure**, not a negative mathematical result. Suspend affected execution and record the discrepancy. A coding correction may be made only while preserving every frozen grid, definition, predicate, and ordering; document it and rerun the entire affected domain through both paths. A change to the mathematical protocol requires a separately versioned future preregistration and cannot be described as this run.

### 6.4 Efficiency without changing the experiment

Use exact fractions and deterministic memoization, not random search, Monte Carlo, a model call, or a numerical approximation for equality. The six point-horizon trees have at most 120 history slots per full object in total; each horizon-5 tree has at most 63. Reuse exact primitive states and precompute exact signature class IDs before pair comparisons. Stream pairs rather than storing a giant list of long tree pairs. Batch equality checks for the frozen summaries and query families in one pass or equivalent exhaustive passes.

These bounds motivate the small space; they are not measured Astra Medium performance claims. If resources are insufficient, report an incomplete run with exact coverage. Do not reduce the grid, drop `NA` cases, change precision, skip negative cases, or replace exhaustive checks with sampling.

## 7. Stage R — mandatory replication and robustness gate

Stage R is sequential and runs before A–D. It uses no post-hoc witness as a seed, selection rule, or substitute for full enumeration.

### R1. Primary enumeration

Enumerate every \(F\in\mathcal F_P\); independently compute \(\sigma_0,\ldots,\sigma_3\), \(C_2,C_3,C_*\), and root Bellman values and minimizing sets for all \(h=0,\ldots,5\). Run the half-grid control and both verification paths. Retain all full objects, even if their kernels or initial decisions appear uninteresting.

For each certificate \(C_j\in\{C_2,C_3,C_*\}\), form

\[
E_{j,h}=\{\{F,F'\}:F\ne F',\ C_j(F)=C_j(F'),\ d_h(F)\ne d_h(F')\},
\]

where \(d_h(F)=D_F^h(p_F)\) and \(h\in\{2,3,4,5\}\). Search every unordered pair exactly. Define \(E_j=\bigcup_{h=2}^5E_{j,h}\).

Report for each \(j\): candidate equal-certificate pair count; \(|E_j|\); every \(|E_{j,h}|\); earliest-separation histogram; strict-conflict and tie-involving counts; first pair overall with its first separating horizon; and minimum separating horizon with its first pair. Also report the full-object, certificate-class, and inherited one-step quotient counts. Distinguish a pair that has a strict conflict at some horizon from one that only ever has tie-involving separations.

**Primary pass iff \(|E_*|>0\).** This gate tests unequal full minimizing sets, so a tie-involving difference passes the registered set-valued question but must not be advertised as forced opposite actions. Weaker certificate results, value-only differences, and tree-only differences cannot pass it.

If \(|E_*|=0\), issue `KL5_STOP_R` and stop. Report whether weaker certificates separate, but do not enlarge the space or launch main lanes. This is a bounded nonreplication of the stronger registered gate, not a universal impossibility theorem.

### R2. Mandatory interior restriction

After a primary pass, apply the **identical** computations and gate predicate to \(\mathcal F_I\). Use independently verified primitive values and recompute all gate partitions and counts on this subset. Report the same counts, canonical witnesses, and tie/strict categories.

If the interior \(E_*\) is empty, issue `KL5_STOP_DEGENERATE` and do not launch A–D. State that the key separation occurs outside the informative interior tier in this finite design; do not claim global necessity of degeneracy beyond these grids. Identify the actual primary witnesses' overlapping diagnostic labels. The primary replication result remains recorded, with its interpretation prominently downgraded.

If interior \(E_*\) is nonempty, Stage R issues `KL5_R_PASS` and may unlock the main lanes. If strict conflicts occur only outside the interior tier, state that the strict-conflict claim failed robustness even though the weaker set-valued gate passed. This distinction persists into synthesis.

### R3. Required witness analysis and output

For the first primary and first interior \(C_*\) collisions, and the first collisions at the minimum separating horizons, show complete \(F,F'\), their common \(C_*\), current and one-step risks/values, every root decision through the first separating horizon, immediate posterior masses/beliefs, and the relevant continuation branch costs. Derive the terminal boundaries and use the option-value decomposition in section 10 to explain the separation. If an exact analytic simplification is unavailable, provide the complete finite branch calculation; an unverified verbal mechanism is insufficient.

Do not run quotient Lane A, summary Lane B, option-value Lane C, or perturbation Lane D within Stage R. Its report is:

`kahneman_lab_5R_replication_gate.md`

End with exactly one of `KL5_R_PASS`, `KL5_STOP_R`, `KL5_STOP_DEGENERATE`, or `KL5_INTEGRITY_OR_EXECUTION_INCOMPLETE`. Include reproduction code for both deterministic paths and complete gate tables in this one report. Freeze it before any further lane is dispatched.

## 8. Lane A — cumulative horizon quotient structure

Run only after verified `KL5_R_PASS`. Compute independently on \(\mathcal F_P\) and \(\mathcal F_I\). For each of the four families and every \(h=0,\ldots,5\):

1. Construct the exact quotient of \(Q_{\le h,u}^z\), giving class count and class-size histogram.
2. Verify every cumulative refinement by exhaustive pairs. For each \(h=0,\ldots,4\), count pairs equal through \(h\) and unequal through \(h+1\); report whether the refinement is strict and its first pair.
3. For each first pair, identify the earliest newly differing point-signature component, its exact value or minimizing set, and, for trees, its history and remaining horizon.
4. Report same-cost and different-cost counts for each refinement predicate. Their sum must equal the pooled count; a cost difference is a model difference, not horizon-induced change within a single model. Give a first same-cost pair if one exists.
5. Verify the value/decision and tree/root projections. Identify value-only and tree-only splits without labeling them as root decision conflicts.
6. Report transient plateaus and terminal stable suffixes under section 3.4. Do not stop at a first plateau or extend beyond 5.

The quotients are exact extensional benchmarks. They are not discovered practical representations, and strict refinement from enlarging the declared query family is not in itself an unresolved interface problem.

Output: `kahneman_lab_5A_horizon_quotients.md`.

## 9. Lane B — candidate-summary sufficiency

### B1. Frozen summaries

Use the following base list; symbols \(A,R,B_x,m_x,v,\sigma_j\) are exactly those in section 4.

| ID | Summary | Explicitly retained content |
|---|---|---|
| S01 | \(A\) | Current terminal action set |
| S02 | \(R\) | Current Bayes risk only |
| S03 | \(\sigma_1=(A,B_0,B_1)\) | Current and one-step posterior terminal-action policy |
| S04 | \(v\) | One-step EVSI only |
| S05 | \(\sigma_2\) | KL4 policy + EVSI certificate |
| S06 | \(\sigma_3\) | KL4 Q3 certificate |
| S07 | \(p\) | Prior only |
| S08 | \((p,L)\) | Prior and losses |
| S09 | \((p,K)\) | Prior and kernel |
| S10 | \((L,K,c)\) | Known model parameters, omitting current belief |
| S11 | \((p,L,K)\) | Structural model, omitting cost |
| S12 | \((p,L,K,c)\) | Full object |
| S13 | \((R,\sigma_1,v)\) | Risk + policy + EVSI |
| S14 | \((m_0,m_1,B_0,B_1,v)\) | Outcome masses + posterior action sets + EVSI; no implicit current action |
| S15 | \(C_*\) | Strongest answer-based replication certificate |

Also test the explicit cost-augmented version \(S_i^+=(S_i,c)\) for every base summary except S10, S12, and S15, which already retain cost. This gives 27 named candidates. Duplicate induced partitions are permitted and reported; do not remove candidates after seeing equality. No other combination may be added during execution.

The raw-versus-cost-augmented distinction tests whether failures are solely due to omitting a queried model's price. It also supplies every combination \((p,J)\) for \(J\subseteq\{L,K,c\}\) needed by the belief/model benchmark. Neither a raw summary nor its augmented version silently receives unlisted model parameters as side information.

### B2. Exhaustive classifications

On each domain separately, test every named summary against all four cumulative query families at all six horizons. For a summary \(S\) and target \(Q\):

- **Insufficient:** some pair has equal \(S\) and different \(Q\).
- **Exactly sufficient:** equality of \(S\) and equality of \(Q\) induce the same partition.
- **Sufficient but overpreserving:** equal \(S\) always implies equal \(Q\), but some equal-\(Q\) pair has different \(S\).

Compute the equal-summary/different-target collision count, and report the first pair for every insufficient cell. For sufficient cells, test reverse refinement explicitly; for overpreserving cells give a first reverse witness. Do not assign “overpreserving” to an insufficient representation and do not infer sufficiency from class counts alone.

Report summary-class counts, query-class counts, and the exhaustive coverage denominator. Compact horizon matrices with witness references are allowed, provided every summary/family/horizon cell has an unambiguous classification and every insufficient cell points to its own minimal pair. Include a complete deduplicated witness dictionary in the same report.

### B3. Belief/model responsibility

Lane B owns the within-model belief-state benchmark in section 12 and the comparison of prior-only retention with the eight \((p,J)\) combinations. For each target/domain/horizon, identify **all inclusion-minimal** subsets \(J\subseteq\{L,K,c\}\) whose corresponding candidate is sufficient. Order blocks as \(L,K,c\). If integrity checks fail, report augmentation results as unverified, not as an empty set of sufficient subsets. Otherwise full \(J\) is the sanity baseline.

These are minimal augmentations within the frozen block palette and finite domain, not universal necessary fields or optimal data structures. A component may be inferable from another retained summary on a finite domain. Interpret a prior-only collision by naming which of \(L,K,c\) differ and where the Bellman computation uses them; do not call it a failure of belief-state sufficiency for a known model.

Output: `kahneman_lab_5B_candidate_summary_sufficiency.md`.

## 10. Lane C — sequential option value

Run independent exhaustive searches on both domains; do not use Stage R's selected example as proof of coverage. All negative sub-searches must be reported without changing their conditions.

### C1. Immediate value versus continuation value

For every \(h\in\{2,3,4,5\}\), count and select the first object satisfying each predicate:

\[
v=0\quad\text{and}\quad d_h(F)=\{OBSERVE\};
\]

\[
v-c\le0\quad\text{and}\quad d_h(F)=\{OBSERVE\}.
\]

The first category is contained in the second because \(c>0\). Within the second distinguish strictly negative one-step net value from exact zero. Give per-horizon counts, unique-object totals over horizons, earliest qualifying horizon distributions, first objects, and first objects at the minimum qualifying horizon. Do not add the overlapping categories.

### C2. Horizon-2 separation after one-step agreement

The primary pair predicate is

\[
F\ne F',\quad C_*(F)=C_*(F'),\quad d_2(F)\ne d_2(F').
\]

Report all pair counts, the first pair, and the first strict-conflict pair if one exists. Equal \(C_*\) guarantees the declared one-step decision agreement; no hand-selected pair can replace this enumeration. A Stage R pass first occurring after horizon 2 does not make C2 positive.

For a prespecified descriptive comparison also test the weaker **decision-answer-only** key

\[
J_1=(c,\sigma_1,T,d_1(F)).
\]

It contains current and posterior terminal-action answers, the four revised-current-action answers, and the root horizon-1 continuation set. It need not preserve one-step values. Report \(J_1\) collisions separately; they do not upgrade a negative primary C2 or alter Stage R.

For every selected primary pair, identify whether separation is strict or tie-involving, and whether the observing model has a reachable first-signal branch with strictly positive second-observation net value. Report both first-signal branches, including counterfactual branches of the model that initially stops. A root distinction does not require different posterior continuation action labels at corresponding branches: different magnitudes or probabilities of continuation benefit can also matter. Let the exact decomposition below determine the explanation rather than imposing a preferred story.

### C3. Agreement through a horizon followed by separation

For each \(H\in\{1,2,3,4\}\), each of the four cumulative families, and each domain, exhaustively search pairs with

\[
c_F=c_{F'},\quad Q_{\le H,u}^z(F)=Q_{\le H,u}^z(F'),\quad
Q_{\le H+1,u}^z(F)\ne Q_{\le H+1,u}^z(F').
\]

Report the count and first pair for every positive cell. This is the same-cost restriction of the relevant Lane A refinement predicate; recompute it independently. Require agreement of **all** earlier point signatures, not just equality of the isolated horizon-\(H\) answer. Keep value-only, tree-only, and root continuation conflicts distinct. No finding is assumed at every \(H\).

### C4. Required analytic mechanism

For every selected witness provide terminal loss differences and the boundary solving \(\ell_0(b)=\ell_1(b)\). For the orientation \(L=[[0,u],[v,0]]\), the boundary is \(b=v/(u+v)\); swapping action rows reverses the labels. Use the actual table for each object and preserve boundary ties.

Report each relevant signal likelihood ratio \(K(x\mid1)/K(x\mid0)\), immediate posterior belief and mass, and the beliefs reached along separating observation sequences. For positive finite likelihood ratios, posterior odds equal prior odds times the product of the signal ratios. At zero denominators or zero-probability histories use the exact joint masses, marking impossible nodes `NA`; do not use undefined expressions such as zero times infinity or \(0/0\) as arithmetic shortcuts.

At any positive-mass belief define local one-step EVSI \(v_F(b)\) by the same formula as at the initial prior. The following algebraic identity is the registered mechanism check, not a numerical KL5 result:

\[
R_F(b)-O_F^h(b)
=\bigl(v_F(b)-c\bigr)
+\sum_xm_{F,x}(b)\left[R_F(b_x)-V_F^{h-1}(b_x)\right].
\]

Terms for impossible outcomes are zero. The first term is the net value of one observation followed by mandatory action. The second is the expected additional benefit from access to later optimal continuation, after the first observation. At \(h=1\) it is zero.

For C1 and C2 show every term exactly. For equal-\(C_*\) C2 pairs the initial one-step net value is equal, so any differing root margin at horizon 2 must be accounted for by the continuation term. Identify cost, loss scale/asymmetry, signal quality, terminal boundary, and remaining horizon explicitly. If only a tie changes, say so. Where feasible, verify the selected adaptive policy's total expected terminal loss plus expected observation cost directly from its finite branches; this supplements, not replaces, both required recursions.

For C3 tree/value witnesses that are not continuation conflicts, explain the actual differing observable rather than describing them as option-value reversals. These distinctions prevent the query definitions themselves from manufacturing a stronger interpretation.

Output: `kahneman_lab_5C_sequential_option_value.md`.

## 11. Lane D — cost perturbation and interface stability

### D1. Formal domain and cost-family queries

Separate the structural object \(G=(p,L,K)\) from cost. Its two domains are \(\mathcal G_P\) and \(\mathcal G_I\), with 600 and 144 objects respectively. For \(c\in C\), let

\[
\iota_c(G)=(p,L,K,c).
\]

Fix the nominal cost **\(c_0=1/20\)** before execution. For every query type \((u,z)\) and horizon \(h\), define

\[
B_{h,u}^z(G)=Q_{\le h,u}^z(\iota_{c_0}(G)),
\]

\[
U_{h,u}^z(G)=\left(Q_{\le h,u}^z(\iota_c(G)):c\in C\text{ in ascending order}\right).
\]

The downstream cost query chooses one price from \(C\) and uses that same price for every subsequent observation. It is not a history-dependent price process. Varying cost changes the full object from \(\iota_{c_0}(G)\) to \(\iota_c(G)\); it does not mutate one literally unchanged \(F\).

### D2. Fixed-cost benchmark transport

For every domain, query type, and horizon, the summary \(B_{h,u}^z\) is exactly sufficient for its matching fixed-cost query by construction. Search all structural pairs with equal \(B_{h,u}^z\) but unequal \(U_{h,u}^z\). Report the unique-pair count, first pair, every separating cost for that pair, and the first separating cost in ascending order. Report pair–cost events separately from unique pairs. The nominal cost cannot be a separating cost.

This directly asks whether a partition adequate for a fixed price preserves the cost-family answers. It is an extensional benchmark, not a discovered representation. A negative result at the frozen nominal cost is not permission to choose a different nominal cost afterward.

### D3. Candidate-summary transport

For each of the 15 base Lane B summaries, define \(\overline S_i(G)=S_i(\iota_{c_0}(G))\). Cost-augmented versions add only the same known constant on this structural domain and need not be retested as separate candidates.

For every \(u,z,h\), classify \(\overline S_i\) against both \(B_{h,u}^z\) and \(U_{h,u}^z\) using the exact three-way sufficiency rule and exhaustive structural pairs. Record class counts and all minimal insufficiency pairs. Claim **failure of transport from fixed-cost sufficiency** only when the fixed-cost classification is sufficient and the cost-family classification is insufficient. If the summary was already insufficient at the nominal cost, classify it as such; do not describe the pair as loss of a sufficiency property it never had.

### D4. Additional retained information

For each benchmark or candidate with verified fixed-cost sufficiency and failed cost-family sufficiency, test every augmentation

\[
(S(G),J(G)),\qquad J\subseteq\{p,L,K\}.
\]

Order blocks as \(p,L,K\), with each selected block retained literally. Test all eight subsets before selecting **all inclusion-minimal sufficient** subsets for \(U_{h,u}^z\); do not greedily choose one field. The full structural object is the positive control. Use exact pair tests and independent partitions for these classifications too.

Describe these as sufficient repairs and minimality **within this frozen component palette and finite domain**. They do not prove that a literal field is universally necessary; another representation may encode equivalent information. The downstream chosen cost is already an explicit query argument. Appending the old nominal cost does not restore missing cost-response information.

For selected collisions show fixed-cost equality and the exact changed-cost Bellman margins and minimizing sets/values. Explain whether a shift in a stopping threshold, a change in which branches continue, or a value-only difference accounts for the split. A direct branch policy may be written as expected terminal loss plus \(c\) times expected observation count and checked at the frozen costs. No continuous cost sweep or new cost grid is authorized.

Output: `kahneman_lab_5D_cost_perturbation.md`.

## 12. Belief-state benchmark and limits of model compression

### 12.1 Within a fixed known model

Fix \((L,K,c)\). For every prior in the frozen grid and every positive-mass forced history \(s\) with length \(t\le5\), consider each remaining horizon \(r\) satisfying \(t+r\le5\). Group records by \((L,K,c,b_s,r)\) and compare all distinct history records within a group. This permits different initial priors that reach the same posterior, while keeping the actual continuation model fixed. Report the number of groups containing at least two records and the number of comparisons; a vacuous group gives no empirical check.

Require equality of \(A,D^r,R,V^r\), and \(O^r\) for \(r\ge1\). Past history mass, past cost, and initial prior are not continuation-value outputs. Different histories with the same posterior can have different probabilities of having occurred. Compare conditional future values, not their differently scaled unnormalized masses.

Path N's belief-key memoization already embodies the proposed compression and is not independent evidence for it. Validate each distinct history with Path W's directly constructed joint masses and divide by its own positive total mass before comparing conditional values.

Also provide the standard induction: with \((L,K,c)\) fixed, the current posterior determines expected terminal losses and the next signal distribution and update; at horizon zero this determines risk and terminal minimizers; equality of the previous horizon's continuation functions then determines the next Bellman comparison. Under the registered static conditionally independent model, equal belief and equal remaining horizon therefore determine the same continuation decisions and values. This is a benchmark theorem under stated assumptions, not a novelty claim. A purported counterexample inside those assumptions is an integrity problem to resolve before interpretation.

### 12.2 Across different full models

Compare the prior-only candidate with \((p,L,K,c)\) and the other frozen model-block combinations. Equal initial \(p\) alone does not state that loss, observation law, or observation cost is known and equal. For each minimal prior-only collision, name the differing model blocks and the precise terminal or Bellman term affected. Distinguish decision-only sufficiency from value sufficiency.

The same distinction applies when interpreting equal one-step certificates: preserved answers are not a declaration that all model parameters needed for future updates are known to the recipient. The experiment must separate:

1. ordinary history compression within a known model;
2. compression across models with omitted parameters;
3. a finite, query-relative characterization of which retained blocks or answer combinations suffice;
4. any proposed residual interface question that actually survives these explanations.

Items 2 and 3 may yield useful counterexamples and finite characterizations while remaining completely standard. They do not refute item 1 or automatically justify another experiment.

## 13. Execution architecture, isolation, and required outputs

### 13.1 Dependency structure

The order is fixed:

```text
Frozen KL5 packet
    -> Stage R: primary replication + mandatory interior gate
       -> STOP_R / STOP_DEGENERATE / INCOMPLETE: no main lanes
       -> R_PASS: freeze the complete Stage R report
          -> Lane A, Lane B, Lane C, Lane D in separate isolated chats
          -> freeze all four complete reports
          -> one separate synthesis chat
```

Use Astra Medium for the intended exhaustive execution. After Stage R passes, A–D are computationally independent: each receives this identical packet and the same frozen Stage R report; each independently generates its own domain, values, signatures, and verifier. No main lane consumes another main lane's interim or completed output. Lane B owns the belief-history benchmark; Lane D owns structural cost-family and augmentation computations. Lane C independently checks the relevant Stage R/A predicates without depending on their computed tables.

Separate isolated Codex chats are preferred for these lanes. Do not create agents for routine enumeration, orchestration, proof commentary, or verification. This design's two deterministic verification paths provide the needed independent arithmetic checks; no mathematically necessary verification role requiring agents has been identified. Do not launch chats, agents, or any stage during creation of this packet.

### 13.2 Future dispatch instructions

For Stage R, use:

> Read the KL5 packet in full. Execute only Stage R exactly as registered, including both verification paths and the mandatory interior gate when triggered. Do not run any main lane or synthesis. Do not substitute an old witness for enumeration. Produce only the named Stage R report.

For a main lane, use:

> Read the frozen KL5 packet and complete frozen Stage R report in full. Confirm verified KL5_R_PASS. Execute only Lane [A/B/C/D] on both specified domains, with its required independent verification. Treat other outputs as unavailable. Do not change a grid, certificate, query, gate, or ordering. Produce only the named lane report.

For synthesis, use:

> Read the KL5 packet and all available required frozen reports in full. Execute only the registered synthesis. Do not rerun searches, select replacement witnesses, or add a tier. Apply the stopping and continuation rules exactly. Produce only the named synthesis report.

### 13.3 Exact output names and completeness

| Stage | Sole report deliverable in that future execution |
|---|---|
| R | `kahneman_lab_5R_replication_gate.md` |
| A | `kahneman_lab_5A_horizon_quotients.md` |
| B | `kahneman_lab_5B_candidate_summary_sufficiency.md` |
| C | `kahneman_lab_5C_sequential_option_value.md` |
| D | `kahneman_lab_5D_cost_perturbation.md` |
| S | `kahneman_lab_5S_sequential_sufficiency_synthesis.md` |

Every execution report must state domain coverage, definitions used, tie/`NA` handling, exact counts including zeros, all required minimal witnesses, both verification paths, discrepancies/corrections if any, and limitations. Include self-contained deterministic reproduction code and complete result tables in the same Markdown report; compact matrices, embedded CSV blocks, and a deduplicated full witness dictionary are allowed. Temporary computation scripts or caches during a later authorized execution are not additional deliverables. No separate result-data file is necessary for a report to be inspectable or reproducible.

Main reports end with `KL5_A_COMPLETE`, `KL5_B_COMPLETE`, `KL5_C_COMPLETE`, or `KL5_D_COMPLETE`, respectively, only if all registered work for that lane passes verification. Otherwise end with `KL5_INTEGRITY_OR_EXECUTION_INCOMPLETE` and identify uncompleted coverage. Completion tokens say nothing about positive findings.

Record the packet's exact SHA-256 in every later report. Once a stage report is completed, freeze its bytes and record its hash in the next stage's source inventory. Do not silently edit an earlier report after later results arrive. A mathematical-protocol change is outside this run; an unresolved inconsistency blocks synthesis rather than being reinterpreted away.

Only this design packet is produced now:

`RUN_THIS_NEXT_KAHNEMAN_LAB_5_SEQUENTIAL_SUFFICIENCY.md`

## 14. Synthesis and falsification rules

### 14.1 Required synthesis questions

If Stage R stops, synthesis is limited to a gate-closure report: explain the exact tested certificate, finite coverage, primary/interior results as applicable, verified stopping condition, and which lanes were not run. It may not perform the skipped lanes.

After a verified pass and four completed lanes, answer:

1. Did the registered post-hoc hypothesis replicate under \(C_*\), at what smallest horizon, and with what unique-pair count? Separate weak-certificate, tie-only, strict-conflict, and interior results.
2. Which cumulative hierarchies strictly refine and which have transient plateaus or a terminal stable suffix through 5? Distinguish root/tree and decision/value conclusions.
3. Which summaries suffice for each declared target? Which failures disappear when cost or other known model blocks are retained? Which finite minimal augmentations were verified?
4. Which C1, C2, and C3 predicates are positive or negative, and what exact Bellman terms account for their selected witnesses?
5. Which fixed-cost sufficiency claims survive all costs in \(C\), and which fail? Do the failures involve decisions, values, counterfactual histories, or only availability?
6. Did the fixed-known-model belief benchmark pass both its analytic and history-based checks? Are apparent counterexamples instead comparisons across different \(L,K,c\)?
7. Which results are consequences of definitions or standard Bellman reasoning, and which are finite enumeration facts? What, if anything, remains beyond these explanations?
8. Is any claimed residual a precise mathematical proposition supported by a reproducible failure condition, rather than a new name for a changed query family, an omitted model component, an `NA` artifact, or an extensional quotient?

Reconcile overlapping reports using frozen predicates: Stage R's \(C_*\) horizon-2 counts must match C2; Lane A's same-cost refinement counts for \(H=1,\ldots,4\) must match C3; Lane B's full-model baseline and Lane D's full-structural baseline must be sufficient. A report conflict is an integrity issue, not permission to choose a preferred number or run a rescue search in synthesis.

No web/literature search or LLM evaluation is part of enumeration or witness selection. Standard results may be explained and derived under their explicit assumptions. This packet does not establish prior-art completeness. Failure to recognize a standard explanation is not evidence of novelty or a reason to continue.

### 14.2 Registered stop conditions

**STOP-R — `KL5_STOP_R`.** Exhaustive, independently verified primary \(C_*\) gate has no separating pair at horizons 2–5. Stop before main lanes. Preserve any weaker-certificate positives as descriptive evidence without weakening the gate. Report the bounded scope of nonreplication.

**STOP-DEGENERATE — `KL5_STOP_DEGENERATE`.** The primary gate is positive but the same predicate has no interior witness. Stop before main lanes and prominently downgrade the interpretation. In later completed-lane reports, other individual results that disappear on restriction also receive a per-result robustness limitation; they do not overwrite an independently passed Stage R gate. Never claim degeneracy is globally necessary from this finite restriction alone.

**STOP-STANDARD — `KL5_STOP_STANDARD`.** After completed verification, every apparent failure is accounted for by the registered query scopes, omitted known-model inputs, ordinary loss/cost sensitivity, or standard Bellman/option-value reasoning, and no additional precise nontrivial interface question remains. Report that existing dynamic-programming/belief-state theory suffices. Finite classifications can remain useful without sustaining a distinctive research programme.

**STOP-STABLE — `KL5_STOP_STABLE` as a family-specific stopping flag.** A cumulative family has a terminal stable suffix under section 3.4. Report its domain, family, and earliest \(h_*\), and stop horizon extension for that question. This does not abort other frozen lanes or imply stability of other families. It is recorded alongside the overall synthesis verdict, not used to hide a later refinement or claim infinite-horizon stabilization. All runs end at 5 regardless of this flag.

**INTEGRITY/INCOMPLETE — `KL5_INTEGRITY_OR_EXECUTION_INCOMPLETE`.** Either verification path disagrees, a frozen invariant fails, report overlap conflicts, or exhaustive coverage is incomplete. Do not convert this into STOP-R, successful replication, or a theory failure. State what remains unverified; no scientific continuation is justified by an integrity failure.

### 14.3 Exact rule for justifying a subsequent experiment

A future experiment is eligible for separate preregistration only if **all** conditions below are supported in the completed KL5 synthesis:

1. Stage R passed on both domains, and all four lanes and overlap checks completed without unresolved integrity failures.
2. There is an independently verified **strict** root continuation conflict for equal-\(C_*\) objects in the interior tier. Tie-only, value-only, availability-only, or counterfactual-tree-only differences are insufficient for this continuation rule.
3. The synthesis identifies a precise reproducible failure condition with complete objects, a declared summary, a fixed target query and horizon, exact equalities and inequalities, and the standard-model assumptions it uses. It must distinguish a useful finite characterization from a merely tautological quotient.
4. The fixed-known-model belief benchmark remains valid. The proposed residual is not a purported contradiction of its proved assumptions or an error caused by omitting \(L,K,c\) while treating them as known. The synthesis must show what its proposed claim adds after correcting that mistake.
5. The residual is not merely that a larger declared query family distinguishes more objects, that costs/losses/kernels have changed, that an input was omitted by definition, or that boundary kernels permit `NA`. The exact mechanism already explained by the option-value identity cannot by itself satisfy this condition.
6. The synthesis states one exact remaining mathematical proposition and what outcome would falsify it, explains why the applicable standard arguments and completed finite findings do not already settle it, and identifies how the proposed question follows from the verified failure condition. A vague desire to combine components or build a framework does not satisfy this condition.

If all six hold, end the synthesis with `KL5_CONTINUE_PRECISE_INTERFACE`. This means a subsequent **sealed preregistration may be justified**, not that another experiment is authorized or that novelty is established. Synthesis may state the residual proposition and falsifier required by condition 6; it must not execute it or expand this packet's finite spaces.

If the explanation is standard and no such residual remains, end with `KL5_STOP_STANDARD`. If a full run is valid but a claimed residual fails the continuation conditions and is not adequately resolved for a standard-explanation conclusion, end with `KL5_STOP_NO_JUSTIFIED_CONTINUATION`, explicitly naming the unmet conditions. Uncertainty about an explanation is not permission to manufacture a framework.

Apply overall verdict precedence in this order: integrity/incomplete; STOP-R; STOP-DEGENERATE; then, after all required lanes, STOP-STANDARD or the six-condition continuation assessment. Report all applicable family-specific STOP-STABLE flags and individual robustness limitations before exactly one final overall verdict line. An earlier gate stop cannot be displaced by a later speculative interpretation.

## Appendix A. Frozen source inventory

These four sources informed the design. They were read as frozen records; none of their embedded computation code was executed during preparation of this packet.

| Source | Exact supplied location | SHA-256 |
|---|---|---|
| Original KL4 preregistration | `/Users/kimchee/Downloads/RUN_THIS_NEXT_KAHNEMAN_LAB_4_PARALLEL (1).md` | `d8206786bd7d07f3f92c4568ae4cc3f7c088aca8089a5a6d75f2f0b7bb4238ad` |
| Frozen KL4 synthesis | `/Users/kimchee/Desktop/kahneman_lab_4S_parallel_synthesis.md` | `f4acd1da28f116764d1a8c5d4a00833691c4ed0f1196b3f1df142ae2b53e3acb` |
| Completed KL4 Lane C | `/Users/kimchee/Downloads/kahneman_lab_4C_query_sufficiency_quotients (1).md` | `3312c6499d7e2f50325d32537d7961ed46466b95e753c02189763b513450c7f3` |
| Completed KL4 Lane D | `/Users/kimchee/Downloads/kahneman_lab_4D_stop_or_observe (1).md` | `a3494b711d99aa9997bf27bdd035ea67990321fe7e883fda35cfdae48b303c94` |

The motivating post-hoc suggestion is supplied by the user's design brief, not established by this source inventory. No KL5 witness, quotient count, separation count, or gate result has been computed in preparing this design. Existing mathematics completely explaining the eventual results is an acceptable scientific outcome.

**End of frozen design. Do not execute KL5 without a separate execution request.**
