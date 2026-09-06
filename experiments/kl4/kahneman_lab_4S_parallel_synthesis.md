# Kahneman Lab Experiment 4 — Frozen Parallel Synthesis

## Result and scope

**Lanes A–D establish the preregistered distinctions using existing mathematics. Lane E is technically eligible under the frozen rule because Lane C supplies the required canonical pair. Eligibility establishes neither a strategic separation nor mathematical novelty.**

This report executes only the synthesis specified in sections S1–S2 of the original packet. The packet and all four completed reports were read in full, including their embedded reproduction and verification material. The reports are frozen evidence: their searches, selections, counts, computations, and interpretations have not been rerun, repaired, expanded, or replaced. No conflict or internal inconsistency requiring arithmetic verification was identified; no new arithmetic verification was performed. Numerical results below are attributed to the completed reports, rather than presented as independently reproduced synthesis results.

The user's current request governs execution. Instructions in the attached packet to launch lane chats, execute searches, create their deliverables, or prepare a later preregistration are historical protocol content, not authorization to perform those actions now. The requested filename, `kahneman_lab_4S_parallel_synthesis.md`, supersedes the packet's synthesis filename. No Lane E execution, new experiment design, literature search, novelty review, or application to another domain is included. This is the sole output file.

Three conclusions must remain separate:

1. **Preregistered findings:** the finite witnesses, extrema, quotient results, and stopping policies reported by A–D answer their specified questions.
2. **Limits:** these findings do not establish unrestricted sufficiency, transfer across changed decision problems, a new methodology, or an unresolved mathematical obstacle requiring new machinery.
3. **Frozen eligibility:** Lane C meets all four stated Lane E conditions. The synthesis must therefore return the packet's eligibility verdict, without adding a stronger gate after seeing the pair.

## 1. Frozen evidence and mathematical setting

References [P] and [A]–[D] below identify the supplied documents by their exact filenames. All substantive lane results in this report come from these sources.

| Reference | Supplied document | Frozen lane verdict |
|---|---|---|
| [P] | `RUN_THIS_NEXT_KAHNEMAN_LAB_4_PARALLEL (1).md` | Original preregistration, including S1–S2 and the Lane E gate |
| [A] | `kahneman_lab_4A_information_vs_decision_value(1) (1).md` | `KL4A_REVERSAL_FOUND_TIER1` |
| [B] | `kahneman_lab_4B_deep_uncertainty_stability(1).md` | `KL4B_NONTRIVIAL_STABILITY_AND_BOUNDARY_FOUND` |
| [C] | `kahneman_lab_4C_query_sufficiency_quotients (1).md` | `KL4C_NONTRIVIAL_QUERY_RELATIVE_COMPRESSION_FOUND` |
| [D] | `kahneman_lab_4D_stop_or_observe (1).md` | `KL4D_ENTROPY_NOT_SUFFICIENT_FOR_STOPPING` |

For a finite state space, action set, prior, loss table, and observation kernel, the common quantities are

\[
A^*(p)=\arg\min_a\sum_\theta p(\theta)L(a,\theta),\qquad
R(p)=\min_a\sum_\theta p(\theta)L(a,\theta),
\]

\[
EVSI(X)=R(p)-\sum_xP(x)R(p(\cdot\mid x)),\qquad
NV(X)=EVSI(X)-c.
\]

Mutual information measures expected state-information gain and contains no loss table. EVSI measures expected reduction in optimal loss for the specified decision problem. Credal-set stability concerns action agreement over admissible priors. Query sufficiency concerns preservation of specified answers. Sequential stopping compares immediate action with an adaptive continuation policy. These are different mathematical objects, even when they share the same underlying ingredients.

Full minimizing action sets are retained. Impossible observations remain `NA`, not invented posteriors or action ties. Exact fractions below retain the reports' rational values; displayed entropy and mutual-information decimals are abbreviated reported approximations.

## 2. Preregistered findings

### 2.1 Lane A: more mutual information can have less decision value

