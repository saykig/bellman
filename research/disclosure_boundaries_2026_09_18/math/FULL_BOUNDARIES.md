# Second layer: all parameters, and a general regular-region theorem

This follows the information-only Theorem I. Its model-specific classification
is exact. The more general theorem is a standard parametric-optimization
specialization, with explicit regularity assumptions and counterexamples to
omitting them. Neither is claimed as a new general maximum theorem.

## Exact full classification within the declared payoff family

Now let p,κ,γ,b,c,L,w,q0,η,v,k12,k23 vary continuously in the domain specified in
INFORMATION_THEOREM.md, including b>2c>0,η>2v>0 and operational feasibility.
No preference ordering, action menu, sender information or message eligibility is
changed. Define the continuous functions C,a,H,t,T,κ12,κ23 as there, and flags

    A(λ)=1[k12<t],
    B(λ)=1[γ=1 and ((κ≥κ12 and k12<T) or (κ≥κ23 and k23<T))].

The SAME proved formula holds pointwise:

    E(λ)=V_A,B(λ),
    V_0,0=C; V_1,0=max{C,a}; V_0,1=V_1,1=H.          (F1)

C remains continuous jointly with these payoffs: it is a continuous compact
maximum, followed by continuous max and scaling. For each flag pair σ, let
D_σ={λ:(A(λ),B(λ))=σ}, with closure taken relative to the parameter domain.

**Theorem F (necessary and sufficient boundary test).** E is continuous at λ0
iff V_σ(λ0)=E(λ0) for EVERY σ such that λ0∈closure(D_σ).

Proof. Every sequence λ_n→λ0 has a subsequence in one of the finitely many phases.
Along a fixed phase its value tends to V_σ(λ0). Conversely membership in a phase
closure supplies such an approaching sequence. Equality of all attainable phase
limits is exactly sequential continuity. ∎

This is not a numerical sign test at λ0: weak and strict inequalities determine
which neighboring phases can actually approach it. Impossible combinations of
flags must not be invented. The criterion handles masking and intersections.

Only the following loci can separate phases:

- γ=1 and the relevant source budget faces κ=κ12(p), κ=κ23(p);
- k12=t, the joint partial-certificate deterrence threshold;
- k12=T or k23=T when the corresponding singleton support regime is attainable.

Changes of which player maximizes C, or C crossing a or H, cause kinks or mask
jumps but do not themselves create discontinuities. Within this declared payoff
family there is no separate receiver-equilibrium-driven jump: varying b,c moves
a and H continuously. The possible jumps from η,v variation are ordinary sender
incentive thresholds. The strict domain assumptions exclude changes of preference
ordering and new game forms. No smooth-surface claim is needed at intersections.

The first counterexample in COUNTEREXAMPLES_FIRST.md is an incentive-only jump:
k12 crosses t while every receiver game remains unchanged. Theorem F also says
when that candidate jump is masked by C≥a or by a singleton requirement H.

## General fixed-support finite-game formulation

Let λ be a parameter in a metric space, e in a fixed compact interval [0,Hbar],
and X(λ) a nonempty compact set of candidate laws. There are finitely many public
histories and certificate messages. At each (λ,e,x,h,m), let T(λ,e,x,h,m) be the
nonempty compact set of admissible posterior/receiver-equilibrium pairs. It must
encode physical support, the actual information structure and the selected
notion of equilibrium. Let g(λ,e,x,h) be the maximum on-path deviation gain, and
let d_j(λ,e,x,h,m,t) be the sender's gain for eligible type j from continuation t.
Eligibility and the relevant positive-probability public histories are fixed in
the regular region. Define

    R(λ,e)=max{ sup_{x,h} g(λ,e,x,h),
                sup_{x,h,m} min_{t∈T(λ,e,x,h,m)} max_j d_j(λ,e,x,h,m,t) }.

Then Γ(λ)={e∈[0,Hbar]:R(λ,e)≤0} and E(λ)=min Γ(λ), when nonempty. This precisely
retains the quantifier ∀law/history/message ∃common continuation ∀eligible type.
It does not impose one law-unobservable equilibrium across all models.

**Theorem R (regular-region continuity).** Suppose locally:

1. Payoff/gain functions are continuous; X is a compact continuous correspondence.
2. T is a nonempty compact continuous correspondence on the admissible graph,
   with a common compact ambient witness space. History/type eligibility does
   not change, and any posterior division has a uniform positive mass bound.
3. Γ is nonempty; fines are uniformly bounded by Hbar.
4. Near-optimal strict feasibility holds at λ0: for every ε>0 there is
   e_ε<E(λ0)+ε with R(λ0,e_ε)<0.

Then E is continuous at λ0. Strict feasibility here concerns all retained
nontrivial constraints; identities such as a type having no possible deviation
must be removed instead of demanding impossible strictness for the number zero.

Proof. Repeated compact maximum/minimum arguments give continuity of R.
Consequently Γ has closed graph and compact values. If E(λ_n) had a limiting
value strictly below E(λ0), a subsequence of minimizing fines would converge to
a feasible lower fine at λ0, contradiction. This proves lower semicontinuity.
For each ε choose the strict witness e_ε; continuity keeps it feasible in a
neighborhood, so E(λ)≤e_ε<E(λ0)+ε there. This proves upper semicontinuity. ∎

Condition 4 can be replaced by the weaker, exact recovery condition:
for every ε>0, all sufficiently nearby λ admit SOME feasible e<E(λ0)+ε.
With closed graph/compactness, this is necessary and sufficient for continuity.
It is the feasible-path/value-continuity condition from existing parametric
optimization, not a new characterization in game-theoretic clothing.

Strict feasibility is a usable sufficient condition, NOT necessary. Likewise,
full lower continuity of T is stronger than needed: persistence of near-optimal
deterrent witnesses can suffice. Strict receiver equilibria can provide local
branches, but their existence alone does not ensure sender strictness or the
robust uniform condition across all candidate laws.

The theorem's contrapositive classifies a discontinuity only relative to its
premises. At least one must fail: information/witness-set regularity (including
support and disappearing histories); equilibrium persistence; incentive/threshold
recovery; or boundedness/feasibility/continuity of the primitives. Failures can
coincide, and can be masked. Merely saying “some equilibrium remains feasible”
is insufficient. There is no general theorem with only that statement and
constant posterior support as hypotheses.

## A minimal genuine equilibrium-persistence obstruction (outside the fixed preference family)

For comparison, change the receiver payoff family while keeping a three-state
one-sender PUBLIC game with the same two certificates. This example is an
assumption test for Theorem R; it is not falsely attributed to Theorem I's game.
One receiver has actions A,B,C, fixed prior (1/5,3/10,1/2), and no informative
source. In states 1 and 2 its payoffs are (1+δ,1,0), and in state 3 they are
(0,0,3). Fine e is subtracted from A and B. Let |δ|<1/4. The advocate's payoffs
in types 1 and 2 are (1,0,1/5), and in type 3 all zero; both certificate costs
are zero. Policy C is a strict on-path best response for every e≥0.

E23 is deterred by posterior δ3 and action C, exactly as before. After E12,
receiver payoffs are (1+δ−e,1−e,0) at EVERY admissible posterior. For δ≤0,
choosing B at e=0 deters both types, hence E=0. For δ>0 and e<1+δ, A is uniquely
optimal; disclosure pays 1>1/5. At e=1+δ, C is optimal and deters. Thus

    E(δ)=0 for δ≤0,   E(δ)=1+δ for δ>0.

All type supports, costs and the information structure remain fixed. At δ=0 the
low-fine deterrent B is a best response, but it disappears for δ>0: T is upper
continuous but not lower continuous there. A receiver best response always exists,
so simple nonemptiness would miss the obstruction. Three receiver actions permit
a distinct on-path target, benign continuation and profitable continuation; the
unreachable third state separates the prior from certificate incentives. This is
a small explicit witness, not a proven globally minimal game-size theorem. It can
be embedded in the two-receiver format by giving a second receiver a strictly
dominant C action and an independent operational task; the discontinuity is unchanged.

In Theorem I's original two-receiver preference family, this mechanism cannot
occur from information variation alone; its continuation set depends on support
and fine, not the remaining information parameters. Here the added payoff
parameter changes a continuation best-response branch. This keeps the two layers
of the investigation separate.
