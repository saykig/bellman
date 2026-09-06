# Kahneman Lab Experiment 4 — Lane D: Stop or Observe

All three required witnesses exist in the preregistered grid. High entropy can coexist with strictly optimal stopping; low entropy can coexist with strictly optimal observation. A strictly negative one-step net information value can coexist with strictly optimal observation at horizon **2**, the smallest eligible multistep horizon. These are standard consequences of Bayesian decision theory and finite-horizon optimal stopping, not claims of mathematical novelty.

## Scope and computation

Only Lane D was executed. The full packet was read; no other lane, synthesis, strategic-interface gate, web search, or literature search was executed. No Writ application or product code was changed.

The exhaustive grid was:

- Initial prior: `p = k/20`, `k = 1,…,19`.
- Symmetric signal accuracy: `q ∈ {3/5, 2/3, 3/4, 4/5, 9/10}`.
- Losses: `C10,C01 ∈ {1,2,4,8}`.
- Observation cost: `c ∈ {1/100,1/50,1/20,1/10,1/5,1/2}`.
- Remaining observations: `h ∈ {1,2,3,4,5}`.

This gives 9,120 parameter tuples and **45,600 initial parameter-and-horizon evaluations**. Repeated observations use the same likelihood conditional on the state, as in the packet's belief-state recurrence. Reachable posterior beliefs were evaluated exactly, without rounding or projection onto the initial-prior grid.

Before inspecting results, witness selection was fixed to ascending numerical lexicographic order `(p,q,C10,C01,c)`; D-MULTISTEP instead orders `(h,p,q,C10,C01,c)`. This resolves a selection convention left unspecified in the packet without changing its search space.

All priors, likelihoods, posteriors, losses, costs, EVSI, and DP values used Python standard-library `Fraction` arithmetic. Entropy used `Decimal` logarithms at 100 significant digits; displayed entropies below are rounded. No floating-point tolerance was used for decisions. Every exact decision tie was retained as `TIE`, and terminal actions were retained as full argmin sets. All reachable outcomes have positive probability because all priors and likelihoods are strictly interior; no invented posterior or `NA` case was needed.

Write the forced-observation cost as

\[
O_h(p)=c+\sum_x m_xV_{h-1}(p_x),\qquad V_h(p)=\min\{R(p),O_h(p)\}.
\]

Here

\[
m_1=pq+(1-p)(1-q),\quad m_0=p(1-q)+(1-p)q,
\]

\[
p_1=\frac{pq}{m_1},\qquad p_0=\frac{p(1-q)}{m_0}.
\]

Stopping selects terminal action 0 for `p < C10/(C10+C01)`, action 1 for `p > C10/(C10+C01)`, and the full set `{0,1}` at equality. Costs in the following tables are future costs from the stated belief, excluding already paid observation costs.

## Exhaustive search results

| Remaining horizon | Strict STOP | Strict OBSERVE | TIE | Total |
|---:|---:|---:|---:|---:|
| 1 | 6,074 | 2,959 | 87 | 9,120 |
| 2 | 4,618 | 4,473 | 29 | 9,120 |
| 3 | 4,088 | 4,997 | 35 | 9,120 |
| 4 | 3,896 | 5,195 | 29 | 9,120 |
| 5 | 3,820 | 5,271 | 29 | 9,120 |

There are **1,012 D-HIGH-STOP cases** and **278 D-LOW-OBSERVE cases** at horizon 5. Entropy eligibility comprises `p ∈ {7/20,8/20,…,13/20}` for high entropy and `p ∈ {1/20,19/20}` for low entropy.

| Horizon | Cases with `EVSI₁−c ≤ 0` and strict OBSERVE |
|---:|---:|
| 2 | 1,514 |
| 3 | 2,038 |
| 4 | 2,236 |
| 5 | 2,312 |

These counts include the original labeled grid without symmetry reduction. Counts across horizons can include the same parameter tuple and are descriptive, not independent replications.

## D-HIGH-STOP

Selected parameters: **`p=7/20, q=3/5, C10=1, C01=1, c=1/20, h=5`**.

| Quantity | Result |
|---|---|
| Prior entropy | `0.934068055375491006007701943191397816` bits, above `0.9` |
| Terminal optimal action set | `{0}` |
| Terminal Bayes risk `R(p)` | `7/20` |
| One-step EVSI | `0` |
| Observation cost | `1/20` |
| One-step net value | `−1/20` |
| Forced-observation cost `O₅(p)` | `2/5` |
| DP value `V₅(p)` | `7/20` |
| Initial choice | **STOP**, strictly |

