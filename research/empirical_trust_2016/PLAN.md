# Retrospective analysis plan — frozen before reduction evaluation

Date: 2026-09-09 UTC. Bellman baseline: v0.0.7 / 2cd6fd7432efccaacc734fd235549a564ddbff48.
This is a new secondary analysis of already published human data, not a prospective prediction,
external preregistration, independent replication sample, or equilibrium test. At fixation the
article, variable labels, row counts, treatment/session/role counts and first CSV rows have been
inspected. No full/reduced fit, held-out score or comparison has been calculated.

## Selection and provenance

Select Herne, Lappalainen, Setälä & Ylisalo, *Accountability as a Warrant for Trust*,
Theory and Decision 93 (2022), 615–648, DOI 10.1007/s11238-021-09864-7.
Human observations: FSD3661 v1.0 (2023-08-28), DOI 10.60686/t-fsd3661.
The archive's accessible CSV, labels, English instructions and CC BY 4.0 declaration
have been downloaded and inspected. 216 people, 12 sessions, six rounds, four treatments.
A selected-column projection will exclude demographics, attitudes and response-time fields;
original file hash and projection mapping will be retained. Never call this projection raw full data.

Alternative inspected: Falk & Kosfeld (2006), *The Hidden Costs of Control*,
DOI 10.1257/aer.96.5.1611; openICPSR E116246V1 lists original XLS, readme,
protocol appendix and paper. Its one-shot control/strategy-method comparison is less suitable
for a remembered-history query. No claim of inaccessible data; download not pursued after the
design comparison. FSD is chosen for actual access and repeated experience, not expected findings.

## Reproduction before extension

Reproduce Table 2's all-round sender means 5.70, 6.20, 6.89, 7.33 and returned-to-sender
means 8.00, 9.06, 9.82, 11.73 by treatment 1..4; rounding tolerance 0.005 points.
Use original role labels, all six rounds, and inspect contradictions/missingness before fitting.
No imputation of missing human observations. Any mapping correction receives an additive note.

## One query and one reduction

At the start of a sender's round t=2..6, predict their sent amount divided by 12, Y in [0,1].
Retrospective evaluation of models on entire held-out sessions. Query is conditional mean
prediction; squared error is a mean-eliciting loss, not a probabilistic distribution score.
Full representation **for this query**: treatment (four-category one-hot), round (five-category
one-hot), complete previous own sent amounts and complete previous amounts returned to that
sender. Five recency-indexed lag slots each; unoccupied slots zero with round distinguishing
absence. Scale sent by 12, returned by 84 (maximum responder resources).
Reduced representation erases the entire return sequence while preserving all previous own
sent amounts, treatment and round. This coarsens observed monetary experience; it does not
alter what humans saw or remembered. Neither representation contains all human information:
other senders' outcomes, justifications, sanctions, private attitudes and identities are excluded.
No current-round return, future outcomes or post-experiment survey features.

## Fixed fitting and split

Within each treatment hold out the session whose string ID minimizes SHA256 of
`bellman-fsd3661-holdout-v1:` followed by the decimal Session ID. All participants and rounds
of that session are held out. Thus eight training sessions, four evaluation sessions, one of
each treatment. Splits use IDs/treatment only. No outcome-driven split, feature, alpha or model choice.

Fit scikit-learn Ridge(alpha=1, fit_intercept=True, solver='svd') to the above fixed-scale
features separately for full and reduced, with outputs clipped to [0,1]. Do not standardize,
tune, or fit again after viewing held-out outcomes. Competent baselines: persistence (previous
own sent amount /12) and the training-only treatment-specific mean of Y on rounds 2..6.
All four predictions are evaluated on the same sender-round rows and with equal session weights.

## Uncertainty and decisions fixed in advance

Primary comparison: mean squared loss(reduced) minus mean squared loss(full).
Report each held-out session's paired difference, overall scores, and point-scale RMSE.
Prespecified equivalence margin: +/-0.01 normalized MSE (1.44 squared-point units);
this is an analyst tolerance, not an established domain threshold.
Primary uncertainty: Hoeffding's two-sided 90% interval for independent bounded session
loss differences D in [-1,1], conditional on training. Half-width sqrt(2 log(20)/4),
intersected with [-1,1]. Sessions may differ in treatment: target is their equal-weight
four-treatment mixture; require independence and within-treatment sampling exchangeability.
This conservative bound will be broad with four clusters. Equivalence requires the entire
interval strictly within the margin. No failure-to-reject-as-equivalence.
For a clearly labelled small-sample descriptive sensitivity only, report SciPy percentile
cluster bootstrap (whole paired session differences, 9999 resamples, seed 20260909,
90% interval). Four heterogeneous clusters make this approximation fragile; it cannot
supersede the primary interval or establish general predictive equivalence.

Reproduce treatment means descriptively. Additionally use statsmodels OLS on the 12 session
mean sent amounts with categorical treatment and a t-based interaction contrast (8 residual df).
This is a small-sample model-based estimate; causal reading is conditional on the reported random
allocation, no cross-session interference, and exchangeable session disturbances. The exact
allocation schedule is unavailable; no exact randomization p-value will be invented.

## Assurance and handoff

Exact integer/rational reconstruction checks data mapping, reproduced means, frozen inputs and
retained score arithmetic. A separate receiver must reconstruct feature timing and scores from
retained predictions with fitting disabled; it cannot independently certify statistical adequacy
or floating-point optimization. Reject forged/stale inputs, altered outcomes, scores or features.
Use established numpy/pandas/scipy/scikit-learn/statsmodels, no custom estimator or QRE.
Bellman's perturbation certificates are unrelated to finite empirical error rates.

Keep the case portable in Bellman unless actual Decision Lab/Writ contracts support its
statistical estimand and assurance. Current main IDs inspected: Decision Lab
 e5f77dfcf929708951f4673b3f394461ef09c752; Writ
 4e9b7f49e240e4ca5d6a8df0c6b8ecb060d606e2.
Their exact finite uncertainty and certificate-transport contracts do not by themselves receive
cluster-dependent empirical prediction evidence. A concrete transfer-gap report is permitted.
A meaningful successor changes the intended use from retrospective prediction to a claim about
hiding feedback from people; it must refuse to inherit a predictive score as causal evidence.

Primary sources: https://services.fsd.tuni.fi/catalogue/FSD3661?lang=en&study_language=en ;
https://link.springer.com/article/10.1007/s11238-021-09864-7 ;
https://www.openicpsr.org/openicpsr/project/116246/version/V1/view .
