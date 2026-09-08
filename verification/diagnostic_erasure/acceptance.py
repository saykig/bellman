"""Receive the diagnostic obstruction and replay frozen prerequisites at their identities."""
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
BASE='5ea19f214ec89536f47fe20cfa5a4d62222b2598'
LIVING={'README.md','docs/programme/ROADMAP.md','docs/programme/ARCHITECTURE.md'}
WORKFLOWS={'.github/workflows/sequential-consistency.yml','.github/workflows/history-migration.yml','.github/workflows/two-stage-longitudinal-causal-policy.yml'}
ADDITIONS={'foundations/BELLMAN_DIAGNOSTIC_HISTORY_ERASURE_OBSTRUCTION.md',
           'reviews/DIAGNOSTIC_HISTORY_ERASURE_REVIEW_2026_09_08.md',
           'docs/history/releases/2026-09-08-diagnostic-history-erasure-obstruction.md'} | {
    'verification/diagnostic_erasure/'+p for p in ('candidate.py','receive_case.py',
        'checks.py','acceptance.py','ACCEPTANCE.md','example_case.json','results.json','final-results.json')}


def need(ok,detail):
    if not ok:raise RuntimeError(detail)


def git(root,*args):return subprocess.check_output(['git',*args],cwd=root)


def preserve(root):
    paths=set(git(root,'ls-tree','-r','--name-only',BASE).decode().splitlines())
    for p in sorted(paths-LIVING-WORKFLOWS):
        need((root/p).is_file() and (root/p).read_bytes()==git(root,'show',BASE+':'+p),'changed retained prerequisite: '+p)
    current=set(git(root,'ls-files').decode().splitlines())
    current.update(git(root,'ls-files','--others','--exclude-standard').decode().splitlines())
    need(not current-paths-ADDITIONS,'unexpected diagnostic-erasure addition: '+str(sorted(current-paths-ADDITIONS)))
    return len(paths-LIVING-WORKFLOWS)


def run(mode='all',verify_retained=False):
    need(mode in ('all','strategic','causal','history'),'unsupported acceptance mode')
    result={'mode':mode,'preserved_base_files':preserve(ROOT),'base':BASE,
            'permitted_existing_changes':sorted(LIVING|WORKFLOWS)}
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    for n in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE'):env.pop(n,None)
    with tempfile.TemporaryDirectory() as folder:
        snapshot=Path(folder)/'snapshot'
        subprocess.run(['git','clone','--quiet','--no-local','--no-checkout',str(ROOT),str(snapshot)],check=True,env=env)
        subprocess.run(['git','-c','advice.detachedHead=false','checkout','--quiet','--detach',BASE],cwd=snapshot,check=True,env=env)
        controls=[]
        p=snapshot/'verification/sequential_consistency/example_warrant.json';original=p.read_bytes();p.write_bytes(original+b' ')
        try:preserve(snapshot)
        except RuntimeError as e:
            need('changed retained prerequisite' in str(e),'wrong preservation rejection');controls.append('changed inherited warrant rejected')
        p.write_bytes(original)
        p=snapshot/'docs/history/releases/unregistered-control.md';p.write_text('control')
        try:preserve(snapshot)
        except RuntimeError as e:
            need('unexpected diagnostic-erasure addition' in str(e),'wrong addition rejection');controls.append('unregistered release rejected')
        p.unlink();need(len(controls)==2,'preservation control failure')
        result['preservation_negative_controls']=controls
        args=[] if mode=='all' else ['--'+mode]
        out=subprocess.run([sys.executable,'verification/history_reduction/acceptance.py',*args,'--verify-retained'],cwd=snapshot,env=env,capture_output=True,text=True)
        need(out.returncode==0,'inherited acceptance failed:\n'+out.stderr[-12000:])
        result['inherited']=json.loads(out.stdout)
    if mode in ('all','strategic'):
        outputs=[]
        for flags in ([],['-O']):
            out=subprocess.run([sys.executable,*flags,'verification/diagnostic_erasure/checks.py'],cwd=ROOT,env=env,capture_output=True,text=True)
            need(out.returncode==0,'diagnostic erasure checks failed:\n'+out.stderr[-12000:])
            outputs.append(json.loads(out.stdout))
        need(outputs[0]==outputs[1],'normal/optimized diagnostic mismatch')
        result['diagnostic_erasure']=outputs[0];result['normal_optimized_equal']=True
    if verify_retained:
        record=json.loads((ROOT/'verification/diagnostic_erasure/final-results.json').read_text())
        expected_paths=ADDITIONS-{'verification/diagnostic_erasure/final-results.json'}|LIVING|WORKFLOWS
        need(set(record['source_files'])==expected_paths,'incomplete source manifest')
        for p,wanted in record['source_files'].items():
            need(sha256((ROOT/p).read_bytes()).hexdigest()==wanted,'changed diagnostic source: '+p)
            need(sha256(git(ROOT,'show',record['source_commit']+':'+p)).hexdigest()==wanted,'source commit mismatch: '+p)
        def subset(actual,wanted):
            return all(k=='mode' or (k in wanted and (subset(v,wanted[k]) if isinstance(v,dict) else v==wanted[k])) for k,v in actual.items())
        need(subset(result,record['validation']),'retained observation mismatch')
    return result

if __name__=='__main__':
    flags=set(sys.argv[1:]);need(flags<={'--strategic','--causal','--history','--verify-retained'},'unknown acceptance flag')
    modes=flags&{'--strategic','--causal','--history'};need(len(modes)<=1,'multiple acceptance modes')
    print(json.dumps(run(next(iter(modes))[2:] if modes else 'all','--verify-retained' in flags),sort_keys=True,indent=2))
