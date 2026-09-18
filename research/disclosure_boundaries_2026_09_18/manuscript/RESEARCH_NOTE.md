# When information changes the fine needed to sustain silence

Research note, 18 September 2026. Author-derived mathematics with a bounded Lean
check; no external review or novelty certification.

A small change in information can make a previously adequate fine inadequate.
But “the information becomes perfect” is not by itself an explanation. A jump
requires a change in what can credibly discourage disclosure, or another failure
of the feasible choices to vary continuously. This note isolates these mechanisms
in a three-state, one-sender game and then tests the limits of that explanation.

## The bounded question and model

Two receivers choose policies A, B or C and a binary operational action. A fine
penalizes policies other than the target C. A privately informed advocate can stay
silent, disclose a certificate proving the state is in {1,2}, or—when eligible—
one proving it is in {2,3}. Type 2 chooses one certificate, not both. Certificates
are public, and receivers have no private information. The advocate benefits from
receiver 1's policy, with different preferred policies in states 1 and 2.

The source has three correlation parameters x_z, an asymmetric positive prior p,
and a shared information budget Σp_z F(x_z)≤κ. Here F(x) is the information in a
uniform binary pair of correlation x, measured in nats. A binary gate has accuracy
(1+γ)/2: γ=1 is perfect. The full convex family of budget-feasible sources is
admitted. Players know the source law; the analyst selects one fine that supports
some pooling equilibrium for every possible law. Continuations may depend on the
known law. This quantifier is weaker than implementing one equilibrium when the
law is unknown to the players.

The complete utilities, definitions and proofs are in
[Theorem I](../math/INFORMATION_THEOREM.md) and the
[model supplement](../math/MODEL_DETAILS.md). Payoffs and disclosure costs are
held fixed for the first theorem. We restrict attention to operationally feasible
gates, strictly positive priors and κ<log 2. Outside operational feasibility the
required fine is infinite; that is a separate failure.

## Exact information-only answer

Let C be the minimum fine if the advocate is forced to remain silent. It is a
continuous function of prior, gate and budget: the source family varies
continuously, posterior denominators remain positive, and its defining maximum
is over a compact set. Let

    a=b/2−c, H=b−c, t=η/2−v, T=η−v,
    κ12=min(p1,p2)log 2, κ23=p3 log 2,
    κC=(1−max(p1,p2))log 2.

Here b rewards a receiver's state-preferred policy, c rewards agreement, η is an
advocate's preferred-policy benefit and v its target-policy benefit. Assume
b>2c>0 and η>2v>0. The message costs are k12,k23≥0.

While both eligible types remain possible, E12 requires either e≥a or k12≥t.
This is a simultaneous constraint: one continuation must deter both types. E23
can instead be deterred by a continuation believing state 3. If information rules
out one of E12's types, or rules out state 3 for E23, the remaining certificate can
reveal a type whose preferred policy requires the larger fine H to dislodge.
A message cost at least T already deters that disclosure.

**Theorem I.** The robust minimum fine is H if

    γ=1 and [(κ≥κ12 and k12<T) or (κ≥κ23 and k23<T)].

Otherwise it is max(C,a) when k12<t, and C when k12≥t.
Consequently it is discontinuous in the information parameters exactly when the
condition above holds AND κ<κC. These are necessary and sufficient conditions,
not merely candidate boundaries.

The last restriction matters: for κ≥κC the controlled fine already equals H, so
support loss cannot raise it. Support change is necessary but not sufficient.
With fixed payoffs and a fixed support region, admissible off-path posterior
simplexes and receiver games are unchanged. There is no independent
information-induced continuation-equilibrium bifurcation in this model.

For p=(1/5,3/10,1/2), b=2,c=1/5,η=1,v=1/5, the thresholds are
κ12≈.139, κ23≈.347, κC≈.485, with H=1.8. At κ=.3 and both message costs .4,
E12 produces a jump at the perfect gate. At κ=.4, k12=.9,k23=.4, E23 produces it.
At κ=.55, the same support loss is masked. These claims follow from the exact
threshold inequalities; numerical curves are corroboration.

If the designer also chooses γ, it can select the least operationally feasible
gate, which is strictly below one. The optimized gate/fine value is continuous
throughout this domain. A discontinuity at a supplied perfect gate therefore
need not survive the actual design problem.

## The broader classification and its limits

