# Recommendation: test justified revision before further interface compression

17 September 2026. Clarification complete; the next experiment is prepared, not
executed. The [canonical research purpose](../foundations/NORTH_STAR.md) remains
broader than the proposed paper question.

**Recommended question:** in a finite causal system with a declared intervention
menu, what must a knowledge record retain so that adding or withdrawing a named
premise, or replacing a mechanism, preserves the detailed reference's answers?

Use labelled assumptions and explicit mechanism versions as the reference state.
Use relational constraints to combine what those assumptions permit, causal
equations to answer interventions, and operation-relative observational
completeness to assess any reduced representation. This is a synthesis of existing
mathematics, not a proposed universal foundation. Compression is an optional
consequence; the purpose is useful conclusions that survive justified revision.

## Why this question earns the next test

Combining knowledge already has an exact finite baseline: intersect constraints
on complete mechanism choices, or use compatible relational joins. Existing
valuation and local-to-global theory connect these operations; causal ownership
supplies intervention semantics that an anonymous constraint does not encode.
The [first investigation](../foundations/manuscript/RESEARCH_NOTE.md) remains
useful evidence. Its current-model and query-signature representations do not,
by themselves, support named withdrawal.

The decisive example is small. Two separately revocable warrants j and k both
assert a=0. Stores {j} and {j,k} describe the same systems today. Withdraw j:
the first store allows either value of a; the second still requires a=0.
Consequently **no operation on the current model family alone can implement
named withdrawal for every store**. This is a written counterexample, checked
computationally. It identifies missing information before any optimization.

A second example shows the desired positive behavior. Let X be an input, and let
modules own Y=X xor a, Z=Y xor b, and W=c. Unknown bits a,b,c describe uncertainty
about the mechanisms, not physical coin flips. One premise says a=b; another
says a=0. Neither alone fixes Z under do(Y=1), but together they imply Z=1.
With c=0 also known, withdraw a=0: Z=X and W=0 remain justified, while the
intervention answer becomes unresolved. A second surviving warrant for a=0
preserves that answer. Physically replace Z's mechanism with Z=Y xor 1:
under the original premises, Z becomes 1−X and W remains 0. The replacement
changes the system; it is not another observation of the original mechanism.

These [executed probes](probe-results.json) also check that inconsistent premises
are reported as inconsistent, rather than used to certify all claims. Copying
one evidence event keeps its source identity: a toy likelihood calculation gives
posterior 3/4 once, versus an unjustified 9/10 if the same event is counted twice.
Logical idempotence alone is not a statistical evidence-pooling rule.

## Theoretical fit and its limits

[Amato and Scozzari](https://www.sci.unich.it/~amato/papers/fi11.pdf), Definitions
3.1–3.3 and Theorems 3.1 and 4.2, provide an appropriate observational-completeness
criterion. Our [translation](TRANSLATION.md) supplies the concrete lattice,
closure operators and transition hypotheses. Sets of labelled, versioned records
form a complete lattice; deterministic operations lifted by direct image preserve
arbitrary unions. The existence result therefore applies, and the least
observationally complete domain coincides with the complete shell in this setting.
That is borrowed theory, not a new theorem about causality or an efficiency claim.

A finite partition implementation has an elementary proof: if each block has one
observation and every operation sends a block into one block, induction preserves
the observation after every finite operation sequence. Repeated splitting by
successor blocks yields the coarsest such partition. This proof justifies checking
finite stability instead of sampling ever longer traces. It does not establish
that a useful smaller partition exists.

[de Kleer's assumption-based truth maintenance](https://dekleer.org/Publications/An%20Assumption-Based%20TMS.pdf),
§4.3, provides the relevant support-environment precedent. Our probe enumerates
two minimal supports for the intervention claim, so losing one proof need not
lose the conclusion. A causal evaluator must still establish what each support
entails at a specified mechanism version. Current answers and complete support
explanations are different observations; the proposed answer quotient does not
authorize deleting the source ledger.

## Alternatives rejected for this next test

1. **More exact-accumulation examples as the main question.** Retain them as a
   baseline, but relation intersection and join already answer this bounded task.
   Repeating them would not resolve revision or evidence identity.
2. **Output-only continuation as the main interface challenge.** Equal complete
   external behavior remains equal after the same output-only postprocessing.
   Enumeration of 16 unary Boolean chains found 32 externally equal unordered
   pairs, zero distinguished by downstream unary postprocessing, and 20 by
   internal interventions. Access permissions matter; another output-only grid
   would test a settled implication. Causal interfaces remain part of the chosen
   question, with Y explicitly available for intervention.

The broader [candidate comparison](CANDIDATES.md) records their merits. These are
scope decisions, not claims that the underlying theories are unnecessary.

## Next experiment and decision rule

The [specification](EXPERIMENT_SPEC.md) fixes eight complete original systems,
five named premises and three replacement modes: 96 reference records. Compare
current-answer equality, current-model-family equality, and a partition stable
under every permitted addition, withdrawal and replacement. The prepared
[next_experiment.py](next_experiment.py) reports blocks and separating revision
traces, then independently checks the stability premises. It has only been
syntax checked in this run; no partition counts are claimed.

Success means exact, informative answers and selective correction against the
full reference. Fewer states are welcome but not required. If the stable partition
is essentially the full record, keep those distinctions. If truth-maintenance
labels plus exact causal evaluation already suffice, recommend that implementation
and a worked synthesis rather than inventing an algebra. A tractable paper could
present this finite specialization, its revision counterexamples and explicit
boundary conditions. Novelty and publication readiness remain unestablished.

For Bellman, retain the mechanism catalogue, explicit interfaces, source identity,
and version history as the reference; treat a query summary as a derived view.
Reuse relational combination and causal evaluation. Delay any architectural
migration. Remaining obstacles include new evidence about replacement versions,
growing source registries, dependent probabilistic evidence, shared physical noise,
and the cost of exact model sets. None is solved by this finite test. A later
experiment should address a concrete demonstrated obstacle, not merely enlarge
the enumeration.

## Evidence status

- **Borrowed:** observational-completeness and support-environment theory;
  prior valuation/compatibility and compositional-causality results.
- **Written elementary derivations:** withdrawal impossibility for anonymous
  families; applicability hypotheses; stable-partition induction and refinement;
  finite minimal-support characterization.
- **Executed exact checks:** the small accumulation, withdrawal, replacement,
  duplicate-event and interface probes. No statistical sampling is involved.
- **Not established:** useful quotient size, scalable algorithms, empirical
  adequacy, novelty, or general revision semantics beyond the declared menu.
- **Formal verification:** no new Lean proof in this clarification. The completed
  investigation's narrow Lean results remain unchanged and do not verify revision.

See [source notes](SOURCES.md) for inspected locations and literature limits.
