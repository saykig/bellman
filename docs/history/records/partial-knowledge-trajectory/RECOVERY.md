# Recovery and revisit guide

## Follow the actual dependencies

R01 supplies the causal/relational foundation. R02 branches into revision and
named provenance; its larger proposed experiment remains unrun. R03 starts the
information–incentive application using supplied external notes and an audit.
R04 changes the game to a three-state partial-certificate setting. R05 investigates
its perfect-gate obstruction and adds overlapping certificates/asymmetric priors.
Do not silently transport numerical values or game assumptions between R03 and R04.

For a suspected issue:

1. Locate the phase and exact theorem, assumptions, source notes and original log
   through [PROGRESS.md](PROGRESS.md).
2. Identify the particular artifact version using Git and the dated inventory.
   The inventory hashes content; it is not a proof of correctness.
3. Inspect which later claim uses that premise. Particularly check shared-budget
   attainability, common continuation witnesses, support, known-law assumptions,
   equilibrium selection, and whether the gate is supplied or optimized.
4. Reproduce only the relevant check using its own instructions. Save new output
   separately; never overwrite old receipts. The R02 larger experiment was not
   executed historically and must not be presented as a replay of past evidence.
5. Append a correction/recovery entry, preserving the original result and explicitly
   marking which conclusions survive, fail, or remain unresolved.

## Git recovery

Use `git log --oneline -- <artifact-path>` to find its history and
`git show <commit>:<artifact-path>` to inspect an earlier version without changing
the worktree. Extract into a separate temporary location when replay is needed.
No branch creation, history reset, deletion or force push is needed for inspection.

The inventory records baseline `ad16961` for already tracked artifacts and names
R06 as the first preservation event for previously untracked material. Use
`git log --all --grep='Preserve prior research phases and consolidate the research trajectory ledgers'`
to find that preservation commit. This avoids embedding a self-referential hash.

## What is and is not preserved

The original five research folders remain in place. All 60 previously untracked
R02–R04 research artifacts are included unchanged in the preservation commit, as
is the existing September 17 research-purpose statement. Its temporary no-commit
constraint has been superseded by the later user request; its text is retained.

The original foundations README has unrelated working-tree navigation edits; this
pass leaves those edits untouched. Its inventory entry describes the baseline Git
version. The local foundations AGENTS.md is not treated as a research artifact
and is not included. No caches, environments, vendor trees or scratch output are
archived. No existing source manifest or historical receipt is rewritten.

External Downloads inputs are identified by the R03 input manifest. Primary-source
PDF identities and retrieval gaps are recorded in each phase's source notes.
Those external bytes are not newly imported here. A hash permits identity checking
if the source is recovered; it does not guarantee future access. The original
empty-checkout recovery bundle is likewise described by R01, not newly recovered
or independently verified by this pass.

This ledger is a repository-backed record of the available research, not a claim
that all original conversations or external files have been archived.

## R07 recovery — 18 September 2026

Start with [the gate-recovery audit](../../../../research/optimized_gate_recovery_2026_09_18/AUDIT.md)
and mathematical/evidence edition `e2daee7`. Activation was `a3bb951`; predecessor
and preservation identities remain `26d3415`, `ad16961`, `5661f9e`. Run the new
receiver directly using [its reproduction instructions](../../../../research/optimized_gate_recovery_2026_09_18/experiments/README.md);
it does not execute the candidate producer. Save any new results separately.

The key recovery inputs are the sender information partition, sequential-consistency
restriction and positive gate-contrast constraint. Removing any of them can change
the answer. Source notes use the directly read July 2025 signaling draft rather
than claiming access to the January 2026 Drive draft. The PWI PDF was text-readable
through the web tool, but direct byte retrieval returned HTTP 406; no new hash was
recorded for it. Other downloaded-source hashes identify bytes, not archival copies.
