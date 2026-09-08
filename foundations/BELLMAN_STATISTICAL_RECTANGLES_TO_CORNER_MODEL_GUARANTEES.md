# Bellman statistical rectangles to sequential corner-model guarantees

**Standing.** Additive bounded mathematical companion. It composes the reviewed multistream
statistical rectangle with the reviewed persistent whole-episode family semantics. It neither
changes those results nor claims a generic robust planner, a new confidence method, empirical
validity, or an engineering transfer.

## 1. Question, object, and guarantee

Let

\[
C=[\ell _1,u_1]\times[\ell _2,u_2]\subseteq[0,1]^2
\]

be an identified outward rational rectangle retained by the multistream receiver. One or two
coordinates are supported by the executable profile. Each statistical stream identity is mapped
explicitly and bijectively to one named transition-parameter identity; registry position or
similar spelling is never a mapping rule.

The sequential subject has:

1. one fixed finite completed observable-history skeleton;
2. parameter-independent horizon, loss unit, legal actions, and outcome labels;
3. exact rational parameter-independent action and terminal costs;
4. fixed transitions or binary transitions whose two probabilities are affine functions of one
   named parameter and sum identically to one on `[0,1]`;
5. one complete deterministic observable-history policy \(\pi\); and
6. a finite explicitly covered deterministic policy class \(\Pi\) for regret and, when declared
   complete, deterministic minimax selection.

For parameter vector \(p\), let \(J^\pi(p)\) be expected additive whole-policy cost and

\[
V_\Pi(p)=\min_{\sigma\in\Pi}J^\sigma(p).
\]

The query is the maximum expected loss and modelwise regret of \(\pi\) over `C`, plus optional
minimum-worst expected loss and regret over a completely enumerated \(\Pi\).

The result below gives an exact reduction to the at most four completed corner subjects, subject
to a structural admissibility condition. The corners represent the robust query. They are not a
posterior, are not assigned probabilities, and are never allowed to select different policies by
hidden model identity.

## 2. Pathwise multi-affine admissibility

A **parameter-dependent transition factor** is an outcome probability with nonzero coefficient
in a named parameter. A complete skeleton path includes every transition from the root to a
terminal history, and an early `STOP` action is a complete path ending without another transition
factor.

> **Admissibility condition A.** For each parameter \(p_i\), every complete root-to-terminal or
> root-to-`STOP` skeleton path contains at most one transition factor depending on \(p_i\).

This condition is structural. It is checked across the entire action/outcome skeleton, not just
positive-mass paths at one corner or paths selected by the queried policy. The same parameter may
occur at several mutually exclusive nodes when no complete path visits two of them.

### Lemma 1 — fixed-policy multi-affinity

Under condition A and parameter-independent costs, \(J^\pi(p_1,p_2)\) is affine in each
coordinate separately with the other coordinate fixed.

**Proof.** Fix a complete path \(\omega\) selected by the total policy. Its probability is the
product of its transition factors. Fixed factors are constants. Every parameter-dependent factor
is affine in its one named parameter. Condition A says the product contains at most one factor
depending on each \(p_i\). Therefore the expanded path probability has degree at most one in each
coordinate, although it may contain the interaction \(p_1p_2\). The total cost
\(L^\pi(\omega)\)—the sum of fixed stage and terminal costs, including an early-`STOP` cost—is
independent of `p`. Hence

\[
J^\pi(p)=\sum_{\omega}L^\pi(\omega)P_p^\pi(\omega)
\]

is a finite sum of functions having degree at most one in every coordinate. It is multi-affine.
Zero-probability paths cause no exception: they remain structural paths, and their exact zero
contribution at a coordinate is ordinary algebra. \(\square\)

Equivalently, backward substitution preserves multi-affinity when a parameter cannot re-enter a
continuation already containing that parameter. The path proof is used here because it makes the
failure boundary visible.

## 3. Rectangle-corner theorem

> **Theorem 2.** If \(f:C\to\mathbb R\) is multi-affine, then
>
> \[
> \max_{p\in C}f(p)=\max_{c\in\operatorname{corners}(C)}f(c),\qquad
> \min_{p\in C}f(p)=\min_{c\in\operatorname{corners}(C)}f(c).
> \]

**Proof.** For a nondegenerate interval define

\[
\lambda_i^0(p_i)=\frac{u_i-p_i}{u_i-\ell_i},\qquad
\lambda_i^1(p_i)=\frac{p_i-\ell_i}{u_i-\ell_i}.
\]

Both weights are nonnegative and sum to one. Applying one-coordinate affine interpolation twice
gives

\[
f(p_1,p_2)=\sum_{e_1,e_2\in\{0,1\}}
 \lambda_1^{e_1}(p_1)\lambda_2^{e_2}(p_2)
 f(c_{e_1e_2}).
\]

