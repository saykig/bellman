# Bellman PR #4 — mathematical, reference-code, and repository review

**Disposition: request targeted changes before merging the reference implementation. Retain the mathematical completion and the repository direction.**

Repository: `saykig/bellman`  
PR: `4`, `codex/bellman-buildout-completion`  
Reviewed head: `81fbcc4d503275f091c8c31588ac02d3abf14466`  
Base: `95d0cab3b3e577a0a990c485cc5e1acb4334517b`  
Review date: 7 September 2026.

## 1. Summary

The completion makes substantial constructive progress. Its weak-duality, Farkas, normalization-specific conditional transformation, matching-original-witness, and conditioning arguments survive this review. The worked posterior bounds `4/7` and `8/11`, action-difference bound `-1/7`, changed-loss extrema, and distinction between outer and original attainability remain supported.

However, exactness is not enforced at all witness-entry paths in `joint_law.py`. Floating-point original witnesses can pass constraints that no exact model satisfies, and the action helpers can then certify a decision over an empty original family. A related single-action shortcut skips the task validator. These are implementation-boundary findings, not counterexamples to the exact mathematical theorems.

No remote write, code repair, PR review submission, push, or merge was performed.

## 2. Evidence and execution limits

The full revised mathematical document, new reference and check source, current README and substrate ledger, findings-ledger addition, manifests and replay notes were read. The exact review artifacts newly copied into this PR match the earlier mounted source artifacts. The pinned repository tree and its verification subtrees were inspected. PR #3 is merged; PR #4 was open at the reviewed head.

Direct container retrieval failed at DNS resolution. The two new executable files were reconstructed from connector-returned source text and matched against their exact Git blob identities before running. The matching original reviewer harness was reused from its mounted artifact after checking both its blob and SHA-256 identities. This is verified-source execution of a subset, not a full Git clone or an all-history audit.

| File | Git blob | SHA-256 |
|---|---|---|
| `verification/joint_law_completion/joint_law.py` | `196c8e05d7b0f9580908236a788fdb2d1ce8581a` | `26c33ca45eaae4db31530f47e816687ac0d372cb02ea3ea7abece815e149a1d2` |
| `verification/joint_law_completion/module_checks.py` | `ca59005ec1856c08d80d794bd53ffc0ec07c4a63` | `718acc28804da3f20bf9ba4fd696fe19c5f0dbfd54cbf17838869ef7a35f11a7` |
| `verification/buildout_review/reviewer_checks.py` | `8f00d17f1df6b3e2b6c5f70827bd5cd97784f2fc` | `55c9fb770e1959c9be3d65ee517fb628b25e940148194e414027043b63aa9486` |

Executed on **CPython 3.13.5**, versus the completion author's reported 3.9.6:

- The committed new suite passed all **19 fixed cases**, normally and with `-O`.
- The archived reviewer harness passed **18 mathematical groups** with **one explicit NOT_RUN** packet-integrity group, normally and with `-O`, as documented for public replay without the optional packet ZIP.
- The new suite's observations and certificate payloads agree across modes. Substituting only the reported original runtime metadata into the fresh normal output reconstructs the archived `module_results.json` digest exactly: `14af2b39a494c2cce524c9f1b393de5a1ce4fa94aef2f073cde4a15a5783c99d`. This comparison is not a claim that different runtime records are byte-identical without normalization.
- A new nine-group pinned-source probe reproduced six paths through **two distinct findings** and retained three positive/control groups, in both modes. Six reproductions are not six independent defects or experiments.

The excluded raw original-author source was not replayed in this review. Its historical 18-group reproduction remains author-reported. None of these tests supplies formal proof checking, independent authorship, empirical model validity, or all-input correctness.

## 3. R1 — original witness paths permit floating-point false membership

**Priority: blocking for the advertised exact decision-certificate reference. Confidence: high, reproduced.**

Locations in the reviewed source:

- `original_member`, lines 164–167;
- `forward`, lines 181–187;
- `impossible_event`, lines 298–302;
- `decide`, lines 305–322;
- `fixed_minimizing_set`, lines 325–339;
- polynomial evaluation in `Polynomial.holds`.

`consume` explicitly requires exact `Fraction` certificate vectors. Model and task constructors also reject floats. But separate `original_point` arguments do not pass through an exact-number check before feasibility or polynomial evaluation. A `Fraction` multiplied by a float becomes a floating-point calculation on the tested runtime. Rounding can then erase a genuine constraint discrepancy.

### Exact contradiction used in the reproduction

The two-atom model has normalization and two retained original predicates:

```math
x_0=\frac12,\qquad x_0=\frac12+2^{-60}.
```

All model coefficients are supplied as exact fractions within the reference's limits. The original domain is empty: one number cannot equal these two different constants. The linear outer domain remains the probability simplex.

Observed with the unmodified pinned code:

```python
original_member(model, (Fraction(1, 2), Fraction(1, 2)))  # False
original_member(model, (0.5, 0.5))                      # True
```

