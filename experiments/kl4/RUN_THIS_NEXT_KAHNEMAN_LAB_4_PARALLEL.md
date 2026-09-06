# RUN THIS NEXT — Kahneman Lab Experiment 4
## Uncertainty, Information, and Action

## 0. Purpose

Experiment 4 is a deterministic finite-mathematics experiment. It follows the KL3v2 result `KL3V2_STOP_CONVENTIONAL_SUFFICES`.

That result retires D as a competing analysis methodology. Do not attempt to rescue D, rerun D-vs-N comparisons, or prove that a special architecture is needed.

The surviving research question is narrower:

> **When do different representations and reductions of uncertainty preserve the same warranted action, and when do they not?**

The experiment studies four pieces in parallel:

- **Lane A:** information gained versus decision value gained;
- **Lane B:** decision stability under deep uncertainty;
- **Lane C:** query-relative sufficiency and compression;
- **Lane D:** stopping versus further observation under residual uncertainty.

The goal is not to invent new mathematics. Use established mathematics wherever it solves the problem. The goal is to obtain exact, reproducible results and identify whether any nontrivial interface/composition question remains.

No global-affairs examples. No Writ product assumptions. No game theory in Lanes A–D. No LLM evaluation. Codex is only the computational assistant.

---

## 1. Parallel execution protocol

Run Lanes A, B, C, and D in **four separate Codex chats from the same frozen packet**.

In each chat, instruct Codex:

> Read the attached Kahneman Lab Experiment 4 packet in full. Execute only Lane [A/B/C/D] exactly as specified. Do not execute another lane, synthesis, or the optional strategic-interface gate. Produce only the required lane report.

The four lanes may run simultaneously because no lane may use another lane's result.

### Isolation rules

1. Do not edit Writ application/product code.
2. Each lane may create temporary computation scripts, but only its named Markdown report is a deliverable.
3. Do not change the search space after seeing preliminary results except where the packet explicitly defines a fallback tier.
4. Do not use a result from another lane until all four lane reports are complete.
5. Do not search the web or literature during lane execution. This is a mathematical replication/discovery run, not a novelty review.
6. If a result is standard or unsurprising, say so. Do not inflate it.
7. If the preregistered search finds nothing, report the bounded negative result. Do not manufacture a harder search after the fact.

---

## 2. Common mathematical definitions

All state, action, loss, prior, likelihood, and cost spaces are finite.

Let:

- `Θ` be the finite state space;
- `A` be the finite action space;
- `p(θ)` be a prior or current belief;
- `L(a,θ)` be loss;
- `X` be a finite observation/test;
- `K(x|θ)` be its likelihood kernel.

### Bayes risk

\[
R(p)=\min_{a\in A}\sum_{\theta\in\Theta}p(\theta)L(a,\theta).
\]

Always retain the full argmin set. Never break ties arbitrarily.

### Posterior

For an outcome with positive marginal probability,

