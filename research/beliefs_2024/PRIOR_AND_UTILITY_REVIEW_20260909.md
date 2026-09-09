# Prior transport and utility: additive review

9 September 2026. An analysis specified in PLAN.md, plus an explicitly labelled investigation
of the first utility-sensitive result. First evidence at f541369 remains unchanged.

## What the range calculation proves

For each of the 20 distinct own/opponent catalogue-state pairs reached by the 8,414 target
queries, and each of the three payment tables, all catalogue continuation alternatives are
covered. HiGHS proposes simplex weights; a separate standard-library receiver checks 600
rational primal/dual certificates against the retained rational-decimal value entries.
The largest extremum-enclosure width is approximately 5.57e-16. These are enclosures of
sharp extrema, not claims that floating LP vertices equal exact optima. The independently
checked Markov residual bound enlarges the score endpoints by twice the value error.

Here is the certificate argument, supplementing METHOD.md. For a fixed C-plan j write
D_lk=v_jk-v_lk. Any posterior w gives a lower bound min_l sum_k w_k D_lk on
max_w min_l sum_k w_k D_lk. Any simplex weights λ on D-plans give an upper bound
max_k sum_l λ_l D_lk, since a minimum is at most any convex average. Taking maxima
over j bounds the maximum score. For a fixed D-plan l, reversing maximum/minimum gives
a lower bound min_k sum_j λ_j(v_jk-v_lk) and an upper bound max_j sum_k w_k(v_jk-v_lk).
Taking minima over l bounds the minimum score. Every inequality is checked with Fraction;
no solver success label is received as a certificate. Posterior attainability follows from
positive likelihoods and p_k proportional to w_k/L_k(h), as proved in METHOD.md.

The target mean response has a history-wise outer range [0.33755, 0.62135] with the final
linear response coefficients. Its endpoints generally use different priors in different
histories. They are not proved attainable under one shared prior, and are not a confidence
interval or an identified set for human preferences. The query-wise feasible posteriors
are the full simplex by a supplied modelling choice, not an empirically estimated family.

## A decisive boundary for shared-prior robustness

The same pure prior can be used at every target history. With positive flip noise its
posterior remains pure. Holding coefficients, catalogue and noise fixed, the shared AC prior
gives updated-minus-fixed Brier +0.0296553, whereas shared TFT gives -0.0131842. All ten pure
priors were examined as declared feasible sensitivity witnesses. These two computed cases
falsify a uniform directional comparison over the entire allowed prior simplex. They do
not show that either pure prior fits observed reports or actions, that every intermediate
contrast is identified, or that no smaller empirically justified prior set would work.
The independently reconstructed score arithmetic is stronger than failure of a numerical
search: it supplies two actual members of the specified family with opposite signs.

Seven producer-disabled rejection controls cover false dual bounds, negative posterior
weights, omitted continuation alternatives, uncovered history states, erased residual
allowances, false aggregate bounds and false shared-prior contrasts. Normal and optimized
receiving agree. Sampling intervals attached to exploratory pure-prior contrasts are not
made into simultaneous confirmatory claims.

## Why the utility sensitivity changes the comparison

This section investigates first results without changing any fit or selecting a new model.
For a single prediction, writing d=p_updated-p_fixed gives the exact Brier identity

    (p_updated-y)^2 - (p_fixed-y)^2 = 2(p_fixed-y)d + d^2.

The second term always penalizes the size of adjustment. In High T, linear utility gives
alignment -0.0006475 and adjustment cost +0.0011204, hence a net loss +0.0004730.
Reciprocal utility gives -0.0001121 and +0.0000504, hence a small gain -0.0000616.
Square utility gives -0.0015614 and +0.0036371, hence loss +0.0020756. Values are equally
weighted over sessions. This decomposition explains the observed predictive difference;
it does not estimate the cause of human behavior.

Both normalized catalogue score changes and the source-fitted response slope differ.
Mean High-T probability adjustments are -2.45, -0.51 and -4.10 percentage points for
linear, reciprocal and square utilities. The corresponding slopes are 1.74, 0.90 and
2.28. Reciprocal utility's smaller adjustment avoids much of the penalty in High T;
all three adjustments improve the point comparison in Low R. The simpler Markov/report
baseline still has lower Brier scores than these candidate predictors in both arms.
Thus the apparent reciprocal-utility success is not a successful general mechanism test.

## Source-reference correction and replication scope

The frozen PLAN.md and SOURCES.md misnumber the descriptive changed-treatment plot as
Figure 11. In the hash-bound 16 October 2024 author paper it is **Figure 9** (page 31).
Figure 11 (page 33) is the type-specific best-response calculation using the authors'
estimated supergame beliefs. This work reproduces the intended descriptive comparison,
not that separate type-assignment/belief-estimation pipeline. No outcome filter changed.

The independently reconstructed round means match the paper's stated 11, 5.8 and 2.0
percentage-point gaps. Pooling all late first-eight rounds gives an indefinite gap of
about 2.17 points; retain that exact-data result rather than reading the paper's prose
“two percentage points” as an exact 2.000 threshold. Finite pooling is below one point.
Our equal-session mean late cooperation is .7555 base, .7015 High T and .4352 Low R.
The new session intervals and target-minus-base comparisons are explicitly our inference;
the archive scripts were not downloaded, so the authors' regression p-values are not
claimed reproduced. Cohort differences remain descriptive without an allocation audit.

## Remaining work

This resolves the declared prior calculation and investigates the substantive first-result
sensitivity. The overall goal still needs end-to-end reproduction, final source-bound
identification/transfer audit, current programme guidance and additive combined acceptance.
No sequential-equilibrium, participation, mechanism-composition or human-utility theorem
follows from these empirical scores.
