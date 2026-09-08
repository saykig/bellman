# Research-history migration checks

Run from the repository root with the existing Python runtime:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verification/history_migration/checks.py
PYTHONDONTWRITEBYTECODE=1 python3 -O verification/history_migration/checks.py
```

The checker binds the four moved records to their exact PR12-merge bytes and permits only the
deterministic relative-link transformation required by the new directory depth. The findings and
substrate records may then receive append-only current entries without changing the migration
manifest's frozen transformation identity. It requires the old root paths to be absent, validates
strict duplicate-free UTF-8 JSON manifests, recomputes every
release target date and tree from Git, hashes every committed release note, and hashes every selected
artifact from its historical target commit. If a proposed tag later exists, it must resolve to the
manifest's exact target commit.

Current certificate preservation runners import the same moved-record check. Their pinned replay
still executes unchanged code at its historical commit; current orchestration recognizes the
reviewed moves without treating mathematical sources or frozen results as living history files.

This validates repository identities and the declared transformation. It is not formal verification
of the summarized mathematics, independent reproduction of historical experiments, or proof that
mutable GitHub release text still matches the committed note. The committed note and manifest remain
the canonical comparison source.
