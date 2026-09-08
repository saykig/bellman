"""Exact repository-history migration and historical-preservation checks."""

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MIGRATION_BASELINE = "92922ab6604840152ad7f7800969673335748272"
MOVED_RECORDS = {
    "FINDINGS_LEDGER.md": "docs/history/records/FINDINGS_LEDGER.md",
    "MATH_ARCHIVE_LEDGER.md": "docs/history/records/MATH_ARCHIVE_LEDGER.md",
    "SUBSTRATE_LEDGER.md": "docs/history/records/SUBSTRATE_LEDGER.md",
    "LEGACY_ARCHIVE_STATUS.md": "docs/history/records/LEGACY_ARCHIVE_STATUS.md",
}
APPEND_ONLY_RECORDS = {"FINDINGS_LEDGER.md", "SUBSTRATE_LEDGER.md"}

# Existing files changed only to govern or execute this reviewed layout migration. Mathematical
# sources, frozen evidence, result records, reviews, and experiment artifacts are deliberately absent.
CURRENT_MIGRATION_PATHS = {
    "AGENTS.md",
    "README.md",
    "verification/substrate_v1/README.md",
    "verification/sequential_certificates/run_checks.py",
    "verification/certificate_transport/run_checks.py",
    "verification/certificate_accumulation/run_checks.py",
    "verification/persistent_model_families/run_checks.py",
    "verification/family_replanning/run_checks.py",
    "verification/statistical_decision_bridge/run_checks.py",
}


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def strict_json_bytes(data, label):
    def no_duplicates(pairs):
        result = {}
        for key, value in pairs:
            need(key not in result, f"duplicate JSON key in {label}: {key}")
            result[key] = value
        return result

    try:
        text = data.decode("utf-8", errors="strict")
        return json.loads(text, object_pairs_hook=no_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"invalid JSON in {label}") from error


def git_bytes(root, commit, path):
    try:
        return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=root)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(f"historical path unavailable: {commit}:{path}") from error


def relocated_bytes(old_path, data):
    if old_path not in {"FINDINGS_LEDGER.md", "SUBSTRATE_LEDGER.md"}:
        return data
    text = data.decode("utf-8", errors="strict")
    for prefix in ("experiments/", "foundations/", "reviews/", "verification/"):
        text = text.replace(f"]({prefix}", f"](../../../{prefix}")
    return text.encode("utf-8")


def verify_moved_records(root=ROOT):
    manifest_path = root / "docs/history/records/migration_manifest.json"
    manifest = strict_json_bytes(manifest_path.read_bytes(), str(manifest_path.relative_to(root)))
    need(manifest.get("migration_baseline") == MIGRATION_BASELINE,
         "record migration baseline mismatch")
    entries = manifest.get("records")
    need(isinstance(entries, list) and len(entries) == len(MOVED_RECORDS),
         "record migration manifest entry mismatch")
    by_old = {}
    for entry in entries:
        need(isinstance(entry, dict), "invalid record migration entry")
        old_path = entry.get("old_path")
        need(old_path in MOVED_RECORDS and old_path not in by_old,
             f"unknown or duplicate moved record: {old_path}")
        by_old[old_path] = entry
    need(set(by_old) == set(MOVED_RECORDS), "moved record manifest is incomplete")

    identities = {}
    for old_path, new_path in MOVED_RECORDS.items():
        entry = by_old[old_path]
        need(entry.get("new_path") == new_path, f"wrong destination for {old_path}")
        need(not (root / old_path).exists(), f"old root record still exists: {old_path}")
        need((root / new_path).is_file(), f"moved record is absent: {new_path}")
        old = git_bytes(root, MIGRATION_BASELINE, old_path)
        new = (root / new_path).read_bytes()
        need(entry.get("old_sha256") == sha256(old), f"old record hash mismatch: {old_path}")
        migrated = relocated_bytes(old_path, old)
        need(entry.get("new_sha256") == sha256(migrated),
             f"migration-result hash mismatch: {new_path}")
        if old_path in APPEND_ONLY_RECORDS:
            need(new.startswith(migrated),
                 f"moved append-only record rewrites migration history: {new_path}")
        else:
            need(new == migrated,
                 f"moved record differs beyond reviewed link repair: {new_path}")
        identities[new_path] = sha256(new)
    return identities


