# Kahneman Lab Experiment 4B — Decision Stability Under Deep Uncertainty

The exhaustive preregistered search finds a nontrivial strongly stable credal segment with maximum total-variation diameter **11/16**, and an unstable segment with minimum positive grid-endpoint diameter **1/16**. Both robust criteria select the same unique action on each selected segment. Thus these witnesses establish the contrast between probability uncertainty and decision stability, but do not establish disagreement between robustness criteria.

## Scope and exact enumeration

Only Lane B was executed, using the supplied `RUN_THIS_NEXT_KAHNEMAN_LAB_4_PARALLEL.md` packet. No other lane, synthesis, strategic-interface gate, web search, or literature search was executed. No Writ application or product code was changed.

States and actions are labeled `0,1`. Write `p=P(θ=1)`, so the full prior is `(1−p,p)`. Loss-table rows index actions and columns index states. Every one of the `5^4=625` labeled tables with entries in `{0,1,2,3,4}` was checked against both validity requirements:

- Each state has minimum action loss zero.
- Each action is uniquely optimal in at least one state.

Exactly **32** tables qualify. For each, all **105** unordered endpoint pairs `p<q` from `{1/16,…,15/16}` were examined, totaling **3,360 distinct table–segment cases**. Reversing the endpoints defines the same credal segment and is not counted twice. State and action labels were retained.

All calculations used exact rational arithmetic. Bayes action sets retained every minimizer. Segments touching a decision boundary at an endpoint were excluded from both the strongly stable and endpoint-unstable categories, as required by their uniqueness conditions.

The packet does not specify how to select among witnesses tied on the requested diameter. Before computation, the selection rule was fixed as lexicographic order on `(L00,L01,L10,L11,p,q)` after optimizing the diameter. This selects witnesses without breaking action ties.

| Classification or extremum | Exact result |
|---|---:|
| Strongly stable table–segment cases | 1,692 |
| Unstable cases with different unique endpoint actions | 1,500 |
| Cases with at least one tied endpoint | 168 |
| Maximum strongly stable diameter | 11/16 |
| Witnesses attaining that maximum | 4 |
| Minimum unstable diameter | 1/16 |
| Witnesses attaining that minimum | 20 |

These categories sum to 3,360. No fallback search was run.

## Analytic classification and extremality

The validity conditions force every table, up to swapping action rows, to have the form

\[
L=\begin{pmatrix}0&u\\v&0\end{pmatrix},\qquad u,v\in\{1,2,3,4\}.
\]

The expected losses and their difference are

\[
\ell_0(p)=up,\qquad \ell_1(p)=v(1-p),\qquad
D(p)=\ell_0(p)-\ell_1(p)=(u+v)p-v.
\]

The exact Bayes boundary is `b=v/(u+v)`: the action set is `{0}` for `p<b`, `{0,1}` at `p=b`, and `{1}` for `p>b`. Swapping rows reverses the action labels without changing the boundary.

For any segment `[p,q]`, the difference at an interior prior is

\[
D((1-t)p+tq)=(1-t)D(p)+tD(q),\qquad 0\le t\le1.
\]

Strictly same-sign endpoint differences therefore prove a unique common optimal action at **every real prior** in the segment, not merely its grid points. Opposite signs prove different unique endpoint actions and a unique boundary strictly inside. An endpoint difference of zero is an exact tie.

Since `1/5≤b≤4/5`, a strongly stable segment below a boundary cannot have its upper grid endpoint above `12/16`; its lower endpoint is at least `1/16`. Its diameter is consequently at most `11/16`. Above a boundary, its lower endpoint is at least `4/16` and its upper endpoint at most `15/16`, giving the same bound. The selected stable witness attains this bound.

Every positive grid-endpoint diameter is at least `1/16`. The selected unstable witness attains that bound with its boundary strictly between adjacent grid priors. These arguments independently establish both extrema.

The four maximum-diameter stable witnesses are:

| Row-major loss tuple | Credal segment |
|---|---|
| `(0,1,4,0)` | `[1/16,12/16]` |
| `(0,4,1,0)` | `[4/16,15/16]` |
| `(1,0,0,4)` | `[4/16,15/16]` |
| `(4,0,0,1)` | `[1/16,12/16]` |

None relies on a globally dominant action or identical action losses. Each has a genuine action boundary inside `(0,1)`. The fallback condition is therefore not met.

## Selected maximum-diameter strongly stable witness

| Action | Loss at θ=0 | Loss at θ=1 |
|---|---:|---:|
| 0 | 0 | 1 |
| 1 | 4 | 0 |

