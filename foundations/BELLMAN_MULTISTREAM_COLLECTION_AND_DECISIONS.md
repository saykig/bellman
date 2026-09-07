# Bellman: controlled multistream collection and checked static decisions

**7 September 2026. Additive bounded construction; no novelty claim.**

Base: main commit `92922ab6604840152ad7f7800969673335748272`, the merge of PR #12.
The repaired PR #12 head is `5017122500450c8f7f890474f7232b9c94d3a3fb`; its scalar
mathematics, result records, and acceptance evidence remain unchanged. This note continues
programme-roadmap section 5A by composing those scalar all-prefix statements across a fixed
finite stream registry. It does not change family replanning, Writ, Decision Lab, or any closed
experiment.

## 1. Independent assessment and result

The proposed construction is sound. The essential proof is simultaneous-event inclusion, not a
claim that a count selected by adaptive collection has a binomial conditional law. Cross-stream
independence is unnecessary for the coverage union bound. It is supplied only in the independent
path-probability examples that multiply transition probabilities. The affine-box formula is exact
by coordinatewise maximization. Independent exact calculations reproduce all proposed M2 and M3
values, so no formula or frozen expected output needs correction.

The bounded result is:

> A receiver can replay a declared built-in rule over a complete append-only transcript from a
> fixed stream registry, verify one PR #12 scalar all-prefix certificate per stream, combine them
> by a finite union bound, and check exact static affine decisions on the retained parameter
> rectangle.

This is a conditional mathematical result. Transcript replay cannot establish that a physical
collector revealed every event, that its declared potential sequences exist, or that its
population and protocol labels are true.

## 2. Sampling subject and collection protocol

Fix a finite ordered registry (j=1,\ldots,m). For each registered stream assume a complete
potential sequence

\[
 X_{j,1},X_{j,2},\ldots\quad\hbox{IID Bernoulli}(p_j),
 \qquad p_j\in[0,1].                                      \tag{M1}
\]

Each row has one fixed real parameter. The rowwise premise excludes arbitrary within-row
dependence, population drift, outcome filtering, and retroactive selection of a favorable
subsequence. The joint premise need not make the rows independent. Mutual row independence is a
sufficient specialization, used below only where complete path probabilities are calculated as
products.

At global time (t), a collector either stops or chooses a registered stream as a deterministic
function of the already revealed history and counts. Choosing stream (j) reveals exactly its next
unused event (X_{j,N_{j,t-1}+1}). Initial counts are zero. The resulting transcript binds:

- registry order and distinct stream, population, and protocol identities;
- row and cross-row premises;
- global index, stream identity, local index, binary value, and a distinct physical-event
  identity for every revealed event;
- built-in rule identity, stopping status, record and revision identity;
- fixed total alpha, stream allocations, spending rule inherited from PR #12, and precision.

The reference has no policy language and executes no submitted code. Its four built-in rules are
a full-budget round robin, six- and eight-event round robins, and the bounded history rule in
section 7. Replay begins at empty prefixes, asks the rule for the next stream, checks that the
transcript supplies precisely that stream's next local event, and finally checks the stopping
status. Equal outcome values are allowed. A repeated event identity, local-index gap/reset, wrong
global index, unregistered stream, observation after stopping, or rule disagreement rejects.

Replay is evidence about the supplied bytes only. A concealed discarded observation can leave a
clean-looking transcript; no finite checker can recover it. Likewise, deterministic
nonanticipation makes the declared collector implementable, but it is not claimed to be necessary
for every random-index consequence of an already established all-prefix event.

## 3. All-stream, all-prefix theorem

Predeclare exact rational (0<\alpha<1) and fixed positive rational allocations (\alpha_j) with
(\sum_j\alpha_j\le\alpha). They are error-budget allocations, not model probabilities or
importance weights. For row (j), apply the unchanged PR #12 interval with

\[
 \varepsilon_{j,n}=\frac{\alpha_j}{2n(n+1)},\qquad n\ge1,  \tag{M2}
\]

and (I_{j,0}=[0,1]). PR #12 proves, for every real (p_j\in[0,1]),

\[
 P(E_j)\ge1-\alpha_j,
 \quad E_j:=\{p_j\in I_{j,n}\text{ for every }n\ge0\}.    \tag{M3}
\]

No cross-row independence is used in the following union bound:

\[
 \begin{aligned}
 P\!\left(\bigcap_{j=1}^mE_j\right)
 &=1-P\!\left(\bigcup_{j=1}^mE_j^c\right)\\
 &\ge1-\sum_{j=1}^mP(E_j^c)
 \ge1-\sum_{j=1}^m\alpha_j
 \ge1-\alpha.                                             \tag{M4}
 \end{aligned}
\]

On (\cap_jE_j), membership holds for every row at every deterministic local index. Therefore it
also holds at each realized local count (N_{j,t}), simultaneously:

