# Explicit translation to observational completeness

All mathematical instantiations below are our elementary derivations. Primary
source locators and what is borrowed are in SOURCES.md. This is a suitability
check, not a claim of a new abstract-interpretation result.

## First attempt: a family of causal models

Fix finite complete mechanisms Ω. A knowledge family C⊆Ω is ordered by inclusion:
a larger family is a less precise description. The lattice P(Ω) is complete.
Fixed-constraint addition C↦C∩R and a specified mechanism transformation C↦r[C]
are monotone, preserve arbitrary unions, and are Scott-continuous. On a finite
poset monotonicity already gives directed continuity; these particular maps have
the stronger union property.

Let σ(θ) be the vector of single-regime laws for a declared finite menu. Define
π(C)=σ⁻¹[σ[C]]. This is an upper closure operator: monotone, extensive and
idempotent. Its closed sets encode sets of jointly attainable answer vectors,
not independently selected per-query ranges or cross-world joint distributions.
Thus signature equality is an observational abstraction of P(Ω).

This attempt fails for named withdrawal. Let two separately revocable assumptions
j,k have the same nontrivial predicate R⊊Ω. Stores {j} and {j,k} both denote R.
Withdrawing j yields Ω and R respectively. Hence there is no function w_j:P(Ω)→P(Ω)
whose result agrees with named withdrawal for all stores. This is failure to define
a concrete operation, not failure of a continuity theorem. Neither causal
abstraction nor better marginal precision restores the missing source distinction.
The same issue arises when inconsistent stores all collapse to the empty family.

## Repair: a source-sensitive concrete state

Fix a finite assumption registry J with immutable predicates R_j⊆Ω, each bound
to the ORIGINAL mechanism revision. Let V be a finite set of replacement modes,
each with an explicit total map r_v:Ω→Ω_current. A concrete record is e=(A,v),
A⊆J. Its current family is

    D(e) = r_v[ ⋂_(j∈A) R_j ].

The empty intersection means Ω. A record with empty D is explicitly inconsistent;
it does not certify every query. An assumption is metadata plus its predicate,
not an independent likelihood. Same-event aliases must resolve to one source key.
Distinct revocable warrants may express the same predicate.

Addition j: (A,v)↦(A∪{j},v). Withdrawal j: (A,v)↦(A\{j},v).
Replacing the named mechanism sets v to the supplied replacement mode. It is a
physical/model transformation, not conditioning. Original assertions remain
about the original revision. New assertions about a later revision require a
new predicate pulled back through that revision map and a new registry entry.
This run's finite menu deliberately excludes those new entries. Replacing a
hypothesis instead is withdrawal plus addition; that is a different operation.

One record can contain much epistemic uncertainty. To apply abstract
interpretation, use the collecting lattice L=P(E), E=P(J)×V. Elements of L are
sets of POSSIBLE RECORDS, not distributions or additional causal latent states.
Record transitions t:E→E lift to f_t(X)={t(e):e∈X}. These maps preserve arbitrary
unions (including empty), so they are completely additive and continuous.
Start real calculations at {e}; set-valued record states describe abstraction.
A fixed incoming partial description is a sequence of addition operations.
Arbitrary two-argument joins on changing uncertain records are not automatically
covered: they require a specified product-state semantics. Currying fixed
registry descriptions suffices for this first test.

Define o(e)=σ[D(e)], with o(e)=empty flagged as inconsistent. On L define

    π(X) = {e∈E : o(e)∈{o(d):d∈X}}.

This saturates equality classes of observations and is an upper closure operator.
Let ρ:L→L be a candidate upper closure. Abstract execution interleaves ρ with
the lifted operations: ρ f_n ρ ... f_1 ρ. Extensivity and monotonicity yield a
sound overapproximation of the concrete records. Observational exactness asks,
for every X and finite permitted operation sequence,

    π(ρ f_n ρ ... f_1 ρ(X)) = π(f_n ... f_1(X)).           (OC)

This matches the source definition (up to chronological composition notation).
The empty sequence demands exact current observations too. A universal closure
ρ(X)=E is sound but normally fails (OC), merges inconsistency with consistency,
and cannot recover the informative positive fixture. Soundness alone is inadequate.

## What the source supplies, and what it does not

With this explicit L, π and F, the complete-lattice, upper-closure, monotonicity
and continuity hypotheses hold. The source's existence theorem applies. Since
these collecting transformers are completely additive, its Theorem 4.2 identifies
the least observationally complete domain with the complete shell. We should not
advertise an extra observational-completeness advantage over that shell here.
It does not say every observationally complete domain is complete.

For our smaller implementation class, a partition of E induces saturation ρ.
Refine initially equal-o blocks until all members of a block transition to the
same block for every t. Stability implies exact observations after every finite
sequence by induction. Conversely any partition preserving all future observed
sequences cannot merge a pair split this way. This proves the coarsest partition
for this finite deterministic transition menu, not a universal optimal format.

Unchecked/outside: efficiency of the general constructive shell; automatic
causal-premise validity; arbitrary external modules, registry growth, random
revision policies, shared physical noise, and probability-valued evidence fusion.
The collecting lift deliberately makes additivity easy by retaining full records;
that alone is no practical compression or scalability achievement. Exact
provenance explanations may require adding support-label observations to o; the
answer-only quotient cannot license deletion of source history.

## Selective correction and truth status

For a fixed claim h at revision v, retain all inclusion-minimal consistent
assumption subsets S that entail h, and separately minimal inconsistent subsets.
On a consistent active set A, h is supported iff some retained S⊆A. In the finite
baseline this follows by choosing a minimal subset of A if h holds; conversely
adding constraints preserves a universally true claim while consistency remains.
This is the elementary support-label idea underlying truth maintenance.

Withdrawal destroys one warrant when it removes a needed assumption, but the
conclusion may survive through another warrant. Mechanism replacement changes
the claim's interpretation, so old supports require recomputation at the new
version. Dependency metadata alone cannot decide semantic survival. Report
supported / negation-supported / unresolved / inconsistent separately; a failed
warrant is not proof that the claim is false. Preserve historical answers with
their original assumptions and versions.