def verify_release_manifest(root=ROOT):
    manifest_path = root / "docs/history/releases/manifest.json"
    manifest = strict_json_bytes(manifest_path.read_bytes(), str(manifest_path.relative_to(root)))
    releases = manifest.get("releases")
    need(isinstance(releases, list) and len(releases) == 6,
         "release manifest must contain the six audited milestones")
    tags = set()
    note_paths = set()
    artifact_count = 0
    for release in releases:
        need(isinstance(release, dict), "invalid release manifest entry")
        tag = release.get("tag")
        note_path = release.get("release_note_path")
        commit = release.get("target_commit")
        need(isinstance(tag, str) and tag.startswith("research/") and tag not in tags,
             f"invalid or duplicate research tag: {tag}")
        need(isinstance(note_path, str) and note_path.startswith("docs/history/releases/")
             and note_path.endswith(".md") and note_path not in note_paths,
             f"invalid or duplicate release note path: {note_path}")
        need(isinstance(commit, str) and len(commit) == 40, f"invalid target commit for {tag}")
        tags.add(tag)
        note_paths.add(note_path)

        try:
            commit_date = subprocess.check_output(
                ["git", "show", "-s", "--format=%cI", commit], cwd=root, text=True).strip()
            tree = subprocess.check_output(
                ["git", "rev-parse", f"{commit}^{{tree}}"], cwd=root, text=True).strip()
        except subprocess.CalledProcessError as error:
            raise RuntimeError(f"release target unavailable: {tag}") from error
        need(release.get("target_commit_date") == commit_date,
             f"historical date mismatch: {tag}")
        need(release.get("tree_sha") == tree, f"tree identity mismatch: {tag}")

        note = (root / note_path).read_bytes()
        need(release.get("release_note_sha256") == sha256(note),
             f"release-note identity mismatch: {tag}")
        note_text = note.decode("utf-8", errors="strict")
        required_lines = (
            f"Historical finalization: {commit_date}",
            f"Tagged commit: `{commit}`",
            f"Git tree: `{tree}`",
        )
        for line in required_lines:
            need(line in note_text, f"release note does not bind {tag}: {line}")

        artifacts = release.get("key_artifacts")
        need(isinstance(artifacts, list) and artifacts, f"release lacks key artifacts: {tag}")
        artifact_paths = set()
        for artifact in artifacts:
            need(isinstance(artifact, dict), f"invalid key artifact for {tag}")
            path = artifact.get("path")
            need(isinstance(path, str) and path not in artifact_paths,
                 f"invalid or duplicate artifact for {tag}: {path}")
            artifact_paths.add(path)
            need(artifact.get("sha256") == sha256(git_bytes(root, commit, path)),
                 f"historical artifact identity mismatch: {tag}:{path}")
            artifact_count += 1

        tag_ref = subprocess.run(
            ["git", "show-ref", "--verify", "--quiet", f"refs/tags/{tag}"], cwd=root)
        if tag_ref.returncode == 0:
            tagged_commit = subprocess.check_output(
                ["git", "rev-parse", f"{tag}^{{commit}}"], cwd=root, text=True).strip()
            need(tagged_commit == commit, f"existing tag targets the wrong commit: {tag}")
        else:
            need(tag_ref.returncode == 1, f"could not inspect tag: {tag}")

    disk_notes = {
        str(path.relative_to(root))
        for path in (root / "docs/history/releases").glob("*.md")
    }
    need(disk_notes == note_paths, "release note set differs from manifest")
    return {"releases": len(releases), "key_artifacts": artifact_count}


def verify_affected_markdown_links(root=ROOT):
    paths = [
        root / "README.md",
        root / "verification/substrate_v1/README.md",
        root / "docs/history/README.md",
        root / "docs/history/PATH_DEPENDENCY_AUDIT.md",
        root / "docs/history/records/CLASSIFICATION.md",
        *(root / path for path in MOVED_RECORDS.values()),
    ]
    checked = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = match.group(1).strip().strip("<>").split("#", 1)[0]
            if not target or target.startswith(("https://", "http://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            need(resolved.exists(),
                 f"broken relative Markdown link: {path.relative_to(root)} -> {target}")
            checked += 1
    return checked


def verify_historical_tree(root, base):
    """Preserve a runner's old tree while recognizing only the reviewed record migration."""
    verify_moved_records(root)
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", base], cwd=root, text=True).splitlines()
    checked = 0
    for path in paths:
        before = git_bytes(root, base, path)
        if path in MOVED_RECORDS:
            now = (root / MOVED_RECORDS[path]).read_bytes()
            expected = relocated_bytes(path, before)
            if path in APPEND_ONLY_RECORDS:
                need(now.startswith(expected), f"moved append-only record rewrite: {path}")
            else:
                need(now == expected, f"moved historical record rewrite: {path}")
        elif path in CURRENT_MIGRATION_PATHS:
            continue
        else:
            need((root / path).is_file(), f"historical file removed: {path}")
            need((root / path).read_bytes() == before, f"historical file changed: {path}")
        checked += 1
    return checked


def run():
    moved = verify_moved_records()
    releases = verify_release_manifest()
    markdown_links = verify_affected_markdown_links()

    # Durable negative controls for the strict metadata and preservation boundary.
    try:
        strict_json_bytes(b'{"x":1,"x":2}', "duplicate-control")
    except RuntimeError:
        duplicate_rejected = True
    else:
        duplicate_rejected = False
    need(duplicate_rejected, "duplicate JSON metadata was accepted")
    need(relocated_bytes("MATH_ARCHIVE_LEDGER.md", b"frozen") == b"frozen",
         "byte-identical move transformation changed content")
    need(relocated_bytes("FINDINGS_LEDGER.md", b"[x](foundations/a.md)") ==
         b"[x](../../../foundations/a.md)", "relative-link transformation control failed")

    result = {
        "migration_baseline": MIGRATION_BASELINE,
        "moved_records": moved,
        "release_manifest": releases,
        "affected_relative_markdown_links_checked": markdown_links,
        "negative_controls": {
            "duplicate_json_key": "rejected",
            "unexpected_record_mutation": "rejected-by-exact-transformation-check",
            "forged_release_or_artifact_identity": "rejected-by-sha256-and-git-object-check",
        },
        "failed": 0,
    }
    print("HISTORY_MIGRATION_RESULT_BEGIN")
    print(json.dumps(result, sort_keys=True))
    print("HISTORY_MIGRATION_RESULT_END")


if __name__ == "__main__":
    run()
