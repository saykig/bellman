# Public-tag history reduction: bounded research review

8 September 2026. Author analytical/adversarial review of the additive PR #22 component.
The exact source commit, byte identities and executable observations are bound by
`verification/history_reduction/results.json`; this document does not claim external
peer acceptance or formal verification. The prior reviewed head is
`eb44e580fe137c50d9c92ea2b284cf0e5d3d90e9`.

## Claim examined

The previous consistency component had no mathematical blocker in the independent
review. A faulty live reproduction link warranted correction. More generic hardening
of that same claim was not justified by a concrete defect. The user explicitly chose
to add the next specified history-reduction question on this same PR.

The new question is deliberately narrower than arbitrary history compression:
erase an initial public tag whose positive-probability branches are identical copies
of a supplied continuation game, profile and assessment. A public tag can be a
strategic device even when payoffs ignore it; invariance of the specified assessment
is essential. No equality of complete source/target strategy spaces is asserted.

## Proof audit

For each tag and information set, explicit tree and information bijections preserve
the available continuation plans and every conditional suffix factor. This proves
all continuation-value equalities, rather than only equality of the retained maxima.
Taking maxima gives identical modelwise and worst-family gains. The ex-ante value and
erased terminal law follow by summing the positive tag weights.

Bayes numerators and denominators in each public copy share the same strictly positive
root factor. It cancels for every completely mixed profile. Copying a common target
sequence proves one direction; restricting a source sequence to one fixed tag across
all models proves the other. The source sequence need not itself be invariant between
copies. Removing large coefficients in other copies can increase the target positivity
radius, which must be recomputed. The power-witness specialization follows directly.

Perfect recall and the inherited chance-reachability restriction are checked on both
subjects. The theorem concerns given assessments. Neither a source equilibrium that
uses the tag for coordination nor an incompatible quotient receives this theorem.
At positive tolerance, no exact-equilibrium claim is made.

## Established mathematics and tool choice

The argument uses exact conditional game isomorphism and elementary Bayes cancellation,
composed with the existing common-power consistency result. This is not a novelty claim.
Kroer and Sandholm's [2014 abstraction paper](https://www.cs.cmu.edu/~sandholm/extensiveGameAbstraction.ec14.pdf)
was inspected for its tree mappings and equilibrium-quality framework; their
[2018 framework](https://papers.nips.cc/paper_files/paper/2018/hash/aa942ab2bfa6ebda4840e7360ce6e7ef-Abstract.html)
provides broader context. Neither is cited as establishing arbitrary off-path assessment
transport. The [Aumann 1974 publication](https://doi.org/10.1016/0304-4068(74)90037-8)
identifies the established correlation literature; the elementary matching counterexample
here is derived and checked directly. Access to its publisher metadata is not represented
as a full-text theorem audit.

Existing exact rational continuation evaluators and SymPy polynomial receiving are reused.
No new game solver or polynomial engine was written. There is no current Rust/JuMP/Lean
escalation trigger: this short proof can be reviewed directly, and no new optimization
bottleneck or durable cross-repository checking deployment is claimed.

## Adversarial cases and receiving

The matching counterexample has source matching probability one but marginal-product
target matching probability one half. Both supplied profiles have zero gain; the map
fails profile invariance. Thus payoff irrelevance and zero deviation gain do not by
themselves preserve the outcome law.

The likelihood counterexample keeps root utility and zero gain while changing the
conditional type priors between public copies. A valid source witness gives posterior
one half in each copy, but its unjustified restriction gives one quarter in the target.
The map rejects the conditional chance mismatch; independent target receiving rejects
the mismatched belief. Another target witness remains valid. This falsifies transport,
not target equilibrium existence.

The new receiver shares declarative structural validation with its candidate constructor,
but imports neither the transfer constructor nor either prior producer. It independently
receives both consistency warrants, checks the exact witness restriction, compares all
continuation rows, and re-evaluates root utilities. A temporary receiving deployment
contains only the three receivers and their structural validation dependencies.

Retained checks include the 127 -> 63 node integrated example, profitable-deviation
preservation, tolerance rebinding rejection, alternate representative choice, unequal
source coefficients, model-dependent tag probabilities, map and identity tampering,
missing continuation queries, changed off-path assessments, and both counterexamples.
Normal and optimized Python observations must agree. Exact counts and results are in
the source-bound result record. These checks are conformance evidence, not a formal proof.

## Preservation and boundary

Every earlier mathematical source, substantive review, fixture, result, release note
and manifest is byte-preserved. Six existing living/workflow files are explicit exceptions.
Inherited causal/history/strategic acceptance runs at its correct source identity after
that current-tree comparison; old runners are not patched to approve new scope.

The result is suitable for retention as a bounded research component. The strongest
remaining limitation is deliberate: identical continuation copies with an invariant
assessment are restrictive. Intermediate observations, approximate likelihood transport,
all-equilibria preservation, general quotient construction and empirical credibility
remain unsupported. The next step should start from a concrete observation whose removal
matters, then determine which of these restrictive premises can be relaxed safely.
