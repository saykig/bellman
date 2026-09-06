# Kahneman Lab Experiment 5 — Stage R Replication Gate

## Result

**The primary gate passes, but the mandatory interior gate fails. The registered Stage R verdict is `KL5_STOP_DEGENERATE`.**

The exhaustive primary search finds **64 distinct unordered pairs** equal under the strongest registered certificate \(C_*\) but with different root STOP/OBSERVE minimizing sets at some horizon 2–5. All 64 have a strict conflict at at least one horizon. The smallest separating horizon is **2**. The lexicographically first pair is **P0100/P0106**, which also separates at that smallest horizon.

On the mandatory informative interior subset, **none of the 144 equal-\(C_*\) candidate pairs separates** at any registered horizon. This negative result is supported by both the exhaustive pair pass and independent partition verification. Weaker certificates still separate in that subset; the frozen protocol explicitly prevents them from rescuing the \(C_*\) gate.

Only Stage R was executed. No main lane, synthesis, strategic experiment, additional tier, or horizon extension was run. No old witness was used as a seed or substituted for enumeration. There was no literature search or mathematical-novelty claim. This is the sole report deliverable.

## 1. Protocol identity and scope

The complete packet was read from:

`/Users/kimchee/Desktop/RUN_THIS_NEXT_KAHNEMAN_LAB_5_SEQUENTIAL_SUFFICIENCY.md`

Its SHA-256 is:

`43bf13e830d72fac72a36f18197b68d3e9465c8692ff9e69370512f88d7636d1`

The current user request authorizes Stage R. The packet's earlier design-only statements describe its creation status, while its main-lane and synthesis instructions remain contingent procedures outside this execution. The grids, strongest certificate, pair ordering, tie rule, and interior stopping rule were preserved exactly.

The motivating C×D statement remains a post-hoc hypothesis relative to frozen KL4. This run supplies a new, bounded KL5 result; it does not retroactively convert that hypothesis into an established KL4 finding.

The full object is \(F=(p,L,K,c)\), where \(p=P(\theta=1)\), state/action/outcome labels are 0,1, and \(k=(K(1\mid0),K(1\mid1))\). Loss matrices have action rows and state columns. The static state and conditional independence of repeated draws from the same kernel are fixed assumptions.

| Component | Frozen primary values |
|---|---|
| Prior | \(1/4,1/2,3/4\) |
| Row-major loss tuples | `(0,1,1,0)`, `(0,1,2,0)`, `(0,2,1,0)`, `(0,2,2,0)`, `(1,0,0,1)`, `(1,0,0,2)`, `(2,0,0,1)`, `(2,0,0,2)` |
| Each kernel coordinate | \(0,1/4,1/2,3/4,1\) |
| Cost | \(1/100,1/20,1/5\) |
| Remaining horizon | \(0,1,2,3,4,5\) |

The interior restriction uses \(k_0,k_1\in\{1/4,1/2,3/4\}\) with \(k_0\ne k_1\), leaving the other coordinates unchanged. It was executed because the primary \(C_*\) gate passed. Its primitive values were reused from the independently verified primary computations, as permitted; its partitions, candidate pairs, counts, and minima were recomputed on the restricted domain.

Full-object IDs follow ascending numerical lexicographic order on \((p,L_{00},L_{01},L_{10},L_{11},k_0,k_1,c)\). Interior objects retain their primary IDs. All pairs are distinct and unordered, with the smaller ID first. No relabeling quotient was applied.

## 2. Registered quantities and gate predicate

At a belief \(b\),

\[
R_F(b)=\min_a\bigl((1-b)L(a,0)+bL(a,1)\bigr),\qquad
V_F^0(b)=R_F(b),
\]

\[
O_F^h(b)=c+\sum_{x:m_x>0}m_xV_F^{h-1}(b_x),\qquad
V_F^h(b)=\min\{R_F(b),O_F^h(b)\}.
\]

The terminal argmin set \(A_F(b)\) and full continuation argmin set \(D_F^h(b)\) were retained exactly. At horizon zero, STOP is forced, not an estimated strict preference. An impossible outcome has posterior, conditional values, and action/continuation answers `NA`; its weighted contribution is zero.

At the initial prior, \(\sigma_1\) contains current and both posterior terminal-action sets, \(\sigma_2=(\sigma_1,EVSI)\), and \(\sigma_3=(\sigma_2,T)\). Here \(T\) records the four revised-current-action answers from separately adding 1 to each original loss cell in row-major order. No revision is renormalized or filtered back into the base loss grid.

The three tested certificates are

\[
C_2=(c,\sigma_2),\qquad C_3=(c,\sigma_3),\qquad
C_*=(c,\sigma_3,R_F(p),m_0,m_1).
\]

For each certificate and \(h=2,3,4,5\), the event is equal certificates and unequal **root continuation minimizing sets**, \(D_F^h(p_F)\ne D_{F'}^h(p_{F'})\). The total counts unique pairs in the union over these four horizons. Value-only or tree-only differences do not qualify. Only \(C_*\) controls the gate.

## 3. Exhaustive coverage and counts

All tables below were independently reproduced by both verification paths. Counts across certificates and domains overlap and must not be added as independent replications. The interior rows are a restriction of the primary space, not an additional disjoint sample. Exact ties were allowed by the predicates; **every observed separating pair–horizon event was a strict STOP-versus-OBSERVE conflict**. Tie-involving event counts, tie-only pair counts, and mixed strict/tie pair counts are all zero in every row.

The per-horizon event counts are point-horizon comparisons, not cumulative quotient refinements. A pair can separate at one horizon and agree at another. No horizon-stabilization or main-lane quotient claim is made here.

### 3.1 Domains and one-step classes

