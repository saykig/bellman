# A fixed-payoff, fixed-prior optimized discontinuity

Author analytical result, 18 September 2026. This is a small witness, not a proof
of global minimality. It changes the sender's information partition relative to
the predecessor. It uses sequentially consistent pooling assessments, not weak
PBE with arbitrary off-path beliefs. Neither distinction may be suppressed.

## 1. Finite game and design query

There is one sender, one receiver, and exactly three payoff states theta=1,2,3.
The prior is permanently p=(1/4,1/4,1/2). A binary chance signal S has law Q_delta:

| State | P(S=+ | theta) |
|---|---:|
| 1 | 1/2+delta |
| 2 | 1/2-delta |
| 3 | 1/4 |

The source family is X(t)={Q_delta: -t<=delta<=t}, 0<=t<=1/4. The actual law is
known to both players. One gate and fine must work for all laws; equilibrium
continuations may depend on that known law. Q_delta denotes the joint law of
(theta,S), including the fixed prior. This is a nontrivial interval ambiguity
family for t>0, Hausdorff continuous including at zero. All source cells are
positive. Only information changes; utilities, prior and costs do not.

The institution chooses a binary channel with

    a=P(T=+|S=+), b=P(T=+|S=-),
    G={ (a,b): 1/4<=a,b<=3/4, a-b>=1/4 }.

This compact two-dimensional menu is fixed. Output orientation is immaterial;
relabeling T covers b-a>=1/4. Every gate is strictly informative about S and
non-perfect. It is also informative about theta at delta=0: the probability of
T=+ given theta in {1,2} differs from its probability given theta=3. Optimization
is over ALL gates in this stated menu, not over every imaginable information
technology. The positive contrast requirement is an exogenous design constraint.

S is unobserved by the players. Both see T. The sender additionally observes only
J=1[theta in {1,2}], not theta itself. If J=1 it can stay silent or send the hard
certificate E={1,2}; if J=0 it can only stay silent. The disclosure cost is zero.
The receiver observes the message and T and chooses A,B,C. Utilities before fines:

| State | Receiver A | Receiver B | Receiver C | Sender A | Sender B | Sender C |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 1 | 0 | 1 | 0 | 1/5 |
| 2 | 0 | 1 | 0 | 1 | 0 | 1/5 |
| 3 | 0 | 0 | 3 | 0 | 0 | 0 |

Fine e>=0 is subtracted from receiver utilities at A and B, never at C. It is not
a sender transfer. The target is silence by the sender and C after silence for
both T realizations. Seek existence of a sequential equilibrium with that target,
using favorable selection at receiver ties. Mixed receiver actions are allowed.

Nature's random signals do not add payoff states. All randomness and information
sets above are explicit. There are no extra senders, strategic receivers or networks.

## 2. Beliefs, support, and why consistency matters

Write d=a-b and w=(a+b)/2. Conditional likelihoods of T=+ are

    l1=w+d*delta, l2=w-d*delta, l3=w-d/4.

Every l_z and 1-l_z is in [1/4,3/4]. Thus the public posterior after silence
has full support on {1,2,3}, with each probability at least p_z/3 (at least 1/12).

For any completely mixed sender perturbation, the probability of E given J=1,T
is one number: it cannot depend on whether theta=1 or 2. It cancels from Bayes'
rule. Therefore the posterior after E is uniquely forced to be

    mu_+(1) = 1/2 + d*delta/(2w),
    mu_-(1) = 1/2 - d*delta/(2(1-w)),
    mu_h(2) = 1-mu_h(1), mu_h(3)=0.                    (C1)

These beliefs are obtained by sending E with probability epsilon at each eligible
sender information set, with silence otherwise, and letting epsilon decrease to
zero; receiver trembles can also be added. On-path beliefs converge to the prior
conditioned on T. Hence the specified assessments are sequentially consistent.

Because d/w<=1 and d/(1-w)<=1 on G, both eligible-state posterior probabilities
lie in [3/8,5/8]. They retain full support RELATIVE TO the certificate {1,2}, with
a uniform lower bound. It would be logically impossible to require positive mass
on state 3 after a truthful certificate excluding it. Sender beliefs likewise have
full support on the states compatible with J, not on incompatible states.

Weak PBE imposing only Bayes on path permits arbitrary beliefs after the unused
certificate. That weaker solution concept would allow (1/2,1/2,0) at every history
and destroys this counterexample. Use sequential equilibrium (or explicitly
Bayes-consistent off-path assessments) throughout this example.

