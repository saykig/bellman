# Sequential credibility under uncertainty

Date: 8 September 2026. Status: new bounded research component, not independently reviewed or formally verified. Base: main `cea4e1a47cb91c1f3917490350deab53d2976908` (merged PR #20). Unmerged PR #21 is not a dependency. This additive record does not replace earlier foundations.

## 1. Question and scope

Can one supplied strategy profile remain sequentially rational across a finite family of games, with private evidence, selective disclosure, a bond, and imperfect monitoring? What must a representation preserve, and what must be rechecked after a mechanism change?

The component checks **uniform sequential rationality conditional on supplied assessments**. It does not solve for an equilibrium, establish Kreps–Wilson consistency, infer human behavior, validate causal premises, or establish an institution's authority. A positive result is not labelled a sequential equilibrium. The family indexes analyst uncertainty; no worst-case preference is imputed to actors.

All four directions enter one subject: game uncertainty, information sets and disclosure actions, remembered history, and mechanism-dependent payoffs/transitions. Credibility is the query over that subject.

## 2. Established foundations and reuse

- Kuhn (1953), *Extensive Games and the Problem of Information*: finite extensive games, perfect recall, and pure/mixed/behavioral strategies. https://doi.org/10.1515/9781400829156-011 . Our pure-continuation reduction below is proved directly for the restricted tree, using finite expansion rather than claiming an imported formal theorem.
- Kreps and Wilson (1982), *Sequential Equilibria*: sequential rationality and consistency of beliefs are distinct obligations. https://www.gsb.stanford.edu/faculty-research/publications/sequential-equilibrium . This component checks Bayes' rule at positive-reach information sets, but does not check limiting tremble consistency off path.
- Aghassi and Bertsimas (2006), *Robust Game Theory*: robust-optimization equilibrium differs from ex-post robustness. https://web.mit.edu/dbertsim/www/papers/Robust%20Optimization/Robust%20Game%20Theory.pdf . Their existence theorem is not an existence theorem for our uniform sequential criterion.
- Hart, Kremer and Perry (2017), *Evidence Games: Truth and Commitment*: verifiable evidence can be selectively disclosed. https://www.aeaweb.org/articles?id=10.1257/aer.20150913 . We borrow that distinction, not their specialized equilibrium/commitment equivalence conclusion.
- Kroer and Sandholm (2014), *Imperfect-Recall Abstractions with Bounds in Games*: transfer guarantees need structural conditions. https://arxiv.org/abs/1409.3302 . Our simpler uniform-payoff transfer lemma below is not their theorem and does not permit arbitrary imperfect recall.
- Epstein and Schneider (2003), *Recursive Multiple-Priors*: recursive ambiguity preferences require additional structure. https://pages.stern.nyu.edu/~dbackus/Exotic/1Ambiguity/EpsteinSchneider%20priors%20JET%2003.pdf . We keep a model fixed during each continuation evaluation, without rectangularizing it or repeatedly choosing worst-case rows.

This is a specialization and composition of established finite-game reasoning. No novelty claim is made. Python's Fraction and itertools supply exact arithmetic and enumeration. Gambit/PyGambit is the next candidate-generation dependency if equilibrium search is requested; it is unnecessary for checking these supplied tiny profiles. OpenSpiel is a later behavioral-experiment option. Mathlib and gametheoryinlean/EconCSLib are candidates for selected formalization; neither has been imported or audited here. No language escalation is earned.

## 3. Exact mathematical subject

A nonempty finite family M shares one finite rooted history tree, player set, action-labelled edges, and information partition. Chance probabilities and terminal utilities may vary by model. Every information set belongs to exactly one player; its nodes have the same action menu. The partition has perfect recall: the sequence of that player's earlier information sets and chosen actions is identical at every node of the set. No information set recurs along a path.

One behavioral profile sigma maps each information set to an action distribution and is **identical across models**. It cannot use hidden model identities or hidden nodes within an information set. Utilities and probabilities are rational in the executable profile; the mathematical finite-sum statements also hold over real inputs.

For each model m and information set I, an assessment mu[m,I] is a probability distribution over its nodes. If I has positive reach under sigma and m, mu must equal normalized reach probabilities. If I has zero reach, a distribution is explicitly supplied and the result remains conditional on it. There is no fabricated conditioning on a zero event. These off-path distributions may fail stronger equilibrium refinements: that is unsupported, not silently certified.

A continuation deviation tau for player i assigns actions to all of i's information sets in the union of subtrees rooted at I. Assignments are shared across nodes in the same information set, including nodes of zero assessed probability. Opponents retain sigma. The model m remains fixed. Let V(m,I,tau;sigma) be conditional expected terminal utility from mu[m,I], replacing only i's continuation by tau. Let V(m,I,sigma) be the proposed value.

Define D(m,I) = max_tau [V(m,I,tau;sigma)-V(m,I,sigma)] and D* = max over m,I D(m,I). The nonnegative tolerance epsilon is expressed in utility units. A result requires D* <= epsilon. It is a simultaneous statement at all declared information sets, including off-path sets, not a sum of local errors or merely a root test. The utility scales are supplied; comparing a common epsilon across players presupposes those declared scales, not interpersonal welfare comparability.

Participation is separate. The fixture reports A's value at its initial private-type decision and B's root value against supplied zero outside options. These are conditional and ex-ante participation views respectively, not universal participation semantics.

## 4. Finite exact soundness

**Proposition 1 (pure continuation sufficiency).** For fixed m,I,sigma,mu, maximizing over deterministic continuation plans attains the maximum over independently randomized behavioral continuations, and bounds mixtures of deterministic continuation plans.

**Proof.** Enumerate the finite set J of deviator information sets below I. Each path uses each J at most once. Expand the product of behavioral action probabilities by drawing one action independently for every J before play. Each complete draw is a legal deterministic plan, with nonnegative weight equal to the product of the draw probabilities; these weights sum to one. Summing terminal probabilities gives exactly the original behavioral value. The value is therefore a convex combination of deterministic-plan values and cannot exceed their maximum. A deterministic plan is a behavioral special case. Mixtures of plans have the same linear bound. Perfect recall ensures the declared continuation interpretation retains the player's own past information and actions. No ambiguous-preference equivalence is claimed. QED.

**Proposition 2 (exact conditional criterion).** For the declared finite subject, exhaustive evaluation of every legal deterministic continuation at every m,I returns D* exactly. D* <= epsilon if and only if every supported continuation gain is at most epsilon.

**Proof.** Each evaluation is a finite sum of products of exact probabilities and utilities starting at the declared assessment. Proposition 1 covers the randomized comparison class. Taking finite maxima is equivalent to the universal inequalities. A maximizing m,I,plan witnesses failure if its gain exceeds epsilon. The profile itself is a mixture of deterministic continuations, so the maximum gain is nonnegative. No interchange of min and expectation, no new adversary choice, and no equilibrium-selection operation occurs. QED.

These are assessment-relative sequential rationality statements, not proof that the assessments can arise together as limits of completely mixed profiles. On-path Bayes checks alone are insufficient for that latter conclusion.

## 5. Representation and mechanism transfer

**Proposition 3 (payoff-error transfer).** Suppose a specified representation maps the proposed continuation and every original legal deviation to represented continuations, with the same actor information restrictions. Suppose for each original m,I the proposed value and every corresponding deviating value differ by at most delta. If every represented deviation gain is <= epsilon, every original deviation gain is <= epsilon+2 delta.

**Proof.** For each original deviation, write its gain as the represented gain plus the deviating-value error minus the proposed-value error. Bound each error by delta. Take the maximum over all original deviations. Coverage of *all original deviations* is necessary: no conclusion follows if the reduction deletes a profitable action. The reverse direction requires corresponding coverage in the other direction. QED.

A bijective renaming of node/information-set identifiers preserving edges, players, probabilities, assessments, action menus and utilities is an exact delta=0 special case. The reference checks this special case and a terminal-payoff perturbation case. It does not implement general history compression. Dropping evidence from B's information can merge nodes where the supplied profile prescribes different actions, so even profile implementability can fail.

**Corollary (composing proved transfers).** If successive transfers satisfy Proposition 3 with error budgets delta_1,...,delta_k and deviation coverage at every step, the forward bound is epsilon+2 sum_j delta_j. This concerns transfer error, not automatic composition of arbitrary economic mechanisms.

**Proposition 4 (model restriction).** For a nonempty subfamily M' subset M with all retained game/assessment/profile data fixed, D*(M') <= D*(M). This is immediate from taking a maximum over fewer entries. It does not imply that strategic public disclosure improves credibility: disclosure can change strategies, beliefs, or information sets rather than merely restrict the analyst's family.

