# Combined strategic and causal acceptance

Current entrypoint after integrating main's merged PR #21 into PR #22:

```sh
python -m pip install -r verification/sequential_consistency/requirements.txt
PYTHONDONTWRITEBYTECODE=1 python verification/combined_acceptance/acceptance.py --verify-retained
```

This checks two preserved lineages: strategic head
`56fb71616212af9719ae7a264eb8c4829d80f235` and main
`4866ffce9b3e935b86188d3fe981d4b9240f0740`. All common frozen files must agree. Main's
historical ledger additions must retain the strategic snapshot as an exact byte
prefix, and the integrated ledgers must equal main's bytes. Only three living
programme documents and four CI entrypoints are editable exceptions. New integration
files have an explicit allowlist. Both evidence-mutation controls and an unregistered
addition control must reject.

The full command replays the strategic aggregate (including its inherited causal and
history chain) at the strategic snapshot, and the kernel-fibre aggregate with its
source-bound receipt and inherited checks at the main snapshot. It also executes
both latest component checks in the actual integrated tree, normally and under `-O`.
Those checks retain their own producer-disabled receiving controls. The wrapper does
not weaken either historical scope guard or rewrite any result/source manifest.

`--strategic`, `--causal`, and `--history` select CI obligations. The causal mode runs
the complete kernel-fibre aggregate and live kernel-fibre checks; strategic mode runs
the strategic aggregate and live diagnostic checks; history mode verifies the entire
frozen union and replays strategic history acceptance. All modes verify the combined
receipt when requested. Only default/strategic mode requires SymPy. Delegated workflow
labels are not counted as mathematical replay.

[results.json](results.json) binds the integration sources to their committed bytes,
records the frozen-union digest and fresh combined observations, and excludes itself
from its source manifest. The prior diagnostic and causal receipts remain unchanged.
Old component README commands describe their retained historical editions; use this
entrypoint in the integrated checkout.

This is repository and validation integration, not a new theorem connecting causal
kernel fibres to strategic disclosure, payoffs, information, beliefs or monitoring.
PR publication follows separately authorized merge and release gates. Writ and Decision Lab are outside this change.
