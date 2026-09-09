# Completion audit: first empirical proving ground

9 September 2026. Audit of main 4685278 and its frozen sources. This closes the bounded
empirical case and design-selection brief, not Bellman's continuing research programme.
It is an internal source and mathematical review, not external peer review or formal verification.

The original goal and revised brief require an actual source-backed empirical result, with
replication, competent baselines, identification, appropriate uncertainty, a meaningful information
comparison, a justified handoff disposition, and a stronger-design comparison before substantial
replacement implementation. An informative null or identification obstruction is permitted.
A shortlist alone would not suffice. Here the retained FSD analysis supplies the empirical result;
the design comparison is additional work, not its substitute. No positive finding is required.

## Requirement-by-requirement disposition

| Requirement | Inspected authoritative evidence | Disposition |
|---|---|---|
| Existing repository instructions and baselines | AGENTS.md, Bellman research-component skill, north star/roadmap/architecture; downstream instructions and remote-main contracts recorded in PLAN.md and TRANSFER.md | Met for this bounded case. Downstream remote heads rechecked unchanged on 9 September. |
| Original data, protocol, edition and reuse | provenance.json names FSD3661 v1.0, original CSV, English instructions, labels, DDI and README with byte hashes; all five downloaded files rehashed successfully at final audit | Met. README and DDI expressly identify data CC BY 4.0; metadata's separate CC0 notice is not substituted for the data licence. Citation and publication-notification limitations remain recorded. |
| Reproducible source mapping | reproduce_projection.py rerun against original archive CSV at audit; exact 15-column output matched observations.csv | Met: 1,296 rows, 216 participants, 12 sessions. Projection is labelled, not called full raw data. |
| Reproduce original result | analyze.py and receiver.py independently reconstruct eight Table 2 means; results.json and checkpoint-validation.json retain values and checks | Met to the paper's displayed rounding; no claim to reproduce every original inference. |
| Prespecified representation comparison and competent baselines | PLAN.md committed/pushed at d9c0075 before fitting; full/reduced Ridge, persistence and training-treatment mean; results.json retains every test prediction | Met as a retrospective held-out comparison. It is not prospective preregistration or an independent new experiment. |
| Timing, leakage, dependence and uncertainty | receiver reconstructs previous-history features and session split; 240 test rows in four whole sessions; IDENTIFICATION.md derives bounded-session inference | Met within supplied sampling assumptions. The primary 90% interval is [-1,1], so equivalence is not established. A favorable bootstrap sensitivity does not replace it. |
| Observed/assumed/identified/unresolved distinctions | IDENTIFICATION.md and REVIEW_20260909.md | Met. Assignment implementation and population exchangeability remain assumptions; neither is claimed empirically verified. |
| A decisive query and failure boundary | Conditional-mean loss identity, exact observational extensions for hidden feedback, and check_handoff.py | Met. Prediction does not identify the feedback intervention. The sharp support-only set concerns a stated nonparametric class, not psychological plausibility. |
| Exact receiving and machine evidence | checks.py disables fitting imports, checks retained arithmetic/residuals and 14 rejection controls; portable revision has three controls | Met for its stated subset. Bootstrap/OLS uncertainty, physical randomization and human beliefs are not independently certified. |
| Borrowing and justified tools | Pinned pandas, sklearn Ridge/SVD, SciPy and statsmodels; primary scoring, concentration and identification sources in IDENTIFICATION.md | Met. No custom estimator, QRE solver, language migration or unsupported Lean claim. |
| Downstream implementation or concrete gap | TRANSFER.md, portable_handoff.json, check_handoff.py; remote Writ 4e9b7f4 and Decision Lab e5f77df unchanged | Met through the expressly allowed portable case and transfer-gap route. Their current exact contracts do not receive this statistical estimand. No native import is claimed. |
| Improvement, serendipity and stronger alternatives | RECOMMENDATION.md, access.json and structure.json in empirical_design_checkpoint | Met for design selection. Preserves the current finding, corrects metadata keys, distinguishes persistence from response, and compares three accessible alternatives. Alternative redistribution/edition reconciliation and fitting remain future work, not completed ingestion. |
| Findings, limitations and next observation | README.md, IDENTIFICATION.md, TRANSFER.md and design recommendation | Met. For this case, the single next causal observation is a randomized feedback-visibility contrast before a subsequent transfer. No intervention was conducted. |
| Frozen evidence, required acceptance and publication constraints | verification/empirical_acceptance/results.json at 4685278: 227 frozen files; local full reproduction and hosted combined/strategic runs passed | Met at that checkpoint. The completion receipt separately binds this audit and updated guidance without changing the first receipt. No branch, downstream edit, PR merge or release publication occurred during this empirical goal. |

