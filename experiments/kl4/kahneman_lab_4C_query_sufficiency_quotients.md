# Kahneman Lab Experiment 4C — Query-Relative Sufficiency and Compression

The preregistered space contains **216 valid full objects**. The exact Q0, Q1, Q2, and Q3 quotients contain **3, 19, 31, and 109 classes**, respectively. All three successive refinements are strict. `S_certificate` is exactly sufficient for Q2 and maps distinct full objects to the same certificate, but is insufficient for Q3. These are finite results about representations and specified queries; they do not establish a competing analysis methodology or mathematical novelty.

Only Lane C was executed. The entire supplied packet was read. No other lane, synthesis, optional strategic-interface gate, web search, or literature search was executed. No Writ application or product code was changed. Temporary computation files are not deliverables; this report contains the reproduction code.

**Finite space and ordering.** States, actions, and outcomes have fixed labels 0 and 1. Write a full object as

\[
F=(p,L,k),\quad p=P(\theta=1),\quad
L=\begin{pmatrix}l_{00}&l_{01}\\l_{10}&l_{11}\end{pmatrix},\quad
k=(K(1\mid0),K(1\mid1)).
\]

Thus the full prior is `(1-p,p)`, and the likelihood matrix, with outcome rows and state columns, is

\[
K=\begin{pmatrix}1-k_0&1-k_1\\k_0&k_1\end{pmatrix}.
\]

There are three priors, eight valid loss tables, and nine likelihood vectors. The loss tables, flattened in row-major order, are exactly

```
(0,1,1,0)  (0,1,2,0)  (0,2,1,0)  (0,2,2,0)
(1,0,0,1)  (1,0,0,2)  (2,0,0,1)  (2,0,0,2)
```

To see exhaustiveness, each action must win strictly in one of the two states. The winners must be different across states, and the winning loss is zero by normalization. Each losing loss can independently be 1 or 2, giving `2 × 2 × 2 = 8` tables. Taking their Cartesian product with all three prescribed priors and all nine prescribed likelihood vectors gives `3 × 8 × 9 = 216` objects. Uninformative and constant tests are included. There is no identification under action, state, or outcome relabeling in Lane C.

The packet does not specify an order for “smallest.” Before computing results, the implementation fixed ascending numerical lexicographic order on `(p,l00,l01,l10,l11,k0,k1)`. Objects are numbered F1 through F216 in that order. Unordered pairs are represented with the smaller object first and ordered lexicographically by their two object indices. Every “smallest pair” and the canonical pair below use this convention.

**Exact signatures and arithmetic.** Let `A` denote the full current argmin set, let `B0,B1` be the two posterior argmin sets or `NA`, let `v` be EVSI, and let `T` be the ordered tuple of four revised current argmin sets. The signatures used were exactly

```
σ0 = A
σ1 = (A,B0,B1)
σ2 = (σ1,v)
σ3 = (σ2,T)
T order: (a0,θ0), (a0,θ1), (a1,θ0), (a1,θ1)
```

Each revision adds 1 to just its selected cell of the original loss table; revisions are separate queries, not cumulative changes. No revised table is renormalized or filtered by the base-table constraints. All ties are retained as `{0,1}`. All arithmetic uses exact fractions or integers; no logarithms or mutual information are needed in this lane. There are 48 zero-probability outcome occurrences among the 432 object/outcome combinations. Their posterior, posterior risk, and action set are `NA`; their contribution to expected posterior risk is zero.

For independent verification, every signature was also calculated with integer, unnormalized state weights. If `p=n/4` and `kθ=mθ/2`, write `w=(4-n,n)`, current loss numerators `Ca=Σθ wθ Laθ`, and outcome loss numerators `Dxa=Σθ wθ mxθ Laθ`, where `m1θ=mθ` and `m0θ=2-mθ`. Then

\[
EVSI=\frac{2\min_a C_a-\sum_x\min_a D_{xa}}8.
\]

At an impossible outcome both numerators are zero, but its action answer is explicitly `NA`. A single-cell revision changes the selected action's current numerator by the corresponding `wθ`. This calculation reproduced all four signatures for all 216 objects. Every EVSI was nonnegative.

