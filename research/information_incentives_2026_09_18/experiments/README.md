# Reproduction and evidence boundaries

Run from the repository root using Python 3.9+ with NumPy and SciPy. The recorded
run used the versions in results.json. A temporary virtual environment is enough;
no environment or vendor tree is included in the repository.

```sh
python3 -m venv /tmp/bellman-incentives-reproduce
/tmp/bellman-incentives-reproduce/bin/pip install -r research/information_incentives_2026_09_18/experiments/requirements.txt
/tmp/bellman-incentives-reproduce/bin/python research/information_incentives_2026_09_18/experiments/check.py
/tmp/bellman-incentives-reproduce/bin/python research/information_incentives_2026_09_18/experiments/hidden_separator.py
/tmp/bellman-incentives-reproduce/bin/python research/information_incentives_2026_09_18/experiments/tree_identity.py
python3 research/information_incentives_2026_09_18/experiments/disclosure_exact.py
```

Programs print JSON and never overwrite retained evidence themselves. Compare
fresh output to the corresponding saved result; numerical optimizer paths may
vary across platforms. Failures are explicit exceptions, including under `-O`.

- **check.py / results.json:** independently sums actual utilities for every
  action deviation, rather than using the reduced gain formula as its oracle.
  Checks 300 parameter cases for both players, the six-branch result, original
  eight-cell numerical support programs, fixed/optimized information–penalty
  comparisons, and known-state disclosure continuation equilibria.
- **hidden_separator.py / hidden_results.json:** asymmetric H–X/H–Y tables,
  three shared budgets, direct 16-cell optimization, four-coupling primal/dual
  witnesses and independently minimized two-likelihood cost profiles. The profile
  reconstruction verifies the proposed intermediate representation. This fixture
  isolates compatibility; active operations are in check.py's two-component game.
- **tree_identity.py / tree_results.json:** 50 full-support 2×3×3 laws, source
  Markov references, augmented event flags, gluing, and KL decomposition. Original
  clique divergences are zero while global and discarded dependence are positive.
  This tests the identity nontrivially: ternary residual categories retain unknown
  dependence even after the binary event flag is fixed.
- **disclosure_exact.py / disclosure_results.json:** rational arithmetic checks
  of the three-type partial-certificate example, an attaining continuation and
  the summed incentive inequality. Its written proof covers all q∈[0,1].

Every result binds its source file(s) by SHA-256. The code is standalone; it does
not import or mutate the supplied Downloads programs. Original source hashes are
in ../sources/INPUT_MANIFEST.json. Theorems are proved in ../math, not inferred
from passing these checks.

Numerical limitations: roots, logarithms and optimizer outputs are floating-point.
Primal/dual residuals are diagnostics, not rigorous interval enclosures. Independent
SLSQP computations issue clipping warnings on some intermediate iterates; final
marginal/cost residuals and objective comparisons are reported. Unlike the earlier
supplied optimizer, none of the tested final objectives here had a material gap
from the analytical bound. The hidden-table implementation clips only negative
roundoff smaller than 1e-12 at theoretically zero cells and rejects larger errors.
Its initial boundary NaN was corrected before retained results; see RESEARCH_LOG.

A new [Lean check](../lean/README.md) verifies the six-branch real-number maximum
identity and the partial-certificate threshold/obstruction. It does not verify
entropy duality or the game semantics. The supplied audit's older Lean result
remains separate; none of its scope is silently inherited by the new statements.
