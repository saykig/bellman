# First findings and unresolved assurance

9 September 2026. Preserves the first result rather than selecting a successful sensitivity.
Specification 4abea07; first evidence f541369. No post-target fitting is introduced here.

| Declared utility/catalogue | Updated minus fixed Brier | Conditional session bootstrap 95% interval |
|---|---:|---:|
| Linear, ten (primary) | -0.000406828 | [-0.001865778, 0.001228148] |
| Linear, six | -0.000174689 | [-0.001593754, 0.001374684] |
| Reciprocal, ten | -0.000975576 | [-0.001544955, -0.000410719] |
| Square, ten | 0.000855507 | [-0.001541078, 0.003637098] |

These are differences between two defined predictors that agree under source payments.
The primary gate does not establish superiority or equivalence. The secondary reciprocal
result cannot replace the prespecified primary result or establish utility curvature.
Intervals condition on fitted source parameters and assume independent/exchangeable sessions;
only eight sessions occur per target arm. The bounded-session Hoeffding interval is much wider.

In High T, primary fixed/updated/Markov Brier scores are .104915/.105388/.093600;
in Low R they are .153144/.151857/.141670. The simpler baseline's better scores materially
limit claims that the additional catalogue-value machinery improves this prediction task.
Investigating utility-dependent value scores and prior transport remains necessary.

The own-action/report and actual-opponent timing distinctions survive replication. After
round-one mutual cooperation, the source-mixture opponent forecast is .924558, actual next
opponent cooperation is .966292 and the post-action report mean is .834625 (534 target rows).
Aggregate agreement across histories would conceal this discrepancy. No report-noise model
was fitted that licenses interpreting all three as the same latent probability.

The source-only R mixture likelihoods were independently reconstructed in Python before
scoring (absolute tolerance 1e-7). A separate standard-library receiver additionally checks
all target predictions and scores and exact rational value residuals, with no fitting-library
imports. Its arithmetic guarantee does not include optimal mixture estimation or confidence
coverage. Thirteen rejection controls target false values, altered automata/noise, an
unsupported utility label, negative incentive coefficient, missing/duplicate/wrong-time
queries, altered predictions, unregistered report fields, false scores and source identity.

The first R call failed before fitting because stratEst coerced colon-delimited participant
IDs to numeric. A bijective numeric code fixed that API requirement. No observation or split
changed. R-generated diagnostic/runtime text has trailing whitespace retained as original
output bytes; the initial diff-check reported it. It is not silently cleaned after freezing.

Outstanding: complete prior-range evidence, investigate the substantive sensitivity, retain
independent replication/uncertainty checks and end-to-end acquisition/refit instructions,
review and source-bound conclusions, inspect downstream contract reuse, update living guidance,
and run additive combined acceptance. This checkpoint is not the completion gate.
