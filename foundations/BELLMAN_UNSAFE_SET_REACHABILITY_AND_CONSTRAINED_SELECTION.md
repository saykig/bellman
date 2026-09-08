# Bellman unsafe-set reachability and robust constrained policy selection

**Standing.** Additive bounded mathematical companion built from the reviewed sequential,
persistent-family, and statistical-corner constructions. It earns one exact risk/constraint
primitive. It is not an authority-to-act rule, an empirical validation of a model or unsafe-set
definition, a generic safety framework, or a tail/dynamic-risk construction.

Base: `2727f7b578cf7bab40cfc1cbb4def583cf7da84d`, the merge of reviewed PR #16.
All earlier mathematical and historical artifacts remain unchanged.

## 1. Subject, query, and meaning

Let (F) be one finite completed observable-history subject from the sequential-certificate
construction. It supplies a finite horizon, exact rational transition laws, signed exact rational
stage and terminal costs in one loss unit, complete action/outcome menus, and all structurally
possible histories. Let (pi) be one complete deterministic history policy.

An identified unsafe set (H_{mathrm{bad}}) is an explicitly supplied subset of the subject's
completed observable histories. Its members need not be terminal, reachable with positive
probability, or prefix-free. The declaration's identity and exact members are part of the query.
Probability theory does not establish that this is the correct normative or operational definition
of harm.

The operation is

\[
q_F^\pi(\varnothing)
=P_F^\pi\{\text{the episode ever visits a history in }H_{\mathrm{bad}}\}.
\tag{U1}
\]

This is a model-implied event probability. It is not expected additive loss, statistical coverage
failure, empirical frequency validation, or authorization. The underlying sequential subject is
not modified. Unsafe histories become absorbing only inside the calculation of (U1).

## 2. Exact recurrence and first-hit theorem

For every completed history (h), define

\[
q_F^\pi(h)=
\begin{cases}
1,&h\in H_{\mathrm{bad}},\\
0,&h\notin H_{\mathrm{bad}}\text{ and }h\text{ is terminal},\\
0,&h\notin H_{\mathrm{bad}}\text{ and }\pi(h)\text{ is STOP},\\
\sum_oP_F(o\mid h,a)q_F^\pi(hao),
 &h\notin H_{\mathrm{bad}},\ a=\pi(h)\text{ continues}.
\end{cases}
\tag{U2}
\]

> **Theorem 1 — reachability soundness.** The root of (U2) is exactly the probability in
> (U1).

**Proof by induction.** At an unsafe history, the event has already occurred, so its conditional
indicator is one regardless of later transitions. At a nonunsafe terminal or STOP history there is
no later history, so the indicator is zero. At a nonunsafe continuing history, partition by the
next outcome and apply the law of total probability. The child quantities are exact by backward
induction on remaining horizon, giving (U2) and then (U1) at the root. (square)

There is an equivalent path proof. Traverse the policy-induced tree and stop a path at its first
unsafe prefix. The cylinder events represented by distinct first-hit paths are disjoint, and their
union is exactly the event of ever hitting (H_{mathrm{bad}}). Therefore

\[
q_F^\pi(\varnothing)=
\sum_{\omega\in\Omega_{\mathrm{first\ hit}}}P_F^\pi(\omega).
\tag{U3}
\]

This expansion is also an independent finite check of the backward recurrence.

### Three invalid shortcuts

1. **Summing unsafe-node masses double-counts.** If one deterministic trajectory visits unsafe
   history (h_1) and later unsafe history (h_2), its hit probability is one but the two node
   marginals sum to two. First-hit absorption counts the trajectory once.
2. **Terminal-only labels miss transient harm.** A deterministic path may enter an unsafe
   nonterminal history, recover, and end at an unmarked safe terminal. Its exact hit probability is
   one while terminal-only inspection returns zero.
3. **Expected loss is a different object.** A policy may have signed expected additive cost (-2)
   and unsafe-hit probability (1/10). Neither number can substitute for the other; the loss unit
   is not a probability unit.

## 3. Certificate and independent receiver

A certificate binds:

- the complete exact subject and a separate model identity;
- one complete deterministic policy;
- the unsafe-set identity and exact history set;
- an exact nodewise reachability table and root value; and
- an optional exact cap (delta\in[0,1]) and its Boolean comparison result.

The receiver independently validates the subject, policy, and unsafe histories, recomputes every
case of (U2), checks the claimed root and cap, and requires equality with the forward first-hit sum
(U3). It does not invoke the candidate producer. A changed model, policy, unsafe-set identity or
membership, cap, or query is a new claim and cannot consume the old certificate.

If the check establishes

\[
q_F^\pi(\varnothing)\le\delta,
\tag{U4}
\]

it establishes only that inequality under the supplied (F,pi,H_{mathrm{bad}}). It does not
establish empirical correctness of (F), normative adequacy of (H_{mathrm{bad}}), or authority
to act.

