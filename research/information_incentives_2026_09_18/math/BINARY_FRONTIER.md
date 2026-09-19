# Both active components: exact and positive-tolerance frontiers

Analytical derivation. The supplied binary model and its exact-zero-tolerance
frontier are borrowed starting results; the six-branch joint expected-gain
calculation below resolves the extension explicitly left open in its §12.

## Model (unchanged from the supplied active benchmark)

θ,R,S∈{−1,1}; Q(θ,R)=Q(θ,S)=1/4. Every compatible law is
Q(θ,r,s)=(1+u rs+v θrs)/8, |u|+|v|≤1. Let

    F(x)=[(1+x)log(1+x)+(1−x)log(1−x)]/2,
    C(u,v)=[F(u+v)+F(u−v)]/2≤κ,  0≤κ≤log 2.

The committed gate sends common T with Pr(T=t|S=s)=(1+γst)/2, 0≤γ≤1.
Both players see R,T and know the actual Q. Target: x_i=R,y_i=T.
Player 1 prefers θ, player 2 prefers −θ. Utility is

    c 1{x_i=x_j}+b 1{x_i=preferred_i(θ)}
    +L 1{y_i=y_j}+w 1{y_i=S}−e 1{x_i≠R},

0<c<b, w>0, 0≤L<w, e≥0. The policy penalty is charged for a policy deviation;
an operational-only deviation is unpenalized. Simultaneous product actions and
additive payoffs allow either or both coordinates to change. Each candidate Q
is held fixed across deviations, messages and comparisons of gate/enforcement.

Set d=c+e. At (r,t), probability and unnormalized deviation gains are

    mass = (1+γu rt)/4,
    policy = [−d(1+γu rt)−bγv t]/4         (player 1),
    operation = [−L−wγ−rt u(Lγ+w)]/4.

Player 2 reverses the v term. These formulas follow by summing the eight cells,
not by assuming obedience. If mass is zero both numerators vanish. Expected
optimal gain is the sum over observations of the two positive parts, since the
choice to change either action is separately available. Both players have the
same expected gain, including for signed u,v by sign symmetry.

## Theorem E — six-branch exact joint vulnerability

Restrict to u,v≥0 by symmetry. Define affine functions

    P0=0,
    P1=(bγv+dγu−d)/4,
    P2=(bγv−d)/2,
    O =[u(w+Lγ)−L−wγ]/2.

Then the expected optimal gain of ONE player under ONE Q is

    V(u,v)=max{P0,P1,P2}+max{0,O}.

Thus its robust value is exactly

    V*(κ,γ,e)=max_{j∈{0,1,2},k∈{0,1}}
               {C_jk + Sκ(A_jk,B_jk)},                (E1)

where Pj+kO=C_jk+A_jk u+B_jk v and

    Sκ(A,B)=max_{u,v≥0,C(u,v)≤κ} (Au+Bv).

All six A,B are nonnegative. The standard log-cosh conjugacy gives

    Sκ(A,B)=inf_{β>0}
       [κ + ½ log cosh(β(A+B))
          +½ log cosh(β(A−B))]/β.                     (E2)

Endpoint convention: κ=0 gives zero; when the unconstrained maximizing face
is affordable the support is max{A,B}. For A=B>0 that face is affordable at
κ=(log 2)/2; for A≠B and both coefficients relevant saturation costs log 2.
A=B=0 gives zero. Otherwise the attaining point has

    x=tanh(β(A+B)), y=tanh(β(A−B)),
    u=(x+y)/2, v=(x−y)/2,
    [F(x)+F(y)]/2=κ.

Proof. Positive policy gains can occur only at the two observations with the
unfavorable sign of t. Their two positive parts give max{P0,P1,P2}; the ordering
uses u,v≥0 and d≥0. The operational gain can be positive only at rt=−1, in two
observations, giving max{0,O}. The sum of these two maxima is the maximum of
six affine functions. A finite maximum commutes with a supremum over the SAME
compact family, so each branch has one legitimate common-law extremizer.
Set x=u+v,y=u−v. The feasible diamond becomes [−1,1]² and the objective becomes
[(A+B)x+(A−B)y]/2. F*(t)=log cosh t proves the upper bound; the tanh construction
attains it when its cost equals κ. For A,B≥0, monotonicity and oddness of tanh
give u,v≥0, so removing quadrant constraints did not enlarge the support. The
explicit affordable maximizing face supplies the endpoint cases. ∎

