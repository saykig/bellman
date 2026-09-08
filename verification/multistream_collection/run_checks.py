"""Run current PR #14 hardening checks and exact historical acceptance replay."""
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
CURRENT_MAIN = "1404949753038d09fa76890ecd01b331dda18d88"
REVIEWED_PR14 = "f3d609b9b2b6aa10c283737cf04a0df58a6c948c"
ORIGINAL_PR14_BASE = "92922ab6604840152ad7f7800969673335748272"
ORIGINAL_PR14_SOURCE = "fdf83a0b2f3b31331ed894fa0d0aeeffea07db00"
REPAIRED_PR12 = "5017122500450c8f7f890474f7232b9c94d3a3fb"
PR12_HISTORICAL_BASE = "2e8d99cdcf289eabb63df15086eaa68251a359f1"

FROZEN_PR12_SHA256 = {
    "foundations/BELLMAN_ANYTIME_VALID_DATA_TO_DECISION.md":
        "bcbb6b7f1f16027a726176bbef69f39013bb7ec6ae55fc79ab23fe0d83e952c2",
    "verification/statistical_decision_bridge/reference.py":
        "4b8f066b5785e04cdb9fd882820ec64fd453d87b3cc253781cea03a9ab152852",
    "verification/statistical_decision_bridge/checks.py":
        "75ec61e882f6207b41481cbde8d9ca1b20c0cd7f14f3bfafecc67208a3c68359",
    "verification/statistical_decision_bridge/results.json":
        "2d937135ea0610da69ba09cd477934ec0b4e88843c1bbcf3212311ce079a5b13",
    "verification/statistical_decision_bridge/ACCEPTANCE_HARDENING.md":
        "a06d94d7d6dbc3d388b2e46246be67f1c5d9a21039bea9fca7825601b89c0844",
    "verification/statistical_decision_bridge/acceptance_hardening_results.json":
        "d2bfc1d3fa90a39b87232b479f969cc38c92185f9c5ddedd0657719089cfc783",
}
FROZEN_ORIGINAL_PR14_SHA256 = {
    "foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md":
        "be495f29011479adab2736bfbe8f3c3e513403fa48c4886652e8137256d1ccbc",
    "verification/multistream_collection/results.json":
        "2b80b11c691be1c297e71bd2c7016c837a3584389748d42ec06c377bf2da7a93",
}
ORIGINAL_PR14_SOURCE_SHA256 = {
    "verification/multistream_collection/reference.py":
        "e6f509678859d1960d843e315c5453008fda7e4807039eedd733599511f2dbc2",
    "verification/multistream_collection/checks.py":
        "1da6c4ee121a753a340ee8f40e8cf526e9648f88e0a66050bb48a1aa49afd196",
    "verification/multistream_collection/run_checks.py":
        "466b2083e650dd09952305069defde05af2f9163ffe19a46b66bb08b8637dfce",
    "verification/multistream_collection/README.md":
        "31e26ab8f397e98aedb7b89ec69daec38e817e8fc14390cd8a76de59830ff3e6",
}

PR14_PATHS = {
    "foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md",
    "verification/multistream_collection/ACCEPTANCE_HARDENING.md",
    "verification/multistream_collection/README.md",
    "verification/multistream_collection/acceptance_checks.py",
    "verification/multistream_collection/acceptance_hardening_results.json",
    "verification/multistream_collection/checks.py",
    "verification/multistream_collection/reference.py",
    "verification/multistream_collection/results.json",
    "verification/multistream_collection/run_checks.py",
}
LIVING_PATHS = {
    ".github/workflows/family-replanning.yml",
    ".github/workflows/statistical-decision-bridge.yml",
    "README.md",
    "docs/history/records/CLASSIFICATION.md",
    "docs/history/records/FINDINGS_LEDGER.md",
    "docs/history/records/SUBSTRATE_LEDGER.md",
    "docs/programme/ARCHITECTURE.md",
    "docs/programme/ROADMAP.md",
    "verification/history_migration/README.md",
    "verification/history_migration/checks.py",
}
AUTHORIZED_PATHS = PR14_PATHS | LIVING_PATHS
APPEND_ONLY_CURRENT = {
    "docs/history/records/FINDINGS_LEDGER.md",
    "docs/history/records/SUBSTRATE_LEDGER.md",
}
RESULT_SOURCES = (
    "verification/multistream_collection/reference.py",
    "verification/multistream_collection/checks.py",
    "verification/multistream_collection/acceptance_checks.py",
    "verification/multistream_collection/run_checks.py",
    "verification/multistream_collection/README.md",
    "verification/multistream_collection/ACCEPTANCE_HARDENING.md",
    "verification/history_migration/checks.py",
    ".github/workflows/statistical-decision-bridge.yml",
    ".github/workflows/family-replanning.yml",
)


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_bytes(commit, path):
    try:
        return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(f"historical path unavailable: {commit}:{path}") from error


