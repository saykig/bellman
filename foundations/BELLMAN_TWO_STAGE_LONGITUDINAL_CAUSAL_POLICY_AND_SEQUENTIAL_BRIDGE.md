# Bellman two-stage longitudinal causal policy identification and sequential bridge

**Status:** additive bounded construction, 8 September 2026. This companion does not revise the
finite one-stage causal construction, the sequential-certificate foundation, or any historical
result. Its exact reference is under
[`verification/longitudinal_causal_policy/`](../verification/longitudinal_causal_policy/README.md).

## 1. Question and boundary

The object is a finite two-stage longitudinal causal decision in one identified population. The
observed temporal order is

\[
A_1\longrightarrow L_1\longrightarrow A_2\longrightarrow Y,
\]

where all four variables are binary. Bellman receives the complete exact rational observational
law \(P(A_1,L_1,A_2,Y)\), explicit variable coding and temporal identity, causal-premise
identities, an adapted complete deterministic policy, and exact costs and losses. It checks what
the longitudinal g-formula implies under those supplied premises.

The central distinction is:

1. a particular policy may be identified under support only for the treatment choices it makes at
   positive-probability histories; but
2. a complete Bellman sequential subject is identified only when every structural first- and
   second-stage action-history transition required by its full action menu is supported.

The first fact does not imply the second. The construction refuses the bridge when the stronger
condition fails while preserving any separately checked policy-specific result.

This is conditional causal mathematics. The observational bytes do not establish consistency,
exchangeability, absence of interference, the substantive meaning of interventions, measurement
quality, or deployment validity. The first profile permits no population transport. It does not
discover a causal graph, use a post-treatment adjustment shortcut, identify a longitudinal causal
fibre under missing support, compose with unsafe reachability, or authorize action.

## 2. Exact subject and policies

### 2.1 Supplied causal subject

Let \(L_1(a_1)\) and \(Y(a_1,a_2)\) denote the supplied intervention semantics in the identified
population. The premise bundle names, separately:

- consistency for the intermediate and final responses under the observed actions;
- the meaning of the interventions \(do(A_1=a_1)\) and adapted \(do(A_2=a_2)\);
- first-stage exchangeability sufficient for the joint counterfactual
  \((L_1(a_1),Y(a_1,a_2))\) not to depend on observed \(A_1\);
- second-stage sequential exchangeability of \(Y(a_1,a_2)\) and observed \(A_2\), conditional on
  the observed \((A_1,L_1)\) history;
- adaptation: the second action uses only the observable history \((A_1,L_1)\); and
- the first-profile no-interference/stable-unit boundary.

These descriptions state the mathematical content expected of the premise identities. A matching
string is not evidence that the premise is true. The observational and deployment population
identities must be identical; a different population needs a separate transport theorem.

### 2.2 Complete deterministic policies