Thus every value is a convex combination of corner values and lies between their minimum and
maximum. Since each corner belongs to `C`, both bounds are attained. A degenerate coordinate is
deleted from the interpolation. This proof uses separate affinity, not an assumption that `f` is
jointly affine or convex; the term \(p_1p_2\) is permitted. \(\square\)

The same interpolation proves the finite-dimensional version with \(2^d\) corners. The executable
profile stops at \(d=2\); the general formula is not permission to extend bespoke enumeration
indefinitely.

## 4. Whole-policy expected loss

By Lemma 1 and Theorem 2, every named complete deterministic policy satisfies

\[
\max_{p\in C}J^\pi(p)
=\max_{c\in\operatorname{corners}(C)}J^\pi(c).
\]

The construction instantiates every corner as a complete ordinary sequential subject on the same
skeleton and loss unit. The persistent-family receiver then checks the one common policy against
every member. A family certificate alone is not a proof of this equality: the mapping and
condition-A warrant must be checked first.

## 5. Modelwise regret

For a finite explicitly covered deterministic class \(\Pi\),

\[
J^\pi(p)-V_\Pi(p)
=\max_{\sigma\in\Pi}\left[J^\pi(p)-J^\sigma(p)\right].
\]

Every difference is multi-affine because both policy costs are multi-affine under the same
skeleton condition. Finite maxima commute:

\[
\begin{aligned}
\max_{p\in C}[J^\pi(p)-V_\Pi(p)]
&=\max_{p\in C}\max_{\sigma\in\Pi}
       [J^\pi(p)-J^\sigma(p)]\\
&=\max_{\sigma\in\Pi}\max_{p\in C}
       [J^\pi(p)-J^\sigma(p)]\\
&=\max_{\sigma\in\Pi}\max_{c\in\operatorname{corners}(C)}
       [J^\pi(c)-J^\sigma(c)]\\
&=\max_{c\in\operatorname{corners}(C)}
       [J^\pi(c)-V_\Pi(c)].
\end{aligned}
\]

The second equality is maximization over the same product set `C × Π`; finiteness of \(\Pi\) and
continuity on compact `C` ensure maxima exist. The last equality is another exchange of two finite
maxima. Each regret subtraction occurs at the same parameter/corner. The invalid cross-pairing

\[
\max_p J^\pi(p)-\min_q V_\Pi(q)
\]

is not modelwise regret and is neither used nor certified.

## 6. Robust deterministic selection

If the supplied catalogue is checked to equal the complete deterministic observable-history
policy class, the same corner matrix exactly determines

\[
\arg\min_{\pi\in\Pi}\max_{p\in C}J^\pi(p)
\]

and

\[
\arg\min_{\pi\in\Pi}\max_{p\in C}[J^\pi(p)-V_\Pi(p)].
\]

The persistent-family receiver checks full deterministic coverage, exact modelwise policy values,
modelwise comparators, and all ties. This says nothing about randomized policies. A vector of
model-indexed policies is not one implementable observable-history policy and is rejected.

## 7. Statistical composition

Let `E` be the simultaneous-coverage event supplied by the checked PR14 construction, with
\(P(E)\ge 1-\alpha\). The receiver first checks the exact collection subject, transcript evidence,
rowwise scalar intervals, stream allocation, outward rectangle, and explicit stream-to-parameter
mapping. It does not empirically validate the supplied IID fixed-parameter or completeness
premises.

On `E`, the true named transition vector \(p^\star\) lies in the exported rectangle `C`. If the
multi-affine warrant and corner-family certificate establish an expected-loss cap \(B_L\) or
regret cap \(B_R\) for every point of `C`, then the same cap holds at \(p^\star\) on `E`.
Consequently, under the statistical premises, the cap statement holds with probability at least
\(1-\alpha\).

This is logical implication on the coverage event, not addition of unlike quantities. Statistical
failure probability `alpha`, expected-loss/regret units, and numerical root-enclosure precision
remain separate fields. An outward dyadic rectangle may conservatively contain a smaller
confidence set. The corner theorem is exact over the rectangle actually exported; it does not
claim that rectangle is the exact confidence region.

## 8. Constructive receiver procedure and provenance

For the bounded profile the receiver performs the following finite procedure:

1. validate the intended collection subject and replay the retained PR14 coverage evidence;
2. require an exact bijection between its one or two stream identities and the transition
   parameter identities;
3. validate the immutable parametric skeleton and all exact fixed costs;
4. enumerate every terminal and early-`STOP` skeleton path and independently count parameter
   factors;
5. return `invalid-corner-reduction-warrant` if condition A fails, without calling the sequential
   problem impossible;
6. map the checked stream rectangle into parameter order and instantiate its distinct corners;
7. reconstruct the persistent family and pass exact policy matrices through the unchanged family
   consumer;
8. recompute every corner value by independent forward complete-path enumeration;
9. compute named loss and paired modelwise regret; and
10. only for a complete checked catalogue, return deterministic minimax-loss and minimax-regret
    winners.

