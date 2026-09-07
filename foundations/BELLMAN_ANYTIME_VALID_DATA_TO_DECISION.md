# Bellman: an anytime-valid Bernoulli data-to-decision bridge

**7 September 2026. Additive bounded construction; no novelty claim.**

Base: main commit `2e8d99cdcf289eabb63df15086eaa68251a359f1`, the merge of PR #10.
The reviewed PR #10 head `82d286c591750a2229664d935a6f9820340233df` is an ancestor of that
commit and has the same file tree. PR #10 completed the selected single-cut family-replanning
construction. The next default capability in programme-roadmap section 5A is statistical learning
with time-uniform coverage. This note constructs one narrow part of that capability; it neither
broadens the PR #10 planner nor changes any earlier mathematical record.

## 1. Result, subject, and limits of authority

Let (X_1,X_2,\ldots) be IID Bernoulli random variables with one fixed unknown **real** parameter
(p\in[0,1]). The object is a complete ordered observed prefix (x_{1:n}\in\{0,1\}^n), together
with independently declared stream, population, and protocol identities, the IID/fixed-parameter
premise, a rational (0<\alpha<1), and the spending rule below. These declarations bind the
mathematical subject. A checker cannot establish physical independence, representativeness,
completeness, absence of drift, or truth of the population interpretation from the data bytes.

The operation returns an outward-certified rational interval for (p). Given a separately bound
finite action table with exact signed losses, it also checks common action optimality and a named
action's worst regret over that retained interval. The loss concerns one static choice and a future
draw from the same stipulated population, or its population expected risk. The action does not
change the Bernoulli law.

This is not a Bayesian posterior, causal intervention model, learned sequential-control rule,
persistent-model update, empirical validation of a sampling design, or authority to act. It does
not turn a confidence set into a PR #10 root-preservation theorem. Probability of coverage failure,
deterministic bracket precision, and conditional loss regret remain three different quantities.

## 2. Exact binomial interval and endpoint theorem

For (n\ge1), let (K_n=\sum_{i=1}^nX_i) and

\[
 \varepsilon_n=\frac{\alpha}{2n(n+1)}.                       \tag{D1}
\]

For (0\le k\le n) and (q\in[0,1]), define

\[
 T_+(n,k,q)=\sum_{j=k}^n {n\choose j}q^j(1-q)^{n-j},\qquad
 T_-(n,k,q)=\sum_{j=0}^k {n\choose j}q^j(1-q)^{n-j}.          \tag{D2}
\]

For (k>0), define (\ell_n(k)) as the unique solution of
(T_+(n,k,\ell_n(k))=\varepsilon_n); put (\ell_n(0)=0). For (k<n), define
(u_n(k)) as the unique solution of (T_-(n,k,u_n(k))=\varepsilon_n); put
(u_n(n)=1).

**Tail monotonicity and roots.** For (1\le k\le n), telescoping the differentiated binomial
sum gives

\[
 \frac{\partial}{\partial q}T_+(n,k,q)
 =n{n-1\choose k-1}q^{k-1}(1-q)^{n-k}>0\quad(0<q<1).         \tag{D3}
\]

Its endpoint values are zero and one. Hence the lower root exists uniquely because
(0<\varepsilon_n<1). Similarly, for (0\le k<n),

\[
 \frac{\partial}{\partial q}T_-(n,k,q)
 =-n{n-1\choose k}q^k(1-q)^{n-k-1}<0\quad(0<q<1),           \tag{D4}
\]

and its endpoint values are one and zero, proving existence and uniqueness of the upper root. The
boundary definitions avoid invoking a nonexistent nontrivial root.

The interval is nonempty. Boundary cases are immediate. For (0<k<n), suppose instead that
(\ell_n(k)>u_n(k)) and choose (q) strictly between them. Monotonicity would give both
(T_+(n,k,q)<\varepsilon_n) and (T_-(n,k,q)<\varepsilon_n). But

\[
 T_+(n,k,q)+T_-(n,k,q)=1+P_q(K_n=k)\ge1,                    \tag{D5}
\]

while (2\varepsilon_n<1), a contradiction. Thus
(0\le\ell_n(k)\le u_n(k)\le1). This includes (n=1), zero successes, and all successes.

## 3. Fixed-time and simultaneous coverage

Fix any real (p\in[0,1]); no finite parameter grid is used. The lower endpoint excludes the true
parameter exactly when (p<\ell_n(K_n)). For (k>0), strict monotonicity gives

\[
 p<\ell_n(k)\quad\Longleftrightarrow\quad
 T_+(n,k,p)<\varepsilon_n.                                  \tag{D6}
\]