[A] reports exhaustive Tier 1 enumeration: 18 valid loss tables, 10 informative test classes after binary-outcome relabeling, and 126 prior/loss contexts. Among 11,340 ordered pairs of distinct tests across these contexts, 388 exhibit the required strict reversal. These are descriptive grid counts, not estimates of prevalence. Tier 2 was correctly not triggered.

The selected witness has prior \((p(0),p(1))=(7/8,1/8)\) and zero-one loss,

\[
L=\begin{pmatrix}0&1\\1&0\end{pmatrix},
\]

with action rows and state columns. Its likelihood vectors are

\[
\bigl(K_1(1\mid0),K_1(1\mid1)\bigr)=(1/4,1),\qquad
\bigl(K_2(1\mid0),K_2(1\mid1)\bigr)=(0,1/4).
\]

The current action set is \(\{0\}\), and current Bayes risk is \(1/8\).

| Quantity | Higher-MI test \(X_1\) | Lower-MI test \(X_2\) |
|---|---:|---:|
| Mutual information, bits | approximately 0.218493713493126 | approximately 0.099212558755323 |
| Expected posterior Bayes risk | 1/8 | 3/32 |
| EVSI | 0 | 1/32 |
| Action sets after outcomes 0 and 1 | \(\{0\},\{0\}\) | \(\{0\},\{1\}\) |

The reported MI gap is approximately 0.119281154737803 bits, above the preregistered strictness threshold; the decision-value gap is exactly \(1/32\). [A] reports high-precision agreement and independent ranking verification within the completed lane.

The action boundary is \(p(1)=1/2\). Test \(X_1\) yields posterior probabilities of state 1 equal to 0 or \(4/11\), both preserving action 0. Test \(X_2\) yields \(3/31\) or 1; its rare outcome of marginal probability \(1/32\) warrants switching to action 1. Thus uncertainty reduction that never changes the optimal terminal action can have zero EVSI, while a smaller entropy reduction can have positive EVSI by crossing the action boundary. No separate nuisance variable is needed for this witness.

**Limit.** This reverses the MI and EVSI rankings for the specified prior, losses, and tests. It does not make higher MI intrinsically harmful, establish a universal test ordering, or show that \(X_1\) has zero value under other losses or sequential uses. “First” is relative to [A]'s declared lexicographic encoding; minimality is within the preregistered tier structure, not all finite models.

### 2.2 Lane B: probability uncertainty and decision instability are different

[B] reports 32 valid loss tables and 105 distinct segments per table, giving 3,360 cases. It classifies 1,692 as strongly stable, 1,500 as endpoint-unstable, and 168 as having an endpoint tie. The selected extrema are:

| Quantity | Maximum-diameter strongly stable witness | Minimum-positive-diameter unstable witness |
|---|---|---|
| Loss matrix, action rows | \(\begin{pmatrix}0&1\\4&0\end{pmatrix}\) | \(\begin{pmatrix}0&1\\2&0\end{pmatrix}\) |
| Segment for \(p=P(\theta=1)\) | \([1/16,3/4]\) | \([5/8,11/16]\) |
| Total-variation diameter | 11/16 | 1/16 |
| Bayes action boundary | 4/5 | 2/3 |
| Bayes action behavior | uniquely 0 throughout | uniquely 0 at left endpoint; uniquely 1 at right endpoint; tie at 2/3 |
| Γ-minimax action set | \(\{0\}\) | \(\{0\}\) |
| Minimax-regret action set | \(\{0\}\) | \(\{0\}\) |

The stable segment lies entirely on one side of its loss-dependent boundary despite its broad probability range. The narrow unstable segment crosses its boundary. [B]'s affine loss-difference argument establishes stability over every real prior in the segment, not just the grid points. Its analytic diameter bounds support the reported finite extrema. No fallback was triggered.

