# Bellman: persistent model-family certificates and one implementable policy

**7 September 2026. Additive finite construction; no novelty claim.**

Base: main commit `9761cd0ce99be6fb6b2dcddc89951960a4a0df34`, the merge of PR7.
The reviewed PR7 head `5c567646e0dec648bfdc9302025b495e8afaeb6e` is an ancestor of that
commit and its file tree is unchanged by the merge. PR7, its historical base statements, all prior
mathematics, and all recorded evidence remain unchanged.

This construction answers one bounded question: what can be certified about one accessible plan
when several fully specified models remain possible, without averaging them, choosing from a hidden
model label, or changing model rows between dates? It builds above the unchanged ordinary
sequential certificates and uses PR7 accumulation only inside an exact model and one exact policy.

## 1. Objects, assumptions, and authority

Let
\(\mathcal F=(F_1,\ldots,F_m)\), \(1\le m\le4\), be an ordered family of finite completed
observable-history subjects in the sense of the [sequential certificate
construction](BELLMAN_SEQUENTIAL_CERTIFICATE_COMPOSITION.md). Members have the same ordered
histories, action and outcome labels, terminal/decision structure, horizon, loss unit, and
expected-additive-cost criterion. Their signed rational costs, rational transition probabilities,
support, names, and declared model premises may differ. Equality of this skeleton is a checked
representation condition; it does not establish the empirical truth of any model premise.

The members are alternative whole-episode models. One \(F_i\) remains fixed throughout an episode.
The index \(i\) is not an observation. A deterministic policy \(\pi\) is one total table on the
common history skeleton, including actions at every union-support completion. Its action at a
history may depend on that declared observed history, but not on an unobserved model identity,
calculation label, realized cost not declared observable, or future observation.

For member \(i\), let \(J_i^\pi(h)\) be the exact expected remaining cost of \(\pi\), and
\[
 V_i(h)=\min_{\rho\in\Pi}J_i^\rho(h),
\]
where \(\Pi\) is the common class of total deterministic history policies. This modelwise optimum is
a comparator. It does not make \(i\) available to the acting policy. No prior or probability over
members, independence, causal validity, statistical coverage, randomization, minimax preference, or
authority to act is inferred.

A family identity binds the complete ordered members. Model identities and policy identities are
nonempty value bindings, not cryptographic signatures or authorship claims. Omitting, duplicating,
renaming, reordering, or substituting a requested member changes the request.

## 2. One named policy across the family

The request independently supplies the complete family, one legal policy \(\pi\), the criterion, and
one source group for every member in family order. Every source in group \(i\) must be an ordinary
certificate for exactly \(F_i,\pi\). The receiver validates every source with the unchanged ordinary
consumer. It then uses PR7's max-lower/min-upper operation only within that group. Invalid, missing,
duplicate, mixed-model, or wrong-policy input rejects the entire collection; no difficult member is
silently removed.

Suppose the resulting checked member tables satisfy, at every completed history,
\[
 L_i(h)\le V_i(h)\le J_i^\pi(h)\le U_i(h).                 \tag{P1}
\]
The returned root records preserve the four-tuple
\((i,L_i,J_i^\pi\hbox{-upper},U_i-L_i)\) before any family aggregation. The aggregate claims are
\[
 \max_i J_i^\pi(\varnothing)\le\max_i U_i(\varnothing),   \tag{P2}
\]
\[
 \max_i\{J_i^\pi(\varnothing)-V_i(\varnothing)\}
 \le\max_i\{U_i(\varnothing)-L_i(\varnothing)\}.          \tag{P3}
\]

**Proof.** P2 follows by taking the maximum of the memberwise upper inequalities in P1. For every
fixed \(i\), subtract the lower inequality from the upper inequality to get
\(J_i^\pi-V_i\le U_i-L_i\); taking the maximum proves P3. The subtraction must occur while the two
quantities retain the same model identity. In general
\(\max_iJ_i^\pi-\max_iV_i\) is not an upper bound on the maximum paired regret. No bound here is
claimed attained. \(\pi\)'s uniform near-optimality also does not prove that it minimizes worst loss
or worst regret over policies. \(\square\)

Within one fixed \(F_i,\pi\), adding another valid PR7 source can only increase the combined lower
table and decrease the combined upper table. Its member gap therefore cannot increase, and so the
family maximum cannot increase when only a source is added to an existing member group. Adding a
new possible model is different: it enlarges the outer maximum and may worsen either aggregate.
These deterministic extrema do not compose data-dependent confidence statements without their own
simultaneous-coverage argument.

## 3. Exact finite policy choice

A model family alone supplies no preference among decision rules. A choice request therefore names
one of three distinct claims:

1. all common modelwise-optimal policies in the supplied catalogue;
2. all policies attaining minimum worst-model expected loss;
3. all policies attaining minimum worst-model regret against the exact modelwise comparators.

