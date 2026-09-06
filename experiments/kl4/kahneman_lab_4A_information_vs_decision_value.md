# Kahneman Lab Experiment 4 — Lane A

## Result and scope

**A strict ranking reversal exists in Tier 1.** The lexicographically first witness under the explicit ordering below has

\[
I(\Theta;X_1)>I(\Theta;X_2),\qquad
EVSI(X_1)=0<\frac1{32}=EVSI(X_2).
\]

Tier 1 was enumerated exhaustively. Tier 2 was not executed because its prerequisite was not met. No other lane, synthesis, or strategic-interface gate was executed. No web or literature search was performed, and no Writ application or product code was changed.

This is a standard distinction between mutual information and value of information for a specified loss function. The result establishes no mathematical novelty or need for a special architecture.

## Enumeration, ordering, and descriptive count

States and actions are labeled `0,1`. The packet requests lexicographic minimality without specifying a serialization; this report fixes the following convention before enumeration:

1. Ascending prior parameter \(p(1)=k/8\), \(k=1,\ldots,7\).
2. Ascending row-major loss tuple \((L(0,0),L(0,1),L(1,0),L(1,1))\).
3. Ascending likelihood vector \(t_1=(K_1(1\mid0),K_1(1\mid1))\).
4. Ascending likelihood vector \(t_2=(K_2(1\mid0),K_2(1\mid1))\).

Each test is represented by the lexicographically smaller of \(t\) and \(1-t\), which identifies binary-outcome relabelings. State and action labels are retained; no additional quotient is imposed. Thus “first” is relative to this explicit encoding, and “smallest tier” means the first successful preregistered tier, not minimality over arbitrary finite models.

The valid loss tables number **18**: each state has one zero loss and one strictly positive loss, and the two states have different uniquely optimal actions. Each orientation permits \(3\times3=9\) positive-loss choices. Of the 25 grid likelihood vectors, 20 are informative; outcome relabeling gives **10** test classes. Their canonical vectors, in order, are

\[
(0,1/4),(0,1/2),(0,3/4),(0,1),
(1/4,0),(1/4,1/2),(1/4,3/4),(1/4,1),
(1/2,0),(1/2,1/4).
\]

There are **126 prior/loss contexts** and **11,340 ordered pairs of distinct canonical tests across those contexts**: \(7\times18\times10\times9\). Including identical-test pairs would give 12,600 cases; identical pairs cannot satisfy either strict reversal. The count of strict reversals is **388**, where each counted object is \((p,L,X_1,X_2)\) with \(I(X_1)>I(X_2)\) and \(EVSI(X_1)<EVSI(X_2)\). It is a descriptive count over the specified grid, not a probability or prevalence estimate outside it.

| Prior \(p(1)\) | Strict reversals |
|---|---:|
| 1/8 | 54 |
| 1/4 | 50 |
| 3/8 | 76 |
| 1/2 | 28 |
| 5/8 | 76 |
| 3/4 | 50 |
| 7/8 | 54 |
| **Total** | **388** |

All priors, likelihoods, losses, posterior calculations, risks, and EVSI values use exact rational arithmetic. Logarithms and mutual information were computed at 100 and 120 decimal digits; the total, counts by prior, and first witness agreed. Selection required an MI gap greater than \(10^{-20}\), and an exact positive EVSI difference. The smallest qualifying MI gap was approximately \(0.0010531378820319897173437564217958878\) bits, comfortably above the threshold. No evaluated EVSI was negative. Full action argmin sets were retained, without selecting a single action in a tie. Zero-probability outcomes are handled as `NA`; none occur in the selected witness.

## First witness

The prior is

\[
\bigl(p(0),p(1)\bigr)=\left(\frac78,\frac18\right).
\]

| Loss \(L(a,\theta)\) | \(\theta=0\) | \(\theta=1\) |
|---|---:|---:|
| \(a=0\) | 0 | 1 |
| \(a=1\) | 1 | 0 |

For each likelihood matrix below, rows are states and columns are outcomes. The canonical likelihood vectors are \(t_1=(1/4,1)\) and \(t_2=(0,1/4)\). Both tests are informative.

| \(K_1(x\mid\theta)\) | \(x=0\) | \(x=1\) |
|---|---:|---:|
| \(\theta=0\) | 3/4 | 1/4 |
| \(\theta=1\) | 0 | 1 |

| \(K_2(x\mid\theta)\) | \(x=0\) | \(x=1\) |
|---|---:|---:|
| \(\theta=0\) | 1 | 0 |
| \(\theta=1\) | 3/4 | 1/4 |

Before observing either test, expected action losses are \((1/8,7/8)\), so

\[
A^*(p)=\{0\},\qquad R(p)=\frac18.
\]

### Outcomes and posterior decisions

Expected-loss columns below use the conditional posterior for the indicated outcome.