\[
 (p_1,\ldots,p_m)\in C_t
 :=\prod_{j=1}^m I_{j,N_{j,t}}.                            \tag{M5}
\]

Equation M5 is event inclusion. It does **not** condition on (N_{j,t}) and does not assert
(K_{j,N}\mid N=n)\sim\mathrm{Binomial}(n,p_j), which can fail even for a valid stopping rule.
The same inclusion holds at any finite data-dependent stopping time. Receiver-checked rational
outward enclosures contain the real-root intervals deterministically, so replacing each factor by
its enclosure preserves M4–M5 without spending more alpha.

Reading a certificate twice neither generates observations nor spends alpha twice. Changing a
loss query can reuse the same checked rectangle after a fresh decision check. Changing an
allocation is a new coverage specification. Renaming or copying the same sample does not reset a
family budget.

The theorem does not supply a posterior, transcript-conditional `(1-alpha)` statement, adaptive
alpha recycling, infinitely created streams, model-drift protection, or sampling-family validity.

## 4. Receiver composition

The executable contract separates four subjects and roles.

1. **Collection:** the receiver replays the built-in rule and reconstructs prefixes and local
   counts from the complete transcript.
2. **Scalar evidence:** for each identified stream it invokes PR #12's receiver on that exact row,
   source identities, allocation, and precision. A refused child is not an interval.
3. **Joint coverage:** it checks one and only one scalar row per registry member, recomputes the
   allocation sum and rectangle, and reports both (1-\sum_j\alpha_j) and the weaker
   (1-\alpha) bound.
4. **Decision:** it binds a separate loss unit, affine action table, intended action, optional
   regret cap, and supported query, then recomputes every comparison.

Correspondence is by explicit identities rather than list position. Scalar-evidence rows may be
presented in a different order; the rectangle and action weights are canonicalized to registry
order. Hashes bind subjects but never substitute for arithmetic, completeness, identity, or rule
checks.

An append-only continuation of a stopped record requires a new revision and predecessor digest.
The classifier distinguishes such a continuation from same-transcript recalculation, a new
coverage specification, and a corrected or retroselected history. Classification is not physical
validation of the successor history, and earlier evidence is never rewritten.

## 5. Exact affine decisions on a retained rectangle

For exact signed rational inputs define population expected risk

\[
 R_a(p)=b_a+\sum_{j=1}^m w_{a,j}p_j.                       \tag{M6}
\]

Let the nonempty retained rectangle be (C=\prod_j[l_j,u_j]). For actions (a,b), put
(d_j=w_{a,j}-w_{b,j}). Separability gives

\[
 \begin{aligned}
 D_{a,b}
 &:=\max_{p\in C}\{R_a(p)-R_b(p)\}\\
 &=b_a-b_b+\sum_{j=1}^m d_j
   \begin{cases}
     u_j,&d_j\ge0,\\
     l_j,&d_j<0.
   \end{cases}                                             \tag{M7}
 \end{aligned}
\]

Proof: each coordinate occurs in its own linear term, so a positive coefficient is maximized at
the upper endpoint and a negative coefficient at the lower endpoint. A zero coefficient has the
same value at both endpoints; choosing the upper endpoint is a fixed witness convention. The
argument includes singleton coordinates, unobserved `[0,1]` rows, signed intercepts and weights,
and ties. Full corner enumeration independently confirms every fixed reference comparison.

The complete common-minimizer set and uniformly strict set are

\[
 \mathcal A_C=\{a:D_{a,b}\le0\ \forall b\},\qquad
 \mathcal A_C^{<}=\{a:D_{a,b}<0\ \forall b\ne a\}.         \tag{M8}
\]

For an independently intended action (a), exact worst regret on the retained rectangle is

\[
 \rho_a=\max_bD_{a,b}
 =\max_{p\in C}\left[R_a(p)-\min_bR_b(p)\right]\ge0.       \tag{M9}
\]

The finite maxima commute, and self-comparison supplies zero. For a uniformly strict action, the
explicit advantage is (\min_{b\ne a}[-D_{a,b}]). The singleton-action strict predicate is vacuous
and is labelled as such; it has no invented positive margin. An independently supplied exact
nonnegative cap (\eta) is certified precisely when (\rho_a\le\eta).

These statements are exact **over the retained rectangle**, not a claim that the rectangle is the
exact unknown-parameter set. An empty common set is noncertification on the retained region, not
proof of real-world unknowability. Alpha, dyadic enclosure precision, and regret in the declared
loss unit are never combined.

The primary interpretation of M6 is risk under fixed population parameters. A conditional risk
for a new outcome after the adaptive history is supported only when the subject additionally
declares that the new population draw is independent of the observed history given those
parameters. Cross-stream dependence otherwise makes a marginal Bernoulli law insufficient for
that conditional claim.

Finally, (C) is a Cartesian parameter set, not a product distribution. A query involving an
unspecified joint event such as (P(X_A=1,X_B=1)) is outside M6 and rejects. Multiplying marginals
would silently add independence.

