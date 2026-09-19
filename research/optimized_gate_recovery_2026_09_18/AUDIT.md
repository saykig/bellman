# Completion and reuse audit — 18 September 2026

Mathematical edition: `e2daee7`. This is an author audit, not an independent review.
The separate receiving implementation supplies arithmetic independence from the
candidate formula, not independent authorship. No new edits to that mathematical
edition are made by this audit.

## Outcome and logical status

Deliverable 3, a sharp boundary theorem, is completed with a small exact witness.
The general claim is false under the reading “some deterrent is available,” but
is NOT refuted when “persists” means uniform recovery of near-optimal feasible
designs. Under R1, R2 is necessary and sufficient. F2 supplies substantive primitive
sufficient conditions. R3 gives an alternative strict-branch route for broader games.

| Obligation | Result | Evidence |
|---|---|---|
| One sender, three states, finite game | One receiver, three actions, two public outputs, one certificate | C1–C3 model |
| Fixed payoffs and disclosure costs first | Both fixed, as is prior; only source channel varies | Exact utility table |
| Continuous admissible source family | Affine Q_delta over [-t,t]; clamp delta to a nearby interval to approximate every law | Hausdorff continuity |
| Endogenous gate | Full stated compact two-dimensional binary gate menu | Global inequality d/min(w,1-w)>=1/2 and attaining gate |
| All relevant posteriors retain support | Public lower bound 1/12; eligible certificate states >=3/8 | Analytical bounds plus original-cell checks |
| Mixed equilibria cannot repair | Harmful history has unique A below threshold; at threshold pure C works | Complete one-receiver best-response proof |
| Explain failure | Low-fine B is lost, high-fine C remains | Closedness survives; uniform near-optimal recovery fails |
| Preserve original full-information case | Fixed-fine invariance and one-receiver smoothing theorem | F1/F2; equal-posterior control |
| Label changed information and solution concept | Coarse sender, sequential consistency | User clarification and explicit weak-PBE control |
| Minimality | Small witness only | No global lower-bound theorem claimed |
| Compare established mathematics | Primary optimization, signaling and communication sources | Versioned source notes; novelty unclaimed |
| Reproduce | 2,025 rational original-cell cases, negative controls, normal/-O equality | Source-bound JSON and separate receiver |
| Preserve history | Prior research untouched; ledgers appended | Git baseline 5661f9e |

## Seven-part component contract

1. **Subject:** minimum robust fine for a pooling target, jointly choosing a gate,
   in the exact three-state finite game, and the explicitly broader R1 design class.
2. **Premises:** known source law for players; one common institution design;
   exact information partitions, gate menu, utilities/costs, relative support,
   favorable tie selection and sequential consistency; additional R1/F2/R3 premises
   are separate and must be supplied when those theorems are invoked.
3. **Query:** compute the optimized fine and determine continuity under information
   variation; identify which witnesses can be recovered.
4. **Guarantee:** C3 exact global formula; F2 primitive continuity; R2 exact recovery
   equivalence under R1. Computation corroborates a bounded rational sample only.
5. **Reuse:** retain state-to-type map, certificate eligibility, source/gate family,
   enforcement instrument, target, belief consistency and quantifier order.
   Law-dependent witnesses require actual player knowledge of the law.
6. **Failure boundary:** arbitrary off-path beliefs, unknown-law common strategies,
   unrestricted channels, changed costs or payoffs, private receiver information,
   extra payoff-relevant hidden variables, open witness sets or unbounded fines
   require fresh arguments. Multiple receivers do not inherit F2's upward closure.
7. **Identity:** exact mathematical edition e2daee7; experiment code hashes and
   candidate binding in results.json; external-source identities/gaps in manifest.

## Adversarial checks of the proofs

* C3 takes a maximum over law/history pairs, not a sum of incompatible worst-law
  payoffs. One gate and fine are used before this universal quantifier.
* At t=0 source states 1 and 2 are observationally equal; the gate is STILL
  informative about the third state. Thus “informative available” is genuinely
  satisfied. The fixed contrast floor is not disguised as unrestricted design.
* On-path C is strict at e=0; the jump is solely a continuation obstruction.
  Fine 2 works uniformly, excluding feasibility-to-infinity as the explanation.
* Sender consistency: J and T specify one decision information set for states 1
  and 2. A tremble has one probability there; arbitrary theta-specific trembles
  would quietly give the sender information it does not possess.
* At e=2q the favorable tie selecting C is allowed and yields sender indifference,
  so the displayed value is attained. A strict-deterrence or hostile-tie query
  would need reanalysis; do not call its infimum the same minimum automatically.
* F1 concerns fixed certificate continuation payoffs and fixed statewise target
  payoffs (as with C here). If a target itself varies with information, its sender
  gain subtraction must also be tracked. The lemma alone is not a multi-receiver
  smoothing theorem.
* F2 preserves a deterring mixture only until C catches up; it does not assert
  that arbitrary Nash equilibria persist when fines change in multi-player games.
* R1's subsequence can depend on q because witnesses are allowed to depend on the
  known law. R3 keeps one fine and one gate branch before the finite law cover.
* Exact R2 is an established value criterion, not a primitive discovery. Full
  lower continuity of every optimizer is stronger than needed.

## Remaining limits and stopping decision

No proof-assistant formalization, independent human review, empirical validation,
publication novelty or global minimality. The signaling source was the directly
read July 2025 version; the newer Drive text was inaccessible. The PWI text was
read through the web tool but byte retrieval failed with HTTP 406, so its manifest
has no invented hash. These gaps do not substitute for unavailable source bytes.

No reason to introduce Lean, Julia/JuMP or Rust: the theorem is elementary and the
finite evidence needs exact rational arithmetic only. The bounded question is
settled at the declared boundary; no numerical frontier, network extension or
product adapter follows. A future application must first specify the sender's
knowledge, admissible gates and belief/refinement rule, then test recovery under
that subject. The September 17 revision experiment remains unrun.
