# Completed build-out: verification evidence and replay

These files accompany the [completed mathematical build-out](../../foundations/BELLMAN_NEXT_MATHEMATICAL_BUILDOUT.md). They are intentionally distinct from the unavailable v1 adversarial-review harness.

- `checks.json` is the exact frozen result record from the completed mathematical task: 18 passing groups under Python 3.9.6, comprising 17 mathematical checks and one integrity check of eight supplied packet inputs.
- `CHECKS.md` is the exact frozen human-readable summary from that task. Its statement about the original workspace not being a Git repository describes that original execution, before this archival PR.
- `checks.py` is an archival portability adaptation. The mathematical calculation block is unchanged. Machine-specific packet paths and output-writing code are removed; the input-integrity check now verifies the six frozen artifacts in `foundations/SOURCE_MANIFEST.json`. It compares all 17 mathematical result entries with `checks.json` and never overwrites the frozen evidence.

Run from the repository root with Python 3.9 or later, using only the standard library:

```sh
python3 verification/substrate_buildout/checks.py
```

An archival replay completed under Python 3.9.6: all 17 mathematical groups matched the frozen result record, and all six archive identities passed. This replay is a distinct run with different integrity inputs, not a rerun of the missing historical v1 tests or of the original eight-file packet check. The old packet's relative filenames/digests in `checks.json` document the original run; those external engineering inputs are not dependencies of the portable replay and are not copied into Bellman.

The checks cover finite rational examples: compatibility and gluing, one fractional-transform witness, structural abstraction, Bellman residuals and local regret, an exact simulator, contextual failure, signed losses, coupling and conditioning, robust timing, coverage allocation, tail risk, and an identified action under an uncertain posterior. They do not implement a general LP solver, independently verify all proofs, sample empirical data, or establish Writ production acceptance. No large logs or disposable runtime outputs are retained.
