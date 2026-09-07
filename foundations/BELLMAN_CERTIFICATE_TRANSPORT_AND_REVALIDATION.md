# Bellman: certificate transport and revalidation

**7 September 2026. Additive mathematical construction, proofs, and bounded exact reference.**

Base: main commit `e4139b6c68f0386b62bf6332b12d2f654c1d4faf`, the merge of PR5 reviewed head `a998b916a5cdb27cd9263c5f9e1520479a396a18`. The trees agree; there is no intervening file change. The reviewed reference and checks retain Git blobs `c1dc8352a6aeac5a03a1c2a4ee3265d84d2954b7` and `599c53cfa0aebf862e4064e1cfc75db2307bc2a5`. Earlier mathematical statements and verification records remain unchanged.

This answers a bounded question: after explicitly changing a supplied model or policy, what evidence warrants a new sequential decision guarantee? The answer is a new certificate for the new subject, constructed from the old tables and independently checked. Established finite backward induction suffices; novelty is not required.

## 1. Review assessment and retained premises

The supplied PR5 review reports no reproduced correctness defect in the declared finite profile. Its proposed envelope construction is independently derived below, including the correction identities and restricted extremality. The candidate-only comparison and overlapping-replan examples identify invalid compositions; they do not refute PR5's uniform-comparator theorem or single-replacement identity. We accept those mathematical objections to the invalid joins and retain the original theorems with their premises.

The supplied review evidence records a separate Python 3.13.5 audit, 17 committed groups, ten audit groups, and three extension groups. Those are reviewer-reported runs, not this module's execution. The new fixed checks independently evaluate the decisive examples and use separate forward path sums and full tiny policy enumeration. We do not describe new code as a byte-identical replay of the attached reviewer script. Current execution, source identities, counts, and limitations are in the [compact verification record](../verification/certificate_transport/results.json).

Inputs are the [sequential construction](BELLMAN_SEQUENTIAL_CERTIFICATE_COMPOSITION.md), especially S3–S12 and S14–S17; [initial build-out](BELLMAN_NEXT_MATHEMATICAL_BUILDOUT.md), especially B3 and §§7–9; [joint-law revision](BELLMAN_NEXT_MATHEMATICAL_BUILDOUT_REVISED.md); and the current [PR4 exact-reference rules](../verification/pr4_repair/README.md). These are mathematical inputs, not ongoing instructions to repeat historical experiments or recovery work.

## 2. Exact subject and admissible transport

Let G and F be finite completed observable-history trees. The first executable profile requires the SAME:

- ordered histories, rooted at the empty history;
- action labels and ordered menus at every history;
- outcome labels and ordered menus, including zero-probability outcomes;
- terminal versus decision nodes, STOP versus continuing actions, and child links;
- horizon, accessible-history interpretation, expected additive total-cost criterion, and loss unit.

Signed rational action costs, terminal costs, and normalized transition probabilities may change. Subject names and supplied modeling-premise labels may change only as part of the explicitly supplied new subject. Matching labels is not empirical proof of observability, causal control, or valid preferences. No hidden model label, future observation, or additional information becomes accessible through transport.

A continuing action at h pays c_F(h,a), emits o with p_F(o|h,a), and reaches hao. STOP pays its cost and ends, with no continuation term. A terminal node pays g_F(h) once. The target policy pi' is a complete deterministic legal history table, including fallbacks at every completed zero-support history. The source policy pi is also total.

This profile validates an explicit ordered identity correspondence: each supplied source history is paired with exactly the same target history. It also validates the entire skeleton, not just that list or a name. Reordering, different observation keys, changed action menus, horizon, STOP structure, loss units, information access, or criterion is unsupported. Such changes would need a separately justified map of policies, histories, cost semantics, and comparator coverage. An arbitrary representation mapper is not implemented.

