#!/usr/bin/env python3
"""Run finite-causal checks and the inherited Bellman acceptance chain."""
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
BASE = "0f8a7e2dc1e420d9ba26c993632c1ec690e1a804"
REVIEWED_PR17 = "afad4c594efdef1c0abc05376464f4325efd24f0"
FROZEN = {
    "foundations/BELLMAN_UNSAFE_SET_REACHABILITY_AND_CONSTRAINED_SELECTION.md":
        "28f038fd633daf7694f31885923fa90ec8926619e8dda497c3df4605036e257d",
    "verification/unsafe_set_reachability/results.json":
        "b672e9a238e210081dacff3257c2348d30c23298f7d317e66a2ea177adbcc73a",
    "foundations/BELLMAN_NEXT_MATHEMATICAL_BUILDOUT.md":
        "af631b49c3e411c57dbbc7baa145bdcc337e26f0ac2eebf7fa508ba840111a2e",
    "foundations/BELLMAN_NEXT_MATHEMATICAL_BUILDOUT_REVISED.md":
        "a54dfb0729759f1237817e516faf81e6d07e5907dadd8ddc6f1a1ba0fdaa27db",
    "reviews/BELLMAN_BUILDOUT_ADVERSARIAL_REVIEW.md":
        "643b12aa3313e16d2bc60768fa2b8fbf2df9c2facdab370a325faffde91c7eb9",
    "verification/joint_law_completion/joint_law.py":
        "ade9182eb5d3daca2f6811968140c33cbcbfd81058c3c1e8cbf3528dff403014",
    "verification/joint_law_completion/module_results.json":
        "14af2b39a494c2cce524c9f1b393de5a1ce4fa94aef2f073cde4a15a5783c99d",
}
APPEND_ONLY = {
    "docs/history/records/FINDINGS_LEDGER.md",
    "docs/history/records/SUBSTRATE_LEDGER.md",
}
EDITABLE_EXISTING = APPEND_ONLY | {
    "README.md",
    "docs/programme/ROADMAP.md",
    "docs/programme/ARCHITECTURE.md",
    ".github/workflows/unsafe-set-reachability.yml",
}
NEW_PREFIX = "verification/finite_causal_identification/"
NEW_PATHS = {
    "foundations/BELLMAN_FINITE_CAUSAL_IDENTIFICATION_AND_DECISION_CERTIFICATION.md",
    ".github/workflows/finite-causal-identification.yml",
}
SOURCES = (
    "foundations/BELLMAN_FINITE_CAUSAL_IDENTIFICATION_AND_DECISION_CERTIFICATION.md",
    "verification/finite_causal_identification/reference.py",
    "verification/finite_causal_identification/checks.py",
    "verification/finite_causal_identification/run_checks.py",
    "verification/finite_causal_identification/README.md",
    "README.md",
    "docs/programme/ROADMAP.md",
    "docs/programme/ARCHITECTURE.md",
    "docs/history/records/FINDINGS_LEDGER.md",
    "docs/history/records/SUBSTRATE_LEDGER.md",
    ".github/workflows/unsafe-set-reachability.yml",
    ".github/workflows/finite-causal-identification.yml",
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
    need(not unexpected, "change outside finite-causal scope: " +
         ", ".join(unexpected))


def verify_base_preservation():
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASE], cwd=ROOT,
        text=True).splitlines()
    checked = 0
    for path in paths:
        before = git_bytes(BASE, path)
        current = ROOT / path
        need(current.is_file(), f"merged PR17 base file removed: {path}")
        if path in APPEND_ONLY:
            need(current.read_bytes().startswith(before),
                 f"append-only historical record rewritten: {path}")
        elif path in EDITABLE_EXISTING:
            pass
        else:
            need(current.read_bytes() == before,
                 f"merged PR17 file changed outside scope: {path}")
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
    path = ROOT / "verification/finite_causal_identification/results.json"
    if not path.exists():
        return False
    record = json.loads(path.read_text())
    need(record.get("status") == "passed" and record.get("failed") == 0,
         "retained causal result is not passing")
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
                         REVIEWED_PR17, BASE], cwd=ROOT).returncode == 0,
         "reviewed PR17 head is not in the required base")
    need(subprocess.run(["git", "diff", "--quiet", REVIEWED_PR17, BASE, "--"],
                        cwd=ROOT).returncode == 0,
         "PR17 merge tree differs from reviewed final head")
    need(subprocess.run(["git", "merge-base", "--is-ancestor", BASE, head],
                        cwd=ROOT).returncode == 0,
         "finite-causal work is not based on merged PR17 main")
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
    causal_runs, current, durations = [], {}, {}
    current_paths = (
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
            "verification/finite_causal_identification/checks.py", flags)
        causal_runs.append(value)
        durations[f"causal_{label}"] = seconds
        for name, path in current_paths:
            value, seconds = call_json(path, flags)
            current.setdefault(name, []).append(value)
            durations[f"{name}_{label}"] = seconds

    first = dict(causal_runs[0])
    second = dict(causal_runs[1])
    first.pop("optimized", None)
    second.pop("optimized", None)
    need(first == second and causal_runs[0]["failed"] == 0,
         "finite causal checks differ by optimization mode or failed")
    for name, runs in current.items():
        first, second = dict(runs[0]), dict(runs[1])
        first.pop("optimized", None)
        second.pop("optimized", None)
        need(first == second, f"current {name} checks differ by optimization mode")
        need(runs[0].get("failed") == runs[1].get("failed") == 0 or
             runs[0].get("status") == runs[1].get("status") == "passed",
             f"current {name} checks failed")

    # The active generic exact compatibility code remains independently green.
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

    # Replay PR17 -> PR16 -> PR14 -> PR12 -> PR10 from PR17's exact merge tree.
    historical_started = time.perf_counter()
    with tempfile.TemporaryDirectory() as temporary:
        subprocess.check_call(["git", "clone", "--quiet", "--no-local",
                               str(ROOT), temporary])
        subprocess.check_call(["git", "checkout", "--quiet", BASE],
                              cwd=temporary)
        raw = subprocess.check_output(
            [sys.executable,
             "verification/unsafe_set_reachability/run_checks.py"],
            cwd=temporary, env=environment, text=True)
    durations["historical_pr17_chain"] = time.perf_counter() - historical_started
    historical = parse_marked(raw, "UNSAFE_SET_REACHABILITY_RESULT_BEGIN",
                              "UNSAFE_SET_REACHABILITY_RESULT_END")
    need(historical["status"] == "passed" and historical["failed"] == 0 and
         historical["retained_result_present_and_source_bound"],
         "merged PR17 historical acceptance chain failed")

    hashes = source_hashes()
    retained_result = verify_optional_result(hashes)
    result = {
        "status": "passed",
        "failed": 0,
        "base_commit": BASE,
        "reviewed_pr17_head": REVIEWED_PR17,
        "executed_source_commit": head,
        "runtime": platform.python_version(),
        "execution": ("GitHub Actions" if
                      os.environ.get("GITHUB_ACTIONS") == "true" else "local"),
        "modes": ["normal", "-O"],
        "normal_optimized_equal": True,
        "passed_per_mode": causal_runs[0]["passed"],
        "rejections_per_mode": causal_runs[0]["rejections"],
        "results": causal_runs[0]["results"],
        "current_checks": {
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
            "pr17_merged_before_start": True,
            "pr17_merge_tree_matches_reviewed_head": True,
            "base_files_checked": preserved,
            "historical_pr17_runner": "passed-at-exact-merge",
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
            "Causal assumptions and the observational law are supplied, not empirically validated.",
            "Analytical proofs plus bounded exact checks are not formal verification.",
            "Binary A/Y, at most four Z categories, eight types, and six restrictions only.",
            "Unsupported nonlinear causal restrictions are never silently linearized.",
            "No causal discovery, transport, sequential-treatment, safety, or authority claim.",
            "No Writ or Decision Lab integration and no language migration.",
            "Complete enumeration stayed at at most 70 bases, so no solver trigger was reached.",
        ],
    }
    print("FINITE_CAUSAL_IDENTIFICATION_RESULT_BEGIN")
    print(json.dumps(result, sort_keys=True))
    print("FINITE_CAUSAL_IDENTIFICATION_RESULT_END")


if __name__ == "__main__":
    run()
