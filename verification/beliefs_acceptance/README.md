# Current acceptance: mathematical release, FSD and AFY 2024

This additive entrypoint preserves the entire pre-existing eec4f51 research snapshot except
explicit living guidance/CI files. It replays the previous aggregate at 349cc42, where its
closed inventory and source-bound receipts still apply. It does not weaken or overwrite
v0.0.7, FSD or first AFY evidence.

Explicit acquisition is separate from deterministic tests. Raw author rows are not in Git:

```sh
python -m pip install -r research/empirical_trust_2016/requirements.txt
python research/beliefs_2024/reproduce.py acquire /external/Aoyagi_2024a_data.txt
PYTHONDONTWRITEBYTECODE=1 python verification/beliefs_acceptance/acceptance.py --source /external/Aoyagi_2024a_data.txt --recompute --verify-retained
```

Full acceptance checks frozen identities and mutation controls; inherited mathematical and
FSD receiving/recomputation at their editions; AFY prediction, prior-certificate, inference
and portable-use checks normally and under `-O`; and fresh AFY source-only response fitting
and target scoring against retained source-mixture fits. The separate AFY reproduction
checkpoint retains an actual full R mixture refit. R need not be installed for ordinary
receiving or this aggregate replay.

`--strategic`, `--causal`, `--history` preserve the corresponding inherited CI routes and
check AFY frozen identities. They do not claim empirical replay without the separately
acquired raw file. Full CI has a named acquisition step and never implicitly fetches data
inside a deterministic check. A network/acquisition failure cannot be reported as a pass.

[results.json](results.json) is creation-only and binds the current entrypoint, new audit,
living guidance and workflows to committed source bytes. Earlier receipts retain their
original scope. `--record` requires full recomputation and committed sources; the receipt
itself is excluded from its source manifest.

Arithmetic conformance, numerical reproduction, statistical sampling validity, empirical
identification, external peer review, formal verification and authority remain separate.
The [completion audit](../../research/beliefs_2024/COMPLETION_AUDIT.md) and
[identification report](../../research/beliefs_2024/IDENTIFICATION_AUDIT.md) state the limits.
