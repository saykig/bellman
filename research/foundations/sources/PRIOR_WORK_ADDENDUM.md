# Bounded prior-work check and question revision

2026-09-17. Additive to NOTES.md: its LT abstract-only access status is superseded
by the successful PDF inspection below. This is a targeted check, not a systematic
review or a proof that no prior paper answers the proposed question.

**LT — Lorenz & Tull (2026).** [Full PDF](https://arxiv.org/pdf/2602.16612),
§§3.1–3.2, Definitions 14–16, Proposition 17, Definition 46, Proposition 47 and
Theorem 51 (pp. 10–18, 33–38) were inspected. They explicitly treat open DAGs,
query-preserving abstraction and stronger component-level abstraction. Theorem 51
has structural and output-coverage hypotheses; it is not an arbitrary black-box
replacement rule. This removes any basis for presenting intervention-aware
component composition itself as the missing bridge. Our remaining issue concerns
sets of possible models and which dependencies can be forgotten, not a new
abstraction definition for a pair of specified models. Their result is relevant
pointwise; a uniform family-level mapping still needs checking.

**BFMY — Beeri, Fagin, Maier & Yannakakis (1983).**
[Author-associated IBM PDF](https://s3.us.cloud-object-storage.appdomain.cloud/res-files/500-jacm83a.pdf),
§1 p. 481 join dependencies; Theorem 3.4 pp. 488/492; conditions 7,9,10 and §6.
Exact recovery from projected relations is precisely a join dependency. Join-tree
and running-intersection criteria already characterize when pairwise consistency
universally gives global consistency. T1/T2 here are elementary specializations,
not new results. This settles exact model-set preservation; it does not require
interpreting attributes as observed physical variables. Mechanism-choice
attributes qualify equally well. A weaker query-specific preservation target
should be stated explicitly if exact recovery is unnecessary.

**RC — Rocha & Cozman (UAI 2002).**
[Inference with Separately Specified Sets of Probabilities in Credal Networks](https://arxiv.org/pdf/1301.0597),
§§2–3, Example 3, Definitions 3–6; §6.2 Proposition 1 and Theorem 3. Inspected PDF;
2013 is the arXiv upload year. Coupled versus independently concatenated choices
are already a substantive issue. Their strong-extension and separable-elimination
results use specified independence/separability semantics. Our finite unweighted
catalogue is not automatically their convex credal set: convexification changes
attainable laws, even when it preserves extrema of a linear functional. Their
separable-message guarantee cannot be imported after silently deleting coupling.
No claim is made to have surveyed all later causal credal-network work.

**Revision to the research judgment.** Existing mathematics suffices for the
immediate Bellman representation: relations over mechanism choices, standard
causal evaluation, and extension tests. The proposed paper should be a bounded
synthesis/algorithmic study of *query-relative* dependency retention, not a new
unified foundation. Database lossless join is a sufficient baseline. A causal
query map may identify distinct mechanisms, permitting more forgetting, but
individual query ranges need not preserve the set of answer vectors.

The new finite signature probe tests this last distinction. A failed signature
comparison may require a vector of several intervention answers as witness;
there need not be one scalar intervention answer outside its old range. This
qualifies the initial paper-question wording in DEVELOPMENT §7.
