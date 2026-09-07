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


def need(ok, message):
    if not ok:
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

    # Authorized living programme-document changes are outside PR #10's historical domain.
    # Execute that complete historical runner at its exact merge, then check current inherited
    # source identities separately below.
    started = time.perf_counter()
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
    inherited = json.loads(raw.split("FAMILY_REPLANNING_RESULT_BEGIN\n", 1)[1]
                           .split("\nFAMILY_REPLANNING_RESULT_END", 1)[0])

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
        ".github/workflows/family-replanning.yml",
        "foundations/BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md",
        "verification/persistent_model_families",
        "verification/joint_law_completion/joint_law.py",
    ]
    need(subprocess.run(["git", "diff", "--quiet", PR10_MERGE, base, "--",
                         *inherited_paths], cwd=ROOT).returncode == 0,
         "reviewed inherited mathematical sources changed on current base")

    allowed_living = {
        "README.md",
        "SUBSTRATE_LEDGER.md",
        "FINDINGS_LEDGER.md",
        "docs/programme/ROADMAP.md",
        "docs/programme/ARCHITECTURE.md",
    }
    paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", base],
                                    cwd=ROOT, text=True).splitlines()
    for path in paths:
        before = subprocess.check_output(["git", "show", f"{base}:{path}"], cwd=ROOT)
        now = (ROOT / path).read_bytes()
        if path not in allowed_living:
            need(before == now, f"historical change: {path}")
        elif path.endswith("LEDGER.md"):
            need(now.startswith(before), f"ledger rewrite rather than append: {path}")

    sources = [
        "verification/statistical_decision_bridge/reference.py",
        "verification/statistical_decision_bridge/checks.py",
        "verification/statistical_decision_bridge/run_checks.py",
        "verification/statistical_decision_bridge/README.md",
        "foundations/BELLMAN_ANYTIME_VALID_DATA_TO_DECISION.md",
        ".github/workflows/statistical-decision-bridge.yml",
    ]
    result = {
        "base_commit": base,
        "reviewed_pr10_head": REVIEWED_PR10,
        "pr10_merge_commit": PR10_MERGE,
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
        "results": observations[0]["results"],
        "source_sha256": {
            path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in sources
        },
        "historical_files_preserved": True,
        "pr10_merge_tree_matches_reviewed_head": True,
        "pr10_sources_unchanged_on_current_base": True,
        "programme_documents_are_authorized_living_changes": True,
        "preservation_seconds": preservation_seconds,
        "preservation": {
            "current_family_replanning_passed_per_mode": current_replanning[0]["passed"],
            "current_family_replanning_rejections_per_mode":
                current_replanning[0]["rejections"],
            "current_family_replanning_normal_optimized_equal": True,
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
