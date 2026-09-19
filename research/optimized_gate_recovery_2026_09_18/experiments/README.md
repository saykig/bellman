# Reproducible exact search and original-cell receiver

From the repository root:

```sh
python3 research/optimized_gate_recovery_2026_09_18/experiments/search.py
python3 research/optimized_gate_recovery_2026_09_18/experiments/check.py
python3 -O research/optimized_gate_recovery_2026_09_18/experiments/check.py
```

These print output without overwriting retained evidence. To test a new producer
edition, save its stdout to a NEW file and pass that path to check.py. Do not
replace historical candidates.json or results.json after this edition is committed.

search.py enumerates 45 rational gates for each of five radii and nine source
parameters per gate. Its candidate formula is tested by check.py, which does not
import or run the producer. The receiver reconstructs joint theta/S/T cells,
conditions on the public output and certificate, enumerates receiver payoff
crossings, checks interval interiors, and computes exact minimum fines. Minimizing
sender utility over receiver best responses covers all mixtures for this one
sender-information-type continuation: a linear function reaches its minimum at
a best-response pure action. This shortcut is NOT valid for general multi-type
simultaneous incentive vectors.

The retained run checks 2,025 law/gate combinations. Wrong-value and stale-producer
packets are rejected. Identity reading of search.py binds the candidate without
executing or trusting it. Normal and optimized Python give byte-identical result
output; checks use explicit exceptions and are not stripped assertions.

The erasure control and the full-information posterior control both give zero
fine. Support bounds and strict on-path C optimality are checked independently.
The analytical argument excludes all unlisted laws, gates and mixtures; the grid
alone proves neither the continuum optimum nor a discontinuity. No floating-point
optimizer, empirical data or proof assistant is used.
