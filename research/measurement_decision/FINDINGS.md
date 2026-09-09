# What measurement would change this decision?

2026-09-09. Stipulated design study, separate from frozen AFY estimates.

## First case: a conditional forecast is useful but does not win

The decision maker can commit to always cooperate (C) or always defect (D).
The opponent is either forgiving F (always C) or retaliatory T (tit-for-tat,
initially C). The utility hypothesis is linear u(x)=x or reciprocal u(x)=-1/x.
The four persistent states are F-linear, T-linear, F-reciprocal, T-reciprocal,
with supplied prior 1/4 each. This prior is not an AFY estimate.

Stage payments are CC=51, CD=22, DC=63, DD=39. Discount δ=7/8; the criterion
is normalized discounted expected stage utility. Normalize each utility by
v(x)=(u(x)-u(39))/(u(51)-u(39)). This cardinal comparability across utility
hypotheses is a normative premise, not empirically identified welfare.
No action implementation noise is supplied in this design.

C gives value 1 in every state. Linear v(63)=2; reciprocal v(63)=34/21.
D against F gives these values forever; against T it gives them in the first
round and v(39)=0 thereafter. Thus D values are (2,1/4,34/21,17/84).
Loss is negative value. These are exactly the two rows in afy-design.json.
Committing to either infinite plan is an assumed available action; we do not
claim it is optimal among arbitrary adaptive plans or sequentially credible.

The unconditional report says the opponent initially cooperates in every state.
Conditional reports concern response after one's hypothetical deviation; symmetric
accuracy is stipulated at .51, .55 or 1. This is a report channel, NOT an actual
deviation intervention: physically inducing defection would alter the history
and require another subject. Utility measurement perfectly reports the utility
hypothesis. Joint measurement reports utility and the .55 conditional signal;
its entire joint likelihood is supplied, not inferred from marginal likelihoods.
The subject assumes no elicitation effect and no strategic report manipulation.
Costs are supplied normalized utility-loss increments, not cash converted through
an unknown utility function.

The no-measurement risk is -57/56, achieved by D. Exact net benefits:

| Measurement | Cost | Net decision benefit |
|---|---:|---:|
| No measurement | 0 | 0 |
| Unconditional report | 1/1000 | -1/1000 |
| .51 conditional report | 1/1000 | -1/1000 |
| .55 conditional report | 1/1000 | 2491/84000 |
| Perfect conditional report | 1/2 | -19/168 |
| Utility hypothesis | 1/100 | **97/2800** |
| Joint utility + .55 report | 1/50 | 69/2800 |

The .55 report selects D after F-report and C after T-report. Utility measurement
selects D after linear and C after reciprocal; the extra conditional report in
joint measurement changes neither choice. Utility measurement wins this menu.
Perfect type information has positive gross value but loses to doing nothing
once cost is charged. Cost reversals do not contradict Blackwell ordering.

For T probability w, D's values are 2-7w/4 (linear) and
34/21-17w/12 (reciprocal). C is preferred at w≥4/7 and w≥52/119 respectively.
With a half-half utility mixture the threshold is 68/133. The weak channel's
posteriors .49 and .51 are distinct but below this threshold: informative,
zero gross decision value. The .55 channel straddles it. However, both .45 and
.55 lie between the two utility-specific thresholds. Hence knowing utility
changes the decision even after that conditional signal, while the conditional
signal adds no value after utility is known. This is an explicit residual
uncertainty calculation, not a claim about subjects' actual utilities.

In each pure state the optimal action is D for F and C for T. Perfect type
information resolves that disagreement; utility information alone does not.
The Bayesian-optimal measurement therefore need not resolve modelwise action
disagreement. No robust preference or shared-prior guarantee is claimed.

## Second case: equipment inspection through the unchanged interface

States healthy/minor/major have prior (.6,.3,.1). Actions run/service/replace
have loss rows (0,8,80), (6,3,35), (24,24,24). No measurement selects service
with risk 8. The supplied noisy inspection costs 2/5 and has rows
(.8,.15,.05), (.2,.6,.2), (.05,.15,.8), for green/amber/red signals.
Its optimal signal-only policy is run/service/replace. Its risk is 1209/200,
net benefit 391/200. Perfect inspection costs 10 and has net benefit -53/10;
a fair independent coin report costs 1/10 and has net benefit -1/10.

This three-state, three-action example uses exactly the same menu file contract,
producer and receiver, with no case-specific engine changes. It establishes
bounded computational reuse, not real maintenance validity or an independently
authored M4 transfer case. All channels, losses, costs and priors are stipulated.

## Proved, checked and still missing

SPEC.md proves the finite menu composition, zero-value criterion and one-way
cost-free garbling implication. The existing exact donor checker independently
enumerates signal-only policies, checks conditional quantities and byte bindings.
The separate Bellman audit enumerates 38 AFY policies and 66 maintenance policies
and checks the ranked risks/action sets without importing donor code. Receiving
also runs with donor producer imports blocked, normally and under optimization.
These are executable checks, not formal verification or external peer review.

The AFY primary comparison remains inconclusive; its simpler Markov/report
baseline performs better and its conclusions depend on utility and priors.
The present study does not refit those data, validate report accuracy, infer
subjective priors, establish that measuring utility is feasible/perfect, or
show that elicitation leaves behavior unchanged. It identifies which supplied
premises would make a measurement worthwhile and when information fails to
change a decision. Before empirical adoption, a protocol must warrant those
channels, a common utility scale and costs, or the calculation must be revised.
