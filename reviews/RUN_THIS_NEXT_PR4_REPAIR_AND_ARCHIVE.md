# Execute: Bellman PR #4 reference repair and source-archive completion

## Task and environment

Work in the **cloud environment** on the existing `saykig/bellman` repository. Do not use or create a checkout on Sara's laptop. Read any current `AGENTS.md`, README, relevant record rules, and the supplied `PR4_ADVERSARIAL_REVIEW.md` first.

This is a bounded repair and source-archive completion, not another mathematical expansion, broad audit, language migration, or Writ integration task. The mathematics remains a continuing programme and is not limited by this reference implementation.

Review target: PR #4, branch `codex/bellman-buildout-completion`, reported head `81fbcc4d503275f091c8c31588ac02d3abf14466`. Inspect the actual current head and ancestry before editing. If it advanced, preserve and account for intervening work. If PR #4 has already merged, use a small follow-up branch from latest main rather than resetting or rewriting it.

Running this prompt authorizes scoped code/documentation/tests, commits, a push to the existing PR branch (or a follow-up PR if already merged), and remote read-back verification. Do not merge, force-push, create another repository, change visibility, modify Writ/Decision Lab, or change the user's machine/global settings.

## 1. Reproduce two concrete findings before repair

Use the supplied pinned original-source reproducer or independently construct these exact cases. Do not weaken its hash guard to run it on revised source. Convert the desired corrected behavior into separate durable regressions.

### R1: original-witness validation

`original_member`, `forward`, and the original-witness routes in `decide`, `fixed_minimizing_set`, and `impossible_event` can reach arithmetic without the exact-number validation used by `consume`.

With `N=2**54+1`, require nonnegative masses satisfying `x0+x1=1` and `N*x0+N*x1=N-1`. The original domain is empty. The exact Farkas vector `(-N,1)` proves this.

The old code accepts `(0.5,0.5)` as an original witness and can certify the zero-loss action over a one-loss competitor. It correctly rejects the corresponding rational witness. Also reproduce the erroneous nonempty-original classification via `impossible_event`.

Apply exact input validation before any witness arithmetic on all relevant public routes. Floats and booleans must be rejected, not silently converted with `Fraction(float)`. Exact integers/strings may be normalized only under the explicitly documented accepted input rules. Preserve exact computed witness/certificate coordinates beyond the model coefficient-size cap; the review's valid transformed point `(2**500-1,1,2**500)` is a positive control, not an oversized input coefficient.

### R2: detached original-constraint subjects

A `Polynomial` can hold a caller-owned list of terms. Passing it through `make_model` does not detach nested data. Clearing that list changes an existing certificate's original-model constraints and promotes a midpoint witness from `outer_attained_only` to `original_attained`.

Normalize/detach polynomial terms and exponents into immutable exact data, or reject mutable/non-normalized forms. Make accepted premise/label payload rules explicit and stable. Test constructor aliases and nested mutation. Deliberate revisions should produce new subjects; unchanged certificates must not silently change their embedded mathematical meaning. Do not build an in-process authentication framework.

## 2. Preserve the mathematical reference and evidential distinctions

Retain the posterior extrema `4/7, 8/11`, strict action-difference upper bound `-1/7`, changed-loss range `[-2/11,2/7]`, tie behavior, Farkas signs, original-versus-outer labels, positive-event support, exact inverse, and unfinished-search meanings.

Keep the stronger conditioning theorem. These findings do not refute weak duality, conditioning, or the revised mathematical proof.

Run the existing module cases normally and optimized, the new negative/positive controls, and the available portable reviewer checks. Report actual counts and shared dependencies. Missing historical material is a disclosed archival limitation, not automatic evidence of a new mathematical failure.

Preserve frozen mathematical documents, reviews, historical results, and old manifests. Repair active code with clear new version/commit evidence. If repository rules designate the code snapshot itself frozen, make a small explicitly versioned successor rather than overwriting it. Do not duplicate entire directories or silently make a historical manifest refer to different bytes. Explain how historical and current replay resolve their correct source versions.

## 3. Complete genuinely recoverable archive gaps

Use the exact recovered source files supplied with this task or retrieve the actual prior attachments through available file access. They include:

| Source | SHA-256 |
|---|---|
| Original substrate v1, 62,246 bytes | `af60646d0118dce72abc65d7440a4faf9e8ed305ca6ffefc00775cc84204bc22` |
| Original `fixed_checks.py`, 18,071 bytes | `8734a8a9fecec01172930b5e163bae307df2a82eb43c1002bcb2a8174d843f01` |
| Original `fixed_check_results.json`, 2,605 bytes | `8205a1db18bc7d60ddd4e384afd75aed78eaea45763532d90a9de81d354ed48f` |
| Original `fixed_check_log.txt`, 2,463 bytes | `1f7c16e517d0cef63d6b9621abb167b6940b8991859ab4eeb42481609e58d8cf` |
| Original `source_manifest.json`, 1,355 bytes | `862dcb5e5bc545a5cc535c0f1a4f0a497a4f628e168f5a9f36f7a40a9b6b2bcd` |

Verify the bytes before addition. Record that they were unavailable to earlier runs and recovered later. Do not relabel them as newly executed tests. The v1.1 conformance harness is a different source and remains unavailable unless actually recovered. Do not recreate it and call it original.

If any actual source cannot be accessed in this cloud task, record that specific remaining gap without fabricating content or blocking otherwise complete code repair.

## 4. Repository hygiene: curate, do not erase research

Keep the current foundation/review/verification/experiment organization. The reviewed snapshot is only about 594 KB; no wholesale pruning is warranted.

Preserve old mathematical versions, negative findings, stopped experiments, substantive reviews, small reference/check source, compact outputs, exact source identities, and a historical governing brief where it is relevant provenance.

Exclude new caches, environments, build products, dependency/vendor trees, duplicate ZIPs, private machine paths, full chat dumps, repeated status documents, and redundant rerun logs. Do not ignore all JSON or all outputs: intentional certificate/results files belong in version control. Keep dependency lockfiles when a real implementation needs them.

Add concise ignore rules and a short repository instruction if absent. Distinguish frozen records from active code, explicitly permit mathematical progress using established results, and keep README/current pointers separate from historical ledger entries. Do not add a fourth overlapping progress ledger.

## 5. No scope expansion

Do not extend the handwritten active-set proposer into a general LP solver. Keep it as a bounded reference. A later engine task may use an established exact optimizer in an appropriate language and check its results against this contract; do not perform that migration in this repair.

Do not add a Bellman DSL, graph database, causal/strategic/risk engine, or another model grid. Do not delete broader mathematical sections merely because they are not yet implemented. KL5/KL6 remain closed.

## Deliver and stop

Return one concise repair-and-archive report identifying the exact reviewed/repaired source, reproduced findings, smallest fixes, tests and commands actually executed, compact evidence, recovered source identities, remaining archival gaps, and the branch/commit/PR link.

Commit and push only curated work, verify remote file identities, and leave the PR unmerged. End after this task; do not start the next mathematical or engineering build.