The evidence binds the complete collection/revision, mapping, template, costs, policy catalogue,
named policy, query, and caps. A changed transcript, statistical revision, mapping, transition
law, loss, policy, class, or query requires new evidence. Candidate producers may be disabled
while both the statistical and corner/family receivers continue to check retained evidence.

## 9. Fixed two-parameter construction

The checked fixture uses the existing round-robin multistream machinery with `alpha = 1/20`, two
allocations of `1/40`, 16-bit outward brackets, eight zeros in `stream-1`, and eight ones in
`stream-2`. Its retained rectangle is

\[
\texttt{stream-1}\in[0,43333/65536],\qquad
\texttt{stream-2}\in[22203/65536,1].
\]

The deliberately permuted explicit mapping is

\[
\texttt{stream-2}\mapsto p_1=\texttt{p-route},\qquad
\texttt{stream-1}\mapsto p_2=\texttt{p-followup}.
\]

One forced root action costs `2` and observes `L` with probability \(p_1\), otherwise `R`. At `L`,
`hold` stops for `-2`, while `inspect` costs `-2` and adds terminal cost `1` with probability
\(p_2\). At `R`, `hold` stops for `-1`, while `inspect` costs `-2` and adds terminal cost `2` with
probability \(p_2\). Costs are signed but parameter-independent. The use of \(p_2\) at `L` and `R`
is admissible because those nodes are mutually exclusive.

For child choices `H` = hold and `I` = inspect,

\[
\begin{array}{c|c}
\pi & J^\pi(p_1,p_2)\\ \hline
HH & 1-p_1\\
HI & 2p_2(1-p_1)\\
IH & 1-p_1+p_1p_2\\
II & 2p_2-p_1p_2.
\end{array}
\]

All four corner models are completed, including exact zero-probability branches. The family
checker and independent path sums agree. `HH` uniquely minimizes worst expected loss, while `HI`
uniquely minimizes worst regret. For the named policy `HI`,

\[
\max_C J^{HI}=\frac{1877748889}{2147483648}<1,
\qquad
\max_C[J^{HI}-V_\Pi]
=\frac{457813145}{2147483648}<\frac14.
\]

An independent `17 × 17` exact rational grid over the entire rectangle includes all corners and
reproduces every policy's corner worst cost, worst regret, and both winners. It is a falsification
check, not the proof; Theorems 1–2 establish all real interior points.

The simultaneous coverage lower bound is `19/20` under the supplied row premises. The fixture
does not empirically establish those premises or the substantive meaning of either transition.

## 10. Mandatory failure boundary

Condition A cannot be dropped. Let one parameter \(p\in[0,1]\) govern two sequential binary
factors. Give loss `1` only to the path whose first factor contributes \(p\) and whose second
factor contributes \(1-p\). Then

\[
J(p)=p(1-p).
\]

At the interval corners, \(J(0)=J(1)=0\), but \(J(1/2)=1/4\). On the nontrivial interval
`[1/4,3/4]`, both corner values are `3/16`, again below the interior value `1/4`. A corner-only
maximum is false.

The executable checker recognizes the completed sequential skeleton and can instantiate it at
any supplied point, but returns `invalid-corner-reduction-warrant`. The decision problem remains
mathematically valid and may be solved by another optimization method. This differs from
`unfinished`, which denotes a supported kind of request beyond the current two-parameter/four-
corner implementation budget.

## 11. Adversarial coverage

The exact cases cover:

- one unobserved parameter with exported interval `[0,1]`;
- the positive two-parameter rectangle and all four completed corners;
- one parameter reused at mutually exclusive nodes but never twice on a path;
- signed costs, early `STOP`, terminal costs, and exact zero-probability branches;
- a deliberately loose valid outward `[0,1]^2` export;
- permuted mapping order and missing, duplicate, or extra mapping identities;
- stale collection evidence and changed transition/loss subjects;
- one common total policy across all corners and rejection of model-indexed policy vectors;
- independent forward path values against the persistent-family matrix;
- full deterministic enumeration with distinct minimax-loss and minimax-regret winners;
- producer-disabled statistical and family receiving;
- signed multi-affine minimum as well as maximum checks; and
- the required repeated-parameter counterexample on both intervals.

## 12. Explicit limits and programme consequence

The executable profile has at most two uncertain parameters, four corner models, the inherited
finite history/action limits, and the inherited 64-policy full catalogue. It adds no randomized
optimization, adaptive alpha allocation, continuous or polynomial optimizer, generic planner,
Julia/JuMP migration, causal effect, dynamic risk, structural graph interface, Lean development,
or Writ/Decision Lab integration.

This composition earns one precise bridge: under a checked data-derived simultaneous rectangle
and a checked pathwise multi-affine warrant, continuous parameter uncertainty for whole-policy
expected loss and deterministic regret can be represented exactly by the existing finite
persistent corner family. It does not earn the bridge when a parameter can re-enter along a path.
If parameter or corner growth becomes the real bottleneck, that is the trigger to evaluate an
established optimization route rather than extending bespoke enumeration.
