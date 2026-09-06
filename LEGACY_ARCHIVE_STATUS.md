# Legacy Archive Status

The initial repository import freezes the complete, unambiguous KL4 chain and the KL5 preregistration.

KL2 and KL3 predate this repository structure. Their accessible legacy source set contains duplicate filenames, combined self-contained packets, embedded copies, private answer keys, and some outputs recorded as chat or pasted-text artifacts rather than uniquely named standalone files. Importing an arbitrary copy would falsely imply that the canonical source identity had been settled.

Accordingly:

- KL2–KL3 findings are indexed in `FINDINGS_LEDGER.md` for continuity.
- Their source artifacts are not represented as a complete repository archive yet.
- A separate migration should select the authoritative bytes using the hashes recorded in the later referee and synthesis packets, preserve private/sealed status labels, and document any artifact that cannot be recovered as an exact standalone source.
- No legacy source should be rewritten merely to make the archive look cleaner.

This is an archival limitation, not a scientific reinterpretation of KL2 or KL3.
