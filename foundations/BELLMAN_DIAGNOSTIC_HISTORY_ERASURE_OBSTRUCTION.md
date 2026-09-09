# Diagnostic history erasure: a shared-consistency obstruction

8 September 2026. Additive research on PR #22, inspected current head
`5ea19f214ec89536f47fe20cfa5a4d62222b2598`. Completion route B: a rigorous obstruction
to a specified reduction, with a useful, limited alternative. Ordinary analytical
proof and exact executable evidence; no novelty, external review or formal-proof claim.

## 1. Concrete subject and proposed query

A sender A privately learns quality q in {g,b}. A public diagnostic observation
z in {H,L} then arrives. A remembers both q and z; B remembers z. A may disclose
its genuine quality certificate (`reveal`) or withhold (`N`); it cannot forge the
other quality's certificate. Revelation ends the interaction with payoffs (1,0).
After N, B accepts or rejects. A receives 0 either way; B receives 1 for accepting
g, -1 for accepting b, and 0 for rejection. These are stipulated normalized
utilities and evidence feasibility, not an empirical model of voluntary disclosure.

Two persistent models supply the joint chance law (all entries strictly positive):

| model | g,H | b,H | g,L | b,L |
|---|---:|---:|---:|---:|
| high | 9/16 | 3/16 | 1/16 | 3/16 |
| low | 3/16 | 1/16 | 3/16 | 9/16 |

This is implemented in temporal order q, then z conditional on q. Conditional
P(g|H)=3/4 and P(g|L)=1/4 in BOTH models. P(H) is respectively 3/4 and 1/4.
The proposed common profile reveals at all four sender sets and rejects at both
receiver sets. The assessment after N is P(g|z,N)=1/2 for each z and model.
Sender sets are singletons. Both players have perfect recall.

Proposed representation: discard z from BOTH players' information and from the
represented history tree. A still knows q; B knows only N. Use the marginal
P(g)=5/8 in high and 3/8 in low. Retain the common reveal/reject profile and the
specified posterior P(g|N)=1/2. This represents two genuinely different diagnostic
histories together. It is not an identical-copy construction: diagnostic likelihoods
and conditional quality distributions differ. The target is also perfect recall;
we do not model a player literally forgetting an earlier decision or information set.
The claim is a representation change, not authority to remove real information.

Required queries are every player's assessed conditional utility for EVERY pure
continuation deviation, maximal continuation gains, and existence of ONE completely
mixed sequence supporting the supplied assessments across both models. There is no
prior over the models and no model-indexed strategy. This is uniform modelwise
credibility, not maxmin preferences, Bayesian model learning or empirical prediction.

## 2. Candidate criterion and deviation audit

Consider criterion V: the profile is constant on proposed merged sets; the projected
assessment on retained quality agrees; both games have perfect recall; at every
source decision set each legal continuation has a target continuation with exactly
the same conditional value in every model, and conversely. Require equal proposed
root utilities too. Does V preserve shared consistency for this specified assessment?

The example satisfies V. A's reveal and N values are 1 and 0 at every sender set.
B's accept and reject values are both 0 at every assessed receiver set. Each player
moves at most once on any path, so these are COMPLETE local continuation plans,
not just one-step deviations standing in for later plans. Randomized values follow
by convex combination. Root utilities are (1,0) in every source and target model.
All gains are zero. Every source history-local query has an exact corresponding
query; there is no bounded-error qualification here.

There is deliberately no bijection of global strategies. Source A can reveal only
after H, and source B can use different responses after H and L. Such global policies
cannot be represented by a signal-blind target. At an individual source decision set,
however, the signal is already fixed and every legal local plan is covered. This
suffices for the stated continuation-value query in THIS one-decision-per-player
class; it must not be promoted to coverage of global outcome distributions or of
an earlier player's plans spanning a future diagnostic observation.

## 3. A common source witness

Let the probabilities of N at (g,H),(b,H),(g,L),(b,L) be t,3t,3t,t,
respectively. Let B accept with probability t at both sets. Complements are the
proposed actions. For 0<t<1/4 every action has positive probability and the common
profile converges to reveal/reject. In each model and each signal, the good and bad
prefix masses after N are equal: e.g. at H, (3/4)t=(1/4)3t conditional on H.
Thus the assessed posterior is exactly 1/2 for every such t. The same four rates
work in both models. Combined with §2 this is a source sequential equilibrium
separately in every model, with a shared consistency witness.

This use of a power sequence is constructive; no completeness theorem for a
bounded rational witness format is needed.

## 4. Exact obstruction, including arbitrary consistency sequences

