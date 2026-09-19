# Query-relative joint feasibility under composition

The preceding frontier is solved before making this abstraction. This is a direct
specialization of established set optimization and relational/valuation algebra,
not a proposed new universal theory. It explains precisely the limited common
structure; it does not identify causal semantics with incentive semantics.

## Exact retained object

A component has boundary value u in U and internal witness x∈X(u). Its vector
of resource usages or deviation gains is r(u,x)∈R^d. Smaller values are better
for the specified queries. Define the feasible image and its upper image by

    K(u)={r(u,x):x∈X(u)},
    B(u)=K(u)+R_+^d={b:∃x∈X(u), r(u,x)≤b}.

No closure or convex hull is taken. Empty witness sets give empty images.
A summary must retain u until every other component referring to it has been
connected. u can include an observation likelihood vector, hidden model identity,
message eligibility, information set, belief-consistency data or shared random seed.
Labels alone do not establish that boundaries refer to the same object.

**Theorem 4 (exactness and coarsest query-relative summary).**
(a) Two components answer every query “at this boundary u, is there one witness
meeting all coordinate bounds b?” identically iff their B(u) are equal for all u.
(b) Suppose, conditional on a common u, component witnesses are freely selectable
and their resource vectors add. Then

    B_combined(u)=B_1(u)+B_2(u).                       (7)

If u is then hidden, the exact retained budget set is ∪_u B_combined(u).
(c) The same identities hold with an external boundary a retained and an internal
wire u eliminated: B(a)=∪_u[B_1(a,u)+B_2(a,u)], with incompatible pairs excluded.
Consequently replacement by equal upper images at the FULL connection interface
preserves all queries constructed by these operations and coordinate upper bounds.

Proof. (a) The truth set of the query is exactly B; if they differ, use the differing
u,b as a distinguishing query. (b) A combined vector is k_1+k_2 with k_i∈K_i.
Since R_+^d+R_+^d=R_+^d, upper closure commutes with the Minkowski sum. Conversely,
if b=b_1+b_2 with b_i∈B_i, choose witnesses k_i≤b_i to get k_1+k_2≤b. Existential
elimination is union, which also commutes with upper closure. This proves (c)
and induction over any finite expression made from these operations. ∎

“Coarsest” means equivalence for THIS query family; it is not a smallest encoding
or a complexity result. Scalar profiles in Theorem 3 are the special case where
B(a)=[J(a),∞); attainment makes the left endpoint closed. With vector costs there
need not be one simultaneous minimum. If K is compact, its minimal elements
suffice because every k dominates a minimal point; the entire upper image is the
more general object, including nonattainment. Coordinates with different units
are retained separately; addition presumes aligned meanings and units.

The proof requires no convexity. Nor does it imply that arbitrary game equilibria
or arbitrary causal mechanisms compose by vector addition: such a decomposition
must first be warranted. If a downstream component tests an equality, transforms
resources nonmonotonically, depends on a discarded internal variable, or changes
the feasible continuation game, equal B is insufficient.

## How the two applications fit—and where they differ

**Controlled information.** Boundary a is the COMPLETE vector of query-relevant
likelihoods. Internal witness is a law; resource is its information cost. Theorem 3
computes its upper image. The budget κ selects attainable a; then robust obedience
checks EVERY selected a. The universal linear numerator query can use a support
function of the resulting compact convex likelihood set. The cost upper image
must not be confused with coordinatewise upper bounds on likelihoods themselves.
For multiple observations, retain their joint likelihood array if one query uses
them together. A separate profile for each observation is enough only when the
specification is a conjunction of independent universal single-observation tests.

**Disclosure.** At fixed public history, x is a COMMON pair (posterior, continuation
Nash equilibrium) and r is the vector of sender benefits minus pooling benefits,
one coordinate for each type eligible for the same certificate. There is pooling
exactly when the cost vector k belongs to B. This is an EXISTENTIAL simultaneous
inequality. For the solved low-e model K={(ηq−v,η(1−q)−v):q∈[0,1]}, so B on the
equal-cost diagonal begins at k=η/2−v. High e adds (0,0), repairing feasibility.
Support/type eligibility is part of the boundary: at γ=1 it can change K.

Thus the shared theorem concerns feasible-image retention BEFORE their different
universal and existential strategic tests. It does not exchange ∀model∃continuation
with ∃continuation∀model. The frontier uses the former; a robust decision maker
who cannot observe the actual model may need the latter and a richer shared witness.

## A credible nonconvex obstruction

Scalar support functions describe closed convex hulls, not general feasible sets.
This is consequential even with one sender and public receiver information.
Consider two receivers with actions A,B and payoffs 1 for coordinating and 0
otherwise, independent of the sender's type. Their Nash equilibria are exactly
(A,A), (B,B), and independent half/half mixing. For sender type 1 assign payoffs
1 at (A,A), 0 at (B,B), and 1 at either mismatch; type 2 swaps the two diagonal
payoffs and also gets 1 at mismatches. The credible payoff set, at EVERY posterior,
is exactly

    K={(1,0),(0,1),(3/4,3/4)}.

No member is coordinatewise ≤(1/2,1/2). Its convex hull contains (1/2,1/2), so
convexifying falsely supplies a common deterrent. All support functions agree
between K and its convex hull, hence a support-only summary cannot answer this
existential query exactly. The Nash list follows directly from each player's
best response to the other's A-probability: A above 1/2, B below, both at equality.
Independent mixed actions do not implement a lottery over two pure equilibria.
A PUBLIC coin selecting (A,A) or (B,B), drawn after the sender chooses disclosure,
would implement the missing point and change the game. Before disclosure, an
observed coin would let the sender condition its deviation and would not justify
the same ex-ante deterrence test. Randomization timing is part of the interface.

## Bounded extension after Theorems 1–4: networks and multiple senders

For a finite network of explicit witness relations, retain every shared variable
until its last connection. Natural join combines compatibility; existential
projection eliminates internal variables; resource vectors add. Theorem 4 proves
exact elimination by induction for ANY fixed elimination order. On a tree of
bags the usual separator messages suffice when all shared variables and costs
are allocated correctly. This is standard variable elimination; bag sizes and
Pareto frontiers can grow exponentially. Pairwise summaries on a cycle need not
recover a global witness, so local consistency alone is not the theorem.

There is NO corresponding automatic theorem for multiple strategic senders.
Here is a decisive belief-consistency obstruction. Let independent binary types
τ_1,τ_2 have uniform prior. Two senders privately know their own type; each can
send an off-path public message m_i, and each randomizes independently. At the
joint message (m_1,m_2), any positive tremble probabilities α_a,β_b give posterior

    μ_ab=α_a β_b/[(α_0+α_1)(β_0+β_1)].

It has determinant μ_00 μ_11−μ_01 μ_10=0, as does every limit. The apparently
admissible joint belief μ_00=μ_11=1/2, μ_01=μ_10=0 has determinant 1/4; it cannot
be generated. Its two uniform marginals conceal this failure. A single sender
knowing BOTH types could generate it. A shared correlated seed or correlated
prior changes the premise. Thus extension must retain common likelihood-factor
and consistency constraints, not choose arbitrary posteriors message by message.
We prove this obstruction only; general multiple-sender equilibrium/frontier
characterization remains outside the earned result.
