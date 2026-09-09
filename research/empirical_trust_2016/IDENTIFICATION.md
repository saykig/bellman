# What this experiment identifies — and what erasing a history does not

9 September 2026. Ordinary analytical audit and specialized established results; not formal
verification or external peer review. Companion to the frozen retrospective PLAN and results.

## Subject, premises, query and identity

Subject: the FSD3661 human trust experiment and the explicit projected monetary histories
in `provenance.json`. Observation is one participant-round; dependence extends across the entire
session because participants are rematched. The measured response is money sent, not a direct
measurement of trust, utility, belief, credibility or institutional legitimacy.

Premises: labels and protocol correctly describe the archived observations; participant and
session identities are correct; random allocation reported by the authors occurred; any sampling
inference assumes independent, suitably exchangeable sessions. Subjects volunteered from a local
laboratory register, mostly university students. There is no probability sample of society.
The 12 sessions (three per treatment) limit inference despite 1,296 participant-round rows.

Query: at sender round 2..6, predict sent points /12 from previous sent and returned amounts;
compare erasing the return sequence. Treatment and round remain represented. Predictions are
models of conditional means for a specified input class, not a fitted game-theoretic equilibrium.
The information discarded from the *analyst's representation* differs from withholding feedback
from a human. The latter changes an experiment and is unsupported by the former comparison.

Guarantee: the receiver reconstructs the fixed mapping, timing, split, predictions and squared
loss arithmetic and checks small ridge normal-equation residuals. It does not establish the
sampling premises. The analytical bounds below state exactly what follows *if* premises hold.
Reuse requires identical data, plan, model feature definition and intended prediction query;
changed intended use is rejected rather than silently reusing an empirical score.

## Observations and interventions

The two factors were availability of costly punishment and mandatory written justification.
The original paper reports random treatment allocation, but the archived data do not supply
an assignment schedule or randomization seed. Each session has a single treatment. Roles were
randomly assigned; the sender/recipient role persists, while numbered sender slots may change.
Thus ordinary sender-round independence is false as a design assumption. The instructions say
new groups each round; the article more cautiously says partners most likely changed. Neither
claim justifies independent rows or identification of persistent partner reputations.

Conditional on random assignment and no cross-session interference, marginal contrasts can
estimate effects of *those bundled experimental rules* for this experimental population.
Punishment availability is assigned; actual punishment is an endogenous action. Written
justifications are mandatory in selected treatments; their content is endogenous. Neither a
punishment/return regression nor a history prediction identifies the causal effect of actual
punishment, a particular explanation, monetary utility, or unobserved trustworthiness.
A session-level OLS interaction uses only 12 means and assumes exchangeable homoskedastic
session disturbances for its t interval. It is not an exact randomization test. Calendar/order
patterns and the allocation implementation cannot be audited from the selected observation file.

The authors' Table 2 is exactly reproducible to rounding. That confirms the mapping, not the
original study's every inference. In particular, our session-level sender interaction interval
is extremely wide. Higher average transfers under both rules do not establish a synergistic
mechanism or explain why subjects changed behavior.

## Prediction is a narrower preservation query

Let H be the selected full monetary history, R=f(H) the representation erasing returns,
Y in [0,1] the next sent amount /12, and m(H)=E[Y|H], r(R)=E[Y|R]. Under the same population law,
finite second moments and nested sigma-fields, conditional-expectation orthogonality gives

    E[(Y-r(R))^2] - E[(Y-m(H))^2] = E[(m(H)-r(R))^2] >= 0.

Proof: write Y-r=(Y-m)+(m-r), expand, and use
E[(Y-m)(m-r)]=E[E[Y-m|H](m-r)]=0. Equality is equivalent to m(H)=r(R)
almost surely. This is exact *conditional-mean* sufficiency, not conditional-distribution
sufficiency. Example: two equally likely histories with Y=1/2 certainly at one and
Y=0 or 1 with equal probabilities at the other have the same mean but different tail queries.
Neither finite ridge fit is guaranteed to equal m or r; equal or ordered sample losses do not
prove this population identity or its equality condition. Training variance can even reverse
which fitted model scores better. Mean elicitation is a standard scoring distinction; see
Gneiting & Raftery (2007), §4.3, equation (23), [primary paper](https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf).

For the fixed fitted models, define each held-out session's paired mean loss difference D_s.
Clipped predictions and Y in [0,1] imply D_s in [-1,1]. Conditional on the training sessions,
independence of the four evaluation sessions allows Hoeffding's bounded-variable inequality:

    P(|average(D_s)-average(E D_s)| >= e | training) <= 2 exp(-n e^2/2).

