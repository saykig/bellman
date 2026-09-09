"""Additive AFY acceptance; immutable prior aggregate replay at its own edition."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
PRIOR='349cc42b11a0cd85ba95523ea530bf80fd93e596'
FROZEN='eec4f51ce5a94382a1654c399f98a7aec442225e'
PREFIX='research/beliefs_2024/'
HERE='verification/beliefs_acceptance/'
RECEIPT=HERE+'results.json'
LIVING={'docs/programme/ROADMAP.md','docs/programme/ARCHITECTURE.md',
        'research/empirical_design_checkpoint/CURRENT_BRIEF.md',PREFIX+'README.md'}
WORKFLOWS={'.github/workflows/'+p for p in ['combined-acceptance.yml','sequential-consistency.yml',
    'history-migration.yml','two-stage-longitudinal-causal-policy.yml','longitudinal-causal-kernel-fibres.yml']}
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for key in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE'): ENV.pop(key,None)


def need(ok,message):
    if not ok: raise RuntimeError(message)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT,env=ENV)


def execute(root,args):
    p=subprocess.run([sys.executable,*args],cwd=root,env=ENV,capture_output=True,text=True)
    need(p.returncode==0,'failed '+str(args)+'\n'+p.stderr[-12000:])
    return json.loads(p.stdout)


def tree(commit):
    return {p:git('show',commit+':'+p) for p in git('ls-tree','-r','--name-only',commit).decode().splitlines()}


def preserve(root,expected,inventory,allowed):
    need(inventory<=allowed,'unregistered additions: '+str(sorted(inventory-allowed)))
    for path,raw in expected.items():
        need((root/path).is_file() and (root/path).read_bytes()==raw,'frozen bytes changed: '+path)


def integrity():
    frozen=tree(FROZEN); old=tree(PRIOR)
    for p,raw in old.items(): need(frozen[p]==raw,'AFY checkpoint changed inherited bytes: '+p)
    allowed=set(frozen)|set(json.loads((ROOT/HERE/'inventory.json').read_text()))
    inventory=set(git('ls-files').decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
    expected={p:b for p,b in frozen.items() if p not in LIVING|WORKFLOWS}
    preserve(ROOT,expected,inventory,allowed)
    # Each additive AFY receipt's complete bindings are checked without requiring raw observations.
    for name in ('first-run-manifest.json','receiving-checkpoint.json','sensitivity-checkpoint.json','reproduction-checkpoint.json'):
        record=json.loads((ROOT/PREFIX/name).read_text())
        for p,h in {**record['source_hashes'],**record.get('outputs',{})}.items():
            need(sha((ROOT/PREFIX/p).read_bytes())==h,'AFY source/evidence binding mismatch: '+p)
    controls=[]
    with tempfile.TemporaryDirectory() as d:
        root=Path(d)
        for p in ('verification/combined_acceptance/results.json','verification/empirical_acceptance/completion-results.json',PREFIX+'first-results/results.json',PREFIX+'prior-sensitivity-results.json'):
            target=root/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(expected[p]+b' ')
            try: preserve(root,{p:expected[p]},{p},{p})
            except RuntimeError as e:
                need(str(e)=='frozen bytes changed: '+p,'wrong mutation diagnostic');controls.append(p)
            else: raise RuntimeError('evidence mutation accepted')
        try: preserve(root,{}, {'__unregistered_probe__.json'},set())
        except RuntimeError as e: need(str(e).startswith('unregistered additions:'),'wrong inventory diagnostic')
        else: raise RuntimeError('unregistered addition accepted')
    return {'prior_commit':PRIOR,'frozen_checkpoint':git('rev-parse',FROZEN).decode().strip(),
        'frozen_files':len(expected),'frozen_digest':sha(json.dumps({p:sha(b) for p,b in sorted(expected.items())},sort_keys=True).encode()),
        'mutation_controls':controls+['unregistered addition'],'registered_files':len(allowed)}


def run(mode,raw,recompute,verify):
    result={'mode':mode,'preservation':integrity()}
    with tempfile.TemporaryDirectory() as d:
        snapshot=Path(d)/'prior'
        # Established ephemeral detached replay convention; no new remote or persistent repository.
        subprocess.run(['git','clone','--quiet','--no-local','--no-checkout',str(ROOT),str(snapshot)],check=True,env=ENV)
        subprocess.run(['git','-c','advice.detachedHead=false','checkout','--quiet','--detach',PRIOR],cwd=snapshot,check=True,env=ENV)
        flags=[] if mode=='all' else ['--'+mode]
        inherited=execute(snapshot,['verification/empirical_acceptance/acceptance.py',*flags,'--verify-retained',*(['--recompute'] if recompute else [])])
        result['inherited']={'mode':mode,'receipt_verified':True,'prior_receipt_sha256':sha((snapshot/'verification/empirical_acceptance/completion-results.json').read_bytes()),
            'validation_digest':sha(json.dumps(inherited,sort_keys=True).encode())}
    if mode=='all':
        need(raw is not None,'full AFY acceptance requires explicitly acquired --source')
        raw=str(Path(raw).resolve())
        operations={'receiving':[PREFIX+'checks.py',raw],
            'sensitivity':[PREFIX+'sensitivity_checks.py',raw,str(ROOT/PREFIX/'prior-sensitivity-results.json')],
            'inference':[PREFIX+'inference_checks.py'], 'portable':[PREFIX+'check_transfer.py',raw]}
        checks={}
        for name,args in operations.items():
            normal=execute(ROOT,args); optimized=execute(ROOT,['-O',*args]); need(normal==optimized,'normal/optimized mismatch: '+name)
            checks[name]=normal
        result['afy_checks']=checks
        if recompute:
            with tempfile.TemporaryDirectory() as d:
                fresh=execute(ROOT,[PREFIX+'reproduce.py','run',raw,str(Path(d)/'fresh')])
                optimized=execute(ROOT,[PREFIX+'reproduce.py','run',raw,str(Path(d)/'optimized'),'--optimized'])
                for label in fresh['fresh_receiving']:
                    need(fresh['fresh_receiving'][label]==optimized['fresh_receiving'][label],'fresh normal/optimized receiving mismatch')
                result['fresh_prediction_reproduction']={'normal_and_optimized_received':True,'within_declared_1e_7':max(fresh['max_prediction_difference_from_first'],optimized['max_prediction_difference_from_first'])<=1e-7,
                    'mixtures':'retained source-only fits; separate full R refit receipt preserved'}
    else:
        result['afy_scope']='frozen identities only; no raw-data empirical replay claimed for this scoped route'
    if verify:
        receipt=json.loads((ROOT/RECEIPT).read_text())
        expected_sources=set(json.loads((ROOT/HERE/'inventory.json').read_text()))-{RECEIPT}|LIVING|WORKFLOWS
        need(set(receipt['source_files'])==expected_sources,'receipt source coverage')
        for p,h in receipt['source_files'].items():
            need(sha((ROOT/p).read_bytes())==h and sha(git('show',receipt['source_commit']+':'+p))==h,'receipt source identity: '+p)
        need(result['preservation']==receipt['validation']['preservation'],'preservation receipt mismatch')
        if mode=='all':
            need(result['afy_checks']==receipt['validation']['afy_checks'],'AFY receipt observation mismatch')
            if recompute: need(result['fresh_prediction_reproduction']==receipt['validation']['fresh_prediction_reproduction'],'fresh receipt mismatch')
        # The delegated prior entrypoint verifies its own full/scoped receipt directly.
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(); modes=p.add_mutually_exclusive_group()
    for name in ('strategic','causal','history'): modes.add_argument('--'+name,action='store_true')
    p.add_argument('--source');p.add_argument('--recompute',action='store_true');p.add_argument('--verify-retained',action='store_true');p.add_argument('--record')
    args=p.parse_args(); mode=next((n for n in ('strategic','causal','history') if getattr(args,n)),'all')
    need(not args.recompute or mode=='all','recompute requires full mode')
    result=run(mode,args.source,args.recompute,args.verify_retained)
    if args.record:
        need(mode=='all' and args.recompute,'record requires full recomputation')
        commit=git('rev-parse','HEAD').decode().strip()
        paths=set(json.loads((ROOT/HERE/'inventory.json').read_text()))-{RECEIPT}|LIVING|WORKFLOWS
        sources={p:sha((ROOT/p).read_bytes()) for p in sorted(paths)}
        for path,h in sources.items(): need(sha(git('show',commit+':'+path))==h,'uncommitted receipt source: '+path)
        with Path(args.record).open('x') as f: json.dump({'source_commit':commit,'source_files':sources,'validation':result},f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(result,indent=2,sort_keys=True))