Allowing every numeric parameter to vary within this payoff family gives four
continuous branches selected by two flags: whether E12 needs its partial-evidence
fine, and whether a harmful singleton certificate can require H. **Theorem F**
says continuity holds precisely when every phase approachable at the parameter
has the same limiting value. Its proof is finite subsequence analysis. This
classifies support boundaries, cost/payoff thresholds, their intersections and
masking; see [the full theorem](../math/FULL_BOUNDARIES.md).

Three small counterexamples prevent overgeneralization:

- **Incentive threshold:** with no informative source, changing k12 through .3
  changes the minimum fine from .8 to zero. Receiver equilibria and supports
  remain unchanged. This belongs to the second layer, not the information-only
  test.
- **Missing information-set regularity:** admit only two source laws, zero and
  (−.8,.8,−.8), by the same budget test. At the second law's admission threshold,
  with γ=.8 the fine jumps from zero to exactly 99/155. Every state likelihood
  remains positive and the disclosure continuation conditions are unchanged.
  The admissible-law set has abruptly expanded. Thus support loss and equilibrium
  changes are NOT an exhaustive classification for arbitrary information families.
- **Equilibrium persistence:** in a changed receiver-payoff family, a benign
  disclosure response B ties a profitable response A at δ=0. For δ>0 only A is
  optimal until the fine reaches 1+δ. The minimum is zero for δ≤0 and 1+δ for
  δ>0, despite unchanged support and costs. Some equilibrium always exists; the
  particular deterrent continuation disappears. This is a small witness, not a
  claim of globally minimal game size.

A general regular-region result, **Theorem R**, follows from compact parametric
optimization. Continuous admissible-law and continuation correspondences make
the worst violation continuous. Closed feasible-fine sets then give lower
semicontinuity of the minimum. Recovery of arbitrarily near-optimal feasible
fines under nearby parameters gives the other direction; strict slack is a useful
sufficient condition. Equilibrium existence alone supplies neither persistence
nor sender incentive slack. This uses established value-continuity mathematics,
including the feasible-path criterion discussed by
[Feinberg, Kasyanov and Kraemer](https://arxiv.org/pdf/2109.06299v1).

## Foundation, evidence and next question

Use constrained parametric optimization over credible continuation-payoff sets
as the foundation for this bounded question. Belief-based signaling already
supplies the common-witness incentive logic; see
[Koessler, Laclau and Tomala](https://drive.google.com/file/d/1tOPbqJrWtDDtZNMC5fBfp4k2UjL8kwIe/view).
Communication discontinuity classifications also have substantial prior art,
including [Lipnowski, Ravid and Shishkin](https://elliotlipnowski.com/wp-content/uploads/PWI.pdf).
The [source audit](../sources/NOTES.md) separates these baselines from this game's
explicit formula. No new universal framework is needed or claimed.

The analytical proofs establish the boundary statements under the listed premises.
[Experiments](../experiments/README.md) compare 56 optimizations of the original
joint probabilities against the reduced formula, with maximum discrepancy below
2.05×10⁻¹⁰; one unsuccessful solver status remains visible. Exact rational checks
verify the catalogue witness. These are tests, not proofs of continuity.
[Lean](../lean/README.md) verifies a fixed-information, one-certificate threshold
from payoffs and mixed best responses, including operational separation and a
full-support wrapper. It does not verify the global continuity classification or
the overlapping-menu theorem. None of these artifacts validates the human model.

For Bellman, preserve the entire feasible-law and credible-payoff correspondences,
the shared-witness quantifiers, support restrictions, tie-selection rule and the
identity of the varying parameter. A single optimum or support label loses the
information needed to diagnose a jump. No Decision Lab or Writ transfer is earned.

One tractable paper question remains: **for finite public evidence games over a
continuous compact source family, when does optimizing an available noisy gate
remove every support-driven discontinuity of the robust minimum fine?** This
example answers yes because low-fine deterrence is constant across positive
supports and control costs increase with gate informativeness. Those special
properties must be tested rather than assumed in a broader theorem.

The next experiment should keep one sender and three states, alter only the
receiver payoff table so E23 is nontrivial even at full support, and search for a
deterrent-equilibrium switch that survives joint gate optimization. Retain common
continuations across eligible types. An exact counterexample or a recovery
criterion would decide the next theorem; more dimensions and strategic networks
would not resolve the present obstacle.
