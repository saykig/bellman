# Sequential credibility research review and disposition

8 September 2026. Author adversarial mathematical/code review, not independent peer
review, human acceptance, empirical validation or formal verification. Reviewed draft:
`19e1904bfd96e8d0eb926ac630193b9f0b1d4265`, PR #22, base/main
`cea4e1a47cb91c1f3917490350deab53d2976908`. The draft had no posted GitHub reviews.
The [addendum](../foundations/BELLMAN_SEQUENTIAL_CREDIBILITY_CONSISTENCY_ADDENDUM.md)
is the corrected current scope; original mathematics, self-review and results remain frozen.

## 1. Adversarial disposition of the preliminary formulation

No counterexample was found to the draft's five propositions **under their stated
premises**. It correctly restricts its principal output to assessment-relative
sequential rationality. Its green fixtures do not establish consistency, a strategic
uncertainty preference model or a history-reduction theorem. These are capability
boundaries, not grounds to falsify its accurately limited finite arithmetic.

| Reviewed obligation | Finding and disposition |
|---|---|
| Definitions and quantifiers | Retain one profile for all models, then universal model/information-set/deviation checks. A failure witness can depend on m; an implemented profile cannot. Add an explicitly stronger common-sequence quantifier for consistency. |
| Pure continuation sufficiency | Finite path expansion is a convex combination of complete pure plans because no information set repeats on a path. The baseline behavioral continuation belongs to this convex hull, so best-minus-baseline is nonnegative. Do not extend this to maxmin preferences. |
| Information and recall | The validator compares each player's earlier information/action sequence across nodes in a set. Both evaluators share actions by information set. The union-of-subtrees plan is legitimate under perfect recall. Private type and own action erasure controls fail validation. |
| Beliefs and zero events | On-path Bayes is exact. Off-path supplied distributions may contradict each other. The J/K game gives zero draft deviation gain while requiring two different limits of the same posterior. New receiving checks a common limiting construction and refuses chance-impossible information sets. |
| Sequential equilibrium | Full continuation optimality plus consistent assessments supplies the standard modelwise conclusion at epsilon=0. Trembles need not be equilibria along the sequence. Neither positive epsilon nor a model-indexed collection of witnesses earns the shared exact-equilibrium label. |
| Representation proof | The 2-delta inequality is valid with complete deviation coverage and common conditional-value errors. A root payoff-error bound does not supply a conditional-value error at an arbitrarily rare information set. Renaming is not compression. Consistency preservation is an additional obligation. |
| Continuous proof | Multiplication by strictly positive reach is valid. The *unnormalized* inequality must be multi-affine; the conditional ratio need not be. Zero reach and repeated parameters remain excluded. No executable generic corner warrant was earned here. |
| Mechanism and participation | g-pb tests bonded compliance alone. The bond-5 and fee-3/2 controls show why all continuations and participation must be inspected. Fixed chance enforcement is an assumed technology, not an incentive-compatible monitor or institutional authority. |
| Checker independence | Old producer uses recursive utility, old receiver terminal paths; they share structure/arithmetic. New producer uses leading orders, new receiver full exact SymPy polynomials. Both candidate producers are absent from isolated receiving. Shared validation and libraries remain trusted. |
| Identity and query | Both layers bind the same subject. Receiving controls epsilon independently and fixes the common-sequence semantics. Outer rehashing cannot rehabilitate stale inner incentives. |

The original evidence manifest also binds the then-current README and living
programme documents. Updating those documents makes its direct current-tree
`--verify-retained` call fail, even while every frozen file and mathematical source
remains unchanged. The additive runner therefore reconstructs the exact draft tree
in a temporary directory and executes the unmodified retained runner there. This
preserves historical source identity rather than modifying old evidence or exempting
changed bytes. All Git access during that replay is read-only.

The draft's references to established packages were candidates, not capability
audits. This review inspects actual source and theorem statements before adding the
power-witness interface. It also keeps mathematical impossibility separate from
failure of a supplied witness or a bounded implementation.

## 2. Established mathematics inspected