The credal segment has scalar endpoints `p=1/16` and `q=3/4`, corresponding to full priors `(15/16,1/16)` and `(1/4,3/4)`. Its total-variation diameter is

\[
\frac34-\frac1{16}=\frac{11}{16}.
\]

The expected losses are `ℓ0(p)=p` and `ℓ1(p)=4(1−p)`. Therefore

\[
A^*(p)=
\begin{cases}
\{0\},&p<4/5,\\
\{0,1\},&p=4/5,\\
\{1\},&p>4/5.
\end{cases}
\]

Every prior in `[1/16,3/4]` is strictly below `4/5`. Action 0 is uniquely optimal throughout, and the Bayes risk is `R(p)=p` there. The smallest advantage over action 1 on the segment is `4−5(3/4)=1/4`, so stability is strict even at its least favorable endpoint.

| Prior p | ℓ0(p) | ℓ1(p) | Bayes action set | R(p) | Regret of 0 | Regret of 1 |
|---|---:|---:|---|---:|---:|---:|
| 1/16 | 1/16 | 15/4 | `{0}` | 1/16 | 0 | 59/16 |
| 3/4 | 3/4 | 1 | `{0}` | 3/4 | 0 | 1/4 |

| Robust criterion | Objective for action 0 | Objective for action 1 | Full argmin set |
|---|---:|---:|---|
| Γ-minimax expected loss | 3/4 | 15/4 | `{0}` |
| Minimax regret | 0 | 59/16 | `{0}` |

This is nontrivial stability under the stated rules: action 1 is uniquely optimal in state 1 and for priors above `4/5`, yet action 0 remains uniquely warranted over a segment of diameter `11/16` that crosses `p=1/2`. Probability uncertainty is broad while all admissible priors remain on the same side of the loss-dependent action boundary.

## Selected minimum-diameter unstable witness

| Action | Loss at θ=0 | Loss at θ=1 |
|---|---:|---:|
| 0 | 0 | 1 |
| 1 | 2 | 0 |

The scalar endpoints are `p=5/8` and `q=11/16`, corresponding to full priors `(3/8,5/8)` and `(5/16,11/16)`. Their total-variation distance is `1/16`.

The expected losses are `ℓ0(p)=p` and `ℓ1(p)=2(1−p)`. Hence

\[
A^*(p)=
\begin{cases}
\{0\},&p<2/3,\\
\{0,1\},&p=2/3,\\
\{1\},&p>2/3.
\end{cases}
\]

The boundary lies strictly inside the segment:

\[
\frac58<\frac23<\frac{11}{16},\qquad
\frac23-\frac58=\frac1{24},\qquad
\frac{11}{16}-\frac23=\frac1{48}.
\]

In the segment parameterization `(1−t)(5/8)+t(11/16)`, the boundary occurs at `t=2/3`. The Bayes risk is `R(p)=min{p,2(1−p)}`; at the boundary it is `2/3` and both actions are optimal.

| Prior p | ℓ0(p) | ℓ1(p) | Bayes action set | R(p) | Regret of 0 | Regret of 1 |
|---|---:|---:|---|---:|---:|---:|
| 5/8 | 5/8 | 3/4 | `{0}` | 5/8 | 0 | 1/8 |
| 11/16 | 11/16 | 5/8 | `{1}` | 5/8 | 1/16 | 0 |

| Robust criterion | Objective for action 0 | Objective for action 1 | Full argmin set |
|---|---:|---:|---|
| Γ-minimax expected loss | 11/16 | 3/4 | `{0}` |
| Minimax regret | 1/16 | 1/8 | `{0}` |

The full segment has no common Bayes-optimal action. Both robust criteria nevertheless uniquely select action 0. That robust choice is not a claim that action 0 is Bayes-optimal at every admissible prior: action 1 is uniquely Bayes-optimal above `2/3`.

## Why endpoint optimization is sufficient

For a fixed action, expected loss is affine in the prior, so its maximum over a closed line segment occurs at an endpoint. This directly justifies the Γ-minimax calculations.

Regret is

\[
g_a(p)=\ell_a(p)-\min_b\ell_b(p)
       =\max_b\bigl(\ell_a(p)-\ell_b(p)\bigr).
\]

It is a maximum of affine functions, hence convex. At any interior point, convexity bounds it by the corresponding convex combination of endpoint regrets, which is at most the larger endpoint regret. Endpoint maximization therefore also gives the exact worst-case regret. The unstable witness's interior boundary gives zero regret for both actions and cannot increase either worst case. The criteria here optimize over the specified two actions; no randomized action space was introduced.

