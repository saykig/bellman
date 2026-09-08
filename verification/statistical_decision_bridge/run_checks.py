"""Run the statistical bridge and the unchanged PR #10 preservation chain."""
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
REVIEWED_PR10 = "82d286c591750a2229664d935a6f9820340233df"
PR10_MERGE = "2e8d99cdcf289eabb63df15086eaa68251a359f1"
REVIEWED_PR12 = "fbfbc182a05952198d9ce9dc6ef4e9a395eaf3c6"
FROZEN_PR12_SHA256 = {
    "foundations/BELLMAN_ANYTIME_VALID_DATA_TO_DECISION.md":
        "bcbb6b7f1f16027a726176bbef69f39013bb7ec6ae55fc79ab23fe0d83e952c2",
    "verification/statistical_decision_bridge/results.json":
        "2d937135ea0610da69ba09cd477934ec0b4e88843c1bbcf3212311ce079a5b13",
}
sys.path.insert(0, str(ROOT))
from verification.history_migration.checks import verify_historical_tree
AUTHORIZED_REPAIR_PATHS = {
    ".github/workflows/history-migration.yml",
    ".github/workflows/family-replanning.yml",
    ".github/workflows/statistical-decision-bridge.yml",
    "AGENTS.md",
    "FINDINGS_LEDGER.md",
    "LEGACY_ARCHIVE_STATUS.md",
    "MATH_ARCHIVE_LEDGER.md",
    "README.md",
    "SUBSTRATE_LEDGER.md",
    "docs/history/PATH_DEPENDENCY_AUDIT.md",
    "docs/history/README.md",
    "docs/history/records/CLASSIFICATION.md",
    "docs/history/records/FINDINGS_LEDGER.md",
    "docs/history/records/LEGACY_ARCHIVE_STATUS.md",
    "docs/history/records/MATH_ARCHIVE_LEDGER.md",
    "docs/history/records/SUBSTRATE_LEDGER.md",
    "docs/history/records/migration_manifest.json",
    "docs/history/releases/anytime-data-decision.md",
    "docs/history/releases/joint-law-certificates.md",
    "docs/history/releases/kl-closure.md",
    "docs/history/releases/manifest.json",
    "docs/history/releases/persistent-model-families.md",
    "docs/history/releases/sequential-certificates.md",
    "docs/history/releases/substrate-v1.1.md",
    "docs/programme/ARCHITECTURE.md",
    "docs/programme/ROADMAP.md",
    "verification/certificate_accumulation/run_checks.py",
    "verification/certificate_transport/run_checks.py",
    "verification/family_replanning/run_checks.py",
    "verification/history_migration/README.md",
    "verification/history_migration/checks.py",
    "verification/persistent_model_families/run_checks.py",
    "verification/sequential_certificates/run_checks.py",
    "verification/substrate_v1/README.md",
    "verification/statistical_decision_bridge/ACCEPTANCE_HARDENING.md",
    "verification/statistical_decision_bridge/acceptance_hardening_results.json",
    "verification/statistical_decision_bridge/README.md",
    "verification/statistical_decision_bridge/checks.py",
    "verification/statistical_decision_bridge/reference.py",
    "verification/statistical_decision_bridge/run_checks.py",
}


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def parse_historical_result(raw):
    start = "FAMILY_REPLANNING_RESULT_BEGIN\n"
    end = "\nFAMILY_REPLANNING_RESULT_END"
    need(start in raw and end in raw, "historical replay result markers missing")
    return json.loads(raw.split(start, 1)[1].split(end, 1)[0])


def require_commit(commit):
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=ROOT,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    need(result.returncode == 0, f"required historical commit unavailable: {commit}")


def enforce_change_scope(paths):
    paths = set(paths)
    frozen = paths.intersection(FROZEN_PR12_SHA256)
    need(not frozen, "frozen PR12 mathematical evidence changed: " + ", ".join(sorted(frozen)))
    unexpected = paths.difference(AUTHORIZED_REPAIR_PATHS)
    need(not unexpected, "unauthorized PR12 hardening path: " +
         ", ".join(sorted(unexpected)))


def verify_frozen_pr12_identities():
    actual = {}
    for path, expected in FROZEN_PR12_SHA256.items():
        digest = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        need(digest == expected, f"frozen PR12 identity changed: {path}")
        actual[path] = digest
    return actual


def expect_failure(operation, message):
    try:
        operation()
    except (RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError):
        return
    raise RuntimeError(message)


