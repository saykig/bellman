# First attempted falsification: an incentive boundary with no information change

18 September 2026. Analytical derivation before the proposed general theorem.

Use the previous two-receiver policy/operational game with asymmetric prior
p=(1/5,3/10,1/2), κ=0, γ=1/2, b=2,c=1/5,η=1,v=1/5. Keep L=1/10,w=1 and quality
floor .6. Now allow BOTH certificates E12={1,2}, E23={2,3}, with separate costs
k12,k23≥0. Type 3's advocate payoff remains identically zero, as in the preceding
model. Types 1 and 2 have the old policy benefits. No new sender or private
receiver information is introduced.

κ=0 forces x=(0,0,0). Every public posterior is p, with unchanged full support.
Target (C,C) is obedient without enforcement: each player's best non-C deviation
has gain b(max{p1,p2}−p3)−c=−3/5. Operational obedience holds. Thus E_ctl=0.

Certificate E23 can always be deterred by posterior δ3 and continuation (C,C):
this is strictly optimal for both receivers in state 3. Type 2 gets v as under
silence; type 3 gets zero, and neither gains after subtracting its nonnegative
cost. The posterior is attainable by sender trembles because type 3 has positive
public probability. This continuation remains valid for every e≥0.

For E12, the previous game derivation gives pooling iff e≥4/5 or k12≥3/10.
Therefore, even with overlapping certificates,

    E(k12)=4/5 for 0≤k12<3/10;  E(k12)=0 for k12≥3/10.

The prior, source law, gate, public supports, available certificate menu and
receivers' payoff functions are ALL unchanged as k12 crosses 3/10. For each
fixed e, the receiver continuation-equilibrium correspondence is identical.
A half-and-half continuation still exists; it simply ceases to satisfy the
sender inequalities below the cost threshold. No parameterized receiver
bifurcation or support change is responsible.

Conclusion: if the proposed theorem permits disclosure-cost variation, its two
conditions are insufficient even when the entire receiver-equilibrium set stays
unchanged. Calling this an “equilibrium-feasibility change” is legitimate only
if that phrase explicitly includes sender deterrence. Otherwise a third mechanism,
a binding incentive threshold without nearby strict feasible witnesses, is missing.
If “feasible” already means the entire pooling equilibrium with incentives, the
claim needs a substantive lower-continuity condition, not the assertion that some
higher-fine pooling equilibrium continues to exist (it does at e=4/5).

This counterexample does not settle the information-only question. There the
receiver and sender payoffs are fixed, and the free off-path posterior set is
constant on a support region. That additional fact may give a strong positive
continuity result; it is the next target.

## An information-only counterexample to an OVERGENERAL claim

Theorem I uses the entire convex KL fibre. If this premise is dropped, a budget
change alone can jump the fine while every possible posterior has the same support.
Keep p=(1/5,3/10,1/2), γ=4/5, b=2,c=1/5, k12=k23=2/5, L=1/10,w=1. Restrict the
source catalogue to two laws x^0=(0,0,0), x^1=(-4/5,4/5,-4/5), retaining laws whose
KL cost is at most κ. The second law costs κ0=F(4/5).

For κ<κ0 only x^0 is admitted and the minimum fine is zero. At κ≥κ0, x^1 is
admitted too. At h=+1 its posterior has

    π2−π3 = [(3/10)(41/25)−(1/2)(9/25)]/(93/125)=13/31.

Thus the exact controlled fine there is 2·13/31−1/5=99/155. The other policy
constraint and h=−1 are smaller, verified directly. Operations remain obedient
because |m|≤8/25 and the gate is sufficiently accurate. E12 costs exceed 3/10;
E23 retains its type-3 continuation. Both certificates therefore add no fine.
Every type has positive likelihood: 1+γh x_z≥9/25>0.

The jump 0→99/155 occurs with fixed payoffs, costs, gate, prior and posterior
support, and unchanged continuation equilibria. The missing mechanism is the
failure of lower continuity of the ADMISSIBLE LAW CORRESPONDENCE as the discrete
catalogue expands. This is outside the declared full-KL-family theorem, but refutes
an unrestricted “only type support or equilibrium loss” claim. A general boundary
classification must include information-feasibility changes, not just support.