**The robustness criteria did not create consequential disagreement in either selected witness.** Both select action 0 uniquely. In the unstable witness this agreement does not restore a common Bayes action: action 1 remains uniquely optimal at admissible priors above \(2/3\). A robust selection and pointwise Bayes agreement are different claims.

**Limit.** The two selected segments use different loss tables, so their width comparison establishes existence across the specified class, not a controlled change of width holding losses fixed. The robust comparison concerns these two selected segments; it does not establish universal agreement of the criteria. The minimum unstable diameter is a grid-endpoint minimum. Probability uncertainty is not classified as irrationality, and neither robustness criterion is established as universally correct.

### 2.3 Lane C: sufficiency is relative to the exact downstream queries

[C] reports 216 valid full objects \(F=(p,L,K)\). Constant and uninformative tests are included, as permitted by [P]. Its nested query signatures preserve:

- **Q0:** the current optimal action set.
- **Q1:** Q0 and the action set after each labeled test outcome, with `NA` for an impossible outcome.
- **Q2:** Q1 and exact one-step EVSI.
- **Q3:** Q2 and the four current-action answers obtained by separately adding 1 to each original loss cell, holding \(p,K\) fixed and applying no renormalization.

The respective quotients contain **3, 19, 31, and 109 classes**. Each successive partition strictly refines its predecessor. Refinement follows from signature nesting; the strictness, counts, and canonical collisions are reported finite results.

Here “exact” means the same partition as the query signature, and “overpreserves” means sufficient while retaining additional distinctions.

| Summary | Summary classes | Q0 | Q1 | Q2 | Q3 |
|---|---:|---|---|---|---|
| `S_action` | 3 | Exact | Insufficient | Insufficient | Insufficient |
| `S_policy` | 19 | Overpreserves | Exact | Insufficient | Insufficient |
| `S_certificate` | 31 | Overpreserves | Overpreserves | Exact | Insufficient |
| `S_pL` | 24 | Overpreserves | Insufficient | Insufficient | Insufficient |
| `S_pK` | 27 | Insufficient | Insufficient | Insufficient | Insufficient |
| `S_full` | 216 | Overpreserves | Overpreserves | Overpreserves | Overpreserves |

The narrowness of the queries explains the sufficient summaries. Current action alone answers Q0; adding contingent actions answers Q1; adding EVSI answers Q2. In particular, `S_certificate` equals \(\sigma_2\) by definition. Its Q2 sufficiency is therefore structural, not an independently discovered universal sufficiency theorem. The enumeration establishes that distinct permitted objects actually share these answers.

The frozen collisions make the successive losses of information concrete:

- F1/F2 share the current action, but differ in contingent policy: outcome 1 is impossible in F1 and requires action 1 in F2.
- F2/F3 share the contingent policy, but have EVSI \(1/8\) and \(1/4\).
- F1/F10 share the policy-plus-EVSI certificate, but differ under a specified loss-revision query.

**Limit.** Among the six candidate summaries, only `S_full` suffices for Q3. Full-object retention is nevertheless not mathematically necessary for Q3: the exact Q3 quotient still merges 216 objects into 109 classes, and \(\sigma_3\) itself preserves its answers. These quotients are extensional benchmarks, not claims about practical storage or unrestricted future queries. A Q2 certificate does not promise preservation of posterior probabilities, outcome masses, absolute Bayes risks, revised-loss decisions, or sequential continuation values merely because it preserves the stated Q2 answers.

### 2.4 Lane D: stopping depends on costs and continuation opportunities

[D] reports all three required witness types within 9,120 parameter tuples and 45,600 initial parameter-and-horizon evaluations. There are 1,012 high-entropy strict-STOP cases and 278 low-entropy strict-OBSERVE cases at horizon 5. At horizon 2 there are 1,514 cases with nonpositive one-step net value and strictly optimal observation. These are labeled-grid counts; counts at different horizons can include the same parameter tuple.

The model uses symmetric signal accuracy \(q\), false-positive loss \(C_{10}\), false-negative loss \(C_{01}\), cost \(c\), and at most \(h\) remaining observations. Its recurrence is

