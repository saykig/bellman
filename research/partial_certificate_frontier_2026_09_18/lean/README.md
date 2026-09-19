# Narrow Lean evaluation

The mathematics was stated before these lemmas were formalized. Lean 4.33.1 with
Mathlib revision `0df444a360eaa60ab8c11dca51a86af692955474` checked:

- the two-component scalar profile identity, assuming attained fibre minima;
- upper-image composition under vector addition, for an arbitrary index type;
- equivalence of all upper-threshold queries with equality of upper images;
- the general two-type disclosure-cost inequality;
- the strict inequality excluding C below the partial-certificate fine;
- the determinant identity behind independent sender likelihoods.

These proofs use only the standard axioms listed in receipt.json and contain no
`sorry`. They do NOT formalize entropy conjugacy, the full game/PBE construction,
support-limit continuity, all finite-network elimination, empirical assumptions or
novelty. In particular, formalizing the cost-threshold arithmetic does not prove
that a proposed continuation is a Nash equilibrium; the written proof and direct
payoff checks handle that separate premise.

Reproduce with a matching built Mathlib package cache, used read-only:

    python verify.py --packages /path/to/.lake/packages --lean /path/to/lean > /tmp/bellman-frontier-lean.json

The verifier checks the Mathlib revision, selects the fixed Lean version and
records the theorem source hash and printed axioms. No vendored toolchain/cache is
stored in the repository. The prior phase's Lean receipt remains untouched.
