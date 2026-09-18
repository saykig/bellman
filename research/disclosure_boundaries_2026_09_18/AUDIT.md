# Completion and mathematical reuse audit — 18 September 2026

## Requirements and evidence

| Obligation | Retained evidence | Status |
|---|---|---|
| Fix payoffs/costs; vary prior, gate, budget first | Theorem I, especially (I2)–(I3) | Exact analytical necessary/sufficient result |
| Then vary costs and payoffs too | Theorem F, phase closures | Exact within the declared strict payoff family |
| Test the unrestricted classification | Two-law admission example | Falsified; missing admissible-law lower continuity |
| Regular-region continuity | Theorem R, with proof and exact recovery condition | Established optimization specialized; not novel |
| Support-driven jump | E12 and E23 asymmetric examples | Explicit analytic witnesses; masked case included |
| Equilibrium-driven jump or exclusion | Exclusion on fixed-support information regions; δ example with changed payoffs | Both proved, with distinct scopes |
| Computation searches/checks | check.py and source-bound results.json | 56 direct optimizations; finite rational checks; one failed solver status preserved |
| Game-to-threshold Lean audit | DisclosureGame.lean and result.json | Checked fixed-information E12 assessment, including operations and full-support wrapper |
| Primary-source and novelty assessment | sources/NOTES.md and manifest.json | Four primary sources; novelty unestablished |
| Rejected approaches and next question | REJECTED_APPROACHES.md and manuscript | Explicit; no network/multiple-sender expansion |

## Seven-part component contract

**Subject:** robust minimum fine for pooling in the specified public evidence game,
with a full binary-correlation KL family and supplied gate. **Premises:** exact
utilities/menu, positive prior, κ<log 2, operational feasibility, player knowledge
of the law, existence selection, shared continuation per message, nonnegative
costs, strict payoff region. **Query:** compute E and identify continuity at a
parameter; a separate query optimizes the gate. **Guarantee:** Theorems I/F give
exact values and continuity criteria, not merely bounds. **Reuse:** preserve the
model and quantifiers; recheck support, menu, information and selection before
transport. **Boundary:** arbitrary source catalogues, zero priors, infinite fines,
private receiver information, unknown-law equilibria, new payoff orderings and
refinements require separate treatment. **Identity:** model text, exact source
hashes, experiment-code hash and Lean-source hash bind the retained evidence.

## Adversarial review conclusions

The budget threshold for controlled saturation is (1−max(p1,p2))log 2, not log 2.
This prevents falsely reporting a jump once ordinary control already requires H.
The support trigger is a closed set only in the fixed-cost layer; full-parameter
analysis therefore uses phase closures rather than reusing that shortcut.

Full-support posterior freedom does not mean arbitrary receiver-specific beliefs.
Both receivers observe the same public message. Overlapping certificates require
simultaneously feasible sender trembles; the construction explicitly accommodates
both messages. No joint-message action is available to type 2.

The Lean algebraic predicate is deliberately distinguished from its full-support
PBE interpretation. The source-kernel and additive-utility premises remain
stipulated. Global continuity, singleton beliefs and simultaneous two-message
consistency are not claimed as Lean theorems.

The finite-phase theorem is exact but model-specific. The general theorem's
strict-slack assumption is sufficient, not necessary, and can fail because of
binding operational constraints or cost-zero indifference. Its weaker recovery
condition is exact under the closed-graph/compactness assumptions. Calling that
condition a new general classification would misrepresent prior art.

This is author mathematical review and machine checking of the stated slice.
No independent human review, empirical adequacy or authority to deploy follows.
