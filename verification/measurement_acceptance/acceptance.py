"""Additive menu acceptance preserving and replaying the completed AFY edition."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[2]
PRIOR='aa2f9f24bb0e2ad777f1ca9df0332b76ce02ea73'
HERE='verification/measurement_acceptance/'
RECEIPT=HERE+'results.json'
LIVING={'README.md','docs/programme/ROADMAP.md','docs/programme/ARCHITECTURE.md'}
WORKFLOWS={'.github/workflows/'+n for n in ['combined-acceptance.yml','sequential-consistency.yml','history-migration.yml','two-stage-longitudinal-causal-policy.yml','longitudinal-causal-kernel-fibres.yml']}
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for k in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE'):ENV.pop(k,None)
def need(ok,message):
    if not ok:raise RuntimeError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,env=ENV)
def execute(root,args):
    p=subprocess.run([sys.executable,*args],cwd=root,env=ENV,capture_output=True,text=True)
    need(p.returncode==0,'failed '+str(args)+'\n'+p.stderr[-12000:])
    return json.loads(p.stdout)
def integrity():
    names=git('ls-tree','-r','--name-only',PRIOR).decode().splitlines()
    expected={p:git('show',PRIOR+':'+p) for p in names if p not in LIVING|WORKFLOWS}
    extras=set(json.loads((ROOT/HERE/'inventory.json').read_text()))
    actual=set(git('ls-files').decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
    need(actual<=set(names)|extras,'unregistered files: '+str(sorted(actual-set(names)-extras)))
    def check(path,data):need(data==expected[path],'frozen bytes changed: '+path)
    for p,b in expected.items():check(p,(ROOT/p).read_bytes())
    local=json.loads((ROOT/'research/measurement_decision/local-receiving.json').read_text())
    local_paths={p for p in extras if p.startswith('research/measurement_decision/') and p!='research/measurement_decision/local-receiving.json'}
    need(set(local['source_files'])==local_paths,'local receipt source coverage')
    for p,h in local['source_files'].items():
        need(sha((ROOT/p).read_bytes())==h and sha(git('show',local['source_commit']+':'+p))==h,'local receiving source '+p)
    controls=[]
    for p in ['verification/beliefs_acceptance/results.json','research/beliefs_2024/first-results/results.json','verification/combined_acceptance/results.json']:
        try:check(p,expected[p]+b' ')
        except RuntimeError:controls.append(p)
        else:raise RuntimeError('mutation accepted')
    return {'prior':PRIOR,'frozen_files':len(expected),'frozen_digest':sha(json.dumps({p:sha(b) for p,b in sorted(expected.items())},sort_keys=True).encode()),'mutation_controls':controls}
def run(args):
    mode=next((n for n in ('history','strategic','causal') if getattr(args,n)),'all')
    out={'preservation':integrity(),'mode':mode}
    with tempfile.TemporaryDirectory(prefix='bellman-afy-replay-') as d:
        snapshot=Path(d)/'prior'
        subprocess.run(['git','clone','--quiet','--no-local','--no-checkout',str(ROOT),str(snapshot)],check=True,env=ENV)
        subprocess.run(['git','-c','advice.detachedHead=false','checkout','--quiet','--detach',PRIOR],cwd=snapshot,check=True,env=ENV)
        flags=['--verify-retained']
        if mode!='all':flags+=['--'+mode]
        else:
            need(args.source is not None,'full replay requires explicitly acquired source')
            flags+=['--source',str(Path(args.source).resolve())]
            if args.recompute:flags+=['--recompute']
        prior=execute(snapshot,['verification/beliefs_acceptance/acceptance.py',*flags])
        out['inherited']={'receipt_verified':True,'recomputed':bool(args.recompute),'receipt_sha256':sha((snapshot/'verification/beliefs_acceptance/results.json').read_bytes()),'validation_digest':sha(json.dumps(prior,sort_keys=True).encode())}
    command=['research/measurement_decision/checks.py']
    normal=execute(ROOT,command);optimized=execute(ROOT,['-O',*command]);need(normal==optimized,'measurement normal/optimized mismatch')
    out['measurement_public_audit']=normal
    if args.verify_retained:
        receipt=json.loads((ROOT/RECEIPT).read_text())
        paths=set(json.loads((ROOT/HERE/'inventory.json').read_text()))-{RECEIPT}|LIVING|WORKFLOWS
        need(set(receipt['source_files'])==paths,'source coverage')
        for p,h in receipt['source_files'].items():need(sha((ROOT/p).read_bytes())==h and sha(git('show',receipt['source_commit']+':'+p))==h,'source binding '+p)
        for key in ('preservation','measurement_public_audit'):need(out[key]==receipt['validation'][key],'receipt '+key)
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group()
    for n in ('history','strategic','causal'):g.add_argument('--'+n,action='store_true')
    p.add_argument('--source');p.add_argument('--recompute',action='store_true');p.add_argument('--verify-retained',action='store_true');p.add_argument('--record',type=Path)
    args=p.parse_args();need(not args.recompute or not any(getattr(args,n) for n in ('history','strategic','causal')),'full recomputation only')
    result=run(args)
    if args.record:
        need(result['mode']=='all' and args.recompute,'full recomputation required')
        commit=git('rev-parse','HEAD').decode().strip()
        paths=set(json.loads((ROOT/HERE/'inventory.json').read_text()))-{RECEIPT}|LIVING|WORKFLOWS
        sources={p:sha((ROOT/p).read_bytes()) for p in sorted(paths)}
        for p,h in sources.items():need(sha(git('show',commit+':'+p))==h,'uncommitted source '+p)
        with args.record.open('x') as f:json.dump({'source_commit':commit,'source_files':sources,'validation':result},f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps(result,sort_keys=True,indent=2))
