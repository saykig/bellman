# Information-only continuity: exact classification in the declared model

Payoffs and disclosure costs are FIXED in this theorem. General parameter changes
are considered only after it. This extends the previous game, without changing its
policy preferences or introducing additional senders.

## Domain and semantics

θ∈{1,2,3}, p_z>0, Σp_z=1, R,S∈{−1,1},
Q_x(z,r,s)=p_z(1+x_z rs)/4, and

    X(p,κ)={x∈[−1,1]^3: Σp_z F(x_z)≤κ},  0≤κ<ln 2.

The gate is P(T=t|S=s)=(1+γst)/2, γ∈[0,1]. The two receivers choose policy a_i∈{A,B,C} and operation y_i∈{−1,1}, with utility

    c·1[a_i=a_j]+b·1[a_i=f_i(θ)]−e·1[a_i≠C]
       +L·1[y_i=y_j]+w·1[y_i=S],

and preferences f1=(A,B,C), f2=(B,A,C).
Fix b>0, 0<c<b/2, w>0, 0≤L<w, 1/2≤q0<1. Policy target is (C,C), operational
target (T,T); only non-C policy actions incur fine e≥0. The advocate's state-1
payoffs at A,B,C are (η,0,v); state-2 payoffs (0,η,v); state-3 payoffs all zero.
Fix 0<v<η/2, k12,k23≥0. Every type can remain silent. Types 1,2 can send E12;
types 2,3 can send E23. Type 2 chooses ONE message, not both. Message costs are
k12 and k23. Receivers see all messages publicly and have no private information.

As before: the actual law is common knowledge among players; the analyst chooses
one fine for all laws. We seek pooling PBE existence with physically supported
beliefs, permitting law-dependent continuation equilibria. The same finite-game
sender-tremble construction supports all selected off-path beliefs simultaneously.
The target is required only on path. Nothing here asserts unique equilibrium,
stronger refinements, unknown-law robustness or an optimal arbitrary gate.

Operational feasibility is independent of e. Write zκ=F⁻¹(κ), ell=L/w and

    γmin(κ)=max{2q0−1,0,(zκ−ell)/(1−ell zκ)}.

Study continuity relative to the domain D={p>0, κ<ln2, γmin(κ)≤γ≤1}. Outside D,
no fine repairs the operational requirement, so the value is +∞. Crossing that
boundary is a separate feasibility loss, not a finite discontinuity claim.

## Controlled fine: a continuous, possibly saturated benchmark

For h=rt, put m=p·x and

    π_z(p,γ,x,h)=p_z(1+γh x_z)/(1+γh m).

Let

    C(p,κ,γ)=max{0, b·max_{x∈X(p,κ),h=±1,j=1,2}(π_j−π_3)−c}.

This is the exact controlled fine because a C→A or C→B deviation gains
b(π_j−π_3)−c−e. It is not an independent-state envelope. Jensen gives
|m|≤zκ<1, so the denominator is bounded below by 1−γzκ>0 locally uniformly.

**Lemma 1.** X(p,κ) is a nonempty compact continuous correspondence (equivalently,
Hausdorff continuous here) on p>0,0≤κ<ln2. Consequently C is continuous on D.

Proof. Its graph is closed by continuity of ΣpF(x), with a fixed compact ambient
cube. For lower continuity at κ>0, any feasible x can be approximated by t x,
t<1. If x≠0, strict convexity and F(0)=0 give ΣpF(t x)<κ; each such point remains
feasible for all sufficiently nearby (p',κ'). A diagonal approximation gives
feasible x_n→x along every parameter sequence. For x=0 use the same point. At
κ=0 the only feasible x is zero because every p_z>0, so lower continuity again
follows by choosing zero. Compactness gives upper continuity. The posterior is
continuous with a local uniform denominator bound; maximizing its continuous
finite family of payoffs over X preserves continuity (the compact maximum theorem,
or directly the two subsequence/witness arguments). ∎

C≤b−c. Its exact saturation condition is

    C=b−c  iff  γ=1 and κ≥κC(p):=(1−max{p1,p2})ln2.       (I1)

Indeed equality requires π_j=1 for j=1 or 2. At γ<1 every type remains possible.
At γ=1 it requires x_z=−h for every z≠j, with minimum cost (1−p_j)ln2; choose
x_j=0 to attain it with positive public mass. Conversely no lower-cost law can
make that posterior degenerate. Compactness and the positive mass bound ensure
that a supremum equal to one is attained. This saturation can MASK a disclosure
jump; not every support change causes a discontinuity.

## Solve both certificates at every supported history

Set

    a=b/2−c,  H=b−c,  t=η/2−v,  T=η−v,
    κ12(p)=min{p1,p2}ln2,   κ23(p)=p3 ln2.

For E12 with both eligible types possible, the previous payoff proof gives the
exact condition e≥a OR k12≥t. At e<a, no continuation receiver best response
uses C; the same continuation must give sender benefits (ηq,η(1−q)). The equal
posterior and half/half action mixture attain the simultaneous lower bound. At
e≥a, posterior (1/2,1/2,0) and continuation (C,C) deter both types.

