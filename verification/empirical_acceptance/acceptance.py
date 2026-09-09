"""Additive current acceptance: frozen v0.0.7 plus the retained empirical checkpoint.
Run the old closed-inventory receiver at its own commit; never weaken its source guard.
"""
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
BASE = '2cd6fd7432efccaacc734fd235549a564ddbff48'
CASE = 'ae7acb7c9ba82f51cd72d6633fc6ecaeda61a6d3'
PREFIX = 'research/empirical_trust_2016/'
LIVING = {'README.md', 'docs/programme/ROADMAP.md', 'docs/programme/ARCHITECTURE.md',
          'research/empirical_design_checkpoint/CURRENT_BRIEF.md'}
WORKFLOWS = {'.github/workflows/' + n for n in ('combined-acceptance.yml',
    'sequential-consistency.yml', 'history-migration.yml', 'two-stage-longitudinal-causal-policy.yml',
    'longitudinal-causal-kernel-fibres.yml')}
NEW = {'verification/empirical_acceptance/' + n for n in ('acceptance.py', 'README.md', 'results.json')}
NEW |= {'research/empirical_trust_2016/REVIEW_20260909.md',
        'docs/history/releases/2026-09-09-human-trust-research-checkpoint.md'}
PREVIOUS_RECEIPT = 'verification/empirical_acceptance/results.json'
RECEIPT = 'verification/empirical_acceptance/completion-results.json'
NEW |= {RECEIPT, 'research/empirical_trust_2016/COMPLETION_AUDIT_20260909.md'}
PREVIOUS_CHECKPOINT = '468527810e6257e5ab1977ed6743bd5707386389'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
for k in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'):
    ENV.pop(k, None)


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, env=ENV)


def digest(raw):
    return sha256(raw).hexdigest()


def tree(commit):
    return {p: git('show', commit + ':' + p) for p in git('ls-tree', '-r', '--name-only', commit).decode().splitlines()}


def preserve(root, expected, inventory, allowed):
    for p, raw in expected.items():
        need((root / p).is_file() and (root / p).read_bytes() == raw, 'frozen bytes changed: ' + p)
    need(not inventory - allowed, 'unregistered addition: ' + str(sorted(inventory - allowed)))


def execute(root, args):
    p = subprocess.run([sys.executable, *args], cwd=root, env=ENV, capture_output=True, text=True)
    need(p.returncode == 0, 'check failed: ' + ' '.join(args) + '\n' + p.stderr[-12000:])
    return json.loads(p.stdout)


def normalized(x):
    if isinstance(x, dict):
        return {k: normalized(v) for k, v in x.items() if k not in {'python', 'optimized'}}
    if isinstance(x, list):
        return [normalized(v) for v in x]
    return x


def check_source_record(path):
    record = json.loads((ROOT / path).read_text())
    for p, h in record['source_files'].items():
        need(digest(git('show', record['source_commit'] + ':' + p)) == h, 'unbound checkpoint source: ' + p)
        need(digest((ROOT / p).read_bytes()) == h, 'checkpoint source changed: ' + p)
    return record