\[
V_0(p)=R(p),\qquad
V_h(p)=\min\left\{R(p),c+\sum_xP(x\mid p)V_{h-1}(p_x)\right\}.
\]

| Quantity | D-HIGH-STOP | D-LOW-OBSERVE | D-MULTISTEP |
|---|---|---|---|
| \((p,q,C_{10},C_{01},c,h)\) | \((7/20,3/5,1,1,1/20,5)\) | \((1/20,3/5,1,8,1/100,5)\) | \((1/20,2/3,1,8,1/100,2)\) |
| Prior entropy, bits | approximately 0.9340680554 | approximately 0.2863969571 | approximately 0.2863969571 |
| Immediate terminal action set | \(\{0\}\) | \(\{0\}\) | \(\{0\}\) |
| Terminal Bayes risk | 7/20 | 2/5 | 2/5 |
| One-step EVSI | 0 | 0 | 0 |
| One-step net value | −1/20 | −1/100 | −1/100 |
| Forced-observation cost at selected horizon | 2/5 | 94039/250000 | 6143/18000 |
| Optimal DP value | 7/20 | 94039/250000 | 6143/18000 |
| Initial choice | strict STOP | strict OBSERVE | strict OBSERVE |

For D-HIGH-STOP, immediate posterior beliefs \(14/53\) and \(21/47\) both strictly stop with four observations remaining. For D-LOW-OBSERVE, posterior \(2/59\) strictly stops while \(3/41\) strictly observes with four remaining. For D-MULTISTEP, posterior \(1/39\) strictly stops while \(2/21\) strictly observes with one remaining. These are the completed report's next-step policies; the first witness's branches are counterfactual because its initial policy stops.

In D-MULTISTEP, one observation cannot change the terminal action. After a first signal 1, a second signal 1 produces belief \(4/23\), which crosses the terminal action boundary \(1/9\). The first observation therefore opens a valuable continuation opportunity even though its one-step EVSI is zero. Horizon 2 is the smallest eligible multistep horizon and already contains a strict witness.

[D] also supplies a same-entropy comparison within its frozen report: holding D-LOW-OBSERVE's prior, signal, losses, and horizon fixed while changing only cost to \(1/2\) makes STOP strictly optimal. Every forced observation then costs more than the stopping risk \(2/5\). The low-cost case strictly observes. This directly rules out entropy alone as a sufficient stopping statistic across the stated class, without relying solely on the high- versus low-entropy examples.

**Limit.** These results concern the prescribed finite-horizon signal model, losses, and costs. They do not imply that low entropy generally calls for observation or high entropy generally calls for stopping. Nonpositive one-step net value is sufficient to rule out a strict benefit from one observation followed by mandatory action; it is not a sufficient stopping rule when valuable later observations remain available.

## 3. What can and cannot be transported across lanes

The lanes share decision-theoretic definitions, not a single common enumerated model space. Their prior grids, likelihood restrictions, loss ranges, and downstream tasks differ. Their witnesses cannot be substituted for one another without changing the question.

| Connection | Supported synthesis | Unsupported transport |
|---|---|---|
| A → D | Information about the state and reduction in decision loss differ; entropy is not a substitute for a decision-value calculation. | A's zero-EVSI test is not thereby valueless in a sequential setting. D does not evaluate repeated uses of A's selected tests. |
| B ↔ A/D | Loss-dependent action regions help explain both stable actions and whether posterior movements affect terminal decisions. | B's stability over a specified credal segment does not imply zero EVSI or optimal stopping for an unspecified signal. B neither specifies reachable posteriors nor evaluates observation policies. |
| C → a fixed one-step decision | For the defined Q2 uses, equal certificates preserve policy and EVSI. With the same externally specified cost and one observation followed by action, they also preserve the sign of \(EVSI-c\), including a tie. | Q2 sufficiency does not promise equal absolute costs or values, revised-loss answers, or decisions with more observations available. |
| C ↔ D | C makes the scope of sufficiency explicit; D shows that one-step net value does not settle a sequential decision. | D does not supply two full objects with equal C certificates and different sequential policies. It is not a completed sequential-insufficiency experiment for C's quotient. |
| C Q2 → Q3 | F1/F10 is an actual frozen same-certificate pair distinguished by the specified loss revision. | Loss-revision distinguishability is not a demonstrated strategic distinction and does not execute Lane E. |
| B → robust observation decisions | The selected robust actions can be reported alongside pointwise Bayes actions. | A single-prior Bayesian EVSI or D's recurrence has not been shown sufficient for decisions over B's credal sets. No robust updating or sequential robust model was tested. |

