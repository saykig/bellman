# Bellman: family-aware replanning and preservation of a root guarantee

**7 September 2026. Additive finite construction; no novelty claim.**

Base: main commit `81eec793094bde8bb26fc88c3f4d6a99ef3ffdfe`, the merge of PR8.
The reviewed PR8 head `59da8f5b9d57afbe2b8c31e78886378f4f456bec` is an ancestor of that
commit and has the same file tree. PR8 and all earlier mathematics, results, reviews, and historical
evidence remain unchanged.

This construction answers one question: after replacing one common policy's continuation below an
observed history, do supplied certificates establish that a named ex-ante root cap still holds in
every fixed member of a persistent model family? The answer is a checked certificate splice and an
honest cap disposition. It is not a dynamic-consistency theorem, a robust planner, a model-learning
rule, or authority to preserve or abandon a commitment.

## 1. Assessment, subject, and separate warrants

The proposed upper-table splice is sound under the existing full-tree premises. Its proof uses
PR5's ordinary terminal and Bellman inequalities, PR8's ordered persistent family, and the
single-replacement path decomposition in S17. It is a new derived-certificate warrant, distinct
from PR6's pointwise one-sided anchored transport. In particular, its signed correction need not be
nonnegative and it has no claim to PR6's restricted extremality.

Let \(\mathcal F=(F_1,\ldots,F_m)\) be a nonempty ordered family as in PR8. Each member has the
same completed observable-history skeleton, legal action menus, horizon, unit, and expected
additive-cost criterion. One \(F_i\) remains fixed for an entire episode. Costs may be signed;
transition probabilities are nonnegative and normalized. The model index is not observable and no
weights over members are supplied.

Let \(\pi\) be one complete deterministic baseline policy, \(h\) one supplied history, and
\(\rho\) one complete deterministic candidate continuation. Define the total policy
\[
 \pi^h(g)=\begin{cases}
 \rho(g),&h\preceq g,\\
 \pi(g),&\text{otherwise},
 \end{cases}                                                   \tag{R1}
\]
at every decision history. Thus the entire subtree, including zero-support fallbacks, is replaced;
all other actions remain exactly those of the baseline. At a terminal cut the policy is unchanged.
At the root cut the whole policy becomes \(\rho\).

For every member, the request supplies two ordinary checked certificates:
\[
 L_i\le V_i\le J_i^\pi\le U_i,
 \qquad A_i\le V_i\le J_i^\rho\le B_i.                         \tag{R2}
\]
The lower tables concern the same full modelwise optimum. The upper tables concern their named
policies. The operation deliberately uses \(L_i,U_i,B_i\); \(A_i\) is still checked because the
replacement source is an ordinary certificate, but it is not substituted for the baseline
comparator.

Keep six warrants distinct:

1. ordinary validity of a certificate for \(F_i,\pi^h\);
2. derivation of that certificate from the two named sources by the splice below;
3. preservation of an existing root cap across the ordered family;
4. preference under a newly posed conditional criterion;
5. actual policy improvement relative to \(\pi\);
6. exact optimality in an explicitly covered candidate class.

The first three are the primary output. A valid ordinary target certificate can fail the second
warrant. A conditional preference can fail the third and fifth. No fresh global optimization is
needed to check a named policy against a cap.

## 2. Path factors and certificate-splice theorem

For \(g\prec h\), let \(w_i(g,h)\) be the product of the \(F_i\) transition probabilities along
the unique suffix of the named history from \(g\) to \(h\), provided \(\pi\) selects every required
action. If it diverges, including by STOP, set the product to zero. Put \(w_i(h,h)=1\). Values at
non-ancestors are recorded as zero by the reference. This is an algebraic path mass, not a posterior
at a zero-probability history.

Define
\[
 U_i^h(g)=
 \begin{cases}
 B_i(g),&h\preceq g,\\
 U_i(g)+w_i(g,h)[B_i(h)-U_i(h)],&g\prec h,\\
 U_i(g),&\text{otherwise}.
 \end{cases}                                                   \tag{R3}
\]