| Test | Outcome | Marginal probability | Posterior \((p(0\mid x),p(1\mid x))\) | Loss of \(a=0\) | Loss of \(a=1\) | Posterior Bayes risk | Full argmin set |
|---|---:|---:|---|---:|---:|---:|---|
| \(X_1\) | 0 | 21/32 | (1, 0) | 0 | 1 | 0 | {0} |
| \(X_1\) | 1 | 11/32 | (7/11, 4/11) | 4/11 | 7/11 | 4/11 | {0} |
| \(X_2\) | 0 | 31/32 | (28/31, 3/31) | 3/31 | 28/31 | 3/31 | {0} |
| \(X_2\) | 1 | 1/32 | (0, 1) | 1 | 0 | 0 | {1} |

Thus the expected posterior risks and EVSI values are exactly

\[
\begin{aligned}
E[R(p\mid X_1)]
 &=\frac{21}{32}\,0+\frac{11}{32}\frac4{11}=\frac18,\\
EVSI(X_1)&=\frac18-\frac18=0,\\[3pt]
E[R(p\mid X_2)]
 &=\frac{31}{32}\frac3{31}+\frac1{32}\,0=\frac3{32},\\
EVSI(X_2)&=\frac18-\frac3{32}=\frac1{32}.
\end{aligned}
\]

### Mutual information

Let \(h(z)=-z\log_2z-(1-z)\log_2(1-z)\), using \(0\log0=0\). Exact expressions are

\[
\begin{aligned}
I(\Theta;X_1)&=h(11/32)-\frac78h(1/4),\\
I(\Theta;X_2)&=h(1/32)-\frac18h(1/4).
\end{aligned}
\]

The following values in bits are rounded to 90 digits after the decimal point from the 120-digit calculation:

```text
I(Theta;X1) = 0.218493713493126372672676588254619702275090439756612336198001740360425792405429543866891085
I(Theta;X2) = 0.099212558755323033480355789293789449883117226674676326452531174348934476117839294650355987
MI gap      = 0.119281154737803339192320798960830252391973213081936009745470566011491316287590249216535098
```

## Independent verification of the rankings

The enumerator computes MI directly from the joint-probability logarithmic sum and EVSI from normalized posteriors. A separate verification calculation, independent of the selection predicate, uses the entropy identity \(I(\Theta;X)=H(X)-H(X\mid\Theta)\) and minimizes unnormalized joint expected losses. At 120 digits the entropy calculation agrees with each direct MI sum to an absolute discrepancy below \(10^{-110}\). It independently yields

\[
I(\Theta;X_1)-I(\Theta;X_2)
=h(11/32)-h(1/32)-\frac34h(1/4)
>10^{-20}.
\]

For a further exact check on decision value, under this zero-one loss the post-test expected Bayes risk is

\[
\sum_x\min\{P(\theta=1,x),P(\theta=0,x)\}.
\]

For \(X_1\), the joint pairs \((P(0,x),P(1,x))\) are \((21/32,0)\) and \((7/32,4/32)\). Their minima sum to \(4/32\). For \(X_2\), they are \((28/32,3/32)\) and \((0,1/32)\), whose minima sum to \(3/32\). Consequently

\[
EVSI(X_2)-EVSI(X_1)=\frac1{32}>0.
\]

Both ranking inequalities are therefore strict, with an exact rational decision-value gap and an MI gap far above the required numerical tolerance.

## Mechanism

Write \(q=P(\theta=1)\). The action boundary is \(q=1/2\): action 0 is uniquely optimal for \(q<1/2\), action 1 for \(q>1/2\), and both are optimal at equality. The prior \(q=1/8\) favors action 0.

The higher-MI test \(X_1\) often certifies the already more likely state 0. Its other outcome raises the probability of state 1 to \(4/11\), which remains below the action boundary. It resolves substantial uncertainty, but both outcomes leave action 0 uniquely optimal. The Bayes risk is linear throughout these posterior beliefs, so averaging their risks returns the prior risk exactly. Its decision value is zero.

The lower-MI test \(X_2\) usually leaves a posterior favoring action 0, but with marginal probability \(1/32\) it certifies state 1. That rare outcome crosses the action boundary and warrants switching to action 1, avoiding the unit loss that the original action would have incurred. Its overall entropy reduction is smaller, yet its expected loss reduction is \(1/32\).

In this two-state example there is no separate nuisance variable: the difference concerns which outcomes resolve the same state uncertainty and whether those outcomes change the loss-minimizing action. MI measures state information without using the loss table; EVSI measures how that information improves decisions under that table.

## Reproduction

The following standalone Python 3 program uses only the standard library. It reproduces the exhaustive Tier 1 count, first witness, posterior calculations, 100/120-digit agreement, and independent verification. It stops after Tier 1 because a witness exists.

