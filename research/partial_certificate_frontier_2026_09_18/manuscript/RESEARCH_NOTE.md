# What must survive when information and incentives are connected?

18 September 2026 · Bounded mathematical research note · No novelty claim

Bellman should retain **joint feasible sets at the interfaces used by subsequent
questions**. For upper-bound resource and incentive questions, a particularly
useful summary is the set of budgets that one common witness can meet. This
answers the question raised by the earlier controlled-information and disclosure
examples, but it does not call for a new universal foundation. Value functions,
set optimization, valuation algebra and signaling theory already supply most of
the mathematics. The substantive work is to identify the right witness, retained
interface and permitted future queries—and to prove that a proposed reduction
preserves them.

This note first solves a three-state partial-certificate model, then isolates the
assumptions behind that recommendation. [Full definitions and proofs](../math/FRONTIER.md),
[cost-profile analysis](../math/PROFILES.md), [composition theorem](../math/COMPOSITION.md)
and [primary-source audit](../sources/AUDIT.md) are separate companions. Earlier
research artifacts remain unchanged.

## A solved model with both incentives active

There are three possible states. Two action players are supposed to coordinate
on policy C and follow a noisy source recommendation T in an operational task.
States 1 and 2 pull their policy preferences in opposite directions; state 3
makes C attractive to both. Coordination has value c, matching a preferred policy
has value b, and departing from C incurs a committed fine e. The operational
payoff separately rewards matching the source and coordinating with the other
player. Thus making the source useless can itself destroy obedience.

The analyst knows two uniform conditional source marginals, but not their
correlations x₁,x₂,x₃ in the three states. One weighted information budget limits
those correlations together. A committed symmetric binary gate has accuracy
(1+γ)/2. Players know the actual law, although the analyst must choose one gate
and fine that work throughout the family. This distinction is an assumption,
not a claim that people can learn the true law from these observations.

A third-party advocate privately knows the state. In states 1 and 2 it can show
the SAME authentic certificate saying “the state is either 1 or 2.” In state 3
it cannot. The advocate prefers player 1 to choose A in state 1 and B in state 2;
either preferred result pays η, the other pays zero, and C pays v, with 0<v<η/2.
Disclosure costs k. There is no commitment to withhold the certificate.

We ask for existence of a pooling equilibrium: the advocate stays silent and
both players follow the target. This is a guarantee of equilibrium existence,
with favorable selection when players are indifferent. It does not guarantee
that all equilibria cooperate or that silence is uniquely optimal.

With prior (1/4,1/4,1/2), write

\[
F(x)=\tfrac12[(1+x)\log(1+x)+(1-x)\log(1-x)],\qquad
\sum_zp_z F(x_z)\leq\kappa.
\]

The controlled-information fine E_ctl is computed exactly from the support
function of this shared-budget set. A scalar equation, supplied with an attaining
witness in Theorem 1's derivation, evaluates it; independently optimized source
intervals do not suffice. Operational obedience places a lower bound on γ.
Within the specified symmetric binary gate family, the smallest allowed γ gives
the smallest controlled fine.

For any γ<1, both certificate-eligible types remain possible after every public
observation. The exact robust disclosure frontier is

\[
E_{\rm vol}(\kappa,\gamma,k)=
\begin{cases}
E_{\rm ctl}(\kappa,\gamma),&k\geq\eta/2-v,\\
\max\{E_{\rm ctl}(\kappa,\gamma),\ b/2-c\},&k<\eta/2-v.
\end{cases}
\]

Why? Below fine b/2−c, C is never a best response after the certificate. If player
1 chooses A with probability q, the two types receive ηq and η(1−q). One common
continuation must deter both, so their inequalities add to k≥η/2−v. At equality,
a common half-and-half continuation works. Above fine b/2−c, policy (C,C) itself
is credible under the equal posterior and makes disclosure unprofitable. This
proves necessity and supplies an equilibrium construction.

For κ=.3, b=2, c=.2, operational coordination L=.1, source-matching value w=1,
quality floor .6, η=1 and v=.2, the optimum in the chosen gate family is:

| Setting | Gate γ | Minimum policy fine |
|---|---:|---:|
| Controlled information | ≈.68287062 | ≈.22436269 |
| Partial certificate, k<.3 | ≈.68287062 | .8 |
| Partial certificate, k≥.3 | ≈.68287062 | ≈.22436269 |

The decimal values are numerical evaluations of the proved formula. Both policy
and operational incentives matter: reducing the selected gate or controlled fine
produces explicit profitable deviations.

A perfectly revealing gate has a sharper failure. At γ=1 and κ≥(log 2)/4, an
allowed source law makes type 1 impossible at a public history while type 2 remains
possible. The same certificate then identifies type 2 completely. It demands
k≥η−v or the larger fine b−c. For the example at k=.4, the fine tends to about
.94068 as γ approaches 1 from below, then jumps to 1.8 at γ=1. This is a support
change, not a computational approximation: an impossible type cannot supply an
off-path threat. Arbitrarily assigning it posterior weight would change the model.

This is also an intervention calculation. Replacing the source mechanism by
γ* changes the observation likelihood from (1+h x_z)/4 at the perfect gate to
(1+γ*h x_z)/4. The latter is positive for every type. By contrast, raising e or
k changes continuation incentives without replacing that observation mechanism.
These operations have different interfaces and different guarantees.

## KL is useful, but not essential