**Odds lemma.** In the binary null-disclosure target, let 0<p_m<1 be the prior
of g and 0<r_m<1 the specified belief after N. The proposed profile reveals at
both types. Its assessment has one common completely mixed consistency sequence
across a finite model family if and only if

    K_m = [r_m/(1-r_m)] [(1-p_m)/p_m]

is the same positive number K in every model.

**Proof, necessity.** For ANY such sequence let x_n>0 and y_n>0 be its N
probabilities at g and b. They are common across models and tend to zero. Bayes gives

    b_m,n = p_m x_n / [p_m x_n + (1-p_m)y_n],
    x_n/y_n = [b_m,n/(1-b_m,n)] [(1-p_m)/p_m].

If b_m,n tends to interior r_m, continuity of the odds map forces x_n/y_n to tend
to K_m. A real sequence cannot have two distinct finite limits. No restriction to
polynomial, monotone, rational, fixed-order or bounded-coefficient trembles was used.
**Sufficiency.** Choose x=Kt, y=t, and any fully mixed B behavior tending to its
specified action, for sufficiently small positive t. Bayes is exactly r_m in every
model; singleton sender beliefs are automatic. QED. Sequential rationality is a
SEPARATE check: in the stated payoffs, proposed rejection requires r_m<=1/2.

For the example, r_m=1/2 gives K_high=3/5 but K_low=5/3. Consequently the target
specified assessment has NO common consistency sequence. Independently, either
model alone does: use its own Kt and t. The target has zero assessed gains and
is a sequential equilibrium model by model with DIFFERENT witnesses. These facts
cannot be joined into a common witness.

**Obstruction theorem.** Criterion V does not preserve shared consistency-existence,
even for positive rational chance laws, two players who each move once, perfect
recall on both sides, identical proposed actions, exact preservation of every local
continuation value, and an explicit common source witness. The construction above
proves the theorem. It strengthens the prior single-model witness-restriction failure:
there, another target witness existed; here, no common target sequence exists at all.

It does NOT say the target game lacks other shared-consistent assessments or
modelwise equilibria. For example, a common x=t^2,y=t gives limiting quality belief
0 in both models; reveal/reject remains sequentially rational. That changes B's
accept value from 0 to -1 and therefore changes the stipulated query. Belief revision
can repair credibility only by relinquishing the original preservation claim.

## 5. Which likelihood information must survive?

The odds lemma also characterizes this entire finite binary null-disclosure class
with any finite signal set and any partition C observed by BOTH players. Write
pi_m(q,z)>0. Let p_m,C be the quality prior conditional on C and let r_m,C be the
supplied interior posterior at N,C. The assessment is shared-consistent exactly when

    K_m,C = [r_m,C/(1-r_m,C)]
            [sum_(z in C) pi_m(b,z) / sum_(z in C) pi_m(g,z)]

is independent of m for each cell C. Apply the necessity proof separately at each
cell; for sufficiency use the finitely many cell rates K_C t,t with one small t.
This characterizes consistency-existence within the stated class; it is not a
characterization of general game abstraction or of all sequential equilibria.
Preserving conditional accept values additionally requires the corresponding r's
to agree. Taking r_m,C=1/2, source singleton cells have K_H=1/3 and K_L=3.
Their merged cell has incompatible model requirements. The discarded distinction
permits different sender tremble ratios at H and L. Equal assessed quality beliefs
do not encode those restrictions.

The exact receiver implements only the two-signal, r=1/2 obstruction instance class,
not a partition search or a general implementation of this formula. A same-ratio
family must not receive an impossibility label. At boundary posteriors 0 or 1 the
interior odds proof does not apply; separate asymptotic-order reasoning is needed.

## 6. Nearest useful alternative: keep the sender's diagnostic information

Keep the same physical source tree and all four A information sets. Merge only
B's two sets into one: B no longer observes z before its first and last action.
B's new belief is over FOUR histories (q,z), not just over q. Thus the sender retains
the likelihood-generating distinction even though the receiver's decision memory
shrinks. There is no reduction in physical tree nodes. Information sets shrink
6 to 5; full erasure would shrink them to 3 but fails the specified query.

For the supplied witness in §3 the new belief in high is

    (g,H; b,H; g,L; b,L) = (3/8,3/8,1/8,1/8),

and in low it is (1/8,1/8,3/8,3/8). Reuse all A trembles, and choose any common B
accept tremble tending to zero. Independent exact polynomial receiving verifies
these full beliefs. In both models their quality marginal is 1/2; every A action
value and both B action values therefore remain exactly the same. B cannot implement
a z-contingent response; at each original local B query, all action values are still
preserved. This is assessment-specific, not preservation for a broader strategy class.

