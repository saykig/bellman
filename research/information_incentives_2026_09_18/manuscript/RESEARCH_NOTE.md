# Compatible information, exact enforcement, and voluntary disclosure

Research note — 18 September 2026. Analytical results and reproducible experiments;
not peer-reviewed, empirically validated, or a claim of historical novelty.

## What was established

We obtained an exact solution to the previously open **positive-tolerance version
of the two-active-component benchmark**: the worst expected benefit from changing
either or both actions is the maximum of six explicitly evaluated entropy-support
branches. Each branch uses one admissible joint law. Adding separately optimized
policy and operational gains can give a strictly excessive answer.

A broader composition result explains what must be retained: for each observable
message probability, keep its **minimum information cost**, and impose the same
budget across states. These functions recover the exact likelihood feasibility
set. On a junction tree with a compatible Markov reference, augmented local tables
and clique-minus-separator KL recover those cost functions exactly. This is a
specialization of established probability gluing and I-projection machinery.

The voluntary-disclosure extension exposes a second compatibility problem. A
certificate can make policy disagreement unavoidable unless enforcement covers
the complete-information temptation. With partial certificates, even separately
credible deterrents may fail: one common disclosed message must produce one
continuation that deters every eligible sender type. A three-type example proves
an exact failure of separate payoff bounds and a sharp disclosure-cost repair.

## The controlled benchmark, in plain language

Two players agree on a common policy R and an operational action T. Their preferred
policies oppose each other, depending on a hidden state θ. Coordination has value,
so neither needs to know θ to accept R. Operations are different: T must respond
well enough to an operational condition S. Too much noise can make T unattractive;
too revealing a connection between the sources can undermine policy cooperation.

The institution controls a noisy public channel from S to T and a credible fine
for departing from R. It cannot tailor either to the analyst's unknown actual
source law. Players know that law and update from their observed R,T. The analyst
knows two marginal tables and a shared dependence budget κ. The budget is measured
in nats; a fine is measured in utility units. Neither measures welfare directly.

The original binary law has only two free coefficients:

    Q(θ,r,s) = [1+u rs+v θrs]/8,
    C(u,v) = [F(u+v)+F(u−v)]/2 ≤ κ,
    F(z) = [(1+z)log(1+z)+(1−z)log(1−z)]/2.

The gate is Pr(T=t|S=s)=(1+γst)/2. Higher γ means a more accurate report.
The policy payoff has coordination benefit c, state preference b, and departure
penalty e; operations have coordination benefit L and state matching benefit w.
Here 0<c<b and 0≤L<w, making operations genuinely incentive-sensitive.
The complete payoffs, information interfaces and assumptions are in
[BINARY_FRONTIER.md](../math/BINARY_FRONTIER.md).

## An exact solution, not just a numerical optimum

Let d=c+e. On the symmetry-reduced region u,v≥0, define

    P0=0,
    P1=(bγv+dγu−d)/4,
    P2=(bγv−d)/2,
    O =(u(w+Lγ)−L−wγ)/2.

For one player under one law, expected optimal deviation gain is

    max{P0,P1,P2} + max{0,O}.

Thus the worst value equals the largest of the six maxima of Pj+kO over C≤κ,
with j=0,1,2 and k=0,1. Each is a constant plus a support function Sκ(A,B), whose
attaining law and scalar log-cosh dual are explicit in **Theorem E**. Its proof
starts from the actual payoff differences at all four observations, combines the
available deviations under the same law, and then solves each affine branch.

This resolves a specific unfinished problem in the supplied note. The technique
of expanding a finite maximum and using convex conjugacy is established; the
contribution earned here is the exact active-component formula and its failure
boundaries. It is not a general efficient algorithm for arbitrary games.

One strict counterexample uses κ=F(4/5), γ=7/10, b=2,c=1,L=1/10,w=1,e=0.
Operations are most vulnerable uniquely at u=4/5,v=0, where policy vulnerability
is zero. A different feasible law makes policy vulnerability positive. Compactness
therefore proves that adding the two separate maxima is strictly excessive.
Evaluating the exact formula gives approximately **0.060 jointly versus 0.088
by adding the separate maxima**. The strict inequality is analytically proved;
these decimals are floating evaluations, not a substitute for that proof.

For exact obedience, both components must have zero gain. Different worst-case
laws for different inequalities are legitimate: both inequalities must hold for
every law. The composition error occurs when incompatible choices are joined
inside an incentive numerator or an expected-gain sum. This distinction prevents
an overbroad rejection of the supplied exact-zero-tolerance result.

## What probability bounds forget, and the sufficient replacement

For a message y and payoff state z, let a_z be the probability of that message.
Statewise bounds retain a range [L_z,U_z]. The tempting calculation makes the
message as common as possible where deviation helps and as rare as possible
where deviation hurts. Each endpoint may be attainable alone, while their
combination costs more information than allowed.