## Interpretation

The selected stable segment has eleven times the diameter of the selected unstable segment. The selected witnesses have different loss tables; this comparison establishes existence across the specified problem class. Its mechanism is exact: uncertainty width alone does not determine whether a credal set stays inside one action region or crosses an action boundary.

For the stable witness, Bayes actions are stable across the whole credal set, and both Γ-minimax and minimax regret agree with that unique action. Indeed, in this finite two-action setting, strict pointwise superiority on a compact segment has a positive minimum loss margin, forcing agreement under minimax expected loss as well as zero worst-case regret for the stable action.

For the unstable witness, endpoint Bayes actions differ, but the two robust criteria agree with each other. **The choice between these robustness criteria is not decision-relevant for either selected witness.** This does not assert universal agreement, or that either criterion is universally correct; the robust comparison was performed on the two selected segments as specified.

These findings are standard consequences of affine expected losses, threshold decisions, and convex regret. They do not establish mathematical novelty. Probability uncertainty is not characterized as irrationality.

## Reproduction and independent verification

The following self-contained Python 3 code reproduces the exhaustive search, its counts and witness selection, and the robust objective values using only the standard library. The final integer-sign enumeration independently checks classification totals and extrema through the forced loss-table structure, without using the enumerator's expected-loss or argmin functions. The displayed analytic arguments additionally verify continuous-segment stability and both diameter bounds.

```python
from fractions import Fraction as F
from itertools import product, combinations
from collections import Counter

P = [F(k, 16) for k in range(1, 16)]

def loss(c, p):
    return ((1-p)*c[0] + p*c[1], (1-p)*c[2] + p*c[3])

def argmin(values):
    return tuple(a for a in range(2) if values[a] == min(values))

valid, stable, unstable, endpoint_ties = [], [], [], []
for c in product(range(5), repeat=4):
    L = (c[:2], c[2:])
    if any(min(L[a][s] for a in range(2)) != 0 for s in range(2)):
        continue
    if any(not any(L[a][s] < L[1-a][s] for s in range(2))
           for a in range(2)):
        continue
    valid.append(c)
    for p, q in combinations(P, 2):
        ap, aq = argmin(loss(c, p)), argmin(loss(c, q))
        row = (c, p, q, q-p)
        if len(ap) == len(aq) == 1:
            (stable if ap == aq else unstable).append(row)
        else:
            endpoint_ties.append(row)

maximum = max(r[3] for r in stable)
minimum = min(r[3] for r in unstable)
S = [r for r in stable if r[3] == maximum]
U = [r for r in unstable if r[3] == minimum]
s, u = min(S), min(U)
assert len(valid) == 32
assert (len(stable), len(unstable), len(endpoint_ties)) == (1692, 1500, 168)
assert (len(S), len(U)) == (4, 20)
assert s == ((0, 1, 4, 0), F(1,16), F(12,16), F(11,16))
assert u == ((0, 1, 2, 0), F(10,16), F(11,16), F(1,16))

def robust(row):
    c, p, q, _ = row
    endpoints = (loss(c, p), loss(c, q))
    mm = tuple(max(v[a] for v in endpoints) for a in range(2))
    mr = tuple(max(v[a]-min(v) for v in endpoints) for a in range(2))
    return mm, argmin(mm), mr, argmin(mr)

assert robust(s) == ((F(3,4), F(15,4)), (0,),
                     (F(0), F(59,16)), (0,))
assert robust(u) == ((F(11,16), F(3,4)), (0,),
                     (F(1,16), F(1,8)), (0,))

# Independent exact classification via integer boundary signs.
counts = Counter()
stable_widths, unstable_widths = [], []
for x in range(1, 5):
    for y in range(1, 5):
        for k in range(1, 16):
            for m in range(k+1, 16):
                left = (x+y)*k - 16*y
                right = (x+y)*m - 16*y
                if left*right > 0:
                    counts['stable'] += 2  # Both action-row orientations.
                    stable_widths.append(m-k)
                elif left*right < 0:
                    counts['unstable'] += 2
                    unstable_widths.append(m-k)
                else:
                    counts['endpoint_ties'] += 2
assert counts == Counter(stable=1692, unstable=1500, endpoint_ties=168)
assert F(max(stable_widths), 16) == maximum == F(11,16)
assert F(min(unstable_widths), 16) == minimum == F(1,16)
print('All exact checks passed.')
print('Stable:', s, robust(s))
print('Unstable:', u, robust(u))
```

KL4B_NONTRIVIAL_STABILITY_AND_BOUNDARY_FOUND
