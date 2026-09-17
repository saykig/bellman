# Finite mechanism knowledge: definitions, proofs, and failure boundaries

Edition 1, 2026-09-17. This file fixes the statements before Lean evaluation.
Labels: **B** borrowed result; **S** specialization/elementary derivation here;
**C** conjecture or open question; **E** computational evidence; **F** formal proof.
No result below is claimed novel. Source keys resolve in ../sources/NOTES.md.

## 1. Three different meanings of combination

For finite variable sets D with nonempty value sets, write Ω_D for their product.
A relation R ⊆ Ω_D means “these assignments remain possible.” Define

    R ⋈ S = {x ∈ Ω_(D∪E) : x|D ∈ R and x|E ∈ S},
    π_C R = {x|C : x ∈ R},                         C ⊆ D.

Join is conjunction; projection is existential forgetting. Join is associative,
commutative, and idempotent; projecting twice equals the direct projection.
It satisfies π_D(R ⋈ S) = R ⋈ π_(D∩E)S. These are relational information-algebra
operations [KS, AC]. The universe is no constraint; empty is contradiction.
Alternative explanations combine by union on a common scope, not conjunction.

A nonnegative potential φ:Ω_D→R_≥0 has a different combination:
(φ⊗ψ)(x)=φ(x|D)ψ(x|E), with focusing by summation. Finite distributivity
proves the same elimination identity, but φ² need not equal φ [SS]. Multiplying
likelihood factors requires a justified factorization. Combining two reported
marginals by multiplication is generally not marginal completion.

Example: let P_B=(3/4,1/4), and let A and C be constant. The compatible AB and BC
marginals both carry P_B. Their normalized product gives B=(9/10,1/10), not P_B.
A correct two-context extension is P_AB P_BC/P_B on positive separator cells,
zero on zero-mass separator cells. Summing verifies its marginals. This picks
conditional independence of A and C given B, not a unique possible extension.
With B constant and both A,C fair, independent and perfectly correlated A,C are
two distinct extensions of the same local marginals. Existence ≠ uniqueness.

## 2. Exact extension versus mere satisfiability

**T1 (S, relational instance of AC Proposition 5.1).** For any finite family of
relations R_i with scopes D_i covering D, let J=⋈_i R_i. There is a relation
G⊆Ω_D with π_Di G=R_i for every i iff π_Di J=R_i for every i.

Proof. Any such G is contained in J: every tuple of G satisfies every local
relation. Thus R_i=π_Di G⊆π_Di J⊆R_i, proving equality. Conversely take G=J.
J is the largest such extension under ordinary set inclusion. □

A nonempty J proves at least one simultaneous assignment exists; it need not
preserve every local possibility. For example AB permits all four bit pairs,
BC imposes B=C, and AC imposes A=C. J={000,111} is nonempty, yet AB's 01 and 10
cannot extend. All singleton overlap projections agree. Exact extension fails.

**T2 (S, two-context gluing).** If R⊆A×S and T⊆S×B have equal S projections,
then J={(a,s,b):R(a,s) and T(s,b)} has exactly R and T as its projections.
Proof: for (a,s)∈R, overlap equality supplies b with T(s,b); the converse side
is symmetric. The reverse inclusions follow from the definition of J. □

By attaching one leaf at a time, T2 gives exact extension for nonempty relations
on a join tree whose bags satisfy running intersection (each variable's bags
are connected), assuming overlap equality on every tree edge. A fresh leaf
shares with previous bags only variables in its adjacent separator. The T2
witness therefore extends the accumulated assignment. This proof does not apply
to an arbitrary cyclic cover.

**X1 (counterexample).** Bits A,B,C obey A=B, B=C, A≠C in contexts AB, BC, AC.
Every overlap permits both bit values, but J is empty by transitivity of equality.
Putting uniform mass on each permitted pair also yields matching singleton
marginals and no global probability law: any law satisfying the first two equalities
has P(A=C)=1, whereas the third requires P(A=C)=0. This is a small illustration of
the extension obstruction [AB]; no quantum realizability is asserted.

Caution: the presheaf of assignments glues compatible individual assignments
uniquely. Relations and distributions over assignments need not glue, and when
they do, extension need not be unique. Do not call all these objects sheaves.

## 3. Selected setting: finite acyclic modules and mechanism catalogues

This setting is selected because it exposes intervention semantics, shared
uncertainty and failures of composition with small exact arithmetic. It does not
require arbitrary SCM discovery, measure theory, or a universal new algebra.

