# Gate choice does not substitute for recovery

18 September 2026. Author-derived bounded mathematics and exact rational checks;
no independent human review, empirical validation or novelty certification.

**The answer is a boundary theorem.** Optimizing an information gate does not,
by itself, make the minimum robust fine continuous. A small example retains
uniformly positive relevant posteriors and a continuous source family, yet its
optimized fine jumps from zero to a right limit of one. But it loses the
near-optimal deterrent continuation. It therefore does **not** refute a claim
that explicitly assumes that continuation can be recovered. Under compact
closedness conditions, uniform recovery of near-optimal designs is precisely
what is necessary and sufficient for continuity.

## An information-only counterexample, with the model change visible

There is one sender, one receiver and three states with fixed prior (1/4,1/4,1/2).
The sender knows whether the state belongs to {1,2}; unlike the predecessor, it
does not know which of those two states occurred. It can disclose that certificate
or stay silent. The target is silence and receiver action C. Utilities and the
zero disclosure cost stay fixed throughout.

A binary source has probabilities (1/2+delta,1/2-delta,1/4) of its positive output
in the three states. At information parameter t, the admissible laws include all
delta in [-t,t], for 0<=t<=1/4. The institution chooses a binary gate (a,b) with
entries in [1/4,3/4] and contrast a-b>=1/4, as well as one fine for all laws.
The law is known to the players; continuations may depend on it. Every available
gate is informative and noisy. This is optimization over the declared complete
two-dimensional menu, not over unrestricted channels.

Receiver actions A,B,C have state payoffs (2,1,0), (0,1,0), (0,0,3), respectively
when the rows are read by state. A and B pay the same fine. The eligible sender
gets 1,0,1/5 at those actions. The exact table and timing are in the
[counterexample](../math/COUNTEREXAMPLE.md).

C is strictly optimal after silence even at zero fine. After the certificate,
sequential consistency pins the receiver's belief: sender trembles at a single
information set cannot vary between states 1 and 2. At t=0 the receiver can choose
B, which deters disclosure. Every nonzero perturbation creates a law and public
history where A strictly beats B. Until the fine reaches A's advantage over C,
A is uniquely optimal and disclosure is profitable. Mixed responses cannot help.

Writing d=a-b and w=(a+b)/2, the exact robust fine at a given gate is
1+d*t/min(w,1-w) for t>0, and zero at t=0. Since d>=1/4 and min(w,1-w)<=1/2,
the optimal gate is (5/8,3/8), yielding

    V(0)=0;       V(t)=1+t/2 for 0<t<=1/4.

All public posteriors have positive mass on all three states. After the certificate,
both eligible states have probabilities in [3/8,5/8]; state 3 is excluded by the
certificate itself. This is full support relative to physical eligibility, with
no changing support and no vanishing likelihood. The interval source family is
Hausdorff continuous and the gate menu is fixed compact.

Some receiver equilibrium always exists. A high-fine C deterrent persists uniformly.
The low-fine B deterrent does not. The fine discontinuity is therefore a loss of
near-optimal recovery, not evidence against a theorem assuming such recovery.
The example is small, not proved globally minimal.

Two controls isolate the boundary. If the sender instead knows the exact state,
it can support the equal certificate posterior using type-dependent trembles,
and zero fine works everywhere. If the institution can choose an uninformative
gate, zero fine also works everywhere. Weak PBE with arbitrary off-path beliefs
likewise removes the jump. These are different models or equilibrium queries;
none may inherit the counterexample unchanged.

## The positive and exact recovery results

For the fully informed public model, [F1](../math/FULL_INFORMATION.md) proves
that at a fixed fine the off-path witness sets do not change with positive-support
information. That excludes the attempted continuation-switch mechanism in the
preceding model; it does not prove all multi-receiver value continuity.

For one receiver, [F2](../math/FULL_INFORMATION.md) adds a useful primitive result.
With fixed state/action utilities, nonnegative disclosure costs and a uniform fine
on non-C actions, the set of deterrent fines is an attained upward interval.
At a witness belief, non-C best actions keep their ordering as the fine rises;
retain the deterring mixture until C becomes optimal, then switch to C. Thus the
optimized value is the minimum over gates of the maximum of a continuous on-path
threshold and a constant disclosure threshold. Continuous compact source and gate
sets make that value continuous. This route does not assume strict inequalities
or a unique equilibrium.

For broader finite continuation games, [R1–R3](../math/RECOVERY_THEOREM.md) give the
exact boundary and primitive sufficient conditions. Compact designs/witnesses,
closed feasibility and lower continuity of the admissible-law set give lower
semicontinuity. Continuity then holds exactly when every neighborhood of the old
minimum fine contains a common gate/fine design feasible for all nearby laws.
The particular old gate or equilibrium need not survive. Strict receiver and
sender incentive margins, admissible continuous belief branches and compactness
can establish this uniform recovery by a finite-cover argument. Mere equilibrium
existence cannot.

This is established compact parametric optimization, specialized carefully to
its quantifier order. Gate selection enlarges the choice set; it does not create
missing recovery. The strongest reading of the proposed smoothing claim is true
with these additional compactness/closedness premises. Its weak reading is false.

## Evidence, prior art and what this earns

The proofs cover the continuum. The [separate original-cell checker](../experiments/README.md)
checks 2,025 rational law/gate cases, receiver payoff breakpoints and mixtures,
support bounds and both controls. It rejects wrong-value and stale-identity
packets without executing the candidate producer. These checks are neither formal
verification nor evidence that the human model is empirically appropriate.

The [primary-source comparison](../sources/NOTES.md) places recovery in established
parametric optimization, common deterrent witnesses in belief-based signaling,
and communication discontinuities alongside existing institutional-credibility
results. No new general theorem or publication novelty is claimed. The useful
result is the precise model boundary and a reproducible small diagnostic witness.

Bellman must retain the sender's information partition and equilibrium consistency
rule alongside the law family, gate menu, support and common-witness quantifiers.
A posterior support label alone loses necessary information. This closes the
bounded question without adding networks, senders, a numerical frontier or an
engineering adapter. No Writ/Decision Lab work or GitHub Release is authorized.
