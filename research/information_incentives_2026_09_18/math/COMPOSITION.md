# Exact composition with a shared information budget

Status: analytical derivations, 18 September 2026. All sets below are finite-
dimensional. Results use established partial minimization, convex duality and
junction-tree gluing; no priority claim. Source comparisons are separate.

## 1. Subject, observables, and budget

Fix positive state weights p_z summing to one. State z contains everything entering
a deviation payoff, including opponents' prescribed actions if necessary. Let
P_z be a nonempty compact convex polytope of source distributions on a finite
alphabet, specified by nonnegativity and consistent marginal equalities. Let
r_z>0 be a specified reference law, and put d_z(q)=D(q||r_z). A source-only
observation channel gives a known vector h_y(s)=Pr(Y=y|s), 0≤h_y≤1.
The cost-constrained family is

    Cκ = {(q_z): q_z∈P_z, Σ_z p_z d_z(q_z)≤κ}.

Assume Cκ nonempty. This is the ONLY coupling across z. For a deviation gain g_z
and flat deviation penalty e, its unnormalized obedience numerator at y is

    Σ_z p_z <h_y,q_z> (g_z−e).

Positive numerators imply positive observation probability. A zero-probability
message supplies a zero numerator and no violation. Players know the actual
law; Cκ describes the analyst's uncertainty, not ambiguity-sensitive preferences.

For each z,y define the extended-real convex function

    J_zy(a) = min {d_z(q): q∈P_z, <h_y,q>=a},

with +∞ for empty fibers. The minimum exists on every nonempty fiber. Its domain
is the attainable interval. It is convex by mixing minimizers and convexity of
KL; lower semicontinuity follows from compactness and continuity of finite KL
against a positive reference.

## 2. Theorem A — exact information-cost composition

The set of jointly attainable message likelihoods is exactly

    K_y(κ) = {a: Σ_z p_z J_zy(a_z)≤κ}.                    (A1)

Consequently exact robust obedience is equivalent to

    max_{a∈K_y(κ)} Σ_z p_z a_z(g_z−e)≤0                  (A2)

for every player, initial observation, message, and deviation in the declared
common model. Conditional applications must retain the original budget weights;
one may not allocate a fresh κ after each conditioning operation.

Proof. Any actual tuple has d_z(q_z)≥J_zy(a_z), proving necessity. Conversely
choose a cost-minimizing q_z in each nonempty fiber. There are finitely many
states, and these choices meet all marginal constraints and the shared budget.
Their joint law p_z q_z attains a. This proves sufficiency and sharpness of A2.
The construction is stronger than storing probability intervals: it retains the
cost of each choice and uses the same budget for their simultaneous selection.
It requires no binary alphabet, symmetry, or state-independent local tables. ∎

For multiple queried message probabilities or payoff moments replace a by a
vector and h by a matrix; the same proof applies. A single-message profile is
sufficient for exact obedience because all those inequalities must hold separately.
Expected optimal gain is a sum of messagewise positive parts under ONE law; it
requires a joint message-vector profile or an equivalent retained full law.

**Failure boundary.** Extra constraints linking q_z outside this separable budget
are not encoded by A1. They require an additional compatibility relation. Ordinary
mutual information with an endogenous reference is not automatically this fixed-
reference KL model. In the binary benchmark the fixed marginals make them equal.

## 3. Theorem B — necessary and sufficient endpoint sharpness

Let [L_z,U_z] be the exact coordinate projections of K_y(κ), and let B be their
product. For any real direction w, define the endpoint face

    E(w)={a∈B: a_z=U_z if w_z>0; a_z=L_z if w_z<0}.

Then

    max_K w·a = max_B w·a  iff  K∩E(w)≠∅.              (B1)

Equivalently, under A1 this happens exactly when

    Σ_(w_z>0) p_z J_zy(U_z)
      +Σ_(w_z<0) p_z J_zy(L_z)
      +Σ_(w_z=0) p_z min_(a∈[L_z,U_z]) J_zy(a) ≤ κ.   (B2)

