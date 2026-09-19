# A robust partial-certificate frontier

Analytical result for an explicit new game, not a claim of historical novelty.
The gate mechanism is an institutional intervention; its seed is hidden. The
fine and disclosure cost change utilities, not the probabilistic conditioning rule.

## 1. Objects and protocol

Let θ∈{1,2,3}, p=(1/4,1/4,1/2), R,S∈{−1,+1}. The analyst's family is

    Q_x(θ=z,r,s)=p_z(1+x_z rs)/4,
    x∈[−1,1]^3,   Σ_z p_z F(x_z)≤κ,
    F(x)=((1+x)ln(1+x)+(1−x)ln(1−x))/2,
    0≤κ<ln 2; 0 ln 0=0.

Thus R and S each have uniform conditional marginals in every state. F(x_z)
is exactly KL(Q(R,S|z) || uniform product); the SINGLE budget couples states.
A committed gate sends T with P(T=t|S=s)=(1+γst)/2, 0≤γ≤1. Only R,T are public.
Gate quality is P(T=S)=(1+γ)/2≥q0, where 1/2≤q0<1. We optimize within this
specified symmetric binary gate family, not all possible information mechanisms.

Two receivers choose (a_i,y_i)∈{A,B,C}×{−1,+1} simultaneously. Their utilities are

    c·1[a_i=a_j]+b·1[a_i=f_i(θ)]−e·1[a_i≠C]
       +L·1[y_i=y_j]+w·1[y_i=S],

where f_1=(A,B,C), f_2=(B,A,C), 0<c<b/2, 0≤L<w, w>0, e≥0.
Target: a_1=a_2=C and y_1=y_2=T. Additive utilities allow either or both
coordinates to change; zero-gain obedience is equivalent to the separate
coordinate inequalities at each public history. This statement does NOT license
adding worst EXPECTED gains attained in different laws at positive tolerances.

An advocate knows θ and R,T, but not S or the gate seed. Types 1 and 2 may send
one common verifiable certificate E={1,2}; type 3 cannot. Silence is feasible for
all types, at zero cost. There is no full-type certificate. The advocate cannot
commit to silence. Its benefit from player 1's policy is (η,0,v) at (A,B,C) for
type 1, and (0,η,v) for type 2, where 0<v<η/2. Type 3's benefit is zero. Sending
E costs k≥0. The sender has no later action and no operational payoff.

Receivers know the actual x, the protocol and utilities. The analyst does not know
x. Robust pooling means: ONE (γ,e,k) and the always-silent sender strategy support
the target in a PBE for EACH x in the family. Off-path beliefs and continuation
equilibria can depend on x and public history. Only positive-probability types
at that history can receive posterior mass after E. A common sequence of sender
trembles generates the beliefs within each game; no cross-model common-tremble
or unobserved-model implementation claim is made. Cooperation is required ON PATH;
off-path operational choices may change after the certificate.

## 2. Exact controlled-information frontier

Write d=c+e, ell=L/w, m=Σp_z x_z, h=rt. The public mass and posterior are

    P(r,t)=(1+γh m)/4,
    P(θ=z|r,t)=p_z(1+γh x_z)/(1+γh m).

For player 1, switching C→A has statewise policy gain

    g(d)=(b−d,−d,−b−d).

Switching C→B swaps the first two entries. Player 2 has the same two constraints.
Since p_1=p_2 and the family is invariant under that swap, only g is needed.
Define the support value

    Hκ(g)=max{Σp_z g_z x_z : x∈[−1,1]^3, Σp_z F(x_z)≤κ}.

Multiplying gains by the public mass, and using x↦−x symmetry, proves the exact
policy condition

    γ Hκ(g(c+e)) ≤ b/4+c+e.                         (1)

Zero-mass histories have zero numerator and impose no spurious condition.
For the operational deviation T→−T, four times the numerator is

    −L−wγ−h m(w+Lγ).

