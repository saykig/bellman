# PR12 support-contract and CI acceptance hardening

**7 September 2026. Additive maintenance record; no new mathematical stage.**

Reviewed PR12 head: `fbfbc182a05952198d9ce9dc6ef4e9a395eaf3c6`.
Pinned PR10 merge: `2e8d99cdcf289eabb63df15086eaa68251a359f1`.
Reviewed PR10 head: `82d286c591750a2229664d935a6f9820340233df`.

The mathematical companion and original `results.json` at the reviewed head are frozen. Their
SHA-256 identities are checked by the maintained runner and recorded separately in
[`acceptance_hardening_results.json`](acceptance_hardening_results.json).

## Receiver support contract

The reported mismatch reproduces. `produce_interval` refuses 129 observations and 65 requested
precision bits, and `produce_decision` refuses five actions. At the reviewed head the corresponding
receiver routes accepted manually authored certificates. Those certificates are mathematically
valid; acceptance contradicted the public executable support profile.

The repair keeps one shared request profile:

- at most 128 observations;
- at most four actions;
- at most 64 requested precision bits.

The precision field gives a producer 64 dyadic search iterations at most and independently asks a
receiver to check bracket width against `2^-b`. These are separate operations with the same bounded
request limit. Receiver refusal occurs after request validation but before evidence inspection,
binomial-tail evaluation, or affine-risk evaluation. It returns `status=unfinished` and
`kind=resource-refusal`; it is not statistical rejection, infeasibility, or mathematical
invalidity. Within the supported request profile, malformed evidence still rejects. Exact derived
`Fraction` coordinates remain uncapped, including the retained 298-bit control and an added
598-bit-or-larger boundary control.

Direct controls cover hand-authored evidence at 129 observations, five actions, and 65 requested
precision bits. Positive controls cover 128 observations, four actions, 64 requested precision
bits, zero observations, an exact rational root, a coarse valid interval, nontrivial evidence, and
large derived proof coordinates. Disabled tail, interval-consumer, and risk helpers establish that
the declared early refusals do not reach expensive arithmetic.

## Live checks and historical replay

The legacy family-replanning workflow invoked its whole-base historical preservation runner on the
current PR. That runner correctly describes its historical execution but cannot classify later,
authorized living roadmap and architecture changes; direct use therefore produced a permanent red
job ending at `historical change: docs/programme/ARCHITECTURE.md`.

The maintained workflow now routes live acceptance through
`verification/statistical_decision_bridge/run_checks.py`. That entry point:

1. runs current statistical, family-replanning, and persistent-family checks normally and with
   `-O`;
2. executes the complete unchanged PR10 historical runner in a disposable clone at the exact PR10
   merge, including its inherited chain;
3. verifies the reviewed PR10 tree and current inherited source identities;
4. checks the frozen PR12 companion and original result identities;
5. permits only named PR12 repair, living-document, ledger, and workflow paths relative to the
   reviewed PR12 head.

Disposable negative controls confirm that an authorized programme-document update passes the path
policy, while protected mathematical source/result mutation, an intentionally failing current
mathematical check, and a missing or malformed historical replay fail. No corrupted fixture or
duplicate execution log is retained.

## Unchanged guarantee and limits

D1–D15 and their scope are unchanged. The all-real-parameter simultaneous coverage statement
remains conditional on a complete IID Bernoulli stream with one fixed real parameter. Outward
rational enclosure, exact affine action comparisons, complete minimizer sets, strictness/ties,
named-action regret, revision semantics, and conditional applicability remain as stated in the
companion. This repair does not validate the IID premise, add adaptive or multistream sampling,
create a posterior, prove a sequential-control rule, establish empirical usefulness, confer
authority, or modify Writ or Decision Lab.