## 6. Controlled failure and executable limits

The mathematical theorem permits any fixed finite registry and finite stopping time. The research
reference supports at most four streams, 128 observations per stream, four actions, 64 requested
precision bits, and 512 transcript events. A well-formed request outside this profile returns
`unfinished` with `kind=resource-refusal`; it is not mathematically false. The same budget applies
to producers and receivers before replay, tail sums, or decision arithmetic. Malformed subjects
and false within-budget evidence reject. Valid but inconclusive action bounds return a checked
empty common set, not failure.

Exact external rational coordinates have PR #12's finite input-bit bound. Valid derived
`Fraction` coordinates are uncapped; the fixed tests produce a 258-bit derived regret. These count
limits do not prove complete operational cost boundedness because intermediate exact integer size
still affects runtime. No hostile-Python-object security claim is made.

## 7. Fixed exact examples and counterexamples

### M2: two streams and three actions

Take total alpha (1/20), allocations (1/40) each, 16-bit outward precision, A all zeros and B all
ones. For risks (R_A=p_A), (R_B=p_B), and (R_C=1/2), independent tail recurrence reproduces:

| local observations per row | retained rectangle | decision |
|---:|---|---|
| 8 | `[0,43333/65536] x [22203/65536,1]` | no common minimizer |
| 16 | `[0,30431/65536] x [35105/65536,1]` | A uniformly strictly optimal |

At 16, A's advantages over B and C are respectively (2337/32768) and (2337/65536), so the
minimum advantage is (2337/65536). These values were recomputed rather than installed as producer
expectations.

### M3: adaptive stream choice

The history rule starts at A, switches streams after a revealed 1, stays after a 0, and stops when
both local counts are at least two and the absolute difference of sample means exceeds (1/2), or
at global time 12. Complete independent enumeration has 3,013 terminal binary histories. Terminal
history counts by length 5 through 12 are `3, 1, 11, 9, 7, 32, 18, 2932`.

With independent row parameters ((1/2,1/2)), exact terminal mass is one and any-prefix exclusion
mass is zero. At ((1/3,2/3)), they are one and (65/531441). These finite probabilities check the
implementation; M4 carries the all-real-parameter theorem. A separate round-robin rule, an
unobserved row, unequal local counts, and global/local clock corruptions are checked.

### M4: conditioning on an adaptive count is invalid

For one fair coin, stop after the first observation if it is 1 and otherwise take one more. The
terminal paths `(1)`, `(0,1)`, `(0,0)` have masses (1/2,1/4,1/4), so the expected terminal sample
mean is

\[
 \tfrac12(1)+\tfrac14(\tfrac12)+\tfrac14(0)=\tfrac58.      \tag{M10}
\]

Conditional on (N=1), the success count is always one, not Binomial(1,1/2). Yet an event covering
every fixed prefix still covers the selected prefix, which is exactly the M5 argument. Confidence
sequences do not claim to debias the terminal empirical mean.

### M5 and M7: invalid collection and invalid composition

Keeping only successes until 16 have accumulated is not a prefix. For a fair coin, accumulation
eventually occurs with probability one, while the false all-success IID interval excludes (1/2).
Visible index gaps and repeated physical-event identities reject; concealed omissions remain
undetectable from a clean-looking record.

For cross-stream dependence, let B's complete row equal A's row of IID fair bits. Both rows
separately satisfy M1, so M4 remains valid. But corresponding bits are jointly one with probability
(1/2), not the product (1/4). Thus rowwise simultaneous coverage neither licenses marginal
multiplication nor handles arbitrary within-row dependence.

## 8. Evidence, independence, and literature scope

The [fixed checks](../verification/multistream_collection/README.md) cover M1–M8. They reduce the
one-row construction to PR #12, use a separate Pascal-style binomial calculation in adaptive path
enumeration, enumerate all reachable small paths, and compare M7 against every rectangle corner
without calling the production sign formula. Hand-authored evidence is consumed with all producers
disabled. These routes share Python `Fraction`, utilities, execution environment, and authorship;
they are independent computations, not independent formal verification.

Howard, Ramdas, McAuliffe, and Sekhon's
[confidence-sequence paper](https://arxiv.org/abs/1810.08240) supplies context for intervals valid
uniformly over an unbounded horizon and develops sharper nonasymptotic constructions. Bellman uses
the elementary PR #12 summable exact-binomial construction instead. Jamieson, Malloy, Nowak, and
Bubeck's [lil'UCB paper](https://proceedings.mlr.press/v35/jamieson14.html) is an established
fixed-confidence adaptive best-arm reference. This task does not implement lil'UCB, claim optimal
sample complexity, or import either paper as proof of Bellman's transcript interface.

The simultaneous-event union bound and affine-box derivation above carry the bounded theorem.
Physical sampling validity, broader dependence, missingness, drift, nonlinear and causal queries,
learned sequential control, production engineering, formal proof, and authority to act remain
outside it.