Remote Bellman v0.0.7 remains 2cd6fd7432efccaacc734fd235549a564ddbff48. Writ main remains
4e9b7f49e240e4ca5d6a8df0c6b8ecb060d606e2 and Decision Lab main remains
e5f77dfcf929708951f4673b3f394461ef09c752. These checks establish current contract identity,
not downstream integration acceptance: no downstream code changed and no such pass is claimed.

## What the stronger design must distinguish

Reading the recommended 2024 paper more closely changes the next comparison's specification.
Its §5 action-to-strategy-belief example and §5.2 estimation require a strategy catalogue,
diagnostic histories and within-type shared-belief assumptions; Tables 2–3 flag collinear
estimates. Round beliefs are not unrestricted identification of beliefs over reactions to a
deviation. [Primary author edition](https://gfrechette.com/print/Aoyagi_2024a.pdf), already
byte-bound in the design checkpoint's access.json. This finding is borrowed, not claimed novel.

Here is an analytical specialization that makes the next test precise. It is **not a fit to
participants** or an impossibility claim about the full 2024 dataset. Consider perfect monitoring,
no implementation/reporting error, risk-neutral monetary payoffs, discount δ, and a fixed opponent
that is always-cooperate with prior probability 1-w and grim-trigger with probability w. Grim
starts C and defects forever after the subject defects. Compare exactly two subject policies:
always C and always D. No claim of optimality over every history-dependent policy is made.

Along any all-(C,C) history, both opponent types choose C and every current-action belief is 1.
The histories and reports therefore cannot distinguish w. Yet normalized discounted value gives

    V(C) = R,
    V(D) = (1-w) T + w ((1-δ) T + δ P),
    V(C)-V(D) = R-T + δ w (T-P).

The expressions follow by summing each constant continuation's geometric series. With T>P,
the sharp range over w in [0,1] is [R-T, R-T+δ(T-P)]; the endpoints are attained by the two
pure opponent types. With δ=7/8 and P=39, using the paper's payoff schedules:

| Schedule (T,R) | Sharp range for this two-policy value difference | Threshold w for C to weakly beat D | Difference at w=7/10 |
|---|---|---|---|
| Base (63,51) | [-12,9] | 4/7 | 27/10 |
| High T (73,51) | [-22,31/4] | 88/119 | -47/40 |
| Low R (63,45) | [-18,3] | 6/7 | -33/10 |

These fractions were checked with Python Fraction arithmetic; the derivation, not those finite
calculations, supplies the continuum guarantee. Both w=7/10 and w=1 prefer C in the base
comparison and generate identical cooperative histories/current beliefs there. Holding the
prior fixed across the payoff change, the former switches its two-policy ranking in both new
schedules while the latter does not. Thus unchanged cooperation can be compatible with an
incentive-based account; calling an invariant predictor "habit" would not identify that mechanism.
The fixed-prior transport premise itself needs scrutiny in different treatment populations.

Within this restricted idealization, a belief about cooperation *after one's first D while the
opponent still chose C* equals 1-w and separates the types. The source paper uses richer
histories and error specifications; no observed report is asserted to equal this ideal quantity.
The proposed next study should expose prediction sets over compatible strategy beliefs and test
where they disagree, rather than select one collinear belief estimate as mathematical authority.
This materially sharpens the candidate comparison without building an unearned estimation engine.

## Closed result and remaining research

The earned empirical result is a modest sample prediction improvement (RMSE 2.590 to 2.511 points)
with inconclusive primary uncertainty, plus a rigorous limitation on its causal reuse. It advances
empirical history assessment and the separation of source, model, result and applicability.
It does not validate strategic disclosure theory, general mechanism composition, human utilities,
participation, ambiguity preferences or shared off-path consistency.

The revised research question is better specified; no new fitted revision is claimed to improve
prediction. The 2024 changed-incentive study remains the recommended next investigation, with
2019 monitoring conditional on an explicit transport bridge and 2022 the disclosure alternative.
Its uncompleted licensing/edition reconciliation and estimation are not silently counted as an
empirical result. They are not needed to replace the bounded, already completed FSD deliverable.
Avoid indefinite expansion of this goal: retain its uncertain result and open a separately bounded
research question when the user elects to pursue that next stage.
