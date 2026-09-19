# Prior-art audit: revise the contribution claim downward

18 September 2026. Read source statements, assumptions and proofs at the locations
below, rather than treating abstracts as theorem evidence. The strategic author PDFs, set-optimization PDF and Boyd slides were
retrieved and text-extracted locally; identities are in MANIFEST.json. Kohlas–Wilson
was read through the web PDF extraction; the local HTTP retrieval returned HTML. Private
paths, caches and full copyrighted PDFs are not retained here. This is a stronger
comparison than the prior run, not an exhaustive priority determination.

## Closest strategic predecessors

**Koessler–Laclau–Tomala, [A belief-based approach to signaling](https://drive.google.com/file/d/1tOPbqJrWtDDtZNMC5fBfp4k2UjL8kwIe/view),
15 January 2026 author edition.** Read §2 pp.6–8; §3 pp.8–11, Theorem 1 and its
surrounding construction; §§7.1–7.2 pp.27–30. Their INTIR condition is already a
joint upper image of credible interim payoff vectors. The theorem additionally
uses constrained convexification in beliefs for on-path signaling. §7.1 discusses
verifiable evidence via reasonable-belief restrictions; §7.2 explicitly replaces
a single receiver's best responses by multiple receivers' mixed Nash equilibria.

Assessment: the earlier one-sender joint-deterrence criterion is an elementary
pooling specialization of this established logic, with eligibility restrictions
and a fixed target. It should NOT be sold as a new general characterization.
Our restricted two-message protocol needs no on-path posterior splitting. We
prove its continuation and budget calculations directly. The robust three-state
fine/cost formula is a solved example inside this broader theory, not a replacement.
The paper's flat convexification does not authorize an arbitrary convex hull of
Nash continuations at one fixed message.

**Koessler–Skreta, [Informed communication equilibrium](https://drive.google.com/file/d/1LDie6EXqrksQYja4fM5eLVg2T7OGNcpn/view),
2 June 2026 author edition.** Read belief consistency Eq.(2), pp.9–10;
Definition 6 and Theorem 1, pp.12–13, including the proof. A SINGLE normalized
likelihood vector supplies consistent off-path updating. INTIR compares the
principal's entire payoff vector to ONE silent-game equilibrium vector; it does
not select a separate equilibrium for each principal type.

Assessment: strong prior art for precisely the common-witness concern. Their
principal chooses a communication device and participants may ignore it. Our
advocate selects a cost-bearing restricted certificate that physically excludes
states. Consequently their all-device theorem is not a literal formula for our
frontier; the payoff-vector discipline already exists. Private receiver information
also explains why arbitrary receiver-by-receiver posteriors would be unjustified.

**Forges–Koessler (2005), [Communication equilibria with partially verifiable types](https://doi.org/10.1016/j.jmateco.2003.12.006).**
The publisher abstract/introduction and description of canonical certification
outcomes were read in the prior run. Renewed attempts at the CORE PDF and the
old institutional path did not recover the full 2005 paper. Do not claim a full
subsumption audit of its Theorems 3.1–3.2. The much closer accessible 2026 signaling
paper above independently settles the key originality concern. A retrieval gap
is not evidence of novelty.

**Other retained baselines.** The previous [source notes](../../information_incentives_2026_09_18/sources/NOTES.md)
cover Saas's disclosure-proof CE, Milgrom–Roberts, certifiable pre-play
communication, linked-game BCE and spillover constraints. They remain relevant;
none is rerepresented as newly inspected in this run. In particular there is no
claim that private signals, evidence incentives or information spillovers are new.

## Closest mathematical predecessors

| Source and inspected location | Consequence for the proposed bridge |
|---|---|
| Boyd–Vandenberghe, [author slides](https://stanford.edu/~boyd/cvxbook/bv_cvxslides.pdf), slide 3.23, partial minimization | Convexity of a cost value function is standard. Our exact feasibility identity requires attainment at the boundary; convexity itself is optional. The elementary minimizer proof is supplied in PROFILES.md. |
| Hamel–Heyde–Löhne–Rudloff–Schrage, [Set optimization](https://arxiv.org/pdf/1404.5928), §2.1 Propositions 2.1–2.2 and Eq.(2.1); §2.3 Examples 2.5 and 2.11 | Upper-set equivalence, union/intersection and Minkowski addition already provide the proposed joint-budget algebra. Their later closed/convex variants have extra hypotheses; our exact finite feasibility statement deliberately takes neither closure nor convex hull. This is a specialization, not a new composition calculus. |
| Kohlas–Wilson (2008), [accepted manuscript](https://cora.ucc.ie/bitstreams/f41f5bb0-d690-4690-89a4-a9164f4cc832/download), §2 Example 5; §3 combination/projection; §4 Theorem 6 | Scalar min-plus elimination and relational combination/projection already belong to valuation algebra. Cost addition is not idempotent conjunction of evidence. Theorem 4's network corollary is standard elimination once the full shared interface is warranted. |
| Csiszár–Shields and Wainwright–Jordan, exact locations in the previous source notes | KL I-projection and junction-tree identities justify the previous specialized entropy calculation. Neither grants the same Markov minimizer for arbitrary divergences; our exact χ² example refutes that extrapolation. |

## Subsumption verdict and a tractable paper question

Three levels must stay separate:

1. **General mathematics already exists.** Scalar partial minimization, joint
   upper images, relational projection and valuation elimination cover the bridge.
2. **General strategic discipline already exists.** Interim payoff vectors and
   consistent beliefs are explicit in close primary predecessors. Retaining one
   credible continuation across types is not a new principle.
3. **This note's contribution is a transparent worked specialization.** It solves
   the specified robust three-state frontier and exposes its support discontinuity,
   with exact assumption failures and reproducible checks. This audit has not
   established priority even for that special formula.

A viable question is narrower: for finite public certificate games under a
shared convex information budget, which boundaries of source support and
continuation-equilibrium feasibility govern discontinuities of the minimum robust
fine? Our three-state example gives a solvable starting case. Existing parametric
optimization and equilibrium-correspondence results should be the first baselines.
Do not call this a novel theorem until those comparisons and less symmetric cases
are worked through. Adding more senders solely to escape known theory is rejected.