The immediate posterior policies below are counterfactual: the optimal initial policy does not take this observation.

| Signal | Marginal probability | Posterior `pₓ` | Remaining `h` | Terminal action set | STOP cost | OBSERVE cost | DP value | Next choice |
|---|---:|---:|---:|---|---:|---:|---:|---|
| 0 | `53/100` | `14/53` | 4 | `{0}` | `14/53` | `333/1060` | `14/53` | STOP |
| 1 | `47/100` | `21/47` | 4 | `{0}` | `21/47` | `211/470` | `21/47` | STOP |

Both next choices are strict. In particular, `211/470−21/47=1/470>0`. Thus

\[
O_5=\frac1{20}+\frac{53}{100}\frac{14}{53}
+\frac{47}{100}\frac{21}{47}=\frac25>\frac7{20}.
\]

Both immediate posteriors remain below the terminal action boundary `1/2`. Their expected terminal risk is `7/20`, so one-step EVSI is zero. Even with four subsequent observations available, continuation at either immediate posterior is too expensive. High residual entropy does not justify the observation cost.

## D-LOW-OBSERVE

Selected parameters: **`p=1/20, q=3/5, C10=1, C01=8, c=1/100, h=5`**.

| Quantity | Result |
|---|---|
| Prior entropy | `0.286396957115956128766475977727897474` bits, below `0.3` |
| Terminal optimal action set | `{0}` |
| Terminal Bayes risk `R(p)` | `2/5` |
| One-step EVSI | `0` |
| Observation cost | `1/100` |
| One-step net value | `−1/100` |
| Forced-observation cost `O₅(p)` | `94039/250000` |
| DP value `V₅(p)` | `94039/250000` |
| Initial choice | **OBSERVE**, strictly |

| Signal | Marginal probability | Posterior `pₓ` | Remaining `h` | Terminal action set | STOP cost | OBSERVE cost | DP value | Next choice |
|---|---:|---:|---:|---|---:|---:|---:|---|
| 0 | `59/100` | `2/59` | 4 | `{0}` | `16/59` | `693/2500` | `16/59` | STOP |
| 1 | `41/100` | `3/41` | 4 | `{0}` | `24/41` | `51539/102500` | `51539/102500` | OBSERVE |

Both next choices are strict. The initial observation value is independently recoverable from these branches:

\[
O_5=\frac1{100}+\frac{59}{100}\frac{16}{59}
+\frac{41}{100}\frac{51539}{102500}
=\frac{94039}{250000}<\frac25.
\]

The reduction in expected total loss, including observation costs, is `5961/250000`. The rare state has false-negative loss 8, moving the action boundary to `1/9`. Both immediate posteriors remain below it, so one observation followed by mandatory action has zero EVSI. Further favorable signals can cross that boundary; the optimal policy stops after signal 0 and continues after signal 1.

The same tuple's horizon values show where future opportunities become useful:

| Horizon | `Vₕ(p)` | Initial choice |
|---:|---:|---|
| 0 | `2/5` | Terminal action `{0}` |
| 1 | `2/5` | STOP |
| 2 | `2/5` | STOP |
| 3 | `1951/5000` | OBSERVE |
| 4 | `97249/250000` | OBSERVE |
| 5 | `94039/250000` | OBSERVE |

## D-MULTISTEP

Selected parameters: **`p=1/20, q=2/3, C10=1, C01=8, c=1/100, h=2`**. Horizon **2** is the smallest qualifying horizon in the preregistered search.

| Quantity | Result |
|---|---|
| Prior entropy | `0.286396957115956128766475977727897474` bits |
| Terminal optimal action set | `{0}` |
| Terminal Bayes risk `R(p)` | `2/5` |
| One-step EVSI | `0` |
| Observation cost | `1/100` |
| One-step net value | `−1/100 < 0` |
| One-observation forced cost `O₁(p)` | `41/100` |
| One-observation value `V₁(p)` | `2/5`, strict STOP |
| Two-observation forced cost `O₂(p)` | `6143/18000` |
| DP value `V₂(p)` | `6143/18000` |
| Initial choice with two available | **OBSERVE**, strictly |