def require_commit(commit):
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    need(result.returncode == 0, f"required historical commit unavailable: {commit}")


def require_ancestor(ancestor, descendant, message):
    need(subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0, message)


def parse_marked_json(raw, begin, end):
    start = begin + "\n"
    finish = "\n" + end
    need(start in raw and finish in raw, f"result markers missing: {begin}")
    return json.loads(raw.split(start, 1)[1].split(finish, 1)[0])


def enforce_change_scope(paths):
    paths = set(paths)
    unexpected = paths.difference(AUTHORIZED_PATHS)
    need(not unexpected, "unauthorized PR14 hardening path: " +
         ", ".join(sorted(unexpected)))


def verify_hashes(expected, *, at_commit=None):
    actual = {}
    for path, digest in expected.items():
        data = git_bytes(at_commit, path) if at_commit else (ROOT / path).read_bytes()
        need(sha256(data) == digest, f"frozen identity changed: {path}")
        actual[path] = digest
    return actual


def verify_protected_bytes(path, data):
    expected = {**FROZEN_PR12_SHA256, **FROZEN_ORIGINAL_PR14_SHA256}
    need(path in expected and sha256(data) == expected[path],
         f"protected mathematical source/result changed: {path}")


def verify_original_result_binding():
    record = json.loads(git_bytes(
        REVIEWED_PR14,
        "verification/multistream_collection/results.json").decode())
    need(record["executed_commit"] == ORIGINAL_PR14_SOURCE,
         "original hosted result has unexpected source commit")
    recorded = record.get("source_sha256", {})
    for path, digest in ORIGINAL_PR14_SOURCE_SHA256.items():
        need(sha256(git_bytes(REVIEWED_PR14, path)) == digest,
             f"reviewed PR14 source identity mismatch: {path}")
        need(recorded.get(path) == digest,
             f"original result does not bind reviewed source: {path}")
    return record


def verify_current_main_preservation():
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", CURRENT_MAIN],
        cwd=ROOT, text=True).splitlines()
    checked = 0
    for path in paths:
        before = git_bytes(CURRENT_MAIN, path)
        if path in APPEND_ONLY_CURRENT:
            need((ROOT / path).read_bytes().startswith(before),
                 f"current history record rewritten: {path}")
        elif path in AUTHORIZED_PATHS:
            pass
        else:
            need((ROOT / path).is_file(), f"current-main file removed: {path}")
            need((ROOT / path).read_bytes() == before,
                 f"current-main file changed outside hardening: {path}")
        checked += 1
    for old_path in ("FINDINGS_LEDGER.md", "MATH_ARCHIVE_LEDGER.md",
                     "SUBSTRATE_LEDGER.md", "LEGACY_ARCHIVE_STATUS.md"):
        need(not (ROOT / old_path).exists(), f"obsolete root history restored: {old_path}")
    return checked


def expect_failure(operation, message):
    try:
        operation()
    except (RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError):
        return
    raise RuntimeError(message)


def source_hashes():
    return {path: sha256((ROOT / path).read_bytes()) for path in RESULT_SOURCES}


def verify_optional_hardening_record(actual_hashes):
    path = ROOT / "verification/multistream_collection/acceptance_hardening_results.json"
    if not path.exists():
        return False
    record = json.loads(path.read_text())
    need(record.get("status") == "passed" and record.get("failed") == 0,
         "recorded PR14 hardening result is not passing")
    need(record.get("current_main") == CURRENT_MAIN and
         record.get("reviewed_pr14_head") == REVIEWED_PR14,
         "recorded PR14 hardening lineage mismatch")
    need(record.get("source_sha256") == actual_hashes,
         "recorded PR14 hardening source identities are stale")
    need(record.get("frozen_original_pr14_sha256") == FROZEN_ORIGINAL_PR14_SHA256,
         "recorded original PR14 identities are stale")
    return True


