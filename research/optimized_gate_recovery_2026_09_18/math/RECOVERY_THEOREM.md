# The exact recovery boundary for optimized robust enforcement

## R1. General finite-game design formulation

Let lambda range over a metric parameter space. A design is z=(g,e) in a fixed
compact gate space K times [0,H]. G(lambda) is a nonempty compact gate set with
closed graph. X(lambda,g) is the nonempty compact admissible-law set, in a common
compact finite-dimensional space of joint probability tables.

Let W(lambda,g,e,q) be the set of COMPLETE feasible continuation witnesses for
law q. A witness encodes all histories, all certificate beliefs, receiver strategies,
shared consistency restrictions and sender inequalities. It includes on-path
target optimality. The ambient witness space Z is compact and fixed. W can be
empty, but its graph is closed. Finitely many simultaneous incentive and Nash
inequalities with continuous payoffs have this property; any stronger consistency
restriction must be verified separately. Do not assume it from the word PBE.

Define

    F(lambda)={(g,e): g in G(lambda),
                         for every q in X(lambda,g), W(lambda,g,e,q) nonempty},
    V(lambda)=min{e:(g,e) in F(lambda)}.

Assume F is nonempty locally. There is one institution design for all laws, with
a law-dependent COMPLETE witness when the law is known to the players. This is
not an unknown-law common strategy. Encode any common-witness requirement inside
W, not by silently changing these quantifiers.

Assume X is lower hemicontinuous on the admissible (lambda,g) graph. This means
that along lambda_n->lambda, g_n->g with g_n admissible, every q in X(lambda,g)
can be approximated by q_n in X(lambda_n,g_n).

**Closedness lemma.** F has closed graph and compact values. Therefore its
minimum is attained and V is lower semicontinuous.

Proof. Given feasible (g_n,e_n)->(g,e), closedness of G gives admissibility of g.
For EACH q in X(lambda,g), choose approximating q_n by lower continuity. Select
w_n in W(lambda_n,g_n,e_n,q_n). A subsequence converges in compact Z and closedness
of W supplies a witness at (lambda,g,e,q). The subsequence can depend on q:
we need existence for each q, not one witness for all q. Thus (g,e) is feasible.
Compactness follows. Apply this argument to converging minimizing designs along
a subsequence realizing liminf V. A strictly smaller limit would contradict
optimality at lambda. QED.

This proof requires neither lower continuity of every equilibrium nor a continuous
equilibrium selector. The lower continuity of X prevents a new unapproximable law
from appearing in the universal constraint at the limit. It has the opposite
quantifier role from recovering witnesses at nearby laws.

## R2. Necessary and sufficient optimized recovery

Under R1, V is continuous at lambda0 if and only if:

    For every epsilon>0 there is a neighborhood U of lambda0 such that
    for every lambda in U there exists ONE admissible pair (g,e),
    e < V(lambda0)+epsilon, for which
    for every q in X(lambda,g) there exists w in W(lambda,g,e,q).       (UR)

Proof. (UR) gives limsup V(lambda)<=V(lambda0). R1 gives the reverse liminf
inequality. Conversely continuity and attained minimizing designs imply (UR).
QED. Equivalently, every sequence approaching lambda0 admits feasible designs
whose fines have limsup at most V(lambda0). The gates and witnesses need not
converge to a preselected optimizer. This is a VALUE recovery condition.

This is the exact boundary, conditional on R1, not a new theorem in optimization:
it is the feasible-path-transfer principle specialized to this robust design query.
Gate optimization can repair a lost witness only if some alternative design meets
(UR). Availability of one noisy informative gate places no such restriction.

A discontinuity in R1 can only be a failure of upper semicontinuity: a low value
at the limit cannot be recovered nearby. The counterexample has precisely this
shape. If R1 fails (support loss, nonclosed equilibrium restrictions, noncompact
design menus, unbounded fines or abrupt law admission), this directional conclusion
need not hold and a separate argument is required.

## R3. Primitive sufficient recovery by local strict branches

Here is a useful stronger condition without assuming continuity of the value or
of the full equilibrium correspondence. For each epsilon>0, suppose there exist
an e_epsilon<V(lambda0)+epsilon and a continuous admissible gate choice g(lambda)
near lambda0. Suppose X is also upper hemicontinuous there. For every
q0 in X(lambda0,g(lambda0)), there is a local continuous specification of admissible
beliefs and a pure receiver continuation profile (for all needed histories), such
that at (lambda0,g(lambda0),e_epsilon,q0):

1. all receiver best-response inequalities for prescribed actions have strict
   margins; with a finite continuation game this is a strict pure equilibrium;
2. all nontrivial sender deviations have strict negative gains;
3. all on-path target constraints have strict slack;
4. identities or inequalities declared structurally nonpositive are verified to
   remain so in that whole neighborhood, rather than treated as strictly slack;
5. beliefs and any cross-history consistency restrictions remain admissible in
   that neighborhood. For pinned Bayesian beliefs, positive denominators and
   continuous cells suffice for belief continuity; free beliefs require a valid
   common tremble construction. Do not infer consistency from Nash inequalities.

Strict finite inequalities and continuity preserve these witnesses on an open
neighborhood of each q0 and lambda0, using the same e_epsilon and gate choice.
Compactness of X(lambda0,g(lambda0)) gives a FINITE subcover. Shrink the parameter
neighborhood so all its patches remain valid; upper continuity of X then puts
ALL nearby admissible laws in their union. Choose the applicable complete witness
for each known law. This proves (UR), hence continuity.

This finite-cover argument upgrades local branch evidence into uniform robustness.
Pointwise persistence with no neighborhood valid for nearby laws is insufficient.
One cannot choose a different institutional gate or fine for each law; e_epsilon
and g(lambda) are fixed before the cover. Pure strictness is convenient, not
necessary: a continuously recoverable mixed branch with suitable incentive margins
works by the same argument. F2 gives a different primitive route without strictness.

## R4. The four meanings of persistence

| Assertion | What it earns |
|---|---|
| Some receiver equilibrium exists at every posterior | Nonemptiness; no deterrence guarantee. |
| Some deterrent exists, perhaps only at a large fine | Feasibility; no near-optimal value recovery. |
| Every desired near-optimal feasible witness has nearby feasible witnesses | Sufficient when it includes the common design and all nearby laws uniformly; stronger than necessary. |
| (UR): some near-optimal common design survives all nearby laws, allowing replacements | Necessary and sufficient under R1. |

Lower continuity of the full equilibrium correspondence is neither the definition
nor a necessary condition for value continuity. Sender incentive inequalities
can still lose feasibility even when equilibria persist. Full lower continuity of
F is sufficient; recovery of EVERY optimizer is unnecessary. For example the
abstract compact design sets F(0)={(0,0),(1,0)} and F(lambda)={(1,0)} for lambda!=0
have closed graph and constant value zero despite loss of the first optimizer.
This abstract illustration is not an additional game counterexample.

A claim explicitly ASSUMING (UR) cannot be killed by disappearance of a branch
that makes (UR) false. The quoted informal claim is true under that strong reading
plus R1, false under mere existence of a high-fine deterrent, and incomplete until
its support, equilibrium notion, gate menu and persistence quantifiers are fixed.
