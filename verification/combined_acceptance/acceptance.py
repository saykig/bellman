"""Combine preserved strategic/causal acceptance; never rewrite their receivers or evidence."""
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
STRATEGIC='56fb71616212af9719ae7a264eb8c4829d80f235'
CAUSAL='4866ffce9b3e935b86188d3fe981d4b9240f0740'
LIVING={'README.md','docs/programme/ROADMAP.md','docs/programme/ARCHITECTURE.md'}
WORKFLOWS={'.github/workflows/'+n for n in ('sequential-consistency.yml','history-migration.yml',
            'two-stage-longitudinal-causal-policy.yml','longitudinal-causal-kernel-fibres.yml')}
LEDGERS={'docs/history/records/FINDINGS_LEDGER.md','docs/history/records/SUBSTRATE_LEDGER.md'}
ADDITIONS={'verification/combined_acceptance/'+n for n in ('acceptance.py','README.md','results.json','release_manifest.py')} | {
    'docs/history/releases/2026-09-09-combined-strategic-causal-acceptance.md',
    'docs/history/releases/v0.0.7-decisions-evidence-and-credible-promises.md'}
RECORD='verification/combined_acceptance/results.json'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for key in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE'):ENV.pop(key,None)


def need(ok,message):
    if not ok:raise RuntimeError(message)


def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,env=ENV)


def snapshots():
    trees={ref:{p:git('show',ref+':'+p) for p in git('ls-tree','-r','--name-only',ref).decode().splitlines()}
           for ref in (STRATEGIC,CAUSAL)}
    expected={}
    for ref,tree in trees.items():
        for p,raw in tree.items():
            if p in LIVING|WORKFLOWS:continue
            if p in LEDGERS:
                need(trees[CAUSAL][p].startswith(trees[STRATEGIC][p]),'ledger histories do not compose: '+p)
                expected[p]=trees[CAUSAL][p]
            else:
                need(p not in expected or expected[p]==raw,'conflicting frozen editions: '+p)
                expected[p]=raw
    return trees,expected


def preserve(root,trees,expected,inventory):
    for p,raw in expected.items():
        need((root/p).is_file() and (root/p).read_bytes()==raw,'changed frozen union: '+p)
    known=set().union(*(set(t) for t in trees.values()))
    need(not inventory-known-ADDITIONS,'unregistered addition: '+str(sorted(inventory-known-ADDITIONS)))
    return {'strategic_commit':STRATEGIC,'causal_main_commit':CAUSAL,'frozen_union_files':len(expected),
            'main_ledgers_preserved_with_strategic_prefix':sorted(LEDGERS),
            'frozen_union_sha256':sha256(json.dumps({p:sha256(raw).hexdigest() for p,raw in sorted(expected.items())},sort_keys=True).encode()).hexdigest()}


def execute(root,args):
    run=subprocess.run([sys.executable,*args],cwd=root,env=ENV,capture_output=True,text=True)
    need(run.returncode==0,'acceptance failed: '+' '.join(args)+'\n'+run.stderr[-16000:])
    return run.stdout


def normalized(x):
    if isinstance(x,dict):return {k:normalized(v) for k,v in x.items() if k not in {'python','optimized'}}
    if isinstance(x,list):return [normalized(v) for v in x]
    return x