For a supplied ordered catalogue \(\Pi_0=(\pi_1,\ldots,\pi_n)\), construct
\[
 C_{ij}=J_i^{\pi_j}(\varnothing),\qquad
 W_j=\max_i C_{ij},\qquad
 R_j=\max_i(C_{ij}-V_i).                                  \tag{P4}
\]
Then
\[
 W_*=\min_jW_j,\qquad R_*=\min_jR_j.                      \tag{P5}
\]
All minimizing ties are returned. A policy is common modelwise optimal exactly when
\(C_{ij}=V_i\) for every member.

The producer supplies one ordinary certificate for every matrix cell. The receiver checks terminal
equalities, every Bellman minimum equality for the lower table, and every selected-policy evaluation
equality for the upper table. Backward induction therefore establishes that the lower roots are the
exact \(V_i\) and the upper roots are the exact \(C_{ij}\), rather than trusting an optimizer name,
`complete` flag, supplied count, or loose lower bound.

**Exact-choice theorem.** If those equalities pass, P4 is the exact matrix and modelwise comparator
vector for the supplied catalogue. Finite maxima and minima then prove the returned \(W_j,R_j\),
\(W_*,R_*\), common optimizers, and complete tie sets. If the receiver also establishes that the
catalogue equals the cartesian product of every action menu at every decision history, these are
full deterministic-class results. If the request explicitly names only a proper candidate subset,
the same calculation proves only best-in-that-subset results. \(\square\)

The reference independently constructs the cartesian policy keys and compares them with the
submitted columns. It accepts at most 64 complete deterministic policies. If full coverage is
larger, that stronger operation returns **unfinished**; a separately valid named-policy family
bound remains available. Duplicate semantic columns reject even under different labels.

This is optimization over deterministic policies only. In the two-model rows \((0,1)\) and
\((1,0)\), every common deterministic action has worst loss one, while a separately specified
private half-half mixture has worst expected loss \(1/2\). The present reference neither accepts
that randomization class nor calls its deterministic result unrestricted.

## 4. Persistence, information, and rectangularization

Every cell \(C_{ij}\) follows one \(F_i\) from root to termination. Maximizing a separate cost or
transition row at each date generally forms trajectories absent from every supplied member. For
models with forced two-date costs \((0,1)\) and \((1,0)\), each whole-episode value is one; separate
datewise maximization gives two. The latter is an enlarged rectangularized uncertainty model, not
the requested family's value.

Iyengar's [publisher abstract](https://pubsonline.informs.org/doi/abs/10.1287/moor.1040.0129)
explicitly places robust dynamic-programming conclusions under a rectangularity property. That is
literature context for why rowwise pasting needs an assumption; this construction neither invokes
the full paper as a proof nor supplies rectangularity. The direct finite evaluations above carry
the present result.