In particular, D compares stopping with \(c+E[V_{h-1}(p_x)]\); one-step EVSI compares current risk with \(E[R(p_x)]\). Replacing the continuation value by terminal risk changes the decision problem when further observations remain. C's initial policy-plus-EVSI signature contains exactly its declared answers, not an established representation of all continuation states and values.

The scientific conclusion is therefore bounded: the distinctions fit together, but a result established for one query family or model does not automatically extend to another. No missing cross-lane experiment has been silently filled in by analogy.

## 4. Existing mathematics, retained concepts, and residual questions

The qualitative results are handled by the mathematical ingredients already specified in [P]:

- **Bayesian decision theory and value of information:** expected-loss minimization explains A's action boundary and why information can have no immediate decision value.
- **Affine expected losses and convex regret:** these explain B's continuous-segment stability, boundary crossing, and endpoint robust calculations.
- **Equality of query answers:** this gives C's exact sufficiency notion and refinement by nested signatures. The finite enumeration contributes the class counts and explicit collisions.
- **Finite-horizon dynamic programming:** this explains D's costs, adaptive continuation, and multistep option value.

The exact selected witnesses, grid extrema, counts, and class sizes are the reports' finite findings. They are not all supplied merely by writing the definitions down. Nevertheless, none requires a new mathematical framework, and no report establishes novelty. This synthesis conducts no external novelty assessment.

The evidence supports a coherent minimal mosaic: use Bayesian expected loss to define an action problem, distinguish information quantity from loss reduction, represent uncertainty over priors explicitly when that is the problem, state the downstream queries before claiming compression, and use continuation values when observations can be sequential. Coherence means that these components have intelligible and bounded roles. It is not evidence that their interfaces have all been solved by a single certificate or architecture.

**Decision sufficiency earns continued use only as a representation property relative to a stated query family.** C directly supports that use. Its support does not restore the retired D analysis methodology; the current Lane D stopping experiment is distinct from that retired methodology.

**Common-completion or compatibility machinery is not required by these KL4 results.** No lane combines mutually constrained partial models or needs a shared completion to obtain its findings. B's set of admissible priors and C's equivalence classes are not, by themselves, such a requirement. Combining the four reports in prose supplies no additional warrant for that machinery. Earlier KL2/KL3 concepts receive no broader endorsement than this packet and the present evidence support.

There is an explicit scope boundary between C's one-step certificate and D's sequential decisions, but A–D do not establish a precise unresolved single-agent mathematical obstacle there. They show neither a tested cross-lane certificate collision nor a failure of the existing dynamic program. A desire to combine the components is not a residual result. The condition for the single-agent continuation verdict has not been established.

The packet's stated strategic-interface question remains unanswered by A–D: whether the exact canonical models, indistinguishable for Q2, become distinguishable when the certificate passes to another responding agent. That is an unexecuted question from the original protocol, not a mathematical discovery of this synthesis. Q3 already shows a particular extension of the query family that distinguishes the pair, and standard query-relative sufficiency explains why preservation outside Q2 is not guaranteed. Neither fact establishes a strategic outcome or an unresolved problem beyond existing mathematics. No new experiment is designed here.

## 5. Lane E eligibility under the unchanged frozen rule