This is an exact analytic finite formula, not a numerical conjecture. It is
not a general polynomial-time algorithm: n independently selectable action
coordinates and finitely many observations can require exponentially many
branches. The finite maximum-of-affine construction itself is established convex
analysis; the result here is its six-branch specialization with active incentives.

For δ≥0, the exact per-player expected-gain requirement is V*≤δ. Since policy
penalties do not change O, no finite e can meet δ below max_C max{0,O}. Otherwise
the least e∈[0,b−c] meeting E1 is the frontier. No claim of source-only channel
optimality is made for δ>0 with both components active: exact symmetrization
survives, but the best symmetric accuracy may be an interior tradeoff.

## Exact obedience and active design (reproduced supplied result)

Put zκ=F⁻¹(κ), ell=L/w and a=(c+e)/b. For e<b−c let
Hκ(a)=Sκ(a,1). Robust obedience is equivalent to

    γ≥γop=max{0,(zκ−ell)/(1−ell zκ)},
    γ Hκ(a)≤a.

For e≥b−c only the operational inequality remains. A quality floor q0 adds
γ≥2q0−1. Hence the optimal exact source-only public symmetric channel uses
γ*=max{γop,2q0−1}; the policy threshold increases with γ. The supplied
coarsening and undisclosed symmetrization argument proves this optimum across
its specified public source-only channel class. This note does not enlarge that
class to private messages or voluntary disclosures without a new analysis.

Under separately sharp statewise correlation bounds, put
rκ=F⁻¹(min{2κ,log 2}). The relaxed square in x=u+v,y=u−v gives
|u|+|v|≤rκ. Its corresponding conditions are

    γ≥max{0,(rκ−ell)/(1−ell rκ)},
    e≥max{0,bγrκ−c}.

The richer cost profile keeps [F(x)+F(y)]/2≤κ and recovers the full law exactly.
For fixed 0<γ<1 and message (r,t), conditional likelihood given θ is
(1+γrt xθ)/4, with xθ=u+θv. Its cost profile is
Jθ(a)=F((4a−1)/(γrt)); both states share weights 1/2. At γ=0 the likelihood
is the single value 1/4, and its minimum cost is zero.

## Exact counterexample 1: sharp local bounds, strictly excessive enforcement

Choose κ=F(1/2)/2, b=2,c=1/2, γ=4/5, w=1,L=1/10.
Each xθ projection is [−1/2,1/2], attained by spending the budget in that state.
The box penalty is exactly 3/10, attained at u=0,v=1/2. That law costs 2κ and
is inadmissible. At e=3/10, a=2/5, the maximizing policy direction has nonzero
coefficients of opposite sign on both x coordinates; its unique endpoint
selection has cost 2κ. Theorem B gives a strict penalty gap.

It is not a zero-risk trick. u=0,v=1/3 is feasible and requires penalty 1/30.
Indeed F(x)=Σ_(n≥1) x^(2n)/[2n(2n−1)], and (2/3)^(2n)<1/2 for every n≥1,
so F(1/3)<F(1/2)/2. Therefore

    1/30 ≤ e_full < e_box=3/10.

Operational obedience holds at γ=4/5 since |u|≤1/2, but γ=0 fails at the
feasible u=1/3,v=0. Useful source information cannot be eliminated.

## Exact counterexample 2: adding separate expected worst cases is strict

Choose κ=F(4/5), b=2,c=1,e=0, γ=7/10, w=1,L=1/10.
The operational optimum is uniquely u=4/5,v=0, giving 7/250. Uniqueness follows
from strict convexity: C(u,v)≥F(u), with equality only at v=0 (away from trivial
endpoints). At that law policy vulnerability is zero. But u=0,v=4/5 is feasible
and policy vulnerability is at least 3/50>0. Thus no common law maximizes both
nonnegative component vulnerabilities. Compactness proves

    max_C (Vpolicy+Voperation)
      < max_C Vpolicy + max_C Voperation.

The six-branch formula computes the correct left side. This is a strict analytic
counterexample, not just a solver discrepancy. In contrast, checking BOTH
components for ZERO vulnerability legitimately uses separate maxima: each must
be nonpositive under every law. Incompatible extrema across different obedience
constraints do not invalidate that universal logical conjunction.