**Quotient counts and refinement.** In the histogram column, `s:n` means `n` equivalence classes each containing `s` full objects.

| Query family | Equivalence classes | Class-size histogram |
|---|---:|---|
| Q0 | 3 | 36:1, 90:2 |
| Q1 | 19 | 2:4, 4:3, 10:4, 12:2, 22:6 |
| Q2 | 31 | 2:6, 4:5, 6:10, 10:8, 22:2 |
| Q3 | 109 | 1:60, 2:28, 3:4, 4:13, 6:2, 12:2 |

Each histogram accounts for exactly 216 objects. Equality of a later signature implies equality of each earlier signature by projection. This proves refinement analytically; it was also checked on all `216 × 215 / 2 = 23,220` distinct unordered object pairs. The smallest pairs establishing strict refinement are F1/F2 for Q0→Q1, F2/F3 for Q1→Q2, and F1/F10 for Q2→Q3. Their exact signatures appear below.

**All candidate-summary/query-family results.** “Exact” means the summary induces the same partition as the query signature. “Overpreserves” means the summary is sufficient but strictly splits at least one query-equivalence class. “Insufficient” means a collision changes a required query answer; overpreservation is not assigned in that case. The final column lists the smallest collision for every insufficient pair.

| Summary | Query | Summary classes | Query classes | Result | Smallest witness pair |
|---|---|---:|---:|---|---|
| `S_action` | Q0 | 3 | 3 | Exact | — |
| `S_action` | Q1 | 3 | 19 | Insufficient | F1/F2 |
| `S_action` | Q2 | 3 | 31 | Insufficient | F1/F2 |
| `S_action` | Q3 | 3 | 109 | Insufficient | F1/F2 |
| `S_policy` | Q0 | 19 | 3 | Overpreserves | — |
| `S_policy` | Q1 | 19 | 19 | Exact | — |
| `S_policy` | Q2 | 19 | 31 | Insufficient | F2/F3 |
| `S_policy` | Q3 | 19 | 109 | Insufficient | F1/F10 |
| `S_certificate` | Q0 | 31 | 3 | Overpreserves | — |
| `S_certificate` | Q1 | 31 | 19 | Overpreserves | — |
| `S_certificate` | Q2 | 31 | 31 | Exact | — |
| `S_certificate` | Q3 | 31 | 109 | Insufficient | F1/F10 |
| `S_pL` | Q0 | 24 | 3 | Overpreserves | — |
| `S_pL` | Q1 | 24 | 19 | Insufficient | F1/F2 |
| `S_pL` | Q2 | 24 | 31 | Insufficient | F1/F2 |
| `S_pL` | Q3 | 24 | 109 | Insufficient | F1/F2 |
| `S_pK` | Q0 | 27 | 3 | Insufficient | F1/F37 |
| `S_pK` | Q1 | 27 | 19 | Insufficient | F1/F37 |
| `S_pK` | Q2 | 27 | 31 | Insufficient | F1/F37 |
| `S_pK` | Q3 | 27 | 109 | Insufficient | F1/F10 |
| `S_full` | Q0 | 216 | 3 | Overpreserves | — |
| `S_full` | Q1 | 216 | 19 | Overpreserves | — |
| `S_full` | Q2 | 216 | 31 | Overpreserves | — |
| `S_full` | Q3 | 216 | 109 | Overpreserves | — |

Sufficiency was tested by exact equality on every unordered pair, not inferred just from class counts. For every sufficient case, overpreservation was tested by finding two objects with equal query signatures but unequal summaries. The resulting classifications also agree with the class-count comparison, which is valid once sufficiency establishes refinement.

**Complete witness objects and signatures.** All witnesses in the table use just the following five full objects. The common prior is `(3/4,1/4)`; each listed `k` specifies the entire matrix through the formula above.

| Object | Loss matrix, action rows | k |
|---|---|---|
| F1 | `[[0,1],[1,0]]` | `(0,0)` |
| F2 | `[[0,1],[1,0]]` | `(0,1/2)` |
| F3 | `[[0,1],[1,0]]` | `(0,1)` |
| F10 | `[[0,1],[2,0]]` | `(0,0)` |
| F37 | `[[1,0],[0,1]]` | `(0,0)` |

