# Bellman longitudinal causal kernel fibres and persistent decisions

**Status:** additive bounded construction, 8 September 2026. This companion does not revise the
one-stage causal foundation, the two-stage longitudinal bridge, the persistent-model foundation,
or any historical result. Its exact reference is under
[`verification/longitudinal_causal_kernel_fibres/`](../verification/longitudinal_causal_kernel_fibres/README.md).

## 1. Question, object, and boundary

The observed temporal order is the two-stage binary structure already used by Bellman,

\[
A_1\longrightarrow L_1\longrightarrow A_2\longrightarrow Y.
\]

The input is a complete exact rational law \(P(A_1,L_1,A_2,Y)\), population and coding identities,
the separately named longitudinal causal premises from the preceding construction, a complete
32-policy deterministic structural catalogue, and exact additive costs and terminal losses. The
query is what policy values and deterministic decisions follow when first-stage and intermediate
kernels are point identified but some second-stage outcome rows lack treatment positivity.

The object constructed here is an **exact saturated interventional-kernel completion fibre**. It is
exact because the supplied profile explicitly imposes no cross-row restrictions on its missing
binary outcome kernels. It is not claimed to be the fibre of every structural causal model that
might additionally impose monotonicity, rank preservation, common errors, mediation restrictions,
cross-world restrictions, or parametric structure. Such a stronger request receives
`unsupported-causal-completion-restriction`; silently dropping the restriction would turn an outer
relaxation into a false exact claim.

The observational law and causal premises are supplied rather than learned or empirically
validated. Free coordinates below express causal identification uncertainty, not sampling
uncertainty or posterior model probabilities. This construction does not discover a causal graph,
transport between populations, authorize action, or implement randomized policies.

## 2. Bounded support profile

Require

\[
P(A_1=a)>0\quad(a=0,1),                                      \tag{K1}
\]

and

\[
P(A_1=a,L_1=l)>0\quad(a,l\in\{0,1\}).                        \tag{K2}
\]

Thus every first-stage/intermediate interventional row in this profile is point identified. At
each positive \((a,l)\), at least one observed second action necessarily has positive probability.
For a second action \(b\), write

\[
s_{alb}=P(A_1=a,L_1=l,A_2=b).
\]

If \(s_{alb}>0\), the identified bad-outcome row is

\[
q_{alb}=P(Y=1\mid A_1=a,L_1=l,A_2=b).                         \tag{K3}
\]

If \(s_{alb}=0\), let \(m=(a,l,b)\) be an explicitly ordered missing row and introduce

\[
\theta_m=P(Y=1\mid do(A_1=a),L_1=l,do(A_2=b))\in[0,1].        \tag{K4}
\]

There can be at most one missing action row at each of four positive histories, hence
\(0\le k\le4\) missing rows. A failure of (K1) or (K2) is
`outside-second-stage-kernel-fibre-profile`. It does not assert incompatibility, zero effect, or
mathematical impossibility. In particular, the preceding policy-specific receiver may still
identify a policy that stays on supported branches. This component does not fabricate a missing
earlier-stage kernel or reclassify it as a free second-stage outcome row.

## 3. Exact continuous saturated fibre

Let \(M=(m_1,\ldots,m_k)\) be the exact support-derived missing-row order and

\[
\Theta=[0,1]^k.
\]

For \(\theta\in\Theta\), construct the complete causal sequential subject \(F_\theta\):

1. root action \(a\) emits \(l\) with the identified
   \(p_l(a)=P(L_1=l\mid A_1=a)\);
2. at \((a,l)\), second action \(b\) emits \(Y=1\) with \(q_{alb}\) when (K3) is supported and
   with \(\theta_{alb}\) when (K4) is missing;
3. the complementary outcome probability is one minus that value; and
4. the action costs and terminal losses are fixed across completions.

Define

\[
\mathcal C=\{F_\theta:\theta\in\Theta\}.                     \tag{K5}
\]

**Theorem A (exact saturated completion fibre).** Under (K1)--(K2), the supplied longitudinal
causal premises, and the explicit saturated no-cross-row-restriction profile, (K5) is exactly the
set of completed interventional kernels represented by this interface.

**Proof.** Every member of (K5) retains every identified \(p_l(a)\) and \(q_{alb}\). Each missing
binary row is \((1-\theta_m,\theta_m)\), so it is nonnegative and normalized. Conversely, every
normalized binary completion of a missing row has exactly one bad-outcome probability in
\([0,1]\). The profile supplies no equation or inequality coupling different missing rows, so any
ordered tuple of these probabilities is admitted and gives one member of (K5). Hence the Cartesian
product is neither missing a represented completion nor adding one relative to this interface.
\(\square\)