Jensen gives |m|≤zκ=F⁻¹(κ), attained by all x_z=±zκ. Therefore the exact
operational and quality condition is

    γ≥γ*:=max{2q0−1, 0, (zκ−ell)/(1−ell zκ)}.         (2)

In particular, policy enforcement cannot repair a violation of (2).

The support function has a one-dimensional exact evaluation:

    Hκ(g)=inf_{β>0} [κ+Σp_z ln cosh(βg_z)]/β.         (3)

At κ=0 it is zero. If κ≥Σ_{g_z≠0}p_z ln 2, it equals Σp_z|g_z|, with x_z=sign g_z
and x_z=0 where g_z=0. Otherwise the unique positive β satisfying
Σp_zF(tanh(βg_z))=κ gives the attaining x_z=tanh(βg_z).
Proof: F*(t)=ln cosh t gives the upper bound. F'(x)=atanh x and the displayed
witness give equality. Cost increases strictly from zero to the stated saturation
cost unless g=0. These are established convex conjugacy specialized to this family.

Let E_ctl(κ,γ) be the least e≥0 satisfying (1), provided (2) holds. It lies in
[0,b−c]: e=b−c makes every C-deviation nonprofitable state by state. The
worst numerator decreases strictly with e (slope at most −(1−γzκ)<0), so either e=0
works or the unique root of equality in (1) gives E_ctl. Hκ≥0, so the feasible
policy set shrinks as γ increases. Thus γ* minimizes E_ctl within the chosen gate
family, and γ*<1 under κ<ln 2 and q0<1. This is an exact analytic characterization
with a scalar root, not a closed elementary expression or an exact decimal.

## 3. Solve the disclosure continuation before composing

Put e_part=b/2−c and k_part=η/2−v.
Suppose BOTH types 1 and 2 have positive public posterior. Their post-certificate
belief μ is unrestricted on {1,2}: silence pools, so E is off path. Every μ is
obtainable by fully mixed sender trembles proportional to
ε μ_z/P(θ=z|r,t)+ε² on eligible types, for sufficiently small ε.

**Lemma 1 (fixed-e partial certificate).** A target-obedient history admits a
pooling continuation iff e≥e_part OR k≥k_part.

Proof, necessity at e<e_part. For either receiver and any opponent's policy mix
with probability r_C on C, the average payoff of A and B minus the payoff of C is

    b/2−e + c(1−r_C)/2 − c r_C ≥ b/2−e−c >0.

Thus C is never a best response for any posterior μ; no continuation Nash
equilibrium uses C. Let q be player 1's probability of A in the common
continuation. The two sender benefits are ηq and η(1−q). Both types must prefer
silence, requiring ηq−k≤v and η(1−q)−k≤v. Adding yields k≥k_part.
Individual minima are both zero, but they are attained by DIFFERENT continuations.

Sufficiency at low e. At μ=(1/2,1/2), each receiver independently mixing A/B
half-and-half is Nash: both actions pay b/2+c/2−e>0 and C pays zero. Both sender
benefits are η/2, so k≥k_part deters both. Choose a symmetric operational best
response to S under this posterior; additivity joins the policy and operation
continuations. For e≥e_part, choose μ=(1/2,1/2) and policy (C,C): switching gains
b/2−c−e≤0. Each sender keeps benefit v and loses k upon disclosure. Again join a
symmetric operational equilibrium. These beliefs have the tremble construction
above, and silence uses Bayes' rule. ∎

At low e the joint attainable sender-payoff set is exactly
{(ηq,η(1−q)):0≤q≤1}. To attain any q, take
μ=1/2+(c/b)(q−1/2), player 1's A-probability q and player 2's A-probability 1−q.
Each receiver is indifferent A/B, with payoff (b+c)/2−e>0 versus C's zero. All
μ are in [0,1] since c<b. This directly verifies attainability, not only an outer
line segment. A public correlating device is unnecessary for this construction.

## 4. The robust frontier and a support discontinuity