Changing a bond, fee, monitor, disclosure rule, payoff, assessment, or profile changes the subject and requires fresh checking unless a transfer warrant has actually been established. A content hash detects changes; it does not itself prove preservation.

## 6. Continuous bridge: analytic only, not a generic imported corner certificate

**Proposition 5 (on-path unnormalized corner criterion).** Let parameters range over a rectangle, with fixed tree and profile. Suppose, for every I and pure continuation tau, the information-set reach R_I(q), and the unnormalized continuation totals N_tau(q) and N_sigma(q) obtained using proposed-profile prefix reaches, are multi-affine. Suppose R_I(q)>0 throughout the rectangle. Then the uniform conditional gain bound <= epsilon is equivalent to the corner inequalities N_tau(q)-N_sigma(q)-epsilon R_I(q)<=0 for all tau.

**Proof.** On-path Bayes conditioning gives gain = (N_tau-N_sigma)/R_I. Multiply by the strictly positive denominator. The resulting expression is multi-affine, hence a convex combination of its corner values by repeated affine interpolation. Checking all corners is necessary and sufficient. QED.

This statement avoids assuming that a ratio of multi-affine polynomials is itself multi-affine. It does not cover zero-reach information sets with free off-path assessments, parameter-dependent strategies, endogenous equilibrium selection, or repeated-parameter products violating the hypotheses. There is no automatic reuse of PR #21, and no claim that its causal fibre identifies strategic behavior.