For fixed (p), (T_+(n,k,p)) is nonincreasing in (k). If the set in D6 is nonempty, it is
({k_0,\ldots,n}) for its smallest member (k_0). Therefore

\[
 P_p\{p<\ell_n(K_n)\}=P_p(K_n\ge k_0)
 =T_+(n,k_0,p)<\varepsilon_n.                               \tag{D7}
\]

Equality of a tail with the allowance is not an exclusion; this is why the strict inequality in
D6–D7 matters. The (k=0) convention cannot exclude any (p\ge0).

Likewise (p>u_n(k)) is equivalent, for (k<n), to
(T_-(n,k,p)<\varepsilon_n). This set of counts, if nonempty, is
({0,\ldots,k_1}), so its probability is
(T_-(n,k_1,p)<\varepsilon_n). The (k=n) convention cannot exclude (p\le1). Hence

\[
 P_p\{p\notin[\ell_n(K_n),u_n(K_n)]\}\le2\varepsilon_n.
                                                                    \tag{D8}
\]

At (p=0), (K_n=0) almost surely and the lower endpoint is zero; at (p=1), (K_n=n) almost
surely and the upper endpoint is one. Thus the proof includes both parameter boundaries rather
than relying on a limiting argument.

The union bound, D1, and the telescoping series
(\sum_{n\ge1}1/[n(n+1)]=1) now prove the all-parameter theorem

\[
 P_p\left\{p\in[\ell_n(K_n),u_n(K_n)]\text{ for every }n\ge1\right\}
 \ge1-\alpha\qquad\text{for every real }p\in[0,1].          \tag{D9}
\]

If a finite stopping time (\tau) depends on the observations, the simultaneous event in D9
implies (p\in[\ell_\tau(K_\tau),u_\tau(K_\tau)]). No optional-stopping calculation is needed:
the guarantee follows by set inclusion. A finite reference may compute only supported prefixes;
that resource boundary does not truncate the mathematical quantifier in D9. For (n=0), the
reference returns the trivial interval ([0,1]) without a binomial inversion or division.

## 4. Outward rational evidence

The real roots need not be rational. A lower-root witness is a rational pair (a\le b) satisfying

\[
 T_+(n,k,a)\le\varepsilon_n\le T_+(n,k,b),                  \tag{D10}
\]

and an upper-root witness is a rational pair (c\le d) satisfying

\[
 T_-(n,k,c)\ge\varepsilon_n\ge T_-(n,k,d).                  \tag{D11}
\]

D3–D4 imply (a\le\ell_n(k)\le b) and
(c\le u_n(k)\le d). Therefore the exported rational interval ([a,d]) contains the exact
binomial interval. On the event in D9 it also contains the true (p), with no extra statistical
spending: outward rounding is a deterministic set enlargement.

The producer starts with ([0,1]) and performs a declared number of dyadic bisections. The receiver
does not trust that search. It recomputes D10–D11 by exact binomial sums, checks the zero/all-success
boundary conventions, recomputes (n), (k), and (\varepsilon_n), and checks each nontrivial
bracket width against (2^{-b}) when (b) precision bits are claimed. A wide valid enclosure is
still conservative but receives `valid-coarse-outward-enclosure`; a false precision claim rejects.
No rounded coordinate is called an exact quantile.

## 5. Exact decision certificate on the retained interval

For action (a) with exact signed losses (\ell(a,0),\ell(a,1)), define the affine risk

\[
 R_a(p)=(1-p)\ell(a,0)+p\ell(a,1).                           \tag{D12}
\]

For a nonempty retained interval (C=[l,u]), every risk difference is affine. Consequently

\[
 D_{ab}=\max_{p\in C}[R_a(p)-R_b(p)]
 =\max\{R_a(l)-R_b(l),R_a(u)-R_b(u)\}.                       \tag{D13}
\]

This proves all of the receiver's finite conclusions:

- (a) is optimal for every (p\in C) exactly when (D_{ab}\le0) for every action (b);
- it is strictly better than every distinct action exactly when (D_{ab}<0) for every (b\ne a);
- checking this condition for every supplied action returns the complete common-minimizer set,
  including every tie rather than an arbitrary representative;
- for an independently intended action (a),

\[
 \rho_a=\max_bD_{ab}
 =\max_{p\in C}\left[R_a(p)-\min_bR_b(p)\right]\ge0.         \tag{D14}
\]

The finite maxima in D14 commute, and the self-comparison contributes zero. Thus (\rho_a) is an
exact worst-parameter regret on this interval, in the declared loss unit. A singleton action is
optimal and satisfies the distinct-competitor strict condition vacuously; the checker labels that
case and does not invent a positive margin.