def run():
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    for commit in (CURRENT_MAIN, REVIEWED_PR14, ORIGINAL_PR14_BASE,
                   REPAIRED_PR12, PR12_HISTORICAL_BASE):
        require_commit(commit)
    require_ancestor(ORIGINAL_PR14_BASE, REVIEWED_PR14,
                     "original PR14 base is not an ancestor of reviewed head")
    require_ancestor(REVIEWED_PR14, "HEAD",
                     "reviewed PR14 head is not an ancestor of current head")
    require_ancestor(CURRENT_MAIN, "HEAD",
                     "current main was not merged into PR14")
    require_ancestor(REPAIRED_PR12, CURRENT_MAIN,
                     "repaired PR12 is not in current main")

    changed = subprocess.check_output(
        ["git", "diff", "--name-only", CURRENT_MAIN, "--"],
        cwd=ROOT, text=True).splitlines()
    enforce_change_scope(changed)
    frozen_pr12 = verify_hashes(FROZEN_PR12_SHA256)
    frozen_pr14 = verify_hashes(FROZEN_ORIGINAL_PR14_SHA256)
    verify_hashes(FROZEN_ORIGINAL_PR14_SHA256, at_commit=REVIEWED_PR14)
    original_result = verify_original_result_binding()
    current_main_files_checked = verify_current_main_preservation()

    def call_json(arguments):
        started = time.perf_counter()
        output = subprocess.check_output(
            [sys.executable] + arguments, cwd=ROOT, env=environment, text=True)
        return json.loads(output), time.perf_counter() - started

    modes = ([], ["-O"])
    scalar_runs, multistream_runs, acceptance_runs = [], [], []
    family_runs, persistent_runs, durations = [], [], {}
    for flags in modes:
        label = "-O" if flags else "normal"
        scalar, seconds = call_json(
            flags + ["verification/statistical_decision_bridge/checks.py"])
        scalar_runs.append(scalar)
        durations[f"scalar_{label}"] = seconds
        multistream, seconds = call_json(
            flags + ["verification/multistream_collection/checks.py"])
        multistream_runs.append(multistream)
        durations[f"multistream_{label}"] = seconds
        acceptance, seconds = call_json(
            flags + ["verification/multistream_collection/acceptance_checks.py"])
        acceptance_runs.append(acceptance)
        durations[f"acceptance_{label}"] = seconds
        family, seconds = call_json(flags + ["verification/family_replanning/checks.py"])
        family_runs.append(family)
        durations[f"family_{label}"] = seconds
        persistent, seconds = call_json(
            flags + ["verification/persistent_model_families/checks.py"])
        persistent_runs.append(persistent)
        durations[f"persistent_{label}"] = seconds

    for key in ("results", "rejections", "unfinished"):
        need(scalar_runs[0][key] == scalar_runs[1][key],
             f"normal and optimized scalar {key} differ")
    need(scalar_runs[0]["failed"] == scalar_runs[1]["failed"] == 0,
         "current scalar checks failed")
    need(multistream_runs[0] == multistream_runs[1] and
         multistream_runs[0]["status"] == "passed",
         "current multistream checks differ or failed")
    need(acceptance_runs[0] == acceptance_runs[1] and
         acceptance_runs[0]["status"] == "passed",
         "PR14 acceptance checks differ or failed")
    for label, runs in (("family", family_runs), ("persistent", persistent_runs)):
        need(runs[0]["results"] == runs[1]["results"] and
             runs[0]["rejections"] == runs[1]["rejections"] and
             runs[0]["failed"] == runs[1]["failed"] == 0,
             f"current {label} preservation checks differ or failed")

    history_runs = []
    for flags in modes:
        output = subprocess.check_output(
            [sys.executable] + flags + ["verification/history_migration/checks.py"],
            cwd=ROOT, env=environment, text=True)
        history_runs.append(parse_marked_json(
            output, "HISTORY_MIGRATION_RESULT_BEGIN", "HISTORY_MIGRATION_RESULT_END"))
    need(history_runs[0] == history_runs[1] and history_runs[0]["failed"] == 0,
         "current PR13 history migration checks differ or failed")

    historical_started = time.perf_counter()
    with tempfile.TemporaryDirectory() as temporary:
        subprocess.check_call(
            ["git", "clone", "--quiet", "--no-local", str(ROOT), temporary])
        subprocess.check_call(
            ["git", "update-ref", "refs/remotes/origin/main",
             PR12_HISTORICAL_BASE], cwd=temporary)
        subprocess.check_call(
            ["git", "checkout", "--quiet", REPAIRED_PR12], cwd=temporary)
        need(subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=temporary, text=True).strip() ==
            REPAIRED_PR12, "historical PR12 head binding failed")
        need(subprocess.check_output(
            ["git", "rev-parse", "origin/main"], cwd=temporary, text=True).strip() ==
            PR12_HISTORICAL_BASE, "historical PR12 base binding failed")
        raw = subprocess.check_output(
            [sys.executable, "verification/statistical_decision_bridge/run_checks.py"],
            cwd=temporary, env=environment, text=True)
    historical_seconds = time.perf_counter() - historical_started
    historical = parse_marked_json(
        raw, "STATISTICAL_DECISION_BRIDGE_RESULT_BEGIN",
        "STATISTICAL_DECISION_BRIDGE_RESULT_END")
    need(historical["failed"] == 0 and historical["historical_files_preserved"],
         "historical PR12 acceptance replay failed")

    enforce_change_scope({"docs/history/records/FINDINGS_LEDGER.md"})
    expect_failure(lambda: verify_protected_bytes(
        "foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md",
        (ROOT / "foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md").read_bytes()
        + b"mutation"),
        "protected PR14 companion mutation was accepted")
    expect_failure(lambda: verify_protected_bytes(
        "verification/multistream_collection/results.json",
        (ROOT / "verification/multistream_collection/results.json").read_bytes()
        + b"mutation"),
        "protected original PR14 result mutation was accepted")
    expect_failure(lambda: require_commit("0" * 40),
                   "missing historical commit was accepted")
    expect_failure(lambda: parse_marked_json(
        "{}", "STATISTICAL_DECISION_BRIDGE_RESULT_BEGIN",
        "STATISTICAL_DECISION_BRIDGE_RESULT_END"),
        "malformed historical output was accepted")
    expect_failure(lambda: require_ancestor(
        CURRENT_MAIN, PR12_HISTORICAL_BASE, "intentional wrong replay base"),
        "wrong historical base was accepted")
    intentional_failure = (
        "import runpy; "
        "runpy.run_path('verification/multistream_collection/acceptance_checks.py', "
        "run_name='__main__'); "
        "raise RuntimeError('intentional current acceptance failure')"
    )
    try:
        subprocess.check_output(
            [sys.executable, "-c", intentional_failure], cwd=ROOT,
            env=environment, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        need('"status": "passed"' in error.output,
             "intentional failure did not first run current acceptance checks")
    else:
        raise RuntimeError("intentional current mathematical failure was suppressed")

    hashes = source_hashes()
    recorded = verify_optional_hardening_record(hashes)
    result = {
        "status": "passed",
        "failed": 0,
        "current_main": CURRENT_MAIN,
        "reviewed_pr14_head": REVIEWED_PR14,
        "original_pr14_base": ORIGINAL_PR14_BASE,
        "executed_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "runtime": platform.python_version(),
        "execution": "GitHub Actions" if os.environ.get("GITHUB_ACTIONS") == "true" else "local",
        "modes": ["normal", "-O"],
        "normal_optimized_equal": True,
        "scalar": {
            "passed_per_mode": scalar_runs[0]["passed"],
            "rejections_per_mode": scalar_runs[0]["rejections"],
            "unfinished_per_mode": scalar_runs[0]["unfinished"],
        },
        "multistream": multistream_runs[0],
        "acceptance_hardening": acceptance_runs[0],
        "current_preservation": {
            "family_passed_per_mode": family_runs[0]["passed"],
            "family_rejections_per_mode": family_runs[0]["rejections"],
            "persistent_passed_per_mode": persistent_runs[0]["passed"],
            "persistent_rejections_per_mode": persistent_runs[0]["rejections"],
        },
        "history_migration": history_runs[0],
        "source_sha256": hashes,
        "frozen_pr12_sha256": frozen_pr12,
        "frozen_original_pr14_sha256": frozen_pr14,
        "original_result_executed_commit": original_result["executed_commit"],
        "recorded_hardening_result_present_and_current": recorded,
        "preservation": {
            "current_main_merged": True,
            "current_main_files_checked": current_main_files_checked,
            "obsolete_root_ledgers_absent": True,
            "historical_pr12_runner": "passed-at-exact-repaired-head",
            "historical_pr12_origin_main": PR12_HISTORICAL_BASE,
            "historical_pr12_seconds": historical_seconds,
            "inherited_pr10_runner": historical["preservation"]["inherited_runner"],
            "historical_files_preserved": historical["historical_files_preserved"],
        },
        "authorized_paths": sorted(changed),
        "negative_controls": {
            "canonical_history_append": "accepted",
            "protected_pr14_companion_change": "rejected",
            "protected_original_pr14_result_change": "rejected",
            "intentional_current_check_failure": "rejected",
            "missing_historical_commit": "rejected",
            "malformed_historical_output": "rejected",
            "wrong_historical_base": "rejected",
        },
        "durations_seconds": durations,
        "limitations": [
            "The valid multistream theorem and original hosted result remain historical evidence.",
            "Constructor hardening checks declared subject completeness; it does not validate physical sampling.",
            "Revision classification records provenance disposition but does not validate a corrected history.",
            "No adaptive allocation, dynamic registry, missingness correction, bandit optimization, or sequential-control composition is added.",
        ],
    }
    print("MULTISTREAM_ACCEPTANCE_HARDENING_RESULT_BEGIN")
    print(json.dumps(result, sort_keys=True))
    print("MULTISTREAM_ACCEPTANCE_HARDENING_RESULT_END")


if __name__ == "__main__":
    run()
