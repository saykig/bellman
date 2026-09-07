"""Run current multistream checks and the exact pinned PR #12 replay."""
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
BASE_MERGE = "92922ab6604840152ad7f7800969673335748272"
REPAIRED_PR12 = "5017122500450c8f7f890474f7232b9c94d3a3fb"
PR12_HISTORICAL_BASE = "2e8d99cdcf289eabb63df15086eaa68251a359f1"
INITIAL_PR12 = "fbfbc182a05952198d9ce9dc6ef4e9a395eaf3c6"

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
    "verification/statistical_decision_bridge/run_checks.py":
        "296fd5a4a60f71732b074f9f3fae0bae691661b51da263fda4c91c13a1701fd4",
    "verification/statistical_decision_bridge/README.md":
        "ef3ad68ca034f14be63f3478292046a07402f0debd2ce414fe3180e080f77b1c",
}

NEW_PATHS = {
    "foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md",
    "verification/multistream_collection/README.md",
    "verification/multistream_collection/checks.py",
    "verification/multistream_collection/reference.py",
    "verification/multistream_collection/results.json",
    "verification/multistream_collection/run_checks.py",
}
LIVING_PATHS = {
    ".github/workflows/family-replanning.yml",
    ".github/workflows/statistical-decision-bridge.yml",
    "FINDINGS_LEDGER.md",
    "README.md",
    "SUBSTRATE_LEDGER.md",
    "docs/programme/ARCHITECTURE.md",
    "docs/programme/ROADMAP.md",
}
AUTHORIZED_PATHS = NEW_PATHS | LIVING_PATHS
RESULT_SOURCES = (
    "foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md",
    "verification/multistream_collection/reference.py",
    "verification/multistream_collection/checks.py",
    "verification/multistream_collection/run_checks.py",
    "verification/multistream_collection/README.md",
    ".github/workflows/statistical-decision-bridge.yml",
    ".github/workflows/family-replanning.yml",
)


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def require_commit(commit):
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    need(result.returncode == 0, f"required historical commit unavailable: {commit}")


def require_ancestor(ancestor, descendant, message):
    need(subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, descendant],
                        cwd=ROOT, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL).returncode == 0, message)


def parse_historical_result(raw):
    start = "STATISTICAL_DECISION_BRIDGE_RESULT_BEGIN\n"
    end = "\nSTATISTICAL_DECISION_BRIDGE_RESULT_END"
    need(start in raw and end in raw, "historical PR12 result markers missing")
    return json.loads(raw.split(start, 1)[1].split(end, 1)[0])


def enforce_change_scope(paths):
    paths = set(paths)
    protected = paths.intersection(FROZEN_PR12_SHA256)
    need(not protected, "protected PR12 source/result changed: " +
         ", ".join(sorted(protected)))
    unexpected = paths.difference(AUTHORIZED_PATHS)
    need(not unexpected, "unauthorized multistream path: " +
         ", ".join(sorted(unexpected)))


def verify_frozen_pr12_identities():
    actual = {}
    for path, expected in FROZEN_PR12_SHA256.items():
        digest = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        need(digest == expected, f"frozen PR12 identity changed: {path}")
        actual[path] = digest
    return actual


def verify_base_preservation():
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASE_MERGE],
        cwd=ROOT, text=True).splitlines()
    for path in paths:
        if path in LIVING_PATHS:
            if path.endswith("LEDGER.md"):
                before = subprocess.check_output(
                    ["git", "show", f"{BASE_MERGE}:{path}"], cwd=ROOT)
                need((ROOT / path).read_bytes().startswith(before),
                     f"ledger rewrite rather than append: {path}")
            continue
        before = subprocess.check_output(
            ["git", "show", f"{BASE_MERGE}:{path}"], cwd=ROOT)
        need((ROOT / path).read_bytes() == before,
             f"historical base file changed: {path}")


def expect_failure(operation, message):
    try:
        operation()
    except (RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError):
        return
    raise RuntimeError(message)


def source_hashes():
    return {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            for path in RESULT_SOURCES}


def verify_optional_record(actual_hashes):
    path = ROOT / "verification/multistream_collection/results.json"
    if not path.exists():
        return False
    record = json.loads(path.read_text())
    need(record.get("status") == "passed" and record.get("failed") == 0,
         "recorded multistream result is not a passing run")
    need(record.get("base_commit") == BASE_MERGE,
         "recorded multistream result has wrong base")
    need(record.get("source_sha256") == actual_hashes,
         "recorded multistream source identities are stale")
    groups = record.get("multistream", {}).get("groups", {})
    need(set(groups) == {f"M{index}" for index in range(1, 9)},
         "recorded multistream result is incomplete")
    return True