## 4. Persistent model-family safety

Let (mathcal F=(F_1,\ldots,F_m)) be a checked persistent family on one common completed skeleton.
One member remains fixed throughout an episode, its identity is not observed, and no member weights
are supplied. The same accessible policy (pi) and unsafe declaration are evaluated in every
member:

\[
q_i^\pi=P_{F_i}^\pi(\operatorname{hit}H_{\mathrm{bad}}),\qquad
q_{\mathrm{worst}}^\pi=\max_iq_i^\pi.
\tag{U5}
\]

The policy is robustly safety-feasible at cap (delta) exactly when

\[
q_i^\pi\le\delta\quad\text{for every }i.
\tag{U6}
\]

The receiver preserves each model identity and exact probability before taking the maximum. A
vector of member-indexed policies is not one implementable policy and rejects. A zero-probability
unsafe branch in one member remains a completed structural branch and contributes zero there; the
same branch may have positive probability in another member and then determines failure of (U6).
Early STOP before the unsafe region gives zero reachability without deleting the off-support
completion.

## 5. Robust constrained deterministic selection

Let the supplied policy catalogue be (Pi_0). Its scope is checked as either the complete bounded
deterministic history-policy class (**FULL**) or a named proper subset. Define one fixed robustly
feasible class

\[
\Pi_\delta=\{\pi\in\Pi_0:\max_iq_i^\pi\le\delta\}.
\tag{U7}
\]

The class in (U7) is the same for every model. It is not replaced by member-dependent classes
(Pi_{delta,i}).

For exact whole-policy cost (J_i^\pi), constrained minimax expected loss is

\[
\operatorname*{argmin}_{\pi\in\Pi_\delta}\max_iJ_i^\pi.
\tag{U8}
\]

For a named (pi\in\Pi_\delta), define the memberwise comparator over that same fixed class,

\[
V_i^\delta=\min_{\sigma\in\Pi_\delta}J_i^\sigma,
\qquad
\rho_\delta(\pi)=\max_i[J_i^\pi-V_i^\delta].
\tag{U9}
\]

Every subtraction in (U9) retains one model identity. The bounded checker can also return every
feasible deterministic policy minimizing (U9). This does not establish a randomized-policy result.

> **Theorem 2 — exact finite constrained choice.** If the persistent-family receiver checks the
> complete cost matrix (J_i^\pi), every reachability cell passes Theorem 1 and the independent
> first-hit check, and FULL coverage is established when claimed, finite filtering by (U7) followed
> by the extrema in (U8)–(U9) returns the exact constrained deterministic results for the declared
> catalogue.

**Proof.** The checked matrices contain the exact values for every pair in the finite product
(mathcal F\timesPi_0). Coordinatewise comparison with (delta) therefore constructs exactly
(Pi_delta). Finite maxima and minima then give (U8) and (U9), including every tie. (square)

If (Pi_delta) is empty, FULL coverage warrants only: no deterministic policy in the completely
covered bounded class satisfies the cap. Subset coverage warrants only: no supplied policy
satisfies it. Neither is real-world impossibility or infeasibility of a broader policy space.

### Operative-constraint control

In the fixed two-member case, `aggressive` has signed expected cost (-2) in both members and unsafe
probabilities (0,1/10). `cautious` stops early, costs (-1), and has unsafe probability zero.
At (delta=1/20), the unconstrained lower-cost policy is excluded and `cautious` is the unique
constrained minimax-loss winner. At (delta=1/10), `aggressive` becomes feasible and is the unique
winner. Thus the selection is driven by the declared cap, not a hard-coded action preference.

## 6. Statistical rectangle to corner-family reachability

Let a retained PR #16 request provide a checked outward rectangle

\[
C=\prod_{j=1}^d[\ell_j,u_j],\qquad d\le2,
\tag{U10}
\]

an explicit bijection from statistical stream identities to transition-parameter identities, and
a fixed parametric completed skeleton. Retain PR #16's pathwise condition:

> for every uncertain parameter and every complete skeleton path, that parameter occurs in at most
> one parameter-dependent transition factor on the path.

For a fixed policy, each first-hit path in (U3) is a prefix of at least one complete skeleton path.
Its probability is a product of fixed factors and at most one affine Bernoulli factor per parameter.
It is therefore multi-affine. A finite sum preserves multi-affinity, so

\[
q^\pi(p)=\sum_{\omega\in\Omega_{\mathrm{first\ hit}}}P_p^\pi(\omega)
\tag{U11}
\]

is multi-affine. PR #16's interpolation theorem then gives

\[
\max_{p\in C}q^\pi(p)=
\max_{c\in\operatorname{corners}(C)}q^\pi(c).
\tag{U12}
\]

