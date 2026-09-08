#!/usr/bin/env python3
"""Run corner composition checks and the complete inherited acceptance chain."""
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = "6c9cec616358cce6e492c84f16d440f60b7d6124"
REVIEWED_PR14 = "ac8fe70ea3fcb1ba8bb5bd7270eed5324109cb02"
FROZEN = {
    "foundations/BELLMAN_ANYTIME_VALID_DATA_TO_DECISION.md":
        "bcbb6b7f1f16027a726176bbef69f39013bb7ec6ae55fc79ab23fe0d83e952c2",
    "foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md":
        "be495f29011479adab2736bfbe8f3c3e513403fa48c4886652e8137256d1ccbc",
    "foundations/BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md":
        "38a461556da18e977c623404bec16a056013019daeb74adb7207bc0f313d749e",
    "foundations/BELLMAN_FAMILY_REPLANNING_AND_ROOT_GUARANTEES.md":
        "da410d964d2282d75dad1e56be7e6dfdd17c1ee8cc1e4c849f0088b758e03379",
    "verification/statistical_decision_bridge/results.json":
        "2d937135ea0610da69ba09cd477934ec0b4e88843c1bbcf3212311ce079a5b13",
    "verification/multistream_collection/results.json":
        "2b80b11c691be1c297e71bd2c7016c837a3584389748d42ec06c377bf2da7a93",
    "verification/multistream_collection/acceptance_hardening_results.json":
        "68d500c54a3a4c2848aa365d144eadd182d0b41da84aa34adcf4f29a04e9f357",
    "verification/multistream_collection/stop_state_hardening_results.json":
        "041d75f5887d0f24fcfeec50822b09b72b6533dcfb09bf580173404a107f03be",
    "verification/persistent_model_families/results.json":
        "10778c1e5067fcd77de75036da4f4c27114534bb66b61c8a346c63fe3f4b86d6",
    "verification/family_replanning/results.json":
        "2ff65f8a26c6ac46c37ee4a7a19caaaf0fc3a17179b17a093680e5952e751ba5",
}
APPEND_ONLY = {
    "docs/history/records/FINDINGS_LEDGER.md",
    "docs/history/records/SUBSTRATE_LEDGER.md",
}
EDITABLE_EXISTING = APPEND_ONLY | {
    "README.md",
    "docs/programme/ROADMAP.md",
    "docs/programme/ARCHITECTURE.md",
    ".github/workflows/statistical-decision-bridge.yml",
    ".github/workflows/family-replanning.yml",
}
NEW_PREFIX = "verification/statistical_corner_models/"
NEW_PATHS = {
    "foundations/BELLMAN_STATISTICAL_RECTANGLES_TO_CORNER_MODEL_GUARANTEES.md",
    ".github/workflows/statistical-corner-models.yml",
}
SOURCES = (
    "foundations/BELLMAN_STATISTICAL_RECTANGLES_TO_CORNER_MODEL_GUARANTEES.md",
    "verification/statistical_corner_models/reference.py",
    "verification/statistical_corner_models/checks.py",
    "verification/statistical_corner_models/run_checks.py",
    "verification/statistical_corner_models/README.md",
    "README.md",
    "docs/programme/ROADMAP.md",
    "docs/programme/ARCHITECTURE.md",
    "docs/history/records/FINDINGS_LEDGER.md",
    "docs/history/records/SUBSTRATE_LEDGER.md",
    ".github/workflows/statistical-corner-models.yml",
    ".github/workflows/statistical-decision-bridge.yml",
    ".github/workflows/family-replanning.yml",
)


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_bytes(commit, path):
    try:
        return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(f"historical path unavailable: {commit}:{path}") from error


def parse_marked(raw, begin, end):
    start, finish = begin + "\n", "\n" + end
    need(start in raw and finish in raw, f"missing result markers: {begin}")
    return json.loads(raw.split(start, 1)[1].split(finish, 1)[0])