For E23 while type 3 is possible, choose posterior δ3 and continuation (C,C),
which is receiver-optimal for every e≥0. The type-2 benefit stays v and the type-3
benefit stays zero. Both message deviations are unprofitable. Thus E23 imposes
no extra fine in this support regime. This is a mathematical property of the
DECLARED payoffs, not evidence that overlapping certificates are generally irrelevant.

If only type 1 or 2 can send E12, or only type 2 can send E23, the certificate
reveals a type with opposed policy preferences. For e<H, the state-preferred
policy is strictly dominant for each receiver and the advocate obtains η rather
than v. The exact condition is therefore e≥H OR the message cost≥T. If only type
3 can send E23 it creates no constraint. A certificate with no eligible possible
type is unreachable even under feasible trembles and is discarded.

The ambiguity family ALWAYS includes x=0, so the both-types E12 condition always
matters. A singleton harmful E12 is attainable exactly when γ=1 and κ≥κ12:
eliminate the cheaper of types 1 and 2 by setting its x_z=−h, with other coordinates
zero. A singleton harmful E23 is attainable exactly when γ=1 and κ≥κ23:
eliminate type 3, leaving type 2 possible. These witness costs are minimal.

## Theorem I: exact robust value and discontinuity locus

Define

    A = a if k12<t, and 0 otherwise;
    B = [γ=1] AND [(κ≥κ12 AND k12<T) OR (κ≥κ23 AND k23<T)].

Then throughout D,

    E(p,κ,γ) = H                         if B,
               max{C(p,κ,γ), A}         otherwise.             (I2)

Necessity follows by the on-path deviation bound and the certificate witnesses
above. Sufficiency selects the specified continuation for each supported message.
Type 2's two deviations must both be deterred, but it has no joint-message action;
choosing the two continuations independently is legitimate. For each history,
positive conditional type probabilities allow trembles of size
ε μ_m(z)/π_z+ε² on each feasible message, with residual probability on silence.
For small ε these sum to at most one, and Bayes' rule converges to both chosen
posteriors simultaneously. Hence no cross-message belief inconsistency is hidden.

**Exact continuity criterion.** With all payoffs and costs fixed, E is
discontinuous at (p,κ,γ)∈D iff

    γ=1,
    κ<κC(p),
    (κ≥κ12(p) AND k12<T) OR (κ≥κ23(p) AND k23<T).        (I3)

At each such point the jump from noisy gates is upward, from max{C,A}<H to H.

Proof. The background branch max{C,A} is continuous. The trigger set B is closed
relative to D because the costs are fixed and the information threshold functions
are continuous. Outside B there is a relative neighborhood with no trigger. At a
point in B with C=H, both branches tend to H, so E is continuous. At a point in B
with C<H, also A<H. Since κ<ln2 and q0<1, γmin<1; a sequence of gates γ_n<1 tends
to 1 within D with the same p,κ, turning B off. Its values tend to max{C,A}<H.
Condition (I1) gives precisely (I3). ∎

Thus the information-only claim is TRUE in this specified model, in a stronger
form: there is no independent continuation-equilibrium bifurcation as information
parameters vary on a support region. At any fixed fine, the allowable posterior
simplex and posterior-indexed receiver games are identical there. Support changes
are necessary but not sufficient for a jump; (I3) is necessary AND sufficient.
The belief-choice freedom, fixed payoffs/menu/costs, known law, full KL fibre and
public receiver information are load-bearing premises.

## Asymmetric overlapping-certificate examples

Use p=(1/5,3/10,1/2), b=2,c=1/5,η=1,v=1/5. Then
κ12=(ln2)/5, κ23=(ln2)/2 and κC=7(ln2)/10; a=4/5,H=9/5,t=3/10,T=4/5.

1. κ=.3, k12=.4,k23=.4: at γ=1, E=9/5; as γ↑1 the value tends to C<9/5.
   E12 supplies the support-driven obstruction, while E23 still has a type-3
   deterrent. A witness is x=(-1,0,0), with public posterior (0,3/8,5/8).
2. κ=.4, k12=.9,k23=.4: E12 is harmless even when singleton. E23 now produces the
   jump. A witness x=(0,0,-1) leaves public posterior (2/5,3/5,0); E23 reveals
   type 2. This shows why the overlapping menu cannot be ignored globally.
3. κ=.55 with the same costs: public information alone already makes C=9/5.
   Support loss occurs but creates NO additional value discontinuity. It is masked
   by the controlled requirement, exactly as (I3) predicts.

Decimals here select budgets; the jump claims follow from their inequalities with
logarithmic thresholds, not from optimization output.

## If the gate is also chosen by the designer

For γ<1, A is constant and C is nondecreasing in γ: every unnormalized policy
gain has the form p·g+γ sup_X p·(g x), with nonnegative support term by sign symmetry.
The least operationally feasible gate γmin<1 therefore minimizes E. The perfect
gate cannot lower either requirement. Hence

    E_design(p,κ)=max{C(p,κ,γmin(κ)),A}

is continuous for positive priors and κ<ln2. The previously discovered fixed-gate
jump is avoidable when the designer is free to introduce arbitrarily small noise.
This distinguishes minimum fine at a supplied gate from joint gate/fine design.
