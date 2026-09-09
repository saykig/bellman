# Research record — 9 September 2026

1. Verified current Bellman main/release v0.0.7 at 2cd6fd7; inspected current remote-main
   Decision Lab e5f77df and Writ 4e9b7f4 through their existing repositories. Writ's newer
   roadmap accepts ADR 0026/0028 and adds certificate transport; the older local checkout's
   proposed-ADR status is stale. No edits or checkouts in either downstream repository.
2. Shortlisted FSD3661 and Falk/Kosfeld E116246V1. Selected the first after acquiring actual
   CSV, variable labels, English instructions, version/reuse declaration and the full article.
   The alternative's one-shot design is less direct for remembered-experience comparison.
3. Fixed PLAN.md at d9c0075, pushed before any prediction fit/evaluation. Only source text,
   metadata/counts and first rows inspected before fixation. Original study published in 2022;
   results here are retrospective and not externally preregistered.
4. All eight Table 2 means reproduced within rounding; no missing selected cells or missing
   participant rounds. Projection intentionally excludes questionnaires and demographics.
5. Initial environment attempt used system Python 3.9, incompatible with chosen numerical
   package pins; used an existing Python 3.12 interpreter in a temporary environment instead.
   This affected no data, model, split or result. No language migration.
6. First fixed fit: return-history model MSE .0437885 vs erased-return model .0465680;
   persistence .0507234; training treatment mean .1489006. Retain all outcomes, including the
   particularly poor treatment-only baseline and inconclusive primary interval.
7. Independent receiver initially required the numeric Rank to stay constant. Data show slots
   2/3 swap within the stable sender role (e.g. ID 1). Corrected that invalid check to require
   only sender/recipient role stability. Producer always groups histories by ID and selects
   both sender slots, so no analysis, plan or result changed. Group-level flow identities
   independently verify both senders' transfers/receipts against their responder.
8. No row-level bootstrap/standard error is defensible here. Four held-out sessions are four
   independent evaluation units under the stated assumption; the 240 rows are not 240 independent
   replications. The attractive small-cluster bootstrap interval does not override the vacuous
   primary bound. No claim that disclosure mechanisms are empirically interchangeable.
9. Identification redirect: feedback visibility was never randomized. Sharp support-only
   bounds for hiding feedback are trivial even if the observable law were known perfectly.
   Retain two exact observational extensions, explicitly mathematical rather than fitted
   psychological explanations. Reject importing predictive evidence as a causal successor.