| Domain | Full objects | Unordered pairs | σ₀ classes | σ₁ classes | σ₂ classes | σ₃ classes |
|---|---|---|---|---|---|---|
| Primary | 1,800 | 1,619,100 | 3 | 19 | 53 | 203 |
| Interior | 432 | 93,096 | 3 | 12 | 24 | 58 |

The registered half-grid control, after cost duplicates were removed, contained 216 objects and yielded σ₀–σ₃ class counts **3, 19, 31, 109**. Costs are part of each C-certificate but not the σ-signatures.

### 3.2 Certificate classes and unique collisions

| Domain | Certificate | Classes | Equal-certificate candidate pairs | Unique separating pairs | Pair–horizon events | Pairs with any strict conflict | Tie-only pairs |
|---|---|---|---|---|---|---|---|
| Primary | C₂ | 159 | 33,912 | 11,440 | 31,376 | 11,440 | 0 |
| Primary | C₃ | 609 | 11,160 | 3,784 | 10,616 | 3,784 | 0 |
| Primary | C* | 1,176 | 696 | 64 | 160 | 64 | 0 |
| Interior | C₂ | 72 | 3,480 | 976 | 2,416 | 976 | 0 |
| Interior | C₃ | 174 | 1,416 | 432 | 1,120 | 432 | 0 |
| Interior | C* | 288 | 144 | 0 | 0 | 0 | 0 |

### 3.3 Per-horizon separating pair counts

| Domain | Certificate | h=2 | h=3 | h=4 | h=5 |
|---|---|---|---|---|---|
| Primary | C₂ | 5,840 | 8,048 | 8,896 | 8,592 |
| Primary | C₃ | 2,120 | 2,680 | 2,960 | 2,856 |
| Primary | C* | 48 | 48 | 32 | 32 |
| Interior | C₂ | 560 | 752 | 656 | 448 |
| Interior | C₃ | 208 | 336 | 320 | 256 |
| Interior | C* | 0 | 0 | 0 | 0 |

Every entry in this table is also its strict-conflict count. Its tie-involving count is zero. For every certificate, pairs with any tie-involving event and pairs with both strict and tie-involving events are also zero.

### 3.4 Earliest separating horizon, counting each pair once

| Domain | Certificate | First at 2 | First at 3 | First at 4 | First at 5 |
|---|---|---|---|---|---|
| Primary | C₂ | 5,840 | 3,168 | 1,520 | 912 |
| Primary | C₃ | 2,120 | 912 | 408 | 344 |
| Primary | C* | 48 | 16 | 0 | 0 |
| Interior | C₂ | 560 | 320 | 64 | 32 |
| Interior | C₃ | 208 | 192 | 0 | 32 |
| Interior | C* | 0 | 0 | 0 | 0 |

### 3.5 Global pair minimum versus global horizon minimum

| Domain | Certificate | First pair overall | That pair’s first separating h | Smallest separating h | First pair at that smallest h |
|---|---|---|---|---|---|
| Primary | C₂ | P0009/P0255 | 2 | 2 | P0009/P0255 |
| Primary | C₃ | P0016/P0019 | 5 | 2 | P0016/P0022 |
| Primary | C* | P0100/P0106 | 2 | 2 | P0100/P0106 |
| Interior | C₂ | P0022/P0034 | 2 | 2 | P0022/P0034 |
| Interior | C₃ | P0022/P0034 | 2 | 2 | P0022/P0034 |
| Interior | C* | — | — | — | — |

For primary C₃, the first pair overall separates first at horizon 5, although the smallest separating horizon anywhere is 2. The packet’s two ordering questions are therefore consequential. All listed minima are strict conflicts. A dash means no qualifying pair, not an impossible observation.

### 3.6 First pair separately at every horizon

| Domain | Certificate | h=2 | h=3 | h=4 | h=5 |
|---|---|---|---|---|---|
| Primary | C₂ | P0009/P0255 | P0009/P0255 | P0009/P0255 | P0009/P0255 |
| Primary | C₃ | P0016/P0022 | P0016/P0022 | P0016/P0022 | P0016/P0019 |
| Primary | C* | P0100/P0106 | P0101/P0107 | P0103/P0109 | P0103/P0109 |
| Interior | C₂ | P0022/P0034 | P0022/P0034 | P0022/P0097 | P0022/P0109 |
| Interior | C₃ | P0022/P0034 | P0022/P0034 | P0097/P0100 | P0097/P0109 |
| Interior | C* | — | — | — | — |

## 4. First strongest-certificate witness: P0100/P0106

This is both the globally first primary \(C_*\) collision and the first collision at the globally smallest separating horizon, \(h=2\). It was selected by exhaustive enumeration, not supplied in advance.

Both models have

\[
p=1/4,\qquad L=\begin{pmatrix}0&1\\2&0\end{pmatrix},\qquad c=1/100.
\]

Their likelihood vectors are

\[
k^{(100)}=(1/4,3/4),\qquad k^{(106)}=(1/2,0).
\]

Equivalently, their kernels with **state rows and outcome columns** are

\[
K^{(100)}=\begin{pmatrix}3/4&1/4\\1/4&3/4\end{pmatrix},\qquad
K^{(106)}=\begin{pmatrix}1/2&1/2\\1&0\end{pmatrix}.
\]

Current expected action losses are \((1/4,3/2)\), so \(A_F(p)=\{0\}\) and \(R_F(p)=1/4\). Both first-signal outcomes leave terminal action 0 uniquely optimal; EVSI is zero. Every single-cell loss-revision query also leaves current action 0 uniquely optimal. With

\[
\pi_0=(\{0\},\{0\},\{0\}),\qquad
T_0=(\{0\},\{0\},\{0\},\{0\}),
\]