**Transport request.** Bind the independently supplied G, pi, an old checked certificate C_G=(G,pi,L,U), F, pi', the exact correspondence, and requested guarantee. Validate all objects and check C_G against G and pi before any conclusion. An old certificate remains a theorem about its old subject; it is not edited or automatically rebound.

**Evidence.** The producer supplies a new ordinary certificate C_F=(F,pi',L',U') and correction tables alpha,beta, together with the bound request. The ordinary target receiver checks C_F against independently supplied F and pi' using PR5's unchanged consumer. The transport receiver additionally validates the old warrant, exact request/correspondence, correction identities, and envelope equations. Thus:

1. target certification warrants a bound about F and pi';
2. transport certification also warrants the claimed anchored derivation from C_G.

A valid target certificate can fail the second test without losing its first warrant. A source certificate that does not check supplies neither transport provenance nor a source guarantee.

## 3. Construction

For any table w define
\[
 Q_F[w](h,a)=c_F(h,a)+P_{F,a}w,\qquad
 P_{F,a}w=\sum_o p_F(o|h,a)w(hao),
\]
where P is zero for STOP.

Traverse by decreasing history depth, independently of storage order. At terminal h set
\[
 L'(h)=\min\{L(h),g_F(h)\},\qquad
 U'(h)=\max\{U(h),g_F(h)\}.                 \tag{T1}
\]
At decision h set
\[
 L'(h)=\min\{L(h),\min_{a\in A(h)}Q_F[L'](h,a)\},
\quad
 U'(h)=\max\{U(h),Q_F[U'](h,\pi'(h))\}.    \tag{T2}
\]
All minima/maxima are attained over finite nonempty menus. Rational arithmetic terminates on a finite tree. Signed costs require no positivity assumption: only transition weights must be nonnegative and normalized. Zero-weight children are still supplied and checked; they need no posterior for algebraic completion.

The lower scan includes EVERY target action. The upper scan includes the target policy action. Missing competitors cannot be repaired by upper-policy validity. At horizon zero only (T1) applies. Ties are retained; a singleton menu is forced availability, not strict superiority over a competitor.

## 4. Soundness and regret proof

T1 immediately gives L'<=g_F<=U'. T2 gives, for every action,
\[
 L'(h)\le Q_F[L'](h,a),\qquad
 U'(h)\ge Q_F[U'](h,\pi'(h)).              \tag{T3}
\]
These are exactly S3–S4 for the new subject. Induct from terminals. Nonnegative transition weights preserve child inequalities; hence L'<=V_F under every action minimum, and J_F^{pi'}<=U' under policy evaluation. The finite deterministic optimum is attained and belongs to the complete target policy class, so at every completed node
\[
 L'\le V_F\le J_F^{\pi'}\le U'.             \tag{T4}
