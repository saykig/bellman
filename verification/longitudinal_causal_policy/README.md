# Two-stage longitudinal causal policy verification

[Mathematical contract and proofs](../../foundations/BELLMAN_TWO_STAGE_LONGITUDINAL_CAUSAL_POLICY_AND_SEQUENTIAL_BRIDGE.md).

Run the complete current and historical acceptance entry point from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verification/longitudinal_causal_policy/run_checks.py
```

`reference.py` accepts a complete exact rational 16-cell `P(A1,L1,A2,Y)`, four explicitly coded
binary variables in fixed temporal order, named consistency/intervention/first- and second-stage
exchangeability/adaptation/no-interference premises, a complete deterministic history policy, and
exact signed costs and losses. The policy receiver independently checks policy-specific positivity
and the two-stage g-formula. A zero-probability intermediate branch needs no selected-action
support; a positive branch with an unsupported selected action fails closed.
Queries outside the complete binary regime-distribution/additive-loss and full-subject bridge
contracts return `unsupported-longitudinal-causal-query` rather than being coerced into them.

The full-subject bridge requires both first-stage actions, both intermediate values under each
first action, and both second-stage actions at each resulting history to have positive
observational support. Only then does it construct the 21-node completed Bellman subject. The
receiver reconstructs every transition, checks all 32 structurally complete deterministic
policies through the existing sequential certificate consumer, and independently compares
complete-path distributions and costs with the causal g-formula. Policies differing only off the
chosen root remain distinct.

Fixed controls include the `1/8` positive dynamic-regime value, equality of the complete causal and
Bellman minimizing sets, exact signed costs, policy-specific versus full-subject support, first-
and second-stage positivity failures, zero-probability intermediate histories, stale binding and
forged claim rejection, and producer-disabled receiving. The decisive two-world control has
identical one-stage `do(A2=0)` and `do(A2=1)` bad-outcome marginals of `1/2` but reverses which
history-dependent policy has risk zero rather than one. One-stage intervention marginals therefore
cannot substitute for the history-conditioned causal kernels.

The runner checks this package normally and with `-O`, exercises inherited current Bellman
packages, verifies history/release identities, preserves every post-PR #19 base file except the
declared living pointers and workflow delegation, and replays PR #19's complete historical chain
from its exact merge commit in an isolated clone. `results.json` is a compact source-bound
execution record; prior result files remain unchanged.

The causal premises and observational law are supplied rather than empirically validated. This is
not graph discovery, longitudinal partial identification, transport, safety or persistent-family
composition, randomized policy optimization, Writ/Decision Lab integration, formal verification,
or authority to act. Exact enumeration remains at 32 policies, so no solver or language trigger
was reached.