A policy \(\pi\) supplies a root action \(a_1\) and a second action
\(d_\pi(a'_1,l)\in\{0,1\}\) at each of the four structural histories
\((a'_1,l)\in\{0,1\}^2\). Thus the bounded complete class contains

\[
2\cdot 2^4=32
\]

policies. A policy whose root is \(a_1=0\) still supplies actions after structural histories whose
first action is 1. Policies that differ only at those presently unreachable histories remain
different complete policies. Bellman does not quotient them by the current root choice because a
complete policy is the reusable executable object and another query or model may make those
histories relevant.

### 2.3 Exact additive value

The supplied loss table contains exact signed quantities with one declared unit:

- \(c_1(a_1)\) at the first action;
- \(c_2(a_1,l,a_2)\) at the second action; and
- \(G(a_1,l,a_2,y)\) at the terminal history.

No nonnegativity is assumed. The query is the complete intervention distribution of \(Y\) and the
expected additive total cost of one named policy.

## 3. Policy-specific identification

For a policy with root action \(a_1\), write \(d(l)=d_\pi(a_1,l)\) for its action at the two
histories reachable under that root.

### 3.1 Positivity required by one policy

The policy-specific support conditions are

\[
P(A_1=a_1)>0,
\tag{L1}
\]

and, for each \(l\) such that \(P(L_1=l\mid A_1=a_1)>0\),

\[
P(A_2=d(l)\mid A_1=a_1,L_1=l)>0.
\tag{L2}
\]

There is no second-stage action-support obligation at a branch with
\(P(L_1=l\mid A_1=a_1)=0\): that term has zero intervention mass for this policy. Nor is support
for an unselected alternative action required merely to identify this policy. These omissions do
not identify the missing structural transitions needed by a complete subject.

### 3.2 The policy g-formula

**Theorem A (two-stage dynamic regime under supplied premises).** Under the causal premises in
section 2 and policy-specific positivity (L1)--(L2),

\[
P_\pi(Y=y)=
\sum_{l\in\{0,1\}}
P(Y=y\mid A_1=a_1,L_1=l,A_2=d(l))
P(L_1=l\mid A_1=a_1).
\tag{L3}
\]

Terms with zero \(P(L_1=l\mid A_1=a_1)\) are zero and require no outcome conditional. The two
values in (L3) form a complete normalized binary distribution.

**Proof.** Under adaptation and consistency, the policy response is
\(Y^\pi=Y(a_1,d(L_1(a_1)))\). Partition by \(L_1(a_1)\):

\[
P(Y^\pi=y)=\sum_l
P(Y(a_1,d(l))=y\mid L_1(a_1)=l)P(L_1(a_1)=l).
\]

First-stage exchangeability permits conditioning the joint counterfactual on \(A_1=a_1\), and
consistency then replaces \(L_1(a_1)\) by observed \(L_1\). Second-stage exchangeability permits
conditioning on \(A_2=d(l)\); second-stage consistency replaces the counterfactual response by
observed \(Y\). Conditions (L1)--(L2) make exactly those conditionals with positive regime mass
defined. The first-stage term likewise becomes
\(P(L_1=l\mid A_1=a_1)\). This gives (L3). Summing over \(y\) yields one because each positive
history supplies a complete conditional distribution. \(\square\)

### 3.3 Expected additive cost

The same decomposition gives

\[
\begin{aligned}
J^\pi={}&c_1(a_1)+\sum_lP(l\mid a_1)\Big[c_2(a_1,l,d(l))\\
&+\sum_yG(a_1,l,d(l),y)P(y\mid a_1,l,d(l))\Big].
\end{aligned}
\tag{L4}
\]

Linearity of finite expectation proves (L4), including for signed costs. The status is
`identified-dynamic-regime-under-supplied-sequential-premises`. Failure of (L1) is
`first-stage-positivity-failure`; failure of (L2) at a positive regime history is
`second-stage-policy-positivity-failure`. Neither failure means the causal effect is zero, the
causal premises are incompatible, or the broader decision is impossible.

The executable query kind is exactly a complete binary regime distribution plus exact additive
loss. A mediation effect, stochastic intervention, later-stage policy, or other query outside that
contract returns `unsupported-longitudinal-causal-query`; it is not silently reinterpreted as the
supported operation.

## 4. Strong support and the complete sequential subject

### 4.1 Strong support condition

The bounded bridge requires

\[
P(A_1=a)>0\quad\text{for every }a,
\tag{S1}
\]

\[
P(L_1=l\mid A_1=a)>0\quad\text{for every }(a,l),
\tag{S2}
\]

and

\[
P(A_2=b\mid A_1=a,L_1=l)>0
\quad\text{for every }(a,l,b).
\tag{S3}
\]

This condition is deliberately stronger than (L1)--(L2). It makes all first-stage intermediate
kernels and all second-stage outcome kernels for both actions identifiable on every structural
history. A deterministic outcome is permitted: outcome positivity is not required to identify a
complete binary conditional distribution.

### 4.2 Constructed Bellman subject

When (S1)--(S3) hold, construct the existing completed observable-history subject as follows:

1. At the root, action \(a\) pays \(c_1(a)\) and emits \(l\) with
   \(P(L_1=l\mid A_1=a)\).
2. At history \((a,l)\), action \(b\) pays \(c_2(a,l,b)\) and emits \(y\) with
   \(P(Y=y\mid A_1=a,L_1=l,A_2=b)\).
3. At terminal history \((a,l,b,y)\), pay \(G(a,l,b,y)\).

The skeleton, menus, labels, horizon, unit, and costs are parameter independent because they are
explicitly supplied here. The subject identity retains the observation, population, coding,
temporal order, causal-premise, loss, and policy-catalogue identities. The bridge evidence also
binds the exact 16 observational masses and all query identities.

### 4.3 Equivalence theorem

**Theorem B (causal-to-sequential bridge).** Under the premises of Theorem A and strong support
(S1)--(S3), the constructed subject is a complete identified two-stage causal subject. For every
one of the 32 complete deterministic policies:

1. its Bellman complete-path probability for terminal \((l,y)\) is
   \(P(l\mid a_1)P(y\mid a_1,l,d(l))\);
2. summing over \(l\) gives exactly the g-formula distribution (L3); and
3. the Bellman expected additive path cost equals (L4).

Consequently the complete minimizing policy set computed from the 32 causal g-formula values is
identical to the set computed on the constructed Bellman subject.

**Proof.** Fix a complete policy. Its root action is one \(a_1\). On the constructed tree the
probability of path \((l,y)\) is the product of its two transition rows,
\(P(l\mid a_1)P(y\mid a_1,l,d(l))\), by the finite chain rule. Summing those path masses over
\(l\) is (L3). The realized path cost is
\(c_1(a_1)+c_2(a_1,l,d(l))+G(a_1,l,d(l),y)\); its expectation under the same path masses is (L4).
This argument applies separately to every complete policy, including distinct policies that agree
on all histories reachable under their chosen root. Pointwise equality of all 32 values makes
their minima and complete attaining sets equal. \(\square\)

Strong support receives `full-two-stage-causal-subject-identified`; after construction and
independent sequential checking, the composition receives `causal-to-sequential-bridge-checked`.
If a named policy is identified but (S1)--(S3) fail, the bridge status is
`policy-identified-full-subject-not-supported`. The missing subject transition is not filled by
extrapolation, by a one-stage marginal, or by an arbitrary zero-probability completion.

## 5. One-stage intervention margins are insufficient

The one-stage construction from PR #19 correctly identifies the causal queries it states. Those
queries need not retain the history-conditioned kernels needed by an adaptive second-stage policy.
The following exact pair is decisive.

In both worlds let \(A_1\), \(L_1\), and observed \(A_2\) be independent fair bits. Let \(A_1\)
have no effect in this control. Both worlds therefore have full treatment support and can satisfy
the supplied randomized sequential-exchangeability premises.

In world \(W_+\), set \(Y=1\) exactly when \(A_2\ne L_1\):

| \(L_1\) | \(P(Y=1\mid A_2=0,L_1)\) | \(P(Y=1\mid A_2=1,L_1)\) |
|---:|---:|---:|
| 0 | 0 | 1 |
| 1 | 1 | 0 |

In world \(W_-\), reverse all four outcomes, so \(Y=1\) exactly when \(A_2=L_1\). In both worlds,

\[
P(Y=1\mid do(A_2=0))=P(Y=1\mid do(A_2=1))=1/2.
\tag{C1}
\]

Thus the two complete one-stage intervention marginals are identical. But the adapted policy
\(A_2=L_1\) has bad-outcome probability zero in \(W_+\) and one in \(W_-\); the opposite policy
\(A_2=1-L_1\) has probabilities one and zero. The optimal history-dependent policies are opposite.

This is not a positivity problem: both actions occur with probability \(1/2\) in every history.
It is not incompatibility: each world is a valid fully supported longitudinal causal model. The
one-stage marginals discarded the effect modification by \(L_1\). Therefore they cannot be
inserted as second-stage transition rows and cannot identify the adaptive sequential subject.

## 6. Exact certificate and receiver

Policy evidence binds the full 16-cell law, population, four coding identities and labels, temporal
order, all causal-premise identities, the complete four-history policy, policy-support query,
cost/loss table, and causal query. The receiver independently reconstructs first-stage support,
positive regime histories, selected-action support, the complete distribution, and (L4). It does
not trust a producer status.

Bridge evidence additionally binds the subject and policy-catalogue identities. The receiver:

1. checks (S1)--(S3) directly from the observational cells;
2. reconstructs every subject transition by a calculation path separate from the producer;
3. requires all 32 complete policies in fixed structural order;
4. recomputes each g-formula distribution and value;
5. passes each retained exact sequential certificate through the existing sequential receiver;
6. independently enumerates complete Bellman paths and compares their distribution and cost; and
7. checks equality of the complete causal and Bellman minimizing sets.

Changing any observational mass, population, coding, temporal order, consistency/intervention/
exchangeability/adaptation/interference premise, policy, cost, terminal loss, support query,
catalogue, constructed subject, or causal/sequential query creates a new claim. Stale evidence
rejects. Forged distributions, values, transitions, and sequential certificates reject. Retained
evidence remains checkable with both the causal and sequential candidate producers disabled.

## 7. Fixed exact results

The positive 16-cell control has \(P(A_1=1)=1/2\),
\(P(L_1=1\mid A_1=0)=1/4\), and \(P(L_1=1\mid A_1=1)=3/4\). Observed second-stage assignment is
strictly positive in every history. Bad-outcome probabilities are

| \(L_1\) | \(A_2=0\) | \(A_2=1\) |
|---:|---:|---:|
| 0 | \(1/10\) | \(4/5\) |
| 1 | \(9/10\) | \(1/5\) |

for either \(A_1\). The adapted policy choosing \(A_2=0\) after \(L_1=0\) and \(A_2=1\) after
\(L_1=1\) has bad-outcome probabilities \(1/8\) under root action 0 and \(7/40\) under root action
1. The unique reachable-history choice under root 0 is best, but its two off-root choices are
free, so the complete minimizing set contains four policies rather than silently collapsing them.

The reference checks all 32 values and distributions against a 21-node Bellman tree, including
signed-cost controls. Separate fixtures establish first-stage failure, reachable second-stage
failure, a zero-probability intermediate branch that needs no selected-action support, and an
identified policy whose missing alternative transition prevents full-subject construction.

## 8. Composition and limits

The bridge may feed existing Bellman sequential expected-additive operations only when its exact
subject, policy, costs, and premise identities match the receiving query. It does not automatically
feed persistent-family, statistical-corner, or unsafe-set machinery. Those joins would require an
explicit common population/model-family meaning, common skeleton and policy access, and any extra
support or unsafe-set premise demanded by the receiving theorem.

The executable profile is exactly 16 observational cells and 32 deterministic policies, with
binary \(A_1,L_1,A_2,Y\), two decision dates, exact rational inputs of at most 256 bits, and the
existing sequential limits. It does not implement:

- longitudinal partial-identification fibres or outer relaxations;
- more stages, larger state/action spaces, continuous variables, or randomized policies;
- censoring, missingness, measurement error, interference, transport, or mediation queries;
- statistical estimation, learned nuisance functions, or empirical premise criticism;
- causal-to-safety or causal-to-persistent-family composition;
- Writ or Decision Lab integration, formal proof, or authority to act.

The finite enumeration is tiny, so no optimization, Julia/JuMP, Rust, or Lean trigger was reached.
Analytical proofs plus exhaustive fixed rational checks are not formal verification.

The construction earns the first exact bridge from a fully identified two-stage longitudinal causal
law to Bellman's existing completed sequential decision subject. Its evidence also identifies the
nearest unresolved causal frontier: when policy-specific queries remain identifiable but one or
more structural transition kernels are not, a future task may need a justified longitudinal causal
fibre or model-family representation. This result does not assume or implement that extension.