The difference is not a statistical tolerance or an alternate mathematical interpretation. The second equality is false, but floating-point polynomial arithmetic rounds the discrepancy away.

Give action `a0` constant loss zero and `a1` constant loss one. Their risk difference has a valid outer upper certificate of `-1`. With only that certificate, `consume` correctly returns `bound_only_nonemptiness_unestablished`. But with the invalid float witness:

```python
decide(task, 'a0', (0.5, 0.5), {'a1': comparison_certificate})
```

returns a common optimal action, strictness, and complete minimizing set `['a0']`. The same failure reproduces for a whole-space conditional task and through `fixed_minimizing_set`. It supplies the nonemptiness warrant that the mathematics explicitly refuses to infer vacuously.

A second control uses `x0=1`, `x0=1+2^-60`, and a linearly impossible event. `impossible_event` accepts `(1.0,0.0)` and returns `original_nonempty: True` even though the original domain is empty. This is a directly false existence statement.

### Scope and correction

This does **not** show that `consume` accepts a float certificate vector. It correctly rejects that control. It shows a gap at other exposed witness paths. The intended exact-input domain is narrower than the values those paths actually accept.

Require exact witness values before any feasibility, polynomial, support, or inverse calculation. Reject floats and booleans; do not silently convert a float into its exact binary fraction or use a tolerance. Normalize explicitly permitted integers/fraction strings only under a clearly stated witness contract. Do not blindly reuse the 256-bit *input coefficient* limit for derived witnesses: exact elimination and conditional inversion can legitimately create larger fractions. Keep any witness resource bound separately justified and explicit.

Tests must exercise the public membership/decision/impossible-event entry points, not just `rational(x)`. Include the empty original family above, a valid exact witness, a false exact witness, and both conditional and unconditional paths.

## 4. R2 — a one-action shortcut skips full task validation

**Priority: targeted contract correction. Confidence: high, reproduced.**

`forward` validates the model but not the complete task. On an unconditional one-action task, neither `decide` nor `fixed_minimizing_set` enters a comparison loop, so no later `difference`/`consume` call runs `Task.validate`.

Using ordinary `dataclasses.replace`, an otherwise valid unconditional task can be given the forbidden event vector `(0,0)`. Its own `validate()` rejects it because unconditional queries require the whole-space event. Both action helpers nevertheless return the singleton minimizing set.

This is invalid-task acceptance, not a separate demonstration of a false numerical optimum. Validate the full intended task before any shortcut or return. Retain legitimate one-action behavior and impossible-event distinctions. This can be repaired together with R1 without a new parser framework or mathematical redesign.

## 5. Mathematical results retained

### Weak duality and infeasibility

For `z>=0`, `Ez=f`, `Gz<=h`, the certificate conditions

```math
\zeta\ge0,\quad E^Ty+G^T\zeta\ge r
```

correctly imply `r^Tz <= f^Ty+h^T zeta`. Matching this bound with an original feasible attainment proves the original optimum even when the bound came from a larger outer set. The Farkas variant with right-hand objective zero and strictly negative scalar is also sound.

A bound is not an existence witness. An outer attainment is not an original attainment. These distinctions are correctly implemented along the exact `consume` path and must also govern the helpers.

### Conditional transformation

The normalization row gives `sum(w)=t`, while the indicator constraint gives `v^T w=1`; therefore `t>=1`. No zero-scale limiting point enters this normalized probability profile. Inverse recovery `x=w/t` is valid on the analyzed linear domain. Polynomial original constraints must still be checked afterward. A bounded linear objective over the transformed polyhedron can attain extrema even if its scale coordinate is unbounded.

The standard linear-fractional transformation and weak-duality foundation were checked against Boyd and Vandenberghe, *Convex Optimization*, §§4.3.2 and 5.2.2, printed pp.151 and 225. The normalization-specific argument above remains Bellman's explicit specialization, not a claim of new general optimization theory.

### Conditioning bound

The stronger inequality

```math
TV(P(.|e),Q(.|e)) <= min(1, TV(P,Q)/max(P(e),Q(e)))
```

is valid for the same event with both masses positive. The event-set proof is particularly short: assume `a=P(e)<=b=Q(e)` and choose the set where the normalized Q mass exceeds normalized P. If its conditional difference is delta, `b*delta=Q(A)-(b/a)P(A)<=Q(A)-P(A)<=TV(P,Q)`. The overlap proof agrees. The sharp equal-mass example and unequal-mass/rare-event controls pass. The old factor-two bound remains valid, merely weaker.

### Existing example and edge cases

The exact posterior extrema, strict `-1/7` comparison, changed-loss range `[-2/11,2/7]`, non-strict/tie distinction, incompatible triangle, positive gluing, disconnected original domain, and matching-original-witness/outer-bound example all remain supported. The new flaws concern premise enforcement in executable helpers, not a reason to rewrite these derivations.

## 6. Repository assessment