**Restricted transport fact.** In this null-disclosure class, suppose every source
receiver set has the same limiting quality belief r_m within a model and the proposed
receiver action is invariant. For any supplied common rational power witness, retain
sender terms and merge B's decision. Every prefix reaching a player decision remains unchanged; the merged
belief is the normalized leading mass on all (q,z) histories. Such limits exist because
these are finite nonnegative polynomial prefix masses with nonzero denominator.
The merged quality belief tends to r_m: it is a convex combination of the conditional
quality beliefs, whose maximum deviation from r_m tends to zero over the finite signal
set. Sender utilities are independent of B, and receiver utilities depend only on q
and its last action. Hence every relevant local conditional value is preserved.
This proves forward transport of the witness AND its induced full assessment.

For arbitrary common source sequences one can choose a COMMON subsequence on which
all finitely many merged full beliefs converge (compactness of the finite product of
simplices). The same marginal argument holds. Thus existence of a source sequence
implies existence of SOME full merged assessment with the required quality marginals.
It does not imply transport to an arbitrary supplied four-history assessment, nor
reverse preservation, nor a bijection of consistency sets. The executable example
binds one exact induced assessment and checks it afresh. Arbitrary sequences and the
general compactness statement are analytical only.

## 7. Decisive boundaries and mechanism composition

An earlier Continue decision followed by a fair diagnostic bit and a later rewarded
bit guess has continuation value 1 with recall and 1/2 for every signal-blind mixture.
Both histories may recommend Continue now; their future optimal guesses disagree.
There is no target plan simultaneously covering the remembered later decisions.
This refutes immediate-action clustering before likelihood questions even arise.
If a player first ACTED at distinct known information sets, merging a later set while
forgetting those distinctions can also violate perfect recall; our target avoids this.

A bond example makes the mechanism dependency explicit. After an identical acceptance
step let A choose comply or defect, with extra gain 3/2 from defect, bond 2, and
history-dependent detection p_H=1, p_L=1/2. The comply-to-defect gains are -1/2 and
+1/2. Replacing p by its average 3/4 would report zero and erase a profitable
conditional deviation. Signal-conditioned monitoring must survive, or its continuation
values must be re-proved equivalent. The retained arithmetic control is not a new
mechanism solver; the earlier full evidence/bond game continues to supply the richer
exact mechanism checks. No optimal mechanism or causal identification follows here.

The retained public-coordination counterexample remains another independent boundary:
a public bit enables matching with probability 1, whereas replacing correlated actions
by their independent marginals gives 1/2. Exact root utility or local zero-gain comparisons
do not license preservation of all outcome laws. That earlier evidence is replayed
unchanged, not copied into a new historical edition.

## 8. Established mathematics and actual tool capabilities

Sources were inspected on 8 September 2026. Their results inform boundaries; the
odds argument and restricted repair above are explicit specialized derivations.

