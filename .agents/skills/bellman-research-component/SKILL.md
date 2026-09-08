---
name: bellman-research-component
description: Develop, extend, review, repair, or assess transfer of a bounded Bellman mathematical component with exact guarantees, adversarial checks, provenance, and conservative failure boundaries.
---

# Bellman Research Component

## Objective and scope

Make consequential decision-making mathematically inspectable, cumulative, and correctable.

Use this skill to improve how Bellman earns mathematical capabilities. Established mathematics
counts as progress. Do not optimize for novelty, a particular implementation language, a fixed
roadmap order, or accumulated infrastructure. Prefer a small exact result with a sharp failure
boundary over a broad vague framework.

Before acting, privately classify the task as one of:

- new mathematical component;
- bounded extension or composition;
- PR hardening or repair;
- adversarial review;
- engineering-transfer assessment;
- history or provenance repair;
- roadmap or frontier selection.

Keep the work within that mode. Do not turn a repair into a new research programme. Do not turn a
new mathematical task into infrastructure work unless the mathematics actually requires it.

## Resolve authority and evidence

Resolve authority in this order:

1. the current user's explicit task;
2. repository `AGENTS.md`;
3. the current Bellman North Star;
4. the current living roadmap and architecture;
5. the exact mathematical foundations, reviews, and frozen results relevant to the task;
6. historical `RUN_THIS_NEXT` or old roadmap material, as provenance only unless explicitly
   reactivated.

Living steering documents are not frozen theorem authority. Never silently rewrite frozen
mathematical editions, reviews, historical results, source manifests, or release records to fit a
current conclusion. If sources conflict, identify the conflict and resolve it from current
authority; do not blend incompatible claims. Correct historical errors additively and preserve the
earlier record.

For a concrete task, inspect the exact relevant foundation, review, reference implementation,
result evidence, and source identity rather than relying on a summary or PR description.

## Specify the component before implementation

Every claimed Bellman component must explicitly identify:

1. **Object / subject** — the exact mathematical thing being reasoned about.
2. **Premises / assumptions** — what must be supplied or true.
3. **Operation / query** — what is computed, transformed, compared, or certified.
4. **Guarantee** — exactly what follows.
5. **Composition / reuse rule** — when the result may safely feed another result.
6. **Failure boundary** — when the guarantee stops, rejects, becomes unresolved, or requires
   another method.
7. **Provenance / identity** — the exact subject, data, model, policy, assumptions, query, and source
   bytes to which the result binds.

The component is incomplete if any of these seven is missing. Clean software structure does not
substitute for missing mathematics.

Preserve semantically distinct statuses. Use repository-native names when they exist, and never
collapse:

- exact or original-model result;
- sound outer enclosure;
- incompatible or infeasible;
- nonidentified or model-dependent;
- unresolved computation;
- unfinished implementation;
- unsupported assumption or query;
- stale or mismatched evidence;
- malformed input;
- mathematically checked;
- empirically validated;
- human reviewed or accepted;
- authority to act.

Absence of proof is not proof of impossibility. A nonempty outer set does not prove that the exact
fibre is nonempty. Variation over an outer relaxation does not prove nonidentification in a smaller
exact fibre. A mathematically checked conditional result does not establish the empirical or
substantive truth of its premises.

## Earn new mathematics before encoding it

For new mathematical work, proceed in this order:

1. state the bounded question;
2. inspect established mathematics already relevant to it;
3. derive the theorem or criterion, or identify the exact established result being specialized;
4. construct a positive witness or example;
5. construct at least one decisive counterexample to the most tempting invalid shortcut;
6. only then design the executable representation.

If established mathematics settles the bounded question, use it. Do not hunt for novelty. Do not
start by designing schemas, registries, graphs, services, DSLs, databases, or generic solver
interfaces.

For bounded exact profiles:

- prefer exact rationals and finite objects where feasible;
- separate producer or construction from receiver or checking;
- never let the receiver trust the producer's success label;
- keep retained evidence checkable with the candidate producer disabled;
- check subject, query, model, policy, and assumption identity before accepting a result;
- fail closed on stale evidence;
- require any numerical solver output used as authority to have an independently checkable exact
  witness, bound, residual, certificate, or reconstruction appropriate to the theorem.

Fixed tests are falsification and conformance evidence, not formal verification. Do not call
normal/optimized equality, broad CI, or exhaustive tiny enumeration a proof assistant.

## Audit composition aggressively

Before combining or reusing results, ask:

- Are both results about the same exact subject, or is transport or revalidation required?
- Are combined quantities in the same units?
- Are probabilities about the same event?
- Are extrema paired from the same model or witness?
- Is one implementable policy used across hidden model alternatives?
- Has conditioning changed the support or meaning?
- Does a future query need information discarded by the current representation?
- Is an output being reused outside the assumptions under which it was checked?

Reject these invalid shortcuts:

- cross-model subtraction presented as modelwise regret;
- hidden model-indexed policy selection when model identity is unobserved;
- statistical coverage probability merged with modelled harm probability;
- observational association silently treated as intervention;
- a changed model or policy inheriting an old theorem label;
- outer-enclosure evidence promoted to exact-fibre evidence;
- local labels or matching field names treated as semantic identity.

When composition is invalid, preserve the valid component results and reject only the unjustified
composition when possible.

For every important theorem or interface, build at least one adversarial case aimed at its strongest
likely overclaim. Prefer small, exact, decisive cases. Useful failure shapes include:

- the same local facts with no global joint completion;
- identical endpoints with an interior extremum;
- good expected value with unacceptable tail or hit behaviour;
- the same observational association with different intervention effects;
- a valid target result with invalid transport provenance;
- individually valid claims that cannot coexist in one common model;
- apparently identical records differing in one decision-relevant premise.

If a counterexample falsifies the proposed theorem, preserve it and redirect. Do not weaken
definitions merely to make an implementation pass.

## Review and repair existing work

When reviewing or hardening an existing PR:

1. inspect the exact final head, base, changed files, and current `main`;
2. inspect the governing mathematical source, not only the PR description;
3. try to construct a concrete counterexample;
4. inspect producer/checker independence;
5. inspect stale-subject handling and identity binding;
6. inspect whether statuses preserve meaningful distinctions;
7. inspect whether committed result evidence is actually source-bound;
8. distinguish mathematical defects from documentation or provenance nits;
9. recommend no changes when no concrete blocker exists.

Do not create hardening work for appearances. Green CI is evidence, not a substitute for semantic
review. Do not send a PR back merely because more tests, abstraction, comments, infrastructure, or
generality could theoretically be added.

Use the existing PR branch when repairing a PR. Start new research from latest current `main`. Do not
force-push unless the current user and repository policy explicitly authorize it. Do not merge a PR
without explicit authorization. Do not rewrite frozen results or historical records. Preserve exact
release and tag identities unless a release task explicitly authorizes mutation. Do not modify Writ
or Decision Lab during bounded Bellman mathematics unless the task is explicitly an engineering
transfer. History records failures and redirects rather than erasing them.

## Select the next gate from evidence

The roadmap is a living capability map, not a queue. After each meaningful build or review, ask:

1. What new statement can Bellman safely make now?
2. What important statement can it still not make?
3. Which missing premise or operation is closest to the current chain?
4. Does that missing capability matter to consequential decisions?
5. Can established mathematics solve a bounded version cleanly?
6. Can the result have a precise failure boundary and decisive counterexample?
7. Would the proposed next step add real decision capability, or only make existing machinery
   bigger?

Prefer the nearest decision-relevant missing premise over mechanical expansion. Do not
automatically add parameters, models, infrastructure, a Writ transfer, a Lean formalization, a
language migration, or a generalized framework. A successful theorem does not itself authorize an
engineering transfer.

### Evidence-triggered language and tool escalation

Begin with the simplest environment that faithfully expresses and checks the bounded mathematics.
Do not choose Julia, JuMP, Rust, Lean, or another tool because of past interest or fashion.

Evaluate Julia/JuMP or another established optimization stack only when exact handwritten search is
the actual bottleneck, the problem has stabilized into a recognized optimization class, larger
constrained model or policy spaces are required by the promised capability, and solver output can be
independently checked to the required assurance level. The mere appearance of an LP, MILP, convex,
or polynomial problem is not a migration trigger.

Evaluate Rust or another strongly typed systems language only when a checker is durable
infrastructure used across repositories or cases, language or runtime ambiguity creates real
assurance or portability problems, stable mathematical contracts exist, and a small independent
checker would materially reduce the trusted computing base. Do not rewrite active research
references merely for cleanliness or performance.

Evaluate Lean or another proof assistant only when the theorem is stable and load-bearing for later
guarantees, a proof error would propagate materially, the statement has stopped changing enough to
avoid throwaway formalization, and formalization adds assurance not obtained more cheaply through
ordinary proof review and exact checking. Prefer narrow formalization of foundational lemmas or
theorems over wholesale formalization.

If a trigger is not reached, say so explicitly and remain with the current toolchain.

## Assess engineering transfer separately

A Bellman capability is only a candidate for Decision Lab or Writ transfer when:

1. its mathematical contract is stable enough to specify;
2. a concrete downstream workflow needs it;
3. the adapter can preserve every decision-relevant distinction;
4. an independent checker can reject false, stale, and mismatched claims;
5. the integration is compared against a competent simpler workflow;
6. provenance, revision, and handoff benefits justify the additional machinery.

Do not port mathematical artifacts merely because they exist. If transfer is attempted, Bellman
remains mathematical authority unless the programme explicitly changes that boundary.

## Retention and reporting gate

A retained bounded Bellman component should normally have:

- a precise subject and typed premises;
- an explicit operation or query;
- an analytical derivation or clearly cited established theorem;
- an exact guarantee, composition rule, and failure or unsupported boundary;
- a constructive, checkable finite procedure where claimed;
- an independent receiver or checker;
- a positive fixture and a decisive negative or counterexample fixture;
- stale and mismatch controls;
- producer-disabled receiving;
- exact evidence and provenance;
- normal and optimized mode consistency where relevant;
- preservation and history checks required by current repository policy;
- explicit limitations and assumptions;
- a conservative roadmap or architecture update only when earned.

Formal proof, empirical validation, production engineering, and domain usefulness are separate gates
unless explicitly promised.

In final reports, separate:

- proved or checked;
- observed in bounded fixtures;
- assumed;
- unsupported;
- falsified;
- unfinished;
- next recommended gate.

Do not inflate progress. Do not call a research reference production-ready, call a supplied premise
verified because conditional mathematics checks, or describe an implementation limit as a
mathematical impossibility. When no meaningful change is needed, say so.

Update this skill only when repeated Bellman work reveals a durable workflow lesson, a recurring
failure mode, or a genuinely new tool or assurance threshold. Frontier-specific instructions belong
in the current task, roadmap, mathematical companion, or verification package.
