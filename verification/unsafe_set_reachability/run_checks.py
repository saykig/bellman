#!/usr/bin/env python3
"""Run unsafe-reachability checks and the inherited acceptance chain."""
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = "2727f7b578cf7bab40cfc1cbb4def583cf7da84d"
REVIEWED_PR16 = "c6be1d14091335c8218d37ca1ed8ac1e15e4c064"
FROZEN = {
    "foundations/BELLMAN_STATISTICAL_RECTANGLES_TO_CORNER_MODEL_GUARANTEES.md":
        "c87033cf4f9d7adaadb745fa0722ff62376eabc11cf1219628cd6b5df388313e",
    "verification/statistical_corner_models/results.json":
        "c2360cdfcbde5f4bb48d0a629bb0c60defcaecd8506224d14c76d49436849a7e",
    "foundations/BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md":
        "38a461556da18e977c623404bec16a056013019daeb74adb7207bc0f313d749e",
    "verification/persistent_model_families/results.json":
        "10778c1e5067fcd77de75036da4f4c27114534bb66b61c8a346c63fe3f4b86d6",
    "foundations/BELLMAN_SEQUENTIAL_CERTIFICATE_COMPOSITION.md":
        "a974aa8e9753bcc1a4f5a5cd4d51c88040ae30bc40f98d1e837c71c6d711d0a4",
    "verification/sequential_certificates/results.json":
        "047be866108cf3097e9e4ee598a80a7fb79dd50729b2547aa11af059dda7cd56",
    "foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md":
        "be495f29011479adab2736bfbe8f3c3e513403fa48c4886652e8137256d1ccbc",
    "verification/multistream_collection/results.json":
        "2b80b11c691be1c297e71bd2c7016c837a3584389748d42ec06c377bf2da7a93",
}
APPEND_ONLY = {
    "docs/history/records/FINDINGS_LEDGER.md",
    "docs/history/records/SUBSTRATE_LEDGER.md",
}
EDITABLE_EXISTING = APPEND_ONLY | {
    "README.md",
    "docs/programme/ROADMAP.md",
    "docs/programme/ARCHITECTURE.md",
    ".github/workflows/statistical-corner-models.yml",
}
NEW_PREFIX = "verification/unsafe_set_reachability/"
NEW_PATHS = {
    "foundations/BELLMAN_UNSAFE_SET_REACHABILITY_AND_CONSTRAINED_SELECTION.md",
    ".github/workflows/unsafe-set-reachability.yml",
}
SOURCES = (
    "foundations/BELLMAN_UNSAFE_SET_REACHABILITY_AND_CONSTRAINED_SELECTION.md",
    "verification/unsafe_set_reachability/reference.py",
    "verification/unsafe_set_reachability/checks.py",
    "verification/unsafe_set_reachability/run_checks.py",
    "verification/unsafe_set_reachability/README.md",
    "README.md",
    "docs/programme/ROADMAP.md",
    "docs/programme/ARCHITECTURE.md",
    "docs/history/records/FINDINGS_LEDGER.md",
    "docs/history/records/SUBSTRATE_LEDGER.md",
    ".github/workflows/statistical-corner-models.yml",
    ".github/workflows/unsafe-set-reachability.yml",
)


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_bytes(commit, path):
    try:
        return subprocess.check_output(["git", "show", f"{commit}:{path}"],
                                       cwd=ROOT)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(
            f"historical path unavailable: {commit}:{path}") from error


def parse_marked(raw, begin, end):
    start, finish = begin + "\n", "\n" + end
    need(start in raw and finish in raw, f"missing result markers: {begin}")
    return json.loads(raw.split(start, 1)[1].split(finish, 1)[0])


def changed_paths():
    tracked = subprocess.check_output(
        ["git", "diff", "--name-only", BASE, "--"], cwd=ROOT,
        text=True).splitlines()
    untracked = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT,
        text=True).splitlines()
    return tuple(sorted(set(tracked + untracked)))


def verify_scope(paths):
    unexpected = [path for path in paths if not (
        path in EDITABLE_EXISTING or path in NEW_PATHS or
        path.startswith(NEW_PREFIX))]
    need(not unexpected, "change outside unsafe-reachability scope: " +
         ", ".join(unexpected))


