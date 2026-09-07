# Bellman/Writ Mathematical Substrate v1 — Adversarial Review

## Disposition

**Retain the foundation; make a focused v1.1 clarification. Continue the existing Build 1 implementation unchanged.**

This is an audit of the supplied substrate and its accompanying summary, not a new experiment, a novelty review, an implementation of Bellman, or authority to reopen KL5/KL6. No repository changes were made.

The central conditional mathematics is coherent. I found no fatal contradiction in its stated core Bayesian, Bellman, policy-transfer, or elementary error-composition arguments. I did find one consequential ambiguity between exact model sets and outer approximations, and several conditions that should become explicit before an implementation relies on the broader guarantees. The accompanying summary drops a loss-domain restriction present in the actual document.

These findings call for contract clarification, not a new architecture or another frontier-search prompt. Established mathematics is the intended foundation and is entirely sufficient as a basis for continued Bellman work.

## 1. What was actually inspected

I read the full supplied substrate and pasted summary, checked their inherited-source hashes against the mounted files, reviewed the displayed mathematical arguments, compared the proposed substrate with the supplied Build 1 contract, and wrote a separate fixed-case exact-arithmetic review harness.

The harness completed **20 test methods with no failures or errors**, under Python 3.13.5. It includes the 12 numerical Build 1 fixtures, two explicitly specified inherited horizon-two models, all 38 deterministic stopping policies through horizon two for a fixed two-action/two-outcome profile, and targeted demonstrations of invalid premise-dropping. It uses normalized and unnormalized recursions plus direct policy evaluation. These methods share the reviewer, literal inputs, and Fraction arithmetic; they are not independent authors or formal proofs.

No observation-model grid, historical experiment, candidate-representation search, or new holdout was executed. The extra fixed examples are review/conformance examples, not experimental discoveries. A passing review test sometimes means that an intentionally invalid inference was correctly shown to fail; it does not mean production software has implemented that refusal.

Focused external checks included JMLR's approximate-information-state Definition 7, Theorem 9 and the relevant proof; the AER publisher's reveal-or-refine statement; the cited May 2026 dynamic-signal manuscript's definitions and theorem; and scope records for proper value equivalence and approximate causal abstraction. This was not an independent full-proof audit of every cited publication. In particular, no full independent reconstruction of the historical KL6 injectivity proof was attempted in this review.

### Provenance check

All four source digests claimed by the substrate match the mounted source bytes:

| Source | SHA-256 | Result |
|---|---|---|
| Bellman North Star | `e2f1f7180fdf05dcd5a1f899b0e2acaf5a64d2e2a0a64c0a6e6679239f8f6b46` | Match |
| KL6 V2 closure | `31a4fb8bfcfbb7e9c4753866628c7784bf769d560d6716e21e878d22bf3d47f2` | Match |
| Post-KL6 frontier audit | `6a01ca1e81da1d6ea1bc5899f20ebe8380c997693b17fff006719d6f357669bd` | Match |
| Next-axis audit | `b044e4b38df0d385d8a32af688a62ac0ea794f08f3c709743d7105680eecc010` | Match |

The inspected substrate digest is `af60646d0118dce72abc65d7440a4faf9e8ed305ca6ffefc00775cc84204bc22`. The complete local source manifest is included separately. Byte matching establishes source identity, not mathematical correctness.

## 2. What survives the review

### Conditional results are the right organizing unit

Substrate §2 separates a result, the assumptions supporting it, the intended query, the receiver's actual information, and the guarantee. It does not pretend that a probability establishes a preference, or that a mathematical optimum authorizes an action. This is a suitable organization for the requested foundation synthesis.

### The important mathematical types remain distinct

The document correctly distinguishes history, model-description, and observation compression; exact values, full minimizing sets, a common optimal action, and a common executable policy; statistical dependence, derivation ancestry, and causal mechanism; and fixed-model uncertainty versus nodewise adversarial choice. Those distinctions are substantive constraints on reuse, not decorative labels.

### The main bounds have the correct structure

Subject to the explicit conditions identified below, the coupling proof controls every common history policy by

