"""Run family-replanning checks and the unchanged PR8 preservation chain."""
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
REVIEWED_PR8 = "59da8f5b9d57afbe2b8c31e78886378f4f456bec"
PR8_MERGE = "81eec793094bde8bb26fc88c3f4d6a99ef3ffdfe"
sys.path.insert(0, str(ROOT))
from verification.history_migration.checks import verify_historical_tree


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def run():
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    base = subprocess.check_output(["git", "merge-base", "HEAD", "origin/main"],
                                   cwd=ROOT, text=True).strip()

    def call(arguments):
        started = time.perf_counter()
        output = subprocess.check_output([sys.executable] + arguments, cwd=ROOT,
                                         env=environment, text=True)
        return output, time.perf_counter() - started

    observations, durations = [], []
    for flags in ([], ["-O"]):
        raw, seconds = call(flags + ["verification/family_replanning/checks.py"])
        observations.append(json.loads(raw))
        durations.append(seconds)
    need(observations[0]["results"] == observations[1]["results"],
         "normal and optimized observations differ")
    need(observations[0]["rejections"] == observations[1]["rejections"],
         "normal and optimized refusal counts differ")
    need(observations[0]["failed"] == observations[1]["failed"] == 0,
         "failed family-replanning checks")

    persistent_observations = []
    for flags in ([], ["-O"]):
        raw, _ = call(flags + ["verification/persistent_model_families/checks.py"])
        persistent_observations.append(json.loads(raw))
    need(persistent_observations[0]["results"] == persistent_observations[1]["results"] and
         persistent_observations[0]["rejections"] ==
         persistent_observations[1]["rejections"],
         "current persistent-family normal and optimized observations differ")

    # Later steering documents changed AGENTS.md after PR8, so PR8's own historical-byte
    # runner is executed at its exact merge commit in a temporary local clone. Current
    # inherited source preservation is checked independently below against the current base.
    started = time.perf_counter()
    with tempfile.TemporaryDirectory() as temporary:
        subprocess.check_call(["git", "clone", "--quiet", "--no-local", str(ROOT), temporary])
        subprocess.check_call(["git", "checkout", "--quiet", PR8_MERGE], cwd=temporary)
        raw = subprocess.check_output([
            sys.executable, "verification/persistent_model_families/run_checks.py"
        ], cwd=temporary, env=environment, text=True)
    preservation_seconds = time.perf_counter() - started
    persistent = json.loads(raw.split("PERSISTENT_FAMILY_RESULT_BEGIN\n", 1)[1]
                            .split("\nPERSISTENT_FAMILY_RESULT_END", 1)[0])

    need(subprocess.run(["git", "merge-base", "--is-ancestor", REVIEWED_PR8, PR8_MERGE],
                        cwd=ROOT).returncode == 0,
         "reviewed PR8 head is not an ancestor of its merge")
    need(subprocess.run(["git", "diff", "--quiet", REVIEWED_PR8, PR8_MERGE, "--"],
                        cwd=ROOT).returncode == 0,
         "PR8 merge tree differs from the reviewed head")
    need(subprocess.run(["git", "merge-base", "--is-ancestor", PR8_MERGE, base],
                        cwd=ROOT).returncode == 0,
         "PR8 merge is not an ancestor of the current base")
    inherited_paths = [
        "foundations/BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md",
        "verification/persistent_model_families/families.py",
        "verification/persistent_model_families/checks.py",
        "verification/persistent_model_families/results.json",
        "verification/persistent_model_families/README.md",
        ".github/workflows/persistent-model-families.yml",
    ]
    need(subprocess.run(["git", "diff", "--quiet", PR8_MERGE, base, "--",
                         *inherited_paths], cwd=ROOT).returncode == 0,
         "reviewed PR8 sources changed on the current base")
    preserved_files = verify_historical_tree(ROOT, base)

    sources = [
        "verification/family_replanning/replanning.py",
        "verification/family_replanning/checks.py",
        "verification/family_replanning/run_checks.py",
        "verification/family_replanning/README.md",
        "foundations/BELLMAN_FAMILY_REPLANNING_AND_ROOT_GUARANTEES.md",
        ".github/workflows/family-replanning.yml",
    ]
    result = {
        "base_commit": base,
        "reviewed_pr8_head": REVIEWED_PR8,
        "pr8_merge_commit": PR8_MERGE,
        "executed_commit": subprocess.check_output(["git", "rev-parse", "HEAD"],
                                                    cwd=ROOT, text=True).strip(),
        "runtime": platform.python_version(),
        "execution": "GitHub Actions" if os.environ.get("GITHUB_ACTIONS") == "true" else "local",
        "modes": ["normal", "-O"],
        "failed": 0,
        "passed_per_mode": observations[0]["passed"],
        "rejections_per_mode": observations[0]["rejections"],
        "seconds_by_mode": durations,
        "normal_optimized_equal": True,
        "results": observations[0]["results"],
        "source_sha256": {
            path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in sources
        },
        "historical_files_preserved": True,
        "historical_files_checked": preserved_files,
        "pr8_merge_tree_matches_reviewed_head": True,
        "pr8_sources_unchanged_on_current_base": True,
        "preservation_seconds": preservation_seconds,
        "preservation": {
            "persistent_passed_per_mode": persistent_observations[0]["passed"],
            "persistent_rejections_per_mode": persistent_observations[0]["rejections"],
            "current_persistent_normal_optimized_equal": True,
            "inherited_runner": "passed-at-pinned-pr8-merge",
            "accumulation_passed_per_mode":
                persistent["preservation"]["accumulation_passed_per_mode"],
            "transport_passed_per_mode":
                persistent["preservation"]["transport_passed_per_mode"],
            "sequential_passed_per_mode":
                persistent["preservation"]["sequential_passed_per_mode"],
            "pr4_repair_passed_per_mode":
                persistent["preservation"]["pr4_repair_passed_per_mode"],
            "joint_law_passed_per_mode":
                persistent["preservation"]["joint_law_passed_per_mode"],
            "historical_joint_law_observations_and_certificates_equal":
                persistent["preservation"][
                    "historical_joint_law_observations_and_certificates_equal"],
        },
        "limitations": [
            "Analytical finite proofs and authored exact cases, not formal verification or empirical coverage.",
            "Shared Fraction arithmetic and authorship; forward paths are a separate calculation route.",
            "One deterministic subtree splice only; no optimizer, model weights or dynamic-consistency theorem.",
        ],
    }
    print("FAMILY_REPLANNING_RESULT_BEGIN")
    print(json.dumps(result, sort_keys=True))
    print("FAMILY_REPLANNING_RESULT_END")


if __name__ == "__main__":
    run()