On the simultaneous event in D9, any separately checked D13–D14 conclusion holds at every
supported inspection. The inspected time and named action may depend on the observed prefix: the
same event already covers all times and the deterministic risk calculation covers the action that
was actually checked. Recalculating several loss queries creates no new sample and spends no new
(\alpha), but every changed loss table, unit, action, or query requires its own decision
certificate. If no common action is certified, the operation reports that limit; it does not force
a midpoint estimate, prior, randomization, minimax preference, or recommendation.

## 6. Exact joint-law representation

For one future binary outcome, the joint-law vector is simply

\[
 p_{\rm vector}=(1-p,p),\qquad p_{\rm vector}\ge0,\qquad
 \mathbf1^Tp_{\rm vector}=1,\qquad l\le p\le u.              \tag{D15}
\]

The last two interval inequalities are linear. Each D12 risk is the dot product of its loss row
with D15, so the retained Bellman joint-law checker can verify D13 as a two-atom linear-query
maximum without changing its semantics. The fixed cross-check does so for the 16-success case and
recovers the same exact maximum (-3891/32768). This is a mathematical interface demonstration,
not a Decision Lab modification or a claim that Writ already integrates the bridge.

## 7. Fixed exact cases and failure boundaries

The [fixed checks](../verification/statistical_decision_bridge/README.md) exercise the following
authored conformance cases.

1. **Boundaries and brackets.** They cover (n=0), (n=1), zero/all successes, an interior count,
   non-default (\alpha), equality at rational roots, (p=0,1), wide valid witnesses, false
   precision, inward/reversed brackets, wrong counts/allocation/identity, and proof coordinates
   whose derived numerator exceeds the external-input bit limit.
2. **Repeated inspection.** At (p=1/2,\alpha=1/20,n\le32), exact recursion gives
   (8962675/67108864\) for at least one exclusion using a nominal fixed-time 95% interval at every
   inspection. The D1 allocation gives (444183/1073741824). Probability is conserved and a
   separate complete binary-path calculation agrees at a smaller horizon. The allocated D9 failure
   budget through time 32 is (8/165). These numbers check arithmetic only; D9 carries the theorem
   for every real (p).
3. **Decision without a point estimate.** With all successes and 16 bisections, the outward
   intervals are ([24213/65536,1]) at (n=8) and ([36659/65536,1]) at (n=16). Zero-one loss
   gives no common action for the first and uniquely certifies `predict1` for the second, with
   minimum advantage (3891/32768). Changed losses remove that action conclusion without changing
   the sampling interval. Genuine ties and a singleton are retained explicitly.
4. **Dependence control.** Copy one fair-coin outcome sixteen times. Both possible copied prefixes
   exclude (p=1/2), so applying the IID procedure under this false premise fails with probability
   one. Different byte identities cannot repair or diagnose the physical dependence. An explicitly
   declared dependent profile is outside this operation and rejects.
5. **Revision and refusal.** Same-prefix recomputation is not fresh evidence; a genuine append is a
   new prefix claim; correction or retroselection is not an append; a changed coverage
   specification or decision subject requires a new bound. Stale certificates, float/Boolean
   pseudo-exact values, false conclusions with matching digests, and mutated subject fields reject.
   Exceeding 128 observations, four actions, or 64 bisection bits is `unfinished`, not a statistical
   finding or mathematical impossibility.
6. **Producer-independent receiving.** Retained and manually authored valid evidence is consumed
   with the bisection and decision producers disabled. The receiver recomputes exact tails, coverage,
   affine endpoint risks, complete action sets, and regret. A separate Pascal recurrence checks
   important binomial sums. All paths share Python `Fraction` arithmetic and this authorship context;
   this is not formal verification or independent authorship.

## 8. Evidence and literature scope

The proof above is elementary and carries the result directly. Howard, Ramdas, McAuliffe, and
Sekhon's [confidence-sequence paper](https://arxiv.org/abs/1810.08240) describes confidence
sequences as intervals uniformly valid over an unbounded time horizon and develops sharper
nonasymptotic constructions. This reference does not claim to implement those sharper boundaries.
The DOI landing path for Clopper and Pearson (1934) was not accessible to the execution environment;
no uninspected historical detail is attributed to it. The exact-binomial inversion here is
distinguished from both the unchanged categorical Hoeffding construction in B21–B22 and modern
confidence-sequence algorithms.

The reference is a research implementation using exact rational arithmetic. It establishes the
conditional theorem under the declared IID Bernoulli premise and checks finite authored examples.
It does not establish that a real data source satisfies that premise, provide adaptive-sampling or
missingness corrections, detect drift or concealed dependence, identify causal effects, optimize a
sequential policy, validate empirical usefulness, or confer authority. Those remain separate
programme obligations rather than failures disguised as conclusions.
