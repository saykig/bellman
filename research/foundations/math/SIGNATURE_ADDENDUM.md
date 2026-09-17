# Query signatures and what the finite search changed

2026-09-17. Additive to DEVELOPMENT edition 1; no earlier result is withdrawn.

For a fixed signature, let Ω be its finite complete-mechanism catalogue and let
C⊆Ω be nonempty. Let H be a covering family of scopes in the catalogue coordinates
and C⁺=⋈_(D∈H) π_D C. Always C⊆C⁺. Fix a finite list Q of input settings,
interventions and requested output marginals. Define

    σ_Q(θ) = (P_θ^q : q∈Q).

This is a vector of single-regime distributions for ONE mechanism assignment.
It is not a joint distribution of potential outcomes, and does not impose or
identify a physical coupling across intervention worlds.

**T5 (elementary set-image criterion).** σ_Q[C]=σ_Q[C⁺] iff

    for every θ⁺∈C⁺ there is θ∈C with σ_Q(θ⁺)=σ_Q(θ).       (3)

Proof. The forward inclusion is automatic from C⊆C⁺. Equality holds exactly
when every element of the larger image has a preimage in C, which is (3). □

This restatement is a finite decision procedure, not a structural characterization
or a novelty claim. Equivalently, C⁺ must introduce no new equivalence class for
θ~_Qη iff σ_Q(θ)=σ_Q(η). It need not introduce no new mechanism assignment.
Lossless join dependencies give the stronger sufficient condition C=C⁺.

**X6: matching every scalar range is weaker.** Take two deterministic modules
Y=K(X), Z=L(Y). The true catalogue has two models:

- K is constant 0 and L is bit-flip: Z is constant 1;
- K is identity and L is constant 0: Z is constant 0.

The two query answers (P(Z=1|X=0),P(Z=1|X=1)) are {(1,1),(0,0)}.
Projecting to the two module catalogues and recombining admits K=identity,
L=bit-flip, whose signature is (1,0). Each individual query still has range
{0,1}. The new model violates equality between the two query answers, even
though neither scalar range widened. Setting X here is an external input;
it agrees with do(X) in a supplied root extension.

**X7: lossless model recovery is stronger than necessary.** Instead use
(K=constant 0,L=constant 1) or (K=identity,L=constant 0). Independent recombination
adds two models, but the possible Z signatures remain the two constant outputs,
even after adding do(Y=0) and do(Y=1). Every L ignores its input; the distinction
between K mechanisms is irrelevant to this exposed-output query class.

Both are direct derivations, not merely numerical patterns. The exhaustive probe
checks all 65,535 nonempty relations on the 16 pairs of unary Boolean functions.
Among 65,310 nonrectangular relations, 37,046 preserve the input/output signature
set, but only 1,902 preserve it after adding both Y interventions. Respectively
27,474 and 62,618 preserve each scalar range while changing the signature set.
These counts are exact finite evidence, not frequencies for real systems.

A failed (3) has a checkable witness consisting of θ⁺ and its full signature,
plus verification that no θ∈C matches. One intervention can distinguish θ⁺ from
a particular θ, yet different θ may require different interventions. The earlier
phrase “model/intervention witness” must allow this finite joint signature.

Next experiment: on a three-module Boolean chain, compare a separator-retaining
join representation with a proposed signature-equivalence reduction. Test whether
merging local choices with identical standalone external signatures stays sound
when a downstream mechanism and an internal intervention target are added.
Use a bounded catalogue and exhaustive reference; report an explicit distinguishing
continuation if it fails. This tests congruence under composition rather than
collecting another grid of the same two-module counts.