```python
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
from itertools import product
from collections import Counter

def dec(q):
    return D(q.numerator) / D(q.denominator)

def action_result(weights, L):
    losses = tuple(sum(weights[s] * L[a][s] for s in range(2)) for a in range(2))
    risk = min(losses)
    return losses, risk, tuple(a for a in range(2) if losses[a] == risk)

def evaluate(p, L, t):
    current = action_result(p, L)
    expected = F(0)
    outcomes = []
    for x in (0, 1):
        joint = tuple(p[s] * (t[s] if x else 1 - t[s]) for s in range(2))
        marginal = sum(joint)
        if not marginal:
            outcomes.append((x, marginal, 'NA', 'NA'))
            continue
        posterior = tuple(v / marginal for v in joint)
        result = action_result(posterior, L)
        expected += marginal * result[1]
        outcomes.append((x, marginal, posterior, result))
    evsi = current[1] - expected
    assert evsi >= 0
    return evsi, outcomes

def mutual_information(p, t):
    result = D(0)
    for x in (0, 1):
        kernel = tuple(t[s] if x else 1 - t[s] for s in range(2))
        marginal = sum(p[s] * kernel[s] for s in range(2))
        for s in range(2):
            joint = p[s] * kernel[s]
            if joint:
                result += dec(joint) * dec(kernel[s] / marginal).ln() / D(2).ln()
    return result

grid = tuple(F(i, 4) for i in range(5))
tests = sorted({min(t, tuple(1-v for v in t))
                for t in product(grid, repeat=2) if t[0] != t[1]})
loss_tables = []
for flat in product(range(4), repeat=4):
    L = (flat[:2], flat[2:])
    if all(min(L[a][s] for a in range(2)) == 0 for s in range(2)) and all(
        any(L[a][s] < L[1-a][s] for s in range(2)) for a in range(2)
    ):
        loss_tables.append(L)
assert len(tests) == 10 and len(loss_tables) == 18

def enumerate_tier1(precision):
    with localcontext() as ctx:
        ctx.prec = precision
        count = 0
        by_prior = Counter()
        first = None
        smallest_mi_gap = None
        near_nonzero_gaps = 0
        for k in range(1, 8):
            p = (F(8-k, 8), F(k, 8))
            mi = {t: mutual_information(p, t) for t in tests}
            for L in loss_tables:
                values = {t: evaluate(p, L, t)[0] for t in tests}
                for t1 in tests:
                    for t2 in tests:
                        if t1 == t2:
                            continue
                        gap = mi[t1] - mi[t2]
                        if abs(gap) > D('1e-70') and abs(gap) <= D('1e-20'):
                            near_nonzero_gaps += 1
                        if gap > D('1e-20') and values[t1] < values[t2]:
                            count += 1
                            by_prior[k] += 1
                            if smallest_mi_gap is None or gap < smallest_mi_gap:
                                smallest_mi_gap = gap
                            if first is None:
                                first = (p, L, t1, t2)
        return count, dict(by_prior), first, smallest_mi_gap, near_nonzero_gaps

r100 = enumerate_tier1(100)
r120 = enumerate_tier1(120)
assert r100[:3] == r120[:3]
assert r100[4] == r120[4] == 0
assert r100[2] is not None  # Otherwise execute only preregistered Tier 2.
p, L, t1, t2 = r100[2]

# Independent verification: entropy identity and unnormalized joint losses.
# Neither function calls the selection evaluator or MI summation above.
def entropy(q):
    return -sum(dec(v) * dec(v).ln() / D(2).ln() for v in (q, 1-q) if v)

def verify(t):
    marginal1 = p[0] * t[0] + p[1] * t[1]
    mi = entropy(marginal1) - sum(dec(p[s]) * entropy(t[s]) for s in range(2))
    baseline = min(sum(p[s] * L[a][s] for s in range(2)) for a in range(2))
    after = sum(min(sum(p[s] * (t[s] if x else 1-t[s]) * L[a][s]
                       for s in range(2)) for a in range(2)) for x in (0, 1))
    return mi, baseline - after

with localcontext() as ctx:
    ctx.prec = 120
    v1, v2 = verify(t1), verify(t2)
    assert v1[0] - v2[0] > D('1e-20')
    assert v1[1] < v2[1]
    for t, v in ((t1, v1), (t2, v2)):
        assert abs(v[0] - mutual_information(p, t)) < D('1e-110')
        assert v[1] == evaluate(p, L, t)[0]
    print('tests', tests)
    print('counts and first', r120)
    print('baseline', action_result(p, L))
    for label, t in (('X1', t1), ('X2', t2)):
        print(label, 'MI', mutual_information(p, t), 'EVSI and outcomes', evaluate(p, L, t))
    print('independent MI gap', v1[0] - v2[0])
    print('independent EVSI gap', v2[1] - v1[1])
```

KL4A_REVERSAL_FOUND_TIER1