- Tang, Subramanian and Teneketzis, [Information Compression in Dynamic Games](https://link.springer.com/article/10.1007/s13235-025-00663-1),
  published 2025, journal volume 2026: Definitions 3–5 impose reward/transition
  sufficiency and, for USI, a conditional factorization for ALL behavioral profiles.
  The finite perfect-recall model and Theorems 3–4 give MSI SE existence and USI
  preservation of SE payoff sets. These retain full-history deviations. They do not
  transport an arbitrary specified full belief or impose one sequence across an
  uncertainty family. Our proposed diagnostic erasure fails the sufficiency test:
  even constant type-independent N trembles leave P(g|H,N)=3/4 and P(g|L,N)=1/4,
  changing B's accept reward. Inspecting only the proposed off-path half-beliefs
  misses this. We therefore do not invoke their theorem as a warrant for erasure.
- Lanctot et al., [No-Regret Learning in Extensive-Form Games with Imperfect Recall](https://arxiv.org/pdf/1205.0622),
  Definition 2 and Theorem 1: terminal bijections with proportional utilities/chance
  reach and matching opponent and own future information/action sequences support
  CFR regret bounds relative to a perfect-recall refinement. Root regret does not
  establish supplied off-path assessments or common family consistency.
- Kroer and Sandholm, [Imperfect-Recall Abstractions with Bounds in Games](https://www.columbia.edu/~ck2945/papers/imperfect-recall-abstraction-with-bounds.pdf),
  CRSWF Definition 2.3 and Theorems 3.2–3.3: structural matching and controlled reward,
  chance and distribution errors give counterfactual-regret/approximate Nash bounds.
  Theorem 3.3 explicitly handles unconstrained off-path Nash behavior by a
  self-trembling modification. This is not a claim preserving the supplied beliefs.
- Dilmé, [A characterization of consistent assessments using power sequences](https://link.springer.com/article/10.1007/s00182-023-00874-z),
  Theorem 3.1 and Proposition 4.2: power sequences characterize consistency with real
  positive coefficients and integer orders. Bellman's bounded rational checker is
  not a complete implementation. Here arbitrary-sequence nonexistence is proved
  directly by Bayes odds; positive witnesses reuse the existing polynomial receiver.
- Tavafoghi, Ouyang and Teneketzis, [Unified Approach, Part II](https://arxiv.org/pdf/1812.01132),
  Definition 2 and Lemma 1: PBE consistency uses Bayesian updates and reachability
  conditions; SIB representations require additional belief compatibility. This
  notion must not silently replace the common completely mixed sequence demanded here.
- Hart, Kremer and Perry, [Evidence Games: Truth and Commitment](https://math.huji.ac.il/~hart/papers/st-ne-201603.pdf),
  author edition March 2016, sections 2–4: truthful feasible messages are constrained
  by an evidence relation, while truth-leaning and single-peaked principal preferences
  under all type mixtures support their commitment comparison. Our binary accept/reject
  payoff and disclosure reward are stipulated; we borrow verifiability, not their
  optimal-mechanism conclusion or equilibrium refinement.
- Aghassi and Bertsimas, [Robust Game Theory](https://www.mit.edu/~dbertsim/papers/Robust%20Optimization/Robust%20Game%20Theory.pdf),
  section 3: robust optimization of worst-case expected payoff differs from requiring
  every modelwise continuation gain to be zero. No ambiguity-preference result is claimed.

Actual implementation inspection reused the retained research checkouts:
[GTE-sequential](https://github.com/tengesser/GTE-sequential/tree/cba2f7c75a64bc6759e3ad1754dc58aa8134bbc9) at
`cba2f7c75a64bc6759e3ad1754dc58aa8134bbc9`, backend
`c8a9588bae77c7913bcbb9233523336ecf1f44b0`, constructs node-pair consistency matrices
in `sequential_solver/solver/solver.py` (around 693–735) and invokes Wolfram
CylindricalDecomposition (around 936–975). It was inspected, not executed. This
construction needs only an odds identity, not a general equilibrium search.
Gambit's inspected `GetBeliefProb` returns no belief at zero reach; OpenSpiel's
inspected `exploitability.py` computes root best responses/NashConv, not these
specified off-path beliefs. Exact revision identifiers remain in the earlier research
review. We reuse the installed SymPy 1.14.0 QQ polynomial receiver and exact rational
path receiver; `linsolve` independently corroborates the example's incompatible
linear odds equations. No handwritten symbolic engine is added.

A Lean formalization of the elementary odds-continuity lemma would add little material
assurance at this stage: the delicate obligations are the information map and query
quantifiers. There is no measured optimization bottleneck or production checker
requirement for Rust/JuMP. No language migration or new framework is warranted.

## 9. Identity, validation and earned scope

`verification/diagnostic_erasure/example_case.json` retains the complete three subjects,
common source/repair witnesses, separate target-model witnesses, all target incentive
rows, and the two-model obstruction. The receiving caller supplies the intended
subject identities separately and the exact query identifier. The receiver recognizes
the entire stated game class, checks marginalization and map restrictions, receives
all positive claims using existing independent receivers, and checks every local
pure action value. Rejection controls cover changed odds, models, payoffs, beliefs,
information, witnesses, missing deviations and stale/query identities. Receiving runs
in a deployment with every candidate producer absent. Normal and optimized observations
must agree. Acceptance byte-checks earlier sources and replays inherited obligations
at their retained commits; no old evidence is rewritten.

Proved: criterion V fails; exact interior-odds characterization for this class;
restricted forward receiver-only repair with the stated belief scope. Computationally
checked: the retained rational instance, its repair, individual targets, all local
values, obstruction premises, and decisive negative controls. Assumed: chance laws,
evidence feasibility, utilities and actual memory. Unresolved: general history
quotients, full strategy-class and specified-belief transport, approximate off-path
consistency, general shared-consistency search and empirical applicability.

This materially advances strategic disclosure and history preservation by identifying
which sender information a likelihood-preserving representation cannot discard. It
clarifies the obligation for mechanism composition; it does not earn a new mechanism
composition theorem. The next useful frontier is a specified deviation- and
likelihood-sufficient representation under a broader strategy class, using the
established MSI/USI conditions as a starting point and explicitly adding cross-model
sequence compatibility. Do not treat repeated passing copies as progress on that gate.
