# Certificate accumulation verification

[Mathematical contract and proofs](../../foundations/BELLMAN_CERTIFICATE_ACCUMULATION_AND_POLICY_SELECTION.md).

Run with the existing Python runtime from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verification/certificate_accumulation/run_checks.py
```

The command runs new checks normally and with -O, compares results, invokes the unchanged transport/preservation runner, and verifies frozen bytes against PR6 head `cd649db893c70bbce4891c8f526a27aaf1bcda1b`. Temporary execution outputs are not archived. GitHub Actions uses the existing runner Python with no installation.

`accumulate.py` imports PR5/PR6, provides separate same-policy and selector producers, an independent combination receiver, and an extra exact-policy-value receiver for actual dominance. Requests retain complete source certificates and identities. Any invalid source rejects the entire requested collection. Source identifiers are value bindings, not authentication.

`checks.py` fixes A–H cases and independent path/policy calculations. `results.json` records actual counts, runtimes, source commit and hashes; an evidence-only successor leaves executed sources identical. Supplied reviewer checks are read as evidence but not claimed freshly replayed. Historical evidence remains unchanged.

Limits: sixteen sources, inherited finite history profile and exact coefficient limits; derived proofs have no bit cap. Bounds are not attained values or statistical confidence. Model premises remain assumed. No Writ integration, general solver, migration, experiment, or mathematical ceiling is implied.