their common certificate is exactly

\[
C_*=
\left(\frac1{100},\bigl((\pi_0,0),T_0\bigr),\frac14,\frac58,\frac38\right).
\]

### 4.1 Root decisions through the first separating horizon

| Model | Horizon | Terminal action set | R | O | V | Continuation set |
|---|---:|---|---:|---:|---:|---|
| Both | 0 | {0} | 1/4 | NA | 1/4 | {STOP}, forced |
| Both | 1 | {0} | 1/4 | 13/50 | 1/4 | {STOP}, strict |
| P0100 | 2 | {0} | 1/4 | 347/1600 | 347/1600 | {OBSERVE}, strict |
| P0106 | 2 | {0} | 1/4 | 13/50 | 1/4 | {STOP}, strict |

The one-step net information value is \(-1/100\) in both models. P0100's horizon-2 improvement over stopping is \(53/1600\). P0106's forced first observation instead increases expected total loss by \(1/100\).

### 4.2 Immediate posteriors and continuation branches

Every row has terminal action set \(\{0\}\). The branch horizon is 1; costs are future costs from the branch, excluding the first observation fee.

| Model | First outcome | Marginal mass | Posterior b | Branch R | Branch O¹ | Branch V¹ | Branch continuation set |
|---|---:|---:|---:|---:|---:|---:|---|
| P0100 | 0 | 5/8 | 1/10 | 1/10 | 11/100 | 1/10 | {STOP} |
| P0100 | 1 | 3/8 | 1/2 | 1/2 | 77/200 | 77/200 | {OBSERVE} |
| P0106 | 0 | 5/8 | 2/5 | 2/5 | 41/100 | 2/5 | {STOP} |
| P0106 | 1 | 3/8 | 0 | 0 | 1/100 | 0 | {STOP} |

All branch choices are strict. P0106's branches are counterfactual because the optimal initial decision stops.

### 4.3 Exact mechanism

The terminal loss difference is \(b-2(1-b)=3b-2\). Action 0 is uniquely optimal for \(b<2/3\), action 1 for \(b>2/3\), and both minimize at the boundary. Prior odds are \(1/3\).

For P0100, signal-0 and signal-1 likelihood ratios are \(1/3\) and 3. After signal 1 the belief is \(1/2\); after a second signal 1 it is \(3/4\), crossing the action boundary. From belief \(1/2\), the second outcomes each have mass \(1/2\) and terminal beliefs \(1/4\) and \(3/4\). Their terminal risks are \(1/4\) and \(1/2\), giving expected posterior risk \(3/8\), one-step EVSI \(1/8\), and net continuation benefit \(23/200\).

For P0106, the signal-0 likelihood ratio is 2 and signal 1 certifies state 0. Two consecutive zeros produce belief \(4/7<2/3\); every other length-two history has belief 0. Thus no second observation can change the optimal terminal action at either immediate posterior. Its branch continuation benefit at this horizon is zero.

The registered decomposition gives

\[
R-O^2=(EVSI_1-c)+\sum_xm_x\bigl(R(b_x)-V^1(b_x)\bigr).
\]

For P0100,

\[
R-O^2=-\frac1{100}+\frac58(0)+\frac38\frac{23}{200}
=\frac{53}{1600}>0.
\]

For P0106, both continuation-benefit terms are zero, so \(R-O^2=-1/100<0\). Equal current risk, one-step policy, EVSI, loss-revision answers, price, and outcome masses do not determine the branch continuation benefit for this primary pair.

A direct policy calculation provides an additional check for P0100: observe once; after outcome 0 stop with action 0; after outcome 1 observe again and choose action 1 exactly if the second outcome is also 1. Its expected terminal loss is

\[
\frac34\left(\frac14\right)^2 2
+\frac14\left(1-\left(\frac34\right)^2\right)
=\frac{13}{64}.
\]

The expected observation count is \(1+3/8=11/8\), giving observation cost \(11/800\). Their sum is \(347/1600\), exactly the two independently computed Bellman values. This check verifies the selected policy after enumeration; it did not select the witness.

## 5. Interior failure and the meaning of the stopping label

The interior domain has 288 \(C_*\) classes and 144 distinct equal-certificate candidate pairs. None has different root continuation sets at horizons 2–5. Independent grouping associates each interior certificate class with a single root-decision trajectory over those horizons. Consequently there is no interior canonical \(C_*\) witness or smallest separating horizon to report.

The primary canonical pair consists of one interior kernel, P0100, and one boundary kernel, P0106. P0106 has \(K(1\mid\theta=1)=0\). Both kernels are informative; neither is a constant-outcome test or a fully deterministic kernel. **Neither selected model has an impossible forced observation history** through the checked range: under state 0 every binary string has positive probability, and that state has positive prior mass. The boundary kernel nevertheless permits a conclusive posterior of zero after outcome 1.

Thus `STOP_DEGENERATE` here records the failure of the registered informative-interior restriction, not a claim that the canonical example needs an impossible marginal observation, a constant test, or a fully deterministic experiment. Across the primary space the overlapping object-label counts are: 1,152 boundary kernels, 360 uninformative kernels, 144 constant-outcome kernels, and 288 fully deterministic kernels. All four labels are false throughout the interior tier.

The weaker interior certificates have 976 separating pairs under \(C_2\) and 432 under \(C_3\). Those are genuine bounded Stage R findings, but they do not satisfy the frozen strongest-certificate gate. The result neither rules out weaker one-step-equivalent/sequentially-different pairs nor proves that a boundary is globally necessary outside these grids. No replacement kernel grid, weaker gate, or follow-on experiment was introduced.

## 6. Verification and integrity