The canonical pair in [C] is **F1/F10**, under that report's declared ordering. Preserve that exact pair:

\[
p=(3/4,1/4),\qquad
L=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
L'=\begin{pmatrix}0&1\\2&0\end{pmatrix}.
\]

The common kernel satisfies

\[
K(0\mid0)=K(0\mid1)=1,\qquad
K(1\mid0)=K(1\mid1)=0.
\]

Thus \(F=(p,L,K)\) and \(F'=(p,L',K)\), with common certificate

\[
S_{\mathrm{certificate}}(F)
=S_{\mathrm{certificate}}(F')
=\bigl((\{0\},\{0\},NA),0\bigr).
\]

| Frozen condition from [P] | Evidence in [C] | Assessment |
|---|---|---|
| 1. \(F\ne F'\) as full objects | Loss of action 1 in state 0 is 1 versus 2, with the same labels, prior, and kernel. | Satisfied |
| 2. Equal `S_certificate` | Both have current action \(\{0\}\), outcome-0 action \(\{0\}\), impossible outcome 1, and EVSI 0. | Satisfied |
| 3. Certificate sufficient for preregistered Q2 | `S_certificate` is exactly \(\sigma_2\); [C] reports sufficiency throughout the 216-object space. | Satisfied |
| 4. Pair indistinguishable for those single-agent uses | Every component of every defined Q2 answer agrees. | Satisfied |

**Lane E is technically eligible.** The constant test and zero EVSI are permitted by Lane C's frozen object space. The gate does not require an informative test, positive EVSI, equal full loss tables, Q3 equivalence, sequential equivalence, a prior strategic separation, or proof of novelty. None of those requirements can be added retrospectively. The pair is genuinely different as specified full objects despite the simplicity of its shared certificate.

The same pair is already distinguishable under Q3: adding 1 to loss cell \((a=0,\theta=0)\) gives current expected losses \((1,3/4)\) for F1 and \((1,3/2)\) for F10, selecting actions 1 and 0 respectively. This reported result bounds Q2 sufficiency. It neither invalidates the gate nor demonstrates the hypothesized strategic distinction.

Eligibility also does not establish that a follow-on would be novel, necessary, or scientifically fruitful. Those are stronger claims than the four frozen conditions. The present request authorizes only reporting eligibility; Lane E and any new preregistration remain unexecuted.

## 6. Preregistered verdict

The mathematical assessment is that existing mathematics handles every reported A–D result. No new methodology, strategic result, or precise unresolved single-agent mathematical obstacle is established. Those limits stand independently of the eligibility assessment.

Section S2 also explicitly directs the strategic-interface eligibility verdict **if and only if** the frozen gate is satisfied. All four gate conditions hold. Returning a stop verdict instead because the canonical pair seems too simple would impose an additional condition absent from that gate. Returning the single-agent continuation verdict would claim a basis not established here.

The required verdict therefore records **technical eligibility only**. It does not assert execution, successful strategic separation, mathematical novelty, or a recommendation based on a newly designed experiment.

## Appendix: source identity

The five supplied files were read from `/Users/kimchee/Downloads/`. Their SHA-256 digests identify the frozen source bytes used for this synthesis; hashing did not execute any embedded reproduction code.

| Reference | SHA-256 |
|---|---|
| [P] | `d8206786bd7d07f3f92c4568ae4cc3f7c088aca8089a5a6d75f2f0b7bb4238ad` |
| [A] | `db484f36e4db782c28e7348f3d5d9da36fc6c7d6838d9aed27c1a06e187fa9b9` |
| [B] | `702f2f8fca10c53323d4f4a3a07798d29dc5176be99ce3feebe1500e70d219fb` |
| [C] | `3312c6499d7e2f50325d32537d7961ed46466b95e753c02189763b513450c7f3` |
| [D] | `a3494b711d99aa9997bf27bdd035ea67990321fe7e883fda35cfdae48b303c94` |

KL4_STRATEGIC_INTERFACE_ELIGIBLE
