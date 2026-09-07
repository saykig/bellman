# Exact finite joint-law completion

Read the [additive mathematical revision](../../foundations/BELLMAN_NEXT_MATHEMATICAL_BUILDOUT_REVISED.md) for assumptions, guarantees, certificates, failure cases, proof, and limits. This standard-library reference uses exact rational arithmetic and explicit resource caps; it is not production acceptance or a complete optimization platform.

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verification/joint_law_completion/module_checks.py --output /tmp/bellman-module-results.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verification/joint_law_completion/module_checks.py --output /tmp/bellman-module-optimized.json
python3 verification/substrate_buildout/checks.py
```

The new suite has 19 fixed cases, including exact primal/dual and Farkas evidence, stale-subject rejection, producer-independent consumption, ties, outer-versus-original models, and conditioning sharpness. Both modes passed on Python 3.9.6 with identical observations and certificates; optimized mode changes runtime metadata. `module_results.json` preserves the normal result exactly. Negative controls pass by rejecting invalid claims. Finite checks do not prove the general theorems, validate empirical premises, or establish coverage.

Original author source was separately recovered and rerun without editing: 18 groups passed; both original compact results and summary reproduced byte-for-byte. Its private absolute path precludes publishing raw source; the pre-existing portable replay preserves the same mathematical block and verifies the existing archive. No original file was overwritten.

The [replay record](REPLAY_RECORD.json) distinguishes exact original replay, optional-packet reviewer replay, public portable replay, and new completion checks. The [manifest](../../foundations/BUILDOUT_COMPLETION_MANIFEST.json) records actual available byte identities. No runtime was installed or globally changed. Disposable rerun copies and packet ZIPs are excluded.