\]
At the root,
\[
 0\le J_F(\pi')-V_F\le U'(\varnothing)-L'(\varnothing). \tag{T5}
\]
The right side is a bound, not a claimed attained regret. Only matching validated lower and upper values certify optimality of that named policy. Neither an approximate value table nor a source optimizer alone certifies the new executed policy.

This proof does not require the source certificate to establish target inequalities: T1–T2 already force them for arbitrary finite anchor tables. The old consumer check is nevertheless necessary for the advertised *transport from a checked source*. The implementation maintains this distinction explicitly.

## 5. Correction form and extremality

Put L'=L-alpha and U'=U+beta. At terminals,
\[
 \alpha(h)=\max(0,L(h)-g_F(h)),\quad
 \beta(h)=\max(0,g_F(h)-U(h)).              \tag{T6}
\]
At decisions,
\[
 \alpha(h)=\max\left(0,\max_a\{L(h)-Q_F[L](h,a)+P_{F,a}\alpha\}\right), \tag{T7}
\]
\[
 \beta(h)=\max\left(0,Q_F[U](h,\pi'(h))-U(h)+P_{F,\pi'(h)}\beta\right). \tag{T8}
\]
To verify equivalence independently, use linearity
Q_F[L-alpha]=Q_F[L]-P alpha and Q_F[U+beta]=Q_F[U]+P beta.
Subtract a minimum from L and a maximum from U. T1 gives T6; T2 gives T7–T8. STOP has P=0, so no fictitious future correction is added. The producer uses T6–T8; the receiver checks T1–T2 against the submitted new tables and checks their exact relation to alpha,beta. It does not invoke the producer.

**Restricted extremality theorem.** Among all target subsolutions x satisfying terminal x<=g_F, x(h)<=Q_F[x](h,a) for every a, and x<=L pointwise, L' is the greatest pointwise. Among target pi' supersolutions y satisfying terminal y>=g_F, y(h)>=Q_F[y](h,pi'(h)), and y>=U pointwise, U' is the least pointwise.

**Proof.** Terminal x<=min(L,g_F)=L'. If x<=L' at children, monotonicity gives
x(h)<=min(L(h),min_a Q_F[x](h,a))<=min(L(h),min_a Q_F[L'](h,a))=L'(h).
Induct. For y, terminal y>=max(U,g_F)=U'. If y>=U' at children, then
y(h)>=max(U(h),Q_F[y](h,pi'(h)))>=max(U(h),Q_F[U'](h,pi'(h)))=U'(h).
Induct. T3 shows both envelopes themselves are feasible, completing the extremality claim.

Equivalently, alpha and beta are the least nonnegative corrections in these pointwise anchored classes. The pair also minimizes the root gap within these two separate anchored classes. It is NOT a globally smallest regret bound: removing anchors can tighten either side. It proves no representation compression, reusable summary sufficiency, or computational speedup. Full node/action scans are allowed. The small implementation uses depth sorting and exact arithmetic; it makes no bit-complexity or large-instance performance claim.

If model and policy are unchanged, the old certificate already satisfies S3–S4. Induction in T1–T2 returns exactly L,U and zero corrections, including slack source tables. If only the policy changes, the lower table remains unchanged; the anchored upper table may retain slack from the old policy.

## 6. Uniform comparison is a separate route

If on one common total policy class
|J_F(rho)-J_G(rho)|<=e_* for EVERY comparator rho, and
|J_F(pi')-J_G(pi')|<=e_pi, then a checked nominal certificate for pi' yields
\[
 J_F(\pi')-V_F\le (U_G-L_G)+e_\pi+e_*.     \tag{T9}
\]
Taking infima in the uniform inequality gives V_F>=V_G-e_*; the candidate inequality gives J_F(pi')<=U_G+e_pi. Subtract. A source certificate for a different pi needs revalidation of its policy upper bound before T9 is applied to pi'. This is the retained S11–S12 argument.

**Comparator counterexample.** G has immediate costs (a,b)=(1,2); F has (1,0). Choose a. Its cost remains one: candidate error zero. But the optimum falls from one to zero, so target regret is one. Rebinding old L=U=1 to F fails b's lower inequality. T1–T2 give L'=0,U'=1, alpha=1,beta=0. Uniform e_*=2 and e_pi=0 give valid but conservative bound two. Replacing e_* by candidate agreement would falsely give zero.

For restricted lifts, let the mapped target policy class have best cost at most V_F+b_cov. Retain b_cov (B3's benchmark-coverage beta) in T9. Uniform comparison inside a class that omits good original policies cannot establish full-class regret without this term. The present identity-skeleton profile compares all target total policies and needs no restricted lift. We write b_cov here to avoid confusing it with the upper correction table beta.

**Neither route is universally tighter.** In §9's off-support case direct transport gives 1/100, while a justified symmetric uniform bound gives 1/50. Conversely, consider a single policy GO followed by END. In G both costs are zero. In F GO costs 100 and END costs -100. Every full-policy total remains zero, so exact uniform error is zero and T9 gives zero. The anchored target upper table retains U'(child)=0 and gives U'(root)=100; the lower root remains zero. Its bound is 100. Direct unanchored target certification gives zero. Thus extremality must retain its stated anchor restriction.

## 7. Conditioning and observed replanning

T5 is ex ante under the supplied target model. At a completed node h, T4 is an algebraic continuation guarantee. To interpret it as a conditional expectation under an episode law, compute the probability of reaching h from F and an explicitly named prefix policy sigma:
\[
 m_F^\sigma(h)=
 \prod_{(a,o)\ \mathrm{along}\ h} p_F(o\mid h_{\mathrm{before}},a)
\]
if sigma selects every indicated action before h; otherwise the mass is zero. STOP before h also gives mass zero. The empty prefix has mass one. Require m>0.

A continuation query binds F, sigma, the exact event h, and the intended continuation policy pi'. The receiver checks the ordinary certificate against F,pi', recomputes the prefix probability, verifies any submitted mass exactly, and returns L'(h),U'(h),U'(h)-L'(h). It accepts no unrelated trajectory vector as evidence. Prefix costs are already paid and excluded. Sigma and pi' may differ: execute sigma before h and pi' afterwards; their roles are separately bound. Future completion of sigma is immaterial mathematically, although this small interface conservatively binds its entire total table.

At zero mass, the normalized conditional answer is undefined, even if fallback actions and completed node bounds exist. This is impossible conditioning in a valid supplied model, not evidence of an empty original model. A different event or prefix policy is a new query and must be rechecked. Structural access assertions are supplied premises, not inferred from text labels.

For cross-model conditional comparisons, retain S14's SAME event, positive masses a,b, and justified trajectory TV Delta:
TV(P(.|e),Q(.|e))<=min(1,Delta/max(a,b)).
An independent proof is to assume a<=b and choose A within e where normalized Q exceeds normalized P. Then b times conditional TV equals Q(A)-(b/a)P(A)<=Q(A)-P(A)<=Delta. Swap P,Q for the other ordering. A model-error bound for a common prefix policy cannot silently authorize differing policies. The direct target query above recomputes its target scope; it does not supply such a cross-model TV warrant. Selecting F from data supplies no statistical coverage theorem.

## 8. Overlapping policy replacements

Use one fixed tree: root STOP costs 2; GO costs 0 and reaches child certainly; child a costs 0 and b costs 1. All these actions stop except GO. The four total policies have costs:

| Policy | Cost |
|---|---:|
| old STOP/a | 2 |
| root-only GO/a | 0 |
| child-only STOP/b | 2 |
| final GO/b | 1 |

The root-only delta against old is -2; child-only delta against old is 0. Their sum -2 is not final minus old, which is -1. The root edit changes the probability of visiting the child. Consecutive deltas are -2 and +1 and sum to -1 exactly. This is not a counterexample to S17, whose single-replacement hypotheses include a common prefix.

For multiple edits, evaluate the actual final policy against one same-model optimum (S15–S16), or compose consecutive genuinely applicable replacement identities. Unrelated predecessor deltas do not do that. The old-policy anchored transport here gives lower 0 and upper 2 for final GO/b: valid bound 2, although actual regret is 1. Recompute a fresh target certificate if tightness is needed; do not call the anchored bound attained.

A finite persistent model family may apply these constructions separately to the SAME accessible policy under each fixed member, giving modelwise bounds gamma_i and uniform bound max_i gamma_i. That is neither minimax optimality nor Bayesian weighting. Switching model rows between dates changes the model; a hidden model label cannot select a different supposedly common policy. No family planner is added.

## 9. Fixed exact cases and verification design

The principal two-step PR5 tree has root STOP 3/4, GO fee 1/8, L/R probabilities 1/2, and child costs L:(a=0,b=1/2), R:(a=1,b=1/4). The old optimal policy is GO/a/b, with L=U=(1/4,0,1/4). Changing to GO/b/a yields lower unchanged and upper (7/8,1/2,1). Independent full paths give cost 7/8; enumeration of all eight policies gives optimum 1/4 and actual regret 5/8. Corrections are alpha=(0,0,0), beta=(5/8,1/2,3/4).

For union-support transfer use nominal GO probabilities (1,0), target (99/100,1/100), with fallback GO/a/a. The old tables are L=(1/8,0,1/4), U=(1/8,0,1). Target transport retains L and gives U'=(27/200,0,1). Thus the certified gap is 1/100. Independent paths and full policies give V_F=51/400, J_F=54/400, actual regret 3/400. Exact uniform policy error is 1/100, so the symmetric bound is 1/50. At R the target mass is 1/100 and the continuation gap 3/4. Nominal R conditioning is impossible.

The deeper fixed tree has horizon four, signed costs and terminal losses, early STOP, a zero-support completed branch with costs 100 and -100, and deliberately non-topological storage. Its source optimum is -53/56 over 16 policies. The checks change two terminal costs and a continuing cost, then evaluate all 16 target policies at all eight completed nodes by a separate forward path oracle. The literal tree is in the fixed source; no parameter grid or random search is used.

Negative controls exercise actual public receiver paths: rebinding stale tables; understated lower/upper corrections; omitted competitor inequalities; missing union-support policy rows; wrong source or target identity, unit, menus, structure, horizon, criterion, correspondence, event or prefix policy; floating-point and Boolean proof values; and caller-container mutation. Accepted controls include unchanged tables, valid explicit new subjects, complete off-support policies, positive target prefixes, arbitrary-size derived rational proofs, terminal-only cases, ties, and singleton menus. Ordinary target-valid but non-anchored certificates distinguish the two warrants. Disabling both producers leaves receiving operational.

## 10. Exact reference, provenance, and limits

The additive [reference](../verification/certificate_transport/transport.py) imports the unchanged PR5 schema and consumer. Model coefficients retain exact int/Fraction normalization and the 256-bit input cap; derived tables, corrections, and prefix mass evidence require exact Fraction values with no such cap. Booleans, floats, strings, and bare integers are rejected on proof routes. Correspondence rows, policies, subjects, and proof containers are detached into immutable values. This protects ordinary caller aliasing, not malicious interpreter memory manipulation.

The full subject and policy are validated before shortcut conclusions. Expected requests are compared with evidence-bound requests only after validation; equality is not a substitute for type checks. There is no tolerance, solver status flag, hash-only semantic comparison, or producer call inside a receiver. Failure to validate is refusal to establish the requested guarantee, not proof of incompatibility or a mathematically opposite answer. Resource refusal remains unfinished. This known normalized tree profile does not solve original nonlinear feasibility or silently replace an original model with an outer relaxation. Those distinctions remain in the unchanged joint-law module.

Limits inherited from PR5: horizon 0–4, at most 64 nodes, four actions and outcomes, and optional exhaustive policy enumeration only on tiny fixed cases. This implementation performs full scans and has no efficiency advantage claim. Proofs are analytical finite inductions, not a formal proof library. Checks share Python Fraction arithmetic and schema; the oracle is a separate calculation path, not independent authorship. Supplied empirical/model/control/access/loss premises are not established by execution.

The [runner](../verification/certificate_transport/README.md) executes new checks normally and with -O, compares observations, runs the existing sequential/PR4/joint-law preservation command, and verifies all base files except the three permitted current pointer/ledger files remain byte-identical. New execution uses GitHub Actions' existing Python with no runtime installation. One compact result record identifies actually executed source bytes; earlier results remain historical.

Bellman remains a continuing mathematical research programme for consequential decisions. Writ and external executable slices do not define its ceiling. This construction does not reopen historical experiments, use unavailable recovery files, modify Writ or Decision Lab, add a general solver, migrate languages, or redesign the architecture.
