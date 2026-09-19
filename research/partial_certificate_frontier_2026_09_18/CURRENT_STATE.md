# Current state — 18 September 2026

Completed the bounded priorities in order. [Read the note](manuscript/RESEARCH_NOTE.md).

**Proved analytically:** the robust partial-certificate frontier in an explicit
three-state, two-receiver game with both action components active; the different
perfect-gate threshold when eligible types lose support; the scalar-profile
identity without KL; upper-image composition at retained shared interfaces.

**Numerical evaluation:** at κ=.3 and the specified payoffs, the optimum symmetric
gate is γ≈.68287062. The controlled fine is ≈.22436269. A partial certificate with
cost k<.3 raises it to .8. For k=.4 the fine limit as γ↑1 is ≈.94068, but the
perfect gate needs 1.8. These numbers refer to the NEW game, not the earlier
binary benchmark.

**Counterexamples:** separate type punishments, nonattained minimum, discarded
coupling, wrong budget query, coordinatewise resource minima, non-KL Markov
gluing, convexification of credible Nash payoffs, and arbitrary joint beliefs for
two independently informed senders. All are small explicit mathematical examples;
several have exact rational computational checks.

**Evidence:** 36 direct 12-cell optimization comparisons (max gap ≈3.06e−12),
200 random feasible laws, 304 continuation checks, 72 exact finite feasibility
queries, exact χ² and nonconvex examples, and six narrow Lean lemmas. Source hashes
bind the retained numerical/Lean output. Numerical agreement is not formal proof.

**Prior-art correction:** KLT's January 2026 signaling paper already gives joint
interim payoff upper sets and a multiple-receiver extension. Koessler–Skreta's
June 2026 paper explicitly uses common payoff vectors and consistent normalized
likelihoods. Set optimization/valuation algebra already supplies the general
composition operations. Treat the present frontier as a worked specialization;
no novelty has been established. The 2005 Forges–Koessler full-text gap remains.

**Bounded extension:** ordinary finite-network elimination follows with complete
interfaces. A rank-one posterior obstruction blocks an automatic multiple-sender
equilibrium extension. A general multiple-sender frontier remains unproved and
was not substituted for the requested first three results.

**Next experiment:** asymmetric three-state prior, certificates {1,2} and {2,3},
and exact continuation-support enumeration. Separate support changes from changes
in equilibrium feasibility before extending to strategic networks.

**Git/preservation:** separate additive folder; historical research and external
inputs preserved. Main remains e3a6a92. Continued the uncommitted research phase;
no branches, commits, pushes, roadmap rewrite or engineering transfer in this run.