`e_h = (L_max + h*c) min(1, h*d)`.

Taking minima over the same policy class gives optimal-value and forced-observation-value error at most `e_h`. Transferring an `eta_h`-optimal surrogate policy gives regret at most `2*e_h + eta_h`. The factor of two is justified by comparing both policy value and optimum. The root STOP/OBSERVE comparison needs only `e_h` when STOP risk is exact. These are not interchangeable claims.

The AIS recursion in substrate equation (20) agrees with the cited JMLR Theorem 9 under that theorem's premises. This verifies the attribution and formula, not the existence of a usable AIS instance in Bellman.

### Elementary composition rules are sound under their specified premises

The Lipschitz error rule, uniform whole-policy error chaining, contraction of total variation through a stochastic simulator, and finite union-bound coverage rule are appropriate. Model compatibility and guarantee applicability remain separate requirements. A posterior normalization cannot generally discard a factor needed for a later evidence probability or model-weighting query.

### The source-summary relationship is mostly faithful

The pasted summary does not claim a completed implementation or an end-to-end formal proof. Its central interpretation matches the substrate. The material exception is the approximation loss-domain simplification discussed in Finding 2.

## 3. Required clarifications

### Finding 1 — Exact compatible models and conservative outer sets must not share an unqualified compatibility conclusion

**Location:** substrate §2.1, lines 65–70; §5, equations (10)–(12); §10.2, equation (28), especially lines 543–556.

**Classification:** consequential cross-section ambiguity, not a refutation of equation (28) for exact model sets.

Section 2 permits the compatible-model object to be either the actual fiber or a sound outer set. Section 10 subsequently says that a nonempty joint set establishes compatibility. That is correct for the exact stated constraints. It does not establish compatibility of the original constraints when the intersection was calculated only from outer approximations.

Fixed example:

- Exact constraint A allows only `p = 1/4`.
- Exact constraint B allows only `p = 3/4`.
- A sound outer approximation to A is `{1/4, 1/2}`.
- A sound outer approximation to B is `{1/2, 3/4}`.

The exact intersection is empty, but the outer intersection contains `1/2`. That point satisfies neither original singleton constraint. Calling it a compatibility witness would be false.

**Required amendment:** distinguish the semantic fiber `Fibre(s,B)` from a certified outer enclosure `U_plus(s,B)`, with `Fibre(s,B) subseteq U_plus(s,B)`. Then state:

- An empty outer joint enclosure can establish inconsistency, provided the enclosure relation is justified.
- A nonempty outer enclosure establishes only that the relaxation is feasible. Exact compatibility remains unestablished unless an actual witness satisfying the original constraints, or another existence proof, is available.
- Uniform bounds over an outer set are sound for actual members, but membership and nonemptiness of the actual admissible set remain separate obligations.
- “Exactly sufficient” and “minimal error” relative to the outer set are not automatically necessary/minimal statements about the true fiber. They may be conservative.

This matters directly to cumulative knowledge: two coarse records must not appear mutually consistent merely because the distinctions proving their inconsistency were omitted. No new theorem is required to fix the issue.

### Finding 2 — Restore all domain restrictions on the approximation certificate

**Location:** substrate §4, equations (7)–(9); §6, equations (14)–(19); summary lines 65–86; Build 1 §3.

**Classification:** missing local domain predicates and a summary-level omission. The substrate's nonnegative-loss theorem is not disproved.

The substrate explicitly requires `0 <= L <= L_max` for its displayed coupling bound. The summary says only that terminal losses are bounded by `L_max`, which can be misread as an upper bound. Build 1 separately permits negative losses. These profiles are both legitimate but cannot be conflated.

A fixed counterexample to dropping the lower bound uses prior `(1/2,1/2)`, zero observation fee, losses

```text
[[-99, 1],
 [  1,-99]]
```

and channels `(k0,k1)=(0,1)` and `(1/100,99/100)`. Their one-observation optimal values are `-99` and `-98`, so the absolute difference is `1`. Their channel distance is `1/100`. Incorrectly using only the upper loss bound `L_max=1` would certify an error of `1/100`—a false certificate.