The inspected pinned inventory contains **39 files, 593,912 bytes** of file contents (about 580 KiB). This excludes Git history and service storage. It is a small curated collection, not a storage-heavy platform. The inventory contains no ZIP bundles, virtual environments, compiled binaries, or cache directories. This is an inventory/selected-content review, not a comprehensive secret scan of every historical blob.

The separation is sensible:

- `foundations/`: source mathematical statements and additive developments;
- `reviews/`: attributed review and the historical instruction that explains this completion;
- `verification/`: reference code, exact check inputs embedded in source where documented, compact results, and replay limits;
- ledgers: short indexes and standing, not replacements for source documents;
- `experiments/`: preserved historical research.

Do not delete a distinct mathematical source or checker because it covers similar examples. The author, reviewer, and new module are different evidence paths. The historical instruction under `reviews/` is explicitly labeled non-operative by its README; it can stay.

### What to omit from future pushes

1. Duplicate ZIP packets, full repeated chat transcripts, repeated source copies with only upload suffix changes, scratch notebooks, caches, environments, solver binaries, generated plots without an evidential purpose, and redundant normal/optimized raw logs.
2. More parallel roadmap or status files. Use the existing `SUBSTRATE_LEDGER.md` for foundation progress, `FINDINGS_LEDGER.md` for concise findings, and a short README for navigation/current position.
3. Downloaded vendor libraries or a home-grown general optimization platform. Keep the small active-set routine as a bounded reference, not the default plan to outgrow mature solver libraries.
4. Repository-wide language rewrites, new Writ architecture, game-theory engines, new grids, or unrelated mathematical extensions in the repair task. Those are not necessary to fix these boundary discrepancies.

Keep the mathematical derivations, assumptions, counterexamples, portable verification source, selected reproducible inputs, compact successes **and failures**, and their source identities. Do not equate minimal storage with erasing negative evidence.

### Small housekeeping worth doing

The inspected tree has no root `AGENTS.md`, `.gitignore`, or CI configuration. A short governing instruction and ignore file would prevent repeated scope and archival mistakes. They should preserve the programme principle that existing mathematics counts as progress and executable slices do not limit Bellman. Historical `RUN_THIS_NEXT` files should not silently become live instructions. A single explicit verification command can be added later without creating another workflow platform.

Keep the historically dated Decision Lab statements as historical statements. Add a separately labeled current pointer only after checking its live repository; do not rewrite history to match the present.

## 7. Recoverable archive gaps

The claim that sources were unavailable during the earlier packaging run can remain historically true. Some are available **now** in this conversation's mounted artifacts:

- Original v1: 62,246 bytes; SHA-256 `af60646d0118dce72abc65d7440a4faf9e8ed305ca6ffefc00775cc84204bc22`, matching v1.1's recorded source identity.
- The earlier review bundle contains `fixed_checks.py`, its compact results, log, and source manifest. Their exact extracted identities are in `REVIEW_EVIDENCE.json`.

They were recovered, not rewritten or relabeled new source. The older harness was not rerun in this review. A subsequent small recovery entry can archive appropriate exact original bytes, audit portability, and record a clearly labeled adapter where needed. Do not copy the whole ZIP. Do not claim recovery of v1.1's separate local harness or the excluded private-path author original merely because these other files exist.

For future code, avoid personal absolute paths at authoring time. Accept explicit input paths or resolve repository-relative paths. That prevents the durable archive from depending on a private source left only on a laptop.

## 8. Next action

Repair R1 and R2 on PR #4's existing branch in a cloud workspace, preserve the mathematical sources and historical evidence, and retain compact before/after checks. No broad Pro rewrite is needed. After those checks pass, reassess this bounded reference for acceptance rather than opening an indefinite general review loop.

The repaired reference can then serve as a precise comparison target for an existing exact solver or another implementation language. That future choice must demonstrate the same original/outer, support, bound, optimum, and decision meanings. This PR does not establish cross-language interoperability merely because it includes a `wire` serializer.

## Source register

All repository paths above are anchored to the reviewed commit unless explicitly marked otherwise.

- GitHub PR #4 metadata and complete changed-file list; PR #3 merge metadata.
- Full revised mathematical companion; `joint_law.py`; `module_checks.py`; normalized reconstruction of `module_results.json` verified to its Git blob/SHA-256.
- README, substrate ledger, findings-ledger patch, completion manifest, replay record, verification README files.
- Pinned repository tree and verification subtree inventories.
- Exact previously supplied build-out review, governing prompt, reviewer source, and results matched to the archive's blob/hash identities.
- Original v1 upload and original review ZIP members, for source recovery only.
- Boyd and Vandenberghe, *Convex Optimization*, §4.3.2 and §5.2.2, author-hosted PDF: `https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf`.
- Review execution: `pr4_review_probe.py` and `REVIEW_EVIDENCE.json`. The probe is pinned to the defective source and records its behavior; turn its cases into corrected regressions instead of weakening its pin.