For compactness, the next table provides each component needed to reconstruct all four signatures, preserving the distinction between a set and `NA`.

| Object | σ0 | σ1 = (current, after 0, after 1) | EVSI | T: four revised action sets |
|---|---|---|---:|---|
| F1 | `{0}` | `({0},{0},NA)` | 0 | `({1},{0},{0},{0})` |
| F2 | `{0}` | `({0},{0},{1})` | 1/8 | `({1},{0},{0},{0})` |
| F3 | `{0}` | `({0},{0},{1})` | 1/4 | `({1},{0},{0},{0})` |
| F10 | `{0}` | `({0},{0},NA)` | 0 | `({0},{0},{0},{0})` |
| F37 | `{1}` | `({1},{1},NA)` | 0 | `({1},{1},{0},{1})` |

The four distinct collision pairs explain every insufficient table entry:

- **F1/F2:** equal `S_action` and `S_pL`, but outcome 1 has action answer `NA` in F1 and `{1}` in F2. Their Q1, Q2, and Q3 signatures differ.
- **F2/F3:** equal `S_policy`, but EVSI differs, `1/8` versus `1/4`. Their Q2 signatures differ.
- **F1/F10:** equal `S_policy`, `S_certificate`, and `S_pK`, but the first loss-revision answer changes from `{1}` to `{0}`. Their Q3 signatures differ. This pair precedes F2/F3 under the fixed pair ordering, so it is the smallest Q3 witness for `S_policy` as well.
- **F1/F37:** equal `S_pK`, but current action sets differ, `{0}` versus `{1}`. Their Q0, Q1, and Q2 signatures differ. For Q3, the earlier F1/F10 pair already witnesses insufficiency of `S_pK`.

The following exact values independently make the contingent-policy and EVSI differences inspectable. Expected loss vectors are ordered by action, and posteriors by state.

| Object | Current expected losses | Current Bayes risk | Outcome 0: mass; posterior; risk | Outcome 1: mass; posterior; risk | Expected posterior risk |
|---|---|---:|---|---|---:|
| F1 | `(1/4,3/4)` | 1/4 | `1; (3/4,1/4); 1/4` | `0; NA; NA` | 1/4 |
| F2 | `(1/4,3/4)` | 1/4 | `7/8; (6/7,1/7); 1/7` | `1/8; (0,1); 0` | 1/8 |
| F3 | `(1/4,3/4)` | 1/4 | `3/4; (1,0); 0` | `1/4; (0,1); 0` | 0 |
| F10 | `(1/4,3/2)` | 1/4 | `1; (3/4,1/4); 1/4` | `0; NA; NA` | 1/4 |
| F37 | `(3/4,1/4)` | 1/4 | `1; (3/4,1/4); 1/4` | `0; NA; NA` | 1/4 |

For example, F2 has expected posterior risk `(7/8)(1/7)+(1/8)(0)=1/8`, giving EVSI `1/4−1/8=1/8`. F3 has zero posterior risk, giving EVSI `1/4`. Their posterior actions agree despite the value difference.

For the Q3 collision F1/F10, adding 1 to `(a0,θ0)` gives revised expected loss vectors `(1,3/4)` and `(1,3/2)`, respectively, so the revised unique actions are 1 and 0. The other three revisions leave action 0 uniquely optimal in both objects. For F37, the unperturbed action is 1; adding 1 to `(a1,θ0)` gives `(3/4,1)`, making action 0 uniquely optimal, while its other revisions preserve action 1.

**Canonical Q2 compression pair.** The lexicographically first two distinct full objects sharing a certificate are **F1 and F10**:

\[
p=(3/4,1/4),\qquad
L=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
L'=\begin{pmatrix}0&1\\2&0\end{pmatrix},\qquad
K=K'=\begin{pmatrix}1&1\\0&0\end{pmatrix}.
\]

They are genuinely different full objects: the loss of action 1 in state 0 is 1 versus 2. This is not a change of labels. Both loss tables satisfy all base-space conditions. They share exactly

\[
S_{\mathrm{certificate}}=\bigl((\{0\},\{0\},NA),0\bigr).
\]