def verify_base_preservation():
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASE], cwd=ROOT,
        text=True).splitlines()
    checked = 0
    for path in paths:
        before = git_bytes(BASE, path)
        current = ROOT / path
        need(current.is_file(), f"base file removed: {path}")
        if path in APPEND_ONLY:
            need(current.read_bytes().startswith(before),
                 f"append-only historical record rewritten: {path}")
        elif path in EDITABLE_EXISTING:
            pass
        else:
            need(current.read_bytes() == before,
                 f"base or historical file changed outside scope: {path}")
        checked += 1
    return checked


def verify_frozen():
    for path, digest in FROZEN.items():
        need(sha256((ROOT / path).read_bytes()) == digest,
             f"frozen prerequisite identity changed: {path}")
        need(sha256(git_bytes(BASE, path)) == digest,
             f"base prerequisite identity mismatch: {path}")
    return dict(FROZEN)


def source_hashes():
    return {path: sha256((ROOT / path).read_bytes()) for path in SOURCES}


def verify_optional_result(hashes):
    path = ROOT / "verification/unsafe_set_reachability/results.json"
    if not path.exists():
        return False
    record = json.loads(path.read_text())
    need(record.get("status") == "passed" and record.get("failed") == 0,
         "retained unsafe-reachability result is not passing")
    commit = record.get("executed_source_commit")
    need(type(commit) is str and len(commit) == 40,
         "result lacks an exact source commit")
    need(record.get("source_sha256") == hashes,
         "retained result source map differs from current source bytes")
    for source, digest in hashes.items():
        need(sha256(git_bytes(commit, source)) == digest,
             f"result does not bind executed source bytes: {source}")
    need(record.get("frozen_prerequisite_sha256") == FROZEN,
         "result prerequisite identities changed")
    return True


def verify_markdown_links(paths):
    checked = 0
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    for path in paths:
        if not path.endswith(".md"):
            continue
        source = ROOT / path
        if not source.is_file():
            continue
        for target in pattern.findall(source.read_text()):
            target = target.strip().strip("<>").split("#", 1)[0]
            if (not target or "://" in target or target.startswith("mailto:") or
                    target.startswith("codex:")):
                continue
            destination = (source.parent / target).resolve()
            need(destination.exists(),
                 f"broken relative Markdown link in {path}: {target}")
            checked += 1
    return checked


