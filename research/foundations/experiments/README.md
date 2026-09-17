# Exact reproduction

From the repository root, using Python 3.9+ standard library:

```sh
python3 research/foundations/experiments/checks.py
python3 research/foundations/experiments/signature_probe.py
```

Both recompute and compare against retained JSON, including a SHA-256 of their
own source. `--write` is for creating the initial evidence and refuses overwrites.
Future corrections require a new edition, not edited old receipts. No seeds,
network access, data download, floating-point arithmetic or optimization tolerances
are involved. Errors use explicit exceptions and checks also run under `python3 -O`.

`checks.py` enumerates all 4,096 triples of binary two-variable relations and
compares the join criterion against a separately constructed oracle of all 256
global three-bit relations. Its 406 overlap-compatible triples include the
all-empty triple, which has an exact empty extension; the four inconsistent
triples count only nonvacuous local relations. There are 166 exact extensions,
236 nonempty lossy joins and four empty inconsistent joins.

It also tests 729 kernel associativity triples, and 2,187 combinations of a fixed
root distribution, two binary kernels and all hard interventions, comparing
factor-product evaluation with sequential path expansion. The tested kernel
rows use {0,1/2,1}. It verifies the worked rational example, the coupled-flip
counterexample, and additional failure controls. These grids do not prove the
arbitrary finite stochastic theorem; the written proof supplies that result.

`signature_probe.py` enumerates all 65,535 nonempty knowledge relations over the
16 pairs of deterministic unary Boolean functions, for two explicitly defined
query families. It compares full per-model answer vectors, not just independent
bounds. Retained witnesses are decoded in math/SIGNATURE_ADDENDUM.md.

The experiments are research code, not a general-purpose causal inference API.
They do not validate empirical premises or infer a catalogue from observations.
Lean reproduction and its narrower proof scope are documented in ../lean/README.md.
