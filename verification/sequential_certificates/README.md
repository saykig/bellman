# Sequential certificate checks

Read the [mathematical construction](../../foundations/BELLMAN_SEQUENTIAL_CERTIFICATE_COMPOSITION.md) for the subject, proofs, guarantees, examples, and failure boundaries. This is a standard-library rational research reference, not a general solver or Writ integration.

From the repository root, using its existing Python runtime:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verification/sequential_certificates/run_checks.py
```

The command executes the new fixed cases normally and with `-O`, compares observations, reruns current PR4 repair and joint-law checks in both modes, compares historical joint-law answers/certificates, and checks that base historical files are unchanged. It uses temporary result files only. It prints one compact JSON result between explicit markers. The read-only GitHub Actions workflow runs the same command using its existing Python; no runtime or dependencies are installed. The workflow checks out the exact PR head, with its base history available. Its [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) is used only for execution, not as mathematical evidence.

The base is `b1266137f824dc65e614722f1f0592846b915262`, main after merging PR4's repaired `efba25bc3a52535e331fe21fe364f394029c853c`. Their file trees match. Run against a checkout that includes this base commit. No historical recovery ZIP or missing harness is required or claimed rerun.

`reference.py` contains immutable exact subjects, whole-policy and residual certificate checkers, a separate backward producer, root-action bounds, conditioning arithmetic, forward path evaluation, tiny full-policy enumeration, and telescoping checks. `checks.py` fixes the literals and decisive negative/positive controls. The consumer does not call `produce`; it shares Fraction arithmetic, schema, and a local sum helper. Forward path sums avoid that helper. This is calculation-path separation, not independent authorship or formal verification.

The completed execution record is retained as `results.json`, with the executed source commit, actual runtime, observed results, source SHA-256 identities, and preservation checks. Runtime/source metadata belongs to this new run; old result files and manifests remain unchanged. If sources later change, rerun and add new evidence rather than rewriting this frozen result to fit different bytes.

Limits: horizon 0–4, at most 64 nodes, four actions and outcomes, and at most 4096 policies for optional exhaustive cross-checking. Model coefficients are exact integers/Fractions with a 256-bit input bound; derived proof tables use arbitrary-size Fractions. Floats and booleans are rejected. Information labels are supplied semantic premises, not empirical proofs of access. Tree completions on zero-probability histories are not posteriors. Enumeration refusal is unfinished, not incompatibility.

Scalable computation, richer uncertainty/risk/causal/strategic structures, and interoperable engineering remain outside this module and inside Bellman's wider programme.