def run(mode='all', verify=False, recompute=False):
    baseline, case = tree(BASE), tree(CASE)
    need(git('rev-parse', 'v0.0.7').decode().strip() == BASE, 'v0.0.7 tag changed')
    expected = {p: raw for p, raw in case.items() if p not in LIVING | WORKFLOWS}
    for p, raw in baseline.items():
        if p not in LIVING | WORKFLOWS:
            need(expected[p] == raw, 'checkpoint rewrote v0.0.7: ' + p)
    # The first aggregate receipt remains frozen at its published checkpoint.
    for path in (PREVIOUS_RECEIPT, PREFIX + 'REVIEW_20260909.md',
                 'docs/history/releases/2026-09-09-human-trust-research-checkpoint.md'):
        expected[path] = git('show', PREVIOUS_CHECKPOINT + ':' + path)
    inventory = set(git('ls-files').decode().splitlines()) | set(git('ls-files', '--others', '--exclude-standard').decode().splitlines())
    allowed = set(case) | NEW
    preserve(ROOT, expected, inventory, allowed)
    # Independent evidence-mutation and addition controls; temporary copies only.
    controls = []
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        for p in ('verification/combined_acceptance/results.json', PREFIX + 'results.json', PREVIOUS_RECEIPT):
            target = root / p
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(expected[p] + b' ')
            try:
                preserve(root, {p: expected[p]}, {p}, {p})
            except RuntimeError as e:
                need(str(e) == 'frozen bytes changed: ' + p, 'wrong preservation rejection')
                controls.append(p)
            else:
                raise RuntimeError('mutated record accepted')
        try:
            preserve(root, {}, {'unknown.json'}, set())
        except RuntimeError as e:
            need(str(e).startswith('unregistered addition:'), 'wrong inventory rejection')
            controls.append('unregistered addition')
        else:
            raise RuntimeError('new unregistered file accepted')
    checkpoint = check_source_record(PREFIX + 'checkpoint-validation.json')
    case_checks = [execute(ROOT, [*flags, PREFIX + 'checks.py']) for flags in ([], ['-O'])]
    need(case_checks[0] == case_checks[1] == checkpoint['checks'], 'empirical retained receiving mismatch')
    handoffs = [execute(ROOT, [*flags, PREFIX + 'check_handoff.py']) for flags in ([], ['-O'])]
    need(handoffs[0] == handoffs[1] == checkpoint['portable_revision'], 'portable revision replay mismatch')
    result = {'mode': mode, 'preservation': {'release_commit': BASE, 'empirical_checkpoint': CASE,
        'frozen_files': len(expected), 'frozen_sha256': digest(json.dumps({p: digest(v) for p, v in sorted(expected.items())}, sort_keys=True).encode()),
        'rejection_controls': controls}, 'empirical_receiving': case_checks[0], 'portable_revision': handoffs[0]}
    # Ephemeral local snapshot follows the historical receiver's own replay convention.
    # No new remote repository, branch, or persistent checkout is created.
    with tempfile.TemporaryDirectory() as d:
        snapshot = Path(d) / 'release'
        subprocess.run(['git', 'clone', '--quiet', '--no-local', '--no-checkout', str(ROOT), str(snapshot)], check=True, env=ENV)
        subprocess.run(['git', '-c', 'advice.detachedHead=false', 'checkout', '--quiet', '--detach', BASE], cwd=snapshot, check=True, env=ENV)
        flags = [] if mode == 'all' else ['--' + mode]
        result['release_replay'] = execute(snapshot, ['verification/combined_acceptance/acceptance.py', *flags, '--verify-retained'])
    # The live source is byte-preserved, but also execute it in its current context.
    for label, path in [('strategic', 'verification/diagnostic_erasure/checks.py'),
                        ('causal', 'verification/longitudinal_causal_kernel_fibres/checks.py')]:
        if mode == 'history' or (mode == 'causal' and label == 'strategic') or (mode == 'strategic' and label == 'causal'):
            continue
        runs = [normalized(execute(ROOT, [*flags, path])) for flags in ([], ['-O'])]
        need(runs[0] == runs[1], 'live normal/optimized mismatch: ' + label)
        result['live_' + label] = runs[0]
    if recompute:
        stored = json.loads((ROOT / PREFIX / 'results.json').read_text())
        with tempfile.TemporaryDirectory() as d:
            fresh = []
            for i, flags in enumerate(([], ['-O'])):
                target = str(Path(d) / f'fresh-{i}.json')
                execute(ROOT, [*flags, PREFIX + 'analyze.py', target])
                fresh.append(json.loads(Path(target).read_text()))
            need(fresh[0] == fresh[1], 'producer normal/optimized mismatch')
            # BLAS/runtime may differ across hosts. Bind the source and compare numerical
            # outputs within 1e-11, retaining statistical implementation, not exact-fit claims.
            def equivalent(a, b):
                if isinstance(a, dict):
                    return set(a) == set(b) and all(k == 'runtime' or equivalent(v, b[k]) for k, v in a.items())
                if isinstance(a, list):
                    return len(a) == len(b) and all(equivalent(x, y) for x, y in zip(a, b))
                if isinstance(a, (str, float)) and isinstance(b, type(a)):
                    try:
                        return math.isclose(float(a), float(b), rel_tol=0, abs_tol=1e-11)
                    except ValueError:
                        pass
                return a == b
            need(equivalent(fresh[0], stored), 'fresh statistical reproduction differs')
            execute(ROOT, [PREFIX + 'checks.py', str(Path(d) / 'fresh-0.json')])
        result['statistical_recomputation'] = 'normal/optimized equal; retained values within 1e-11'
    if verify:
        receipt = check_source_record(RECEIPT)
        need(set(receipt['source_files']) == NEW - {RECEIPT} | LIVING | WORKFLOWS, 'current receipt source coverage')
        def subset(a, b):
            return all(k == 'mode' or (k in b and (subset(v, b[k]) if isinstance(v, dict) else v == b[k])) for k, v in a.items())
        need(subset(normalized(result), normalized(receipt['validation'])), 'current observation differs from receipt')
    return result


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    m = p.add_mutually_exclusive_group()
    for name in ('strategic', 'causal', 'history'):
        m.add_argument('--' + name, action='store_true')
    p.add_argument('--verify-retained', action='store_true')
    p.add_argument('--recompute', action='store_true')
    p.add_argument('--record', help='creation-only receipt output; source files must be committed')
    args = p.parse_args()
    mode = next((name for name in ('strategic', 'causal', 'history') if getattr(args, name)), 'all')
    result = run(mode, args.verify_retained, args.recompute)
    if args.record:
        need(mode == 'all' and args.recompute, 'record requires full inherited and statistical checks')
        commit = git('rev-parse', 'HEAD').decode().strip()
        sources = {f: digest((ROOT / f).read_bytes()) for f in sorted(NEW - {RECEIPT} | LIVING | WORKFLOWS)}
        for f, h in sources.items():
            need(digest(git('show', commit + ':' + f)) == h, 'uncommitted source: ' + f)
        with Path(args.record).open('x') as f:
            json.dump({'source_commit': commit, 'source_files': sources, 'validation': result}, f, sort_keys=True, indent=2)
            f.write('\n')
    print(json.dumps(result, sort_keys=True, indent=2))
