# Statistical decision bridge verification

[Mathematical contract and proofs](../../foundations/BELLMAN_ANYTIME_VALID_DATA_TO_DECISION.md).

Run from the repository root with the existing Python runtime:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verification/statistical_decision_bridge/run_checks.py
```

The runner executes all new checks normally and with `-O`, compares exact observations, reruns the
current family-replanning and persistent-family cases, and invokes PR #10's complete inherited
preservation chain at its pinned merge commit in a temporary local clone. It verifies that the PR
#10 merge tree equals its reviewed head, that current inherited mathematical sources retain their
identities, and that every pre-existing base file is unchanged except the named living documents,
append-only ledgers, and maintained workflow routing. The historical family-replanning workflow
now routes live PR execution through this maintained entry point; the old runner is still executed
unchanged at the pinned PR #10 merge instead of being asked to classify authorized later document
edits.

`reference.py` separates the sampling subject from the decision subject. A sampling request binds
the complete ordered binary prefix, stream/population/protocol identities, the exact IID Bernoulli
fixed-parameter premise, rational alpha, the fixed summable spending rule, and requested dyadic
precision. A decision request separately binds the exact signed two-outcome losses, unit, query,
and independently intended action. Changing a decision table therefore requires a new decision
certificate without inventing a new sample or invalidating the unchanged sampling interval.

The interval producer uses bounded dyadic bisection. Its receiver recomputes `n`, `k`, the per-tail
allowance and both exact binomial-tail inequalities; it neither calls nor trusts the root search.
The decision receiver recomputes every pairwise affine-risk maximum at the two retained interval
endpoints, the complete common-minimizer and strict sets, and named-action regret. Producer-disabled
checks retain both generated and manually authored evidence. A separate Pascal recurrence checks
important tails, complete binary-path enumeration checks the repeated-inspection recursion at a
smaller horizon, and the existing joint-law receiver independently reproduces the headline risk
difference on the two-atom `(1-p,p)` model.

Producer and receiver entry points share one finite request profile: at most 128 observations,
four actions, and 64 requested precision bits. The precision field is both the producer's number of
dyadic search iterations and the receiver's independent maximum bracket-width obligation; those
roles remain distinct even though this bounded reference supports the same request limit for each.
An out-of-profile, otherwise mathematically valid certificate receives a typed
`unfinished`/`resource-refusal`, never a mathematical rejection. A request is validated before its
budget is checked; once the resource boundary is established, the receiver may decline to inspect
the evidence and performs no tail or risk arithmetic. Within-budget malformed evidence still
rejects. Derived proof coordinates are not capped by the external-input bit limit.

The authored S1–S6 controls include `n=0`, boundary and interior counts, exact equality brackets,
wide but valid evidence, false precision, wrong counts/allocation/identity, large derived rational
coordinates, stale data and decision subjects, immutable caller inputs, data correction versus
append, nominal fixed-time repeated inspection, dependence/copying, changed losses, ties,
singletons, Boolean/float refusals, and explicit resource exhaustion. `results.json` records the
actual hosted runtime, source hashes, exact observations, base/source identities, and inherited
preservation results.

The [acceptance-hardening record](ACCEPTANCE_HARDENING.md) and its separate
[`acceptance_hardening_results.json`](acceptance_hardening_results.json) preserve the reviewed
mathematics and original `results.json` while recording the receiver-contract and live-CI repair.
Resource refusal is `unfinished`, with `kind=resource-refusal`. Passing arithmetic does not validate IID sampling, independence,
representativeness, absence of drift, causal meaning, loss legitimacy, empirical usefulness, or
authority to act. The implementation supplies no Bayesian posterior, adaptive-sampling theorem,
sequential controller, Writ integration, Decision Lab change, language migration, or formal proof.
