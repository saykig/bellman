# AFY 2024: identification and empirical challenge audit

9 September 2026. Source specification 4abea07; first evidence f541369; independent receiving
f9cc715; prior/utility evidence f3d0397; full reproduction and transfer eec4f51. This report
reviews the bounded result, not the entire empirical adequacy of the original paper.

## Actual observation and earned comparison

Aoyagi, Fréchette and Yuksel's [author paper](https://gfrechette.com/print/Aoyagi_2024a.pdf)
and [appendix](https://gfrechette.com/print/Aoyagi_2024a_oa.pdf) specify repeated PD choices,
after-action/before-feedback belief reports, δ=7/8, and changed temptation or cooperation
reward payments. The hash-verified author table has 55,724 rows, 556 people and 32 sessions.
The archive's displayed CC BY 4.0 licence is recorded, but authenticated archive bytes
were not acquired or equated with the author file. Raw rows remain external to this repository.

Independent reconstruction reproduces the stated first-three-round base gaps and the
finite-game end decline. The intended descriptive treatment comparison is Figure 9;
the frozen plan's Figure 11 reference is corrected in PRIOR_AND_UTILITY_REVIEW_20260909.md.
Equal-session late cooperation averages .7555 base, .7015 High T and .4352 Low R. These
are our reproduced observations. Our session intervals are not the authors' regression
p-values, and unverified cohort assignment does not make the contrasts causal effects.

The evaluation plan was pushed before human-data fitting, but published outcomes and raw
structural information had already been seen. It is retrospective, not a prospective blind
confirmation. Source sessions 1 and 14 selected penalties; six other base sessions trained
initial estimates; all eight base sessions supplied final fitting. None of sessions 17..32
entered fitting or selection. Current reports are not prediction features: only a prior-round
report and observed prefixes are used. Payment-invalid early-block choices remain because
validity was not known at decision time. Future game lengths and late labels are excluded
from prediction features. Pair identities are not manufactured from matching margins.

The fixed and updated predictors are algebraically identical under source payments. Their
only difference at test is whether catalogue continuation values use source or actual stage
payments. This is a conditional parameter-transport comparison. The ten-plan class admits
history-responsive own continuation plans; it does not optimize over all behavioral policies
or prove sequential rationality. The six-plan and two utility sensitivities were prespecified.
Existing stratEst supplies mixture estimation; SciPy supplies response optimization and LPs.
The source wrapper's absent cluster interface is corrected additively, and package standard
errors are not used as session uncertainty. No new solver or language migration was needed.

## Results and what they do not identify

The primary equal-treatment/equal-session Brier difference updated-minus-fixed is
-0.000406828. Its prespecified 95% session bootstrap interval is
[-0.001865778, 0.001228148]. This does not establish superiority or equivalence. There
are only eight target sessions per arm and two source validation sessions. The interval
conditions on the source fit; it does not cover parameter estimation plus all forms of
transport uncertainty. The conservative bounded-session interval is much wider.

Reciprocal stage utility yields a secondary interval below zero; square utility reverses
the point direction. These are supplied utility transformations, not estimates of human
utility over total earnings. The retained Brier decomposition shows that reciprocal utility
induces smaller adjustments, avoiding much of High T's quadratic adjustment cost. No
post-test refit or model selection produced this explanation. The simpler Markov/report
baseline has lower Brier scores than both candidates in both target arms. This materially
limits the practical predictive case for the added catalogue-value machinery in this study.

After mutual cooperation, predicted opponent cooperation, actual opponent cooperation and
reported belief have different means (.9246, .9663 and .8346). The population strategy
mixture is therefore not a direct measurement of subjective belief. No fitted measurement
model licenses interpreting report noise, choice noise, payoff curvature and a subjective
prior interchangeably. Current reports also cannot establish an untouched pre-action belief
or a causal mediation path from incentives through beliefs to actions.

The finite observations do not logically exclude any finite-logit predictor merely because
it has nonzero residual error: each binary action has positive conditional probability when
its logit is finite. A predictive comparison requires the declared statistical criterion and
sampling premises. This analysis did not construct an empirically identified set of all
subjective priors, utilities or behavioral types. “Not rejected” is not evidence of true
psychology, and a secondary predictive advantage does not select a unique mechanism.

## Mathematical and computational identification boundary

METHOD.md derives the finite Markov reward equation and its residual bound, and finite LP
formulas for extrema of the difference between best C-plan and best D-plan values. The
posterior simplex is attainable under arbitrary supplied priors because all history
likelihoods are positive. That is an analytical statement about the stipulated model family.

All 20 observed catalogue-state pairs and three payment tables have independently checked
rational primal/dual enclosures, 600 certificates in total. These enclose sharp extrema
of the retained value vectors; exact Markov residual allowances cover their value error.
They are not vertex-only guesses or assertions that floating solver statuses prove optima.

Averaging query-specific probability extrema gives only an outer range for a shared prior.
A decisive construction in METHOD.md shows why separately attainable endpoints need not
coexist. The resulting mean response outer range [.33755,.62135] is not an empirical
confidence interval or an exact shared-prior identified set. No missing joint optimization
is silently marked complete.

Actual shared pure-prior sensitivity witnesses give opposite target score directions:
AC +.0296553 and TFT -.0131842. Their score arithmetic is independently reconstructed
numerically, with separately exact value-error assurance. This falsifies the proposed
uniform directional comparison over that declared prior family at the implemented query;
it is not an exact-symbolic theorem about all human models or evidence that either prior
is empirically plausible. A smaller justified prior family could give a different result.

## Assurance and unsupported claims

Analytical proofs: base-predictor identity, existence of changed-payment disagreement,
finite reward uniqueness/residual bound, prior attainability, finite LP reduction, and
history-wise versus common-prior distinction. These specialize standard finite mathematics.
No Lean formalization or formal-verification claim is made.

Executable checks: source and query identity; canonical strategy definitions; exact rational
reward residuals and prior-bound certificates; all 8,414 target predictions in each declared
comparison; session scores; uncertainty arithmetic and replication projections; rejection
controls; normal/optimized receiving; and complete source-to-fit-to-score reproduction.
Fresh mixture fitting on the original host reproduces all retained predictions exactly.
Other supported hosts use an explicit numerical tolerance. Fitting convergence is diagnostic,
not proof of a global mixture optimum. Bootstrap arithmetic is not proof of coverage.

Supplied empirical assumptions: catalogue adequacy, response noise, population-to-subjective
prior mapping, utility transformation, response parameter stability, session sampling and
measurement interpretation. They are distinct dependencies, not consequences of exact checks.
Unsupported: global psychological identification, unrestricted best responses, off-path
belief consistency from human data, ambiguity preferences, participation, causal treatment
assignment, mechanism welfare, institutional transport and authority to act.

The result materially advances empirical model criticism and the inspectability of
history-conditioned prediction. It does not establish a new strategic-disclosure theorem,
history-preservation theorem or mechanism-composition rule. Earlier strategic/causal/FSD
mathematics and evidence remain intact. TRANSFER.md documents the concrete downstream gap
and a portable changed-use rejection; Writ and Decision Lab were not modified.

## Single most informative next observation

At an otherwise cooperative history, obtain an incentive-compatible forecast of the
opponent's next cooperation **conditional on the subject deviating to D**, before the
subject chooses, with the payoff condition recorded. Such a counterfactual response forecast
would directly distinguish forgiving AC-like beliefs from retaliatory TFT/Grim-like beliefs
that can agree on current cooperation. It would constrain the prior dimension that reverses
this study's comparison more directly than another unconditional current-action report.
Its elicitation, information and causal interpretation would require a separate approved
study design; no participant contact, recruitment or data collection is authorized here.
The 2019 dataset is not automatically opened as a successor task.
