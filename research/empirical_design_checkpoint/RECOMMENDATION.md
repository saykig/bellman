# Design checkpoint: improve the question, then test changed incentives

9 September 2026. Recommendation before replacement-model implementation. This is a bounded
comparison of the retained FSD case and three serious alternatives, not an effect-size search.
No new alternative was fitted; published results and initial raw rows were visible during design
inspection, so none of these papers can be labelled a prospectively unseen test.

**Recommendation:** retain and improve the FSD case, and make *Beliefs in Repeated Games* (Aoyagi,
Fréchette & Yuksel, 2024) the primary next proving ground for a sharply defined comparison of
history-following behavior and incentive-responsive strategic explanations. Its own changed-payoff
treatments provide the first test. Stage the 2019 monitoring experiment as a complementary,
conditional transport challenge only after that test is specified. Do not pool the experiments.
The 2022 rules/commitment experiment is the strongest alternative if the question becomes
verifiable disclosure itself; it is not automatically the better experiment merely because its
title matches Bellman's mathematical programme.

## What the current case changed

FSD3661 remains useful evidence, not a sunk cost to defend or a preliminary exercise to discard.
The original means reproduce. The fixed full-history predictor has held-out MSE .04379 versus
.04657 after erasing returns, and .05072 for persistence. The small difference is not established
as equivalent or population-positive under the prespecified conservative inference. Four held-out
sessions remain four clusters, regardless of the 240 scored participant-rounds.

The striking *descriptive* contrast is that simple personal persistence outperforms the training
mean by treatment (.14890 MSE) by a large amount on this split. This suggests asking whether the
useful history is mainly a participant's stable sending tendency/session context, or updating after
experienced returns. It does not yet distinguish those explanations. Nor does the poor treatment
baseline on this split refute random assignment or the existence of treatment effects.

**Retain-and-improve proposal:** compare stable-propensity and response-to-unexpected-return
models, conditioning on prior sending and allowing session dependence. Predeclare the return
innovation and calibration target; do not call this inspected split independent confirmation.
Repeated random rematching is helpful for separating experience from a continuing partner's
reputation, but returned money remains endogenous to the sender's prior choice and the partner's
response. Random rematching alone is not an instrument for returned money. An exploratory
within-person association can motivate a subsequent test, not certify causal belief updating.
Corroboration would require improvement beyond personal persistence on newly designated
session-held-out data or an additional experiment; lack of improvement or unstable sign would
weaken that interpretation. No new fit was run at this checkpoint.

This is a substantive improvement to the research question: distinguish *what a history predicts*
from *why it predicts it*, then challenge the explanation using assigned changes. An identification
failure, null result or measurement problem in FSD may still redirect the whole programme.

## Bounded design comparison

All listed alternative author data files, primary PDFs and protocol/appendix PDFs were actually
downloaded and parsed. `access.json` binds exact bytes. `structure.json` records metadata counts,
not fitted outcomes. These are public author analysis files with observations, not a claim to have
recovered untouched original laboratory logs. Publisher replication packages were located too.
Author-file redistribution licences have not yet been independently bound; no alternative data
have been copied into the repository. Acquiring that declaration and matching the author's table
to the archived source edition precede persistent ingestion. The 2024 archive download redirects
to login here, while the author TXT and PDFs are directly accessible. No author was contacted.

