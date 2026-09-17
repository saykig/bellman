# Primary-source notes and claim map

Accessed 2026-09-17. Notes are selective, not an exhaustive literature review.
HTML conversions occasionally corrupt notation; use the mathematical definitions,
not malformed displayed indices. No third-party summaries establish our claims.

| Key | Primary work and inspected locator | What is used; limit |
|---|---|---|
| SS | Shenoy & Shafer (1990), [Axioms for Probability and Belief-Function Propagation](https://www.glennshafer.com/assets/downloads/articles/article43.pdf), §3.1 axioms A1–A3, §3.2 Proposition 2 | Associative/commutative combination, transitive marginalization and distributivity permit local elimination of a supplied factorization. They do not establish that arbitrary evidence factors may be multiplied. |
| KS | Kohlas & Schmid, [Commutative Information Algebras: Representation and Duality Theory](https://arxiv.org/html/2012.15090), §2.1 conditions N,A,Q,C; §2.4 examples | Idempotent information aggregation and extraction differ from probability multiplication. Their commutative domain-free profile is a specified class, not every notion called an information algebra. |
| AB | Abramsky & Brandenburger (2011), [The Sheaf-Theoretic Structure of Non-Locality and Contextuality](https://arxiv.org/html/1102.0264), §§2–3, §4.4.1, Theorem 8.1 | Compatible local empirical distributions can lack a global extension. The theorem equates a global section with a factorizable hidden-variable realization in its measurement setting; it is not an identification theorem for arbitrary SCMs. |
| AC | Abramsky & Carù (2019), [Non-locality, contextuality and valuation algebras: a general theory of disagreement](https://arxiv.org/html/1911.03521), §§2.3, 3.1, 4.2–4.3; Theorem 4.1; Proposition 5.1 and Appendix A.3 | Explicit existing valuation/presheaf bridge. Restriction supplies a presheaf, not a general combination law. For adjoint valuation algebras, extension is characterized by projecting the combination back. Our T1 proves the relational instance directly. Ordinary probability product must not inherit this relational criterion without its hypotheses. |
| F | Fong (2013), [Causal Theories: A Categorical Perspective on Bayesian Networks](https://arxiv.org/html/1301.6201), §2.3 Definition 2.11; §§4.1–4.2; [author errata](https://arxiv.org/abs/1301.6201) | Stochastic maps compose by integration; typed causal diagrams separate syntax and interpretation. In our finite specialization integration is summation. Errata specify words as objects, swaps, and strong symmetric monoidal functors. No arbitrary feedback operation is borrowed. |
| P | Pearl (2009), [Causal inference in statistics: An overview](https://escholarship.org/uc/item/6d71p32b), §3.2.3, Corollary 1, equation (17), [PDF mirror](https://www.cs.columbia.edu/~blei/fogm/2018F/materials/Pearl2009a.pdf) | Truncated factorization follows from replacing mechanisms in a Markovian model. The supplied causal premises matter; observational conditionals do not alone establish intervention semantics. One mirror fetch failed; indexed primary PDF passages supplied the equation and its surrounding explanation. |
| RW | Rischel & Weichwald (2021), [Compositional abstraction error and a category of causal models](https://proceedings.mlr.press/v161/rischel21a/rischel21a.pdf), Definitions 2.2–2.5, footnote 1 | Finite DAG mechanisms and intervention laws are sufficient for the paper's single-regime questions; counterfactuals are excluded. Maps between whole models include observation and intervention maps. Composing these abstractions is different from wiring two mechanisms. |
| LT | Lorenz & Tull (2026), [Causal and Compositional Abstraction](https://arxiv.org/abs/2602.16612) | Abstract-level screening only: query-indexed and component-level abstractions are close prior work for the proposed next question. Full text was not successfully inspected here. No theorem from this preprint is assumed, and novelty assessment remains open. |

Interpretation: AC already supplies a direct bridge between the first two
candidates. F, P and RW supply established finite causal semantics. Bellman's
immediate need is an explicit representation mapping and retained assumptions,
not evidence of a missing universal mathematical theory. The exact finite
results in this folder are elementary specializations, not priority claims.

Search scope: valuation propagation; information idempotence; contextuality and
valuation algebras; finite stochastic causal composition; causal abstraction.
A future paper review should add database acyclicity/join dependencies and credal
network literature, particularly separately specified versus coupled mechanism
sets. This first note proves its finite claims without relying on uninspected
results in those literatures.

Later access and scope update: see [PRIOR_WORK_ADDENDUM](PRIOR_WORK_ADDENDUM.md)
for inspected LT full-text sections, database join dependencies, credal-network
separability, and the resulting narrower paper question.