**Required amendment:** state `c >= 0`, `d >= 0`, `eta_h >= 0`, integer `0 <= h <= H`, and `0 <= L <= L_max` explicitly in the coupling profile. Restrict forced-observation values and margins to `h >= 1`; at `h=0` STOP is forced. Sum posterior-dependent quantities only over positive-mass observations rather than performing arithmetic on `NA`.

A signed-loss extension is possible: with known `L_min <= L <= L_max` and `c >= 0`, shifting every terminal loss by `-L_min` yields the conservative range `(L_max - L_min + h*c)`. This is an elementary specialization, not permission to add approximate functionality to Build 1. The smaller amendment is simply to keep the existing theorem's narrower domain explicit.

Nonnegative fees also cannot be left implicit. With `L_max=1`, `h=1`, `c=-2`, and `d=1/10`, the printed expression gives a negative “error bound.” Negative fees are outside the intended profile.

### Finding 3 — A transferred policy must handle every history possible under a covered model

**Location:** substrate §2.1 decoder requirement; §4 impossible branches; §6 equations (16)–(18).

**Classification:** make the existing “common implementable policy” premise operationally explicit.

A surrogate can give probability zero to an outcome that a compatible original model gives small positive probability. The original-model policy-value guarantee is meaningful only when the transferred policy is defined at that outcome.

Fixed example: a surrogate channel never emits `x1`; the true channel emits `x1` with probability `1/100` in state 1 and zero in state 0. With prior `1/2`, that supposedly impossible outcome actually occurs with probability `1/200`.

A surrogate posterior there remains undefined. That does not prevent a total history policy from having a predeclared feasible response. But a missing branch, runtime crash, or unmodeled refusal is not a policy whose bounded loss has been proved.

**Required amendment:** require the policy/lift to be defined on the union of relevant history supports across the compatible models. Alternatively impose a support condition ensuring the surrogate filter is defined there. A declared fallback may be valid, but it is an operational policy choice, not a fabricated posterior or a claim of conditional optimality. Its loss must be included in the policy being bounded.

Do not require engineering to implement this now: Build 1 is an exact, supplied-model calculator. This is a prerequisite for a later approximate transferred-policy profile.

### Finding 4 — Exact surrogate mathematics and approximate solver output need different error accounting

**Location:** substrate §6, equations (18)–(19), and §10.5.

**Classification:** existing exact theorem is sound; the computation-to-certificate bridge needs a displayed rule.

Equation (19) compares the exact surrogate forced-observation optimum with exact STOP risk. It must not be applied to an uncertified numerical estimate as though the estimate were that optimum. The `eta_h` term for whole-policy suboptimality is not automatically an error certificate for the forced-observation optimum.

If a supplied computation establishes

`abs(O_tilde - O_surrogate) <= xi_O` and `abs(R_tilde - R) <= xi_R`,

then, by the triangle inequality,

`abs((R_tilde - O_tilde) - Gamma_true) <= e_h + xi_O + xi_R`.

Certify a strict sign only when the resulting interval excludes zero. With exact rational evaluation of both optima, the numerical errors are zero.

A fixed misuse example has zero model error, true margin `-1/1000`, numerical margin `+1/1000`, and numerical error allowance `1/500`. Checking only the model error would incorrectly certify OBSERVE. Including numerical error correctly leaves the sign uncertified.

### Finding 5 — State what “a decoder exists” proves and what still has to be supplied

**Location:** substrate §2.1 and §5, equation (11).

**Classification:** precision improvement, not an error in the ordinary fiber-constancy theorem.

Constancy on exact fibers establishes that an answer map factors through the representation as a mathematical function. Without further effective-representation assumptions it is not itself a proof that the receiver has an executable decoder, or that determining applicability is algorithmically feasible. In a genuinely finite, explicitly enumerated domain a lookup can provide a decoder, but that is a separate construction with its own cost.

The document already warns that the criterion is not an economical encoding or construction algorithm. Strengthen that warning into separate obligations: semantic sufficiency; an available decoder; and evidence that its premises hold for the claimed use. Do not invent a universal solver or require formalization of all seven components at once.