def run():
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                   text=True).strip()
    need(subprocess.run(["git", "merge-base", "--is-ancestor",
                         REVIEWED_PR16, BASE], cwd=ROOT).returncode == 0,
         "reviewed PR16 head is not in the required base")
    need(subprocess.run(["git", "diff", "--quiet", REVIEWED_PR16, BASE, "--"],
                        cwd=ROOT).returncode == 0,
         "PR16 merge tree differs from reviewed final head")
    need(subprocess.run(["git", "merge-base", "--is-ancestor", BASE, head],
                        cwd=ROOT).returncode == 0,
         "unsafe-reachability work is not based on merged PR16 main")
    scope = changed_paths()
    verify_scope(scope)
    preserved = verify_base_preservation()
    frozen = verify_frozen()
    markdown_links = verify_markdown_links(scope)

    def call_json(path, flags=()):
        started = time.perf_counter()
        raw = subprocess.check_output([sys.executable, *flags, path], cwd=ROOT,
                                      env=environment, text=True)
        return json.loads(raw), time.perf_counter() - started

    modes = ((), ("-O",))
    unsafe_runs, current, durations = [], {}, {}
    current_paths = (
        ("corner", "verification/statistical_corner_models/checks.py"),
        ("persistent", "verification/persistent_model_families/checks.py"),
        ("sequential", "verification/sequential_certificates/checks.py"),
        ("multistream", "verification/multistream_collection/checks.py"),
        ("replanning", "verification/family_replanning/checks.py"),
    )
    for flags in modes:
        label = "-O" if flags else "normal"
        value, seconds = call_json(
            "verification/unsafe_set_reachability/checks.py", flags)
        unsafe_runs.append(value)
        durations[f"unsafe_{label}"] = seconds
        for name, path in current_paths:
            value, seconds = call_json(path, flags)
            current.setdefault(name, []).append(value)
            durations[f"{name}_{label}"] = seconds

    first = dict(unsafe_runs[0])
    second = dict(unsafe_runs[1])
    first.pop("optimized", None)
    second.pop("optimized", None)
    need(first == second and unsafe_runs[0]["failed"] == 0,
         "unsafe reachability checks differ by optimization mode or failed")
    for name, runs in current.items():
        first, second = dict(runs[0]), dict(runs[1])
        first.pop("optimized", None)
        second.pop("optimized", None)
        need(first == second, f"current {name} checks differ by optimization mode")
        need(runs[0].get("failed") == runs[1].get("failed") == 0 or
             runs[0].get("status") == runs[1].get("status") == "passed",
             f"current {name} checks failed")

    history = []
    for flags in modes:
        started = time.perf_counter()
        raw = subprocess.check_output(
            [sys.executable, *flags, "verification/history_migration/checks.py"],
            cwd=ROOT, env=environment, text=True)
        durations[f"history_{'-O' if flags else 'normal'}"] = (
            time.perf_counter() - started)
        history.append(parse_marked(raw, "HISTORY_MIGRATION_RESULT_BEGIN",
                                    "HISTORY_MIGRATION_RESULT_END"))
    need(history[0] == history[1] and history[0]["failed"] == 0,
         "history/release identity checks differ or failed")

    # Replay PR16 -> PR14 -> PR12 -> PR10 from PR16's exact merged tree.
    historical_started = time.perf_counter()
    with tempfile.TemporaryDirectory() as temporary:
        subprocess.check_call(["git", "clone", "--quiet", "--no-local",
                               str(ROOT), temporary])
        subprocess.check_call(["git", "checkout", "--quiet", BASE],
                              cwd=temporary)
        raw = subprocess.check_output(
            [sys.executable,
             "verification/statistical_corner_models/run_checks.py"],
            cwd=temporary, env=environment, text=True)
    durations["historical_pr16_chain"] = time.perf_counter() - historical_started
    historical = parse_marked(raw, "STATISTICAL_CORNER_MODEL_RESULT_BEGIN",
                              "STATISTICAL_CORNER_MODEL_RESULT_END")
    need(historical["status"] == "passed" and historical["failed"] == 0 and
         historical["retained_result_present_and_source_bound"],
         "merged PR16 historical acceptance chain failed")

    hashes = source_hashes()
    retained_result = verify_optional_result(hashes)
    result = {
        "status": "passed",
        "failed": 0,
        "base_commit": BASE,
        "reviewed_pr16_head": REVIEWED_PR16,
        "executed_source_commit": head,
        "runtime": platform.python_version(),
        "execution": ("GitHub Actions" if
                      os.environ.get("GITHUB_ACTIONS") == "true" else "local"),
        "modes": ["normal", "-O"],
        "normal_optimized_equal": True,
        "passed_per_mode": unsafe_runs[0]["passed"],
        "rejections_per_mode": unsafe_runs[0]["rejections"],
        "results": unsafe_runs[0]["results"],
        "current_checks": {
            "corner_passed_per_mode": current["corner"][0]["passed"],
            "persistent_passed_per_mode": current["persistent"][0]["passed"],
            "sequential_passed_per_mode": current["sequential"][0]["passed"],
            "multistream_status": current["multistream"][0]["status"],
            "replanning_passed_per_mode": current["replanning"][0]["passed"],
            "history": history[0],
            "affected_relative_markdown_links_checked": markdown_links,
        },
        "preservation": {
            "pr16_merged_before_start": True,
            "pr16_merge_tree_matches_reviewed_head": True,
            "base_files_checked": preserved,
            "historical_pr16_runner": "passed-at-exact-merge",
            "historical_pr14_runner":
                historical["preservation"]["historical_pr14_runner"],
            "historical_pr12_runner":
                historical["preservation"]["historical_pr12_runner"],
            "inherited_pr10_runner":
                historical["preservation"]["inherited_pr10_runner"],
            "historical_files_preserved":
                historical["preservation"]["historical_files_preserved"],
            "release_versions": history[0]["release_manifest"]["versions"],
            "release_identities_unchanged": True,
        },
        "source_sha256": hashes,
        "frozen_prerequisite_sha256": frozen,
        "retained_result_present_and_source_bound": retained_result,
        "authorized_paths": list(scope),
        "durations_seconds": durations,
        "limitations": [
            "Analytical proofs plus bounded exact checks are not formal verification.",
            "Model validity and normative unsafe-set adequacy are supplied, not established.",
            "Statistical IID/completeness premises are not empirically validated.",
            "Deterministic policies, four models, and two statistical parameters only.",
            "No CVaR, dynamic risk, resource constraint, randomized-policy, or authority claim.",
            "Finite enumeration remained small, so no solver or language trigger was reached.",
        ],
    }
    print("UNSAFE_SET_REACHABILITY_RESULT_BEGIN")
    print(json.dumps(result, sort_keys=True))
    print("UNSAFE_SET_REACHABILITY_RESULT_END")


if __name__ == "__main__":
    run()
