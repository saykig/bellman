"""Run persistent-family checks and the unchanged PR7 preservation command."""
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "9761cd0ce99be6fb6b2dcddc89951960a4a0df34"
REVIEWED_PR7 = "5c567646e0dec648bfdc9302025b495e8afaeb6e"


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def run():
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")

    def call(arguments):
        started = time.perf_counter()
        output = subprocess.check_output([sys.executable] + arguments, cwd=ROOT,
                                         env=environment, text=True)
        return output, time.perf_counter() - started

    observations, durations = [], []
    for flags in ([], ["-O"]):
        raw, seconds = call(flags + ["verification/persistent_model_families/checks.py"])
        observations.append(json.loads(raw))
        durations.append(seconds)
    need(observations[0]["results"] == observations[1]["results"],
         "normal and optimized observations differ")
    need(observations[0]["rejections"] == observations[1]["rejections"],
         "normal and optimized rejection counts differ")
    need(observations[0]["failed"] == observations[1]["failed"] == 0,
         "failed persistent-family checks")

    raw, preservation_seconds = call(["verification/certificate_accumulation/run_checks.py"])
    accumulation = json.loads(raw.split("ACCUMULATION_RESULT_BEGIN\n", 1)[1]
                              .split("\nACCUMULATION_RESULT_END", 1)[0])

    need(subprocess.run(["git", "merge-base", "--is-ancestor", REVIEWED_PR7, BASE],
                        cwd=ROOT).returncode == 0, "reviewed PR7 head is not an ancestor of base")
    need(subprocess.run(["git", "diff", "--quiet", REVIEWED_PR7, BASE, "--"],
                        cwd=ROOT).returncode == 0, "PR7 merge base differs from reviewed head tree")
    paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE],
                                    cwd=ROOT, text=True).splitlines()
    mutable = ("README.md", "SUBSTRATE_LEDGER.md", "FINDINGS_LEDGER.md")
    for path in paths:
        before = subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)
        now = (ROOT / path).read_bytes()
        if path not in mutable:
            need(before == now, f"historical change: {path}")
        elif path.endswith("LEDGER.md"):
            need(now.startswith(before), f"current pointer/ledger rewrite: {path}")

    sources = [
        "verification/persistent_model_families/families.py",
        "verification/persistent_model_families/checks.py",
        "verification/persistent_model_families/run_checks.py",
        "verification/persistent_model_families/README.md",
        "foundations/BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md",
        ".github/workflows/persistent-model-families.yml",
    ]
    result = {
        "base_commit": BASE,
        "reviewed_pr7_head": REVIEWED_PR7,
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
        "pr7_merge_tree_matches_reviewed_head": True,
        "preservation_seconds": preservation_seconds,
        "preservation": {
            "accumulation_passed_per_mode": accumulation["passed_per_mode"],
            "accumulation_rejections_per_mode": accumulation["rejections_per_mode"],
            "transport_passed_per_mode": accumulation["preservation"]["passed_per_mode"],
            "transport_rejections_per_mode": accumulation["preservation"]["rejections_per_mode"],
            "sequential_passed_per_mode": accumulation["preservation"]["sequential_passed_per_mode"],
            "pr4_repair_passed_per_mode": accumulation["preservation"]["pr4_repair_passed_per_mode"],
            "joint_law_passed_per_mode": accumulation["preservation"]["joint_law_passed_per_mode"],
            "historical_joint_law_observations_and_certificates_equal":
                accumulation["preservation"]["historical_joint_law_observations_and_certificates_equal"],
        },
        "limitations": [
            "Finite analytical proofs and fixed cases, not formal verification or empirical coverage.",
            "Shared Fraction arithmetic and authorship; the forward oracle is a separate calculation path.",
            "Deterministic policies only; no prior, randomized-policy optimum or dynamic-consistency claim.",
        ],
    }
    print("PERSISTENT_FAMILY_RESULT_BEGIN")
    print(json.dumps(result, sort_keys=True))
    print("PERSISTENT_FAMILY_RESULT_END")


if __name__ == "__main__":
    run()
