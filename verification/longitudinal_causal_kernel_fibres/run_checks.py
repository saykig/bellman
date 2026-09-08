#!/usr/bin/env python3
"""Run kernel-fibre checks plus current and historical Bellman acceptance."""
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
BASE = "cea4e1a47cb91c1f3917490350deab53d2976908"
REVIEWED_PR20 = "c5c6782fcc74d523701b7d67c0ff476130747f6c"
PR20_MERGE = BASE
FROZEN = {
    "foundations/BELLMAN_TWO_STAGE_LONGITUDINAL_CAUSAL_POLICY_AND_SEQUENTIAL_BRIDGE.md":
        "0fa7a39c19e723f3c4903e56a198a02c4bd97a10a9303da2bc14c145f7c60422",
    "verification/longitudinal_causal_policy/results.json":
        "f7a08484ae260667ba8e511ad333dfce40ff55078ed21b2440cddccd3e008c21",
    "foundations/BELLMAN_FINITE_CAUSAL_IDENTIFICATION_AND_DECISION_CERTIFICATION.md":
        "e543bed5725932678f9134e5f658de32f72c8a508b799b9e5588585b98ece4ee",
    "verification/finite_causal_identification/results.json":
        "2687e889e2e7f9d4995a868f86fe879b9205a9b56a68a431a6dff06061685a5d",
    "foundations/BELLMAN_PERSISTENT_MODEL_FAMILY_CERTIFICATES.md":
        "38a461556da18e977c623404bec16a056013019daeb74adb7207bc0f313d749e",
    "verification/persistent_model_families/families.py":
        "40163e00ae5d0be54c9effbd78ad25f99d05d29d08dda1849d1be28e3819925f",
    "verification/persistent_model_families/results.json":
        "10778c1e5067fcd77de75036da4f4c27114534bb66b61c8a346c63fe3f4b86d6",
    "foundations/BELLMAN_STATISTICAL_RECTANGLES_TO_CORNER_MODEL_GUARANTEES.md":
        "c87033cf4f9d7adaadb745fa0722ff62376eabc11cf1219628cd6b5df388313e",
    "verification/statistical_corner_models/reference.py":
        "443400ef102deb43c9bb4234528cc51c209afd384259381ae4f3a908c9eb4a38",
    "verification/statistical_corner_models/results.json":
        "c2360cdfcbde5f4bb48d0a629bb0c60defcaecd8506224d14c76d49436849a7e",
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
    ".github/workflows/two-stage-longitudinal-causal-policy.yml",
}
NEW_PREFIX = "verification/longitudinal_causal_kernel_fibres/"
NEW_PATHS = {
    "foundations/BELLMAN_LONGITUDINAL_CAUSAL_KERNEL_FIBRES_AND_PERSISTENT_DECISIONS.md",
    ".github/workflows/longitudinal-causal-kernel-fibres.yml",
}
SOURCES = (
    "foundations/BELLMAN_LONGITUDINAL_CAUSAL_KERNEL_FIBRES_AND_PERSISTENT_DECISIONS.md",
    "verification/longitudinal_causal_kernel_fibres/reference.py",
    "verification/longitudinal_causal_kernel_fibres/checks.py",
    "verification/longitudinal_causal_kernel_fibres/run_checks.py",
    "verification/longitudinal_causal_kernel_fibres/README.md",
    "README.md",
    "docs/programme/ROADMAP.md",
    "docs/programme/ARCHITECTURE.md",
    "docs/history/records/FINDINGS_LEDGER.md",
    "docs/history/records/SUBSTRATE_LEDGER.md",
    ".github/workflows/two-stage-longitudinal-causal-policy.yml",
    ".github/workflows/longitudinal-causal-kernel-fibres.yml",
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
    need(not unexpected, "change outside kernel-fibre scope: " +
         ", ".join(unexpected))


def verify_base_preservation():
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASE], cwd=ROOT,
        text=True).splitlines()
    checked = 0
    for path in paths:
        before = git_bytes(BASE, path)
        current = ROOT / path
        need(current.is_file(), f"post-PR20 base file removed: {path}")
        if path in APPEND_ONLY:
            need(current.read_bytes().startswith(before),
                 f"append-only historical record rewritten: {path}")
        elif path in EDITABLE_EXISTING:
            pass
        else:
            need(current.read_bytes() == before,
                 f"post-PR20 file changed outside scope: {path}")
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
    path = ROOT / "verification/longitudinal_causal_kernel_fibres/results.json"
    if not path.exists():
        return False
    record = json.loads(path.read_text())
    need(record.get("status") == "passed" and record.get("failed") == 0,
         "retained kernel-fibre result is not passing")
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
            need((source.parent / target).resolve().exists(),
                 f"broken relative Markdown link in {path}: {target}")
            checked += 1
    return checked


