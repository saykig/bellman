# Bounded source and software review

Inspected 2026-09-09. This review stops at the finite one-observation question;
no further data fitting or data collection was performed.

- Bellman `foundations/BELLMAN_WRIT_MATHEMATICAL_SUBSTRATE_V1_1.md` §7 supplies
  comparison by state-independent garbling and the need for an explicit joint
  law. SPEC.md derives only the finite, same-prior, same-loss, cost-free one-way
  implication. Blackwell (1951), *Comparison of Experiments*, Berkeley Symposium
  pp.93–102, and Blackwell (1953), *Equivalent Comparisons of Experiments*,
  [DOI](https://doi.org/10.1214/aoms/1177729032), are the foundational references.
  The original full paper could not be retrieved in this session; no claim to
  inspect its general proof or borrow its converse is made. The specialized
  finite derivations here are explicit and need no general theorem black box.
- Decision Lab existing commit `e5f77dfcf929708951f4673b3f394461ef09c752`:
  actually inspected SPEC.md, solver.py, checker.py, consumer.py, decode.py and
  identity.py, and executed the finite-one-observation API. Uses Fraction, exact
  Bayes sums and independent enumeration, with 1–8 states/actions, 1–6 signals,
  ≤4096 policies. Perfectly suited to each supplied channel. It does not rank a
  menu, validate empirical inputs or optimize ambiguous priors. The menu bridge
  is proved here; no arbitrary composition inferred from its result format.
  The repository is private, and no LICENSE/COPYING was found at the pinned
  edition. No public redistribution licence is asserted. Source remains an
  external user-owned dependency, accessed read-only and never vendored.
- [OpenMarkov users](https://www.openmarkov.org/users.html) documents a Java17+
  graphical-model tool and explicitly states that the bundled sensitivity
  plugin is free but not open-source. Its
  [tutorial, chapter 6](https://www.openmarkov.org/docs/tutorial/openmarkov-tutorial.pdf)
  describes deterministic/probabilistic parameter sensitivity, including
  second-order distributions. That is not an exact independently checked
  finite menu interface. Documentation was examined; no binary or code execution
  was performed and no package-wide licensing inference is made. It adds no
  demonstrated benefit over the already inspected exact engine for this task.
- AFY (2024), author paper and instructions already inspected in the retained
  `research/beliefs_2024/SOURCES.md` and IDENTIFICATION_AUDIT.md: current-action
  reports occur after own action, before feedback. This does not establish a
  pre-action counterfactual-response channel or the supplied utility measurement.
  Those frozen findings remain the empirical motivation, not fitted design inputs.
- Dal Bó and Fréchette (2019), *Strategy Choice in the Infinitely Repeated
  Prisoner's Dilemma*, AER109(11),3929–52:
  [paper §I](https://gfrechette.com/print/Dal_Bo_2019a.pdf),
  [appendix A, printed pp.37–38](https://gfrechette.com/print/Dal_Bo_2019a_oa.pdf).
  The instructions elicit initial and previous-action-contingent plans. Plans
  are initially nonbinding; in a later phase they control play and cannot be
  revised. This supplies a concrete protocol precedent for contingent responses,
  while also distinguishing elicitation from commitment. It does not calibrate
  our .51/.55 channels, identify this utility mixture, or establish no effect of
  our proposed measurement. No raw data from this paper was acquired or fitted.

The bounded protocol gap is therefore specific: neither inspected AFY protocol
nor that contingent-plan protocol establishes the joint premises needed for this
particular forecast/utility/cost comparison. This is not a universal claim that
no suitable experiment exists. A new empirical campaign is outside authorization.
No Lean, Rust or optimization backend is needed for this finite exact operation;
existing code and a small transparent checker settle it. No Foundry, ASCE,
Isabelle, product interface or general inference framework was added.
