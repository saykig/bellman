# Sequential credibility: shared consistency witnesses

8 September 2026. Additive mathematical review and extension of the preliminary
[assessed formulation](BELLMAN_SEQUENTIAL_CREDIBILITY_UNDER_UNCERTAINTY.md) at PR #22
head `19e1904bfd96e8d0eb926ac630193b9f0b1d4265`. That edition and its recorded checks
remain frozen. This is an analytical derivation, not formal proof or external peer acceptance.

## 1. Subject and query

Retain the finite perfect-recall tree family, common behavioral profile sigma,
model-specific fixed chance laws and utilities, and assessed beliefs mu of the draft.
Information sets determine both the proposed strategy and every continuation deviation.
Use the draft's **full-continuation** maximum D*, not a root or single-action substitute.
The unresolved model is fixed throughout each interaction; the family has no probability weights.

The new query is whether this supplied assessment has a **shared consistency witness**
and whether D* <= the separately supplied tolerance epsilon. Shared consistency means

    exists (sigma_n) common to every model, completely mixed, sigma_n -> sigma,
    such that for every m,I,h in I, Bayes_m(sigma_n)(h|I) -> mu_m(h|I).

This is stronger than `for every m, exists a sequence for m`. Neither statement is a
preference rule under ambiguity. At epsilon=0, shared consistency and D*=0 imply that
(sigma,mu_m) is a sequential equilibrium of each supplied game m. This is a family of
ordinary expected-utility equilibrium statements with a shared witness, **not** an
equilibrium theory of agents who have ambiguity-sensitive preferences. For epsilon>0
we report a consistent assessment with a continuation-gain bound, not exact equilibrium.

Structural chance zeros are kept fixed. Every assessed information set must contain a
node with a positive chance-only prefix product; otherwise Bayes is undefined even
under completely mixed player strategies. Such a subject is outside this witness
profile. Zero chance branches to terminals do not by themselves invalidate the query.

## 2. Established route and selected boundary