The implementation used Python 3.9.6 and standard-library exact fractions. Normalized posterior recursion and unnormalized joint-mass recursion were implemented independently, sharing only the frozen inputs, labels, and basic library infrastructure. The raw recursion did not call the normalized posterior, loss, signature, or Bellman functions. Zero-mass branches contributed zero algebraic weight but retained `NA` conditional answers.

Both implementations agreed on all 1,800 full-object records, all 10,800 initial object–horizon evaluations, all four one-step signatures, all three certificates, and the primitive records needed at every positive-probability forced-history/remaining-horizon node within the registered bound. There were 189,648 positive node slots and 26,352 impossible node slots, totaling 216,000. Across the 63 histories per object, 97,704 history slots were positive and 15,696 impossible.

Checks passed for nonnegative EVSI, normalized probabilities, retained minimizer sets, value bounds, horizon monotonicity, known-state and uninformative-kernel sanity conditions, and 126,432 adjacent-cost comparisons of optimal value at matched nodes. The nested one-step signatures were checked by projection. These are Stage R arithmetic controls; no sequential quotient hierarchy, candidate-summary lane, history-compression comparison across models, or cost-family lane was executed.

For selection and counts, Path N inspected every unordered pair in each domain for each certificate. Path W independently grouped its own exact certificates by root-decision trajectory and counted differing-trajectory pairs using multiplicities. The candidate-pair and collision totals, per-horizon and earliest-horizon counts, strict/tie classifications, class counts, and every reported canonical minimum matched exactly. A negative gate was therefore checked over every equal-certificate candidate, not inferred from a missing sampled witness.

The KL4C half-grid control independently reproduced 216 structural objects and the one-step class counts **3, 19, 31, 109**. These inherited counts were used only as the registered control. The enlarged primary-space counts were computed anew.

A final complete run incorporating the per-object reporting diagnostics reproduced every first-run count and gate outcome. There was no arithmetic disagreement, integrity failure, implementation correction, or mathematical-protocol change. Full terminal and continuation ties were preserved even though no separating event or selected-witness node involved a tie.

## 7. Complete dictionary of selected witnesses

These objects cover every minimum in section 3. Loss tuples are row-major, and k lists K(1|0), K(1|1); complements specify outcome 0. Label B means boundary kernel, U means uninformative interior-coordinate kernel excluded by the tier, and I means membership in the informative interior tier. No selected object is a constant-outcome or fully deterministic kernel.

| Object | p | Loss tuple | k | c | Label |
|---|---|---|---|---|---|
| P0009 | 1/4 | (0,1,1,0) | (0,1/2) | 1/5 | B |
| P0016 | 1/4 | (0,1,1,0) | (1/4,0) | 1/100 | B |
| P0019 | 1/4 | (0,1,1,0) | (1/4,1/4) | 1/100 | U |
| P0022 | 1/4 | (0,1,1,0) | (1/4,1/2) | 1/100 | I |
| P0034 | 1/4 | (0,1,1,0) | (1/2,1/4) | 1/100 | I |
| P0097 | 1/4 | (0,1,2,0) | (1/4,1/2) | 1/100 | I |
| P0100 | 1/4 | (0,1,2,0) | (1/4,3/4) | 1/100 | I |
| P0101 | 1/4 | (0,1,2,0) | (1/4,3/4) | 1/20 | I |
| P0103 | 1/4 | (0,1,2,0) | (1/4,1) | 1/100 | B |
| P0106 | 1/4 | (0,1,2,0) | (1/2,0) | 1/100 | B |
| P0107 | 1/4 | (0,1,2,0) | (1/2,0) | 1/20 | B |
| P0109 | 1/4 | (0,1,2,0) | (1/2,1/4) | 1/100 | I |
| P0255 | 1/4 | (0,2,2,0) | (1/4,1) | 1/5 | B |

For all 13 selected objects, the checked 63 forced history slots have **zero impossible histories** and **zero terminal-tie histories**. Their positive history/remaining-horizon slots with at least one observation remaining have **zero continuation ties**. These diagnostics were checked on both value paths’ matching records; a boundary label alone does not imply an impossible marginal history.

### 7.1 Exact one-step answers

Use π₀=({0},{0},{0}), π₁=({0},{0},{1}), T₀=({0},{0},{0},{0}), and T₁=({1},{0},{0},{0}). Each row therefore specifies σ₂=(π,EVSI), σ₃=((π,EVSI),T), and, together with its cost, all three certificate values exactly. All current terminal action sets are {0}.

| Object | Policy | EVSI | Revisions | R | m₀ | m₁ |
|---|---|---|---|---|---|---|
| P0009 | π₁ | 1/8 | T₁ | 1/4 | 7/8 | 1/8 |
| P0016 | π₀ | 0 | T₁ | 1/4 | 13/16 | 3/16 |
| P0019 | π₀ | 0 | T₁ | 1/4 | 3/4 | 1/4 |
| P0022 | π₀ | 0 | T₁ | 1/4 | 11/16 | 5/16 |
| P0034 | π₀ | 0 | T₁ | 1/4 | 9/16 | 7/16 |
| P0097 | π₀ | 0 | T₀ | 1/4 | 11/16 | 5/16 |
| P0100 | π₀ | 0 | T₀ | 1/4 | 5/8 | 3/8 |
| P0101 | π₀ | 0 | T₀ | 1/4 | 5/8 | 3/8 |
| P0103 | π₀ | 0 | T₀ | 1/4 | 9/16 | 7/16 |
| P0106 | π₀ | 0 | T₀ | 1/4 | 5/8 | 3/8 |
| P0107 | π₀ | 0 | T₀ | 1/4 | 5/8 | 3/8 |
| P0109 | π₀ | 0 | T₀ | 1/4 | 9/16 | 7/16 |
| P0255 | π₁ | 1/8 | T₀ | 1/2 | 9/16 | 7/16 |