Because `S_certificate=σ2` by definition, this summary is sufficient for Q2 over the entire enumerated space. This distinct pair therefore cannot be distinguished by any preregistered Q2 answer. The shared certificate's class contains 10 full objects. The constant test and zero EVSI are permitted by C2; no informativeness or positive-value restriction was added. The pair is mathematically simple, and its existence should not be overstated. It also explicitly demonstrates failure under the specified Q3 loss revision. No strategic follow-on was designed or executed.

**Interpretation and limits.** The current action set forgets distinctions needed for contingent policies. A contingent policy forgets distinctions needed for exact EVSI. A policy-plus-EVSI certificate forgets distinctions needed for responses to changes in losses. Retaining `(p,L)` suffices for the current decision but omits the test needed for Q1 and higher. Retaining `(p,K)` omits losses needed even for Q0.

The three summaries defined as σ0, σ1, and σ2 are sufficient for their matching families directly by construction. Their sufficiency is a standard consequence of equality of query answers. The enumeration supplies the exact class counts, strict refinements, and minimal counterexamples in this finite space. The nontrivial compression finding means that different full objects share every answer in the specified family; it is not a novelty claim or a claim about computational storage efficiency.

Among the six evaluated candidate summaries, only `S_full` suffices for Q3. Nevertheless, the Q3 quotient has 109 classes rather than 216, so full-object retention is not mathematically necessary for Q3: σ3 itself is sufficient and merges some objects. More generally, the exact Qj quotient is the coarsest partition preserving these exact answers. This is an extensional mathematical benchmark, not a proposed practical data structure. No conclusion about unrestricted future decision queries follows from these bounded families.

**Reproduction.** The following complete Python 3 standard-library script enumerates all objects, calculates signatures in two ways, checks refinement and nonnegative EVSI, searches every candidate-summary/query-family pair, and reports the canonical pair. Internal array indices in its JSON output are zero-based; report labels are those indices plus one. Its only file output is temporary `/tmp/kl4c_results.json`.