Dilmé, *A characterization of consistent assessments using power sequences of strategy
profiles*, IJGT 53 (2024), 673–693, [Definition 3.1, Theorem 3.1 and Proposition 4.2](https://link.springer.com/article/10.1007/s00182-023-00874-z),
characterizes consistency by powers and permits integer exponents. The coefficient
domain is positive reals. We specialize the sufficient direction with rational
coefficients and bounded positive integer exponents; we do not implement the paper's
necessity argument or claim that bounded rational witness search is complete. Its
ordinary game assumes positive chance actions; the direct argument below explicitly
handles fixed structural zeros under the preceding reachability restriction.

This is a material bridge beyond on-path Bayes: one finite witness determines all
off-path beliefs jointly, including restrictions caused by the same action being
used in several histories and by changing the model's chance law. Generic continuous
uncertainty and general history reduction remain separate gates. No novelty is claimed.

## 3. Construction and proof

For every zero-probability action a at information set I supply c[I,a]>0 and an integer
k[I,a]>=1. These are indexed only by information set and action, never by model or
hidden node. Write Z_I(t)=sum_{a:sigma[I,a]=0} c[I,a] t^k[I,a], and define

    sigma_t[I,a] = c[I,a] t^k[I,a]             if sigma[I,a]=0,
                   sigma[I,a](1-Z_I(t))      otherwise.

Let C=max_I sum_{a:sigma[I,a]=0} c[I,a] and t0=1/(1+C). For 0<t<t0,
Z_I(t)<=Ct<1 (also when C=0). All action probabilities are positive, sum to one,
and converge to sigma. Thus t_n=t0/(n+1) supplies an actual common completely mixed
sequence. The perturbation need not itself be an equilibrium or be optimal at any n.

For node h with positive chance-only prefix mass, define r_h as the sum of k over
zero-profile player actions on its root prefix. Let L_m(h) be the product of fixed
chance probabilities, positive-profile action probabilities, and c for zero-profile
actions along that prefix. All factors are positive. The prefix probability is

    P_m,t(h) = t^r_h (L_m(h)+o(1)).

This follows by multiplying finitely many factors: supported player factors tend to
their positive sigma values and have order zero; unsupported player factors are exact
monomials; chance factors are constant. A zero chance factor instead makes the entire
prefix identically zero. Put r_m,I=min r_h over positive-chance nodes of I and
S_m,I=sum_{h in I:r_h=r_m,I} L_m(h). The restriction in section 1 gives S_m,I>0.
Dividing every prefix by t^r_m,I yields the exact limiting belief

    mu^w_m(h|I) = L_m(h)/S_m,I   if h has positive chance prefix and r_h=r_m,I,
                  0             otherwise.                         (C1)

**Theorem (sufficient shared consistency).** If (C1) equals the supplied assessment
at every m,I,h, the single sequence sigma_{t_n} witnesses its consistency in every
model simultaneously. Conversely, (C1) is necessary for this specified witness to
support the supplied assessment. This is an if-and-only-if for a *given witness*,
not a complete decision procedure for existence of any witness.

**Proof.** The normalized family is completely mixed and converges as shown above.
There are finitely many nodes and models. At each information set its positive
leading sum prevents cancellation; division gives (C1). Hence all component limits
hold along the same sequence. Failure of an equality proves that this sequence has
a different limit, not that every possible sequence fails. QED.

**Corollary (credibility with consistent assessments).** Combine this theorem with
draft Propositions 1–2 on the *identical subject and tolerance*. At epsilon=0 the
supplied assessment satisfies consistency and sequential rationality, the two defining
requirements of sequential equilibrium, separately in every game. No prior on M,
hidden-model strategy selection, participation conclusion, or empirical prediction
is introduced. For epsilon>0 retain the exact conditional gain bound without an
equilibrium label. Full continuations make this corollary independent of any additional
one-shot deviation principle for arbitrary off-path beliefs. QED.

## 4. Decisive impossibilities and non-implications

**Incompatible off-path assessments within one game.** A chooses O,L,R and proposes O.
O pays A=1; either other action pays A=0. After L or R, chance independently routes
to J or K with probability 1/2 each. B observes the route but not L/R, and guesses
left/right, receiving 1 for a correct guess and 0 otherwise. B proposes left at J,
right at K. Assess mu_J(L)=1 and mu_K(L)=0. Every full-continuation incentive is
nonpositive, so the draft's exact assessment-relative check passes. But for *every*
completely mixed strategy, both posteriors equal sigma(L)/(sigma(L)+sigma(R)). Their
limits cannot be 1 and 0. This rules out consistency of this assessment, not merely
one witness and not the existence of other equilibria in this game.

**Modelwise sequences do not imply a shared sequence.** Nature selects g/b; A observes
the type and chooses exit/enter, proposing exit for both types. B sees entry only and
has one action. A receives 1 for exit and 0 for entry; B receives 0. Consider model
priors P(g)=1/2 and P(g)=1/4, both with assessed P(g|entry)=1/2. If x,y are the two
entry trembles, posterior odds are x/y in the first model and x/(3y) in the second.
Separate sequences with x/y -> 1 and x/y -> 3 exist and are individually consistent.
One common sequence cannot satisfy both limits. Modelwise sequential equilibria need
not satisfy the stronger query of this addendum.

**Equal-rate noise is insufficient.** In the evidence/bond fixture, equal withholding
rates yield posterior 1/2, not the draft's off-path probability one on bad quality.
Taking withholding order 2 for good and order 1 for bad generates that posterior.
Give the unchosen bond actions the same order at both hidden types. At withheld/no-bond
histories the relative orders are 2 versus 1; at withheld/bond histories they are
3 versus 2. Both produce probability one on bad quality. Other zero-profile actions
can have coefficient/order one. The singleton information sets require no posterior
choice. The same witness works in all four models; detection with p=1 makes some
terminal histories impossible but leaves all information sets chance-reachable.

## 5. One integrated arrangement, four connected directions

Strategic disclosure is an action with type-dependent evidence menus; it changes
prefix likelihoods rather than simply deleting models from an analyst's family.
History representation supplies the information sets, legal deviations and shared
tremble variables. Memory loss can make a profile unimplementable or change (C1),
even if on-path payoff averages are preserved. No general compression warrant follows.
Commitment and monitoring enter fixed feasible actions, chance laws and utility
consequences; they do not enforce themselves through an equilibrium label.

In the supplied fixture, with g in {1,3}, p in {1/2,1}, bond b=6 and fee zero,
the post-acceptance gain from defection under a bond is g-pb<=0. The full check is
still necessary for every other information set. Bond 5 gives gain 1/2. Fee 3/2 with
bond 6 makes good A's initial value -1/10, so rejection improves utility by 1/10 even
though bonded compliance remains optimal. These mechanism changes preserve the
consistency witness when the tree, profile, chance prefixes to information sets and
beliefs are unchanged; they require fresh incentive checks. They demonstrate why
deterrence and participation must be kept separate.

The draft's maxmin example remains decisive: L=(1,0), R=(0,1) across two models has
maxmin-optimal half mixing, but modelwise deviation gain 1/2. A uniform expected-utility
test does not solve recursive ambiguity preferences. Nor do stipulated monitor
probabilities establish causal effects. Merged causal PR #20 and separately unmerged
PR #21 do not identify a strategic information partition, evidence availability,
utility, disclosure behavior, or commitment technology.

## 6. Reuse, receiving and failure boundary

The executable warrant binds the full subject, witness and continuation certificate;
the receiving query fixes both epsilon and shared consistency semantics independently.
A valuation producer is checked by a separate receiver that constructs complete
prefix polynomials using SymPy exact rational arithmetic. It compares every limiting
posterior and invokes the unchanged draft's independent full-continuation receiver.
The symbolic receiver does not import the valuation producer. Shared structural
validation, Python and exact arithmetic remain trusted infrastructure.

The reference accepts rational c and 1<=k<=32. Limits beyond that are implementation
boundaries, not mathematical impossibilities. Unsupported structural reachability,
malformed witnesses, stale identity, witness-limit mismatch, and profitable deviation
remain distinct. No rejection of an arbitrary witness is labelled global inconsistency.
The two impossibilities above have separate universal analytical arguments.

Reusing a witness on a changed payoff table can preserve consistency, but not incentive
bounds. Changed chance laws, disclosure menus, information partitions, profile or beliefs
require rechecking consistency too. A bijective history renaming transports the whole
subject and witness; arbitrary merging needs a new theorem covering both deviations
and assessment consistency. Dilmé's completeness theorem does not license silently
accepting a failed bounded witness, nor certify uniform continuous-model uncertainty.
