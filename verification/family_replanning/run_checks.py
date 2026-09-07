"""Run family-replanning checks and the unchanged PR8 preservation chain."""
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "81eec793094bde8bb26fc88c3f4d6a99ef3ffdfe"
REVIEWED_PR8 = "59da8f5b9d57afbe2b8c31e78886378f4f456bec"


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
        raw, seconds = call(flags + ["verification/family_replanning/checks.py"])
        observations.append(json.loads(raw))
        durations.append(seconds)
    need(observations[0]["results"] == observations[1]["results"],
         "normal and optimized observations differ")
    need(observations[0]["rejections"] == observations[1]["rejections"],
         "normal and optimized refusal counts differ")
    need(observations[0]["failed"] == observations[1]["failed"] == 0,
         "failed family-replanning checks")

    raw, preservation_seconds = call([
        "verification/persistent_model_families/run_checks.py"
    ])
    persistent = json.loads(raw.split("PERSISTENT_FAMILY_RESULT_BEGIN\n", 1)[1]
                            .split("\nPERSISTENT_FAMILY_RESULT_END", 1)[0])

    need(subprocess.run(["git", "merge-base", "--is-ancestor", REVIEWED_PR8, BASE],
                        cwd=ROOT).returncode == 0,
         "reviewed PR8 head is not an ancestor of the base")
    need(subprocess.run(["git", "diff", "--quiet", REVIEWED_PR8, BASE, "--"],
                        cwd=ROOT).returncode == 0,
         "PR8 merge tree differs from the reviewed head")
    paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE],
                                    cwd=ROOT, text=True).splitlines()
    mutable = ("README.md", "SUBSTRATE_LEDGER.md", "FINDINGS_LEDGER.md")
    for path in paths:
        before = subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)
        now = (ROOT / path).read_bytes()
        if path not in mutable:
            need(before == now, f"historical change: {path}")
        elif path.endswith("LEDGER.md"):
            need(now.startswith(before), f"ledger rewrite rather than append: {path}")

    sources = [
        "verification/family_replanning/replanning.py",
        "verification/family_replanning/checks.py",
        "verification/family_replanning/run_checks.py",
        "verification/family_replanning/README.md",
        "foundations/BELLMAN_FAMILY_REPLANNING_AND_ROOT_GUARANTEES.md",
        ".github/workflows/family-replanning.yml",
    ]
    result = {
        "base_commit": BASE,
        "reviewed_pr8_head": REVIEWED_PR8,
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
        "pr8_merge_tree_matches_reviewed_head": True,
        "preservation_seconds": preservation_seconds,
        "preservation": {
            "persistent_passed_per_mode": persistent["passed_per_mode"],
            "persistent_rejections_per_mode": persistent["rejections_per_mode"],
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
