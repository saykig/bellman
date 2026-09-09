# AFY 2024: fixed retrospective incentive challenge

9 September 2026. Baseline Bellman main 349cc42b11a0cd85ba95523ea530bf80fd93e596.
This specification is to be committed and pushed before new human-data model fitting or scoring.
The original papers, figures, first raw rows and structural counts have already been inspected.
This is a retrospective held-out challenge, not a prospectively unseen experiment.

## Subject and acquisition

Use the author-distributed Aoyagi_2024a_data.txt at the SHA256 in source-manifest.json, the
16 October 2024 author paper and its appendix. No raw author data are checked into the repository.
Acquisition is explicit and external to deterministic analysis/checking. A different hash requires
an additive edition decision, never silent substitution. SOURCES.md distinguishes this author
edition from the inaccessible authenticated archive download and the archive's displayed licence.

Source reconstruction precedes fitting. Assert unique (session,id,supergame,round), complete
within-person sequences, session-fixed treatment, matched own/opponent action totals, balanced
CD/DC counts and own/opponent belief totals within session-game-round. Pair identities themselves
are not in the author table and must not be fabricated. Reconstruct common termination draws,
post-four-supergame elicitation, structural missingness, early/late flags and payment-validity.

Treatments: finite 1, base indefinite 2, High T 3, Low R 4. Base stage payments (CC,CD,DC,DD)
are (51,22,63,39); High T changes 63 to 73, Low R changes 51 to 45. Indefinite continuation is
7/8. Finite horizon is 8. At least eight choices are recorded before block termination is revealed.
Beliefs are elicited after one's current action and before feedback. The first four supergames
have no elicitation; blank beliefs there are not zero. Finite validround is not applicable.

Reproduce main-paper Figure 2's late-supergame first-eight-round action/belief means, including
the reported indefinite first-three-round gaps (approximately 11, 5.8 and 2 percentage points),
and the finite/indefinite end-round difference. Reconstruct Figure 11's base/High T/Low R comparison
with session uncertainty. Use the supplied late flag only for these replication queries, and
investigate discrepancies rather than changing filters to get desired agreement. Retain all rows
and the distinction between observed choices and payment-valid choices. Reproduction of these
published summaries is not permission to use target outcomes for model selection.

## Primary prediction query and independent units

Predict a subject's current cooperation action in rounds 2..8 of supergames >=5, in indefinite
conditions. Include all first-eight-round choices, including those later found payment-invalid:
validity was not known when those choices were made. Do not use validity, eventual game length,
late labels, final risk-task responses, opponent ID, future/current actions or current beliefs as
prediction features. Previous reported belief is available at this time and may be used.
Post-elicitation belief fields currently have no missing values; any contradiction stops the
primary run for an additive mapping decision. No imputation of human outcomes.

All observations in a session stay together. Base sessions are 1,2,3,4,10,11,14,15. Holding out
the two lowest SHA256 values of `bellman-afy2024-base-validation-v1:<session>` selects **1,14**.
Initial training uses 2,3,4,10,11,15. Select regularization using only the two base validation
sessions, then refit the specified models on all eight base sessions before evaluating treatments
3 and 4 (sessions 17..24 and 25..32). The target files/rows are never inputs to fitting or tuning.
Finite treatment is replication context, not training for the primary indefinite query.

The experimental dependence unit for uncertainty is the session, including shared termination,
rematching and both players. Within-session rows and people are not independent experimental
replicates. Sessions 17..32 are additional treatment cohorts; absent an allocation schedule, do
not report exact assignment tests or assume cohort contrasts isolate incentive causality.

## Declared candidate classes

Use ten strategies from the paper's consideration set: AD, AC, GRIM, TFT, STFT, T8, T7, T6,
GRIM2, TF2T, with exact definitions from appendix Table 11. Reuse stratEst 1.1.8 automata and
constructor. Its DTFT is checked against STFT's stated start-D-then-TFT definition. Threshold
strategies follow Grim until their named round, then always defect. Do not select catalogue
members using target outcomes. METHOD.md specifies the state and value calculations.

Fit the source-population mixture and one global action-flip probability with stratEst's finite
mixture estimator, on source participants' post-elicitation rounds 1..8. A participant has one
latent strategy across the fitted games; automaton state resets between games. Use deterministic
responses, global flip noise, no strategy selection, seed 20260909, outer.runs=20, inner.runs=10,
outer.max=2000, inner.max=20, outer.tol=1e-10. Retain convergence/likelihood diagnostics; a numerical
maximum is not a proof of a global maximum. The package's standard errors are not used as session
uncertainty. Its actual wrapper does not expose the cluster interface earlier descriptions implied.

For prediction, smooth mixture shares by adding .001 to each and renormalizing; clip the fitted
flip rate to [.01,.49]. Retain fitted and operational values separately. These fixed regularizers
prevent zero likelihood after unfamiliar histories, not a proof about human errors. Reconstruct
posterior opponent-type weights from only that supergame's preceding actions, starting from this
source population prior. Subjective beliefs equalling this model is a testable supplied hypothesis,
not an inference from a participant's identity. No prior is updated with future or current actions.

At each history, evaluate all ten **subject continuation plans** against this opponent mixture.
The subject plans respond to subsequent observed play according to their automata; they are not
limited to always-C/always-D. Take the best expected normalized discounted value among plans
prescribing C now, and similarly among plans prescribing D. AC and AD ensure both groups exist.
Their difference is d_g(h). Optimization is only over this declared catalogue, not all behavioral
policies. Recomputing this score each round defines a response predictor, not a commitment to a
plan for the whole game or a sequential-equilibrium claim.