```python
from fractions import Fraction as R
from itertools import product, combinations
from collections import Counter
import json

def argmin(v):
    return tuple(i for i, x in enumerate(v) if x == min(v))

def evaluate(f):
    p, l, k = f
    prior = (1-p, p)
    losses = tuple(sum(prior[t]*l[2*a+t] for t in range(2)) for a in range(2))
    action = argmin(losses)
    policies, posterior_details = [], []
    after_risk = R(0)
    for x in range(2):
        weights = tuple(prior[t]*(k[t] if x else 1-k[t]) for t in range(2))
        mass = sum(weights)
        if mass == 0:
            policies.append('NA')
            posterior_details.append((mass, 'NA', 'NA', 'NA'))
        else:
            post = tuple(w/mass for w in weights)
            el = tuple(sum(post[t]*l[2*a+t] for t in range(2)) for a in range(2))
            policies.append(argmin(el))
            posterior_details.append((mass, post, el, min(el)))
            after_risk += mass*min(el)
    evsi = min(losses)-after_risk
    assert evsi >= 0
    revisions = []
    for cell in range(4):
        revised = list(l)
        revised[cell] += 1
        revisions.append(argmin(tuple(sum(prior[t]*revised[2*a+t] for t in range(2)) for a in range(2))))
    s1 = (action, *policies)
    s2 = (s1, evsi)
    s3 = (s2, tuple(revisions))
    return (action, s1, s2, s3), (losses, min(losses), tuple(posterior_details), evsi, tuple(revisions))

# Independent integer calculation: p=n/4, K(1|theta)=m_theta/2.
def integer_signatures(f):
    p, l, k = f
    n = int(4*p)
    w = (4-n, n)
    m = tuple(int(2*v) for v in k)
    current = tuple(sum(w[t]*l[2*a+t] for t in range(2)) for a in range(2))
    action = tuple(a for a in range(2) if all(current[a] <= current[b] for b in range(2)))
    policy = []
    conditional_min_sum = 0
    for x in range(2):
        z = tuple(w[t]*(m[t] if x else 2-m[t]) for t in range(2))
        v = tuple(sum(z[t]*l[2*a+t] for t in range(2)) for a in range(2))
        policy.append('NA' if sum(z) == 0 else tuple(a for a in range(2) if all(v[a] <= v[b] for b in range(2))))
        conditional_min_sum += min(v)
    evsi = R(2*min(current)-conditional_min_sum, 8)
    revisions = []
    for cell in range(4):
        v = tuple(current[a]+(w[cell % 2] if a == cell//2 else 0) for a in range(2))
        revisions.append(tuple(a for a in range(2) if all(v[a] <= v[b] for b in range(2))))
    s1 = (action, *policy)
    s2 = (s1, evsi)
    return action, s1, s2, (s2, tuple(revisions))

loss_tables = [l for l in product(range(3), repeat=4)
               if all(min(l[t], l[2+t]) == 0 for t in range(2))
               and all(any(l[2*a+t] < l[2*(1-a)+t] for t in range(2)) for a in range(2))]
objects = sorted((p, l, k) for p in (R(1,4), R(1,2), R(3,4))
                 for l in loss_tables for k in product((R(0), R(1,2), R(1)), repeat=2))
assert len(loss_tables) == 8 and len(objects) == 216
signatures, details = zip(*(evaluate(f) for f in objects))
assert all(s == integer_signatures(f) for f, s in zip(objects, signatures))
names = ('S_action', 'S_policy', 'S_certificate', 'S_pL', 'S_pK', 'S_full')
summaries = [(s[0], s[1], s[2], f[:2], (f[0], f[2]), f) for f,s in zip(objects,signatures)]
qcounts = [len(set(s[j] for s in signatures)) for j in range(4)]
scounts = [len(set(s[i] for s in summaries)) for i in range(6)]
pairs = list(combinations(range(len(objects)), 2))
for j in range(3):
    assert all(signatures[a][j+1] != signatures[b][j+1] or signatures[a][j] == signatures[b][j] for a,b in pairs)
results = []
for i, name in enumerate(names):
    for j in range(4):
        witness = next(((a,b) for a,b in pairs if summaries[a][i] == summaries[b][i] and signatures[a][j] != signatures[b][j]), None)
        sufficient = witness is None
        over = sufficient and any(signatures[a][j] == signatures[b][j] and summaries[a][i] != summaries[b][i] for a,b in pairs)
        assert not sufficient or over == (scounts[i] > qcounts[j])
        results.append(dict(summary=name, query=j, sufficient=sufficient, summary_classes=scounts[i], query_classes=qcounts[j], witness=witness, overpreserves=over if sufficient else None))
canonical = next((a,b) for a,b in pairs if summaries[a][2] == summaries[b][2])
refinement_witnesses = [next((a,b) for a,b in pairs if signatures[a][j] == signatures[b][j] and signatures[a][j+1] != signatures[b][j+1]) for j in range(3)]

def encode(x):
    if isinstance(x, R): return str(x)
    if isinstance(x, (tuple,list)): return [encode(v) for v in x]
    if isinstance(x, dict): return {k:encode(v) for k,v in x.items()}
    return x

data = dict(objects=objects, signatures=signatures, details=details, results=results,
            qcounts=qcounts, scounts=scounts, canonical=canonical, refinement_witnesses=refinement_witnesses,
            qclass_size_histograms=[dict(sorted(Counter(Counter(s[j] for s in signatures).values()).items())) for j in range(4)],
            zero_probability_outcomes=sum(d[2][x][0] == 0 for d in details for x in range(2)))
with open('/tmp/kl4c_results.json','w') as out:
    json.dump(encode(data),out,indent=2)
print(json.dumps(encode({k:v for k,v in data.items() if k not in ('objects','signatures','details')}),indent=2))
print('WITNESS OBJECTS')
needed = sorted(set(v for r in results if r['witness'] for v in r['witness']) | set(canonical) | set(v for pair in refinement_witnesses for v in pair))
for i in needed:
    print(i+1, encode(objects[i]), 'signature=', encode(signatures[i]), 'details=', encode(details[i]))

```

KL4C_NONTRIVIAL_QUERY_RELATIVE_COMPRESSION_FOUND
