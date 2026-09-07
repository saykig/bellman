# Executed illustrative checks

Python 3.9.6. 18 groups passed using exact rational arithmetic.

These are authored example checks, not independent formal verification, an LP implementation, a production test suite, or a model-grid experiment. No statistical sampling was performed. General results rely on the draft's analytic arguments.

| Group | Result | Scope |
|---|---|---|
| input_integrity | PASS | All 8 packet inputs match supplied SHA-256 and byte counts. |
| triangle_incompatibility | PASS | Required expectation 3 exceeds pointwise bound 2. |
| farkas_witness | PASS | A^T y=0; b^T y=-1/2. |
| positive_gluing | PASS | Constructed joint is normalized and preserves both supplied pair marginals. |
| fractional_transform_witness | PASS | t=2; transformed objective and conditional answer both 1/4; inverse recovers p. |
| structural_abstraction | PASS | Three-date original and two-class values agree; original transition rows differ. |
| bellman_residual_certificate | PASS | Checked exact residuals and evaluated greedy-policy regret in all 3 initial states; bound=63/80 |
| local_regret_telescoping | PASS | Expected sum of exact Bellman disadvantages equals evaluated policy regret: 7/64 |
| deficiency_simulator | PASS | Identity experiment simulates the binary noisy experiment with T=G and d=0. |
| contextual_failure | PASS | XOR auxiliary evidence changes risks to 0 versus 1/2. |
| signed_loss_span | PASS | Values -99,-98; span bound 1 is attained. |
| coupling_product_bound | PASS | Two-observation mismatch bound 19/100 improves union bound 1/5. |
| conditioning_amplification | PASS | Joint TV 1/100; conditional TV 1. |
| private_robust_mixture | PASS | Feasible mixture and equal-weight model lower bound both 1/2; pure worst loss 1. |
| persistent_vs_rectangular | PASS | Fixed-model worst cost 1; independently selected date costs total 2. |
| coverage_allocation | PASS | Exact first-100 allocation sum equals alpha*(1-1/101); infinite-tail identity is analytic. |
| tail_risk | PASS | Means 1 versus 2; CVaR_0.95 values 20 versus 2. |
| integrated_identified_action | PASS | Posterior range [4/7,8/11] varies; action 1 is uniformly strictly optimal with minimum gap 1/7. |

All eight packet inputs match the supplied manifest. The workspace is not a Git repository; no branch, commit, or push was made. Source inputs were not edited.