Proof. Each coordinate's contribution is bounded by its selected endpoint.
Equality of their sum forces equality on every nonzero-weight coordinate.
Compactness supplies a maximizer; zero-weight coordinates can minimize cost.
Conversely a feasible selected face point attains the box support. ∎

This criterion allows a nonrectangular family to be sharp for a particular gain:
full rectangularity is sufficient but not necessary. Equality for ALL support
directions is equivalent to K=B by separation of compact convex sets. This last
fact and the general rectangularity motivation are established convex geometry.

For a SINGLE message/deviation let m=inf_K Σp_z a_z>0, and let its box conditional
gain maximum e_B be positive. Its exact required penalty equals e_B iff B1 holds
for w_z=p_z(g_z−e_B). Indeed the box numerator maximum at e_B is zero. If no
attaining face point lies in K, compactness makes the exact maximum negative;
continuity and the positive denominator permit a strictly smaller penalty.
If e_B≤0 both nonnegative penalties can be zero despite a support gap. For many
constraints equality of the overall frontier needs only one binding constraint
to attain the maximum; do not require all directions to attain their endpoints.

## 4. Theorem C — dual and certified approximation

Assume κ>min_(q_z∈P_z) Σp_z d_z(q_z) (strict budget feasibility).
For w_z=p_z(g_z−e), A2's left side equals

    inf_(λ≥0) {λκ + Σ_z p_z sup_(q∈P_z)
                           [(g_z−e)<h_y,q> − λd_z(q)]}. (C1)

This is a standard finite convex Lagrange dual, not a new duality theorem.
Proof: weak duality follows by adding λ(κ−Σp_z d_z). Strict feasibility separates
the convex hypograph of attainable (cost,value) from a larger value at κ, giving
a supporting slope λ≥0 and equality. At a slack budget λ=0 is allowed; an infimum
need not have a positive minimizer. Boundary budgets use A1 directly or limits.
Each inner supremum is conjugate to J_zy. A feasible primal and any λ give a
lower and upper support bound respectively. The minimum enforcement is the
smallest e≥0 for which each support is nonpositive (with the positive-mass
assumption, the usual linear-fractional root characterization).