Certificate equality for every minimum is directly inspectable from these fields. For example, P0016/P0019 agree on C₃ but differ in outcome masses, while P0009/P0255 agree on C₂ but differ in both current risk and the Q3 revision answers.

### 7.2 Exact distinguishing root answers for every per-horizon minimum

Each row uses the pair listed in section 3.6. Both models have the equal certificate reconstructed in section 7.1 at the common cost in their object rows. The exact differing minimizing sets and the corresponding optimal and forced-observation values are shown below. Left and right refer to the ordered pair. Repeated pairs across certificate/domain conditions are intentional.

| Domain | Cert. | h | Pair | Left D | Right D | Left V | Right V | Left O | Right O |
|---|---|---|---|---|---|---|---|---|---|
| Primary | C₂ | 2 | P0009/P0255 | {STOP} | {OBSERVE} | 1/4 | 61/160 | 13/40 | 61/160 |
| Primary | C₂ | 3 | P0009/P0255 | {STOP} | {OBSERVE} | 1/4 | 237/640 | 13/40 | 237/640 |
| Primary | C₂ | 4 | P0009/P0255 | {STOP} | {OBSERVE} | 1/4 | 237/640 | 13/40 | 237/640 |
| Primary | C₂ | 5 | P0009/P0255 | {STOP} | {OBSERVE} | 1/4 | 237/640 | 13/40 | 237/640 |
| Primary | C₃ | 2 | P0016/P0022 | {STOP} | {OBSERVE} | 1/4 | 99/400 | 13/50 | 99/400 |
| Primary | C₃ | 3 | P0016/P0022 | {STOP} | {OBSERVE} | 1/4 | 783/3200 | 13/50 | 783/3200 |
| Primary | C₃ | 4 | P0016/P0022 | {STOP} | {OBSERVE} | 1/4 | 15/64 | 13/50 | 15/64 |
| Primary | C₃ | 5 | P0016/P0019 | {OBSERVE} | {STOP} | 2731/12800 | 1/4 | 2731/12800 | 13/50 |
| Primary | C* | 2 | P0100/P0106 | {OBSERVE} | {STOP} | 347/1600 | 1/4 | 347/1600 | 13/50 |
| Primary | C* | 3 | P0101/P0107 | {OBSERVE} | {STOP} | 63/256 | 1/4 | 63/256 | 93/320 |
| Primary | C* | 4 | P0103/P0109 | {OBSERVE} | {STOP} | 661/25600 | 1/4 | 661/25600 | 13/50 |
| Primary | C* | 5 | P0103/P0109 | {OBSERVE} | {STOP} | 2453/102400 | 1/4 | 2453/102400 | 13297/51200 |
| Interior | C₂ | 2 | P0022/P0034 | {OBSERVE} | {STOP} | 99/400 | 1/4 | 99/400 | 13/50 |
| Interior | C₂ | 3 | P0022/P0034 | {OBSERVE} | {STOP} | 783/3200 | 1/4 | 783/3200 | 823/3200 |
| Interior | C₂ | 4 | P0022/P0097 | {OBSERVE} | {STOP} | 15/64 | 1/4 | 15/64 | 261/1024 |
| Interior | C₂ | 5 | P0022/P0109 | {OBSERVE} | {STOP} | 5959/25600 | 1/4 | 5959/25600 | 13297/51200 |
| Interior | C₃ | 2 | P0022/P0034 | {OBSERVE} | {STOP} | 99/400 | 1/4 | 99/400 | 13/50 |
| Interior | C₃ | 3 | P0022/P0034 | {OBSERVE} | {STOP} | 783/3200 | 1/4 | 783/3200 | 823/3200 |
| Interior | C₃ | 4 | P0097/P0100 | {STOP} | {OBSERVE} | 1/4 | 2167/12800 | 261/1024 | 2167/12800 |
| Interior | C₃ | 5 | P0097/P0109 | {OBSERVE} | {STOP} | 25469/102400 | 1/4 | 25469/102400 | 13297/51200 |

The reproduction output supplies every selected object’s root records for horizons 0–5, immediate posterior masses and beliefs, and branch records for remaining horizons 0–4. These are arithmetic records for Stage R witnesses, not a main-lane policy-tree quotient analysis.

## 8. Reproduction

The following self-contained Python 3.9+ standard-library program reproduces the full Stage R computation, both verification paths, half-grid control, primary gate, conditional interior gate, exact counts, canonical pairs, and witness records. It writes results to standard output only. It contains no hand-selected witness input and no main-lane or synthesis execution.

Records in its output are ordered `(terminal_action_set, R, continuation_set, V, O)`. The `sig` tuple contains \(\sigma_0\) through \(\sigma_3\); `cert` contains \(C_2,C_3,C_*\); root records use horizons 0–5, and immediate branch records use remaining horizons 0–4. Object IDs are one-based primary IDs. Fractions serialize exactly; `NA` remains distinct from a minimizing set. Computational grouping checks full tuple equality rather than relying on hashes alone.

