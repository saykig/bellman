# Measurement selection for one persistent decision state

2026-09-09. Bounded Bayesian design study; not an empirical sequel fit.

## Subject and premises

A finite hidden state s, supplied rational prior p, common actions A, finite loss
matrix L(a,s) in a declared common unit, and a finite menu of exogenous channels
K_m(x|s) with nonnegative constant costs c_m. One persistent state determines both
observation and loss. A policy sees m and x, never s. Measurement neither changes
state nor the loss/action menu. These are supplied premises. Utilities represented
in different states require a supplied common cardinal scale. No ambiguous-prior
or modelwise robust guarantee is inferred from the Bayesian criterion.

## Query and derivation

Let R0 = min_a sum_s p(s)L(a,s). For forced measurement m,

    Rm = c_m + sum_x min_a sum_s p(s)K_m(x|s)L(a,s).

Choose every minimum among R0 and all Rm. Net benefit is R0-Rm. Each branch
minimizes independently: expanding the expected loss of any signal-only policy
as a sum over x proves the formula. A branchwise minimizing deterministic policy
attains it. Randomization is a convex combination and cannot improve it. Zero-mass
outcomes have no posterior and impose no condition on the selected action.

Ignoring information is feasible, so the gross benefit is nonnegative. Gross
benefit is zero **iff** all positive-mass outcomes have a common minimizing
action. Proof: a prior minimizer is constant and achieves R0. The difference
between its risk and the branch minimum is a sum of nonnegative terms; equality
forces each positive-mass term to vanish. Conversely a common branch minimizer
attains the sum of minima with a constant action, so R0 equals that sum.

For a state-independent stochastic garbling G, K_weak=K_strong G: observing the
strong signal and sampling G simulates every weak policy. Thus strong gross risk
is no greater. This says nothing about cost-adjusted ordering. It is the finite
one-way specialization of the comparison-of-experiments argument already stated
in Bellman substrate v1.1 section 7; no general converse is claimed.

## Reuse and boundary

Reuse the pinned Decision Lab finite-one-observation.v1 solver and independent
joint-mass/policy-enumeration checker. Its single-test acquisition minimum is NOT
a measurement ranking: compare its forced observe_once risks, otherwise rejected
expensive measurements incorrectly tie the no-observation baseline. Composition
is justified only after exact common state/prior/action/loss/unit equality and
complete menu identity are bound. Input identity includes the whole design file.

The result concerns this supplied prior and menu, not all priors, arbitrary
sequential measurements, state-changing experiments, strategic truthfulness,
equilibrium, empirical calibration, authority to commit, or an optimal policy
outside A. Informative channels may have zero decision value. Even useful
measurement may leave disagreement between possible states. These limitations
are mathematical scope, not missing optimizer features.

## Provenance and implementation plan

AFY findings and acceptance at aa2f9f24bb0e2ad777f1ca9df0332b76ce02ea73 remain
frozen. No AFY target data is refit or used to estimate the design below. Exact
engine source is read from existing Decision Lab commit
e5f77dfcf929708951f4673b3f394461ef09c752; it is not modified or vendored. A source
manifest and raw input/result identities accompany retained evidence. A receiving
process blocks producer imports and invokes the independent donor checker.

Analytical derivation, executable checks, formal verification and empirical
validity are separate. No Lean or language migration is justified: finite sums and
existing exact enumeration suffice. CPython 3.13 is the existing donor runtime.
