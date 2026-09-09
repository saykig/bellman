# Correction: maintenance inspection selects run / service / service

2026-09-09. Additive correction to FINDINGS.md at 1c35622, second-case policy
sentence. The original report is preserved. The original machine-readable
maintenance-result.json is correct and unchanged. Read this correction with
[SPEC.md](SPEC.md), [FINDINGS.md](FINDINGS.md), [SOURCES.md](SOURCES.md) and
[REVIEW.md](REVIEW.md); it supersedes only the reported red-signal action.

The noisy inspection's signal-only optimal policy is **run after green, service
after amber, and service after red**. The report incorrectly said replace after
red. This was caught by independently expanding the red joint expected losses:

| Action | Green joint loss | Amber joint loss | Red joint loss |
|---|---:|---:|---:|
| Run | 22/25 | 66/25 | 172/25 |
| Service | 647/200 | 321/200 | 79/25 |
| Replace | 327/25 | 171/25 | 102/25 |

Each entry is sum_s p(s)K(x|s)L(a,s), before the fixed measurement fee.
Red has mass 17/100; its service conditional risk is 316/17, below replace's
24. The minimum joint losses sum to 1129/200; adding cost 2/5 gives 1209/200.
The net benefit 8 - 1209/200 = 391/200 and all measurement rankings are unchanged.
The perfect inspection still selects replace in the known major-fault state;
that does not justify replacing after the noisy red observation.

This correction illustrates the distinction between diagnosing a likely state
and choosing an action at its posterior. It changes no theorem or input and does
not add an empirical claim. Both cases remain stipulated studies. The preserved
public checker already verifies the returned branch action sets by joint losses;
the original discrepancy was in prose, not the executable reference. Later
acceptance binds this correction while retaining the original report and receipt.
