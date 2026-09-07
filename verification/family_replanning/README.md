# Family-replanning verification

[Mathematical contract and proofs](../../foundations/BELLMAN_FAMILY_REPLANNING_AND_ROOT_GUARANTEES.md).

Run from the repository root with the existing Python runtime:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verification/family_replanning/run_checks.py
```

The runner executes R1–R8 normally and with `-O`, compares their exact observations, invokes the
unchanged persistent-family preservation chain, verifies that PR8's merge tree equals its reviewed
head, and checks every pre-existing file at the pinned base. Historical files must remain
byte-identical; only README and the cumulative ledgers may receive their append-only entries.

`replanning.py` imports the existing ordinary, accumulation, transport, and persistent-family
types and consumers. A request binds one ordered family, common baseline and replacement policies,
one cut, checked modelwise source certificates, one root-cap kind, and an exact threshold. The
producer constructs the complete policy and signed upper-table splice. The receiver independently
reconstructs the policy and every path factor, validates both source certificates, verifies every
table identity, invokes the unchanged ordinary consumer, and recomputes the cap disposition and
positive-mass continuation allowances without calling the producer.

Actual performance is a separate exact-evidence route. It checks full optimum and policy-evaluation
equalities for baseline, replacement, and final policies and verifies the single-splice path
identity. It never interprets the difference of two loose upper bounds as a bound on actual change.

The checks use independent forward complete-path sums and tiny full policy enumeration for the
headline cases. They cover signed costs, STOP, root/terminal/unreachable cuts, zero probabilities,
non-topological storage, different model supports, large derived fractions, immutable inputs,
ordinary-valid but false splice provenance, loose-bound versus exact-violation dispositions,
overlapping edits, and optimized execution. Receiver checks are repeated with all relevant new and
inherited candidate producers disabled.

`results.json` records the actual GitHub Actions runtime, counts, exact observations, source hashes,
base/head identities, and inherited preservation results. The implementation budget is inherited
from the finite reference. The result supplies no model validity, statistical coverage, authority
to act, randomized-policy claim, robust dynamic-programming recursion, or dynamic-consistency
theorem.