This follows from Theorem 1, equation (2.3), after mapping [-1,1] to [0,1], applied to both tails. Identical distributions
are unnecessary, allowing the equal-weight four-treatment target. Setting the RHS to .1 gives
sqrt(2 log(20)/4)=1.2238734. Intersecting the resulting interval with the known range [-1,1]
here leaves the entire range. This is a conditional sampling guarantee, not an exact rational
confidence certificate; numerical evaluation is ordinary floating point. The selected IDs are
deterministic, so exchangeability within treatment is a substantive premise, not proved by hashing.
[Hoeffding (1963), Theorem 1 and scaling discussion](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf).

The prespecified bootstrap sensitivity draws entire session differences, not rows. With four
heterogeneous sessions it cannot justify equivalence by itself, even though its narrow interval
lies inside the prespecified +/- .01 margin. This is a decisive failure of the tempting shortcut:
"the observed gap is small, therefore return history can safely be discarded."

## A sharp obstruction for a changed feedback mechanism

This is a specialization of the observational-equivalence approach to identification discussed
by Tamer (2010), §§1 and 3: [author's full paper](https://tamer.scholars.harvard.edu/sites/g/files/omnuum7756/files/tamer/files/pie.pdf).
Identification concerns a population observable law, separately from uncertainty in estimating
that law from finite data. The following proof does not assume our empirical distribution is
that population law.

Consider an additional intervention V: V=1 shows the usual end-of-round monetary feedback;
V=0 hides it before a next sender choice. No original treatment randomized V: all used V=1.
Fix any observable joint law P of histories, treatment, and next choices under V=1. Assume
only consistency for observed V=1 and the protocol's feasible next action Y(v) in [0,1].
Let mu=E_P Y(1). Then the **sharp identified set** for E Y(0) is [0,1], and for
E[Y(0)-Y(1)] is [-mu,1-mu].

Proof of necessity: the support bound gives 0 <= E Y(0) <= 1. Proof of attainability:
let an exogenous variable U carry an entire observed record distributed according to P.
Both constructions return U's observed next choice whenever V=1, preserving *all* the
observable joint law, not merely a mean. Construction A returns 0 whenever V=0;
construction B returns 1 whenever V=0. Neither violates feasible sender choices. A Bernoulli
mixture independent of U with weight q attains every hidden-feedback mean q in [0,1],
without altering P under V=1. The intervention occurs before the next choice, so prior
observed history remains unchanged. This settles the specified nonparametric class.

The two extensions are saturated mathematical explanations, not fitted psychological accounts,
claims of plausibility, QREs, or discoveries that real people would send zero/all under hidden
feedback. The executable check instantiates them on the empirical law of 720 sender-rounds:
mu_hat=1649/2880, with plug-in normalized endpoints -1649/2880 and 1231/2880. Those endpoints
are not a population confidence interval. Positive transfers or good prediction cannot rule
out either extension without an additional structural or intervention assumption.

Retaining returned amounts in the analyst model may improve prediction; it cannot restore
missing intervention support. Assuming feedback affects behavior only through the represented
state and imposing a stable response function could narrow the set, but those restrictions
are not tested here. The nearest informative addition is randomized feedback visibility before
a next sender choice, with session-level independence preserved and the altered information
protocol recorded. That would estimate a particular visibility intervention; it would still
not identify utilities or original off-path beliefs.

## Behavioral and Bellman boundaries

Payments are observed; utility, risk attitudes, reciprocity motives, subjective expectations and
attention are not measured by these rows. Unconditional transfers cannot separate altruism,
expected reciprocity, anticipated sanctions, confusion and learning. Imposing monetary utility
would supply, not estimate, a premise. Post-experiment attitudes would not automatically supply
pre-choice beliefs and are excluded from prediction.

QRE is an established possible response model: McKelvey & Palfrey (1995) formulate mutual
quantal best responses. Its [primary author record](https://authors.library.caltech.edu/records/4fh4n-4c340)
is metadata-only; the linked hosted full-paper attempt failed certificate/access checks here.
We do not borrow a QRE theorem or claim to fit it. This case lacks justified utility and
belief restrictions; a large extensive-form QRE would add unsupported structure to a small
sample. Even a logit response exp(lambda u_a)/sum_b exp(lambda u_b) is unchanged under
u -> c u and lambda -> lambda/c for c>0, showing that a scale normalization is essential.
No QRE package is built or substituted for the empirical baseline.

Bellman's v0.0.7 common perturbation witness establishes a consistency property across supplied
games and assessments. Observed finite errors neither specify nor validate that limiting
sequence. The diagnostic-erasure obstruction concerns equality of continuation values and
existence of a *shared* off-path consistency sequence; our empirical history comparison
concerns neither. IID Bernoulli confidence receivers cannot ingest these dependent, bounded
nonbinary choices as if there were 720 IID trials. No new strategic-disclosure theorem,
mechanism-composition guarantee, ambiguity-sensitive preference or participation result is earned.

This case materially advances empirical history assessment and source-to-model identification
discipline. Strategic disclosure and mechanism composition remain conditional mathematical
research rather than verified descriptions of this human experiment. Lean, Rust and optimization
migration have no demonstrated assurance or performance benefit for this bounded audit.