Observed information is different from a hidden model key. If an accessible observation has
different model-specific likelihoods, one shared policy may select different later actions because
the observed histories differ. Every union-support fallback remains total and checked. PR7's policy
switching result also remains within one exact subject. Chang's [2021 policy-switching
paper](https://arxiv.org/abs/2112.02177) concerns policy updates within an infinite-horizon discounted
MDP; it supplies no license to choose a different action from an unobserved member identity here.

## 5. Support-filtered continuation

Fix one total prefix policy \(\sigma\), one observed history \(h\), and one total accessible
continuation policy \(\pi\). For each member, recompute the exact prefix mass
\[
 m_i^\sigma(h)=\prod_{(a,o)\text{ along }h}p_i(o\mid h_{\rm before},a), \tag{P6}
\]
provided \(\sigma\) selects every indicated action; otherwise the mass is zero. Define the retained
index set \(I_h=\{i:m_i^\sigma(h)>0\}\). Zero-mass members are preserved in an explicit exclusion
record, not assigned a posterior weight and not treated as conditional models.

For each \(i\in I_h\), the receiver checks an ordinary certificate for exactly \(F_i,\pi\), invokes
the inherited positive-prefix receiver, and returns
\[
 L_i(h)\le V_i(h)\le J_i^\pi(h)\le U_i(h).                \tag{P7}
\]

**Continuation theorem.** Positive P6 makes the completed node an actual conditional event under
the fixed member and prefix policy. The finite policy and optimum recurrences from that node exclude
already-paid prefix costs, so the unchanged ordinary backward-induction proof gives P7. Applying it
separately to every \(i\in I_h\) proves the returned unweighted conditional family records. No
conclusion is produced for \(i\notin I_h\). \(\square\)

An empty original family is invalid input. A valid nonempty family with \(I_h=\varnothing\) is an
event impossible under every supplied member, so normalized conditioning is undefined. A resource
limit or unexecuted check is **unfinished**, not either of those facts. Positive likelihood alone
supplies no statistical coverage and no Bayesian weights.

Continuation recomputation is a new query binding the original family, prefix policy, event,
continuation policy, criterion, and retained/excluded scope. No theorem here says a root minimax
policy is dynamically consistent, or that conditional replanning preserves its prior root
guarantee. Such a claim would require a separately specified preference and composition argument.

## 6. Fixed exact cases

The [fixed checker](../verification/persistent_model_families/README.md) verifies the following
authored cases. They are conformance evidence, not preregistered discovery data.

- **F1 — paired aggregation.** Rows \((2,0)\), \((100,100)\), candidate `a`: candidate values
  \((2,100)\), optima \((0,100)\), actual worst regret 2. The invalid cross-model subtraction is
  \(100-100=0\), and a forged zero bound rejects.
- **F2 — criterion identity.** Rows \((0,2)\), \((10,9)\): worst losses \((10,9)\), worst regrets
  \((1,2)\). Minimum worst loss selects `b`; minimum worst regret selects `a`. Relabelling rejects.
- **F3 — hidden oracle.** Rows \((0,1)\), \((1,0)\): no common modelwise optimizer; each common
  deterministic action has worst loss and regret 1. A model-indexed policy list rejects. The
  half-half value \(1/2\) is recorded only as a separate randomization-class distinction.
- **F4 — genuine observations.** Model A emits `L` surely and B emits `R` surely. The shared total
  rule `a` after `L`, `b` after `R` costs zero under both. At `L`, A is retained with mass one and B
  is explicitly excluded with mass zero; both off-support fallbacks remain defined.
- **F5 — fixed model between dates.** Forced rows \((0,1)\), \((1,0)\) have whole-episode worst cost
  1. A forged datewise value 2 rejects as the wrong persistent-family calculation.
- **F6 — coverage.** Costs \((0,1,2)\): the candidate subset `{b,c}` has subset optimum 1. It cannot
  certify the full optimum, which is 0 at `a`. A missing column, duplicate semantic column, and false
  policy count reject.
- **F7 — within-model accumulation.** Complementary loose same-policy certificates combine to exact
  member gaps 2 and 0 before the family maximum gives 2. A certificate forged from favorable
  coordinates of different models and a mismatched certificate/member pair reject.

**F8 — nontrivial sequential family.** Both members use node storage order root, `R`, `L`, `M`.
The root may stop early or pay a signed probe cost. The probe emits three observations; A supports
`L,M`, B supports `M,R`. At `M` their optimal actions compete. In the table, a policy code lists
root/`R`/`L`/`M`; \(V_A=-1\), \(V_B=-1/4\).

| Policies | Code | \(C_A\) | \(C_B\) | worst loss | worst regret |
|---|---|---:|---:|---:|---:|
| p00–p07 | stop / every `x,y` completion | 2 | 1 | 2 | 3 |
| p08 | probe/x/x/x | 0 | 3/4 | 3/4 | 1 |
| p09 | probe/x/x/y | -1 | 7/4 | 7/4 | 2 |
| p10 | probe/x/y/x | 1 | 3/4 | 1 | 2 |
| p11 | probe/x/y/y | 0 | 7/4 | 7/4 | 2 |
| p12 | probe/y/x/x | 0 | -1/4 | 0 | 1 |
| p13 | probe/y/x/y | -1 | 3/4 | 3/4 | 1 |
| p14 | probe/y/y/x | 1 | -1/4 | 1 | 2 |
| p15 | probe/y/y/y | 0 | 3/4 | 3/4 | 1 |

Separate forward path sums compute all 16 columns. Minimum worst loss uniquely selects p12. Minimum
worst regret is 1 with ties p08, p12, p13, p15. There is no common modelwise optimizer. At prefix
`L`, only A survives with mass \(1/2\); at `M`, both survive with mass \(1/2\). Choosing root STOP
before querying `L` makes the event impossible under the whole supplied family. These checks make no
dynamic-consistency claim.

Additional controls cover wrong model identity, changed unit or criterion, missing union-support
actions, Boolean and float proof values, 1026-bit derived rationals, caller-container mutation,
zero horizon, singleton policy classes, one-model reduction to the inherited answer, and a
256-policy full-coverage refusal that leaves the named-policy bound available. Receiving is rerun
with the new producers, PR7 producer, and inherited ordinary producer disabled.

## 7. Reference, evidence, and limits

The [small exact reference](../verification/persistent_model_families/families.py) imports PR7 and the
ordinary PR5/PR6 consumers unchanged. Producers build within-model extrema, exact cell certificates,
and support partitions. Receivers recheck complete requests, ordinary inequalities, exact matrix
equalities, cartesian coverage, pairings, extrema, ties, masses, and exclusions without invoking a
candidate producer. The independent forward oracle uses complete paths rather than Bellman backups.
All paths share Python `Fraction` arithmetic and one authorship context; separate function names are
not formal verification or independent authorship.

Reference budgets are four models and 64 policies for a full-class claim, plus the inherited
horizon, node, menu, and exact model-coefficient limits. These are implementation budgets, not
theory restrictions. There is no optimizer for larger families, robust Bellman recursion, Bayesian
learner, randomized planner, new language, schema platform, or Writ/Decision Lab integration.

The fixed proofs and executions establish conditional finite mathematics. They do not establish the
models' empirical premises, statistical coverage, causal meaning, tail or dynamic risk, authority to
act, formal theorem-library verification, or computational advantage. Persistent uncertainty,
statistical learning, structural transport, richer criteria, and later narrowly scoped formalization
remain open without reopening KL5/KL6 or any closed experiment.