def semantic(payload):
    if isinstance(payload, dict):
        return {key: semantic(value) for key, value in payload.items()
                if key not in {"optimized", "python", "runtime",
                               "elapsed_seconds", "source_sha256"}}
    if isinstance(payload, list):
        return [semantic(value) for value in payload]
    return payload


def run():
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                   text=True).strip()
    need(subprocess.run(["git", "merge-base", "--is-ancestor",
                         REVIEWED_PR20, PR20_MERGE], cwd=ROOT).returncode == 0,
         "reviewed PR20 head is not in its merge commit")
    need(subprocess.run(["git", "diff", "--quiet", REVIEWED_PR20,
                         PR20_MERGE, "--"], cwd=ROOT).returncode == 0,
         "PR20 merge tree differs from reviewed final head")
    need(subprocess.run(["git", "merge-base", "--is-ancestor", BASE, head],
                        cwd=ROOT).returncode == 0,
         "kernel-fibre work is not based on post-PR20 main")
    scope = changed_paths()
    verify_scope(scope)
    preserved = verify_base_preservation()
    frozen = verify_frozen()
    markdown_links = verify_markdown_links(scope)

    durations = {}

    def call_json(name, path, flags=()):
        started = time.perf_counter()
        raw = subprocess.check_output([sys.executable, *flags, path], cwd=ROOT,
                                      env=environment, text=True)
        durations[name] = time.perf_counter() - started
        return json.loads(raw)

    modes = (("normal", ()), ("-O", ("-O",)))
    component_paths = (
        ("kernel_fibre", "verification/longitudinal_causal_kernel_fibres/checks.py"),
        ("longitudinal", "verification/longitudinal_causal_policy/checks.py"),
        ("finite_causal", "verification/finite_causal_identification/checks.py"),
        ("unsafe", "verification/unsafe_set_reachability/checks.py"),
        ("corner", "verification/statistical_corner_models/checks.py"),
        ("persistent", "verification/persistent_model_families/checks.py"),
        ("sequential", "verification/sequential_certificates/checks.py"),
        ("multistream", "verification/multistream_collection/checks.py"),
        ("replanning", "verification/family_replanning/checks.py"),
        ("statistical", "verification/statistical_decision_bridge/checks.py"),
        ("accumulation", "verification/certificate_accumulation/checks.py"),
        ("transport", "verification/certificate_transport/checks.py"),
    )
    component_runs = {}
    for mode, flags in modes:
        for name, path in component_paths:
            result = call_json(f"{name}_{mode}", path, flags)
            component_runs.setdefault(name, []).append(result)
    for name, results in component_runs.items():
        need(semantic(results[0]) == semantic(results[1]),
             f"current {name} checks differ by optimization mode")
        need(results[0].get("failed") == results[1].get("failed") == 0 or
             results[0].get("status") == results[1].get("status") == "passed",
             f"current {name} checks failed")

    joint_runs = []
    for mode, flags in modes:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "joint.json"
            started = time.perf_counter()
            raw = subprocess.check_output(
                [sys.executable, *flags,
                 "verification/joint_law_completion/module_checks.py",
                 "--output", str(output)], cwd=ROOT, env=environment, text=True)
            durations[f"joint_{mode}"] = time.perf_counter() - started
            result = json.loads(raw)
            need(json.loads(output.read_text())["passed_cases"] ==
                 result["passed_cases"], "joint-law output mismatch")
            joint_runs.append(result)
    need(semantic(joint_runs[0]) == semantic(joint_runs[1]),
         "joint-law checks differ by optimization mode")

    history_runs = []
    for mode, flags in modes:
        started = time.perf_counter()
        raw = subprocess.check_output(
            [sys.executable, *flags, "verification/history_migration/checks.py"],
            cwd=ROOT, env=environment, text=True)
        durations[f"history_{mode}"] = time.perf_counter() - started
        history_runs.append(parse_marked(
            raw, "HISTORY_MIGRATION_RESULT_BEGIN",
            "HISTORY_MIGRATION_RESULT_END"))
    need(history_runs[0] == history_runs[1] and
         history_runs[0]["failed"] == 0,
         "history checks differ by optimization mode or failed")

    historical_started = time.perf_counter()
    with tempfile.TemporaryDirectory() as temporary:
        subprocess.check_call(["git", "clone", "--quiet", "--no-local",
                               str(ROOT), temporary])
        subprocess.check_call(["git", "checkout", "--quiet", PR20_MERGE],
                              cwd=temporary)
        raw = subprocess.check_output(
            [sys.executable,
             "verification/longitudinal_causal_policy/run_checks.py"],
            cwd=temporary, env=environment, text=True)
    durations["historical_pr20_chain"] = time.perf_counter() - historical_started
    historical = parse_marked(raw, "LONGITUDINAL_CAUSAL_POLICY_RESULT_BEGIN",
                              "LONGITUDINAL_CAUSAL_POLICY_RESULT_END")
    need(historical["status"] == "passed" and historical["failed"] == 0 and
         historical["retained_result_present_and_source_bound"],
         "merged PR20 historical acceptance chain failed")

    hashes = source_hashes()
    retained_result = verify_optional_result(hashes)
    fibre = component_runs["kernel_fibre"][0]
    result = {
        "status": "passed",
        "failed": 0,
        "base_commit": BASE,
        "reviewed_pr20_head": REVIEWED_PR20,
        "pr20_merge_commit": PR20_MERGE,
        "executed_source_commit": head,
        "runtime": platform.python_version(),
        "execution": ("GitHub Actions" if
                      os.environ.get("GITHUB_ACTIONS") == "true" else "local"),
        "modes": ["normal", "-O"],
        "normal_optimized_equal": True,
        "passed_per_mode": fibre["passed"],
        "rejections_per_mode": fibre["rejections"],
        "results": fibre["results"],
        "current_checks": {
            name: {"failed": runs[0].get("failed", 0),
                   "passed": runs[0].get("passed",
                                                 runs[0].get("passed_cases")),
                   "status": runs[0].get("status")}
            for name, runs in component_runs.items()
        },
        "joint_law_passed_per_mode": joint_runs[0]["passed_cases"],
        "history": history_runs[0],
        "affected_relative_markdown_links_checked": markdown_links,
        "preservation": {
            "pr20_merged_before_start": True,
            "pr20_merge_tree_matches_reviewed_head": True,
            "base_files_checked": preserved,
            "historical_pr20_runner": "passed-at-exact-merge",
            "historical_pr19_runner":
                historical["preservation"]["historical_pr19_runner"],
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
            "release_versions":
                history_runs[0]["release_manifest"]["versions"],
            "release_identities_unchanged": True,
        },
        "source_sha256": hashes,
        "frozen_prerequisite_sha256": frozen,
        "retained_result_present_and_source_bound": retained_result,
        "authorized_paths": list(scope),
        "durations_seconds": durations,
        "limitations": [
            "The observational law and longitudinal causal premises are supplied, not empirically validated.",
            "The exact fibre is profile-relative to independent saturated missing second-stage binary rows.",
            "Finite corners are exact only for the proved multi-affine query class and are not the continuous fibre.",
            "Binary A1/L1/A2/Y, two dates, four missing rows, sixteen corners, and 32 deterministic policies only.",
            "Minimax loss is a supplied robust criterion, not causal identification; regret is same-completion only.",
            "No earlier-stage completion, transport, estimation, unsafe-set composition, authority, Writ, or Decision Lab claim.",
            "Analytical proofs plus bounded exact checks are not formal verification.",
            "The maximum 512 exact values were small; no solver, Julia/JuMP, Rust, Lean, or other trigger was reached.",
        ],
    }
    print("LONGITUDINAL_CAUSAL_KERNEL_FIBRE_RESULT_BEGIN")
    print(json.dumps(result, sort_keys=True))
    print("LONGITUDINAL_CAUSAL_KERNEL_FIBRE_RESULT_END")


if __name__ == "__main__":
    run()