def run(mode='all',verify_retained=False):
    need(mode in ('all','strategic','causal','history'),'unknown mode')
    trees,expected=snapshots()
    inventory=set(git('ls-files').decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
    result={'mode':mode,'preservation':preserve(ROOT,trees,expected,inventory)}
    # Both frozen lineages must reject mutation, even where their older scope guards differ.
    with tempfile.TemporaryDirectory() as folder:
        root=Path(folder)
        for p,raw in expected.items():
            dest=root/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
        controls=[]
        for p in ('verification/diagnostic_erasure/final-results.json','verification/longitudinal_causal_kernel_fibres/results.json'):
            dest=root/p;dest.write_bytes(expected[p]+b' ')
            try:preserve(root,trees,expected,set(expected))
            except RuntimeError as e:need('changed frozen union: '+p==str(e),'wrong mutation failure');controls.append(p)
            else:raise RuntimeError('mutation accepted')
            dest.write_bytes(expected[p])
        try:preserve(root,trees,expected,set(expected)|{'docs/history/releases/unregistered.md'})
        except RuntimeError as e:need('unregistered addition:' in str(e),'wrong addition failure');controls.append('unregistered addition')
        else:raise RuntimeError('unregistered addition accepted')
        result['rejection_controls']=controls
    # Living links must identify a usable current route; historical docs retain their old instructions.
    links=0
    for p in LIVING|{'verification/combined_acceptance/README.md'}:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',(ROOT/p).read_text()):
            target=target.strip('<>').split('#',1)[0]
            if not target or '://' in target or target.startswith('mailto:'):continue
            # A first run precedes creation of the receipt; it is separately required on retained verification.
            if (ROOT/p).parent.joinpath(target).resolve()==(ROOT/RECORD).resolve() and not verify_retained:continue
            need(((ROOT/p).parent/target).exists(),'broken current link: '+p+' -> '+target);links+=1
    # Link count intentionally excludes the record in both modes for deterministic observations.
    result['current_links_checked']=True
    for ref,label in ((STRATEGIC,'strategic'),(CAUSAL,'causal')):
        if label=='causal' and mode not in ('all','causal'):continue
        if label=='strategic' and mode=='causal':continue
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'snapshot'
            subprocess.run(['git','clone','--quiet','--no-local','--no-checkout',str(ROOT),str(root)],env=ENV,check=True)
            subprocess.run(['git','-c','advice.detachedHead=false','checkout','--quiet','--detach',ref],cwd=root,env=ENV,check=True)
            if label=='strategic':
                flags=[] if mode=='all' else ['--'+mode]
                result['strategic']=json.loads(execute(root,['verification/diagnostic_erasure/acceptance.py',*flags,'--verify-retained']))
            else:
                raw=execute(root,['verification/longitudinal_causal_kernel_fibres/run_checks.py'])
                body=raw.split('LONGITUDINAL_CAUSAL_KERNEL_FIBRE_RESULT_BEGIN\n',1)[1].split('\nLONGITUDINAL_CAUSAL_KERNEL_FIBRE_RESULT_END',1)[0]
                r=json.loads(body)
                need(r['status']=='passed' and r['failed']==0 and r['retained_result_present_and_source_bound'],'causal replay did not validate retained evidence')
                result['causal']={k:r[k] for k in ('status','failed','normal_optimized_equal','passed_per_mode','rejections_per_mode','results','current_checks','joint_law_passed_per_mode','preservation','retained_result_present_and_source_bound','source_sha256')}
    # Execute the actual integrated tree too; preservation alone is not a runtime compatibility claim.
    for label,path in (('live_strategic','verification/diagnostic_erasure/checks.py'),
                       ('live_causal','verification/longitudinal_causal_kernel_fibres/checks.py')):
        if mode=='history' or (mode=='causal' and label=='live_strategic') or (mode=='strategic' and label=='live_causal'):continue
        outputs=[normalized(json.loads(execute(ROOT,[*flags,path]))) for flags in ([],['-O'])]
        need(outputs[0]==outputs[1],'integrated normal/optimized mismatch: '+label)
        result[label]=outputs[0]
    if verify_retained:
        record=json.loads((ROOT/RECORD).read_text())
        sources=ADDITIONS-{RECORD}|LIVING|WORKFLOWS
        need(set(record['source_files'])==sources,'combined manifest coverage')
        for p,h in record['source_files'].items():
            need(sha256((ROOT/p).read_bytes()).hexdigest()==h,'changed integrated source: '+p)
            need(sha256(git('show',record['source_commit']+':'+p)).hexdigest()==h,'unbound integrated source: '+p)
        def subset(a,b):return all(k=='mode' or (k in b and (subset(v,b[k]) if isinstance(v,dict) else v==b[k])) for k,v in a.items())
        need(subset(result,record['validation']),'combined observation mismatch')
    return result

if __name__=='__main__':
    flags=set(sys.argv[1:]);need(flags<={'--strategic','--causal','--history','--verify-retained'},'unknown flags')
    modes=flags&{'--strategic','--causal','--history'};need(len(modes)<=1,'multiple modes')
    print(json.dumps(run(next(iter(modes))[2:] if modes else 'all','--verify-retained' in flags),sort_keys=True,indent=2))
