"""Read-only evidence receiving, normal/optimized agreement and frozen preservation."""
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from witness import demand
from consistency_receiver import receive

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DRAFT = '19e1904bfd96e8d0eb926ac630193b9f0b1d4265'
LIVING = {'README.md', 'docs/programme/ROADMAP.md', 'docs/programme/ARCHITECTURE.md'}


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, check=True).stdout


def run():
    observations = []
    for flags in ([], ['-O']):
        process = subprocess.run([sys.executable, *flags, str(HERE / 'checks.py')],
                                 capture_output=True, text=True, check=True)
        observations.append(json.loads(process.stdout))
    demand(observations[0] == observations[1], 'normal-optimized-mismatch')
    preserved, snapshot = 0, {}
    for path in git('ls-tree', '-r', '--name-only', DRAFT).decode().splitlines():
        snapshot[path] = git('show', DRAFT + ':' + path)
        if path not in LIVING:
            demand((ROOT / path).read_bytes() == snapshot[path],
                   'changed-frozen-draft-or-inherited-file', path)
            preserved += 1
    # The old source manifest includes then-current living docs. Replay it with
    # those exact historical bytes; never rewrite it to describe the current docs.
    with tempfile.TemporaryDirectory() as folder:
        target = Path(folder)
        for path, data in snapshot.items():
            destination = target / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        env = dict(os.environ, GIT_DIR=git('rev-parse', '--absolute-git-dir').decode().strip(),
                   GIT_WORK_TREE=str(target))
        original = subprocess.run([sys.executable, str(target / 'verification/sequential_credibility/run_checks.py'),
                                   '--verify-retained'], env=env, capture_output=True, text=True, check=True)
    inherited = json.loads(original.stdout)
    result = {'draft_commit': DRAFT, 'normal_optimized_equal': True,
              'preserved_draft_and_inherited_files': preserved,
              'original_retained_replay': {'snapshot_commit': DRAFT,
                  'normal_optimized_equal': inherited['normal_optimized_equal'],
                  'preserved_base_files': inherited['preserved_base_files'],
                  'max_gain': inherited['checks']['positive']['max_gain'],
                  'rejections': len(inherited['checks']['receiver_rejections'])},
              'checks': observations[0]}
    if '--verify-retained' in sys.argv:
        record = json.loads((HERE / 'results.json').read_text())
        for path, wanted in record['source_files'].items():
            demand(sha256((ROOT / path).read_bytes()).hexdigest() == wanted, 'stale-retained-source', path)
            demand(sha256(git('show', record['source_commit'] + ':' + path)).hexdigest() == wanted,
                   'retained-source-commit-mismatch', path)
        subject = json.loads((HERE.parent / 'sequential_credibility' / 'example_subject.json').read_text())
        certificate = json.loads((HERE / 'example_warrant.json').read_text())
        demand(receive(subject, certificate) == record['validation']['checks']['integrated'],
               'retained-warrant-mismatch')
        demand(result == record['validation'], 'retained-observation-mismatch')
    return result


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