def run():
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    base = subprocess.check_output(
        ["git", "merge-base", "HEAD", "origin/main"], cwd=ROOT, text=True).strip()

    def call(arguments):
        started = time.perf_counter()
        output = subprocess.check_output([sys.executable] + arguments, cwd=ROOT,
                                         env=environment, text=True)
        return output, time.perf_counter() - started

    changed = subprocess.check_output(
        ["git", "diff", "--name-only", REVIEWED_PR12, "--"],
        cwd=ROOT, text=True).splitlines()
    enforce_change_scope(changed)
    frozen_pr12 = verify_frozen_pr12_identities()

    observations, durations = [], []
    for flags in ([], ["-O"]):
        raw, seconds = call(flags + ["verification/statistical_decision_bridge/checks.py"])
        observations.append(json.loads(raw))
        durations.append(seconds)
    for key in ("results", "rejections", "unfinished"):
        need(observations[0][key] == observations[1][key],
             f"normal and optimized {key} differ")
    need(observations[0]["failed"] == observations[1]["failed"] == 0,
         "failed statistical bridge checks")

    current_replanning = []
    for flags in ([], ["-O"]):
        raw, _ = call(flags + ["verification/family_replanning/checks.py"])
        current_replanning.append(json.loads(raw))
    need(current_replanning[0]["results"] == current_replanning[1]["results"] and
         current_replanning[0]["rejections"] == current_replanning[1]["rejections"] and
         current_replanning[0]["failed"] == current_replanning[1]["failed"] == 0,
         "current family-replanning preservation checks failed")

    current_persistent = []
    for flags in ([], ["-O"]):
        raw, _ = call(flags + ["verification/persistent_model_families/checks.py"])
        current_persistent.append(json.loads(raw))
    need(current_persistent[0]["results"] == current_persistent[1]["results"] and
         current_persistent[0]["rejections"] ==
         current_persistent[1]["rejections"] and
         current_persistent[0]["failed"] == current_persistent[1]["failed"] == 0,
         "current persistent-family preservation checks failed")

    # Authorized living programme-document changes are outside PR #10's historical domain.
    # Execute that complete historical runner at its exact merge, then check current inherited
    # source identities separately below.
    started = time.perf_counter()
    require_commit(PR10_MERGE)
    with tempfile.TemporaryDirectory() as temporary:
        subprocess.check_call(["git", "clone", "--quiet", "--no-local", str(ROOT), temporary])
        # A GitHub branch-head checkout can clone locally without carrying an
        # origin/main remote-tracking ref.  The historical runner resolves its
        # own base through that name, so bind it to the exact pinned merge in
        # this disposable clone; no historical source or check is bypassed.
        subprocess.check_call(["git", "update-ref", "refs/remotes/origin/main",
                               PR10_MERGE], cwd=temporary)
        subprocess.check_call(["git", "checkout", "--quiet", PR10_MERGE], cwd=temporary)
        raw = subprocess.check_output([
            sys.executable, "verification/family_replanning/run_checks.py"
        ], cwd=temporary, env=environment, text=True)
    preservation_seconds = time.perf_counter() - started
    inherited = parse_historical_result(raw)

    need(subprocess.run(["git", "merge-base", "--is-ancestor", REVIEWED_PR10,
                         PR10_MERGE], cwd=ROOT).returncode == 0,
         "reviewed PR #10 head is not an ancestor of its merge")
    need(subprocess.run(["git", "diff", "--quiet", REVIEWED_PR10, PR10_MERGE, "--"],
                        cwd=ROOT).returncode == 0,
         "PR #10 merge tree differs from reviewed head")
    need(subprocess.run(["git", "merge-base", "--is-ancestor", PR10_MERGE, base],
                        cwd=ROOT).returncode == 0,
         "PR #10 merge is not an ancestor of current base")
    inherited_paths = [
        "foundations/BELLMAN_FAMILY_REPLANNING_AND_ROOT_GUARANTEES.md",
        "verification/family_replanning",
        "foundations/BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md",
        "verification/persistent_model_families",
        "verification/joint_law_completion/joint_law.py",
    ]
    need(subprocess.run(["git", "diff", "--quiet", PR10_MERGE, base, "--",
                         *inherited_paths], cwd=ROOT).returncode == 0,
         "reviewed inherited mathematical sources changed on current base")

    preserved_files = verify_historical_tree(ROOT, base)

    # Disposable negative controls prove that orchestration failures remain failures.
    enforce_change_scope({"docs/programme/ROADMAP.md"})
    expect_failure(
        lambda: enforce_change_scope({
            "foundations/BELLMAN_ANYTIME_VALID_DATA_TO_DECISION.md"}),
        "protected mathematical source mutation was accepted")
    expect_failure(
        lambda: enforce_change_scope({
            "verification/statistical_decision_bridge/results.json"}),
        "protected recorded-result mutation was accepted")
    expect_failure(lambda: require_commit("0" * 40),
                   "missing historical replay commit was accepted")
    expect_failure(lambda: parse_historical_result("{}"),
                   "broken historical replay output was accepted")
    intentional_failure = (
        "import runpy, sys; "
        "sys.path.insert(0, 'verification/statistical_decision_bridge'); "
        "runpy.run_path('verification/statistical_decision_bridge/checks.py', "
        "run_name='__main__'); "
        "raise RuntimeError('intentional live mathematical check failure')"
    )
    try:
        subprocess.check_output(
            [sys.executable, "-c", intentional_failure], cwd=ROOT,
            env=environment, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        need('"failed": 0' in error.output,
             "intentional live failure did not first execute current mathematics")
    else:
        raise RuntimeError("intentional current mathematical failure was suppressed")

    sources = [
        "verification/statistical_decision_bridge/reference.py",
        "verification/statistical_decision_bridge/checks.py",
        "verification/statistical_decision_bridge/run_checks.py",
        "verification/statistical_decision_bridge/README.md",
        "foundations/BELLMAN_ANYTIME_VALID_DATA_TO_DECISION.md",
        ".github/workflows/statistical-decision-bridge.yml",
        ".github/workflows/family-replanning.yml",
        "verification/statistical_decision_bridge/ACCEPTANCE_HARDENING.md",
    ]
    result = {
        "base_commit": base,
        "reviewed_pr10_head": REVIEWED_PR10,
        "pr10_merge_commit": PR10_MERGE,
        "reviewed_pr12_head": REVIEWED_PR12,
        "executed_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "runtime": platform.python_version(),
        "execution": "GitHub Actions" if os.environ.get("GITHUB_ACTIONS") == "true" else "local",
        "modes": ["normal", "-O"],
        "failed": 0,
        "passed_per_mode": observations[0]["passed"],
        "rejections_per_mode": observations[0]["rejections"],
        "unfinished_per_mode": observations[0]["unfinished"],
        "seconds_by_mode": durations,
        "normal_optimized_equal": True,
        "receiver_support_contract": {
            "observations": 128,
            "actions": 4,
            "requested_precision_bits": 64,
            "disposition": "unfinished-resource-refusal",
        },
        "results": observations[0]["results"],
        "source_sha256": {
            path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in sources
        },
        "historical_files_preserved": True,
        "historical_files_checked": preserved_files,
        "frozen_pr12_sha256": frozen_pr12,
        "authorized_hardening_paths": sorted(changed),
        "pr10_merge_tree_matches_reviewed_head": True,
        "pr10_sources_unchanged_on_current_base": True,
        "programme_documents_are_authorized_living_changes": True,
        "preservation_seconds": preservation_seconds,
        "preservation": {
            "current_family_replanning_passed_per_mode": current_replanning[0]["passed"],
            "current_family_replanning_rejections_per_mode":
                current_replanning[0]["rejections"],
            "current_family_replanning_normal_optimized_equal": True,
            "current_persistent_passed_per_mode": current_persistent[0]["passed"],
            "current_persistent_rejections_per_mode":
                current_persistent[0]["rejections"],
            "current_persistent_normal_optimized_equal": True,
            "inherited_runner": "passed-at-pinned-pr10-merge",
            "persistent_passed_per_mode":
                inherited["preservation"]["persistent_passed_per_mode"],
            "accumulation_passed_per_mode":
                inherited["preservation"]["accumulation_passed_per_mode"],
            "transport_passed_per_mode":
                inherited["preservation"]["transport_passed_per_mode"],
            "sequential_passed_per_mode":
                inherited["preservation"]["sequential_passed_per_mode"],
            "pr4_repair_passed_per_mode":
                inherited["preservation"]["pr4_repair_passed_per_mode"],
            "joint_law_passed_per_mode":
                inherited["preservation"]["joint_law_passed_per_mode"],
            "historical_joint_law_observations_and_certificates_equal":
                inherited["preservation"][
                    "historical_joint_law_observations_and_certificates_equal"],
        },
        "negative_controls": {
            "authorized_programme_document_change": "accepted",
            "protected_mathematical_source_change": "rejected",
            "protected_recorded_result_change": "rejected",
            "intentional_live_mathematical_failure": "rejected",
            "missing_historical_commit": "rejected",
            "broken_historical_result": "rejected",
        },
        "limitations": [
            "Coverage is conditional on an IID Bernoulli stream with one fixed real parameter.",
            "Finite authored checks and analytical proofs are not empirical validation or formal verification.",
            "Static actions, at most 128 observations, four actions and 64 bisection bits; no adaptive sampling or sequential control.",
        ],
    }
    print("STATISTICAL_DECISION_BRIDGE_RESULT_BEGIN")
    print(json.dumps(result, sort_keys=True))
    print("STATISTICAL_DECISION_BRIDGE_RESULT_END")


if __name__ == "__main__":
    run()
