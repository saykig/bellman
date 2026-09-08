"""Current-tree preservation plus exact strategic/causal/history snapshot replay.

The old task-scoped runners remain unmodified. Only three workflow entrypoints
change; every mathematical source and retained artifact is compared byte-for-byte.
"""
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
STRATEGIC = 'af7a8fc67cb204b67474eb7749c76c414189a5d5'
CAUSAL = 'cea4e1a47cb91c1f3917490350deab53d2976908'
WORKFLOWS = {'.github/workflows/sequential-consistency.yml',
             '.github/workflows/two-stage-longitudinal-causal-policy.yml',
             '.github/workflows/history-migration.yml'}
ADDITIONS = {'verification/sequential_consistency/acceptance.py',
             'verification/sequential_consistency/ACCEPTANCE.md',
             'verification/sequential_consistency/acceptance-results.json',
             'reviews/SEQUENTIAL_CREDIBILITY_CI_REPLAY_ADDENDUM.md'}


def need(ok, detail):
    if not ok:
        raise RuntimeError(detail)


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)


def preserve(root):
    paths = git(root, 'ls-tree', '-r', '--name-only', STRATEGIC).decode().splitlines()
    for path in paths:
        if path not in WORKFLOWS:
            need((root / path).is_file() and (root / path).read_bytes() == git(root, 'show', STRATEGIC + ':' + path),
                 'changed mathematical/source/evidence file: ' + path)
    current = set(git(root, 'ls-files').decode().splitlines())
    current.update(git(root, 'ls-files', '--others', '--exclude-standard').decode().splitlines())
    need(not current - set(paths) - ADDITIONS, 'unexpected acceptance scope addition')
    notes = {str(p.relative_to(root)) for p in (root / 'docs/history/releases').glob('*.md')}
    expected = {p for p in paths if p.startswith('docs/history/releases/') and p.endswith('.md')}
    need(notes == expected, 'unexpected research or published release note')
    # Causal mode independently binds current prerequisites to their actual merge,
    # not just to the later strategic snapshot's claim that they were preserved.
    living = {'README.md', 'docs/programme/ROADMAP.md', 'docs/programme/ARCHITECTURE.md'}
    for path in git(root, 'ls-tree', '-r', '--name-only', CAUSAL).decode().splitlines():
        if path not in WORKFLOWS | living:
            need((root / path).read_bytes() == git(root, 'show', CAUSAL + ':' + path),
                 'changed merged causal prerequisite: ' + path)
    return len(paths) - len(WORKFLOWS)


def marked(raw, label):
    return json.loads(raw.split(label + '_BEGIN\n', 1)[1].split('\n' + label + '_END', 1)[0])


def run(mode='all'):
    need(mode in ('all', 'strategic', 'causal', 'history'), 'unsupported acceptance mode')
    preserved = preserve(ROOT)
    result = {'preserved_strategic_snapshot_files': preserved,
              'workflow_only_exceptions': sorted(WORKFLOWS), 'mode': mode}
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    # Do not inherit alternate Git index/worktree settings into the isolated clones.
    for name in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'):
        env.pop(name, None)
    with tempfile.TemporaryDirectory() as folder:
        target = Path(folder)
        subprocess.run(['git', 'clone', '--quiet', '--no-local', '--no-checkout', str(ROOT), str(target)],
                       check=True, env=env)

        def checkout(commit):
            subprocess.run(['git', '-c', 'advice.detachedHead=false', 'checkout', '--quiet', '--detach', commit],
                           cwd=target, check=True, env=env)

        def call(path, flags=(), args=()):
            p = subprocess.run([sys.executable, *flags, path, *args], cwd=target,
                               capture_output=True, text=True, env=env)
            need(p.returncode == 0, 'snapshot replay failed: ' + path + '\n' + p.stderr[-10000:])
            return p.stdout

        checkout(STRATEGIC)
        # Decisive preservation controls: altered evidence and an extra release
        # note must fail before any replay can mask their existence.
        negative = []
        evidence = target / 'verification/sequential_consistency/example_warrant.json'
        original = evidence.read_bytes()
        evidence.write_bytes(original + b' ')
        try:
            preserve(target)
        except RuntimeError:
            negative.append('altered retained evidence rejected')
        evidence.write_bytes(original)
        extra = target / 'docs/history/releases/unregistered-control.md'
        extra.write_text('unregistered')
        try:
            preserve(target)
        except RuntimeError:
            negative.append('unregistered note rejected')
        extra.unlink()
        need(len(negative) == 2, 'preservation negative control failed')
        result['preservation_negative_controls'] = negative
        if mode in ('all', 'strategic'):
            r = json.loads(call('verification/sequential_consistency/run_checks.py', args=('--verify-retained',)))
            result['strategic'] = {'snapshot': STRATEGIC, 'normal_optimized_equal': r['normal_optimized_equal'],
                'integrated': r['checks']['integrated'], 'rejections': len(r['checks']['rejections']),
                'both_producers_disabled': r['checks']['both_producers_disabled'],
                'original_retained_replay': r['original_retained_replay']}
        checkout(CAUSAL)
        if mode in ('all', 'causal'):
            r = marked(call('verification/longitudinal_causal_policy/run_checks.py'), 'LONGITUDINAL_CAUSAL_POLICY_RESULT')
            need(r['status'] == 'passed' and r['failed'] == 0 and r['retained_result_present_and_source_bound'],
                 'causal historical acceptance failed')
            result['causal'] = {'snapshot': CAUSAL, 'normal_optimized_equal': r['normal_optimized_equal'],
                'passed_per_mode': r['passed_per_mode'], 'rejections_per_mode': r['rejections_per_mode'],
                'current_checks_at_snapshot': r['current_checks'], 'preservation': r['preservation'],
                'retained_result_present_and_source_bound': True}
        if mode in ('all', 'history'):
            history = [marked(call('verification/history_migration/checks.py', flags), 'HISTORY_MIGRATION_RESULT')
                       for flags in ((), ('-O',))]
            need(history[0] == history[1] and history[0]['failed'] == 0, 'history replay mismatch')
            result['history'] = {'snapshot': CAUSAL, 'normal_optimized_equal': True,
                                 'release_manifest': history[0]['release_manifest']}
    if '--verify-retained' in sys.argv:
        record = json.loads((ROOT / 'verification/sequential_consistency/acceptance-results.json').read_text())
        for path, expected in record['source_files'].items():
            need(sha256((ROOT / path).read_bytes()).hexdigest() == expected, 'acceptance source changed: ' + path)
            need(sha256(git(ROOT, 'show', record['source_commit'] + ':' + path)).hexdigest() == expected,
                 'acceptance source commit mismatch: ' + path)
        wanted = record['validation']
        need(all(wanted[key] == value for key, value in result.items() if key != 'mode'), 'acceptance observation mismatch')
    return result


if __name__ == '__main__':
    modes = [a[2:] for a in sys.argv[1:] if a in ('--strategic', '--causal', '--history')]
    need(len(modes) <= 1, 'multiple acceptance modes')
    print(json.dumps(run(modes[0] if modes else 'all'), sort_keys=True, indent=2))