Two primary predictors share one fitted coefficient vector:

    fixed:   sigmoid(a + b*d_base(h) + c*previous_own + e*previous_report + f*(round-2)/6)
    updated: sigmoid(a + b*d_actual(h) + c*previous_own + e*previous_report + f*(round-2)/6)

Constrain b>=0. Both use identical history and report information; only payoff revaluation differs.
They are exactly identical in the base treatment. This is a test of a specific parameter/belief
transport restriction, not a contest between labels such as habit and rationality. Fitted b=0 or
coincident scores can make them overlap. Do not turn that overlap into a general identification
impossibility. Derive changed-payoff values rather than assuming a universal direction.

Use normalized stage utility (u(x)-u(39))/(u(51)-u(39)), with primary u(x)=x, and discount 7/8.
The value score comes from finite Markov systems, not a newly built equilibrium solver. A
state-value residual has an explicit discounted error bound; numerical values are not exact
optimality certificates over unrestricted strategies.

Fit the logistic coefficients by SciPy bounded convex minimization of session-weighted mean
negative log likelihood plus tau/2 times the squared non-intercept coefficients. Candidate tau
values are [0,.001,.01,.1]. Select the smallest validation Brier score, breaking ties within
1e-12 toward larger tau. Use analytic gradients, maxiter=10000, gtol=1e-8; retain projected-gradient
and convergence checks. No tuning by target fit. Both predictors inherit the same selected tau.

Competent baselines: source-session-weighted constant cooperation; previous own action (hard
persistence); and a logistic predictor with previous own action, previous opponent action,
previous report, previous mean opponent cooperation in this game, and (round-2)/6. Fit the latter
with the same loss/penalty grid and source validation, without the b>=0 restriction. This baseline
uses the same pre-action information budget; all features are directly reconstructed from prefixes.

## Scores, uncertainty and failure criteria

Primary outcome: equal-weight average across the two target treatments of their equal-weight
session mean **Brier(updated)-Brier(fixed)**. Negative favors revaluation. Report the two arms
separately, every session's difference, all baselines, base validation and target scores, and
calibration means. Secondary logarithmic scores clip probabilities at [1e-6,1-1e-6] for evaluation
only; retain unclipped predictions. Do not select the primary metric after observing it.

Report a 95% stratified session bootstrap percentile interval (9999 draws, seed 20260910),
resampling eight entire sessions within each target treatment. This is approximate sampling
inference conditional on source fitting, requiring independent/exchangeable sessions within
arm. Also report the stratified mean-difference standard error and Welch-style t interval, and
a distribution-free bounded-session Hoeffding interval as an assurance sensitivity. No method
here verifies the sampling assumptions or population transport. The primary direction is
supported only if its prespecified 95% bootstrap interval excludes zero; otherwise report
inconclusive comparison, not equivalence. Arm-specific intervals are descriptive secondary
results, not unadjusted confirmatory discoveries. Source validation has only two sessions.

Aggregate treatment means and session differences are distinct from individual prediction.
Compare model opponent-cooperation forecasts with actual opponent actions and separately with
post-action reported beliefs. Report overall and diagnostic second-round histories CC, CD, DC,
DD (own action first), with counts. These checks assess joint prediction/measurement assumptions;
current reported beliefs are never pre-action features or a causal mediator. Do not declare a
psychological mechanism identified from a convenient predictive win.

## Predeclared sensitivity and identification

1. Refit with the six-strategy catalogue AD,AC,GRIM,TFT,GRIM2,TF2T; use the same source-only
   tuning procedure. This probes catalogue dependence, not post-test model selection.
2. Keep the primary mixture but use stage utilities u(x)=-1/x and u(x)=x^2; refit the response
   coefficients with the same source-only tuning. These are exact rational stage-utility
   sensitivities, not estimates of utility over total earnings or validated risk preferences.
3. For the fixed final response coefficients/noise/catalogue, compute a per-history response
   range over all opponent-type priors. With positive likelihoods, all posterior weights are
   attainable. For each current action, values maximize finitely many affine functions of the
   posterior. Their difference need not be affine: do not assert corner sharpness. Use the
   finite linear-program formulation in METHOD.md for sharp per-history score extrema, and
   distinguish a computational outer bound if only a bound is retained. Aggregating different
   history-wise extrema is generally only an outer bound for one shared target prior.

Parameter-estimation uncertainty, prior transport, catalogue restriction, stage utility,
measurement and sampling uncertainty remain separate. Investigate a substantive discrepancy
or surprise with an explicitly labelled additive analysis; preserve the first predictions and
results. The 2019 study is outside this primary goal unless an essential new comparison warrants it.

## Assurance and handoff

Retain source hashes, acquisition instructions, specification commit, package versions, model
parameters, independent candidate predictions, session scores and diagnostics. Keep raw human
rows outside the repository while author/archive redistribution equivalence is unresolved.
Derived predictions must not bundle original actions, reports or raw feature matrices; receiving
uses a separately acquired hash-verified source file. An independent receiver disables fitting,
reconstructs timing, states, values and probabilities, and rejects altered sources, queries,
parameters, predictions, scores and unjustified reuse. Exact arithmetic claims concern their
specified numerical objects; fitting and sampling adequacy are not certified by arithmetic.

Review actual downstream contracts before choosing a handoff. Current inspected remote heads
remain Writ 4e9b7f49e240e4ca5d6a8df0c6b8ecb060d606e2 and Decision Lab
e5f77dfcf929708951f4673b3f394461ef09c752. Reuse them only if a stable statistical contract adds
value; otherwise retain a portable case, a concrete transfer gap and one meaningful changed-use
rejection. Preserve all FSD, v0.0.7 and prior receipt bytes. No new branches, repositories,
PR merges, release publication, author contact, recruitment or spending are authorized.