```python
from fractions import Fraction as Q
from functools import cache
from itertools import product, combinations
from collections import defaultdict, Counter
from math import comb
import json

NA = 'NA'
STOP, OBSERVE = 'STOP', 'OBSERVE'
PRIORS = (Q(1,4), Q(1,2), Q(3,4))
LOSSES = ((0,1,1,0), (0,1,2,0), (0,2,1,0), (0,2,2,0),
          (1,0,0,1), (1,0,0,2), (2,0,0,1), (2,0,0,2))
GRID = tuple(Q(i,4) for i in range(5))
COSTS = (Q(1,100), Q(1,20), Q(1,5))
HISTORIES = tuple(s for t in range(6) for s in product((0,1), repeat=t))
OBJECTS = tuple(sorted((p,l,k,c) for p in PRIORS for l in LOSSES
                       for k in product(GRID, repeat=2) for c in COSTS))
assert len(OBJECTS) == len(set(OBJECTS)) == 1800
assert len(HISTORIES) == 63
assert all(min(l[t],l[2+t]) == 0 for l in LOSSES for t in range(2))
assert all(any(l[2*a+t] < l[2*(1-a)+t] for t in range(2))
           for l in LOSSES for a in range(2))


def normalized(f):
    p,l,k,c = f
    kernel = ((1-k[0],1-k[1]), k)
    assert all(kernel[0][t]+kernel[1][t] == 1 for t in range(2))

    def losses(b, table=l):
        return tuple((1-b)*table[2*a]+b*table[2*a+1] for a in range(2))

    def amin(v):
        return tuple(a for a in range(2) if v[a] == min(v))

    def signals(b):
        out = []
        for row in kernel:
            mass = (1-b)*row[0]+b*row[1]
            post = b*row[1]/mass if mass else NA
            if mass:
                assert (1-b)*row[0]/mass+post == 1
                assert 0 <= post <= 1
            out.append((mass,post))
        assert sum(x[0] for x in out) == 1
        return tuple(out)

    @cache
    def dp(b,r):
        el = losses(b)
        a, risk = amin(el), min(el)
        if r == 0:
            return (a,risk,(STOP,),risk,NA)
        after = signals(b)
        forced = c+sum(m*dp(bp,r-1)[3] for m,bp in after if m)
        value = min(risk,forced)
        decision = tuple(name for name,cost in ((STOP,risk),(OBSERVE,forced))
                         if cost == value)
        return (a,risk,decision,value,forced)

    root = tuple(dp(p,h) for h in range(6))
    out = signals(p)
    policy = (root[0][0],)+tuple(dp(bp,0)[0] if m else NA for m,bp in out)
    evsi = root[0][1]-sum(m*dp(bp,0)[1] for m,bp in out if m)
    revision = []
    for cell in range(4):
        changed = list(l)
        changed[cell] += 1
        revision.append(amin(losses(p,changed)))
    sig = (root[0][0], policy, (policy,evsi), ((policy,evsi),tuple(revision)))
    cert = ((c,sig[2]), (c,sig[3]), (c,sig[3],root[0][1],out[0][0],out[1][0]))
    assert evsi >= 0 and root[1][4] == c+root[0][1]-evsi
    assert sig[3][0] == sig[2] and sig[2][0] == sig[1] and sig[1][0] == sig[0]

    history = {(): (Q(1),p)}
    nodes = {}
    for s in HISTORIES:
        mass,b = history[s]
        for r in range(6-len(s)):
            if not mass:
                nodes[(s,r)] = NA
                continue
            row = dp(b,r)
            nodes[(s,r)] = row
            assert 0 <= row[3] <= row[1]
            if r:
                assert row[3] <= dp(b,r-1)[3]
                if b in (0,1):
                    assert row[1] == row[3] == 0 and row[2] == (STOP,)
            local = signals(b)
            assert row[1]-sum(m*dp(bp,0)[1] for m,bp in local if m) >= 0
            if k[0] == k[1]:
                assert all(bp == b for m,bp in local if m)
        if len(s) < 5:
            for x in (0,1):
                if mass:
                    m,bp = signals(b)[x]
                    history[s+(x,)] = (mass*m,bp)
                else:
                    history[s+(x,)] = (Q(0),NA)
    branches = tuple(tuple(dp(bp,r) for r in range(5)) if m else NA for m,bp in out)
    return dict(sig=sig,cert=cert,roots=root,outcomes=out,branches=branches), nodes, history


def weighted(f):
    p,l,k,c = f

    @cache
    def solve(w0,w1,r):
        total = w0+w1
        if not total:
            return (NA,Q(0),NA,Q(0),NA)
        j0 = w0*l[0]+w1*l[1]
        j1 = w0*l[2]+w1*l[3]
        actions = (0,) if j0 < j1 else (1,) if j1 < j0 else (0,1)
        stop = j0 if j0 <= j1 else j1
        if not r:
            return (actions,stop,(STOP,),stop,NA)
        observe = total*c + solve(w0*(1-k[0]),w1*(1-k[1]),r-1)[3]
        observe += solve(w0*k[0],w1*k[1],r-1)[3]
        if stop < observe:
            decision, value = (STOP,),stop
        elif observe < stop:
            decision, value = (OBSERVE,),observe
        else:
            decision, value = (STOP,OBSERVE),stop
        return (actions,stop,decision,value,observe)

    def conditional(w0,w1,r):
        total = w0+w1
        if total == 0:
            return NA
        a,stop,d,value,observe = solve(w0,w1,r)
        return (a,stop/total,d,value/total,observe/total if r else NA)

    # Products are evaluated directly from each history, without posterior updates.
    history = {}
    nodes = {}
    for s in HISTORIES:
        w0,w1 = 1-p,p
        for x in s:
            w0 *= k[0] if x == 1 else 1-k[0]
            w1 *= k[1] if x == 1 else 1-k[1]
        total = w0+w1
        history[s] = (total,w1/total if total else NA)
        for r in range(6-len(s)):
            nodes[(s,r)] = conditional(w0,w1,r)
    root = tuple(conditional(1-p,p,h) for h in range(6))
    policy = [solve(1-p,p,0)[0]]
    posterior_minimum_sum = Q(0)
    branches = []
    outcomes = []
    for x in (0,1):
        a0 = (1-p)*(k[0] if x else 1-k[0])
        a1 = p*(k[1] if x else 1-k[1])
        m = a0+a1
        term = solve(a0,a1,0)
        policy.append(term[0] if m else NA)
        posterior_minimum_sum += term[1]
        outcomes.append((m,a1/m if m else NA))
        branches.append(tuple(conditional(a0,a1,r) for r in range(5)) if m else NA)
    initial_min = solve(1-p,p,0)[1]
    value_information = initial_min-posterior_minimum_sum
    revised = []
    for cell in range(4):
        costs = [(1-p)*l[0]+p*l[1], (1-p)*l[2]+p*l[3]]
        costs[cell//2] += (1-p) if cell % 2 == 0 else p
        revised.append((0,) if costs[0]<costs[1] else (1,) if costs[1]<costs[0] else (0,1))
    q0 = root[0][0]
    q1 = tuple(policy)
    q2 = (q1,value_information)
    q3 = (q2,tuple(revised))
    certificates = ((c,q2),(c,q3),(c,q3,initial_min,outcomes[0][0],outcomes[1][0]))
    return dict(sig=(q0,q1,q2,q3),cert=certificates,roots=root,
                outcomes=tuple(outcomes),branches=tuple(branches)), nodes, history


def pair_scan(ids, data):
    # Exhaustive unordered full-object pairs. No outcome-dependent pruning.
    result = []
    for j in range(3):
        intern = {}
        classes = {}
        for i in ids:
            key = data[i]['cert'][j]
            if key not in intern:
                intern[key] = len(intern)
            classes[i] = intern[key]
        stat = dict(classes=len(intern),candidate_pairs=0,pairs=0,events=0,
                    per_h=[0]*4,strict_h=[0]*4,tie_h=[0]*4,earliest=[0]*4,
                    any_strict=0,any_tie=0,both_types=0,tie_only=0,
                    first=None,first_by_h=[None]*4,first_strict=None)
        checked = 0
        for a,b in combinations(ids,2):
            checked += 1
            if classes[a] != classes[b]:
                continue
            stat['candidate_pairs'] += 1
            if j == 2:
                assert data[a]['roots'][:2] == data[b]['roots'][:2]
            differences, stricts, ties = [],[],[]
            for t,h in enumerate(range(2,6)):
                da,db = data[a]['roots'][h][2],data[b]['roots'][h][2]
                if da != db:
                    differences.append(t)
                    (stricts if len(da)==len(db)==1 else ties).append(t)
                    stat['per_h'][t] += 1
                    if stat['first_by_h'][t] is None:
                        stat['first_by_h'][t] = (a,b)
            if differences:
                stat['pairs'] += 1
                stat['events'] += len(differences)
                stat['earliest'][differences[0]] += 1
                if stat['first'] is None:
                    stat['first'] = (a,b,differences[0]+2)
            for t in stricts:
                stat['strict_h'][t] += 1
            for t in ties:
                stat['tie_h'][t] += 1
            stat['any_strict'] += bool(stricts)
            stat['any_tie'] += bool(ties)
            stat['both_types'] += bool(stricts and ties)
            stat['tie_only'] += bool(ties and not stricts)
            if stricts and stat['first_strict'] is None:
                stat['first_strict'] = (a,b,stricts[0]+2)
        assert checked == comb(len(ids),2)
        stat['checked_pairs'] = checked
        stat['minimum_h'] = next((h for h in range(2,6) if stat['per_h'][h-2]),None)
        result.append(stat)
    return result


def partition_check(ids, data):
    # Independent certificate/profile grouping and multiplicity counts.
    answer = []
    for j in range(3):
        groups = defaultdict(lambda: defaultdict(list))
        for i in ids:
            trajectory = tuple(data[i]['roots'][h][2] for h in range(2,6))
            groups[data[i]['cert'][j]][trajectory].append(i)
        candidate = unique = event = astrict = atie = both = tieonly = 0
        per, sh, th, earliest = [0]*4,[0]*4,[0]*4,[0]*4
        first = first_strict = None
        first_h = [None]*4
        for profiles in groups.values():
            n = sum(len(members) for members in profiles.values())
            candidate += comb(n,2)
            expected_union = comb(n,2)-sum(comb(len(v),2) for v in profiles.values())
            group_union = 0
            for (left,lids),(right,rids) in combinations(profiles.items(),2):
                mult = len(lids)*len(rids)
                pair = tuple(sorted((min(lids),min(rids))))
                differing = [t for t in range(4) if left[t] != right[t]]
                assert differing
                strict = [t for t in differing if set(left[t]).isdisjoint(right[t])]
                tied = [t for t in differing if t not in strict]
                group_union += mult
                event += mult*len(differing)
                earliest[min(differing)] += mult
                item = pair+(min(differing)+2,)
                if first is None or item[:2] < first[:2]:
                    first = item
                for t in differing:
                    per[t] += mult
                    if first_h[t] is None or pair < first_h[t]:
                        first_h[t] = pair
                for t in strict:
                    sh[t] += mult
                for t in tied:
                    th[t] += mult
                astrict += mult if strict else 0
                atie += mult if tied else 0
                both += mult if strict and tied else 0
                tieonly += mult if tied and not strict else 0
                if strict and (first_strict is None or pair < first_strict[:2]):
                    first_strict = pair+(min(strict)+2,)
            assert group_union == expected_union
            unique += expected_union
        answer.append(dict(classes=len(groups),candidate_pairs=candidate,pairs=unique,
                           events=event,per_h=per,strict_h=sh,tie_h=th,earliest=earliest,
                           any_strict=astrict,any_tie=atie,both_types=both,tie_only=tieonly,
                           first=first,first_by_h=first_h,first_strict=first_strict,
                           checked_pairs=comb(len(ids),2),
                           minimum_h=next((t+2 for t,n in enumerate(per) if n),None)))
    return answer


def domain_result(ids, nd, wd):
    exhaustive = pair_scan(ids,nd)
    independent = partition_check(ids,wd)
    assert exhaustive == independent
    qn = [len({nd[i]['sig'][j] for i in ids}) for j in range(4)]
    qw = [len(Counter(wd[i]['sig'][j] for i in ids)) for j in range(4)]
    assert qn == qw
    for row in exhaustive:
        assert row['events'] == sum(row['per_h'])
        assert row['pairs'] == sum(row['earliest']) == row['any_strict']+row['tie_only']
        assert row['any_tie'] == row['tie_only']+row['both_types']
        assert all(a == b+c for a,b,c in zip(row['per_h'],row['strict_h'],row['tie_h']))
    return dict(objects=len(ids),unordered_pairs=comb(len(ids),2),
                one_step_classes=qn,certificates=exhaustive)


def encode(x):
    if isinstance(x,Q):
        return str(x)
    if isinstance(x,dict):
        return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):
        return [encode(v) for v in x]
    return x


def run():
    nd,wd = {},{}
    positive_nodes = impossible_nodes = positive_histories = impossible_histories = 0
    previous_model = previous_nodes = None
    cost_checks = 0
    for number,f in enumerate(OBJECTS,1):
        n,nn,nh = normalized(f)
        w,wn,wh = weighted(f)
        assert n == w, ('record mismatch',number)
        assert nn == wn and nh == wh, ('node/history mismatch',number)
        assert len(nn) == 120
        positive_nodes += sum(v != NA for v in nn.values())
        impossible_nodes += sum(v == NA for v in nn.values())
        positive_histories += sum(m > 0 for m,b in nh.values())
        impossible_histories += sum(m == 0 for m,b in nh.values())
        model = f[:3]
        if model == previous_model:
            for key,v in nn.items():
                if v != NA:
                    assert v[3] >= previous_nodes[key][3]
                    cost_checks += 1
        previous_model,previous_nodes = model,nn
        labels = dict(boundary_kernel=any(v in (0,1) for v in f[2]),
                      uninformative=f[2][0] == f[2][1],
                      constant_outcome=f[2] in ((0,0),(1,1)),
                      fully_deterministic=all(v in (0,1) for v in f[2]))
        diagnostics = dict(labels=labels,
                           impossible_histories=sum(m == 0 for m,b in nh.values()),
                           terminal_tie_histories=sum(nn[(s,0)] != NA and len(nn[(s,0)][0]) == 2
                                                      for s in HISTORIES),
                           continuation_tie_nodes=sum(v != NA and r > 0 and len(v[2]) == 2
                                                      for (s,r),v in nn.items()))
        n['diagnostics'] = diagnostics
        w['diagnostics'] = diagnostics
        nd[number],wd[number] = n,w
        if number % 300 == 0:
            print('Verified objects:',number,flush=True)
    control = [i for i,f in enumerate(OBJECTS,1)
               if f[2][0] in (0,Q(1,2),1) and f[2][1] in (0,Q(1,2),1)
               and f[3] == COSTS[0]]
    assert len(control) == 216
    controls_n = [len({nd[i]['sig'][j] for i in control}) for j in range(4)]
    controls_w = [len(Counter(wd[i]['sig'][j] for i in control)) for j in range(4)]
    assert controls_n == controls_w == [3,19,31,109]
    print('KL4C half-grid control:',controls_n,flush=True)
    result = dict(control_classes=controls_n,
                  verification=dict(objects=1800,root_evaluations=10800,
                                    positive_nodes=positive_nodes,impossible_nodes=impossible_nodes,
                                    positive_histories=positive_histories,impossible_histories=impossible_histories,
                                    cost_monotonic_comparisons=cost_checks))
    print('Exhaustive primary pair pass and independent partitions',flush=True)
    result['primary'] = domain_result(list(nd),nd,wd)
    if not result['primary']['certificates'][2]['pairs']:
        result['verdict'] = 'KL5_STOP_R'
        result['interior'] = None
    else:
        interior = [i for i,f in enumerate(OBJECTS,1)
                    if 0 < f[2][0] < 1 and 0 < f[2][1] < 1 and f[2][0] != f[2][1]]
        assert len(interior) == 432
        print('Primary gate passed. Exhaustive interior restriction',flush=True)
        result['interior'] = domain_result(interior,nd,wd)
        result['verdict'] = ('KL5_R_PASS' if result['interior']['certificates'][2]['pairs']
                             else 'KL5_STOP_DEGENERATE')
    needed = set()
    for name in ('primary','interior'):
        if result[name] is not None:
            for stat in result[name]['certificates']:
                for item in (stat['first'],stat['first_strict'],*stat['first_by_h']):
                    if item:
                        needed.update(item[:2])
    result['witness_objects'] = {i:dict(object=OBJECTS[i-1],**nd[i]) for i in sorted(needed)}
    result['primary_diagnostic_counts'] = {
        label:sum(d['diagnostics']['labels'][label] for d in nd.values())
        for label in ('boundary_kernel','uninformative','constant_outcome','fully_deterministic')}
    print('RESULT_JSON',flush=True)
    print(json.dumps(encode(result),indent=2))
    return result


if __name__ == '__main__':
    run()
```

## 9. Stage R disposition

The primary \(C_*\) result is positive and the triggered interior \(C_*\) result is negative. Section R2 therefore requires stopping before all main lanes. The weaker interior positives do not change that rule. This report ends at the Stage R gate and supplies no synthesis verdict or broader programme recommendation.

KL5_STOP_DEGENERATE
