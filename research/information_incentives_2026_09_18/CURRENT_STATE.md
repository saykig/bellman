# Current state — 18 September 2026

**Outcome:** completed this research run with analytical results, exact
counterexamples, a solved disclosure benchmark and an executable evidence set.
See the [manuscript](manuscript/RESEARCH_NOTE.md).

**Strongest computationally useful result:** Theorem E's six-branch exact formula
for worst expected joint deviation gain with both components active. It resolves
the positive-tolerance extension left open by the supplied binary note.

**General foundation:** Theorems A–D preserve the information cost and joint
attainability needed for exact enforcement; D computes event costs through local
augmented junction-tree tables. These specialize established convex/probability
machinery, with explicit assumptions and written proofs.

**Strategic result:** F characterizes pooling disclosure at fixed enforcement and
combines it with the active controlled frontier. Costless verified-state advocacy
raises the benchmark's required penalty from ≈.09018 to 1. G handles one sender
and overlapping partial certificates with a joint credible-continuation set. Its
three-type example proves impossibility below disclosure cost 3/10 despite
individually credible deterrents for every type.

**Evidence:** standalone payoff enumeration, original 8-/16-cell optimization,
primal/dual residuals, 50 nonbinary tree identities and exact rational certificate
arithmetic. See experiments/README.md. Computations test the proofs; they are not
formal verification. Original source bytes are identified and preserved externally.

**Next theorem:** a robust three-state partial-certificate information–enforcement
frontier with one common gate and penalty across the shared-budget family. Determine
when the common continuation-payoff set is convex or yields a sharp nonconvexity
obstruction. Do not substitute independent typewise punishment bounds.

**Unresolved:** novelty, full Forges–Koessler subsumption, efficiency for large
systems, arbitrary private information/multiple senders, endogenous information
acquisition, and empirical warrant. The new Lean receipt checks only the six-branch maximum identity and the
partial-certificate arithmetic; it does not formalize the entire research.

**Git/preservation:** work is additive and uncommitted. Main remains e3a6a92.
No branches, commits, pushes, historical rewrites, or architecture migration in
this run. The earlier clarification and coordinator-owned files remain untouched.
