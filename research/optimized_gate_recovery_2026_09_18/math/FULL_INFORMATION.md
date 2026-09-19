# What full state knowledge changes

## F1. Fixed-fine invariance lemma (any finite number of public receivers)

Suppose one sender knows theta, all receivers have only public information, utilities
and message costs depend only on theta and terminal actions, and a fixed hard
certificate menu has eligible sets E_m. At every public history all theta have
positive probability. The target pools on silence. No equilibrium refinement
beyond sequential consistency is imposed. The law is known to the players.

At a fixed fine, the set of achievable certificate posterior / receiver-Nash /
sender-deviation-payoff witnesses is independent of the positive pre-certificate
posterior, source law and public gate. It depends on the eligible set and fixed
utilities, including the fine. In particular, information variation on this
support region cannot remove an off-path continuation at a FIXED fine.

Proof. If the public posterior is pi>0 and desired message posterior is mu_m in
Delta(E_m), set the type-z message probability to

    epsilon * mu_m(z)/pi(z) + epsilon^2

for each eligible message, zero for ineligible messages, and use residual silence.
For small epsilon the probabilities are feasible simultaneously for the finite
menu and histories. Bayes' rule converges to each mu_m. All receiver games and
sender typewise gains at these beliefs use the same fixed utilities. Conversely
physical feasibility forces every message belief to lie in Delta(E_m). Product
receiver trembles can be added; only limiting optimality is needed. QED.

The lemma does NOT prove optimized value continuity with multiple receivers.
The set of deterrent fines could have its own geometry; on-path thresholds and
operational requirements still move. It excludes one proposed mechanism only.
It also does not cover receiver private information, payoff-relevant hidden source
variables beyond theta, stronger refinements, or unknown-law common equilibria.

## F2. A primitive smoothing theorem for one receiver

Add: one receiver, finite actions including fixed target C; fine e subtracts the
same amount from every action other than C; all disclosure costs are nonnegative;
sender's payoff at action C is the same after disclosure as after silence before
message cost. Source and gate affect neither terminal utilities nor costs. For
all messages choose beliefs in fixed compact sets B_m subset Delta(E_m) that can
be implemented by the preceding trembles. B_m=Delta(E_m) is allowed; a trimmed
simplex mu(z)>=eta>0 is allowed if one wants uniformly positive chosen beliefs.
An OPEN full-support simplex alone does not supply compact attainment.

Let D_m be the fines admitting a single posterior and receiver best-response
mixture that deters EVERY eligible sender type. D_m is closed by compactness and
continuous finite inequalities. It is nonempty for a sufficiently large finite
fine, which makes C optimal at every posterior. Crucially it is upward closed.

Proof of upward closure. Keep a witness posterior mu at fine e. All non-C pure
actions shift by the same amount as the fine rises. If C is already a best
response, choose pure C at all larger fines; nonnegative costs deter every type.
Otherwise all support actions of the witness mixture are non-C and remain best
responses until C catches them. Retain the same mixture until that point and
choose C from then on. Sender gains are unchanged before the switch and nonpositive
after it. QED. Thus D_m=[d_m,infinity), with d_m attained. Put d*=max_m d_m.

For information parameter lambda and admissible gate g, let

    c(lambda,g)=max(0, max_{q in X(lambda,g),h,a!=C}
                           E_q[u_R(a,theta)-u_R(C,theta)|h,g]).

Assume a fixed finite history set, continuous joint probability cells, uniformly
positive public history probabilities locally, and a nonempty compact continuous
law correspondence X on the admissible gate graph. Then c is continuous by the
compact maximum theorem. Let G(lambda) be nonempty compact continuous with a
common compact gate space. Any operational constraints must already be encoded
in this continuous G, without coupling to the fine. Then

    V(lambda)=min_{g in G(lambda)} max(c(lambda,g),d*)             (F1)

is continuous, and all minima are attained. Choose a locally uniform fine cap
above the finite utility differences if compact design space is desired.

Proof. F1 makes all off-path tests independent of information at fixed e; the
upward-closure argument makes their intersection [d*,infinity). Target optimality
is exactly e>=c. Independent certificate beliefs are simultaneously consistent
by the finite tremble construction. The formula follows, and minimizing its
continuous objective over compact continuous G proves continuity. QED.

This theorem does not need a strictly informative gate: the decisive conditions
are attainable invariant beliefs, the common fine shift and continuous design
feasibility. It provides a primitive positive result beyond assuming value
recovery itself. It is a specialization of familiar best-response and compact
optimization arguments, not a new general maximum theorem.

In the counterexample with the sender upgraded to full information, take
B_E={(1/2,1/2,0)}. B deters at e=0, hence d*=0; c=0 for every gate. Formula (F1)
gives V_full=0. With the coarsely informed sender the fixed set B_E is no longer
implementable: beliefs are pinned by (C1). That is the precise broken premise.
