# Statistical rectangle to corner-model verification

[Mathematical contract and proofs](../../foundations/BELLMAN_STATISTICAL_RECTANGLES_TO_CORNER_MODEL_GUARANTEES.md).

Run the complete current and historical acceptance entry point from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verification/statistical_corner_models/run_checks.py
```

`reference.py` is a bounded adapter over existing components. It asks the controlled-multistream
receiver to reconstruct the retained outward rectangle, checks an explicit bijection from stream
identities to one or two transition-parameter identities, and inspects every completed sequential
skeleton path. Only a skeleton in which each parameter occurs in at most one transition factor per
path receives the multi-affine corner warrant. Its distinct corners are instantiated as complete
ordinary sequential subjects and sent through the unchanged persistent-family exact matrix
consumer.

Receiving independently reconstructs the path-use table, mapped rectangle, corner coordinates,
corner subjects, exact family matrix, covered-class regret, caps, and deterministic winners. A
separate forward complete-path sum must match every family cell. For the fixed two-parameter case,
a `17 × 17` exact rational grid supplies an additional interior audit; the mathematical companion,
not that finite grid, proves the statement for all real rectangle points. Candidate statistical,
corner, family, and ordinary-certificate producers can all be disabled while retained evidence is
checked.

The fixed cases cover the four-corner data-derived construction, one unobserved `[0,1]` parameter,
a deliberately loose outward rectangle, permuted/malformed mappings, signed costs, early `STOP`,
zero-probability branches, mutually exclusive parameter reuse, stale evidence, changed losses,
full deterministic minimax-loss/minimax-regret selection, hidden-model policy rejection, and the
exact `p(1-p)` failure on `[0,1]` and `[1/4,3/4]`. A repeated parameter on one path returns an
invalid corner-reduction warrant while leaving the sequential model valid. More than two
parameters returns a typed `unfinished` resource refusal.

`run_checks.py` executes these cases normally and with `-O`, executes the current multistream,
PR14 acceptance, persistent-family, family-replanning, and history-layout checks in both modes,
and runs PR14's complete acceptance/historical chain at its exact merge in a disposable clone.
It verifies frozen PR12, PR14, PR8, PR10, and historical result identities without feeding this
new stage through an obsolete prior-PR path allowlist. `results.json` is the separately retained
source-bound result record; it is not rewritten historical evidence.

The result supplies conditional mathematics only. The IID/completeness premises are supplied but
not empirically validated. Corners have no model probabilities. Coverage failure probability,
loss/regret units, and bracket precision remain separate. No randomized policy, continuous
optimizer, Writ/Decision Lab integration, language migration, dynamic risk, or causal claim is
added.
