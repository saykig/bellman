# PR4 targeted reference repair

Starting/reviewed source: commit `81fbcc4d503275f091c8c31588ac02d3abf14466`, reference SHA-256 `26c33ca45eaae4db31530f47e816687ac0d372cb02ea3ea7abece815e149a1d2`. The [review](../../reviews/PR4_REVIEW.md) and [governing brief](../../reviews/RUN_THIS_NEXT_PR4_REPAIR_AND_ARCHIVE.md) are preserved historical inputs. The brief was explicitly adopted for this repair; it is not an ongoing instruction. The user instructed continuation of the already prepared repair in the existing temporary checkout; no new checkout or toolchain was created for finishing.

## Findings and fixes

All supplied review findings were confirmed; none required weakening a theorem. The previously supplied review calls the shortcut finding R2; the governing brief calls mutable original constraints R2. These are distinct boundary issues, recorded by description rather than conflated identifiers.

- Exact-witness defect: polynomial constants differing by `2^-60` and the separate `N=2^54+1` contradictory linear model both admit false floating-point witnesses in the original source. The latter has exact Farkas value −1. False decision and false original-nonempty conclusions were reproduced normally and optimized. The repair checks exact witness types before membership, polynomial, feasibility, dot-product, support, inverse, and elimination arithmetic.
- Mutable subject: changing a caller-owned polynomial constant changes an existing certificate's original membership; clearing the original term list can promote an outer witness to an original witness. Constructors now snapshot nested term/exponent, matrix, atom, action/loss, premise, and certificate-vector containers. Model/task labels and premise payloads are immutable strings; original nonlinear predicates are immutable `Polynomial` objects. Deliberate revisions use new subjects and require rechecking. This is ordinary immutable value semantics, not authentication against deliberate interpreter tampering.
- Shortcut validation: `forward` and all task entry paths validate the complete task before arithmetic or early return, including single-action menus. `consume` validates the embedded subject too: Python equality between `True` and `Fraction(1)` is not validation. Valid exact single-action and impossible-event cases remain accepted.

Witness and derived-coordinate arguments accept lists/tuples of exact `Fraction` values only. Floats, booleans, bare integers, and strings are rejected at these routes. External model/task constructors retain their documented integer/fraction-string normalization; callers may explicitly use `vector` for that bounded input profile. Derived witnesses and certificates have no 256-bit coefficient cap: the exact transformed point `(2^500−1,1,2^500)` passes. No float-to-Fraction coercion or tolerance was introduced. Invalid subjects may be represented for diagnostic validation; public mathematical operations reject them before returning conclusions.

No mathematical document was edited. Original/outer, witness/bound/attained optimum, common/strict/tied action, incompatible/unfinished, and impossible-event/empty-original distinctions remain intact. The 19 original cases retain identical observations and certificates.

## Current and historical execution

All recorded repair executions use existing CPython 3.9.6, normally and with `-O`. [Compact results and actual source hashes](repair_results.json) retain baseline negative evidence, 13 targeted repair groups, and original-case comparison without duplicate full rerun logs. Groups share the same Python exact arithmetic; they are not independent theorem proofs or new experiments.

From the repository root, current checks are:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verification/pr4_repair/repair_checks.py --output /tmp/bellman-repair.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verification/pr4_repair/repair_checks.py --output /tmp/bellman-repair-optimized.json
PYTHONDONTWRITEBYTECODE=1 python3 verification/joint_law_completion/module_checks.py --output /tmp/bellman-module.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verification/joint_law_completion/module_checks.py --output /tmp/bellman-module-optimized.json
PYTHONDONTWRITEBYTECODE=1 python3 verification/buildout_review/reviewer_checks.py --output /tmp/bellman-review.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verification/buildout_review/reviewer_checks.py --output /tmp/bellman-review-optimized.json
PYTHONDONTWRITEBYTECODE=1 python3 verification/substrate_buildout/checks.py
PYTHONDONTWRITEBYTECODE=1 python3 -O verification/substrate_buildout/checks.py
```

Results: 13 repair groups and 19 existing module cases pass; the portable reviewer passes 18 with packet integrity explicitly NOT_RUN; the portable author matches 17 mathematical groups and passes archive integrity. No failing repair case is omitted.

The exact supplied `pr4_review_probe.py` deliberately pins the defective source. Its actual baseline command was `python3 pr4_review_probe.py --repo PINNED_CHECKOUT --output NEW_FILE`, also with `-O`: nine groups, six reproduced paths, three controls. It is not a post-repair acceptance script; do not weaken its hash guard. The separate exact linear and mutation cases in the governing prompt were independently reproduced on source obtained with `git show` from the starting commit, and their corrected behavior is in `repair_checks.py`.

Historical `module_results.json`, `REPLAY_RECORD.json`, and `BUILDOUT_COMPLETION_MANIFEST.json` remain unchanged. Resolve their source paths at the starting commit above; current replay uses the repaired active reference and the new repair evidence. Source/version metadata differs intentionally. The bounded proposer is not a general solver; nonlinear optimization, scalable certificate discovery, and certified numerical radii remain outside this repair. Bellman's broader programme continues beyond this module.

## Source recovery limitation

The governing prompt was accessible, but `BELLMAN_PR4_FINISH_PACKET.zip` and its recovered source members were not accessible in the supplied locations. Its explicit section 3 fallback allows publication of completed repair while recording inaccessible artifacts. [Recovery status](recovery_status.json) distinguishes expected source hashes from actual verification; none of the five reported recovered originals was added or relabeled as executed. Packet-specific review/probe files and `RECOVERY_MANIFEST.json` were likewise unavailable. The earlier supplied `PR4_REVIEW.md` and singular `pr4_review_probe.py` are archived exactly under their actual names; they are not passed off as the differently named packet files. The separate v1.1 conformance harness remains unresolved. Earlier truthful unavailable-source records remain unchanged.