| Case | Design and recorded information | Independent structure and exact limitation | What the comparison can distinguish |
|---|---|---|---|
| **FSD3661 / Herne et al. 2022, retained** | Sanctions × written justification; six rounds; 12 points to send; returned amounts and prior own choices. Full original CSV and English instructions verified; CC BY 4.0. Partners rematched each round. | 216 people, 12 sessions, 3 per cell. Current split: 8 training, 4 test sessions. Observations are not independent rounds; no randomized feedback visibility. | Responses under assigned sanction/justification rules, conditional on design assumptions. Prior experience without a lasting dyad; does not identify partner reputation, private beliefs or the effect of hiding feedback. |
| **Aoyagi–Fréchette–Yuksel 2024, recommended primary** | Continuing partner within each supergame; finite 8-round versus indefinite δ=7/8; additional High-T and Low-R incentives. Cooperation, opponent action, elicited beliefs, history, elicitation status and payment-validity flags. | **556 participants, 32 sessions, 8 per treatment**, 55,724 participant-round records. Rematch only between supergames. Main cells 158+144 people; incentive cells 126+128. Beliefs begin after four supergames and are asked **after one's action but before feedback**. Block termination means some recorded choices do not count for payment. | Whether measured expectations plus a declared response model explain choices across changed future incentives, versus history-following without incentive response. Cannot interpret contemporaneous reported belief as an untouched pre-action predictor or causal mediator. |
| **Aoyagi–Bhaskar–Fréchette 2019, complementary stress test** | Perfect, noisy public and noisy private monitoring; same underlying stage strategic form; δ=.9; low/high signal noise. Own/opponent actions, generated signals, matched group, supergame and termination sequence recorded. Pairs persist within supergame. | **302 people, 18 sessions**: 12 low-noise sessions (4 per monitoring cell), 6 high-noise (2 per cell). Session numbers restart with noise regime: key is (epsilon, session). Six shared termination-sequence blocks, each spanning three monitoring sessions; do not ignore paired design or shared environmental draws. | Reaction to unreliable evidence and asymmetric knowledge; whether a short-memory strategy generalizes when monitoring changes. No elicited beliefs; private players do not see all researcher-recorded actions/signals. Cannot identify beliefs from actions without restrictions. |
| **Fréchette–Lizzeri–Perego 2022, strongest disclosure alternative** | Verifiable/unverifiable messages × commitment probability 20%, 80%, 100%, plus full-commitment payoff/message-space controls. Chosen information policy before the state, state-contingent revision, messages and contingent receiver guesses are recorded. 25 rematched rounds. | Author file: **32 sessions, 543 retained participant IDs**, 13,180 participant-round records, 4 sessions per 8 cells. Explicit software-bug note: .3% interactions affected; dropping involved subjects removes about 6% of collected data. Author PDF's core sample count differs from the current data and must be reconciled before estimation. | Direct test of commitment-sensitive information design versus commitment blindness, and whether verifiability changes that response. Rematching intentionally removes relationship reputation; good identification of this within-game mechanism, not continuing relational enforcement. |

Primary protocol/data links:

- FSD: [archive](https://services.fsd.tuni.fi/catalogue/FSD3661?lang=en&study_language=en).
- 2024: [paper](https://gfrechette.com/print/Aoyagi_2024a.pdf), [protocol appendix](https://gfrechette.com/print/Aoyagi_2024a_oa.pdf), [actual data/dictionary](https://gfrechette.com/data/Aoyagi_2024a_data.txt), [archival package](https://doi.org/10.3886/E205541V1).
- 2019: [paper](https://gfrechette.com/print/Aoyagi_2019a.pdf), [instructions](https://gfrechette.com/print/Aoyagi_2016a_inst.pdf), [actual data/dictionary](https://gfrechette.com/data/Aoyagi_2019a_data.txt), [archival package](https://doi.org/10.3886/E114360V1).
- 2022: [paper](https://gfrechette.com/print/Frechette_2021b.pdf), [protocol appendix](https://gfrechette.com/print/Frechette_2021b_oa.pdf), [actual data/dictionary and exclusion notice](https://gfrechette.com/data/Frechette_2022a_data.txt), [publisher materials](https://doi.org/10.3982/ECTA18585).

The 2019 counts initially looked like 12 sessions/274 people if epsilon was omitted. The dictionary
and cell counts revealed reused IDs; correcting the key yields 18/302. This is a metadata correction,
not evidence of new participants appearing through a model choice. The perfect-monitoring rows'
epsilon labels index the associated payoff/noise environment; they do not mean perfect observation
itself is erroneous. Shared termination schedules and `same` flags require faithful handling.

The 2022 paper explicitly motivates rematching to isolate commitment from relational reputation.
It should not be rejected just for rematching. It is deferred because the recommended question
currently needs belief measurements and a continuing interaction; sample/exclusion reconciliation
is an additional concrete burden. Its surprising behavioral departures remain potentially valuable.

## A decisive model disagreement, before fitting

Use 2024's base indefinite game to ask:

> Do models that explain both experienced cooperation and reported expectations correctly predict
> the response when unilateral temptation rises or mutual cooperation becomes less rewarding?

Candidate A is a restricted stochastic history-following model: persistent cooperation tendency
and a fixed response to recent own/opponent choices. Conditional on the same history, its fixed
parameters contain no payoff channel, so it predicts no change under a payoff revision.
Candidate B is a declared finite strategy-mixture/subjective best-response model in which expected
continuation payoffs and beliefs matter. Its payoff differences change when T rises from 63 to 73
or R falls from 51 to 45. It can therefore predict different choices at the same represented history.
Those are restrictions to test, not labels that identify "habit" and "rationality" in humans.
A reinforcement model that learns new payoff contingencies is a relevant stronger competitor;
include it only with a fixed update law and an explicit online information budget.

Before interpreting a direction, derive the actual predictions for the supplied strategy class:
multiple equilibria and belief adaptation can undo a simplistic "less cooperative incentives must
reduce cooperation" claim. If candidate classes overlap on every available query, report that
identification failure instead of fitting a decorative richer model. Belief measurements can
reject some otherwise observationally equivalent explanations, but neither monetary utility nor
the finite strategy catalogue follows from reported beliefs. Allow partial-identification or
sensitivity sets over unsupported utility and catalogue assumptions.

Design the first challenge **within 2024**, where recorded outcomes and implementation are most
comparable. Predeclare source/treatment/session splits, predictions, simple baselines, scoring,
missingness and cluster uncertainty before fitting. Hold the High-T and Low-R treatment outcomes
out of fitting; use separately declared session holdout for validation within source treatments.
Both published results and data previews have already been inspected, so call this a retrospective
held-out challenge, never a prospective discovery. Do not infer more independent samples from
thousands of rounds. Distinguish action-prediction evaluation from joint action/reported-belief
fit, and respect the action-before-belief timing. The first four supergames' unelicited beliefs
are structurally missing, not zeros; payment-invalid blocks are not arbitrary dropout.

A useful decision consequence would be knowing whether a predictor calibrated under one incentive
schedule can support comparing a specified new schedule, or whether it must return a wide set of
possible outcomes. No positive policy recommendation follows merely from a better probability score.

## Conditional pair, rather than pooled data

If the primary models earn testable predictions, the 2019 experiment supplies a distinct challenge:
replace reliable action history with noisy public/private evidence. Score only information the
player actually received; researcher-visible opponent actions are unavailable inputs under private
monitoring. Within that study, exploit controlled monitoring variation and the matched termination
blocks. Two high-noise sessions per cell will still yield fragile uncertainty.

Cross-study transfer additionally needs payoff normalization, discount-factor change (.875 to .9),
UCSB versus NYU population differences, timing/block termination, random payoff implementation,
and the presence versus absence of belief elicitation. Parameter equality is a substantive transport
premise. Use explicit sensitivity sets or reject transport; do not learn the target's parameters
from its outcomes and then call it a held-out prediction. A comparison of qualitative restrictions
may be supportable even where common numerical parameters are not. If these bridges fail, retain
2019 as a separate study and keep the first challenge entirely inside 2024.

The two experiments are complementary because one measures expectations while changing incentives
and the other changes the evidence on which expectations can be based. They are not an automatic
joint proof of learning, reputation or deterrence. Neither supplies verifiable-disclosure choices;
the 2022 experiment is the distinct route for that question, not a third dataset to ingest by default.

## Established methods and staged work

1. **Bellman:** specify the competing models, information access, estimands and nonidentification
   boundaries; reproduce an original comparison; freeze a retrospective evaluation plan. First
   finish the initial FSD evidence/report and additive acceptance reconciliation. Retain all
   corrections and inconclusive findings. No strategy catalogue is treated as exhaustive by fiat.
2. **Computation / Decision Lab:** inspect archived estimation scripts and reuse them where their
   assumptions fit. `stratEst` 1.1.8 is a serious existing option: its actual manual documents EM
   and Newton–Raphson maximum-likelihood estimation of supplied strategy shares/choice probabilities,
   covariates, sample-specific parameters and nested cluster IDs. It does not identify arbitrary
   strategies, beliefs, causal effects, or Bellman shared consistency. It is R/Rcpp software;
   use as a bounded reference tool if it saves implementing SFEM, not as a repository migration.
   No model or adapter has been implemented for the new candidates at this checkpoint.
   [Manual inspected](https://cran.r-project.org/web/packages/stratEst/refman/stratEst.html).
3. **Writ:** only after a stable empirical contract exists, preserve source-to-model mapping,
   declared applicability, predictive failures and successor claims. Current exact decision/transport
   receivers cannot certify these statistical explanations. Keep a portable case if a native handoff
   adds no demonstrated value; no Writ changes are made now.

**Most informative missing observation:** for the cooperation/monitoring bridge, an incentivized
expectation elicited *before the next choice* after a randomly varied public/private signal, with
an elicitation-control arm and continuing partner. This separates changes in reported expectations
from changes in actions at comparable beliefs, subject to the elicitation assumptions. It would
not prove causal mediation or reveal utilities automatically. Existing conditions cannot be
retroactively changed; this is a proposed future measurement, not authorized recruitment.

For the narrower FSD feedback-erasure question, the relevant next observation remains a randomized
feedback-visibility contrast before the next transfer. That is a different question and must not
be silently replaced by the belief-measurement proposal.

**Checkpoint disposition:** retain-and-improve FSD; recommend 2024 as primary changed-incentive
proving ground, 2019 as a conditional second stage; keep the 2022 disclosure route as a serious
alternative. Do not start substantial replacement modeling or integration until this recommendation
has been returned. The existing goal stays active; this checkpoint is not its completion claim.
