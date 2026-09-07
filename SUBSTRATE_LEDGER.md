# Substrate Ledger

This is the cumulative index of Bellman's mathematical foundation. Frozen documents remain historical statements under their own assumptions. A frozen draft is not a claim that its mathematics is finished or independently verified. Existing experiment artifacts and the Mathematical Archive Ledger are preserved unchanged.

## Foundation sequence

| Record | Contribution and standing | Durable source |
|---|---|---|
| v1, 6 September 2026 | First seven-component mathematical substrate: joint probability/evidence, information and sequential decisions, representations, approximation/regret, information comparison, model uncertainty, and a separate causal interface. | Exact original source unavailable in this archival pass. Its existence and content are described by the exact review and v1.1; no reconstructed v1 file is supplied. |
| Adversarial review | Retained the central conditional mathematics and recommended focused clarification. Main issues: exact fibers versus outer enclosures; explicit loss, fee, horizon, and support premises; off-support policy execution; numerical error in computed margins; semantic decoder existence versus constructibility; and precise engineering correspondence. | [Frozen exact review](reviews/BELLMAN_SUBSTRATE_V1_ADVERSARIAL_REVIEW.md) |
| v1.1, 6 September 2026 | Focused amendment: separates exact and outer sets; restores nonnegative-loss coupling premises; requires total executable transferred policies; separates model, optimization/evaluation, and coverage errors; clarifies decoders and existing Build 1 scope. **Working foundation, not finished Bellman mathematics.** | [Frozen exact v1.1](foundations/BELLMAN_WRIT_MATHEMATICAL_SUBSTRATE_V1_1.md) |
| Initial next mathematical build-out, 7 September 2026 | Completed additive development draft, frozen before repository packaging. Distinguishes conventions, exact characterizations, and constructive procedures; develops compatibility witnesses, representation/simulation procedures, signed-loss and sequential bounds, persistent uncertainty, and scoped extensions. No novelty requirement or claim of formal proof-library completion. | [Frozen exact build-out](foundations/BELLMAN_NEXT_MATHEMATICAL_BUILDOUT.md) |

The [North Star](foundations/BELLMAN_NORTH_STAR.md) remains: **Make consequential decision-making mathematically inspectable, cumulative, and correctable.** Its first capability is to know exactly what information a representation must preserve for specified future decisions.

## Continuing mathematical programme

Active work includes constructive exact compatibility and identification; discoverable task-relative representations; dependence-aware and online information comparison; conditioning and sequential error composition; solver certificates; persistent robust/Bayesian uncertainty; statistical model learning and time-uniform coverage; constraints, reachability, and tail risk; causal identification; and, where required, multiple objectives and strategic incentives.

The build-out specifies bounded finite procedures and short derivations for these gaps, while identifying what remains an interface or further formalization. More general partial observation, nonlinear model constraints, adaptive data collection, dynamic risk consistency, causal transport, and equilibrium selection remain open development areas. These are not automatic new experiments or selected engineering builds. Historical KL4/KL5/KL6 conclusions and stopping dispositions remain unchanged.

## Verification evidence

- The exact review reports 20 fixed test methods under Python 3.13.5. Its original `fixed_checks.py`, `fixed_check_results.json`, and companion execution/source records were not located. Those claims remain source-reported; this PR neither recreates nor claims to rerun that harness. See [historical verification status](verification/substrate_v1/README.md).
- v1.1 §14.3 reports its own bounded conformance calculations. Its original local harness is also unavailable; those are not this archive's executions.
- The completed build-out's [frozen results](verification/substrate_buildout/checks.json) and [check summary](verification/substrate_buildout/CHECKS.md) record 18 passing illustrative groups under Python 3.9.6: 17 mathematical groups and packet-input integrity. These are example calculations, not independent formal verification, statistical experiments, or production acceptance tests.
- The [portable replay](verification/substrate_buildout/checks.py) retains the mathematical calculation block unchanged. It replaces machine-specific packet access with the archive manifest, checks all six frozen artifacts, and compares the 17 mathematical results with the frozen record. See its [replay notes](verification/substrate_buildout/README.md). It is explicitly not the missing v1 review harness.

## Executable engineering relationship

The first executable Bellman slice is `finite-one-observation.v1` in [`saykig/writ-decision-lab`](https://github.com/saykig/writ-decision-lab). Its [Build 1 specification](https://github.com/saykig/writ-decision-lab/blob/cd8016eda9ccf17ccda4cdb2c37b22f72660bf76/SPEC.md) supplies exact finite rational model/query semantics, signed terminal losses, one optional observation, and all minimizing sets. The [review PR #1](https://github.com/saykig/writ-decision-lab/pull/1) was open at archival inspection, with head `cd8016eda9ccf17ccda4cdb2c37b22f72660bf76`; later reported local repairs are not certified here.

That implementation does not define Bellman's mathematical ceiling. Writ is the engineering/provenance infrastructure intended to progressively embody stable mathematics. Separate implementations may support interface development; permanent repository separation is not a doctrine. Mathematical development may continue beyond current engineering, while an implementation must not claim guarantees outside its specified scope.

## Source identity and archival gaps

The [small source manifest](foundations/SOURCE_MANIFEST.json) records SHA-256 and byte counts for exact artifacts actually obtained. The v1.1, review, and North Star identities match those recorded in the supplied substrate/packet. The completed build-out and its compact results are copied byte-for-byte from the finished mathematical task.

Not included as exact originals: v1; the historical review harness/results and companion log/manifest; v1.1's local conformance harness. No placeholder document or new test script is passed off as any of these. Original upstream audit documents referenced inside the frozen sources are not newly archived by this PR. Packet wrappers, engineering review reports, ZIPs, duplicate copies, local paths, caches, and disposable outputs are excluded. The historical source references inside frozen documents remain historical references; this ledger provides their repository mapping without rewriting their bytes.

## Focused constructive completion — 7 September 2026

The [build-out adversarial review](reviews/BELLMAN_BUILDOUT_ADVERSARIAL_REVIEW.md) identified constructive gaps, numerical-domain premises, maturity overstatement, and evidence limitations. The [additive revision](foundations/BELLMAN_NEXT_MATHEMATICAL_BUILDOUT_REVISED.md) assesses R1–R5 individually; it does not reject a central theorem merely because construction or evidence was incomplete.

The completion supplies precise finite rational compatibility, conditional identification, and decision certificates: full subjects, primal witnesses, dual/Farkas checking, support/inverse checks, and a bounded reference producer with explicit unfinished outcomes. It distinguishes attainable answers from bounds, outer from original feasibility, and assumed premises from checked certificates. Two algebraic proof paths support the sharper conditioning bound, while frozen B15 remains unchanged. Exact fixed cases exercise these constructions; general scalability, nonlinear optimization, certified transcendental radii, and broader temporal/causal/risk mathematics remain active.

Definitions and theorem derivations, fixed-instance execution, and production engineering acceptance remain separate. See [verification](verification/joint_law_completion/README.md) and [source identities](foundations/BUILDOUT_COMPLETION_MANIFEST.json). Author results were recovered and reproduced exactly; reviewer replay passed 19 groups with the temporary packet, and the new module passed 19 fixed cases in normal and optimized modes. The public reviewer replay explicitly skips packet integrity without the excluded ZIP. Earlier missing substrate-v1 originals remain missing.

PR #3 established the first clean substrate archive and was merged externally during this completion. This additive record branches from that existing main history; no old mathematical or KL artifact is rewritten. The external Decision Lab relationship and Bellman's wider mathematical programme remain as stated above. No Writ integration or KL5/KL6 reopening is undertaken.
