# Partial knowledge and causal composition: a foundation recommendation for Bellman

Research note, 17 September 2026. Bounded first investigation; no novelty claim.

Bellman should use **explicit causal mechanisms for intervention semantics,
relations over admissible mechanism choices for partial knowledge, and global
extension tests for compatibility**. Probability valuation operations can evaluate
an already justified causal factorization. These are complementary tools; there
is no demonstrated need for a new universal algebra.

In ordinary language: keep separate what could be true, how a proposed system
works, and whether several descriptions can all be true together. “Combine” means
different things in those three sentences. Choosing an operation before choosing
its meaning is the main failure risk.

## What the comparison establishes

Information algebras describe constraints well: repeat the same constraint and
nothing changes. Probability factors behave differently: using a likelihood twice
usually changes the answer. Shenoy–Shafer's axioms justify local computation once
the factors and operations are legitimate; they do not make unrelated reports
independent. [SS](../sources/NOTES.md)

Local-to-global methods ask whether local descriptions extend to one global
object. The valuation connection is already explicit in Abramsky–Carù, building
on the contextuality framework of Abramsky–Brandenburger. A compatible family
need not extend, and an extension need not be unique. [AC and AB](../sources/NOTES.md)
The database literature already identifies conditions for lossless relational
reconstruction. [BFMY](../sources/PRIOR_WORK_ADDENDUM.md)

Causal composition introduces different information: mechanisms have inputs,
outputs, owners and permitted replacements. Stochastic wiring is established
mathematics; the causal interpretation requires invariance and randomness
assumptions. Composing maps between whole models is another operation, with its
own query-preservation conditions. [F, P and RW](../sources/NOTES.md)
Recent work explicitly handles open models and component-level abstraction.
[LT](../sources/PRIOR_WORK_ADDENDUM.md)

Thus the useful bridge is a concrete representation: use relations whose entries
are *mechanism choices*, then evaluate each allowed realization causally. Do not
identify conjunction with stochastic composition. Do not erase mechanism ownership
when flattening the numerical calculation into probability factors.

The [comparison table](../COMPARISON.md) states each candidate's objects,
operations, guarantees and limitations. The [source notes](../sources/NOTES.md)
and [prior-work addendum](../sources/PRIOR_WORK_ADDENDUM.md) give direct primary
links, inspected sections and remaining literature limits.

## The bounded setting and why it was chosen

We study finite directed acyclic modules with typed ports, one owner per internal
variable, complete normalized probability tables, and named hard interventions.
Partial knowledge is a relation selecting admissible combinations from finite
catalogues of whole mechanisms. A model choice remains fixed across the answers
computed from that model. We assign no probability to the catalogue unless one
is separately supplied.

This setting is large enough to show intervention and dependency mistakes, small
enough for exact experiments, and simple enough for a useful Lean proof. It omits
feedback, unrepresented shared physical noise, statistical estimation, continuous
catalogues and joint counterfactual distributions. Those omissions delimit the
first result; they do not define Bellman's eventual foundation or ceiling.

The [mathematical development](../math/DEVELOPMENT.md) specifies all objects and
operations. In symbols, a model θ gives a joint law by multiplying its node
kernels. To intervene, replace the targeted kernels by point masses. To combine
knowledge about θ, join the corresponding relations. To forget a choice, project
that relation only when the remaining queries no longer need its dependencies.

## A result, a successful calculation, and a failed claim

We prove an exact-extension criterion: local relations have a global relation
with exactly those projections if and only if their natural join projects back
to every original relation. This is a relational specialization of established
mathematics, proved directly here. For two contexts, agreement on the common
variables suffices. On a suitable join tree this extends inductively; arbitrary
cycles do not enjoy that guarantee.

We also prove the finite causal composition result: with single ownership,
acyclic wiring and normalized kernels, replacing mechanisms before wiring or
after wiring gives the same joint law. Marginalization and evaluation over the
same admissible family preserve that equality. The proof uses normalization in
reverse topological order and equality of the replaced factors. It is a
specialization of standard semantics, not a new identification theorem.

For a concrete three-bit system X→Y→Z, take

- P(X=1)=1/4;
- P(Y=1|X=0)=1/5 and P(Y=1|X=1)=4/5;
- P(Z=1|Y=0)=1/10 and P(Z=1|Y=1)=9/10.

The modules own Y and Z separately; their shared port is Y. Direct calculation
gives P(Z=1)=19/50 and P(Z=1|do(X=1))=37/50. Setting Y to one gives
P(Z=1|do(Y=1))=9/10 and leaves P(X=1)=1/4. Merely observing Y=1 instead gives
P(X=1|Y=1)=4/7. This makes the intervention/conditioning distinction explicit.

