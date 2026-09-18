# Boundary checks

Use Python with numpy 2.0.2 and scipy 1.13.1 (the retained run), then:

    python check.py > /tmp/bellman-boundaries-replay.json

Keep assertions enabled. Do not overwrite the historical results.json on replay.
The file records its source hash, seed, residuals and solver statuses.

Checks: asymmetric source-support jumps caused by each certificate; a support
change whose effect is masked by the controlled fine; 14 independent parameter
cases comparing the support-function formula with 56 optimizations over the
original 12 probabilities; six saturation-threshold checks; simultaneous sender
trembles for both overlapping certificates; and rational catalogue/incentive/
equilibrium counterexamples. The largest direct/formula difference is about
2.05e−10. One SLSQP branch reported unsuccessful status despite a final point
whose independently checked feasibility and objective gap met the tolerances.
That status is retained, not suppressed or treated as a proof. Intermediate
bound-clipping warnings are also possible.

These computations test the analytical results. They do not prove continuity or
exclude all counterexamples; the written theorems do that within their stated
scope. Rational arithmetic checks finite witnesses, not transcendental budget
identities. No empirical or production claim is made.
