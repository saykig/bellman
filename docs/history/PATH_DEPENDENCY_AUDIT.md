# Ledger-path dependency audit

This audit records the complete disposition of references to the four former root filenames at the
history-migration head. It distinguishes current navigation and execution from historical text.

| Reference group | Classification | Disposition |
| --- | --- | --- |
| `README.md` and `verification/substrate_v1/README.md` | current maintained documentation | Repointed to `docs/history/`; the root README now has one history entry. |
| `verification/sequential_certificates/run_checks.py`, `certificate_transport/run_checks.py`, `certificate_accumulation/run_checks.py`, `persistent_model_families/run_checks.py`, `family_replanning/run_checks.py`, and `statistical_decision_bridge/run_checks.py` | current maintained executable/CI dependency | Repaired to use the reviewed migration checker. Frozen historical bytes are read from their original commit paths; current records are checked at their explicit destinations. |
| `verification/history_migration/checks.py` and the record migration manifest | current maintained executable/CI dependency | Intentionally name both old and new paths to prove absence, exact origin bytes, reviewed relocation, and link-only transformation. |
| `reviews/PR4_REVIEW.md` | historical prose | Left unchanged. Its advice accurately named the ledgers as they existed when that review was written. |
| Links and text inside `docs/history/records/` | current maintained documentation preserving historical records | Same-file sibling references remain valid; plain historical filenames remain accurate. The migration/classification files intentionally name the old records to bind and audit them. |
| `docs/history/README.md` | current maintained documentation | Names only the canonical moved paths as the detailed record index. |
| `verification/statistical_decision_bridge/run_checks.py` path authorization | current maintained executable/CI dependency | Intentionally names old deletions and new destinations so PR12 frozen evidence stays protected while this one reviewed migration is accepted. |

No current consumer opens a former root path. Historical runners checked out at their pinned commits
remain unchanged and continue to see the layout for which they were written. Searches will continue
to find the old filenames in the migration proof, the moved records themselves, and the preserved
PR4 review; these are intentional and are not live root-path dependencies.
