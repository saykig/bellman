# What makes a minimum-cost profile exact?

This is established value-function/partial-minimization mathematics. KL is NOT
required for the basic exactness theorem. It matters to particular formulas and
factorizations. See the source audit for precise prior-work comparisons.

## Theorem 3: scalar profiles

There are finitely many components i. Component i has a set X_i, a retained
observable f_i:X_i→A_i, cost c_i:X_i→[0,∞), and weight w_i>0. For each nonempty
fibre f_i⁻¹(a_i), assume its cost infimum is attained. Set

    J_i(a_i)=min{c_i(x_i): f_i(x_i)=a_i},

with J_i=+∞ for an empty fibre. Assume the global set is EXACTLY the product
of local choices restricted by one budget Σw_i c_i(x_i)≤κ, for finite κ.
Then its exact observable image is

    {a: Σ_i w_i J_i(a_i)≤κ}.                         (6)

Proof. Any feasible tuple has costs at least J_i. Conversely choose a minimizer
in each fibre; independent selection is permitted and their weighted sum meets
the budget. This proves both inclusions. ∎

No probability, KL, convexity, linear f, differentiability, duality, or uniqueness
is needed. Compact X_i, continuous f_i into a Hausdorff space and lower
semicontinuous c_i are sufficient for attainment on nonempty fibres; extended
costs require a finite-cost point for a finite J. For finite X_i attainment is
automatic. Convex X_i and c_i with affine f_i additionally make J_i convex by
mixing witnesses. Suitable constraint qualifications separately license strong
Lagrange duality. Those are computational advantages, not premises for (6).

These are sufficient structural assumptions, not a claim that every violation
forces failure for every instance. For independently selectable fibres, attainment
of every finite fibre infimum is necessary for exact (6) at EVERY budget and every
observable tuple (assuming all other selected fibres have finite minima): test
κ=Σw_i J_i(a_i). At a fixed slack budget nonattainment need not matter.

If an extra constraint depends only on retained a, intersect the right side of
(6) with that constraint. If it depends on a shared hidden interface u, retain u
and use J_i(u,a_i), minimizing only after selecting ONE common u. If it depends
on additional discarded witness features, this representation is not sufficient.

## Sharp failures of tempting relaxations

1. **Infimum without attainment.** X=(0,1], f≡0, c(x)=x. Infimum J(0)=0 but no
   witness has cost≤0. The infimum test at κ=0 is a false positive. At κ>0 it works.
   Do not automatically close an epigraph if exact boundary feasibility matters.
2. **Unretained coupling.** X_1=X_2={0,1}, f_i(x)=x, c_i=0, but globally x_1=x_2.
   Each separate profile allows a_i=0 and 1; their product falsely allows (0,1).
   Retaining the common value (or the equality relation) repairs the claim.
3. **Wrong query.** Two cost sets {0} and {0,1} have minimum zero. They answer
   all upper-budget queries alike but disagree on whether cost is EXACTLY one.
   A minimum is sufficient for upper bounds, not arbitrary equality constraints.
4. **Multiple resources.** A component offers cost vectors (0,1) and (1,0).
   Separate coordinate minima (0,0) falsely meet budget (0,0). Retain the joint
   upper image of achievable vectors, or the Pareto frontier when attained.
5. **Shared unknown model.** Minimize each local component over a different hidden
   model and their minimizers may disagree. Treat that model as a shared interface;
   it cannot be independently selected just because it is not observed.

## Same source family, different information costs

For q_x(r,s)=(1+xrs)/4 against uniform r:

    KL(q_x||r)=F(x),  χ²(q_x||r)=x²,  TV(q_x,r)=|x|/2.

For a fixed public message (r,t), γ>0 and h=rt, the retained state likelihood is
 a_z=(1+γh x_z)/4. Its cost profile for ANY of the three costs is simply
 J_z(a_z)=c((4a_z−1)/(γh)) on |4a_z−1|≤γ, and +∞ otherwise.
Thus (6) recovers the exact likelihood set under each shared budget. At γ=0 only
 a_z=1/4 is attainable and its minimum cost is zero.

Quadratic support is obtained by x_i=clip(βg_i,−1,1) with the weighted quadratic
cost matching κ until saturation; this follows by completing the square/KKT.
For TV, allocating budget to decreasing |g_i| is fractional knapsack: per unit
weighted cost the return is 2|g_i|, and each coordinate's capacity is w_i/2.
The experiment tests all three profiles against direct optimization. Numerical
values at equal numeric κ do not mean equal empirical informational restriction:
KL, χ² and TV have different units/scales and sublevel sets.

## KL-specific tree shortcut fails for χ²

The earlier junction-tree minimum-KL decomposition uses the logarithm's chain
rule and I-projection identity, not just (6). Here is a strict exact failure for
Pearson χ². Let X,Y∈{−1,+1} with uniform product reference r and marginal means
α=β=1/4. The independent/Markov glue is

    q_prod(x,y)=(1+αx)(1+βy)/4,
    χ²(q_prod||r)=α²+β²+α²β²=33/256.

The alternative q_add(x,y)=(1+αx+βy)/4 is positive, has the SAME marginals and
χ²(q_add||r)=α²+β²=1/8=32/256. Every law with these marginals has the unique
form (1+αx+βy+txy)/4; orthogonality gives χ²=α²+β²+t². Since t=0 is feasible,
q_add is the unique minimum. Markov glue chooses t=αβ and is strictly worse.
So minimum-cost profiles remain exact, while a KL-specific way to compute them
cannot be transferred blindly to another divergence. This example is a two-bag
tree with empty separator, already enough to refute universal transfer.