Let component i have internal choices x_i, retained output a_i=f_i(x_i), and
cost c_i(x_i). Suppose its cheapest cost at each attainable a_i is achieved, and
choices in different components are independent except for one shared budget.
Then the outputs are jointly attainable exactly when

\[
\sum_i w_i J_i(a_i)\leq\kappa,\qquad
J_i(a_i)=\min_{f_i(x_i)=a_i}c_i(x_i).
\]

The proof simply selects all the cheapest witnesses. It uses neither KL nor
convexity. Convexity helps solve the optimization; it does not establish the
underlying compatibility. This is established partial-minimization mathematics.
[Boyd–Vandenberghe, slide 3.23](https://stanford.edu/~boyd/cvxbook/bv_cvxslides.pdf)

The companion records sharp failures: an unattained infimum can falsely certify
the boundary budget; a hidden equality between components invalidates independent
selection; an exact-cost question cannot use a minimum alone; several resource
coordinates need a joint cost set. A shared interface may repair a failed product
assumption, but it must be retained until its last use.

The same source family admits exact profiles for KL, total variation and χ².
Their computational shortcuts differ. For two binary variables with fixed means
1/4, the independent glue has χ² cost 33/256, while a dependent law with the same
marginals has the smaller, optimal cost 32/256. Therefore the earlier KL-specific
Markov-gluing minimizer does not transfer to χ². The profile theorem survives;
the proposed method of computing it fails.

## The common theorem, with its limits

At a retained interface u, let K(u) be the vectors obtainable from one valid
component witness. Define

\[
B(u)=\{b:\text{some }r\in K(u)\text{ satisfies }r\leq b\}.
\]

This is the full set of simultaneous upper bounds the component can meet.
Two components answer all such threshold questions alike exactly when their
B(u) agree. If their witnesses are independently selectable at the SAME u and
their resources add, their budget sets combine by Minkowski addition. Hiding u
then takes a union over its possible values. Theorem 4 proves these identities
without closing or convexifying the sets. They specialize established upper-set
and valuation operations. [Hamel et al., §2](https://arxiv.org/pdf/1404.5928),
[Kohlas–Wilson, §§2–3](https://cora.ucc.ie/bitstreams/f41f5bb0-d690-4690-89a4-a9164f4cc832/download)

For controlled information, the retained interface is the likelihood vector and
the resource is the cost of a compatible law. The budget selects feasible
likelihood vectors, after which obedience is checked against ALL of them. For
disclosure, the witness is one credible continuation and its vector records gains
for ALL types sharing the certificate. The question asks whether SOME common
continuation meets all bounds. These quantifiers differ; the theorem does not
exchange them.

In particular, support functions can lose too much at the strategic layer.
A two-receiver coordination game has credible sender-payoff vectors exactly
(1,0), (0,1) and (3/4,3/4). None meets bounds (1/2,1/2), although their convex hull
does. A support-only description preserves the convex hull and therefore gives
a false positive. An added public lottery could make the missing point available,
but its timing and availability change the game.

The harder prior-art audit changes how this work should be presented. The
one-sender joint-payoff condition is already part of the signaling framework in
[Koessler–Laclau–Tomala, §§3 and 7](https://drive.google.com/file/d/1tOPbqJrWtDDtZNMC5fBfp4k2UjL8kwIe/view).
[Koessler–Skreta, Definition 6 and Theorem 1](https://drive.google.com/file/d/1LDie6EXqrksQYja4fM5eLVg2T7OGNcpn/view)
also retains one common continuation-payoff vector and consistent beliefs. The
bounded frontier is useful as a solved example; the broad conceptual bridge is
not a defensible novelty claim on current evidence.

## Implications, obstacles and the next experiment

For Bellman, use established game and causal semantics to define valid witnesses;
use relational compatibility, cost profiles and set-valued elimination to retain
what the specified next question needs. A marginal law, scalar endpoint, cheapest
cost or individual punishment has no automatic right to substitute for a joint
witness. General strategic or causal composition still requires its own semantic
premises. No new universal algebra or engineering migration is needed here.

After solving the frontier and composition result, a bounded network extension
follows by ordinary elimination with complete shared interfaces. Multiple senders
present a new obstruction: two independently randomized senders with independent
types generate a rank-one posterior likelihood matrix at a joint message. Uniform
marginals alone cannot justify a posterior concentrated equally on the two diagonal
states. The companion proves that obstruction; it does not claim a general
multiple-sender frontier.

The tractable paper question is: **which support and continuation-equilibrium
boundaries govern discontinuities of the minimum robust fine in finite public
certificate games with a shared convex information budget?** Existing mathematics
is the starting point, and novelty remains unproved.

The next experiment should break the convenient symmetry while keeping three
states and one sender: use an asymmetric prior and two overlapping certificates
{1,2} and {2,3}, retaining one continuation per observed certificate and the true
support at each history. Enumerate continuation equilibria by supports and compare
the resulting fine frontier with the joint-budget calculation. Test first whether
new jumps come from source support or equilibrium feasibility. Do not add networks
until that distinction is resolved.

The present evidence comprises written proofs, 36 direct probability-table
optimization comparisons, rational counterexamples, payoff enumeration and six
narrow Lean lemmas. Numerical agreement is not formal verification. Lean does
not cover the full equilibrium or entropy proof. Empirical warrant, stronger
equilibrium refinements, unknown-law players, acquisition choices and scalability
remain outside the results.