A signature consists of:
- typed input ports I and owned internal/output nodes V, all with finite nonempty
  state sets; ports refer to variable identities, not merely matching names;
- a directed acyclic graph on I∪V, with no mechanism owned by an input;
- one owner for each v∈V and parents pa(v)⊆I∪V;
- designated exposed outputs O⊆V and a declared intervention target set T⊆V.

A realization θ assigns a normalized kernel k_v^θ(x_v|x_pa(v)) at every owned
node. Rows are supplied even at observationally unreachable parent values.
The semantics, conditional on input i, is

    P_θ(v|i) = ∏_(v∈V) k_v^θ(x_v|x_pa(v)).                  (1)

This is a causal model only with the additional mechanism-invariance and
independent-local-randomness interpretation [P, RW]; a fitted conditional table
alone does not supply it. Hidden common causes must be explicitly represented
or handled by a richer model. The chosen profile excludes hidden shared noise.
It also excludes feedback and cross-world counterfactual queries. Kernels give
single-regime laws, not a specified coupling across different interventions.

Partial knowledge is a set C of complete assignments θ to a finite catalogue of
mechanism choices. A catalogue element specifies a whole kernel, not an observed
outcome. C is an epistemic set, not a random variable with an invented prior.
Constraints over subsets of catalogue coordinates are relations; combine them
by join and retain shared coordinates until all constraints using them meet.
A continuum of kernels is mathematically possible, but our enumeration is complete
only for the explicitly finite catalogues. No claim about all real SCMs follows.

Observation e restricts C to {θ∈C : observation-map(θ)=e} for exact population
constraints. Actual finite samples require a separately justified statistical
observation model; exact equality to empirical frequencies is not assumed.
For query q, report q[C]={q(θ):θ∈C}; empty C is inconsistency, not identification.
A singleton range for nonempty C is point identification relative to the profile.

Wiring M:I→O to N:O→Z identifies N's inputs with M's outputs, retains internal
node/owner labels, and requires disjoint owned nodes, matched types, no backward
edge and no undeclared common randomness. Reusing one output twice uses a single
sample copied to both consumers, not two independent draws. On kernels with no
other inputs, the external semantics is

    (L∘K)(z|i) = Σ_o K(o|i)L(z|o).                         (2)

Parallel disjoint modules have product kernels under the stated randomness
assumption. Composition is associative by rearranging finite sums; identity is
the deterministic copy kernel. Sequential composition is directional, unlike
commutative information join. Finite kernel composition is borrowed [F].

Hard intervention α:S→values replaces each owned mechanism at s∈S⊆T by
δ_(α(s)), ignoring its parents. Other mechanisms and the knowledge constraints
on the ORIGINAL realizations remain fixed. Evaluate every θ∈C under this same
replacement. Do not condition C on an action setting, and do not reselect a
mechanism independently at each node. A downstream input port can be clamped
only by specifying whether this changes its upstream owner globally or breaks a
particular wire; our do operation changes the owner globally.

## 4. A compositional result with intervention semantics

**T3 (S, finite specialization of stochastic composition and surgery).** Let M,N
satisfy the wiring conditions above, with complete normalized kernels. Let J be
any nonempty admissible relation on their mechanism catalogues, retaining all
shared constraints. For every θ∈J and hard intervention α on owned nodes:

(a) the product (1) after replacement is a normalized distribution for each input;
(b) replacing the owned factors in M and N before wiring yields exactly the same
joint law as wiring first and replacing those factors;
(c) summing internal variables produces the same external law in either order;
(d) the set of these laws over the same J agrees in either construction.

Proof. Topologically order the DAG. Sum its last unobserved node in reverse
order: its factor sums to one, also when replaced by a point mass. Continue to
obtain one, proving (a). For (b), single ownership assigns each replaced factor
to exactly one module. Both procedures contain the identical replaced factors
and identical untouched factors in their joint product. Thus their joint
probabilities agree pointwise. Finite summation proves (c). Applying the
pointwise equality to every member of the SAME J proves (d). □

This is an elementary compiler-correctness result, not a new causal identification
theorem. Observational positivity is unnecessary for supplied total kernels.
It becomes relevant if one tries to learn those kernels from observational
conditionals. Acyclicity and normalization are essential to this proof: two
cyclic deterministic equations X=Y and Y=X have product total mass two, whereas
X=Y and Y=1−X have mass zero. A cycle is not licensed by tensor contraction alone.

