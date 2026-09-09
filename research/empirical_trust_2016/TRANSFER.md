# Concrete portable handoff and disposition

9 September 2026. No downstream source changes, branch creation, PR merge or release.

## Inspected baselines and real capabilities

- Bellman main/release v0.0.7: `2cd6fd7432efccaacc734fd235549a564ddbff48`.
- Decision Lab remote main: `e5f77dfcf929708951f4673b3f394461ef09c752`.
  `BUILD_2_SPEC.md` and `src/writ_decision_lab` accept exact finite rational probability
  constraints and loss queries; `CERTIFICATE_TRANSPORT_SPEC.md` permits a separately bound
  finite observable-history identity-skeleton transfer. It explicitly excludes statistical
  learning. Its existing small SciPy search is not a statistical model-validation interface.
- Writ remote main: `4e9b7f49e240e4ca5d6a8df0c6b8ecb060d606e2`.
  The current roadmap accepts ADR 0026/0028 and retains PR #51 certificate transport.
  `packages/decision-case/README.md`, `src/types.ts` and `src/engine.ts` restrict native
  decision cases to `finite-linear-uncertainty.v1`, compatibility and static decision uses.
  Transport is a separate bounded adapter, not permission for arbitrary empirical results.
  `packages/shared-analysis` provides revision/replay for its supported contract. None of
  these checks archived-data design, cluster loss inference, or fitted behavioral meaning.

Current remote files were read with `git show origin/main:...`; stale local branch documentation
was not treated as current authority. No new checkout or downstream test claim is made. Existing
Writ/Decision Lab instructions were read. Their local/cloud workflow is not needed for this
portable disposition; source trees remain unchanged.

## Specific gap, not a general platform proposal

Converting decimal coefficients into rational strings would preserve bytes but not establish
population loss bounds. The FSD outcomes are dependent, bounded amounts, not IID Bernoulli
observations. Feeding them to Bellman's Bernoulli receiver would invent a sampling premise.
An exact finite loss-table wrapper around point estimates would similarly hide sampling and
identification uncertainty. The protocol does not even define a downstream decision-loss table
or authority to hide feedback. There is no justified native decision case to import.

This case therefore travels as the present directory: projected observations, original hashes and
reprojection procedure, fixed plan, retained predictions, mathematical audit, receiving code,
source-bound validation and the intended-use revision below. It is not a new interchange schema
or Writ native record. The separate `portable_handoff.json` binds concrete old evidence and a new
intended claim. `check_handoff.py` demonstrates that the old result remains arithmetically valid
and the new causal use fails; changing an evidence hash or reusing the old query also fails.
A native Writ implementation is deferred, not silently simulated or labelled complete.

## Meaningful revision

Original intended use: compare fitted conditional-mean predictors on unseen sessions under the
original visible-feedback protocol. Result: a retained point-score difference and no established
equivalence at the prespecified margin.

Successor intended use: advise hiding monetary feedback from participants because analyst-side
erasure had a small observed prediction gap. This changes the subject from representation to
intervention and cannot inherit the old result. `IDENTIFICATION.md` proves sharp support-only
bounds [-mu,1-mu] on the normalized mean effect in the explicit nonparametric class. The new
claim is `not_identified_without_additional_assumptions`, not false, harmless, or authorized.
No old result bytes are changed; receipt preserves the parent-result and intended-use identity.

## Comparison against a competent simpler workflow

A pinned notebook or script with grouped holdout, data hashes, saved predictions and an immutable
analysis plan already performs the empirical work. This case uses that baseline (pandas + Ridge
+ SciPy + statsmodels), adding a small separate arithmetic receiver and explicit intended-use
binding. Its demonstrated benefit is recipient detection of stale plans, altered predictions,
leakage and causal overclaim without rerunning a fit. It does not establish superior statistics,
and native Writ integration adds no demonstrated empirical value yet. Fourteen receiving
rejection controls and the revision replay are evidence of that limited benefit, not proof that
an unrestricted author could never supply a different model or misdescribe the experiment.

Smallest prerequisite for later transfer: a concrete recipient needs to compare empirical claims
with a declared sampling design, data-to-model mapping, query-specific statistical uncertainty,
and separately assessed intervention applicability. Agree that contract and its receiver first;
then reuse Writ provenance/revision rather than inventing an empirical solver registry. No Lean,
Rust, new service or language migration is justified by this single case.