def changed_paths():
    tracked = subprocess.check_output(
        ["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, text=True).splitlines()
    untracked = subprocess.check_output(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=ROOT, text=True).splitlines()
    return tuple(sorted(set(tracked + untracked)))


def verify_scope(paths):
    unexpected = [path for path in paths if not (
        path in EDITABLE_EXISTING or path in NEW_PATHS or path.startswith(NEW_PREFIX))]
    need(not unexpected, "change outside corner-composition scope: " +
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
    path = ROOT / "verification/statistical_corner_models/results.json"
    if not path.exists():
        return False
    record = json.loads(path.read_text())
    need(record.get("status") == "passed" and record.get("failed") == 0,
         "retained corner-composition result is not passing")
    commit = record.get("executed_source_commit")
    need(type(commit) is str and len(commit) == 40,
         "result lacks an exact source commit")
    for source, digest in record.get("source_sha256", {}).items():
        need(digest == hashes.get(source), f"result source map changed: {source}")
        need(sha256(git_bytes(commit, source)) == digest,
             f"result does not bind executed source bytes: {source}")
    need(record.get("frozen_prerequisite_sha256") == FROZEN,
         "result prerequisite identities changed")
    return True


def run():
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                   text=True).strip()
    need(subprocess.run(["git", "merge-base", "--is-ancestor", REVIEWED_PR14, BASE],
                        cwd=ROOT).returncode == 0,
         "reviewed PR14 head is not in the required base")
    need(subprocess.run(["git", "diff", "--quiet", REVIEWED_PR14, BASE, "--"],
                        cwd=ROOT).returncode == 0,
         "PR14 merge tree differs from reviewed final head")
    need(subprocess.run(["git", "merge-base", "--is-ancestor", BASE, head],
                        cwd=ROOT).returncode == 0,
         "corner work is not based on merged PR14 main")
    scope = changed_paths()
    verify_scope(scope)
    preserved = verify_base_preservation()
    frozen = verify_frozen()

    def call_json(path, flags=()):
        started = time.perf_counter()
        raw = subprocess.check_output([sys.executable, *flags, path], cwd=ROOT,
                                      env=environment, text=True)
        return json.loads(raw), time.perf_counter() - started

    modes = ((), ("-O",))
    corner_runs, current = [], {}
    durations = {}
    for flags in modes:
        label = "-O" if flags else "normal"
        value, seconds = call_json(
            "verification/statistical_corner_models/checks.py", flags)
        corner_runs.append(value)
        durations[f"corner_{label}"] = seconds
        for name, path in (
            ("scalar", "verification/statistical_decision_bridge/checks.py"),
            ("multistream", "verification/multistream_collection/checks.py"),
            ("pr14_acceptance", "verification/multistream_collection/acceptance_checks.py"),
            ("persistent", "verification/persistent_model_families/checks.py"),
            ("replanning", "verification/family_replanning/checks.py"),
        ):
            value, seconds = call_json(path, flags)
            current.setdefault(name, []).append(value)
            durations[f"{name}_{label}"] = seconds

    need(corner_runs[0]["results"] == corner_runs[1]["results"] and
         corner_runs[0]["rejections"] == corner_runs[1]["rejections"] and
         corner_runs[0]["unfinished"] == corner_runs[1]["unfinished"] and
         corner_runs[0]["failed"] == corner_runs[1]["failed"] == 0,
         "corner checks differ by optimization mode or failed")
    for name, runs in current.items():
        first = dict(runs[0])
        second = dict(runs[1])
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

    # Run the complete PR14 -> PR12 -> PR10 historical chain at the exact merged tree.
    historical_started = time.perf_counter()
    with tempfile.TemporaryDirectory() as temporary:
        subprocess.check_call(["git", "clone", "--quiet", "--no-local",
                               str(ROOT), temporary])
        subprocess.check_call(["git", "checkout", "--quiet", BASE], cwd=temporary)
        raw = subprocess.check_output(
            [sys.executable, "verification/multistream_collection/run_checks.py"],
            cwd=temporary, env=environment, text=True)
    durations["historical_pr14_chain"] = time.perf_counter() - historical_started
    historical = parse_marked(
        raw, "MULTISTREAM_ACCEPTANCE_HARDENING_RESULT_BEGIN",
        "MULTISTREAM_ACCEPTANCE_HARDENING_RESULT_END")
    need(historical["status"] == "passed" and historical["failed"] == 0 and
         historical["recorded_stop_state_result_present_and_current"],
         "merged PR14 historical acceptance chain failed")

    hashes = source_hashes()
    retained_result = verify_optional_result(hashes)
    result = {
        "status": "passed",
        "failed": 0,
        "base_commit": BASE,
        "reviewed_pr14_head": REVIEWED_PR14,
        "executed_source_commit": head,
        "runtime": platform.python_version(),
        "execution": ("GitHub Actions" if os.environ.get("GITHUB_ACTIONS") == "true"
                      else "local"),
        "modes": ["normal", "-O"],
        "normal_optimized_equal": True,
        "passed_per_mode": corner_runs[0]["passed"],
        "rejections_per_mode": corner_runs[0]["rejections"],
        "unfinished_per_mode": corner_runs[0]["unfinished"],
        "results": corner_runs[0]["results"],
        "current_checks": {
            "scalar_passed_per_mode": current["scalar"][0]["passed"],
            "multistream_status": current["multistream"][0]["status"],
            "pr14_acceptance_status": current["pr14_acceptance"][0]["status"],
            "persistent_passed_per_mode": current["persistent"][0]["passed"],
            "replanning_passed_per_mode": current["replanning"][0]["passed"],
            "history": history[0],
        },
        "preservation": {
            "pr14_merged_before_start": True,
            "pr14_merge_tree_matches_reviewed_head": True,
            "base_files_checked": preserved,
            "historical_pr14_runner": "passed-at-exact-merge",
            "historical_pr12_runner":
                historical["preservation"]["historical_pr12_runner"],
            "inherited_pr10_runner": historical["preservation"]["inherited_pr10_runner"],
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
            "The theorem is proved analytically and checked on bounded exact cases, not formally verified.",
            "Statistical IID/completeness premises are supplied inputs and are not empirically validated.",
            "One or two parameters and deterministic policies only; no continuous optimizer or randomized-policy claim.",
            "Invalid corner reduction leaves the sequential problem valid for another optimization method.",
        ],
    }
    print("STATISTICAL_CORNER_MODEL_RESULT_BEGIN")
    print(json.dumps(result, sort_keys=True))
    print("STATISTICAL_CORNER_MODEL_RESULT_END")


if __name__ == "__main__":
    run()