\[
p(\theta\mid x)=\frac{p(\theta)K(x\mid\theta)}{\sum_{\theta'}p(\theta')K(x\mid\theta')}.
\]

Zero-probability outcomes are marked `NA` and are not assigned invented posteriors.

### Expected value of sample information

\[
EVSI(X)=R(p)-\sum_x P(x)R(p(\cdot\mid x)).
\]

For a test cost `c`, net information value is

\[
NV(X)=EVSI(X)-c.
\]

### Mutual information

\[
I(\Theta;X)=\sum_{\theta,x}p(\theta)K(x\mid\theta)
\log_2\frac{K(x\mid\theta)}{P(x)}.
\]

Use the convention `0 log 0 = 0`.

### Numerical discipline

- Use exact rational arithmetic for priors, likelihoods, expected losses, posteriors, Bayes risks, EVSI, regret, and dynamic-programming values wherever possible.
- Use at least 80-digit precision for logarithms/mutual information.
- A claimed strict mutual-information inequality must have a numerical gap greater than `1e-20` at 80-digit precision.
- Treat all exact rational ties as ties.
- If a theoretically nonnegative EVSI is computed as negative, investigate the implementation before continuing.

---

# LANE A — Information Gain Is Not Decision Value

## A1. Question

Find the smallest preregistered finite witness, if one exists, where two tests are ranked in opposite order by mutual information and expected decision value:

\[
I(\Theta;X_1)>I(\Theta;X_2)
\]

but

\[
EVSI(X_1)<EVSI(X_2).
\]

The point is to test the exact distinction:

\[
\text{information gained}\neq\text{decision value gained}.
\]

Do not assume a counterexample exists in the first search tier.

## A2. Search Tier 1

Use:

- `|Θ| = 2`;
- `|A| = 2`;
- binary tests `X ∈ {0,1}`;
- priors `p(θ=1)=k/8`, `k=1,...,7`;
- losses in `{0,1,2,3}`;
- require `min_a L(a,θ)=0` for each state;
- require each action to be uniquely optimal in at least one state somewhere in the loss table, so no action is globally useless;
- test likelihoods `K(1|θ) ∈ {0,1/4,1/2,3/4,1}`;
- require both tests to be informative: `K(1|θ=0) != K(1|θ=1)`;
- treat tests equivalent under binary-outcome relabeling as the same test for minimality purposes.

Enumerate exhaustively.

A qualifying witness requires both inequalities to be strict.

## A3. Fallback Tier 2

Run Tier 2 **only if Tier 1 contains no witness**.

Use:

- `|Θ| = 3`;
- `|A| = 2`;
- binary tests;
- strictly positive priors with denominator 6;
- losses in `{0,1,2}` with the same normalization and non-useless-action rule;
- likelihoods `K(1|θ) ∈ {0,1/2,1}`;
- both tests informative.

Enumerate exhaustively.

Do not create a third tier.

## A4. Required analysis

If one or more witnesses exist:

1. report the lexicographically first witness in the smallest tier;
2. show the full prior, loss table, likelihood matrices, mutual information, Bayes risk, posterior risks, and EVSI values;
3. verify both ranking inequalities independently from the enumerator's selection logic;
4. explain the mechanism in plain mathematical language: which uncertainty does the higher-MI test resolve that is relatively irrelevant to the action boundary, and why does the lower-MI test have greater decision value?
5. report how many valid ordered test pairs in that tier exhibit a strict ranking reversal, as a descriptive count only.

If no witness exists through Tier 2, report the bounded negative result without extrapolating beyond the search space.

## A5. Output

Produce only:

`kahneman_lab_4A_information_vs_decision_value.md`

End with exactly one verdict line:

- `KL4A_REVERSAL_FOUND_TIER1`
- `KL4A_REVERSAL_FOUND_TIER2`
- `KL4A_NO_REVERSAL_IN_PREREGISTERED_SPACE`

---

# LANE B — Decision Stability Under Deep Uncertainty

## B1. Question

How can large uncertainty about probabilities coexist with a stable decision, while a small change in admissible probabilities can sometimes change the optimal decision?

The lane studies **sets of admissible priors** rather than one privileged prior.

## B2. Base problem class

Use:

- `|Θ| = 2`;
- `|A| = 2`;
- priors `p(θ=1)=k/16`, `k=1,...,15`;
- losses in `{0,1,2,3,4}`;
- require `min_a L(a,θ)=0` for each state;
- require each action to be uniquely optimal in at least one state, excluding a globally dominant action.

For every distinct pair of grid priors `p,q`, define the credal line segment

\[
\mathcal P(p,q)=\{(1-t)p+tq:0\le t\le1\}.
\]

For two-state priors, total-variation diameter is `|p-q|`.

### Strong decision stability

A segment is strongly stable if the same **unique** Bayes-optimal action is optimal for every prior in the segment.

Because expected-loss differences are linear in `p`, verify stability analytically from the action-loss boundary, not by checking grid points only.

### Instability

A segment is unstable if its two endpoints have different unique Bayes-optimal actions. Locate the exact decision boundary inside the segment.

## B3. Required searches

Search exhaustively for:

1. the valid strongly stable segment with **maximum total-variation diameter**;
2. the valid unstable segment with the **smallest positive grid-endpoint diameter**;
3. for each selected witness, derive the exact Bayes action boundary as an inequality in `p`.

Then evaluate the same selected credal segments using two robust criteria:

### Γ-minimax / minimax expected loss

\[
a_{MM}\in\arg\min_a\max_{p\in\mathcal P}E_p[L(a,\theta)].
\]

### Minimax regret

\[
a_{MR}\in\arg\min_a\max_{p\in\mathcal P}
\left(E_p[L(a,\theta)]-\min_bE_p[L(b,\theta)]\right).
\]

For a line segment and linear expected losses, optimize over endpoints or analytically justify any interior candidate if needed.

## B4. Interpretation discipline

Do not call probability uncertainty “irrationality.”

The desired result is not that robust criteria always agree. Report whether:

- Bayes actions are stable across the whole credal set;
- minimax expected loss agrees with that stable action;
- minimax regret agrees or differs;
- the choice of robustness criterion itself becomes decision-relevant.

Do not claim that one robustness criterion is universally correct.

## B5. Optional fallback

Only if every maximum-diameter stable witness is trivial for a reason not excluded by the rules, repeat with `|Θ|=3`, `|A|=2`, denominator-8 priors, and line segments between grid priors. Do not otherwise expand the lane.

## B6. Output

Produce only:

`kahneman_lab_4B_deep_uncertainty_stability.md`

End with exactly one verdict line:

- `KL4B_NONTRIVIAL_STABILITY_AND_BOUNDARY_FOUND`
- `KL4B_ONLY_TRIVIAL_STABILITY_FOUND`
- `KL4B_PREREGISTERED_SEARCH_INCONCLUSIVE`

---

# LANE C — Query-Relative Sufficiency and Compression

## C1. Question

For a finite decision problem, what can be forgotten while preserving the answers to a specified class of future decision queries?

This lane explicitly treats decision sufficiency as a **property of a representation**, not as a competing analysis methodology.

## C2. Full finite object

Each full object is

\[
F=(p,L,K)
\]

with:

- `|Θ|=2`;
- `|A|=2`;
- one binary test `X`;
- priors `p(θ=1) ∈ {1/4,1/2,3/4}`;
- losses in `{0,1,2}`;
- require `min_a L(a,θ)=0` for each state;
- require each action to be uniquely optimal in at least one state somewhere in the loss table;
- likelihoods `K(1|θ) ∈ {0,1/2,1}`.

Enumerate every valid full object. Preserve zero-probability outcomes as `NA`.

## C3. Nested downstream query families

Define exact query signatures.

### Q0 — Current decision

\[
\sigma_0(F)=\text{current Bayes-optimal action set}.
\]

### Q1 — One-step contingent policy

\[
\sigma_1(F)=\left(\sigma_0(F),\;A^*_0(F),\;A^*_1(F)\right)
\]

where `A*_x` is the Bayes-optimal action set after observing `x`, or `NA` if outcome `x` has zero probability.

### Q2 — Policy plus value of information

\[
\sigma_2(F)=\left(\sigma_1(F),EVSI(F)\right).
\]

EVSI is exact rational.

### Q3 — Q2 plus loss-revision queries

For each of the four loss cells `(a,θ)`, form a downstream query that adds `+1` to that single loss cell while holding `p` and `K` fixed, then asks for the new current Bayes-optimal action set.

`σ3(F)` is `σ2(F)` plus the ordered answers to all four such perturbation queries.

Do not renormalize the perturbed loss table.

## C4. Q-equivalence

For each `j ∈ {0,1,2,3}`, define

\[
F\sim_{Q_j}F'\iff\sigma_j(F)=\sigma_j(F').
\]

This quotient is the exact extensional notion of what the defined future query family can distinguish.

Verify that the partitions monotonically refine:

\[
Q_0\preceq Q_1\preceq Q_2\preceq Q_3.
\]

## C5. Candidate summaries

Evaluate at least these summaries:

1. `S_action` = current optimal action set only;
2. `S_policy` = current action set + post-outcome action sets;
3. `S_certificate` = `S_policy + EVSI`;
4. `S_pL` = `(p,L)` only;
5. `S_pK` = `(p,K)` only;
6. `S_full` = `(p,L,K)`.

A summary `S` is sufficient for `Qj` iff no two full objects share the same summary while having different `σj`.

For every summary/query-family pair, determine:

- sufficient or insufficient;
- number of summary equivalence classes;
- number of `Qj` equivalence classes;
- if insufficient, the smallest witness pair `F,F'` with the same summary but different query signature;
- if sufficient, whether it overpreserves relative to the exact `Qj` quotient.

Do not call the quotient a practical data structure. It is a mathematical benchmark.

## C6. Key gate object

Pay special attention to `S_certificate` for `Q2`.

Determine whether there exist **at least two genuinely different full objects** `(p,L,K)` that map to the same `S_certificate` and therefore cannot be distinguished by Q2.

If yes, record a canonical pair. This pair is the only object that may later justify a strategic-interface follow-on.

Do not run that follow-on in this lane.

## C7. Output

Produce only:

`kahneman_lab_4C_query_sufficiency_quotients.md`

End with exactly one verdict line:

- `KL4C_NONTRIVIAL_QUERY_RELATIVE_COMPRESSION_FOUND`
- `KL4C_ONLY_FULL_OBJECT_SUFFICIENT_FOR_Q2_OR_HIGHER`
- `KL4C_PREREGISTERED_SEARCH_INCONCLUSIVE`

---

# LANE D — Stop or Observe Under Residual Uncertainty

## D1. Question

When should a rational finite-horizon agent stop acquiring information and act, even though uncertainty remains?

This lane tests whether the **amount of uncertainty alone** determines whether further observation is worthwhile.

## D2. Sequential model

Use:

- states `Θ={0,1}`;
- terminal actions `A={0,1}`;
- correct-action loss `0`;
- false-positive loss `C10` for choosing action 1 when `θ=0`;
- false-negative loss `C01` for choosing action 0 when `θ=1`;
- one repeatable binary signal with symmetric accuracy `q`:

\[
P(X=1\mid\theta=1)=q,\qquad P(X=1\mid\theta=0)=1-q;
\]

- each observation costs `c`;
- at most `h` observations remain.

Parameter grid:

- initial prior `p=P(θ=1)=k/20`, `k=1,...,19`;
- `q ∈ {3/5,2/3,3/4,4/5,9/10}`;
- `C10,C01 ∈ {1,2,4,8}`;
- `c ∈ {1/100,1/50,1/20,1/10,1/5,1/2}`;
- horizon `h=1,...,5`.

## D3. Dynamic program

Terminal Bayes risk is

\[
R(p)=\min\{pC_{01},(1-p)C_{10}\}.
\]

Define

\[
V_0(p)=R(p)
\]

and for `h>=1`

\[
V_h(p)=\min\left\{R(p),\;c+\sum_xP(x\mid p)V_{h-1}(p_x)\right\}.
\]

The first term is `STOP`; the second is `OBSERVE`.

Use exact rational arithmetic for all values and posteriors. If tied exactly, record `TIE`; do not force `STOP` or `OBSERVE`.

For descriptive uncertainty only, compute binary entropy

\[
H(p)=-p\log_2 p-(1-p)\log_2(1-p)
\]

at high precision.

## D4. Required witness searches

Search the full grid for:

### Witness D-HIGH-STOP

A case with:

- `H(p) >= 0.9` bits;
- horizon `h=5`;
- `STOP` strictly optimal immediately.

### Witness D-LOW-OBSERVE

A case with:

- `H(p) <= 0.3` bits;
- horizon `h=5`;
- `OBSERVE` strictly optimal immediately.

### Witness D-MULTISTEP

A case, if one exists, where the **one-step** net information value is nonpositive,

\[
EVSI_1(p)-c\le0,
\]

but with at least two observations available the dynamic program strictly chooses `OBSERVE` because of the option value of sequential information.

Search `h=2,...,5` and report the smallest horizon where such a witness exists.

If no D-MULTISTEP witness exists in the preregistered grid, report that bounded negative result. Do not enlarge the grid.

## D5. Policy structure

For each of the three selected witnesses, show:

- prior entropy;
- terminal action and terminal Bayes risk;
- one-step EVSI;
- observation cost;
- dynamic-programming value;
- initial `STOP/OBSERVE/TIE` choice;
- the immediate posterior beliefs after each possible signal;
- the next-step policy at those beliefs.

Then explain why entropy alone is insufficient: action losses, signal quality, cost, and future option value affect whether uncertainty is worth reducing.

## D6. Output

Produce only:

`kahneman_lab_4D_stop_or_observe.md`

End with exactly one verdict line:

- `KL4D_ENTROPY_NOT_SUFFICIENT_FOR_STOPPING`
- `KL4D_ONLY_PARTIAL_WITNESSES_FOUND`
- `KL4D_PREREGISTERED_SEARCH_INCONCLUSIVE`

---

# AFTER ALL FOUR LANES — Synthesis protocol

Do not run synthesis until A, B, C, and D are complete.

Start a **new Codex chat**. Supply this packet plus all four lane reports and instruct:

> Execute only the KL4 synthesis protocol. Treat all four completed lane reports as frozen evidence. Do not rerun searches to rescue a preferred interpretation. Verify arithmetic only where reports conflict or contain an internal inconsistency. Produce only `kahneman_lab_4S_synthesis.md`.

## S1. Required synthesis questions

1. What exact distinction did Lane A establish between information quantity and decision value?
2. What did Lane B establish about probability uncertainty versus decision stability, and did robustness criteria themselves create consequential disagreement?
3. What did Lane C establish about query-relative sufficiency? Which representations were sufficient only because the downstream query class was narrow?
4. What did Lane D establish about uncertainty, observation cost, and stopping?
5. Which findings are direct consequences of standard definitions, and which expose a nontrivial interface/composition issue worth another exact experiment?
6. Did any KL2/KL3 concept earn continued use? In particular:
   - retain decision sufficiency only as a representation property if supported;
   - retain common-completion/compatibility machinery only if a KL4 result actually requires combining mutually constrained models;
   - do not preserve D as a methodology merely for continuity.
7. Does the evidence support a coherent minimal mosaic involving:
   - Bayesian decision theory;
   - information/value-of-information;
   - deep-uncertainty/robust decision criteria;
   - query-relative sufficiency;
   - sequential stopping?
8. Is there an unresolved mathematical question at the **interface** between two of these components, rather than merely a desire to combine them?

## S2. Stopping discipline

A positive educational result is not automatically a reason to continue a research programme.

If A–D are completely handled by existing mathematics and the synthesis identifies no precise unresolved interface question, return:

`KL4_STOP_EXISTING_MATH_SUFFICES`

This does **not** mean the mathematics is useless. It means it should be learned/applied rather than expanded as a distinctive research programme.

If there is a precise unresolved single-agent representation/composition question with an exact next experiment, return:

`KL4_CONTINUE_SINGLE_AGENT_INTERFACE`

If and only if the strategic-interface gate below is satisfied, return:

`KL4_STRATEGIC_INTERFACE_ELIGIBLE`

Do not claim mathematical novelty in any verdict.

---

# OPTIONAL FUTURE LANE E — Strategic Interface Gate

**Do not run Lane E now. Do not design its detailed game before synthesis.**

The purpose is not to add game theory to Writ. It is to test one narrow possible connection to compositional/open-game ideas:

> **Can two full decision models be indistinguishable under a defined single-agent decision certificate, yet become distinguishable once that certificate crosses an interface to another strategically responding agent?**

Lane E becomes eligible only if Lane C identifies a canonical pair `F,F'` such that:

1. `F != F'` as full objects;
2. `S_certificate(F)=S_certificate(F')`;
3. the certificate is sufficient for the preregistered Q2 single-agent query family;
4. therefore the pair is genuinely indistinguishable for those single-agent uses.

If those conditions do not hold, do not run Lane E.

If they do hold, the next step is to write a **new sealed preregistration** using that exact pair. The new experiment may introduce one minimal second agent and one strategic response, then test whether the formerly sufficient interface remains sufficient for equilibrium/best-response behavior.

Do not invoke category theory, open games, Bayesian games, or international-security examples unless the minimal two-agent problem actually requires them.

The point of Lane E would be to test the hypothesized gap between:

\[
\text{single-agent decision sufficiency}
\]

and

\[
\text{strategic/interface sufficiency}.
\]

It is a contingent follow-on, not part of KL4 A–D.

---

# Scientific interpretation rule

The most desirable outcome is not necessarily `CONTINUE`.

A clean result that says established mathematics completely handles the problem is scientifically successful and should stop unnecessary architecture-building.

A continuation is justified only by an exact residual question that survives the four-lane experiment.