Define J_zy(a) as the smallest KL cost of a source distribution with that message
probability and the required local marginals. **Theorem A** proves exactly

    jointly attainable a  iff  Σ_z p_z J_zy(a_z)≤κ.

This constructive statement eliminates unused source coordinates without losing
the coupling relevant to one incentive inequality. **Theorem B** gives a sharp
criterion: the separate bounds compose exactly for a specified payoff direction
iff its selected endpoint face intersects this shared-budget set. Equivalently,
the cheapest simultaneous endpoint selection must fit the budget. **Theorem C**
gives the dual and a conservative error bound when an outer model's excess
information cost and a positive observation-mass floor are known.

These results allow arbitrary finite alphabets and asymmetric marginals. They
require that the shared separable KL budget is the only cross-state restriction.
One cannot silently discard other common-source or causal constraints. Expected
vulnerability across multiple messages needs their joint probability vector;
separate single-message profiles generally do not suffice.

**Theorem D** computes the needed minimum costs using transcript flags on a
junction tree. Its proof uses the KL identity

    D(Q||reference) = D(Q||Markov extension of retained tables)
                     + D(Markov extension||reference).

Retain augmented clique and separator tables, including which transcript occurred.
Their KL expression is exact. Keeping only the original clique divergences is
insufficient: with fixed clique marginals those numbers can all be zero even
when the full dependence cost is positive. These are direct uses of
[junction-tree consistency](https://people.eecs.berkeley.edu/~jordan/sail/readings/wainwright-jordan-fnt.pdf)
and [I-projection geometry](https://www.renyi.hu/~csiszar/Publications/Information_Theory_and_Statistics:_A_Tutorial.pdf),
with a proof of the event-specific specialization in
[COMPOSITION.md](../math/COMPOSITION.md).

## Discriminating computations

| Calculation | Full admissible model | Separate statewise bounds | Shared-cost profiles |
|---|---:|---:|---:|
| Policy fine, κ=.2 and γ=.8 (audit regression) | .08042888249 | .32485021344 | .08042888249 |
| Best γ with BOTH components obedient, κ=.3, L/w=.1, quality floor .6 | .68287061666 | .95434855115 | .68287061666 |
| Minimum fine at each model's best γ in that active design | .09017922558 | .83710789829 | .09017922558 |
| Hidden-separator example, shared KL budget .15 | .02351047748 | .20000000000 | .02351047748 |

The first row's box extremizer costs .4 nats against a .2 budget. The active-design
rows optimize each model's feasible channel: the box also makes the operational
lower bound too severe. A policy fine calculated at the full model's γ would
not repair the box's operational failure, because that fine does not penalize
operational deviations.

The hidden-separator test extends the supplied H–X/H–Y example: H is fair,
Pr(X=0|H) is .7 or .3, and Pr(Y=0|H)=.5. Marginals are fixed in each payoff state.
The reference makes X,Y conditionally independent given H; admissible laws need
not. Full 16-cell optimization, four coupling coordinates with a common KL budget,
and independently reconstructed likelihood cost profiles agree. The separate
bound extremizer costs about .27436, above .15. This test isolates the probability
bridge; the preceding binary design is where the active operational incentive is
imposed.

The calculations include 600 conditional-player aggregate payoff checks over
300 signed/asymmetric parameter cases, independent original eight-cell support
optimizations, and 50 nonbinary 2×3×3 checks of the augmented-tree KL identity.
Primal laws, costs, marginal residuals, support upper bounds and source hashes are
saved in [experiments](../experiments/README.md). Floating residuals were around
10⁻¹³ or smaller in the independent optimizations and around 10⁻¹⁶ for the payoff
and tree identities. These are numerical checks of proved formulas, not formal
verification or empirical evidence.

A new [Lean verification](../lean/README.md) checks the real-number six-branch
maximum identity and the partial-certificate threshold and obstruction, with no
admitted proofs. It does not formalize entropy duality, Bayesian updating, or the
whole strategic theorem. This is new, narrowly scoped verification rather than
reuse of the supplied audit's older success log.

There is also a wholly analytic local-bound counterexample at κ=F(1/2)/2:

    1/30 ≤ required fine in the full model < 3/10 = box fine.

Its feasible witness, infeasible box witness, and strictness proof do not depend
on rounding or an optimizer. The independently evaluated full fine is about .09510.

## The information arrangement must itself survive incentives

Add an advocate who privately knows θ from an authenticated record, sees public
R,T, and values player 1 choosing θ. The advocate can send a public truthful
certificate or remain silent before action; cannot fabricate the other state;
and cannot commit to conceal evidence. Neither action player initially knows θ.
The gate and policy fine remain committed. Disclosure costs k and correct policy
is worth η>0 to the advocate. This is genuine voluntary disclosure of additional
information, not a new name for T.

**Theorem F** first solves disclosure at fixed enforcement. If e<b−c, a certificate
makes the policy continuation uniquely (θ,−θ). Whenever θ≠R, revealing gives the
advocate benefit η instead of zero. Consequently, conditional on controlled
obedience, a pooling equilibrium preserving the agreement exists exactly when

    e≥b−c  or  k≥η.

Combining with Stage 1 gives the exact pooling enforcement frontier:

    E_vol(k)=b−c for k<η;  E_vol(k)=E_controlled for k≥η.

Thus costless disclosure raises the active benchmark's fine from approximately
.09018 to **1**. At the boundaries silence or compliance can be weakly optimal;
this is existence of an equilibrium, not uniqueness or a prediction of selection.
The result concerns the prescribed arrangement on path; requiring operations
also to remain unchanged after an off-path certificate adds another information
constraint, stated in [DISCLOSURE.md](../math/DISCLOSURE.md).

We then removed the binary full-certificate simplification. **Theorem G** gives a
finite one-sender criterion: each partial certificate needs one credible posterior
and continuation whose entire sender-type payoff vector deters all eligible types.
A shared tremble construction checks consistency of those beliefs.

A three-type example proves why separate deterrence bounds fail. Pooling pays
both potentially disclosing types 1/5. After their shared partial certificate,
credible continuation payoff vectors are (q,1−q), 0≤q≤1. Each type separately has
a credible minimum payoff of zero. But deterring both requires q−k≤1/5 and
1−q−k≤1/5. Therefore **pooling is impossible for k<3/10 and possible at k=3/10**.
The proof is addition of the two inequalities plus an attaining mixed continuation.
It is a sharp nonbinary counterexample, with an exact rational certificate.

## Position relative to existing results

[Dobra–Fienberg](https://sites.stat.washington.edu/adobra/Files/Papers/pnas.pdf)
already gives the decomposable marginal cell bounds. It supplies the probability
baseline, not permission to select all extremes under one information budget.
[Linked-game BCE](https://benjaminbrooks.net/downloads/bbm_counterfactuals.pdf)
and [seed/spillover theory](https://www.jperego.com/files/papers/GP/draft.pdf)
already characterize important forms of common-information feasibility. We ask
for a fixed arrangement's exact robust enforcement under additional quantitative
restrictions, rather than propose another general equilibrium concept.

[Saas's disclosure-proof CE](https://eller.arizona.edu/sites/default/files/2025-10/Disclosure_Proof_Correlated_Equilibria-8.pdf)
is the closest direct robustness comparison, but its signals are payoff-irrelevant
recommendations. Our advocate verifies a payoff state. General
[certification equilibria](https://www.sciencedirect.com/science/article/pii/S0304406804000874)
and [certifiable pre-play communication](https://edurichet.github.io/papers/HardInfoV13.pdf)
are closer foundations for the partial-certificate extension. We do not claim that
our pooling criterion is a new general characterization; full subsumption against
the inaccessible Forges–Koessler PDF remains a literature task.

[Bayesian persuasion](https://web.stanford.edu/~gentzkow/research/BayesianPersuasion.pdf)
provides the committed benchmark, while voluntary evidence requires interim
sender incentives. [Endogenous acquisition](https://onlinelibrary.wiley.com/doi/10.3982/TE4541)
adds a different choice—what to learn—which our model does not contain.
The [source notes](../sources/NOTES.md) give inspected locations, exact borrowed
claims and access limits. None of these comparisons proves novelty.

## Recommendation and next theorem

Keep this programme: the disclosure extension strengthens it. The useful common
question is **which jointly feasible objects must survive composition**. For
controlled information, retain attainable likelihood vectors or their exact
minimum-cost profiles. For strategic disclosure, retain credible continuation
payoff vectors shared by all types capable of sending the same certificate.
A single information scalar or a collection of best/worst payoffs is insufficient.

The tractable paper question is now: *How do shared information budgets and
shared certificate continuations constrain exact cooperation guarantees?*
The current contribution can be a rigorous solved benchmark plus exact composition
and impossibility results; a new foundational language is unnecessary.

The next theorem to attack is a **robust partial-certificate frontier**: combine
the shared-budget likelihood profiles with the jointly feasible continuation set
of Theorem G, for a finite three-state extension of the active two-component game.
Start with one sender and one overlapping partial certificate. Determine when a
single policy fine and gate support pooling for every admissible source law, and
whether the continuation constraints admit a useful convex representation or a
sharp nonconvexity obstruction. Do not replace the common continuation by separate
typewise minima. This target is not claimed solved by this run.

For Bellman, these results suggest mathematical interfaces, not an architecture
rewrite: retain common laws or exact query-preserving projections, declare the
players' observations, and bind incentive claims to the gate, sanctions, evidence
menu and solution concept. Remaining obstacles are scalability, multiple senders,
private receiver signals, stronger consistency restrictions, strategic acquisition,
and empirically warranted primitives. No production implementation or publication
readiness follows from this research reference.
