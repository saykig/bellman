# Beliefs in Repeated Games: retrospective incentive challenge

The specification was committed and pushed at **4abea07 before fitting**. First replication,
source-only fits, target predictions and results are retained at **f541369**. The prior-sensitivity and utility review is retained at f3d0397. This is ongoing
research: final identification audit, programme guidance and combined acceptance remain
outstanding. No completion or empirical mechanism identification is claimed.

The first run reproduces the paper's indefinite first-three-round action/report gaps
(10.89, 5.79, 1.97 percentage points). Under primary linear stage utility, the target
Brier difference updated-minus-fixed is -0.000407, with a session bootstrap interval
[-0.001866, 0.001228]. The comparison is inconclusive. A simpler history/report logistic
baseline performs better than either candidate in both target treatments. The prespecified
utility sensitivities change the conclusion within the candidate pair; they do not estimate
human utility. See [the plan](PLAN.md), [derivation](METHOD.md) and [source limits](SOURCES.md).

## Reproduce

Python dependencies are the existing pinned statistical stack in
`../empirical_trust_2016/requirements.txt`; this calculation uses NumPy, pandas and SciPy.
Mixture fitting additionally uses R 4.4.2, stratEst 1.1.8 and its Rcpp dependencies.
The retained R runtime files describe the first run. No raw data, source-input CSV,
participant assignment table or post-fit individual classification is redistributed here.

Download the author data explicitly from the URL in source-manifest.json to a location
outside the repository. Both the producer and receiver reject a changed hash. Receiving
needs only Python's standard library and that source file:

```sh
PYTHONDONTWRITEBYTECODE=1 python research/beliefs_2024/checks.py /external/Aoyagi_2024a_data.txt
PYTHONDONTWRITEBYTECODE=1 python -O research/beliefs_2024/checks.py /external/Aoyagi_2024a_data.txt
```

The receiver checks frozen source/output hashes, canonical automata, exact rational Markov
residual bounds, decision-time reconstruction, all target predictions and session scores.
It blocks imports of the producer and statistical libraries. This is not a bootstrap
coverage proof, global mixture-optimum certificate, assignment audit or formal verification.

For replication and fresh scoring from the retained source-only mixture fits:

```sh
python research/beliefs_2024/reconstruct.py /external/Aoyagi_2024a_data.txt /external/replication.json
python research/beliefs_2024/analyze.py /external/Aoyagi_2024a_data.txt research/beliefs_2024/mixture-fits /external/new-results
```

The output directory must not already exist. The analyzer independently reconstructs each
R mixture likelihood, refits response coefficients using source-only validation, and scores
the two target arms. Re-estimating the mixtures uses fit_mixture.R with a source-only CSV
containing treatment, session, id, supergame, round, coop, o_coop; restrict to treatment 2,
supergames >=5 and rounds 1..8. Training excludes sessions 1 and 14; the final fit uses all
eight source sessions. Run each table once with catalogue argument `ten` and once with `six`.
The wrapper rejects target treatments and out-of-scope sessions/times. End-to-end acquisition and refitting are now explicit:

```sh
python research/beliefs_2024/reproduce.py acquire /external/Aoyagi_2024a_data.txt
python research/beliefs_2024/reproduce.py run /external/Aoyagi_2024a_data.txt /external/fresh-run --refit-mixtures
python research/beliefs_2024/reproduce.py run /external/Aoyagi_2024a_data.txt /external/optimized-run --optimized
```

If R packages use a separate library, set `R_LIBS_USER` before invoking the refit. Without
`--refit-mixtures`, the runner uses the retained source-only mixture estimates but freshly
fits/tunes the response predictors. It rejects working directories inside this repository.
The first full refit and optimized replay reproduce retained predictions exactly on one host;
the runner allows a declared 1e-7 numerical prediction tolerance on other supported hosts.
Every fresh result is independently received.

The [prior review](PRIOR_AND_UTILITY_REVIEW_20260909.md) corrects the frozen plan's figure
number and distinguishes sharp per-history extrema from shared-prior outer bounds. Run:

```sh
python research/beliefs_2024/sensitivity_checks.py /external/Aoyagi_2024a_data.txt research/beliefs_2024/prior-sensitivity-results.json
python research/beliefs_2024/check_transfer.py /external/Aoyagi_2024a_data.txt
```

[TRANSFER.md](TRANSFER.md) records the current downstream contract gap and meaningful
changed-use rejection. No Writ or Decision Lab adapter was added.

Frozen first-run outputs must not be regenerated in place. The current aggregate inventory
gate rejects this newly added research until an additive acceptance entrypoint registers and
checks it; that known failure does not invalidate the preserved v0.0.7 or FSD receipts.