## 4. Edge cases the document already handles correctly

These are confirmations of existing safeguards, not newly discovered deficiencies.

**Shared evidence and residual dependence.** With a common prior, common signal C of accuracy `3/4`, and conditionally independent additional signals of accuracies `2/3` and `4/5`, three positive signals yield posterior `24/25`. Multiplying the two shared-C posteriors without removing C gives `72/73`. When the two residual signals are actually the same signal, the correct result is `6/7`, while the unjustified residual-independence formula yields `12/13`. Equation (4)'s qualification is essential and is present.

**Standalone sufficiency versus joining.** For a fair hidden bit and an independent fair bit, the fair bit and its XOR with the state are individually uninformative but jointly reveal the state. Dropping either based on standalone predictive value loses a potentially decisive distinction. Section 7 correctly requires the joint context.

**Pairwise consistency versus a global model.** Fair binary pair laws asserting X=Y, Y=Z, and X!=Z agree on shared singleton marginals but admit no joint model. The substrate's global-extension requirement is correct. This is different from Finding 1's exact-versus-outer-set problem.

**Rare conditioning.** Two channels can differ by only `1/10000` per row while a common rare outcome has posterior state-1 probabilities `1/3` and `2/3`. Its mass is `3/20000`. Section 6 correctly declines to promote an ex ante bound to a uniform conditional guarantee.

**Action changes with small regret.** In a fixed near-boundary one-observation example, the true optimum observes and the surrogate stops, yet the transferred-policy regret is only `1/1000`, within the conservative certified bound `1249/50000`. The margin interval contains zero, so no strict common action is certified. Small regret is not exact action preservation.

**Fixed model versus resampling.** If a fair choice between an always-zero and always-one channel is made once, the probability of two ones is `1/2`. Independently averaging/resampling the channel at each step gives `1/4`. The substrate explicitly prohibits silently exchanging those models.

**Randomization changes robust optimization.** For common zero-one loss and two possible point-mass priors on opposite states, every deterministic immediate action has worst-case loss 1, whereas a private fair mixture has worst-case loss `1/2` when Nature chooses the model before seeing that randomization. Build 1's deterministic-policy reference is valid for its known-model linear expectation; it must not become a default for every later robust profile. The substrate permits declared randomization and does not currently make that invalid extension. For notation, randomized policies are measurable action-distribution kernels, or actions measurable after augmenting information with the permitted private random seed.

**A preserved minimum need not preserve minimizers.** Costs `(0,1)` and `(1,0)` have the same optimum 0 but opposite optimal actions. Likewise, `{0,1}` and `{1,2}` have a common optimum without identical minimizing sets. Both distinctions are correctly retained.

**Causal action coverage.** Preserving the law and cost of a mapped action does not preserve the optimum if the correspondence omits another action with lower loss. The substrate correctly requires the action/intervention mapping and cost conditions.

## 5. Engineering alignment

Build 1 is a narrow exact instantiation, not an implementation of the seven-component substrate.

Its mapping is straightforward:

- `model.json` supplies the prior and labeled observation kernel.
- `query.json` supplies the actions, losses, unit and one-observation cost.
- The mathematical profile is the finite, known-model, at-most-one-observation specialization of substrate §4.
- The solver and checker evaluate the numerical instance through different arithmetic routes.
- `check_and_load` binds the answer to the consumer's intended original bytes and requires fresh checking.
- Unsupported sequential, robust, causal, fusion or approximate guarantees remain unsupported.

The mathematical substrate need not restrict all future mathematics to this first profile. Conversely, the implementation must not claim the rest of the substrate merely because its files mention it.

Important profile differences are intentional: Build 1 allows negative losses; the printed coupling theorem requires nonnegative losses. Build 1 writes JSON `null` for undefined conditional quantities; the mathematical document uses `NA`. Build 1 retains all minimizers and treats byte-identical inputs differently from merely mathematically equivalent inputs. These differences need explicit correspondences, not a redesign.