The last sentence is profile-relative. It does not prove that every \(F_\theta\) satisfies a
stronger unimplemented SCM assumption. If such an assumption is later supplied, (K5) may be only
an outer relaxation until that stronger completion set is characterized exactly.

When \(k=0\), \(\Theta\) is a singleton. The construction deliberately calls the preceding
full-support subject constructor and requires the sole subject, all 32 policy distributions and
values, and the complete minimizing set to agree exactly. There are not two divergent notions of a
fully identified two-stage causal Bellman subject.

## 4. Policy distributions and additive values

A complete deterministic policy \(\pi\) gives one root action \(a\) and a second action
\(d_\pi(a',l)\) at every structural history. Its bad-outcome probability at completion \(\theta\)
is

\[
r^\pi(\theta)=\sum_l p_l(a)q^\theta_{al,d_\pi(a,l)},           \tag{K6}
\]

where a supported \(q\) is constant and a missing selected row is its named \(\theta_m\). The full
binary outcome distribution is \((1-r^\pi(\theta),r^\pi(\theta))\). For first-action costs
\(c_1\), second-action costs \(c_2\), and terminal loss \(G\),

\[
\begin{aligned}
J^\pi(\theta)={}&c_1(a)+\sum_l p_l(a)\big[c_2(a,l,d_\pi(a,l))\\
&+(1-q^\theta_{al,d_\pi(a,l)})G(a,l,d_\pi(a,l),0)\\
&+q^\theta_{al,d_\pi(a,l)}G(a,l,d_\pi(a,l),1)\big].          \tag{K7}
\end{aligned}
\]

Signed costs are allowed. Every quantity retains the supplied loss unit.

**Theorem B (multi-affine policy queries).** Each component of the outcome distribution in (K6)
and the additive value (K7) is multi-affine in \(\theta\). In this two-stage profile it is in fact
additive affine: a trajectory uses exactly one second-stage outcome row, and a fixed policy uses at
most one row below each reached intermediate history.

**Proof.** Each summand is either constant or a constant coefficient times one named
\(\theta_m\). Finite sums preserve affinity in each coordinate. The complement \(1-r^\pi\) does
also. \(\square\)

For a multi-affine \(f:[0,1]^k\to\mathbb R\), repeated one-coordinate interpolation gives

\[
f(\theta)=\sum_{c\in\{0,1\}^k}f(c)
\prod_{j=1}^k\theta_j^{c_j}(1-\theta_j)^{1-c_j}.              \tag{K8}
\]

The weights are nonnegative and sum to one. Therefore

\[
\min_c f(c)\le f(\theta)\le\max_c f(c),                      \tag{K9}
\]

with both bounds attained at corners. Thus exact policy outcome and loss intervals, including all
attaining corner witnesses, follow from at most \(2^4=16\) completed subjects.

The finite corner family is not the continuous fibre when \(k>0\). It is an exact extremal
representative only for query classes justified by (K8): deterministic policy outcome
probabilities, expected additive loss, pairwise deterministic policy differences, and the finite
decision criteria below. For example, \(g(q)=q(1-q)\) is zero at both corners of \([0,1]\) but
equals \(1/4\) at \(q=1/2\). An arbitrary nonlinear causal query therefore receives no corner
warrant.

A policy has `point-identified-across-kernel-fibre` status when both its distribution and loss
intervals are singletons; otherwise it is `partially-identified-across-kernel-fibre`. A policy
that selects only supported rows can stay point identified while other policies and the complete
subject remain partial.

## 5. Decisions across one fixed hidden completion

The true completion is one member \(F_\theta\) that remains fixed throughout an episode. The
policy does not observe \(\theta\). Bellman therefore evaluates one complete implementable policy
on every completion. A vector choosing a different policy by hidden corner, or a trajectory made
from rows belonging to inconsistent corner assignments, is not a policy in this problem.

For candidate \(\pi\) and competitor \(\sigma\), define the same-completion difference

\[
D_{\pi\sigma}=\max_{\theta\in\Theta}
[J^\pi(\theta)-J^\sigma(\theta)].                             \tag{K10}
\]

The difference is multi-affine, so Theorem B and (K9) give

\[
D_{\pi\sigma}=\max_{c\in\{0,1\}^k}
[J^\pi(c)-J^\sigma(c)].                                      \tag{K11}
\]

**Theorem C (common causal decision).** The exact common minimizing set is

\[
\Pi_{\rm common}=\{\pi:D_{\pi\sigma}\le0\text{ for every }\sigma\}. \tag{K12}
\]

A policy is in (K12) if and only if it minimizes loss in every \(F_\theta\).

**Proof.** If every pairwise difference is nonpositive at every completion, the candidate is no
worse than every competitor there and is minimizing. Conversely, a policy minimizing at every
completion has every pointwise difference nonpositive, hence each maximum is nonpositive. Equation
(K11) makes the finite check exact. \(\square\)

A nonempty set receives `causal-decision-identified-across-every-completion`; the complete set is
returned, preserving off-root ties. An empty set receives
`causal-decision-model-dependent-across-completions`, together with exact corner minimizing sets
that witness the disagreement. It is not forced into consensus.

### 5.1 A separately supplied robust criterion

Minimax expected loss is

\[
M(\pi)=\max_{\theta\in\Theta}J^\pi(\theta),\qquad
\Pi_{\rm minimax}=\arg\min_\pi M(\pi).                        \tag{K13}
\]

Equation (K9) checks each inner maximum at corners. The complete minimax set can exist even when
(K12) is empty. That selection is a supplied robust criterion over causal ambiguity; it is not a
claim that the winner is causally identified as modelwise optimal.

For same-completion regret let

\[
V(\theta)=\min_\sigma J^\sigma(\theta),\qquad
\rho(\pi)=\max_\theta[J^\pi(\theta)-V(\theta)].                \tag{K14}
\]

Because the policy class is finite,

\[
\begin{aligned}
\rho(\pi)
&=\max_\theta\max_\sigma[J^\pi(\theta)-J^\sigma(\theta)]\\
&=\max_\sigma\max_\theta[J^\pi(\theta)-J^\sigma(\theta)]\\
&=\max_\sigma\max_c[J^\pi(c)-J^\sigma(c)].                  \tag{K15}
\end{aligned}
\]

Every subtraction is inside one completion. The shortcut
\(\max_\theta J^\pi(\theta)-\min_\phi V(\phi)\) is invalid because its two extrema may use
different causal models. The receiver requires identical completion identities for a direct
regret subtraction.

## 6. Decisive exact fixtures

### 6.1 One missing row

Let both first actions and both intermediate values conditional on each first action be fair. At
\((A_1,L_1)=(0,0)\), observe only \(A_2=0\), with bad-outcome risk \(1/2\); the missing
\(A_2=1\) risk is \(q\in[0,1]\). At \((0,1)\), supported action 0 has risk zero and action 1 has
risk one. Both actions are supported below root 1, whose exact first-stage cost is 2. Other action
costs are zero and terminal loss is \(Y\).

The supported reachable rule \(S=(A_1=0;A_2=0,0)\) has
\(J^S=1/4\). The rule \(U=(A_1=0;A_2=1,0)\) has \(J^U(q)=q/2\), hence exact interval
\([0,1/2]\). At \(q=0\), every complete-policy variant of \(U\)'s reachable rule beats \(S\);
at \(q=1\), every variant of \(S\)'s rule beats \(U\). The full 32-policy common set is empty.
Minimax loss nevertheless selects the supported rule because \(1/4<1/2\); that is (K13), not
causal decision identification. For \(U\), exact same-model worst regret is \(1/4\), while the
invalid cross-completion shortcut gives \(1/2\).

If only the missing action's second-stage cost is changed to 1, its value becomes
\(J^U(q)=1/2+q/2\). The causal row remains \([0,1]\), and \(U\) remains partially identified, but
the supported rule is now uniformly better. The exact common minimizing set is nonempty. Unknown
causal probability does not automatically mean unknown decision.

### 6.2 Two missing rows

Make \((0,0,1)\) and \((0,1,1)\) missing with coordinates \((q_0,q_1)\). A policy choosing both
has bad-outcome probability

\[
f(q_0,q_1)=(q_0+q_1)/2.
\]

In ordered corner order \((0,0),(0,1),(1,0),(1,1)\), the exact values are
\(0,1/2,1/2,1\). The interior point \((1/3,2/5)\) gives \(11/30\). This audit is falsification
evidence; the proof of corner sufficiency is (K8)--(K9).

## 7. Persistent-family composition and its boundary

Every corner subject has a stable identity containing the observation identity, ordered missing
row identities, and complete bit assignment. The corner family retains those model identities,
uses the same completed skeleton and loss unit, and evaluates the same complete policy in every
member. For \(k\le2\), the existing persistent-family receiver accepts the one-, two-, or
four-member family and independently reproduces the common-optimal, minimax-loss, and same-model
minimax-regret results.

The historical persistent reference deliberately supports at most four models. For \(k=3,4\), the
eight- or sixteen-corner family is checked by the new bounded exact receiver, and evidence records
`local-exact-corner-family-existing-persistent-limit`. The mathematical persistent semantics still
apply; the old checker is not silently widened or rewritten. This small mismatch is not an
optimization bottleneck: the maximum is only \(16\times32=512\) exact policy values.

Crucially, finite-family checking alone would not justify a continuous-fibre result. Theorem B is
the separate warrant connecting supported queries on (K5) to their corner extrema.

## 8. Constructive receiver and provenance

The candidate producer emits the continuous fibre description, ordered corner assignments,
completed subjects, a 32-policy value/distribution matrix with ordinary sequential certificates,
policy intervals and witnesses, pairwise maxima, common and robust decisions, and the applicable
persistent-family evidence. The authoritative receiver independently:

1. reconstructs first-stage/intermediate support and the exact support-derived missing-row order;
2. rejects an earlier-stage gap, stronger restriction, or unsupported query with its own status;
3. reconstructs \([0,1]^k\), all \(2^k\) assignments, and every completed transition row;
4. recomputes every policy distribution and loss directly from observational cell slices;
5. compares each value and distribution with independent complete-path enumeration and the
   existing sequential certificate consumer;
6. recomputes exact extrema, all corner witnesses, pairwise differences, common minimizers,
   minimax loss, and same-model regret; and
7. invokes the existing persistent receiver where its four-model bound permits.

The receiver never trusts a producer status. Retained evidence remains consumable with the new
producer, ordinary sequential producer, preceding bridge producer, and persistent-family producer
disabled.

Evidence binds exact observational masses and identity, population, coding, temporal order, all
causal-premise identities, completion-profile identity, missing-row identities and order, loss
table, all 32 policies and catalogue identity, continuous-fibre query, corner-family identity,
assignments, subjects, and certificates. Changed support, row order, premise, loss, policy,
catalogue, assignment, supported transition, interval, corner coverage, common set, or robust
winner rejects as stale or forged.

## 9. Guarantee, composition rule, and limits

The earned conditional statement is:

> If the supplied first-stage/intermediate causal kernels satisfy the named longitudinal premises
> and support conditions, and uncertainty is confined to unsupported binary second-stage outcome
> rows under the explicit saturated no-cross-row-restriction profile, then Bellman represents the
> exact continuous kernel fibre; computes exact deterministic policy outcome/loss intervals;
> reduces those queries and same-completion pairwise comparisons to the finite corners; and
> distinguishes point policies, common modelwise-optimal decisions, model-dependent decisions, and
> separately supplied minimax-loss and same-model-regret criteria.

Safe reuse requires the same observation, population, coding, temporal order, causal premises,
profile, missing-row order, loss, policy class, and supported query kind. A finite corner family is
not reusable for an arbitrary nonlinear query. A stronger causal restriction needs its own exact
fibre or an honestly labelled outer relaxation. A changed subject or policy receives a new claim.

The executable profile is limited to binary \(A_1,L_1,A_2,Y\), two treatment dates, exact rational
16-cell observations, missing second-stage outcome rows only, at most four free rows, 16 corners,
and 32 deterministic policies. It adds no missing earlier-stage kernels, longitudinal response-type
SCM enumeration, arbitrary cross-world restrictions, extra stages, continuous variables,
randomized policies, transport, estimation, confidence sets, unsafe-set composition, tail/dynamic
risk, graph infrastructure, Writ/Decision Lab transfer, or authority claim. Analytical proofs and
bounded exact checks are not proof-assistant formalization.

Enumeration remained tiny and exact. No evidence-triggered threshold for Julia/JuMP, Rust, Lean, or
another language or solver was reached.

## 10. Next-gate judgment

The nearest decision-relevant open interfaces now include causal-kernel-family composition with
unsafe-set reachability, statistical estimation/coverage for longitudinal causal rows, population
transport, and exact stronger longitudinal restrictions. This result does not precommit their
order. A next build should be selected from substantive need and a precise compositional warrant,
not by mechanically enlarging the present enumeration.