| Signal | Marginal probability | Posterior `pₓ` | Remaining `h` | Terminal action set | STOP cost | OBSERVE cost | DP value | Next choice |
|---|---:|---:|---:|---|---:|---:|---:|---|
| 0 | `13/20` | `1/39` | 1 | `{0}` | `8/39` | `839/3900` | `8/39` | STOP |
| 1 | `7/20` | `2/21` | 1 | `{0}` | `16/21` | `509/900` | `509/900` | OBSERVE |

Both next choices are strict. Neither first signal changes the terminal optimal action, establishing `EVSI₁=0`. Following signal 1, however, the next observation has EVSI `13/63` and net value `1237/6300>0`.

After first signal 1, the second signal has probabilities `40/63` for 0 and `23/63` for 1. The corresponding terminal beliefs are `1/20` and `4/23`; their full optimal action sets are `{0}` and `{1}`. The latter belief crosses the action boundary `1/9`.

Consequently,

\[
O_2=\frac1{100}+\frac{13}{20}\frac8{39}
+\frac7{20}\frac{509}{900}
=\frac{6143}{18000}<\frac25,
\]

with strict improvement `1057/18000`. As a direct policy check, observe once; stop with action 0 after signal 0; after signal 1 observe again, then choose action 1 exactly when the second signal is also 1. Its expected terminal loss is

\[
\underbrace{\frac1{20}\,8\left(1-\frac49\right)}_{\text{false negatives}}
+\underbrace{\frac{19}{20}\frac19}_{\text{false positives}}
=\frac{59}{180}.
\]

The expected observation count is `1+7/20=27/20`, so its expected observation cost is `27/2000`. Their sum is exactly `6143/18000`. The first observation is worthwhile because it can lead to a valuable second observation, despite having no immediate terminal decision value on its own.

## Verification and reproducibility

The exhaustive enumerator applied this recursion at every parameter tuple and initial horizon:

```text
R(p) = min(p*C01, (1-p)*C10)
V(p, 0) = R(p)
V(p, h) = min(R(p), c + m0*V(p0, h-1) + m1*V(p1, h-1))
EVSI1(p) = R(p) - m0*R(p0) - m1*R(p1)
choice = STOP if R < O; OBSERVE if O < R; TIE otherwise
```

It memoized exact `(p,h)` values within each parameter tuple. All 45,600 evaluations passed checks that one-step EVSI is nonnegative, `Vₕ≤R`, and `Vₕ≤Vₕ₋₁`. Counts sum to 9,120 at every horizon. The entropy thresholds lie well away from their nearest grid entropies: the adjacent high-threshold values are approximately `0.8812908992` and `0.9340680554`; the adjacent low-threshold values are approximately `0.2863969571` and `0.4689955936`.

A separate, non-memoized verifier used unnormalized joint state masses, avoiding the enumerator's posterior construction and expectation weights. For state masses `(w0,w1)`, it computed

\[
W_0(w_0,w_1)=\min\{w_1C_{01},w_0C_{10}\},
\]

\[
W_h(w_0,w_1)=\min\left\{
W_0(w_0,w_1),\;(w_0+w_1)c
+W_{h-1}(w_0q,w_1(1-q))
+W_{h-1}(w_0(1-q),w_1q)
\right\}.
\]

For all selected witnesses, this independently matched every initial value from horizon 1 through the selected horizon, both immediate posterior optimal values, and the initial forced-observation value exactly. One-step EVSI was independently checked using the sum of the two outcomes' minimum joint-mass losses. The explicit D-MULTISTEP policy calculation above supplies an additional direct check.

## Interpretation

Entropy describes uncertainty about the state, but the stopping decision compares expected action loss with the cost of an adaptive information policy. Loss asymmetry determines the action boundary and the consequence of an error; signal quality determines reachable posterior beliefs; observation cost determines whether improvements are worth paying for; remaining horizon creates opportunities to condition later observations on earlier outcomes.

The high-entropy and low-entropy witnesses establish the requested opposing cases. There is also a same-entropy check within the unchanged grid: hold the D-LOW-OBSERVE prior, signal, losses, and horizon fixed and change only `c` to `1/2`. Every forced observation costs at least `1/2`, exceeding the stopping risk `2/5`, so STOP is strictly optimal. At `c=1/100`, the reported DP strictly chooses OBSERVE. Thus identical prior entropy permits opposite choices, directly ruling out entropy alone as a sufficient stopping statistic across this problem class.

The multistep witness additionally rules out nonpositive one-step net information value as a sufficient stopping rule when later observations remain available. These results require no new mathematics and make no claim beyond the specified finite decision model.

KL4D_ENTROPY_NOT_SUFFICIENT_FOR_STOPPING
