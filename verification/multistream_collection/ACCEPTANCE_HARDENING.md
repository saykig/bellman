# PR #14 acceptance hardening and current-main synchronization

**7 September 2026. Additive repair record; no new mathematical stage.**

Reviewed pre-repair head: `f3d609b9b2b6aa10c283737cf04a0df58a6c948c`.
Original PR base: `92922ab6604840152ad7f7800969673335748272`.
Synchronization target: latest main after PR #15, `fc45c4fff0f2958450f7073b46b67b92cb306bb3`.

The [mathematical companion](../../foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md)
and original [`results.json`](results.json) remain byte-identical. The reviewed coverage theorem,
affine-box proof, and M1–M8 values were not changed. This record concerns public-constructor subject
binding, revision classification, and current repository-history acceptance.

## 1. Reproduced findings

### R1 — extra allocation identity was erased

Through `make_collection`, a two-stream registry A/B and caller table

```text
A -> 1/40, B -> 1/40, ghost -> 9/10
```

were accepted. The caller table summed to `19/20`, but dictionary lookup followed by registry-only
canonicalization silently discarded `ghost` and stored the apparently valid sum `1/20`. Direct
`CollectionRequest.validate()` already rejected the full table. Thus the public helper and typed
subject disagreed.

The repair validates pair shape and identity, exact-normalizes each allocation, rejects duplicate
keys, and requires the caller key set to equal the registry before canonicalization. A complete
reordered table remains accepted and is stored in registry order. Missing, duplicate, and extra
keys reject.

### R2 — extra affine coefficient was erased

For registered parameters A/B, the public decision helper accepted `safe` with risk zero and a
caller-supplied `risky` action with intercept `-1` and coefficients

```text
A -> 0, B -> 0, ghost -> 2.
```

It discarded `ghost`, reinterpreted `risky` as constant risk `-1`, and produced a certificate
naming `risky` as the sole common minimizer. Under the caller's supplied expression at
`ghost = 1`, its risk is instead `+1`, so `safe` is better. This is a material subject change, not
an ordering detail.

The repair validates the original `AffineAction` before conversion, requires its weight identities
to equal the registered parameter identities, and only then canonicalizes. Complete signed,
zero-valued, exact weights in arbitrary order remain accepted. The hostile action now rejects
through both direct validation and `make_decision` and cannot reach a producer or receiver.

### R3 — provenance changes were classified as ordinary reuse

At the reviewed head, an unchanged transcript with a changed record identity, revision identity,
or predecessor digest returned `same-transcript-recalculation-no-new-evidence`. A longer prefix
with either the old revision identity or a different record identity could return
`append-only-transcript-extension` when its predecessor digest happened to match.

The repaired classification order is:

- changed registry, population/protocol identity, premise, or rule:
  `new-collection-subject`;
- changed alpha allocation, precision, or joint/cross-stream premise:
  `new-coverage-specification`;
- identical subject, transcript, record, revision, and predecessor:
  `same-transcript-recalculation-no-new-evidence`;
- strict prefix growth with the same record, a genuinely new revision, and the exact predecessor
  digest: `append-only-transcript-extension`;
- an otherwise unchanged transcript or prefix extension with altered/missing lineage:
  `provenance-changed-new-claim`;
- non-prefix correction or retroselection:
  `corrected-or-retroselected-transcript-new-claim`.

This classifier records a provenance disposition. It does not validate physical sampling or make
a corrected/retroselected history valid.

## 2. Current-main synchronization and history layout

Current main was merged into the existing PR branch without rewriting history. PR #13's current
`AGENTS.md`, migration classification, and canonical `docs/history/records/` layout were retained.
PR #15's versioned release notes, manifest, and lightweight-tag checks were then retained when it
became the latest main. The two PR #14 ledger additions moved to
[`FINDINGS_LEDGER.md`](../../docs/history/records/FINDINGS_LEDGER.md) and
[`SUBSTRATE_LEDGER.md`](../../docs/history/records/SUBSTRATE_LEDGER.md), with only the required
relative-link repairs. The obsolete root ledger paths remain absent.

The history migration checker still binds the migration manifest to the exact PR #12 baseline and
reviewed relative-link transformation. It now correctly treats the findings and substrate records
as append-only after that frozen transformed prefix; the other two moved records remain
byte-identical. This prevents a valid current history append from being mistaken for corruption
without weakening the migration identity.

This repair creates no GitHub Release and does not alter PR #15's published prereleases. It is not
a newly accepted research-state transition and does not warrant a release note under the current
repository policy.

## 3. Frozen evidence and acceptance routes

The protected PR #14 identities are:

| File | SHA-256 |
|---|---|
| `foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md` | `be495f29011479adab2736bfbe8f3c3e513403fa48c4886652e8137256d1ccbc` |
| `verification/multistream_collection/results.json` | `2b80b11c691be1c297e71bd2c7016c837a3584389748d42ec06c377bf2da7a93` |

The original result remains a hosted record of source commit
`fdf83a0b2f3b31331ed894fa0d0aeeffea07db00`; it is not relabelled as evidence for repaired code.
The new `acceptance_hardening_results.json` separately records the repaired hosted run.

The maintained runner executes, normally and with `-O`:

- the repaired PR #12 scalar checks;
- the unchanged M1–M8 multistream checks against the repaired reference;
- the constructor/revision controls R1–R3;
- current family-replanning and persistent-family preservation checks;
- current PR #13 migration and PR #15 version/release checks.

It also runs the unchanged PR #12 acceptance program at exact repaired head
`5017122500450c8f7f890474f7232b9c94d3a3fb` in a disposable clone whose `origin/main` is bound to
the historical PR #10 merge `2e8d99cdcf289eabb63df15086eaa68251a359f1`. That supplies the
complete inherited PR #10 replay in its original context. Negative controls reject mutation of
the protected companion/result, a deliberately failing current check, a missing historical
commit, malformed replay output, and a wrong historical base.

## 4. Remaining boundaries

The repair establishes exact public subject coverage for fixed allocation keys and affine weight
keys. It does not validate IID sampling, reveal concealed outcome filtering, validate corrected
histories, provide adaptive alpha allocation or dynamic registries, correct arbitrary missingness,
optimize a bandit policy, compose the rectangle into sequential control, or authorize action. It
adds no Writ/Decision Lab change, language migration, formalization, or reopened experiment.
