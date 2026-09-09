"""Bounded portable-use gate; no downstream adapter or authority inferred."""
import copy
import hashlib
import json
from pathlib import Path
import sys
from receiver import HERE,need,run as receive


def disposition(case,intended_use):
    need(case['schema']=='bellman.afy2024.portable-case.v1','portable schema mismatch')
    need(set(case['bindings'])=={'PLAN.md','source-manifest.json','first-results/parameters.json','first-results/results.json','first-run-manifest.json','receiving-checkpoint.json','prior-sensitivity-results.json','sensitivity-checkpoint.json'},'portable binding coverage')
    for path,digest in case['bindings'].items():
        target=(HERE/path).resolve(); need(target.is_relative_to(HERE),'outside portable scope')
        need(hashlib.sha256(target.read_bytes()).hexdigest()==digest,'portable evidence mismatch')
    fields={'operation','population','decision_time','conclusion','authority'}
    need(set(intended_use)==fields and set(case['intended_use'])==fields,'unregistered use context')
    changed=sorted(k for k in fields if intended_use[k]!=case['intended_use'][k])
    return {'old_evidence':'identity preserved; fresh receiving required',
        'applicability':'reassessment_required' if changed else 'same_declared_use',
        'changed_dependencies':changed,'human_disposition':case['human_disposition'],
        'authority_to_act':False,'downstream_integration':'not implemented'}


def run(raw):
    case=json.loads((HERE/'portable-case.json').read_text())
    receiving=receive(raw)
    same=disposition(case,case['intended_use']); changed=copy.deepcopy(case['intended_use'])
    changed['operation']='choose an institutional commitment mechanism'
    control=disposition(case,changed)
    need(control['applicability']=='reassessment_required' and not control['authority_to_act'],'changed use silently accepted')
    changed=copy.deepcopy(case['intended_use']); changed['decision_time']='current reported belief observed before own current action'
    timing=disposition(case,changed)
    need(timing['applicability']=='reassessment_required','timing reuse accepted')
    bad=copy.deepcopy(case); bad['bindings']['PLAN.md']='0'*64
    try: disposition(bad,bad['intended_use'])
    except ValueError: mismatch='rejected'
    else: raise RuntimeError('mismatched mathematical edition accepted')
    return {'fresh_receiving':receiving,'same_use':same,'changed_mechanism_use':control,
        'changed_report_timing':timing,'changed_evidence_identity':mismatch}

if __name__=='__main__': print(json.dumps(run(sys.argv[1]),indent=2))
