# Kahneman Lab

Kahneman Lab is a research repository for bounded, falsifiable, and reproducible experiments on uncertainty, information, belief, decision, and action.

The repository is deliberately separate from Writ. Kahneman Lab tests mathematical claims. A result moves into Writ only after it is replicated, identifies a concrete representation or operation that Writ needs, and survives a separate product-level justification.

## Record discipline

- Preregistrations, sealed inputs, lane reports, referee reports, and syntheses are frozen artifacts.
- Frozen artifacts are never edited in place. A correction or reinterpretation is added as a new, explicitly labelled artifact.
- Preregistered findings, post-hoc findings, replications, failures, and conjectures remain distinct.
- Exact source bytes and SHA-256 digests are retained where available.
- Existing mathematics fully explaining a result is an acceptable outcome.
- No architecture or product claim follows merely because a mathematical result is interesting.

## Repository map

- [`FINDINGS_LEDGER.md`](FINDINGS_LEDGER.md) — short cumulative record of what survived, failed, or remains untested.
- [`experiments/kl4/`](experiments/kl4/) — complete frozen KL4 preregistration, four lane reports, and synthesis.
- [`experiments/kl5/`](experiments/kl5/) — frozen KL5 preregistration only. KL5 has not been executed.
- [`LEGACY_ARCHIVE_STATUS.md`](LEGACY_ARCHIVE_STATUS.md) — status of the earlier KL2–KL3 migration.

## Current research question

The current bounded question is not whether one special architecture outperforms competent analysis. It is:

> What information must a representation preserve for a declared class of downstream decisions, especially when information acquisition is sequential?

This question may be settled entirely by established Bayesian decision theory, value-of-information analysis, dynamic programming, POMDP/belief-state results, and finite sufficient-statistic theory. Kahneman Lab should report that outcome plainly if it occurs.
