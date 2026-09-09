# Compare measurements by the decisions they improve

This runnable reference ranks a supplied finite menu by Bayesian expected loss
plus measurement cost. Read [SPEC.md](SPEC.md) for premises, [FINDINGS.md](FINDINGS.md)
for exact examples and limits, and [SOURCES.md](SOURCES.md) for borrowed capabilities.

Using Python 3.13 and an existing read-only Decision Lab repository containing the
pinned commit in menu.py:

```sh
python3.13 research/measurement_decision/menu.py produce research/measurement_decision/afy-design.json /tmp/new-measurement-result.json --engine-repository /path/to/existing/decision-lab
python3.13 research/measurement_decision/menu.py receive research/measurement_decision/afy-design.json /tmp/new-measurement-result.json --engine-repository /path/to/existing/decision-lab
python3.13 research/measurement_decision/checks.py --engine-repository /path/to/existing/decision-lab
```

Output creation refuses overwrite. Receiving freshly checks all component answers
with solver imports blocked, checks the exact whole design and engine identities,
and recomputes menu ranking. Every input quantity is a reduced rational string.
Edit a copy of either design JSON to supply another problem; the common prior,
actions, losses and unit occur once, and each measurement supplies a channel and
cost. `no_measurement` must be a zero-cost single-outcome channel. No extra fields
for hidden-state policies, changing state or changing actions are supported.

Without the private engine repository, the public retained evidence still has a
small independent exact risk/action/ranking audit:

```sh
python research/measurement_decision/checks.py
```

That audit enumerates all outcome-only policies; it is not a replacement receiver
for all donor result metadata. It explicitly reports that donor receiving was
not executed. Full local receiving is recorded separately; hosted acceptance
must not claim access to the private dependency. Neither path validates a prior,
utility scale, channel, cost or real-world applicability.
