# Narrow Lean verification — new results

Checked on 18 September 2026 with Lean 4.33.1 and Mathlib commit
`0df444a360eaa60ab8c11dca51a86af692955474`. See [receipt.json](receipt.json), which
binds the exact [source](CompositionCore.lean) by SHA-256 and prints its axiom
dependencies. All four reported declarations use only `propext`, `Classical.choice`
and `Quot.sound`. There are no admitted proofs or custom axioms in the final file.

- `six_branch_reduction`: distributive real-number maximum identity converting
  three policy branches plus two operational branches into six common-law branches.
- `certificate_threshold`: for every real cost k, a common mixed continuation
  satisfying both sender inequalities exists iff k≥3/10.
- `separate_deterrents`: each type separately has a feasible zero-cost deterrent.
- `no_common_zero_cost_deterrent`: those separate possibilities cannot coexist.

Not formalized: derivation of policy/operational numerators from the game,
optimization over law families, KL/conjugacy, tree gluing, the PBE correspondence,
empirical assumptions, or novelty. These remain written proofs or modelling
premises. The formal max identity alone is not the whole Theorem E.

Reproduce with the included Lake configuration and `lake env lean CompositionCore.lean`.
Alternatively, use an existing matching built dependency cache read-only:

```sh
python3 verify.py --packages /path/to/project/.lake/packages --lean lean
```

The verifier checks the Mathlib Git revision, invokes the pinned Lean toolchain,
rejects compilation failures or `sorryAx`, and prints a fresh receipt. It does
not overwrite the retained receipt automatically. The default invocation expects
`lean` to be the elan toolchain selector. No dependency cache or build output is
included in this research folder.

Development record: an initial blanket Mathlib import was stopped and replaced
by three specific modules. The first narrow build found proof-script mismatches
in addition-order lemmas and maximum grouping; these were fixed with explicit
inequalities and associativity/commutativity. Only the subsequently successful
source and its receipt are claimed as verified.
