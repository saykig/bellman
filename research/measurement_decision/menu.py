"""Finite menu composition over the existing exact Decision Lab receiver."""
from __future__ import annotations
import argparse
import hashlib
import importlib
import importlib.abc
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
from fractions import Fraction

PIN = 'e5f77dfcf929708951f4673b3f394461ef09c752'
BASE = Path(__file__).resolve().parent

def wire(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def strict(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate key')
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=pairs, parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite')))

def rational(value):
    if not isinstance(value, str):
        raise ValueError('rational string required')
    q = Fraction(value)
    if value != f'{q.numerator}/{q.denominator}':
        raise ValueError('noncanonical rational')
    return q

class NoProducer(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'writ_decision_lab.solver' or fullname.startswith('writ_decision_lab.solver.'):
            raise ImportError('producer disabled')
        return None

def engine(repository, target, receiving):
    """Load exact committed source without changing donor checkout or importing __init__."""
    paths = subprocess.check_output(['git','-C',str(repository),'ls-tree','-r','--name-only',PIN,'src/writ_decision_lab']).decode().splitlines()
    manifest = []
    for name in paths:
        if not name.endswith('.py'):
            continue
        data = subprocess.check_output(['git','-C',str(repository),'show',f'{PIN}:{name}'])
        p = target / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        manifest.append({'path':name,'sha256':digest(data)})
    if not manifest:
        raise ValueError('missing pinned engine')
    package = types.ModuleType('writ_decision_lab')
    package.__path__ = [str(target/'src/writ_decision_lab')]
    sys.modules['writ_decision_lab'] = package
    if receiving:
        sys.meta_path.insert(0, NoProducer())
    return manifest

def inputs(data):
    case = strict(data)
    keys = {'schema','criterion','states','prior','actions','losses','loss_unit','measurements'}
    if set(case) != keys or case['schema'] != 'bellman.measurement-menu.v1' or case['criterion'] != 'bayesian-expected-loss':
        raise ValueError('unsupported subject or criterion')
    ms = case['measurements']
    if not isinstance(ms, list) or not 1 <= len(ms) <= 32:
        raise ValueError('bounded nonempty menu required')
    names = [m['name'] for m in ms]
    if any(not isinstance(n,str) or not n for n in names) or len(set(names)) != len(names):
        raise ValueError('unique names required')
    if names.count('no_measurement') != 1:
        raise ValueError('no-measurement baseline required')
    pairs = []
    for m in ms:
        if set(m) != {'name','outcomes','likelihood','cost'}:
            raise ValueError('unsupported measurement effects or fields')
        if m['name'] == 'no_measurement' and (m['cost'] != '0/1' or len(m['outcomes']) != 1 or m['likelihood'] != [['1/1'] for _ in case['states']]):
            raise ValueError('invalid baseline')
        model = {'schema':'wdl.model.v1','states':case['states'],'outcomes':m['outcomes'],'prior':case['prior'],'likelihood':m['likelihood']}
        query = {'schema':'wdl.query.v1','semantics':'finite-one-observation.v1','state_order':case['states'],'actions':case['actions'],'losses':case['losses'],'loss_unit':case['loss_unit'],'cost':m['cost']}
        pairs.append((m['name'],wire(model),wire(query)))
    return pairs

def ranking(answers):
    risks = {name:rational(a['acquisition_risks']['observe_once']) for name,a in answers}
    least = min(risks.values())
    baseline = risks['no_measurement']
    return {'forced_risks':{n:f'{v.numerator}/{v.denominator}' for n,v in risks.items()},
            'net_benefits':{n:f'{(baseline-v).numerator}/{(baseline-v).denominator}' for n,v in risks.items()},
            'minimizers':[n for n,v in risks.items() if v == least]}

def run(data, manifest, retained=None):
    receiving = retained is not None
    pairs = inputs(data)
    if receiving:
        if set(retained) != {'schema','subject_sha256','engine_commit','engine_manifest','results','ranking'}:
            raise ValueError('result fields')
        if retained['schema'] != 'bellman.measurement-result.v1' or retained['subject_sha256'] != digest(data) or retained['engine_commit'] != PIN or retained['engine_manifest'] != manifest:
            raise ValueError('subject or source identity mismatch')
        if list(retained['results']) != [n for n,_,_ in pairs]:
            # JSON object order is not authority; membership is.
            if set(retained['results']) != {n for n,_,_ in pairs}:
                raise ValueError('measurement menu mismatch')
    check = importlib.import_module('writ_decision_lab.consumer').check_and_load
    solve = None if receiving else importlib.import_module('writ_decision_lab.solver').solve_bytes
    answers, results = [], {}
    for name,model,query in pairs:
        result = retained['results'][name].encode() if receiving else solve(model,query)
        check(model,query,result)
        answers.append((name,strict(result)['answer']))
        results[name] = result.decode()
    rank = ranking(answers)
    if receiving and retained['ranking'] != rank:
        raise ValueError('ranking mismatch')
    return {'schema':'bellman.measurement-result.v1','subject_sha256':digest(data),'engine_commit':PIN,'engine_manifest':manifest,'results':results,'ranking':rank}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode',choices=['produce','receive'])
    ap.add_argument('case',type=Path)
    ap.add_argument('result',type=Path)
    ap.add_argument('--engine-repository',type=Path,required=True)
    args=ap.parse_args()
    with tempfile.TemporaryDirectory(prefix='bellman-measurement-') as tmp:
        manifest=engine(args.engine_repository,Path(tmp),args.mode=='receive')
        if args.mode=='receive':
            try:
                importlib.import_module('writ_decision_lab.solver')
            except ImportError as exc:
                if str(exc) != 'producer disabled':
                    raise
            else:
                raise RuntimeError('producer import unexpectedly enabled')
        data=args.case.read_bytes()
        if args.mode=='produce':
            answer=run(data,manifest)
            with args.result.open('xb') as f:
                f.write(wire(answer))
        else:
            run(data,manifest,strict(args.result.read_bytes()))
            print('checked: complete menu, exact policies and ranking; producer disabled')
if __name__ == '__main__':
    main()