Failure control: f(q)=q(1-q) is zero at both endpoints but positive inside. Reusing one parameter twice can invalidate corner sufficiency. For the fixture's compliance incentive g-pb, the rectangle bound is separately affine and holds continuously by direct algebra; the generic executable checker's subject remains the supplied finite family.

## 7. Integrated fixture and predictions to check

Nature privately reveals quality good/bad to A with probabilities 1/2 each. A can disclose its true quality (hard evidence) or withhold (N); it cannot submit the other type's evidence. A then chooses bond 0 or b. B observes message and bond, not undisclosed quality, and accepts or rejects. After acceptance A complies or defects. Defection is caught with probability p; the bond is forfeited only then. The bond is refunded otherwise. A pays liquidity cost b/10 when posted, including on rejection. A's compliance payoff before liquidity cost and any acceptance fee is 2; defection adds g. B receives 2 from good compliance, -1 from bad compliance, -2 from defection, and 0 from rejection. Forfeitures leave the game rather than going to B. These are stipulated game payoffs, not empirically identified causal effects.

Proposed profile: reveal quality; post b only after message G and otherwise post zero; B accepts only G with bond; A complies with bond and defects without it. After withheld evidence B's off-path assessment puts probability one on bad quality. At other multi-node information sets use Bayes if reached and explicitly declared beliefs otherwise. A remembers quality and its earlier actions.

For g in {1,3}, p in {1/2,1}, b=6 and no acceptance fee, compliance gain from defection is g-6p<=0. Good A gets 7/5, bad A gets 0, and B's root value is 1. Every information set must nevertheless be checked: this scalar observation does not by itself certify the entire profile.

Controls to execute: bond 5 gives a deviation gain 1/2 at g=3,p=1/2; fee 3/2 with bond 6 makes accepted compliance worth -1/10 to good A, so rejection is preferred despite deterrence; prescribing compliance without bond creates a profitable continuation deviation; claiming no risk only because a node is off path is invalid; merging B's distinct evidence information sets can make the proposed strategy impossible to implement.

Further scalar controls: with action payoffs L=(1,0), R=(0,1) across two models, mixing each with probability 1/2 is maxmin optimal but has modelwise deviation gain 1/2. In a one-player two-stage tree, Stay pays 0, Enter then Exit pays -1, and Enter then Take pays 1: a root-only one-step check misses the profitable full continuation Enter/Take. In an entry game an unreached costly punishment can be a root-Nash threat but fail sequential rationality.

## 8. Provenance, assurance and next gate

The certificate binds the full subject, epsilon, assessment semantics, and all information-set bounds. The receiver recomputes those bounds by explicit terminal-path evaluation rather than trusting the producer's recursive evaluator. Structural validation and exact arithmetic are shared trusted infrastructure; this is implementation diversity, not independent formal verification. Exact schema/support/recall/Bayes checks precede either evaluator. Deliberate mutations must be rejected without relying on Python assert statements. A separate receiver process must work with the producer unavailable.

Existing tracked files except living steering documents remain byte-identical to the base. No Writ/Decision Lab edits, branch creation, merge, or modification of the causal task occur. Source-bound evidence and a local publication bundle make this package reviewable without appending it to someone else's open PR.

The next gate, if this component survives review, is not a larger fixture: it is a checked off-path consistency warrant or a restricted continuous on-path family warrant under Proposition 5. Mechanism search and strategic-causal identification are later distinct operations. General coalition deviations, learning dynamics, mechanism optimality, formal Lean proofs, external-solver integration, and empirical validation remain unsupported.