**Sequential assessment consistency.** Kreps–Wilson's
[publication record](https://www.gsb.stanford.edu/faculty-research/publications/sequential-equilibrium)
locates the original distinction; attempts to retrieve its original PDF failed.
The working definition was checked in Dilmé's full primary text, not inferred from
that abstract. [Dilmé (2024), sections 2–4](https://link.springer.com/article/10.1007/s00182-023-00874-z)
states the common completely mixed limiting assessment definition, power-sequence
characterization and integer-exponent result. We inspected Definition 3.1,
Theorem 3.1, its proof setup and Proposition 4.2. The sufficient direction gives
the right small reference: exact positive leading terms determine off-path ratios.
The theorem allows real coefficients and unbounded integer orders; our rational,
order-at-most-32 input is not a complete implementation of the existence theorem.

**Robust games.** [Aghassi–Bertsimas (2006)](https://www.mit.edu/~dbertsim/papers/Robust%20Optimization/Robust%20Game%20Theory.pdf),
section 3 (especially the max-inf best response and Definition 3), and Theorem 2
on p.248, concern robust-optimization equilibrium in finite one-shot games with
bounded payoff uncertainty (that theorem has no private information). Existence
for that criterion does not give a profile optimal in every model. The draft's
L/R half-mixing counterexample exactly distinguishes the two quantifiers. No
recursive ambiguity model, model weights or rectangular worst-case switching is
imported from this result.

**Evidence and commitment.** [Hart–Kremer–Perry, 28 March 2016 author edition](https://math.huji.ac.il/~hart/papers/st-ne-201603.pdf)
of the later AER paper: sections 2.1–2.4, Theorem 2 (printed p.22), and Appendix B
specify the truth structure, truth-leaning requirements and payoff conditions
under which equilibrium and optimal commitment outcomes coincide. In particular,
single-peakedness is required for the principal's payoff under every type mixture.
The truth relation is reflexive/transitive; the refinement disciplines disclosure.
Bellman's post-acceptance effort, forfeiture and uncertainty family are not shown
to fit those assumptions. Therefore no commitment-equivalence or unraveling
theorem is imported. Evidence feasibility and enforcement incentives stay explicit.

**Game abstraction.** [Lanctot et al. (2012)](https://arxiv.org/pdf/1205.0622),
Definition 2 and Theorem 1, use terminal-history bijections preserving proportional
utilities/chance reach and relevant player/opponent action-information sequences.
Their result bounds average regret for CFR in a well-formed imperfect-recall game
relative to a perfect-recall refinement. Section 7 supplies failure cases when
structural conditions break. This is not a theorem about arbitrary supplied
off-path assessments or the new shared-sequence quantifier.
[Kroer–Sandholm's expanded author version](https://www.columbia.edu/~ck2945/papers/imperfect-recall-abstraction-with-bounds.pdf),
Definition 2.3 and Theorems 3.2–3.3, adds chance-relaxed skew well-formed conditions
and error terms for payoffs, transitions and information-set distributions. These
are substantive abstraction routes, but neither their root bound nor the draft's
renaming fixture proves Bellman's desired all-information-set consistency transport.
The preliminary citation's 2014 date refers to the arXiv origin; later versions
have a different publication history. No historical citation bytes were replaced.

**Symbolic equilibrium computation.** [Graf–Engesser–Nebel, AAMAS 2024](https://www.ifaamas.org/Proceedings/aamas2024/pdfs/p715.pdf),
sections 3–4, gives polynomial conditions for sequential rationality and consistency,
using approximate linear systems, polyhedral directions and real algebraic solving.
Theorems 8–9 and Propositions 10–14 address the off-path consistency problem rather
than ordinary root Nash regret. This is a relevant established complete-search
route. Our task is supplied-witness receiving, so we borrow exact polynomial
arithmetic and retain this solver as a future cross-check/search candidate.

## 3. Actual implementation inspection and reuse

| Implementation inspected | Actual capability and use in this task |
|---|---|
| [GTE-sequential at cba2f7c](https://github.com/tengesser/GTE-sequential/tree/cba2f7c75a64bc6759e3ad1754dc58aa8134bbc9) with [backend at c8a9588](https://github.com/tengesser/GTE-Backend/blob/c8a9588bae77c7913bcbb9233523336ecf1f44b0/sequential_solver/solver/solver.py) | Read actual consistency-matrix construction around lines 693–735 and `wolfram_solve_equations` around 936–975. Uses `pypolyhedron`, NumPy and Wolfram `CylindricalDecomposition` of generated conditions. Docker configuration requires Wolfram Engine licensing. No Wolfram runtime was available; no backend execution or comparison is claimed. Not reimplemented here. |
| [Gambit 16.6.0 at 1ce412b](https://github.com/gambitproject/gambit/blob/1ce412badec6edb5407d870b962c0c7ee4d68861/src/games/behavmixed.cc) | `GetBeliefProb` at lines 292–299 returns `nullopt` for zero-reach information sets. Its rational behavior representation can support candidate arithmetic; that API does not supply limiting beliefs. Inspected source and solver documentation, not an installed execution. A Nash/logit output alone is not a consistency certificate. |
| [OpenSpiel at 4840189](https://github.com/google-deepmind/open_spiel/blob/48401890ee9857e611678302371378175a8e4c6b/open_spiel/python/algorithms/exploitability.py) | Read `exploitability` and `nash_conv`: root best-response values and NumPy differences; the former requires two-player constant/zero sum. The latter's own information-state restriction is documented but not enforced there. These metrics do not check supplied off-path beliefs. No adapter or runtime comparison added. |
| [SymPy 1.14.0](https://docs.sympy.org/1.14.0/modules/polys/reference.html) | Installed and actually used `Rational`, `Poly(..., domain=QQ)`, exact polynomial products/sums and trailing terms. No numerical limit tolerance, custom polynomial engine or generated code evaluation is used. Exact symbolic identities also test the two impossibility arguments. The receiver and producer disagreeing on domain-sensitive polynomial equality exposed an initial QQ/ZZ comparison issue; it was corrected before retention. |

Only SymPy (with its pinned mpmath dependency) is borrowed into the reference. A
Wolfram deployment would add licensing/runtime costs without improving this bounded
supplied-witness query; complete equilibrium search would be a reason to revisit it.
Nothing here rules out wider capability elsewhere in Gambit or OpenSpiel.

## 4. Review of the new derivation and executable boundary

The normalization proof uses t<1/(1+C), not the unsupported assumption that arbitrary
power weights already sum to one. Supported-action multipliers tend to one. Their
higher-order polynomial terms cannot cancel a positive leading prefix coefficient.
The receiver expands those terms and independently recovers the same limiting ratios.
Fixed structural-zero histories are assigned zero mass and may be pruned without
removing an entire assessed information set. The modelwise equilibrium statement
uses this conventional fixed-chance interpretation, not perturbed chance laws.

Every receiving pass checks actual beliefs against the subject, not merely against
the producer's prediction. Positive nonunit coefficients matter (the weighted J/K
case has 1:3 likelihoods); equal-order default noise cannot reproduce the evidence
fixture's zero good-type off-path belief. Shared information/action keys prevent
node-specific or model-specific perturbations from evading those restrictions.

The two impossibilities quantify over **all** completely mixed sequences via
posterior identities derived from the actual small trees. They do not conclude
impossibility from a finite failed search. In the family example each individual
model admits a sequence, and the impossibility concerns only the common sequence.
The original J/K game still has other sequential equilibria.

Exact checks include the original integrated subject, weighted posteriors, fully
mixed baseline, partial structural zeros, unsupported entirely impossible information,
bond/fee changes, epsilon changes, full renaming, forgotten own history and 33
receiving rejection controls. Original checks (including maxmin, root-only and
costly-threat controls) replay unchanged. Normal and optimized observations agree;
158 tracked draft/inherited files are preserved, excluding only three living docs.
Detailed source-bound observations live under
[`verification/sequential_consistency/`](../verification/sequential_consistency/README.md).

## 5. Programme direction and assurance assessment

**Bridge earned:** a supplied rational power witness upgrades an assessed continuation
result to simultaneous modelwise sequential equilibrium when epsilon=0. This resolves
the constructive consistency-warrant gate beyond the preliminary draft. It does not
settle unrestricted consistency search, continuous model families or strategic prediction.

The most decision-relevant next history question is whether a specified information
reduction preserves both legal continuation values and the relative likelihood orders
and coefficients required by off-path assessments. Root-payoff abstraction guarantees
alone cannot establish that. Use the inspected abstraction results where applicable;
do not respond by generating bigger fixtures or an unrestricted history mapper.
A concrete continuous on-path query may instead justify the draft's restricted
multi-affine warrant. Neither frontier was silently declared earned here.

Lean was assessed against the repository's stable-foundation/material-assurance
trigger. The small positive-leading-term limit lemma is a possible later target if
many transports rely on it. Today the shared-family interface is new and no downstream
component relies on it; formalizing the full changing subject would cost more than
the added assurance. No Lean theorem/package coverage is claimed. Exact checks and
ordinary proof review meet the present bounded gate; language migration is not needed.

The causal inspection covered merged PR #20's g-formula and strong-support distinction,
and unmerged PR #21 at `deb58f612ab7b9ab22e08f2ce493527e63cf9cfb`, including its
saturated second-stage kernel fibre, multi-affine argument and restriction boundary.
Those premises are not strategic response laws. Its branch was not modified and its
unmerged results are not dependencies. No Writ or Decision Lab files were changed.

Disposition: retain the new result as an M1 checked research reference and leave PR #22
unmerged for human review. No external peer acceptance, formal proof, empirical
validation, complete mechanism design or authority to act is claimed.
