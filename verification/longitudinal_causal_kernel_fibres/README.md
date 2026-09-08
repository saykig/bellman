# Longitudinal causal kernel-fibre verification

This bounded exact reference implements the additive companion
[`BELLMAN_LONGITUDINAL_CAUSAL_KERNEL_FIBRES_AND_PERSISTENT_DECISIONS.md`](../../foundations/BELLMAN_LONGITUDINAL_CAUSAL_KERNEL_FIBRES_AND_PERSISTENT_DECISIONS.md).

It accepts the PR #20 binary `A1,L1,A2,Y` subject only when both first actions and every
intermediate history are supported. Supported second-stage outcome rows are reconstructed exactly;
each unsupported second-stage binary row is one explicitly ordered free coordinate in `[0,1]`
under a supplied saturated no-cross-row-restriction profile. The continuous fibre remains in the
evidence. A distinct family of at most 16 corner subjects is used only for deterministic outcome
probabilities, additive losses, pairwise policy differences, common optima, minimax loss, and
same-completion regret, for which the companion proves multi-affine corner reduction.

`reference.py` contains separate candidate and receiver paths. The receiver reconstructs support,
the exact missing-row order, all corner subjects, and all 32 policies. It compares direct cell
arithmetic with ordinary sequential certificates and independent complete-path enumeration. For at
most four corners it also reuses the unchanged persistent-family receiver; eight and sixteen
corners are checked locally while exposing that historical reference's four-model limit.

`checks.py` includes:

- the exact zero-gap collapse to PR #20;
- the one-gap `S=1/4`, `U(q)=q/2` example with opposite completion optima;
- a decision identified despite one unresolved row after a declared cost change;
- the two-gap `(q0+q1)/2` example, all four corners, and the exact `11/30` interior audit;
- all dimensions zero through four, up to 16 corners and 512 policy values;
- a nonlinear `q(1-q)` demonstration that corners are not the continuous fibre or a generic query
  method;
- outside-profile earlier-stage gaps and unsupported stronger causal restrictions;
- complete-policy/no-hidden-model-oracle and same-completion regret controls;
- changed support/order/premise/profile/loss/policy and forged transition, corner, interval,
  certificate, common-set, and minimax controls; and
- receiving with all candidate producers disabled.

Run the complete current and historical acceptance chain with:

```bash
python3 verification/longitudinal_causal_kernel_fibres/run_checks.py
```

The runner executes the new checks normally and with `-O`, runs inherited current Bellman checks,
checks append-only/frozen preservation and Markdown links, and replays the exact merged PR #20
acceptance chain in an isolated clone. Fixed examples and exhaustive bounded checks are not formal
verification or empirical validation of the supplied causal premises.
