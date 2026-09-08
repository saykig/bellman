#!/usr/bin/env python3
"""Run longitudinal-causal checks and inherited Bellman acceptance."""
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
BASE = "0289a1660b21d86af3a897bb74270f562cb64dc9"
REVIEWED_PR19 = "f984ae5294a16c5189e6b49f9d1c828a8ab5514d"
PR19_MERGE = "0289a1660b21d86af3a897bb74270f562cb64dc9"
FROZEN = {
    "foundations/BELLMAN_FINITE_CAUSAL_IDENTIFICATION_AND_DECISION_CERTIFICATION.md":
        "e543bed5725932678f9134e5f658de32f72c8a508b799b9e5588585b98ece4ee",
    "verification/finite_causal_identification/results.json":
        "2687e889e2e7f9d4995a868f86fe879b9205a9b56a68a431a6dff06061685a5d",
    "foundations/BELLMAN_SEQUENTIAL_CERTIFICATE_COMPOSITION.md":
        "a974aa8e9753bcc1a4f5a5cd4d51c88040ae30bc40f98d1e837c71c6d711d0a4",
    "verification/sequential_certificates/reference.py":
        "99d0f1a3a32334cce826a7a582502122bc25e195f7024ed40f0c45753cbde1df",
    "verification/sequential_certificates/results.json":
        "047be866108cf3097e9e4ee598a80a7fb79dd50729b2547aa11af059dda7cd56",
    "foundations/BELLMAN_NEXT_MATHEMATICAL_BUILDOUT.md":
        "af631b49c3e411c57dbbc7baa145bdcc337e26f0ac2eebf7fa508ba840111a2e",
    "foundations/BELLMAN_NEXT_MATHEMATICAL_BUILDOUT_REVISED.md":
        "a54dfb0729759f1237817e516faf81e6d07e5907dadd8ddc6f1a1ba0fdaa27db",
    "reviews/BELLMAN_BUILDOUT_ADVERSARIAL_REVIEW.md":
        "643b12aa3313e16d2bc60768fa2b8fbf2df9c2facdab370a325faffde91c7eb9",
}
APPEND_ONLY = {
    "docs/history/records/FINDINGS_LEDGER.md",
    "docs/history/records/SUBSTRATE_LEDGER.md",
}
EDITABLE_EXISTING = APPEND_ONLY | {
    "README.md",
    "docs/programme/ROADMAP.md",
    "docs/programme/ARCHITECTURE.md",
    ".github/workflows/finite-causal-identification.yml",
}
NEW_PREFIX = "verification/longitudinal_causal_policy/"
NEW_PATHS = {
    "foundations/BELLMAN_TWO_STAGE_LONGITUDINAL_CAUSAL_POLICY_AND_SEQUENTIAL_BRIDGE.md",
    ".github/workflows/two-stage-longitudinal-causal-policy.yml",
}
SOURCES = (
    "foundations/BELLMAN_TWO_STAGE_LONGITUDINAL_CAUSAL_POLICY_AND_SEQUENTIAL_BRIDGE.md",
    "verification/longitudinal_causal_policy/reference.py",
    "verification/longitudinal_causal_policy/checks.py",
    "verification/longitudinal_causal_policy/run_checks.py",
    "verification/longitudinal_causal_policy/README.md",
    "README.md",
    "docs/programme/ROADMAP.md",
    "docs/programme/ARCHITECTURE.md",
    "docs/history/records/FINDINGS_LEDGER.md",
    "docs/history/records/SUBSTRATE_LEDGER.md",
    ".github/workflows/finite-causal-identification.yml",
    ".github/workflows/two-stage-longitudinal-causal-policy.yml",
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
    need(not unexpected, "change outside longitudinal-causal scope: " +
         ", ".join(unexpected))


def verify_base_preservation():
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASE], cwd=ROOT,
        text=True).splitlines()
    checked = 0
    for path in paths:
        before = git_bytes(BASE, path)
        current = ROOT / path
        need(current.is_file(), f"post-PR19 base file removed: {path}")
        if path in APPEND_ONLY:
            need(current.read_bytes().startswith(before),
                 f"append-only historical record rewritten: {path}")
        elif path in EDITABLE_EXISTING:
            pass
        else:
            need(current.read_bytes() == before,
                 f"post-PR19 file changed outside scope: {path}")
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
    path = ROOT / "verification/longitudinal_causal_policy/results.json"
    if not path.exists():
        return False
    record = json.loads(path.read_text())
    need(record.get("status") == "passed" and record.get("failed") == 0,
         "retained longitudinal result is not passing")
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
                         REVIEWED_PR19, PR19_MERGE], cwd=ROOT).returncode == 0,
         "reviewed PR19 head is not in its merge commit")
    need(subprocess.run(["git", "diff", "--quiet", REVIEWED_PR19,
                         PR19_MERGE, "--"], cwd=ROOT).returncode == 0,
         "PR19 merge tree differs from reviewed final head")
    need(subprocess.run(["git", "merge-base", "--is-ancestor", BASE, head],
                        cwd=ROOT).returncode == 0,
         "longitudinal-causal work is not based on post-PR19 main")
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
    longitudinal_runs, current, durations = [], {}, {}
    current_paths = (
        ("finite_causal", "verification/finite_causal_identification/checks.py"),
        ("unsafe", "verification/unsafe_set_reachability/checks.py"),
        ("corner", "verification/statistical_corner_models/checks.py"),
        ("persistent", "verification/persistent_model_families/checks.py"),
        ("sequential", "verification/sequential_certificates/checks.py"),
        ("multistream", "verification/multistream_collection/checks.py"),
        ("replanning", "verification/family_replanning/checks.py"),
    )
    for flags in modes:
        label = "-O" if flags else "normal"
        value, seconds = call_json(
            "verification/longitudinal_causal_policy/checks.py", flags)
        longitudinal_runs.append(value)
        durations[f"longitudinal_{label}"] = seconds
        for name, path in current_paths:
            value, seconds = call_json(path, flags)
            current.setdefault(name, []).append(value)
            durations[f"{name}_{label}"] = seconds

    first, second = dict(longitudinal_runs[0]), dict(longitudinal_runs[1])
    first.pop("optimized", None)
    second.pop("optimized", None)
    need(first == second and longitudinal_runs[0]["failed"] == 0,
         "longitudinal checks differ by optimization mode or failed")
    for name, runs in current.items():
        first, second = dict(runs[0]), dict(runs[1])
        first.pop("optimized", None)
        second.pop("optimized", None)
        need(first == second, f"current {name} checks differ by optimization mode")
        need(runs[0].get("failed") == runs[1].get("failed") == 0 or
             runs[0].get("status") == runs[1].get("status") == "passed",
             f"current {name} checks failed")

    joint_law = []
    with tempfile.TemporaryDirectory() as temporary:
        for flags in modes:
            label = "optimized" if flags else "normal"
            output = Path(temporary) / f"joint-law-{label}.json"
            started = time.perf_counter()
            subprocess.check_call(
                [sys.executable, *flags,
                 "verification/joint_law_completion/module_checks.py",
                 "--output", str(output)], cwd=ROOT, env=environment,
                stdout=subprocess.DEVNULL)
            durations[f"joint_law_{label}"] = time.perf_counter() - started
            joint_law.append(json.loads(output.read_text()))
    first, second = dict(joint_law[0]), dict(joint_law[1])
    first.pop("optimized", None)
    second.pop("optimized", None)
    need(first == second and joint_law[0]["passed_cases"] > 0,
         "active joint-law checks differ by optimization mode or failed")

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

    # Replay PR19 -> PR17 -> PR16 -> PR14 -> PR12 -> PR10 from PR19's merge.
    historical_started = time.perf_counter()
    with tempfile.TemporaryDirectory() as temporary:
        subprocess.check_call(["git", "clone", "--quiet", "--no-local",
                               str(ROOT), temporary])
        subprocess.check_call(["git", "checkout", "--quiet", PR19_MERGE],
                              cwd=temporary)
        raw = subprocess.check_output(
            [sys.executable,
             "verification/finite_causal_identification/run_checks.py"],
            cwd=temporary, env=environment, text=True)
    durations["historical_pr19_chain"] = time.perf_counter() - historical_started
    historical = parse_marked(raw, "FINITE_CAUSAL_IDENTIFICATION_RESULT_BEGIN",
                              "FINITE_CAUSAL_IDENTIFICATION_RESULT_END")
    need(historical["status"] == "passed" and historical["failed"] == 0 and
         historical["retained_result_present_and_source_bound"],
         "merged PR19 historical acceptance chain failed")

    hashes = source_hashes()
    retained_result = verify_optional_result(hashes)
    result = {
        "status": "passed",
        "failed": 0,
        "base_commit": BASE,
        "reviewed_pr19_head": REVIEWED_PR19,
        "pr19_merge_commit": PR19_MERGE,
        "executed_source_commit": head,
        "runtime": platform.python_version(),
        "execution": ("GitHub Actions" if
                      os.environ.get("GITHUB_ACTIONS") == "true" else "local"),
        "modes": ["normal", "-O"],
        "normal_optimized_equal": True,
        "passed_per_mode": longitudinal_runs[0]["passed"],
        "rejections_per_mode": longitudinal_runs[0]["rejections"],
        "results": longitudinal_runs[0]["results"],
        "current_checks": {
            "finite_causal_passed_per_mode": current["finite_causal"][0]["passed"],
            "unsafe_passed_per_mode": current["unsafe"][0]["passed"],
            "corner_passed_per_mode": current["corner"][0]["passed"],
            "persistent_passed_per_mode": current["persistent"][0]["passed"],
            "sequential_passed_per_mode": current["sequential"][0]["passed"],
            "multistream_status": current["multistream"][0]["status"],
            "replanning_passed_per_mode": current["replanning"][0]["passed"],
            "joint_law_passed_per_mode": joint_law[0]["passed_cases"],
            "history": history[0],
            "affected_relative_markdown_links_checked": markdown_links,
        },
        "preservation": {
            "pr19_merged_before_start": True,
            "pr19_merge_tree_matches_reviewed_head": True,
            "base_files_checked": preserved,
            "historical_pr19_runner": "passed-at-exact-merge",
            "historical_pr17_runner":
                historical["preservation"]["historical_pr17_runner"],
            "historical_pr16_runner":
                historical["preservation"]["historical_pr16_runner"],
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
            "The observational law and longitudinal causal premises are supplied, not empirically validated.",
            "Policy-specific identification does not imply every structural subject transition is identified.",
            "Binary A1/L1/A2/Y, two dates, 16 cells, and 32 deterministic policies only.",
            "No longitudinal partial identification, transport, safety/family composition, or authority claim.",
            "Analytical proofs plus bounded exact checks are not formal verification.",
            "No Writ or Decision Lab integration and no language migration.",
            "Enumeration remained at 32 policies, so no solver or language trigger was reached.",
        ],
    }
    print("LONGITUDINAL_CAUSAL_POLICY_RESULT_BEGIN")
    print(json.dumps(result, sort_keys=True))
    print("LONGITUDINAL_CAUSAL_POLICY_RESULT_END")


if __name__ == "__main__":
    run()