**Theorem 1 (full-support gate).** For 0≤γ<1 satisfying (2), robust pooling
exists exactly when e≥E_ctl and (e≥e_part OR k≥k_part). Consequently

    E_vol(κ,γ,k)=E_ctl(κ,γ)                  if k≥k_part,
                max{E_ctl(κ,γ),e_part}     if 0≤k<k_part.       (4)

The optimum over our symmetric gate family uses γ*: every γ<1 retains both
eligible types at every public history, and the disclosure condition is independent
of γ there. Lower γ weakens every controlled policy inequality. The endpoint γ=1
cannot improve controlled obedience and cannot improve the disclosure condition.

Proof. For γ<1 every state likelihood is positive; apply Lemma 1 at every history.
Necessity of controlled obedience follows because silence is pooling. The explicit
continuations prove sufficiency for every x with the same gate, fine and sender
strategy. Each game has finitely many histories, so choose the trembles jointly
across histories. ∎

**Theorem 2 (perfect gate).** At γ=1, if κ<(ln 2)/4, formula (4) still holds.
If κ≥(ln 2)/4, the exact robust frontier instead is

    E_vol(κ,1,k)=E_ctl(κ,1)     if k≥η−v,
                b−c           if 0≤k<η−v.                     (5)

Proof. Losing an eligible type z after some h requires x_z=−h, costing at least
p_z ln 2=(ln 2)/4. Below that budget both eligible types remain possible.
At or above it, choose x_1=−1,x_2=x_3=0 and h=+1. This history has mass 3/16;
only type 2 can send E. The certificate now reveals θ=2 with certainty. For
e<b−c each receiver's preferred policy is strictly dominant: its advantage over
C is at least b−e−c>0, and over the other non-C action at least b−c>0. Thus the
sender gets η upon disclosure versus v in silence, requiring k≥η−v. This proves
necessity for robust pooling. For sufficiency at k≥η−v, no sender continuation
benefit can exceed η, so any continuation equilibrium deters disclosure. For
e≥b−c, (C,C) is Nash at every posterior, making all sender deviations weakly
unprofitable. If no eligible type is possible the certificate cannot occur, even
under feasible trembles, and is irrelevant. ∎

PBE here respects physical support and can be made sequentially consistent within
each game. Assigning probability to the impossible type in Theorem 2 would erase
the discontinuity by changing the equilibrium specification. The jump is a
failure of using full-support beliefs at a support-changing limit, not a numerical
ill-conditioning claim. Neither theorem imposes a stronger equilibrium refinement
such as the intuitive criterion or requires unique/strict pooling. At k=0 high-e
silence is weak; at the threshold equalities receivers/senders may be indifferent.

## 5. Worked design and the invalid shortcut

Take κ=.3, b=2,c=.2,L=.1,w=1,q0=.6,η=1,v=.2.
Then e_part=.8,k_part=.3,γ*≈.682870616657 and E_ctl≈.224362693945.
Thus a low-cost certificate (k<.3) raises the minimum fine to .8; at k≥.3 it is
≈.22436. Both policy and operation constraints are active in controlled design.
For k=.4, γ↑1 keeps the partial-certificate condition satisfied, whereas γ=1
requires fine 1.8 because .3>(ln 2)/4 and .4<.8. The controlled endpoint limit
is ≈.940677710374; it must not be confused with .22436 at γ*. The strict slope
bound and continuity of the support function imply continuity of E_ctl as γ↑1.
Thus the voluntary frontier jumps from this limit to 1.8 at k=.4.

A concrete failed shortcut: at e=.5,k=0 and a controlled-obedient noisy gate,
each type has an individually credible continuation with benefit zero. These
summaries falsely certify pooling: their common continuation would require
q≤.2 and q≥.8. The exact joint line proves impossibility. Raising e to .8 makes
(C,C) credible and repairs the joint constraint. Computation checks the on-path
condition, the support-loss witness and the payoff inequalities in the original
finite game. The written proofs, rather than floating-point optimizer status,
establish the universal frontier.
