# Bellman: certificate accumulation and policy selection

7 September 2026. Additive finite construction; no novelty claim.

Base: reviewed PR6 head `cd649db893c70bbce4891c8f526a27aaf1bcda1b`. PR6 was open at branch creation, so this work is a dependent PR targeting its branch, not a claim that PR6 is in main. PR6 and all historical mathematical sources/results are preserved unchanged.

## 1. Objects, authority, and review disposition

Use the finite completed observable-history subject F and expected additive cost of [PR5](BELLMAN_SEQUENTIAL_CERTIFICATE_COMPOSITION.md). Signed rational costs, normalized nonnegative transitions, STOP with no continuation, terminal costs, ordered histories/menus, horizon, loss unit, accessible information and total deterministic policies have exactly their existing meanings. Every completed decision node, including probability-zero nodes, must have a legal action.

The supplied PR6 review reports no false core theorem or incorrectly accepted supported certificate. We independently accept the max-lower/min-upper proposal with the proofs below. Different-policy minimum uppers require a new accessible selector. Actual improvement with loose upper bounds is rejected by the mandatory counterexample. PR6's conservative round trip is not a correctness defect.

The review reports 16 committed transport groups and 12 audit plus four proposed-extension groups under Python 3.13.5; these remain attributed reviewer evidence, not fresh executions here. Our exact cases and cloud preservation runs are separately recorded. No byte-identical replay of the attached reviewer script or unavailable harness is claimed.

The [transport construction](BELLMAN_CERTIFICATE_TRANSPORT_AND_REVALIDATION.md), its unchanged implementation, and the [joint-law revision](BELLMAN_NEXT_MATHEMATICAL_BUILDOUT_REVISED.md) remain governing mathematical inputs. The latter's original/outer, attainment/bound, and impossible-conditioning/empty-model distinctions are retained. Combining numerical tables is not joining distinct original model sets or proving their compatibility.

## 2. Complete contract and separate warrants

A source is an immutable pair (identity, ordinary certificate). The identity is a nonempty string bound to the full certificate, not a cryptographic signature or an assertion of independently authored evidence. A request contains the independently intended exact subject F, an ordered nonempty finite source collection, a criterion, and one of two operations:

- **same-policy:** additionally name one intended total policy pi; every source must certify that exact F,pi;
- **selection:** sources share exact F but may name different total policies; the operation constructs a new total policy.

Full subject equality includes costs, transitions, support completions, node/menu order, horizon, unit and premise labels. Matching root values or display names does not suffice. Semantic observability/control/loss assertions remain supplied premises; text equality cannot validate the world. The criterion is fixed to expected additive total cost, not tail risk or a robust or statistical criterion.

The implementation accepts at most 16 sources. Empty, duplicate-identifier, invalid, incomplete, mixed-subject, or wrong-policy collections reject in their entirety. Nothing is silently filtered. Resource refusal is unsupported/unfinished, not incompatibility. Distinct identities carrying identical valid certificates remain distinct warrant records but cannot numerically improve bounds twice.

Evidence retains the entire request, a new ordinary certificate, and (for selection) one source identifier per decision history. The receiver independently receives the expected request and intended output policy. It validates all source certificates with the unchanged PR5 consumer, validates the new certificate with that consumer, checks exact request equality, and verifies the claimed extrema and selector. A valid ordinary certificate with a false derivation fails the combination warrant. Omitting or renaming a requested source fails even when numbers happen to be unchanged.

These are separate conclusions: ordinary output validity; same-policy combination; new-policy selection; and checked exact-source-value dominance. No identity label substitutes for mathematical checks or authenticates external provenance. Nested historical transport warrants can remain archived beside the ordinary certificates they establish; this small operation does not invent a derivation graph.

## 3. Same-policy theorem

Suppose each C_i=(F,pi,L_i,U_i) passes S3–S4. Write
Q[w](h,a)=c(h,a)+sum_o p(o|h,a)w(hao), with an empty sum for STOP.
Set
\[
 L_*(h)=\max_i L_i(h),\qquad U_*(h)=\min_i U_i(h). \tag{A1}
\]

