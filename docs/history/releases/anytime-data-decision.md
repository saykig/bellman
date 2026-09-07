# Anytime-valid Bernoulli data-to-decision bridge

Historical period: 2026-09-07

Historical finalization: 2026-09-07T18:43:07-04:00

Tagged commit: `92922ab6604840152ad7f7800969673335748272`

Git tree: `2345b79ccd0bfee81703330506e8c647989ae1f1`

Standing: Bounded bridge completed; receiver support and live-CI preservation boundary repaired.

## Question

Bellman asked whether an explicit statistical premise could yield uncertainty evidence valid under
repeated inspection and data-dependent stopping, then support a separately checked exact action
conclusion without manufacturing a point estimate or conflating coverage probability with loss.

## What we tried

The bridge bound a complete ordered binary prefix, stream/population/protocol identities, an IID
Bernoulli fixed-parameter premise, rational error level, summable spending rule, and requested
dyadic precision. A producer used bounded bisection for an outward rational interval. A receiver
recomputed exact binomial-tail inequalities and width. A separate decision request bound rational
losses, unit, query, and intended action; its receiver checked endpoint affine risks, complete
minimizer/strict sets, and named-action regret. Acceptance review then aligned receiver limits with
the advertised producer profile and routed live CI through current checks plus pinned replay.

## What worked

The construction gives simultaneous coverage over all inspection times under the complete fixed-IID
Bernoulli premise and preserves validity at a data-dependent stopping time. Exact affine losses are
checked over the retained interval without choosing a midpoint. The statistical and decision
subjects revise independently. The maintained profile supports at most 128 observations, four
actions, and 64 requested precision bits; out-of-profile requests are typed
`unfinished`/`resource-refusal` rather than mathematical rejection.

## What failed or was falsified

At the reviewed PR12 head, receiver routes accepted some manually authored certificates outside the
producer's stated support limits. The mathematics of those certificates was not false, but the
public executable support contract was inconsistent. A legacy live workflow also treated later
authorized steering-document changes as forbidden historical mutation. The additive hardening
restored one support profile and separated current validation from unchanged replay at the pinned
PR10 merge.

## What stopped or closed

The repair did not rewrite the mathematical companion or original result record. No posterior,
adaptive-sampling theorem, sequential controller, multistream process, empirical study, Writ
integration, Decision Lab change, or formal proof was added.

## What survived

Complete data identity, explicit sampling assumptions, exact outward intervals, all-time coverage,
independent decision subjects, endpoint risk certificates, strict/tied action sets, regret in loss
units, typed resource refusal, and immutable historical replay remained the bounded contract.

## Verification and evidence

- [Mathematical companion](https://github.com/saykig/bellman/blob/92922ab6604840152ad7f7800969673335748272/foundations/BELLMAN_ANYTIME_VALID_DATA_TO_DECISION.md) and [original result](https://github.com/saykig/bellman/blob/92922ab6604840152ad7f7800969673335748272/verification/statistical_decision_bridge/results.json)
- [Acceptance-hardening record](https://github.com/saykig/bellman/blob/92922ab6604840152ad7f7800969673335748272/verification/statistical_decision_bridge/ACCEPTANCE_HARDENING.md) and [separate repair result](https://github.com/saykig/bellman/blob/92922ab6604840152ad7f7800969673335748272/verification/statistical_decision_bridge/acceptance_hardening_results.json)
- Merged evidence: [PR #12](https://github.com/saykig/bellman/pull/12)

## Known gaps

Coverage depends on the supplied complete IID Bernoulli stream with one fixed real parameter; the
checks do not establish independence, representativeness, absence of drift, loss legitimacy,
causal meaning, empirical usefulness, or authority. The bounded exact reference uses shared Python
arithmetic/authorship and fixed cases, not independent formal verification or scalable inference.

## Direction after this milestone

The programme retained the bridge as one narrow capability while the living roadmap continued to
govern any next mathematical or transfer work. Further work would have to preserve the separation
among sampling premises, uncertainty evidence, decision losses, calculation, applicability, and
authority rather than treating this reference as a general reasoning system.
