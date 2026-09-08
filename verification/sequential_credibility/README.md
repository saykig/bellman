# Assessed sequential credibility: exact bounded reference

The [mathematical companion](../../foundations/BELLMAN_SEQUENTIAL_CREDIBILITY_UNDER_UNCERTAINTY.md) defines the guarantee. Start there: `assessment-relative-pass` is not a sequential-equilibrium certificate.

## Run

From the repository root, using Python 3 (standard library only):

```sh
python3 verification/sequential_credibility/run_checks.py
```

Receive the retained positive example independently:

```sh
python3 verification/sequential_credibility/receiver.py verification/sequential_credibility/example_subject.json verification/sequential_credibility/example_certificate.json
```

An explicitly requested nonzero tolerance is a third argument to the receiving command. The default query is zero; changing a certificate's tolerance does not change the receiving query.

## Contract

- A nonempty finite family shares one finite rooted tree, information sets and one behavioral profile. Model identity is not a strategy input.
- Player labels A/B; exact canonical rational strings; at most 300 nodes, depth 24, four actions per node, 16 models and 4096 pure plans per continuation query. These are implementation limits, not mathematical impossibility results.
- Chance/payoff/belief coverage is complete. Perfect recall, information-set action menus, probability normalization and on-path Bayes conditioning are checked.
- Off-path beliefs are explicitly supplied. Tremble consistency and equilibrium existence/search are unsupported.
- Every model/information set has one row with baseline, exact best continuation, gain, full legal maximizing plan and plan count.
- Positive and negative candidate certificates are both receiveable: `profitable-deviation` certifies a failure witness and exact maximum, not a malformed result.
- Generic continuous fibres are not executable subjects. The companion proves a restricted analytic corner criterion and identifies its unsupported boundaries.

`producer.py` evaluates recursively. `receiver.py` independently enumerates continuation plans and sums terminal paths iteratively. They share structural validation, rational parsing and identity in `subject.py`; the receiver does not import the producer or fixtures. This is a small research checker, not a hardened hostile-input service or independent formal proof. Schema limits are not a general computational resource guarantee.

The retained positive fixture has 63 nodes, 20 information sets and four models. It combines private good/bad quality, selective hard evidence, zero/nonzero bond, acceptance/rejection, compliance/defection and imperfect detection. It has no fitted data or causal-identification certificate.

## Evidence

`run_checks.py` compares normal and optimized Python execution, invokes a receiver in an isolated temporary directory containing no producer, and verifies byte preservation of base files except the three explicitly updated living steering documents. It emits a summary to stdout; it does not overwrite retained evidence.

`results.json` records the source Git commit and hashes of the mathematical companion, implementation, harness, steering and review files. `example_subject.json` and `example_certificate.json` are retained exchange examples; the certificate binds subject identity, not a claim that the source model is true. `run_checks.py --verify-retained` checks source-file hashes and the receiving example before running the suite. Base-preservation checks require the recorded base commit in the Git object database.

The suite includes exact positive values; weak-bond and costly-mechanism failures; full-continuation and off-path threat controls; model restriction; exact renaming and a 2-delta utility perturbation; scalar maxmin/uniform and conditional-corner counterexamples; malformed, missing, forged and stale subject/query/certificate rejections. Scalar examples and fixed fixtures are arithmetic tests; continuous propositions are analytic derivations, not validated by sampling.

No existing mathematical source, verification record, experiment or release identity is rewritten. The historical suites are not rerun because no old code is changed and no old checker is called as a dependency. Byte preservation is reported separately from test replay. Hosted CI, external solver comparison, formal Lean verification and third-party review have not been performed.
