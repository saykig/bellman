# Voluntary verifiable disclosure after the controlled gate

Analytical result, 18 September 2026. This is a new specified extension of the
supplied game, not a reinterpretation of its already-public report as disclosure.

## Protocol and solution concept

Keep the binary gate, game, and uniform (θ,R) marginal of BINARY_FRONTIER.md.
Add a third actor D, a policy advocate, whose only terminal benefit is

    U_D=η 1{x_1=θ} − k 1{a certificate is disclosed},   η>0, k≥0.

D is not either action player. Nature draws Q, then θ,R,S; the committed gate
draws T. In each analyst candidate, Q is common knowledge. The action players
initially know R,T, not θ,S or the gate's seed. D privately learns θ through a
perfect, authenticated record and also sees public R,T; D does not learn S or
the seed. D can publicly send silence ∅ or certificate cert(θ), then both players
choose their two actions simultaneously. No other communication or acquisition
is allowed. Verification means cert(θ) cannot be fabricated in state −θ. The
binary type has no nontrivial partial certificate; silence and the full certificate
are the complete menu. Nonbinary partial disclosure is a later extension.

The gate and the policy penalty e are committed before types; D cannot commit
to conceal evidence in the voluntary baseline. Monitoring/enforcement remain the
same credible external primitives. Disclosure has direct cost k to D, not a
policy-deviation fine. k=0 is the central voluntary-sharing case. After a
certificate, players update to θ with certainty and play a continuation Nash
equilibrium. After silence they update using D's actual disclosure strategy;
silence is NOT assumed uninformative outside the pooling candidate.

We ask for existence of a perfect Bayesian equilibrium (PBE) in which D always
remains silent and x_i=R,y_i=T at every on-path information set. This preserves
the controlled arrangement, not merely some cooperative-looking aggregate.
Robustness means such a PBE exists for every Q in the fixed family, with the same
gate, penalty, and pooling disclosure rule. Continuation beliefs may depend on
Q as players know it. We do not claim equilibrium uniqueness or selection.

## Lemma: disclosed-state policy continuation

For 0≤e<b−c and known θ, the player whose preferred sign is R strictly prefers
R regardless of the other player's policy. The other player strictly prefers
−R: matching preference gains b, while the largest coordination loss plus fine
is c+e<b. Thus the unique policy equilibrium is (θ,−θ).

For e≥b−c, (R,R) is a policy equilibrium at every θ: the opposed player's
switch gain when the other follows is b−c−e≤0. A stronger statement is not
needed; at equality the conclusion is weak obedience. Operational continuation
always has a pure symmetric equilibrium: both choose the sign maximizing
Pr(S=sign|R,T,θ), with arbitrary common tie-breaking. Changing that sign loses
L and cannot improve state matching. Additivity joins these equilibria.

## Theorem F — pooling disclosure and the enforcement frontier

Fix Q and a gate at which the original target is obedient after R,T.
Then a pooling PBE preserving that target exists iff

    e≥b−c  OR  k≥η.                                    (F1)

For e<b−c, this iff uses positive probability of θ≠R, guaranteed by the fixed
uniform (θ,R) marginal. No full-support assumption on all eight Q cells is needed.

Proof of necessity. If e<b−c and D has θ≠R, silence under the target yields
benefit zero. A truthful certificate forces the unique policy continuation with
x1=θ, giving η−k. For k<η this is strictly profitable, regardless of off-path
beliefs about S or operational equilibrium. Such types occur with probability
1/2. Pooling therefore fails. In fact no PBE that prescribes x_i=R almost surely
on path can exist in this regime: those same types either reveal on path and
break the target, or profit by revealing off path.

Proof of sufficiency. For k≥η and e<b−c, choose the known-state policy equilibrium
after any certificate and any symmetric operational equilibrium described above.
At θ≠R the net disclosure advantage is η−k≤0; at θ=R it is −k≤0.
After always-silent play, Bayes beliefs are exactly the controlled R,T posteriors,
so the assumed target is obedient. Certificates pin down θ, and Bayes applied to
Q and the known gate supplies consistent remaining beliefs. Thus these strategies
and beliefs form a PBE. For e≥b−c select (R,R) after every certificate and the
same type of operational continuation. D's policy benefit never changes, so
its disclosure advantage is −k≤0. The same construction applies. ∎

For robust design combine F1 with the controlled frontier. Put γ*=max{2q0−1,γop}
and let E_ctl be the exact shared-budget penalty at γ*. Then the minimum policy
penalty preserving pooling and the prescribed on-path arrangement is

    E_vol(k) = b−c     if 0≤k<η,
             = E_ctl if k≥η.                          (F2)

The lower bound is Theorem F; the construction above and the active-operational
bound attain it. Equality at k=η or e=b−c relies on favorable weak best-response
selection. For strict sender incentives use k>η (low e) or k>0 (high e).
With k=0, high enforcement supports silence only weakly; it does not make
nondisclosure the unique behavior.

At the supplied active benchmark κ=.3,b=2,c=1,L/w=.1,q0=.6, controlled design
needs approximately .090179225583, but a costless advocate requires 1. This
is an exact formula comparison whose displayed decimals are numerical evaluations.
It demonstrates why a technologically valid information restriction need not be
self-enforcing. Increasing policy enforcement neutralizes the benefit of disclosure;
a disclosure cost changes the advocate's incentives instead. Removing the relevant
certificate from the message menu, or an enforceable commitment to remain silent,
restores the controlled frontier. These are different institutional interventions.

## Scope and nonbinary generalization

