# Bellman foundations research brief

Opened: 2026-09-17. Status: active research, not a claim of novelty.

Question: how should Bellman represent partial knowledge of systems, combine it,
and reason about changes to mechanisms? Compare information/valuation algebras,
local-to-global compatibility, and compositional causal models without requiring
one universal formalism. Decisions and strategy motivate this work but are outside
this first investigation.

Deliverables: a critical comparison grounded in primary sources; a bounded setting;
precise objects, operations, assumptions, proof, successful example and failed
claim; executable exact experiments; a small evaluated Lean formalization; a
research note recommending a foundation and tractable paper question. Preserve
negative results and distinguish borrowed mathematics from new conjectures.

Working interpretation: “partial knowledge” can mean missing variables, uncertain
parameters, multiple admissible mechanisms, or incompatible sources. These are
not interchangeable. Start with finite systems and explicit intervention targets;
identify which interpretations each candidate supports before selecting a scope.

Repository policy: use existing main; do not create branches. Preserve historical
artifacts. Commit coherent milestones and push when a remote is available. The
supplied checkout is empty, with no commits or remote; a clarification requesting
the historical repository and destination has been sent. Research can proceed
without inventing repository history or a publishing destination.

Planned milestones:
1. Repository audit, brief, initial source map.
2. Candidate comparison and stable finite mathematical setting with proofs.
3. Exact experiments, counterexamples, Lean evaluation and research manuscript.

Completion does not require publication, a broad world model, or strategic demos.

Repository clarification received: use `https://github.com/saykig/bellman.git`.
Fetched existing main at `58987d2`; all tracked historical files restored and the
new research files retained. This research is additive to that history.