At terminals each L_i<=g<=U_i, hence L_*<=g<=U_*.
At a decision choose an index i attaining the finite maximum L_i(h).
For EVERY action a, monotonicity of Q gives
\[
 L_*(h)=L_i(h)\le Q[L_i](h,a)\le Q[L_*](h,a). \tag{A2}
\]
Choose j attaining the minimum U_j(h). Because the policy is identical,
\[
 U_*(h)=U_j(h)\ge Q[U_j](h,\pi(h))\ge Q[U_*](h,\pi(h)). \tag{A3}
\]
Thus complete nodewise S3–S4 hold, including STOP, zero probabilities, signed costs and terminal-only trees. Backward induction yields
L_*<=V_F<=J_F(pi)<=U_* at every completed node. The root regret is at most U_*-L_*.

For each i, U_*<=U_i and L_*>=L_i, so the combined gap is nonnegative and no greater than any input gap. Adding a valid same-subject/same-policy source can only increase the lower and decrease the upper table. Numerical table accumulation is associative, commutative and idempotent because finite scalar max and min have those properties at each coordinate. Every intermediate table remains a valid certificate by A2–A3.

These are table laws, not erasure of the retained sources, their identities or their premises. The executable request conservatively binds collection order, so permuted requests require their own matching warrant even though their tables agree. Grouping may use a checked intermediate certificate while retaining its original derivation externally; it does not prove that its leaf provenance disappeared.

No statistical independence is required to take extrema of deterministic valid bounds on one identical quantity. This does not license multiplying evidence, pooling model uncertainty, or intersecting individually probabilistic confidence statements. Joint statistical validity would need a simultaneous-coverage argument. None is supplied or assumed by this arithmetic operation.

## 4. Different policies: explicit selection theorem

For certificates (F,pi_i,L_i,U_i), A2 still proves the lower maximum is a subsolution for V_F. Define U_* by A1. At each observable decision history choose j(h) minimizing U_i(h), breaking ties by lexicographically smallest source identity, and let
\[
 \pi_{\rm switch}(h)=\pi_{j(h)}(h). \tag{A4}
\]
This rule uses only retained fixed tables and observed history. It includes all zero-probability completion nodes and is a legal total policy. At every decision,
\[
 Q[U_*](h,\pi_{\rm switch}(h))
 \le Q[U_j](h,\pi_j(h))
 \le U_j(h)=U_*(h). \tag{A5}
\]
Terminal bounds are unchanged. S3–S4 and backward induction now give
\[
 L_*\le V_F\le J_F(\pi_{\rm switch})\le U_*=\min_i U_i. \tag{A6}
\]
The new root gap is no greater than each input's certified root gap, but concerns the new policy. Attaching this upper table to an arbitrary unchanged source policy is invalid.

The selector's source identity, tie choice, selected action, node coverage and intended output policy are all checked. It cannot depend on a hidden model label or an unprovided observation. Deterministic identity-based tie breaking is independent of input order; no uniqueness of an optimal policy is asserted.

**Stronger sufficient premise.** If every U_i equals its actual policy value at every node, A6 gives
J_F(pi_switch)(h)<=min_i J_F(pi_i)(h).
The reference offers an additional receiver that verifies terminal equality U_i=g and each policy evaluation equality U_i(h)=Q[U_i](h,pi_i(h)). Backward induction uniquely identifies these tables as J_F(pi_i), proving the premise. It never infers equality from upper-bound validity or a solver label. Exact upper values do not force the selected policy's value to equal their minimum: it may be strictly better.