For a quantitative approximation assume r_z∈P_z, κ>0, and every observation
likelihood in an outer model O has mass ≥m>0. O obeys the same marginal constraints
and every q∈O has total cost≤κ+ε. Mixing any q with the baseline r in fraction
α=κ/(κ+ε) gives q'∈Cκ by convexity of KL. For one deviation let G=max_z|g_z|.
Writing N,D for its unpenalized numerator and mass, |N(q)−N(q')|≤(1−α)G and
|D(q)−D(q')|≤1−α, while |N(q')|≤G D(q'). Hence

    0 ≤ e_O−e_C ≤ 2G ε/[m(κ+ε)]                        (C2)

if Cκ⊆O, also after taking positive parts and a finite maximum over deviations.
Proof: subtract N/D and N'/D', use the preceding bounds and D≥m, then optimize.
This conservative bound needs positive mass and a verified total excess-cost
bound; separate endpoint sharpness alone supplies neither. Rare observations
explain the deterioration as m→0. No claim that this constant is optimal.

## 5. Theorem D — compute the cost profile using local tree tables

Assume original source bags form a junction tree (running intersection), and
r_z is their strictly positive Markov extension. For one coordinate-projection
transcript y, augment each bag C with a subtree flag F_C and its children's flags.
Assign each observed variable to one bag containing it; F_C equals the AND of
local matches and children's flags. A leaf flag equals its local match. The
augmented bags still form a junction tree: each new child flag occurs exactly
in its bag and parent; original variable occurrences remain connected.

Let R_z be the lift of r_z with these deterministic flags. It is Markov on the
augmented tree, with zeros only outside the legal flag configurations. One way
to see this is to factor r_z by its original clique/separator functions and
multiply by the local 0/1 flag factors; this is a tree factorization. The root
flag is exactly the transcript event, and lifting preserves KL.

For locally consistent augmented bag tables τ_C with correct original marginals,
legal flags, and root event mass a, define

    D_tree(τ||R_z) = Σ_C D(τ_C||R_z,C)
                    −Σ_edges D(τ_sep||R_z,sep).        (D1)

Then the exact cost profile is

    J_zy(a)=min_τ D_tree(τ||R_z).                       (D2)

Proof. Gluing τ along the augmented tree gives its Markov extension Qτ, with
conditional factors defined arbitrarily on zero-mass separators. Every forbidden
flag configuration has zero probability, so Qτ lifts a valid source law. The
clique/separator factorization gives D(Qτ||R_z)=D_tree. For any other joint Q
with these same τ, expectations of log(Qτ/R_z) depend only on the retained tables.
Thus

    D(Q||R_z)=D(Q||Qτ)+D(Qτ||R_z)≥D_tree.

Terms on structural zeros are omitted; Q's support is contained in Qτ's support
since positive joint mass implies all relevant local factors positive. This
establishes both directions and attaining construction. ∎

Although D1 is written as a difference of KL sums, on the consistent-table domain
it is convex: it is the partial minimum of convex global KL. For bounded original
bag size, alphabet, and degree, one-transcript flag tables have size linear in
the number of bags. This is a representation-size statement, not a strongly
polynomial algorithm, nor permission to drop the separator terms. A general
stochastic channel can instead retain its expectation in A1; D2 needs a suitable
local realization if used for that channel.

Dobra–Fienberg supplies sharp probability bounds on decomposable marginal
systems. Tree gluing and the entropy identity are established mathematics; D2
specializes them to the exact information cost needed by A1. Keeping only the
original clique KL values fails: with fixed clique marginals all those terms
can be zero while unresolved higher-order dependence has positive global KL.
The flags retain the event-specific dependence needed by the query.

## 6. Asymmetric hidden-separator instantiation

In each of two equally likely payoff states, H is a fair hidden bit and local
marginals satisfy Pr(X=0|H=0)=.7, Pr(X=0|H=1)=.3, Pr(Y=0|H)=.5. Use the
conditionally independent reference r(H,X,Y)=Pr(H)Pr(X|H)Pr(Y|H), while allowing
all completions of those same two marginals. For p_h∈{.7,.3}, a conditional
2×2 table is

    (t_h, p_h−t_h, .5−t_h, .5−p_h+t_h),
    max{0,p_h−.5}≤t_h≤min{p_h,.5}.

Let d_h(t_h) be its KL divergence from the table at t_h=p_h/2.
For transcript X=Y=0 the event probability is a=(t_0+t_1)/2 and

    J(a)=min_{t_0+t_1=2a} [d_0(t_0)+d_1(t_1)]/2.

This is a scalar convex minimization, with derivative

    d_h'(t)=log[t(.5−p_h+t)/((p_h−t)(.5−t))].

It is strictly increasing in the interior. Hence each dual inner optimum can be
found by the monotone equation d_h'(t_h)=β(g_z−e), and a single β allocates the
shared information budget. There is no appeal to a multidimensional optimizer's
success flag for the analytic characterization.

The joint feasibility condition is [J(a_0)+J(a_1)]/2≤κ. The separately sharp
coordinate interval instead uses J(a)≤2κ, letting the other state remain at the
reference. At κ=.15 its interval is the unrestricted [.1,.4], but using opposite
endpoints simultaneously costs J(.4)≈.274358, too much. Conditional deviation
payoffs (1,−3) give the true penalty ≈.0235105 and box penalty 1/5. R can be an
independent fair policy recommendation; exchanging payoff-state labels gives
the other recommendation/player. Flipping Y, or flipping H and X together,
preserves the marginal/reference family and covers every observed transcript.
Thus the single-transcript calculation gives the uniform policy threshold in
this diagnostic. Active operational design is supplied by the separate two-
component benchmark; it is not asserted for an unspecified hidden-star operation.