def run():
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    for commit in (BASE_MERGE, REPAIRED_PR12, PR12_HISTORICAL_BASE,
                   INITIAL_PR12):
        require_commit(commit)
    require_ancestor(REPAIRED_PR12, BASE_MERGE,
                     "repaired PR12 head is not an ancestor of the branch base")
    require_ancestor(PR12_HISTORICAL_BASE, REPAIRED_PR12,
                     "PR12 historical base is not an ancestor of repaired PR12")
    require_ancestor(INITIAL_PR12, REPAIRED_PR12,
                     "initial PR12 record is not an ancestor of repaired PR12")

    changed = subprocess.check_output(
        ["git", "diff", "--name-only", BASE_MERGE, "--"],
        cwd=ROOT, text=True).splitlines()
    enforce_change_scope(changed)
    frozen_pr12 = verify_frozen_pr12_identities()
    verify_base_preservation()

    def call(arguments):
        started = time.perf_counter()
        output = subprocess.check_output(
            [sys.executable] + arguments, cwd=ROOT, env=environment, text=True)
        return json.loads(output), time.perf_counter() - started

    scalar_observations, scalar_seconds = [], []
    multistream_observations, multistream_seconds = [], []
    for flags in ([], ["-O"]):
        observed, seconds = call(
            flags + ["verification/statistical_decision_bridge/checks.py"])
        scalar_observations.append(observed)
        scalar_seconds.append(seconds)
        observed, seconds = call(
            flags + ["verification/multistream_collection/checks.py"])
        multistream_observations.append(observed)
        multistream_seconds.append(seconds)

    for key in ("results", "rejections", "unfinished"):
        need(scalar_observations[0][key] == scalar_observations[1][key],
             f"normal and optimized scalar {key} differ")
    need(scalar_observations[0]["failed"] ==
         scalar_observations[1]["failed"] == 0,
         "current scalar checks failed")
    need(multistream_observations[0] == multistream_observations[1],
         "normal and optimized multistream observations differ")
    need(multistream_observations[0].get("status") == "passed",
         "current multistream checks failed")

    # Execute the complete repaired PR12 runner once in its exact historical context.
    # That unchanged runner recursively supplies the pinned PR10 preservation replay.
    historical_started = time.perf_counter()
    with tempfile.TemporaryDirectory() as temporary:
        subprocess.check_call(
            ["git", "clone", "--quiet", "--no-local", str(ROOT), temporary])
        subprocess.check_call(
            ["git", "update-ref", "refs/remotes/origin/main",
             PR12_HISTORICAL_BASE], cwd=temporary)
        subprocess.check_call(
            ["git", "checkout", "--quiet", REPAIRED_PR12], cwd=temporary)
        bound_base = subprocess.check_output(
            ["git", "rev-parse", "origin/main"], cwd=temporary,
            text=True).strip()
        checked_head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=temporary, text=True).strip()
        need(bound_base == PR12_HISTORICAL_BASE and checked_head == REPAIRED_PR12,
             "historical PR12 replay checkout/base binding failed")
        raw = subprocess.check_output(
            [sys.executable,
             "verification/statistical_decision_bridge/run_checks.py"],
            cwd=temporary, env=environment, text=True)
    historical_seconds = time.perf_counter() - historical_started
    historical = parse_historical_result(raw)
    need(historical["failed"] == 0 and
         historical["frozen_pr12_sha256"] == {
             "foundations/BELLMAN_ANYTIME_VALID_DATA_TO_DECISION.md":
                 FROZEN_PR12_SHA256[
                     "foundations/BELLMAN_ANYTIME_VALID_DATA_TO_DECISION.md"],
             "verification/statistical_decision_bridge/results.json":
                 FROZEN_PR12_SHA256[
                     "verification/statistical_decision_bridge/results.json"],
         }, "historical PR12 acceptance did not pass intact")

    # Current inherited files are byte-identical to the PR12 merge. Their complete execution is
    # attributed to the exact replay above; no recursive second historical chain is created.
    inherited_paths = (
        "foundations/BELLMAN_FAMILY_REPLANNING_AND_ROOT_GUARANTEES.md",
        "verification/family_replanning",
        "foundations/BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md",
        "verification/persistent_model_families",
        "verification/joint_law_completion",
    )
    need(subprocess.run(["git", "diff", "--quiet", BASE_MERGE, "HEAD", "--",
                         *inherited_paths], cwd=ROOT).returncode == 0,
         "current inherited mathematical sources changed")

    # Disposable negative controls demonstrate that orchestration errors remain fatal.
    enforce_change_scope({"docs/programme/ROADMAP.md"})
    expect_failure(
        lambda: enforce_change_scope({
            "verification/statistical_decision_bridge/reference.py"}),
        "protected PR12 source mutation was accepted")
    expect_failure(
        lambda: enforce_change_scope({
            "verification/statistical_decision_bridge/results.json"}),
        "protected PR12 result mutation was accepted")
    expect_failure(lambda: require_commit("0" * 40),
                   "missing historical replay commit was accepted")
    expect_failure(lambda: parse_historical_result("{}"),
                   "broken historical replay output was accepted")
    expect_failure(
        lambda: require_ancestor(BASE_MERGE, PR12_HISTORICAL_BASE,
                                 "intentional wrong historical base"),
        "wrong historical replay base was accepted")
    intentional_failure = (
        "import runpy; "
        "runpy.run_path('verification/multistream_collection/checks.py', "
        "run_name='__main__'); "
        "raise RuntimeError('intentional live mathematical failure')"
    )
    try:
        subprocess.check_output(
            [sys.executable, "-c", intentional_failure], cwd=ROOT,
            env=environment, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        need('"status": "passed"' in error.output,
             "intentional failure did not first execute current mathematics")
    else:
        raise RuntimeError("intentional current mathematical failure was suppressed")

    hashes = source_hashes()
    recorded_result_present = verify_optional_record(hashes)
    result = {
        "status": "passed",
        "failed": 0,
        "base_commit": BASE_MERGE,
        "repaired_pr12_head": REPAIRED_PR12,
        "pr12_historical_base": PR12_HISTORICAL_BASE,
        "initial_pr12_record": INITIAL_PR12,
        "executed_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "runtime": platform.python_version(),
        "execution": ("GitHub Actions" if os.environ.get("GITHUB_ACTIONS") == "true"
                      else "local"),
        "modes": ["normal", "-O"],
        "normal_optimized_equal": True,
        "scalar": {
            "passed_per_mode": scalar_observations[0]["passed"],
            "rejections_per_mode": scalar_observations[0]["rejections"],
            "unfinished_per_mode": scalar_observations[0]["unfinished"],
            "results": scalar_observations[0]["results"],
            "seconds_by_mode": scalar_seconds,
        },
        "multistream": multistream_observations[0],
        "multistream_seconds_by_mode": multistream_seconds,
        "support_profile": {
            "streams": 4,
            "observations_per_stream": 128,
            "transcript_events": 512,
            "actions": 4,
            "requested_precision_bits": 64,
            "out_of_profile": "unfinished-resource-refusal",
        },
        "source_sha256": hashes,
        "frozen_pr12_sha256": frozen_pr12,
        "recorded_result_present_and_current": recorded_result_present,
        "preservation": {
            "base_merge": BASE_MERGE,
            "base_files_preserved_except_named_living_routes": True,
            "current_inherited_sources_unchanged": True,
            "historical_runner": "passed-at-exact-repaired-pr12-head",
            "historical_origin_main": PR12_HISTORICAL_BASE,
            "historical_seconds": historical_seconds,
            "pr12_passed_per_mode": historical["passed_per_mode"],
            "pr10_inherited_runner":
                historical["preservation"]["inherited_runner"],
            "pr10_historical_files_preserved":
                historical["historical_files_preserved"],
        },
        "authorized_paths": sorted(changed),
        "negative_controls": {
            "living_programme_document_change": "accepted",
            "protected_pr12_source_change": "rejected",
            "protected_pr12_result_change": "rejected",
            "intentional_live_mathematical_failure": "rejected",
            "missing_historical_commit": "rejected",
            "broken_historical_result": "rejected",
            "wrong_historical_base": "rejected",
        },
        "limitations": [
            "Coverage is conditional on complete IID Bernoulli rows with fixed parameters.",
            "Transcript replay cannot detect concealed outcome filtering or prove physical sampling premises.",
            "Cross-row dependence is allowed for coverage, not for unsupported joint-event queries.",
            "Exact affine static risk is checked only on the retained parameter rectangle.",
            "Fixed checks are neither formal proof nor empirical validation, optimized collection, or authority to act.",
        ],
    }
    print("MULTISTREAM_COLLECTION_RESULT_BEGIN")
    print(json.dumps(result, sort_keys=True))
    print("MULTISTREAM_COLLECTION_RESULT_END")


if __name__ == "__main__":
    run()
