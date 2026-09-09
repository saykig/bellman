"""Render a release asset from immutable Git objects; performs no publication."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]
TAG='v0.0.7'
NOTE='docs/history/releases/v0.0.7-decisions-evidence-and-credible-promises.md'
RECEIPTS={
 'shared_consistency':('verification/sequential_consistency/results.json',[
     'foundations/BELLMAN_SEQUENTIAL_CREDIBILITY_UNDER_UNCERTAINTY.md',
     'foundations/BELLMAN_SEQUENTIAL_CREDIBILITY_CONSISTENCY_ADDENDUM.md',
     'reviews/SEQUENTIAL_CREDIBILITY_RESEARCH_REVIEW_2026_09_08.md']),
 'public_copy_reduction':('verification/history_reduction/results.json',[
     'foundations/BELLMAN_PUBLIC_TAG_HISTORY_REDUCTION.md','reviews/PUBLIC_TAG_HISTORY_REDUCTION_REVIEW_2026_09_08.md']),
 'diagnostic_obstruction':('verification/diagnostic_erasure/final-results.json',[
     'foundations/BELLMAN_DIAGNOSTIC_HISTORY_ERASURE_OBSTRUCTION.md','reviews/DIAGNOSTIC_HISTORY_ERASURE_REVIEW_2026_09_08.md']),
 'causal_kernel_fibres':('verification/longitudinal_causal_kernel_fibres/results.json',[
     'foundations/BELLMAN_LONGITUDINAL_CAUSAL_KERNEL_FIBRES_AND_PERSISTENT_DECISIONS.md']),
 'combined_acceptance':('verification/combined_acceptance/results.json',[]),
}


def need(ok,message):
    if not ok:raise RuntimeError(message)


def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)


def build(commit,accepted_head):
    commit=git('rev-parse',commit+'^{commit}').decode().strip()
    accepted_head=git('rev-parse',accepted_head+'^{commit}').decode().strip()
    need(git('rev-parse',commit+'^{tree}')==git('rev-parse',accepted_head+'^{tree}'),'release tree differs from accepted PR head')
    def raw(path,ref=commit):return git('show',ref+':'+path)
    def artifact(path):return {'path':path,'sha256':sha256(raw(path)).hexdigest(),'url':f'https://github.com/saykig/bellman/blob/{commit}/{path}'}
    components={}
    for name,(receipt,paths) in RECEIPTS.items():
        r=json.loads(raw(receipt));source=r.get('source_commit',r.get('executed_source_commit'))
        hashes=r.get('source_files',r.get('source_sha256'))
        need(type(source) is str and type(hashes) is dict,'receipt lacks source binding: '+receipt)
        for path,h in hashes.items():
            need(sha256(raw(path,source)).hexdigest()==h,'historical receipt source mismatch: '+path)
            if name=='combined_acceptance':need(sha256(raw(path)).hexdigest()==h,'released source differs from accepted source: '+path)
        components[name]={'receipt':artifact(receipt),'recorded_source_commit':source,'artifacts':[artifact(p) for p in paths]}
    combined=json.loads(raw(RECEIPTS['combined_acceptance'][0]))
    v=combined['validation']
    for parent in ('strategic_commit','causal_main_commit'):
        need(subprocess.run(['git','merge-base','--is-ancestor',v['preservation'][parent],commit],cwd=ROOT).returncode==0,'release does not include both lineages')
    body=raw(NOTE).decode().replace('{{RELEASE_COMMIT}}',commit)
    manifest={
      'schema':'bellman.research-release.v1','tag':TAG,'prerelease':True,'released_commit':commit,
      'released_tree':git('rev-parse',commit+'^{tree}').decode().strip(),'accepted_pr_head':accepted_head,
      'previous_release':{'tag':'v0.0.6','commit':git('rev-parse','v0.0.6^{commit}').decode().strip(),
                          'historical_index':artifact('docs/history/releases/manifest.json')},
      'release_note_template':artifact(NOTE),'rendered_release_note_sha256':sha256(body.encode()).hexdigest(),
      'components':components,
      'inherited_since_previous_release':[artifact(p) for p in (
        'foundations/BELLMAN_MULTISTREAM_COLLECTION_AND_DECISIONS.md',
        'verification/multistream_collection/results.json',
        'foundations/BELLMAN_STATISTICAL_RECTANGLES_TO_CORNER_MODEL_GUARANTEES.md',
        'verification/statistical_corner_models/results.json',
        'foundations/BELLMAN_UNSAFE_SET_REACHABILITY_AND_CONSTRAINED_SELECTION.md',
        'verification/unsafe_set_reachability/results.json',
        'foundations/BELLMAN_FINITE_CAUSAL_IDENTIFICATION_AND_DECISION_CERTIFICATION.md',
        'verification/finite_causal_identification/results.json',
        'foundations/BELLMAN_TWO_STAGE_LONGITUDINAL_CAUSAL_POLICY_AND_SEQUENTIAL_BRIDGE.md',
        'verification/longitudinal_causal_policy/results.json')],
      'validation':{'recorded_source_commit':combined['source_commit'],
        'command':'PYTHONDONTWRITEBYTECODE=1 python verification/combined_acceptance/acceptance.py --verify-retained',
        'dependency_command':'python -m pip install -r verification/sequential_consistency/requirements.txt',
        'status':'passed','frozen_union_files':v['preservation']['frozen_union_files'],
        'frozen_union_sha256':v['preservation']['frozen_union_sha256'],
        'causal_cases_per_mode':v['live_causal']['passed'],'causal_rejections_per_mode':v['live_causal']['rejections'],
        'diagnostic_local_action_values':len(v['live_strategic']['received']['conditional_action_values']),
        'diagnostic_rejections':len(v['live_strategic']['rejections']),
        'normal_optimized_equal':True,
        'observation_scope':'Receipt records its own source execution; release tree matches accepted PR tree. Historical observations are not relabelled as release-commit runs.'},
      'claim_status':{'analytical_proofs':'retained, bounded, not proof-assistant verified',
                      'executable_checks':'exact bounded references with retained independent receiving controls',
                      'formal_verification':False,'empirical_validation':False,'engineering_integration':False},
      'limitations':['Supplied probabilities, utilities, evidence feasibility, memory and causal premises.',
                     'No general history quotient, arbitrary assessment transport or complete equilibrium search.',
                     'No general mechanism composition or optimum.',
                     'No causal-to-strategic bridge from component coexistence.',
                     'No authority to act or production-readiness claim.']}
    return manifest,body

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--commit',required=True)
    parser.add_argument('--accepted-head',required=True);parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args();manifest,body=build(args.commit,args.accepted_head)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for name,data in [('bellman-v0.0.7-manifest.json',json.dumps(manifest,sort_keys=True,indent=2)+'\n'),('release-notes.md',body)]:
        with (args.output_dir/name).open('x') as f:f.write(data)
    print(json.dumps({'released_commit':manifest['released_commit'],'files':['bellman-v0.0.7-manifest.json','release-notes.md']},sort_keys=True))