The final substrate statement that a checker must distinguish arithmetic correctness from premise applicability should not be interpreted as requiring Build 1 to establish real-world source reliability, causal assumptions, or statistical independence. It checks formal input well-formedness and exact arithmetic under the supplied profile. Empirical model adequacy remains a declared limitation.

## 6. The next mathematical work

The useful continuation is a **small operational refinement** of the existing mathematics, not more mathematical breadth. Make the above changes in v1.1, then bind the exact one-observation profile to the equations and the already-specified Build 1 tests.

A compact readiness annotation would help:

- Explicit finite rules that a named implementation profile can evaluate.
- Referenced general theorems whose application requires additional instantiated premises.
- Provenance/correction conventions proposed by the synthesis, not themselves mathematical proofs or implemented workflow guarantees.

This is not a new universal schema, feature request, or extra implementation gate. Keep theorem statements, executable instances, and empirical model warrants distinguishable.

A worked handoff should show a calculation, its premises, a later permitted reuse, and a rejected reuse after a changed input. The existing Build 1 fixed sequence already supplies the relevant channel, loss, cost, action-menu and tampering changes. Reuse those definitions rather than inventing another experimental domain.

**Do not expand the component list, re-run closed KL experiments, require an original theorem, or pause Build 1 while rewriting the synthesis.**

## 7. Confidence

High confidence in the specific outer-set counterexample, the premise-dropping counterexamples, the checked scalar identities and fixed examples, and the basic Build 1 alignment.

High confidence in the inspected AIS formula and reveal-or-refine attribution within their cited scopes. The dynamic source is identified by its actual May 2026 manuscript version, not promoted here to a publication claim.

Moderate confidence that this seven-component organization is the best long-term organization. No exact study or theorem establishes that it is uniquely optimal. Its usefulness should be judged through defined operations and reuse.

Not established: end-to-end formal verification, automatic checking of arbitrary model compatibility or empirical assumptions, a running general Bellman system, broad interoperability, or real-world decision improvement.

**Bottom line:** this is useful foundation-building. Retain the substance and correct the interfaces. The most consequential amendment is preventing an outer approximation from masquerading as an exact compatibility witness.

## Sources and companion evidence

Primary supplied document: `BELLMAN_WRIT_MATHEMATICAL_SUBSTRATE_V1(1).md`, especially §§2, 4–7, 10–14. Accompanying summary: `Pasted markdown(20260907-012508).md`. Engineering alignment: `RUN_THIS_NEXT_WRIT_ENGINEERING_BUILD_1(1).md` and `writ_engineering_direction(1).md`. Exact input identities are in `source_manifest.json`.

Focused external sources:

1. Subramanian, Sinha, Seraj and Mahajan (2022), *Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems*, JMLR 23(12), Definition 7 and Theorem 9. Inspected PDF pp. 15–17, including rendered equations. `https://www.jmlr.org/papers/volume23/20-1165/20-1165.pdf`
2. Brooks, Frankel and Kamenica (2024), *Comparisons of Signals*, AER 114(9), publisher theorem summary. Full journal proof not reread in this audit. `https://www.aeaweb.org/articles?id=10.1257/aer.20230430`
3. Whitmeyer and Williams, *Strong Dominance for Dynamic Signals*, arXiv version 2, 17 May 2026. Inspected model, definitions and Theorem 2.5; no application experiment evaluated. `https://arxiv.org/html/2407.16648v2`
4. Grimm et al. (2021), *Proper Value Equivalence*, author abstract/scope record inspected, not the complete proof. `https://arxiv.org/abs/2106.10316`
5. Beckers, Eberhardt and Halpern (2020), *Approximate Causal Abstractions*, PMLR 115; proceedings scope record inspected, not the complete paper. `https://proceedings.mlr.press/v115/beckers20a.html`

The review does not treat a historical source hash or citation as independent verification of all that source's claims.

Companion files: `fixed_checks.py`, `fixed_check_results.json`, `fixed_check_log.txt`, and `source_manifest.json`. The scripts and results concern only this review. They are not the production Build 1 checker.