**Literature context.** [Chang (2021), §II-A](https://arxiv.org/html/2112.02177) describes switching based on exact policy values for infinite-horizon discounted rewards. That primary text was retrieved. It supplies context, not automatic authority for loose finite cost bounds; A2–A6 are derived directly here. The supplied [Chang, Givan and Chong (2004) DOI](https://doi.org/10.1023/B:DISC.0000028199.78776.c4) could not be retrieved through the available browser. No uninspected theorem detail is attributed to it.

## 5. Restored subjects and transport algebra

Let G have immediate costs (a,b)=(0,1), policy a, certificate [0,0].
Let F have (2,1). Unchanged PR6 transport gives [0,2] on F.
Transport back to the exact original G retains [0,2], whereas direct G-to-G transport retains [0,0]. Actual restored-model regret is zero. This is valid one-sided anchor retention, not uncertainty growth or actual suboptimality.

After checking both the returned certificate and the retained original on exactly G,a, A1 gives [0,0]. Both source identities and their histories remain retained. A different target, cost, premise or unit prevents using the old warrant unchanged. Evidence from different models needs target revalidation first, or remains distinct alternatives.

Optional comparison follows from monotonicity: for a fixed final target and policy, its lower-envelope operator is increasing in its lower anchor, by induction in T1–T2; its upper-envelope operator is increasing in its upper anchor by the same induction. Every intermediate transport lowers its lower anchor and raises its upper anchor. Therefore direct transport from the original anchors has lower at least the via-intermediate lower and upper at most the via-intermediate upper. Repeating proves this for any finite valid chain with a common skeleton and fixed final policy. This is no full path-independence or arbitrary commutation claim. The round trip explicitly disproves path independence.

## 6. Exact worked cases

**Complementary same-policy evidence.** In PR5's two-step tree root STOP=3/4 and GO=1/8, L/R equiprobable; child costs L:(0,1/2), R:(1,1/4). Policy GO/b/a has optimum table V=(1/4,0,1/4) and policy table J=(7/8,1/2,1). Sources (V,J+1) and (V-1,J) are locally valid. On continuing normalized rows, shifting every child by one shifts the backup by one; on STOP the shifted lower/upper inequalities remain valid. Each root gap is 13/8. A1 returns (V,J), gap 5/8. Separate full-path sums and all eight policies establish those exact values; fusion alone does not establish exactness.

**Different-policy control.** Root GO=0, L/R equiprobable; losses L:(a=0,b=2), R:(a=2,b=0). Policies a/a and b/b each cost one and have exact upper tables (1,0,2) and (1,2,0). Minimum (1,0,0) fails the upper inequality at R if assigned to a/a. The explicit selector chooses a at L, b at R, with true cost zero. Its certified root upper remains one; this is a bound, not attained cost.

**Loose upper anti-overclaim.** One-step a=0,b=1. Source a has valid upper 2; source b has exact upper 1. The selector chooses b, costs one, and is worse than a's actual zero. A6 survives; actual dominance fails, and the exact-value receiver rejects the loose premise.

**Different models.** Costs (0,1) versus (1,0) give respective optimal zero costs but common deterministic policy cost vectors (0,1) and (1,0). No common zero-cost policy exists. Mixed-subject fusion and model-keyed selectors are rejected.

Additional fixed controls cover false extrema despite standalone validity; missing/duplicate/renamed sources; invalid source lower bounds and missing coordinates; wrong policy/criterion/unit; reversed directions; float/Boolean proof inputs; 1025-bit derived Fractions; caller-owned containers; terminal-only/singleton/tied selectors; and non-topological storage with a zero-support branch. Conditional conclusions reuse PR6's positive-prefix query: algebraic zero-mass node values never become posteriors. An impossible prefix is not an empty model.

## 7. Execution and remaining boundaries

The [small reference](../verification/certificate_accumulation/README.md) imports PR5 and PR6 unchanged. Input coefficient limits remain separate from arbitrary-size exact Fraction proof coordinates. Frozen dataclasses detach source lists, selector rows and inherited policies/tables from caller mutation. This is ordinary immutable value semantics, not interpreter-tampering security.

Producers form extrema and a selector; receivers check all sources, exact extrema by inequalities plus attainment, and invoke the unchanged ordinary checker. Both candidate producers, the internal producer, PR5's producer and PR6 transport are disabled in receiver tests. The forward path oracle is separately coded and enumerates only tiny fixed policy lists. Shared Fraction arithmetic and authorship remain limitations.

Normal and -O runs, actual timing, source SHA-256 identities, pinned commit, and the full existing transport/preservation execution are recorded in one compact JSON. Historical results are not rewritten to describe this run. No model-grid experiment, environment installation, recovery archive, local repository checkout or Writ/Decision Lab change is required.

Analytical proofs and fixed executions are not formal verification, empirical premise validation, statistical coverage, global tightness, or computational advantage. At most 16 sources and the inherited horizon-four/node/menu limits define the small implementation, not Bellman's ceiling. Wider model uncertainty, dependence, causal identification, statistical coverage, risk and structural lifting remain active mathematical areas and are not further tasks in this PR.