The result concerns cooperation ON PATH under the pooling arrangement. It does
not require y_i=T after an off-path certificate. If that stronger requirement is
imposed, state revelation exposes conditional RS correlations individually:
rκ=F⁻¹(min{2κ,log 2}), and operational obedience additionally requires
γ≥max{0,(rκ−ell)/(1−ell rκ)}. This follows from the same operational posterior
calculation with u replaced by xθ. The two robustness specifications differ.

An alphabet-free necessary condition survives. For any finite sender type τ
and feasible verifiable message m, let V_target(τ) be its prescribed continuation
payoff and let V_min(τ,m) be its minimum payoff over all sequentially rational
continuations compatible with the verified content. If

    V_min(τ,m)−cost(τ,m)>V_target(τ),

no pooling equilibrium preserving the target exists when τ has positive
probability: even the least favorable credible continuation rewards disclosure.
This is proved by the single deviation and uses no binary symmetry. If each
message pins down a unique continuation payoff V(τ,m), pooling exists precisely
when the target is obedient and all the corresponding sender inequalities hold,
provided those continuations and consistent beliefs can be simultaneously chosen.
Without uniqueness, separate minima can be mutually inconsistent across types
sharing a message. A proper generalization must retain their JOINT continuation
feasibility, rather than repeat the statewise-envelope mistake at the strategic
layer. This is the next theorem target, not a proved general sufficiency claim.

Closest precedents: voluntary evidence/unraveling and certification equilibria;
Saas's disclosure-proof CE result uses payoff-irrelevant recommendation signals
and endogenous feasible punishments. Our third-party advocate has payoff-relevant
verified state information and a specified penalty; his theorem cannot be imported
as F1. These differences do not establish historical novelty.

## Theorem G — one informed sender, overlapping partial certificates

Here is an exact finite extension of the preceding necessary condition. It is a
specialization of standard sequential-rationality reasoning, to be compared with
Forges–Koessler certification equilibria, not a new revelation principle.

Fix a public history and a finite type set Ω with full-support posterior p. Only
D knows τ∈Ω. Every other player has only that public information. A message m
is feasible exactly for τ∈E_m⊆Ω, with E_m nonempty; discard impossible
messages. Silence is feasible for all types and costs zero. There are
finitely many messages and actions. After m, the action players play a Nash
equilibrium σ_m of the common-belief game with posterior μ_m on E_m. Their
utilities may depend on τ. D has no subsequent action. Let vτ(σ) be D's expected
payoff at true type τ under continuation σ and kτm its message cost.

Fix an obedient target σ0 after pooling silence. Let

    T_m = {(μ,σ): supp μ⊆E_m, σ∈NE(action game averaged under μ)}.

There is a pooling PBE with evidence-consistent beliefs iff for every m≠silence
there is ONE pair (μ_m,σ_m)∈T_m such that

    vτ(σ_m)−kτm ≤ vτ(σ0)   for ALL τ∈E_m.             (G1)

Proof. Necessity is sequential rationality for the actual common continuation
and all types that could deviate to it. For sufficiency choose the displayed
pairs, use p and σ0 after silence, and let D always remain silent. Receiver best
responses and every sender deviation inequality hold, so this is a PBE. The
beliefs can also be generated by one common sequence of sender trembles: for
every eligible τ set its probability of message m proportional to
ε μ_m(τ)/pτ + ε² (with a common sufficiently small prefactor if needed), and
assign the residual to silence. Infeasible messages keep probability zero.
Bayes' rule converges to μ_m for every m simultaneously. Independent action
perturbations converge to σ_m. Thus no mutually inconsistent choice of off-path
beliefs has been silently used. This supports sequential consistency in the
finite perfect-recall game, as well as the stated PBE conclusion. ∎

This theorem does not permit a separate σ_m for each hidden type: the receivers
do not observe which type sent the same certificate. Shared private receiver
information, multiple informed senders, or restrictions coupling continuation
randomizations require a richer T and new consistency analysis.

### Exact nonbinary counterexample: separately credible punishments do not compose

There are three sender types with prior (1/4,1/4,1/2), and one receiver with actions
A,B,C. Receiver payoff is 1 for choosing the action matching types 1,2,3 respectively,
and 0 otherwise. Before evidence, C is the unique best response. Sender payoffs:

| True type | A | B | C |
|---|---:|---:|---:|
| 1 | 1 | 0 | 1/5 |
| 2 | 0 | 1 | 1/5 |
| 3 | 0 | 0 | 0 |

Types 1 and 2 possess the same verifiable partial certificate E={1,2}; type 3
cannot send it. Every type can remain silent. No full-type certificate is available.
The sender initially knows its type; the receiver knows only the prior. Disclosure
is public, costs k, and changes beliefs but not these utilities or available actions.

After the certificate C is strictly inferior. Any continuation uses A with
probability q and B with probability 1−q. Both pure outcomes are credible under
appropriate posteriors; every q∈[0,1] is credible at posterior (1/2,1/2,0), where
the receiver is indifferent. Thus each type SEPARATELY has a credible punishment
paying 0, less than its pooling payoff 1/5. Nevertheless G1 jointly requires

    q−k≤1/5,       1−q−k≤1/5.

Adding yields k≥3/10; for k=3/10 choose q=1/2 and that same posterior.
Therefore pooling is possible iff k≥3/10. At k=0 separate typewise minima falsely
certify feasibility. This is an exact impossibility and a sharp restoration
threshold, proved algebraically. It is not a numerical equilibrium search.

The same compatibility issue therefore appears twice: statewise probability
extrema can be incompatible under one budget, and typewise disclosure deterrents
can be incompatible under one publicly observed certificate. The second phenomenon
is not solved by retaining a better probability scalar. It requires a joint set
of credible continuation PAYOFF VECTORS. This example strengthens the disclosure
extension as a research direction, while ruling out a naive independent-punishment
summary. General certification-equilibrium theory remains the natural host.
