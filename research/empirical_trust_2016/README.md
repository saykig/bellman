# A human trust case: what past returns help predict

This is a retained retrospective case, not a completed empirical theory of credibility.
Herne and colleagues' human experiment varied sanctions and required justifications. We reproduced
all eight published treatment means for money sent/returned, then evaluated a fixed history
comparison on four entirely held-out sessions. [Original archive](https://doi.org/10.60686/t-fsd3661).

| Predictor | Held-out RMSE (points out of 12) |
|---|---:|
| Previous own sending, treatment and round; return history retained | 2.511 |
| Same representation, return history erased | 2.590 |
| Repeat previous own amount | 2.703 |
| Training treatment mean | 4.631 |

The full-history model did modestly better in this sample. The primary uncertainty interval is
uninformative with four independent held-out sessions; equivalence is **not established**.
A narrow four-cluster bootstrap sensitivity cannot fix the small independent sample.
This comparison changes the analyst's representation, not what participants see.

The original sender means were 5.699, 6.199, 6.894 and 7.333 across baseline, punishment,
justification and both. Their increasing order does not establish synergy: the session-level
interaction is -0.060 points with a model-based 95% interval [-5.578, 5.458]. This is a
small-sample diagnostic, not an exact randomization p-value or a general claim about institutions.

**Learned:** recorded personal history predicted behavior better than a treatment-only mean on
this split. Why it predicts remains unresolved: stable participant tendencies, context and
reaction to experience need distinguishing. Feedback visibility was never randomized. Two exact
mathematical extensions of the observable law disagree completely about hiding it. Utilities,
private beliefs, reputation, and shared off-path equilibrium consistency are not measured here.

**Next:** the current [design checkpoint](../empirical_design_checkpoint/RECOMMENDATION.md)
considers retaining and improving this question alongside experiments with continuing partners,
measured beliefs and changed incentives. The study is not discarded for having a modest result.
The next observation for its original causal-erasure query would be a randomized visibility
contrast before a subsequent transfer; no such intervention was performed.

## Inspect and reproduce

- [Frozen plan](PLAN.md), fixed/pushed at d9c0075 before prediction evaluation.
- [Source and projection identities](provenance.json); [original-to-projection checker](reproduce_projection.py).
- [Retained results and predictions](results.json); [identification and proofs](IDENTIFICATION.md).
- [Research record](RESEARCH_LOG.md); [portable handoff and concrete gap](TRANSFER.md).
- [Source-bound checkpoint validation](checkpoint-validation.json).

Use Python 3.12 and a temporary environment; no live network access occurs during analysis/checks:

```sh
python3.12 -m venv /tmp/bellman-trust
/tmp/bellman-trust/bin/pip install -r research/empirical_trust_2016/requirements.txt
PYTHONDONTWRITEBYTECODE=1 /tmp/bellman-trust/bin/python research/empirical_trust_2016/analyze.py /tmp/new-trust-results.json
PYTHONDONTWRITEBYTECODE=1 /tmp/bellman-trust/bin/python research/empirical_trust_2016/checks.py
PYTHONDONTWRITEBYTECODE=1 /tmp/bellman-trust/bin/python -O research/empirical_trust_2016/checks.py
PYTHONDONTWRITEBYTECODE=1 /tmp/bellman-trust/bin/python research/empirical_trust_2016/check_handoff.py
```

The producer refuses to overwrite output files. The independent receiver uses only Python's
standard library, reconstructs timing and arithmetic, and checks numerical fit residuals. It
rejects 14 semantic/identity controls with the producer and statistical imports disabled; the
portable revision has three additional controls. It does not verify statistical or empirical
premises. Historical check evidence remains bound to its recorded commit. Later documents add
interpretation without changing the original plan or predictions.

For original-source reconstruction, download FSD3661 v1.0 through its archive, extract
`daF3661_eng.csv` outside the repository, and run `reproduce_projection.py` with that file path.
The script verifies the original hash and exact column selection. This repository contains a
cited 15-column projection, not the original full survey data. CC BY 4.0 applies to the archived
data; retain attribution and consult the archive's publication-notification request before public
publication. The creators and archive are not responsible for this secondary analysis.

At this checkpoint, frozen v0.0.7 files are unchanged. The old combined-acceptance entrypoint
has a closed release inventory, so its successor for the expanded tree remains outstanding.
Checkpoint checks must not be described as completion of combined programme acceptance.
