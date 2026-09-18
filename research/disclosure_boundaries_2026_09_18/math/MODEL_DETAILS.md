# Model conventions and elementary derivations — additive completion

This supplements, rather than replaces, the first committed theorem edition.
All logarithms are natural. Define

    F(x)=[(1+x)log(1+x)+(1−x)log(1−x)]/2,

using 0 log 0=0. F is even, strictly convex, F(0)=0, F(±1)=log 2;
F⁻¹ means the inverse on [0,1]. The source family has uniform R and S conditional
on each state, with correlation x_z. Its information I(R;S|θ) is Σp_z F(x_z).
The reference product law is p_z/4. This fixes the meaning of the shared budget.

**Advocate convention:** the state-dependent payoffs listed in Theorem I depend
on receiver 1's POLICY action. They do not depend on receiver 2, the operations,
the hidden S, or the gate's random seed. Costs are incurred only upon disclosure.
This convention is also the one used by the Lean game and the earlier threshold.
The advocate observes θ,R,T. The players know the law; a single fine must work
for every law, with existence of an equilibrium assessed separately for each law.

## Operational bound

Let h=rt and m=Σp_z x_z. Conditional on public (r,t),

    E[S t | r,t]=(γ+h m)/(1+γ h m).

Jensen implies |m|≤zκ=F⁻¹(κ), and equality is attainable with all x_z=±zκ.
The target common operation t is a best response iff
L+w E[S t|r,t]≥0. Its smallest expectation over the source family is
(γ−zκ)/(1−γ zκ). Rearranging gives γ≥(zκ−L/w)/(1−(L/w)zκ).
The gate accuracy is P(T=S)=(1+γ)/2. Combining these restrictions and γ≥0 gives
γmin in Theorem I. Because κ<log 2 and q0<1, γmin<1. After a certificate, some
common source-majority operation is always an equilibrium: the majority advantage
and the nonnegative coordination reward favor it. No off-path operational target
is imposed. This is why the operational coordinate adds no disclosure threshold.

## Both-type E12 threshold without an inherited theorem

For any posterior (u,1−u,0), let q be a receiver's opponent policy distribution.
That receiver's pure payoffs satisfy

    U(A)+U(B)=c(q_A+q_B)+b−2e,
    2U(C)=2c q_C.

For e<b/2−c, their difference is b−2e+c−3c q_C>0,
since q_C≤1 and c≥0. Thus at least one of A,B strictly beats C; no best-response
mixture assigns C positive probability. If receiver 1 chooses A with probability
α, the two possible advocates obtain ηα and η(1−α). Deterring both requires
ηα−k12≤v and η(1−α)−k12≤v, which sum to k12≥η/2−v.
Conversely the half/half posterior and half/half policy mixtures form a Nash
equilibrium at low fine and attain these equal benefits. At e≥b/2−c, the same
posterior makes (C,C) a Nash equilibrium; disclosure yields v−k12≤v.
These prove the claimed disjunction. On-path (C,C) is an equilibrium exactly
when e≥max{0,b(π1−π3)−c,b(π2−π3)−c}.

At singleton type 1 or 2, for e<b−c each receiver's state-preferred action beats
every other action for every opponent mixture. At e=b−c, (C,C) is an equilibrium.
This proves the singleton threshold including its weak boundary. E23 with type 3
possible admits posterior δ3, where (C,C) is always optimal.

These are existence statements with favorable selection at ties. Changing the
selection/refinement is a change of mathematical query requiring a new proof.