Thus the same completed corner family exactly represents the rectangle-wide reachability query.
A valid family of corner subjects is not by itself the warrant for (U12): the statistical evidence,
mapping, immutable skeleton, and pathwise condition must all be checked first.

### Statistical guarantee and typed probabilities

Let (E) be the checked simultaneous-coverage event, with (P(E)\ge1-\alpha). On (E), the true
parameter vector (p^\star) lies in the exported rectangle. If (U12) and the family receiver show
(q^\pi(p)\le\delta) for every (p\in C), then
(q^\pi(p^\star)\le\delta) on (E).

The two probabilities have different events:

- (alpha) bounds failure of a random confidence region to cover an unknown parameter;
- (q^\pi(p)) is the model-implied probability of a future unsafe trajectory conditional on a
  particular parameter value.

Even when both numbers equal (1/20), they are not one unlabeled “5% uncertainty.” This contract
has no generic addition operation for them and does not certify (alpha+delta) as a universal
total-risk quantity. Statistical enclosure precision is a third, deterministic quantity. An
outward rectangle may be conservative; (U12) is exact over the exported rectangle and does not say
the export is the exact confidence region.

## 7. Repeated-parameter failure boundary

The pathwise condition cannot be removed. Let one parameter (p) govern two sequential factors and
mark as unsafe only the path having probability

\[
q(p)=p(1-p).
\tag{U13}
\]

On `[0,1]`, both corners give zero while (q(1/2)=1/4). On `[1/4,3/4]`, both corners give `3/16`
while the interior value remains `1/4`. The subject remains a valid finite sequential decision
problem, but it receives `invalid-corner-reachability-warrant` and needs a different optimization
method. This is distinct from an unfinished implementation budget and from mathematical
impossibility.

Using the same parameter at several mutually exclusive nodes is admissible when no complete path
visits two such occurrences. Zero-probability branches do not relax the structural condition.

## 8. Exact checked profile and constructive procedure

The reference receiver performs these finite operations:

1. validate the complete subject, common policy, unsafe-set identity, and optional cap;
2. recompute the exact backward recurrence and independent forward first-hit expansion;
3. for a persistent family, repeat without model weights and retain every model identity;
4. for selection, reuse the existing exact expected-cost matrix and policy coverage receiver,
   independently check every reachability cell, form one fixed (Pi_delta), and compute exact
   constrained extrema;
5. for a statistical request, first invoke the PR #16 statistical/mapping/admissibility receiver,
   then build the safety matrix on its reconstructed corner family; and
6. use an exact `17 × 17` rational grid as additional falsification evidence for the two-parameter
   fixture, not as proof of the real-valued theorem.

The positive statistical fixture has

\[
p\in[22203/65536,1],\qquad
q\in[0,43333/65536],\qquad q^{\mathrm{risky}}=p(1-q).
\]

Its four exact corner reachabilities are

\[
22203/65536,
492973209/4294967296,
1,
22203/65536.
\]

At cap (1/2), only `guard` is robustly feasible and wins constrained minimax loss; at cap one,
`risky` becomes feasible and wins. Independent first-hit paths, independent complete cost paths,
the existing family checker, direct formulas, and the exact interior audit agree. Further controls
cover one unconstrained `[0,1]` parameter, mutually exclusive reuse, signed costs, early STOP,
zero/positive unsafe branches, loose outward rectangles, mapping permutation and malformed
mappings, hidden model policies, FULL/subset empty classes, stale statistical evidence, changed
model/policy/unsafe set/cap, false tables/winners/comparators, and producer-disabled receiving.

These authored fixtures are exact conformance and falsification evidence, not formal verification,
empirical safety validation, or independently authored proof.

## 9. Limits and programme consequence

The executable profile inherits at most four persistent models, at most 64 policies for FULL
coverage, horizon four, and the PR #16 limit of two uncertain parameters/four corners. It covers
complete deterministic observable-history policies only. It adds no CVaR, entropic or recursively
coherent risk, general chance-constrained optimization, resources, continuous state/action space,
occupancy LP, randomized policies, causal effects, adaptive alpha allocation, new language,
formalization, Writ integration, or Decision Lab integration.

Finite exact enumeration remains small, so no solver or language trigger was reached. Substantially
larger constrained catalogues or hard resource constraints would trigger evaluation of an
established optimization route such as Julia/JuMP rather than indefinite bespoke enumeration.

This component earns the first bounded constraints/risk primitive: exact unsafe-set hitting
probability, unweighted persistent-family safety, deterministic policy selection under one fixed
robust cap, and—under the inherited multi-affine warrant—exact statistical-rectangle reduction to
corner safety models. Resource/operational constraints, loss-tail distributions and CVaR,
dynamically consistent risk, larger constrained optimization, randomized feasibility, and the
empirical validity of unsafe-set and model declarations remain open.
