"""Small explicit evidence game and candidate bundle; not a receiving dependency."""
from copy import deepcopy
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'sequential_consistency'))
from valuation_producer import produce
from cases import unit_witness
from witness import rational, digest
from producer import produce as incentive_produce


def game(joints, observed=True):
    nodes={'root':{'kind':'chance','edges':{q:'signal.'+q if observed else 'A.'+q for q in ('g','b')}}}
    profile={};payoffs={};models={}
    for q in ('g','b'):
        if observed:
            nodes['signal.'+q]={'kind':'chance','edges':{z:'A.'+q+'.'+z for z in ('H','L')}}
        for z in (('H','L') if observed else ('',)):
            suffix=q+('.'+z if z else '')
            a='A.'+suffix;b='B.'+suffix;I='B.'+z if observed else 'B'
            nodes[a]={'kind':'player','player':'A','info':a,'edges':{'reveal':'reveal.'+suffix,'N':b}}
            nodes[b]={'kind':'player','player':'B','info':I,'edges':{'accept':'accept.'+suffix,'reject':'reject.'+suffix}}
            profile[a]={'reveal':'1','N':'0'};profile[I]={'accept':'0','reject':'1'}
            for act in ('reveal','accept','reject'):
                v=act+'.'+suffix;nodes[v]={'kind':'terminal'}
                payoffs[v]={'A':str(int(act=='reveal')),'B':str((1 if q=='g' else -1) if act=='accept' else 0)}
    for name,j in joints.items():
        prior={q:sum(rational(j[q+'.'+z]) for z in ('H','L')) for q in ('g','b')}
        chance={'root':{q:str(p) for q,p in prior.items()}}
        if observed:
            chance.update({'signal.'+q:{z:str(rational(j[q+'.'+z])/prior[q]) for z in ('H','L')} for q in ('g','b')})
        beliefs={I:{I:'1'} for I in profile if I.startswith('A.')}
        if observed:
            beliefs.update({'B.'+z:{'B.'+q+'.'+z:'1/2' for q in ('g','b')} for z in ('H','L')})
        else:beliefs['B']={'B.g':'1/2','B.b':'1/2'}
        models[name]={'chance':chance,'payoffs':deepcopy(payoffs),'beliefs':beliefs}
    return {'schema':'bellman.assessed-credibility.v1','root':'root','nodes':nodes,'models':models,'profile':profile}


def build():
    joints={'high':{'g.H':'9/16','b.H':'3/16','g.L':'1/16','b.L':'3/16'},
            'low': {'g.H':'3/16','b.H':'1/16','g.L':'3/16','b.L':'9/16'}}
    source=game(joints);target=game(joints,False)
    w=unit_witness(source)
    for q,z,c in [('g','H','1'),('b','H','3'),('g','L','3'),('b','L','1')]:
        w['A.'+q+'.'+z]['N']['coefficient']=c
    private=deepcopy(source)
    for n in private['nodes'].values():
        if n.get('player')=='B':n['info']='B'
    private['profile'].pop('B.H');private['profile'].pop('B.L');private['profile']['B']={'accept':'0','reject':'1'}
    for name,m in private['models'].items():
        m['beliefs'].pop('B.H');m['beliefs'].pop('B.L')
        mass={key:rational(val)*rational(w['A.'+key]['N']['coefficient']) for key,val in joints[name].items()}
        total=sum(mass.values());m['beliefs']['B']={'B.'+key:str(v/total) for key,v in mass.items()}
    pw={I:deepcopy(row) for I,row in w.items() if I.startswith('A.')};pw['B']={'accept':{'coefficient':'1','order':1}}
    individual={}
    for name,m in target['models'].items():
        t=deepcopy(target);t['models']={name:deepcopy(m)};tw=unit_witness(t)
        tw['A.g']['N']['coefficient']=str(rational(m['chance']['root']['b'])/rational(m['chance']['root']['g']))
        individual[name]={'subject':t,'warrant':produce(t,tw)}
    return {'schema':'bellman.diagnostic-erasure-case.v1','query':'all-local-values-and-one-common-consistency-sequence.v1',
            'source':source,'target':target,'sender_retains_signal':private,
            'source_warrant':produce(source,w),'private_warrant':produce(private,pw),
            'target_incentives':incentive_produce(target),'individual_targets':individual,
            'identity':{'source':digest(source),'target':digest(target),'sender_retains_signal':digest(private)},
            'obstruction':{'models':['high','low'],'required_ratios':['3/5','5/3']}}

if __name__=='__main__':
    import json
    print(json.dumps(build(),sort_keys=True,indent=2))
