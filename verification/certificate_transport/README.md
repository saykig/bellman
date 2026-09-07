# Certificate transport checks

Read the [construction and proofs](../../foundations/BELLMAN_CERTIFICATE_TRANSPORT_AND_REVALIDATION.md). This additive module uses the unchanged PR5 subject and ordinary certificate consumer.

From the repository root, with an existing Python runtime:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verification/certificate_transport/run_checks.py
```

The command executes fixed transport cases normally and with -O, compares exact observations and rejection counts, invokes the existing sequential preservation command (17 sequential groups, 13 PR4 repair groups, 19 joint-law cases per mode), and compares historical joint-law values/certificates. It checks that base `e4139b6c68f0386b62bf6332b12d2f654c1d4faf` files remain byte-identical except README and append-only current ledgers. The GitHub Actions workflow checks the exact PR head using the runner's existing Python; no dependencies or toolchain are installed.

- `transport.py`: immutable requests/correspondence, correction producer, separate envelope receiver, and target-induced positive-prefix continuation checks.
- `checks.py`: literal fixed examples, decisive negative/positive controls, independently coded forward path sums and complete tiny policy lists.
- `run_checks.py`: normal/optimized and historical preservation orchestration, compact JSON output.
- `results.json`: actual executed commit, runtime, counts, times, fixed observations, and SHA-256 identities. An evidence-only successor can include this record while leaving the executed mathematical sources identical.

Ordinary target consumption and transport provenance are deliberately different checks. Receivers do not call either producer. The prefix interface binds target, event history, prefix policy, continuation policy, and ordinary certificate; mass is recomputed from target transitions. There is no free-standing trajectory-vector evidence route.

Limits: same ordered completed history skeleton, criterion and unit; total deterministic accessible policies; horizon at most four and at most 64 nodes, four actions/outcomes. Input model coefficients have PR5's exact 256-bit profile. Derived rational tables/corrections have no inherited bit cap. Unsupported structure/access/criterion changes require another mathematical correspondence, not automatic rebinding. The reference is not a general mapper, solver, statistical coverage procedure, or formal verifier.

New fixed checks are distinct from the supplied review's reported Python 3.13.5 audit. No byte-identical reviewer-script replay, unavailable harness, historical experiment, or Writ/Decision Lab execution is claimed. Historical sources/results remain unchanged. Repository work uses the GitHub connector and mathematical execution uses GitHub-hosted Actions; no laptop checkout or execution is required.
