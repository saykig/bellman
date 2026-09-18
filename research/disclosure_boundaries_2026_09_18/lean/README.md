# Fixed-information disclosure game: formal assumption audit

Lean 4.33.1 and Mathlib revision `0df444a360eaa60ab8c11dca51a86af692955474`
checked [DisclosureGame.lean](DisclosureGame.lean). The source-bound
[result.json](result.json) reports 14 axiom inspections, with only standard
`propext`, `Classical.choice`, and `Quot.sound`; no sorry axioms or compiler warnings.

## What was proved

The file starts with three states, three policy actions, actual pure utilities,
probability distributions, expected utilities and best responses. It proves the
closed expected-payoff formula rather than assuming the threshold as a game axiom.
It then derives all mixed policy deviation bounds, the absence of C at low fine,
both-type sender necessity, and explicit half/half and C/C equilibria. These give
`pooling_iff`, the exact disjunction e≥b/2−c OR k≥η/2−v together with on-path obedience.
The formal result only needs c,k≥0; the manuscript uses stronger economically
interpretable restrictions. Fine nonnegativity is imposed by the optimization,
not needed by this algebraic equivalence.

The operational game is defined separately and joined through additive payoffs.
`joint_br_iff` proves the separation of policy and operational best responses;
`operational_exists` constructs a common source-majority continuation.
`fixed_information_pbe_iff` combines the threshold with on-path operational
obedience, a valid conditional-source kernel and full-support prior. Pure joint
action deviations are included in `JointBR`; averaging their inequalities rules
out arbitrary lotteries over the six policy/operation pairs as well.

## Definition-to-game boundary

`AlgebraicPooling` allows arbitrary prior distributions. Its off-path witness only
requires posterior mass on types 1,2. It is NOT a valid full-game PBE predicate
at an arbitrary prior with absent eligible types. `FixedInformationPBE` explicitly
requires all three prior probabilities positive. `full_support_allows` proves
support consistency there; `zero_eligible_prior_rejected` prevents the wrapper
from being applied at one support-loss boundary. Positivity is a supplied premise,
not an empirically verified fact. The formalization does not certify Theorem I's
singleton or overlapping-certificate cases.

The wrapper is an explicitly defined finite pooling assessment: Bayes on-path
belief is the prior, off-path beliefs are supported on eligible types, receivers
best respond, and both eligible sender types prefer silence. No library of general
extensive-form games is imported. The interpretation as the stipulated PBE follows
by listing those finite-game conditions; that semantic translation is an author
audit, not a theorem about an independent extensive-game implementation.

`equal_posterior_tremble` proves that positive eligible prior weights permit valid
sender message probabilities giving posterior (1/2,1/2,0). The silence limit
lemmas prove the corresponding Bayes beliefs converge to the prior. These connect
the canonical witness to feasible sender perturbations. They do not establish
sequential equilibrium under a separately formalized sequence of fully mixed
receiver actions, nor formalize arbitrary off-path posterior selection.

The advocate sees the state but not the residual source uncertainty. Its utility
depends on receiver 1's policy only. `source` supplies P(S=positive|state) at the
fixed public history; evidence reweights states without changing that conditional
kernel. Neither this information restriction nor payoff additivity is inferred.

## Reproduce

Install the Lean toolchain with elan, and use a built Mathlib checkout at the exact
revision above, with its dependency packages available. Then run:

    python3 verify.py --packages /path/to/project/.lake/packages --lean lean > /tmp/disclosure-replay.json

The verifier checks the Mathlib Git identity and invokes the pinned Lean toolchain.
It uses existing compiled packages read-only; no cache or dependency tree is
vendored. Trusted compiled dependencies must correspond to that checkout. The
receipt binds the proof-source SHA-256; it does not attest the whole host or cache.

Continuity, KL optimization, the two-certificate menu and global robustness are
proved on paper and tested computationally, not formally verified in this file.