Intervention must precede erasing the identity of an internal target. Once only
L∘K is stored, separate K and L and the target's meaning cannot in general be
recovered. T3 is about structured modules, not surgery on an anonymous matrix.

## 5. Successful stochastic example with explicit interfaces

Root owns X∈{0,1} with P(X=1)=1/4. M has input X, owns/exposes Y∈{0,1}, and
K(Y=1|X=0)=1/5, K(Y=1|X=1)=4/5. N has input Y, owns/exposes Z∈{0,1}, with
L(Z=1|Y=0)=1/10, L(Z=1|Y=1)=9/10. Allowed targets are X,Y,Z at their owners.
Internal randomizers are independent; kernels are invariant under interventions.

P(Y=1)=3/4·1/5+1/4·4/5=7/20.
P(Z=1)=1/10+4/5·7/20=19/50.
P(Z=1|do(X=1))=1/10+4/5·4/5=37/50.
P(Z=1|do(Y=1))=9/10, with P(X=1|do(Y=1))=1/4.
But P(X=1|Y=1)=(1/4·4/5)/(7/20)=4/7.

Surgery and conditioning are different operations even in this simple model.
Enumerating the full joint and applying formula (2) independently reproduces
these numbers in the experiment.

## 6. The pivotal false claim: local mechanism sets compose exactly

Claim (false): projecting knowledge to each module, forgetting their shared
parameter, and taking every pair of surviving mechanisms preserves all causal
query answers.

**X2.** Input X is a bit. Let K_a output Y=X xor a and L_b output Z=Y xor b.
The original knowledge says (a,b)∈C={(0,0),(1,1)}: two alternatives, one persistent
shared bit, no probability over alternatives. Both full models give Z=X. Thus
under do(X=0), P(Z=1) is exactly 0.

Separate projections yield a∈{0,1}, b∈{0,1}. Their product also admits (0,1) and
(1,0), giving Z=1−X. The reported query range becomes {0,1}. This is a strict
outer approximation, not an exact uncertainty family and not evidence of genuine
nonidentification in C. Shared epistemic uncertainty is distinct from correlated
physical random noise.

A safe local encoding uses R={(t,a):t=a} and S={(t,b):t=b}. Join on t first, then
forget t; this recovers C. Forgetting t in both relations before joining produces
the spurious rectangle. This is precisely where relational information algebra
is useful alongside causal evaluation; no new universal algebra is necessary.

**T4 (S).** For any C⊆A×B, C⊆π_A C×π_B C. Therefore q[C]⊆q[π_A C×π_B C]
for any query function q. Equality of model sets holds iff C is rectangular.
Equality for every function q:C's ambient space→{0,1} also implies rectangularity:
if w is in the rectangle but outside C, use q=1_{w}. However equality for a
particular interventional query family can hold without rectangularity, because
it may not distinguish all mechanism assignments. No necessity claim for that
restricted family has been proved here.

## 7. Additional boundaries

**X3 (observational agreement is not interventional agreement).** Model A has
X=U, Y=X, U fair. Model B has Y=U, X=Y. Both observations put half on 00 and 11.
Under do(X=1), A gives P(Y=1)=1 and B gives 1/2. Choosing a compatible joint law
cannot choose causal direction. All mechanisms are deterministic given roots.

**X4 (off-support mechanism rows).** With X identically 0, Y=X and Y=0 give the
same observational law. Under do(X=1), Y differs. Supported observational rows
cannot stand in for an entire input/output causal interface.

**X5 (hidden shared randomness).** Two modules with no inputs each have fair-bit
marginals. Independent randomizers give P(Y=Z)=1/2; one unrepresented shared
randomizer gives P(Y=Z)=1. Merely matching individual kernels licenses neither
model. Our module tensor presumes independent randomness; otherwise expose the
common parent or retain a joint mechanism.

**Paper question (C, open).** For a fixed finite acyclic signature, finite
mechanism catalogues, allowed hard interventions and exposed outputs, when does
replacing a coupled catalogue relation by joins of its stored projections
preserve the full *joint signature* of all allowed intervention laws? Develop a
small exact test with an attaining model/intervention witness when it fails.
Do not silently replace joint signatures by separate scalar ranges. Their equality
is weaker and can lose dependence between answers to different questions.

First finite method: enumerate realizations, construct each intervention-law
signature with exact arithmetic, and compare the two signature sets. This already
decides the finite problem; research value would be a structural sufficient
condition or a smaller query-sufficient representation. Stop if existing database
join dependencies and causal abstraction results supply that condition directly.