## 3. Target C is always strictly optimal on path at zero fine

Use unnormalized expected payoffs. At T=+, C minus A equals

    (1/2)[2w-d(3/4+delta)] > 0,

and C minus B equals (1/2)[2w-3d/4]>0. Since b>=1/4,
2w>=d+1/2, and delta<=1/4, the first bracket is at least 1/2.
At T=-, the corresponding brackets are

    2(1-w)+d(3/4+delta), and 2(1-w)+3d/4,

both strictly positive. Increasing e strengthens C relative to A,B. Thus no
on-path instability or changing target feasibility explains the jump.

## 4. Exact continuation condition, including all mixtures

At posterior (q,1-q,0), receiver payoffs are (2q-e,1-e,0).
The sender gets (1,0,1/5) from (A,B,C) and 1/5 from silence.

If q<=1/2, B is a best response when e<=1 and C is a best response when e>=1;
either deters. At q=1/2,e=0, B ties A and deters strictly.
If q>1/2 and e<2q, A is the UNIQUE best response: A beats B by 2q-1>0 and C
by 2q-e>0. No mixture deters. At e=2q, A and C tie and pure C deters weakly;
for e>2q pure C is optimal and deters. This proves necessity against every mixed
continuation, not just a finite search over pure equilibria.

At delta=0 both public histories have q=1/2 and e=0 works. For any nonzero delta
one of the two histories has q>1/2. Robustness over [-t,t] gives, for t>0,

    E(t,a,b)=1 + d*t/min(w,1-w).                       (C2)

The maximizing sign of delta can depend on the public history. This maximization
is valid because the requirement is FOR EVERY law AND EVERY positive history;
it does not combine different laws in a single expected-payoff expression.
The bound is attained by delta=+t,T=+ or delta=-t,T=-, whichever denominator
is smaller. At the proposed fine C after E is optimal at every law/history,
so sufficiency uses one feasible design across the entire law family.

## 5. Gate optimization and exact answer

Since d>=1/4 and min(w,1-w)<=1/2, the ratio in (C2) is at least 1/2.
Equality is attained at a=5/8,b=3/8. Consequently

    V(0)=0,
    V(t)=1+t/2 for 0<t<=1/4.                          (C3)

The optimum is attained. A fine cap of 2 suffices uniformly. At zero, every gate
is optimal. For t>0, the displayed orientation has the unique minimizing gate.
The right limit at zero is 1, not V(0)=0. All source and gate probabilities and
all relevant relative-support posteriors remain uniformly positive.

The disappearing object is low-fine best response B at the harmful certificate
history. For each fixed e<1 it vanishes under an arbitrarily small positive
perturbation with the appropriate sign. Equilibria still exist, and the high-fine
C deterrent persists uniformly (e=2). Thus existence of SOME deterrent at some
fine is inadequate. The witness violates persistence of NEAR-OPTIMAL deterrents;
it is not a refutation of a hypothesis that actually assumes such recovery.

## 6. Decisive controls and the exact boundary of this witness

* Fully informed sender: if it sees theta, choose tremble probabilities proportional
  to mu_z/pi_z separately at each T. Then mu=(1/2,1/2,0) is attainable after E for
  every law and gate. B at e=0 deters both types, while C remains optimal on path.
  Hence V_full(t)=0 throughout. The changed sender information is load-bearing.
* Permit an uninformative gate a=b=1/2: then mu=(1/2,1/2,0) and V(t)=0. Hence
  a noisy gate's availability is different from a gate able to erase the relevant
  distinction. An unrestricted-all-channels smoothing claim is NOT refuted here.
* Permit every strictly informative symmetric noisy gate, without a positive
  contrast floor, but exclude d=0: for t>0 the infimum is 1, not attained; at
  t=0 it is zero. Arbitrarily small positive informativeness alone still fails,
  and calling that infimum a minimum would be wrong.
* Fix the singleton source family {Q_delta} instead of the interval. Its value
  is zero at delta=0 and at least 1 for every delta!=0 under the same gate menu.
  Robust ambiguity is therefore not essential to the mechanism.

One receiver and three actions suffice. Three states are as requested; the third
makes the silent target attractive while being excluded by the certificate.
No theorem excludes other mechanisms with two actions or states, alternative
certificates or different enforcement instruments. Global minimality is unproved.
