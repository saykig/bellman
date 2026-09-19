# Reproduction and evidence status

Create an external Python environment and install requirements.txt. From this
folder, run `python check.py > /tmp/bellman-frontier-replay.json`.
The retained results.json is a dated record, not a file to overwrite on replay.
Compare benchmark values, residuals, exact results and source_sha256; environment
version fields may differ. All randomness uses seed 20260918.

The checks include:

- 36 comparisons of profile supports with optimization over the original 12
  probability cells: 12 each for KL, Pearson χ² and total variation;
- KL primal/dual equality, an attaining policy witness, direct enumeration of all
  six unilateral product actions for both receivers, and 200 feasible random laws;
- a profitable operational deviation below the gate threshold and a profitable
  policy deviation below the fine threshold;
- 303 credible mixed-policy witnesses and the (C,C) threshold witness, checking
  all unilateral policy actions;
- 72 exact finite profile/composition threshold queries;
- rational χ² Markov-glue counterexample, nonconvex continuation-payoff obstruction,
  and a finite search for inconsistent two-sender posteriors.

The budget and marginal residuals are inspected independently of solver success.
Maximum direct/profile gap in the retained run is approximately 3.06e−12. These
are numerical falsification checks; they are not universal proofs or certified
interval bounds. Exact rational arithmetic checks finite examples, while the
written mathematics proves the universal results. Narrow Lean checks are separate.

Initial failed approach: applying SLSQP directly to total variation produced a
0.0377 objective gap and unsuccessful status. The absolute-value objective is
nonsmooth. The retained code instead uses an explicit 24-variable linear program
(12 probabilities and 12 absolute-value slacks) for TV. No failed result was
promoted to evidence of the theorem. Smooth SLSQP checks can emit clipping warnings
when trial steps leave bounds; retained final points satisfy the displayed residuals.

The script is a research test suite, not a production certificate receiver. Python
assertions must be enabled. Its source hash binds the retained JSON to this code;
no empirical validity of the game or information budget is asserted.