**Certificate-splice theorem.** The package
\((F_i,\pi^h,L_i,U_i^h)\) satisfies every ordinary S3–S4 inequality. Consequently
\[
 L_i(g)\le V_i(g)\le J_i^{\pi^h}(g)\le U_i^h(g)               \tag{R4}
\]
at every completed history.

**Proof.** The baseline lower table is independent of the named upper-policy choice. At each
terminal it still satisfies \(L_i\le g_i\), and at each decision it still satisfies
\(L_i(g)\le Q_i[L_i](g,a)\) for every action. These are all lower conditions.

For an upper terminal below the cut, R3 uses \(B_i\), whose replacement certificate bounds the
same terminal cost. At any other terminal it uses \(U_i\). A terminal cannot be a strict ancestor
of another supplied history in a completed tree, so these exhaust terminal cases.

At a decision \(g\) in the replaced subtree, R1 selects \(\rho(g)\) and R3 uses \(B_i\) at \(g\)
and all its children. The replacement source supplies exactly
\(B_i(g)\ge Q_i[B_i](g,\rho(g))\). At a node neither above nor below the cut, every child of the
selected baseline action is also outside the affected ancestor chain and subtree. R3 is \(U_i\)
throughout that backup, so the baseline source supplies its inequality.

It remains to consider \(g\prec h\). Write \(\delta_i=B_i(h)-U_i(h)\). If the baseline action at
\(g\) differs from the action named by the path to \(h\), then \(w_i(g,h)=0\); none of the selected
action's children lies on that path, and both sides of the baseline upper inequality are unchanged.
Otherwise let \(o_*\) be the next observation on that path and \(g'=g\pi(g)o_*\). The only changed
child term in the selected backup is the \(o_*\) term. Whether \(g'=h\) or \(g'\prec h\), R3 and
\(w_i(h,h)=1\) give
\[
 Q_i[U_i^h](g,\pi(g))
 =Q_i[U_i](g,\pi(g))+p_i(o_*\mid g,\pi(g))w_i(g',h)\delta_i
 =Q_i[U_i](g,\pi(g))+w_i(g,h)\delta_i.                         \tag{R5}
\]
R3 adds the identical quantity to \(U_i(g)\). Therefore
\[
 U_i^h(g)-Q_i[U_i^h](g,\pi(g))
 =U_i(g)-Q_i[U_i](g,\pi(g))\ge0.                              \tag{R6}
\]
The argument uses linearity and nonnegative transition weights, not a sign assumption on
\(\delta_i\). Zero probabilities make both corrections zero. STOP has no continuation term and can
only occur in the divergence case. Signed costs occur equally in the old and new backups. Ordinary
backward induction now proves R4. \(\square\)

The proof includes a zero-horizon terminal tree, a root cut, a terminal cut, unreachable subtrees,
and non-topological storage because it depends only on history prefixes and finite depth, not array
order. At the root,
\[
 U_i^h(\varnothing)=U_i(\varnothing)+m_i^\pi(h)
 [B_i(h)-U_i(h)],                                             \tag{R7}
\]
where \(m_i^\pi(h)=w_i(\varnothing,h)\). For \(h=\varnothing\), this reads
\(B_i(\varnothing)\). R7 is a certificate upper bound. It is not an exact cost identity.

## 3. Root caps, allowances, and honest dispositions

Two requests are supported:

- **worst-model-expected-cost-cap:** an exact signed threshold \(C\);
- **worst-model-regret-cap:** an exact nonnegative threshold \(\Gamma\), paired with the unchanged
  full modelwise optimum lower table \(L_i\).

The submitted spliced certificates establish the cost cap exactly when
\[
 U_i^h(\varnothing)\le C\quad\text{for every }i,              \tag{R8}
\]
and establish the regret cap exactly when
\[
 U_i^h(\varnothing)-L_i(\varnothing)\le\Gamma
 \quad\text{for every }i.                                    \tag{R9}
\]
The subtraction remains paired within each model before taking a maximum.

Calling either result *preservation* additionally requires the submitted baseline evidence to
establish the same cap: respectively \(U_i(\varnothing)\le C\), or
\(U_i(\varnothing)-L_i(\varnothing)\le\Gamma\), for all members. If this premise fails, the result
is `baseline-preservation-premise-not-established`, even if the new evidence happens to pass.
When the baseline passes and the splice passes, the result is `preservation-certified`; when the
baseline passes but the splice does not, it is `preservation-not-established`.

For \(m_i=m_i^\pi(h)>0\), substituting R7 and rearranging gives the exact submitted-certificate
allowance
\[
 B_i(h)\le U_i(h)+\frac{C-U_i(\varnothing)}{m_i}              \tag{R10}
\]
for the cost cap, and
\[
 B_i(h)\le U_i(h)+
 \frac{L_i(\varnothing)+\Gamma-U_i(\varnothing)}{m_i}         \tag{R11}
\]
for the regret cap. These are equivalent to R8–R9 for the submitted tables, not necessarily to
actual feasibility when the tables are loose. If \(m_i=0\), R7 leaves the old root upper unchanged;
there is no division and no conditional interpretation. That member remains in the ex-ante cap.

A bound above a cap establishes only insufficiency. It does not prove that the named policy violates
the cap. The separate exact route checks terminal equality, every Bellman optimum equality, and
every named-policy evaluation equality. Only then does an exact value above the threshold receive
`supported-exact-violation`; an exact value at or below it receives
`supported-exact-satisfaction`. Invalid family, criterion, unit, threshold, event, policy, source,
or comparator input rejects as outside this operation. A valid nonempty family whose members all
give \(h\) zero mass still permits R3, but its observed-event conditional query is impossible.

## 4. Actual change is a separate identity

For one fixed member, R1 changes no prefix action before \(h\). Partition complete paths into those
that reach \(h\) and those that do not. On the latter, every action and cost agrees. On the former,
all prefix costs agree and the remaining policies are respectively \(\pi\) and \(\rho\). Taking
expectations yields the S17 specialization
\[
 J_i^{\pi^h}(\varnothing)-J_i^\pi(\varnothing)
 =m_i^\pi(h)[J_i^\rho(h)-J_i^\pi(h)].                         \tag{R12}
\]
This remains true at zero mass, for signed costs, at a root cut, at a terminal cut, and when STOP
makes the cut unreachable. The exact receiver checks both sides rather than trusting a submitted
delta.

The difference \(B_i(h)-U_i(h)\) must never replace the bracket in R12. From
\(J_i^\rho(h)\le B_i(h)\) and \(J_i^\pi(h)\le U_i(h)\), no ordering of the difference follows:
subtracting two upper bounds is not a bound on a difference. Therefore these conclusions remain
separate:

- actual non-worsening in every member, checked by R12 with exact values;
- non-worsening of the aggregate worst exact cost or regret;
- a tighter submitted certificate upper;
- preservation of a named cap by submitted evidence.

None implies all the others.

## 5. Exact fixed cases

The [checker](../verification/family_replanning/README.md) treats these authored cases as
conformance evidence, not discovered or preregistered data.

**R1 — conditional improvement, root deterioration.** Models A and B give \(h\) masses \(9/10\)
and \(1/10\). At \(h\), action `a` costs 0 and 10, while `b` costs 2 in both. The baseline root
costs are \((0,1)\); the splice gives \((9/5,1/5)\); modelwise optima are \((0,1/5)\). Complete
policy enumeration and independent paths show that `a` uniquely minimizes deterministic worst
root loss \(1\) and worst root regret \(4/5\), versus \(9/5\) for `b` under both criteria.
Conditionally, worst remaining loss improves \(10\to2\) and worst regret \(8\to2\). Nevertheless
the original root caps 1 and \(4/5\) both fail. The cost allowances are \((10/9,10)\), and the
regret allowances are \((8/9,10)\). No dynamic-consistency claim from PR8 is contradicted.

**R2 — genuine preserved improvement.** Both members reach a non-root cut with masses \(1/2\) and
\(1/3\). Signed root fees and terminal costs are used. The baseline root values are
\((3/2,-5/12)\); the shared replacement gives \((-1/2,-3/4)\). Every member improves, the worst
cost cap \(3/2\) and regret cap 2 are certified, every generated certificate passes the ordinary
consumer, and the PR8 named-family route returns worst upper \(-1/2\) and worst regret bound zero.

**R3 — certificate tightening is not actual improvement.** One-step costs are `a=0,b=1`. The
baseline `a` certificate has valid upper 100 and the replacement `b` certificate has upper 1. The
root splice validly tightens the reported upper by \(-99\), while exact evaluation shows actual cost
increases by 1. A submitted claim that the actual delta is \(-99\) rejects.

**R4 — failure to certify is not violation.** One unchanged action has true cost and regret zero.
An exact baseline plus a valid replacement upper 2 does not establish cost or regret cap 1. Exact
evaluation establishes satisfaction, not violation; replacing the loose table with the exact table
certifies preservation. Supplying upper 2 as the purported baseline also produces the distinct
`baseline-preservation-premise-not-established` disposition.

**R5 — conditional exclusion does not erase a root member.** Model A gives \(h\) mass zero and
cost 10 on `other`; B gives \(h\) mass one and replacement continuation cost 1. Conditioning at
\(h\) retains only B, while the root family still has worst cost 10. An all-zero event has a valid
zero-impact algebraic splice and an impossible conditional query. An empty original family rejects.

**R6 — complete binding.** Accepted controls bind the baseline prefix, entire replacement subtree,
all off-support actions, family order and identities, source policies, event, loss unit, criterion,
cap, threshold, path factors, and unchanged lower comparator. Tests reject altered prefix actions,
an outside-subtree change, a hidden-model-indexed continuation, an incomplete fallback policy,
wrong event/member/order/source/unit/criterion/cap, floats, forged masses, and a changed comparator.
An exact ordinary certificate for the target in R4 remains valid as an ordinary warrant but rejects
as false splice provenance.

**R7 — overlapping replacements.** In the root `STOP=2` versus `GO=0`, child `a=0,b=1` tree, the
root-only and child-only edits against `STOP/a` have changes \(-2\) and 0. Their sum is not the
`GO/b` final change \(-1\). The supported interface accepts one cut and rejects an overlapping cut
collection. Consecutive edits against their correct predecessors give \(-2,+1\) and telescope to
\(-1\).

**R8 — deeper exact controls.** A horizon-three, non-topologically stored tree includes signed
costs, early STOP, terminal costs, continuing actions, and different model supports. Independent
forward paths agree with the checked certificate roots for root, terminal, support-varying, and
deep cuts: respectively \((2,3)\), \((-37/12,113/90)\), \((-37/12,-7/90)\), and
\((25/6,41/30)\). At the support-varying cut the masses are \((0,2/3)\). A 1027-bit derived exact
fraction is accepted while Boolean/float proof values reject. Caller containers are detached.
With two units of replacement-source terminal slack, the unchanged terminal-cut policy retains exact
path values \((-37/12,113/90)\) while its valid constructed roots become
\((-13/12,143/90)\). A separate zero-horizon terminal root at \(-2\) certifies the signed cap
\(-2\).

Final receiver checks disable the splice and exact-evidence producers together with PR8, PR7,
transport-internal, and ordinary candidate producers. The receivers continue to accept retained
evidence and reject a forged factor.

## 6. Reference boundary and remaining limits

The [small exact reference](../verification/family_replanning/replanning.py) uses standard-library
`Fraction` arithmetic and imports the existing consumers unchanged. The producer constructs one
cut; the receiver reconstructs it independently, recomputes all modelwise path factors, checks both
source certificates, checks every lower/upper identity, invokes the ordinary target consumer, and
recomputes cap values and allowances. The exact-performance route separately checks three full
policy-evaluation tables and the common modelwise optimum.

The executable inherits PR8's maximum of four models and PR5's horizon-four, 64-node, four-action,
and four-outcome limits. These are implementation budgets, not restrictions on the finite theorem.
No multi-cut formula, randomized policy, policy optimizer, posterior over models, rectangularized
adversary, statistical coverage, empirical model validation, tail/dynamic risk criterion, causal
transport, Writ integration, or Decision Lab change is supplied. The fixed executions share schema,
arithmetic, and authorship; the forward paths are a separate calculation route, not formal theorem
verification. A mature ordinary-certificate soundness theorem remains a candidate for a separate
later Lean feasibility check, not work opened here.