A tempting composition rule fails even without randomness. Suppose Y=X xor a
and Z=Y xor b, with admissible choices only (a,b)=(0,0) or (1,1). Both models give
Z=X. Forgetting their shared choice and independently combining the two local
catalogues admits (0,1) and (1,0). Under do(X=0), the genuine answer P(Z=1)=0
is falsely broadened to {0,1}. That larger set is a sound outer approximation,
but it is not evidence of uncertainty within the original family. The distinction
between coupled and separately specified choices is established in credal-network
research too; its independence and convexity conventions must be stated before
reusing its algorithms. [RC](../sources/PRIOR_WORK_ADDENDUM.md)

## What was actually checked

Exact standard-library Python experiments enumerate all 4,096 binary relation
triples. Of 406 agreeing on overlaps, 166 admit exact extensions, four have no
simultaneous assignment, and 236 have nonempty joins that lose some local
possibilities. An independent oracle enumerates every global three-bit relation.
The all-empty triple is included as an exact empty extension; it is not a
nonempty compatible system.

The scripts also check 729 kernel-composition triples and 2,187 intervention
cases, comparing full factor products with sequential path expansion. All numbers
are rational or integer. They reproduce the worked example and the counterexamples.
These are exhaustive finite checks within their enumerated domains, not empirical
findings or proofs for every stochastic model.

Lean 4.33.1 verifies the two-context relational theorem, overlap gluing, the
logical parity obstruction, rectangular inclusion, and the disjoint-owner
replacement identity. The full DAG normalization and stochastic semantics remain
proved on paper, not formalized. The ownership identity uses standard function
extensionality; the other retained theorems report no axiom dependencies.
[Proof scope and reproduction](../lean/README.md)

A second exact search considers every nonempty subset of 16 pairs of deterministic
Boolean mechanisms. It finds cases where separate query ranges agree but the
joint set of attainable answer vectors changes. A short example suffices: one
model always outputs zero and another always outputs one. Recombining their
component choices can add a model that outputs one at input zero and zero at
input one. Both scalar ranges remain {0,1}; the new answer pair (1,0) was never
possible. [Derivation and counts](../math/SIGNATURE_ADDENDUM.md)

This vector records several single-regime laws of one model. It is not a joint
probability distribution of counterfactual outcomes. Preserving that distinction
prevents another unjustified promotion of the result.

## What changes for Bellman

The fetched baseline already distinguishes exact fibres from relaxations,
interventions from observations, and persistent models from rowwise choices.
This investigation supports those distinctions without treating the existing
seven-component organization as mandatory. Its principal addition is an explicit
choice of mathematical representation for partial *mechanism* knowledge and a
comparison against established alternatives.

Retain the existing saturated kernel-completion profile: its independence of
missing coordinates is explicit and valid within that profile. For coupled
mechanisms, represent the relation rather than silently extending the profile.
Keep causal direction, complete input rows, randomness assumptions and intervention
targets alongside any compiled probability factors. Preserve shared catalogue
coordinates until their constraints have been combined. Label forgetting that
introduces new models as an outer approximation unless query preservation is proved.

No migration of existing certificate code, new universal language, strategic
application or Writ/Decision Lab adapter follows from this result. The reproducible
research reference is useful without promising an engineering product.

## One tractable paper question, and the stopping rule

**For a fixed finite acyclic signature and declared intervention queries, which
local projections of a coupled mechanism catalogue can be stored and recombined
without changing the set of jointly attainable intervention-law signatures?**

Let C be the true catalogue relation, C⁺ the join of its stored projections, and
σ_Q the vector of laws for the declared queries. The exact target is

    σ_Q[C] = σ_Q[C⁺].

A finite exhaustive decision procedure already follows from elementary set images.
Lossless join dependencies supply a stronger sufficient condition C=C⁺. The
potential research contribution is a usable structural condition or smaller
query-sufficient representation, compared with those existing baselines. Novelty
is unresolved; there is no claim that an undecided mathematical bridge is required.
A synthesis paper showing that existing theory suffices is an acceptable outcome.

The next experiment should test whether a local signature reduction is preserved
when adding a downstream mechanism and an internal intervention. Use a three-module
Boolean chain and compare against exhaustive evaluation. A failure must return a
specific continuation and a full distinguishing signature; one scalar range need
not witness it. This tests safe reuse rather than accumulating more examples of
an already settled two-module phenomenon.

Remaining obstacles are catalogue adequacy, scalable representation of coupling,
shared physical noise, preservation under changed query menus, and statistical
justification of constraints. Approximation and causal abstraction across different
state spaces require additional premises. Current proofs do not resolve those
issues, and this note makes no claim about better real-world decisions yet.
