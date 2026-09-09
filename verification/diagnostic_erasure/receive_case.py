"""Independent receiving of one narrowly specified obstruction class and repair.

No candidate import; class recognition precedes use of the analytical odds theorem.
"""
from copy import deepcopy
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'sequential_consistency'))
from consistency_receiver import receive as receive_consistency
from witness import rational as Q, digest, demand, validate
from receiver import receive as receive_incentives, paths

QUERY='all-local-values-and-one-common-consistency-sequence.v1'


def recognize(s, public):
    """Recognize the entire binary null-disclosure game, not merely selected odds."""
    validate(s)
    demand(s['root']=='root','class-root')
    expected={'root'};chances={'root'};profiles={};terminals={}
    root=s['nodes']['root']
    demand(root=={'kind':'chance','edges':{q:'signal.'+q if public else 'A.'+q for q in ('g','b')}},'class-root-edges')
    for q in ('g','b'):
        if public:
            v='signal.'+q;expected.add(v);chances.add(v)
            demand(s['nodes'].get(v)=={'kind':'chance','edges':{z:'A.'+q+'.'+z for z in ('H','L')}},'class-signal')
        for z in (('H','L') if public else ('',)):
            suffix=q+('.'+z if z else '');a='A.'+suffix;b='B.'+suffix;I='B.'+z if public else 'B'
            expected.update((a,b))
            demand(s['nodes'].get(a)=={'kind':'player','player':'A','info':a,'edges':{'reveal':'reveal.'+suffix,'N':b}},'class-sender')
            demand(s['nodes'].get(b)=={'kind':'player','player':'B','info':I,'edges':{'accept':'accept.'+suffix,'reject':'reject.'+suffix}},'class-receiver')
            profiles[a]={'reveal':'1','N':'0'};profiles[I]={'accept':'0','reject':'1'}
            for act in ('reveal','accept','reject'):
                v=act+'.'+suffix;expected.add(v)
                demand(s['nodes'].get(v)=={'kind':'terminal'},'class-terminal')
                terminals[v]={'A':str(int(act=='reveal')),'B':str((1 if q=='g' else -1) if act=='accept' else 0)}
    demand(set(s['nodes'])==expected and s['profile']==profiles,'class-coverage-profile')
    joints={}
    for name,m in s['models'].items():
        demand(m['payoffs']==terminals and set(m['chance'])==chances,'class-payoff-chance')
        demand(all(Q(p)>0 for row in m['chance'].values() for p in row.values()),'class-strict-positivity')
        if public:
            joints[name]={(q,z):Q(m['chance']['root'][q])*Q(m['chance']['signal.'+q][z]) for q in ('g','b') for z in ('H','L')}
        # The obstruction preserves the specified interior assessment exactly.
        for I,row in m['beliefs'].items():
            demand(all(Q(p)==(1 if I.startswith('A.') else Q('1/2')) for p in row.values()),'class-assessment')
    return joints


def receive(c, expected_identity, expected_query=QUERY):
    demand(type(c) is dict and set(c)=={'schema','query','source','target','sender_retains_signal','source_warrant','private_warrant','target_incentives','individual_targets','identity','obstruction'},'case-schema')
    demand(c['schema']=='bellman.diagnostic-erasure-case.v1' and c['query']==expected_query==QUERY,'case-query')
    identity={key:digest(c[key]) for key in ('source','target','sender_retains_signal')}
    demand(c['identity']==identity==expected_identity,'case-identity')
    s,t,p=c['source'],c['target'],c['sender_retains_signal']
    joints=recognize(s,True);recognize(t,False)
    demand(set(s['models'])==set(t['models'])==set(p['models']),'case-models')
    required={}
    for name,m in t['models'].items():
        for q in ('g','b'):
            demand(Q(m['chance']['root'][q])==sum(joints[name][q,z] for z in ('H','L')),'not-marginal-erasure')
        required[name]=Q(m['chance']['root']['b'])/Q(m['chance']['root']['g'])
    ob=c['obstruction']
    demand(type(ob) is dict and set(ob)=={'models','required_ratios'},'obstruction-schema')
    pair=ob['models']
    demand(type(pair) is list and len(pair)==2 and all(type(n) is str and n in required for n in pair),'obstruction-pair')
    demand(ob['required_ratios']==[str(required[n]) for n in pair],'false-required-ratios')
    demand(required[pair[0]]!=required[pair[1]],'no-odds-obstruction')
    # Analytical necessity for ALL sequences: x_n/y_n must converge to BOTH ratios.
    sr=receive_consistency(s,c['source_warrant']);tr=receive_incentives(t,c['target_incentives'])
    demand(sr['max_gain']==tr['max_gain']=='0','unexpected-incentives')
    individual={}
    demand(set(c['individual_targets'])==set(t['models']),'individual-coverage')
    for name,item in c['individual_targets'].items():
        demand(type(item) is dict and set(item)=={'subject','warrant'},'individual-schema')
        singleton=deepcopy(t);singleton['models']={name:deepcopy(t['models'][name])}
        demand(item['subject']==singleton,'individual-subject')
        individual[name]=receive_consistency(singleton,item['warrant'])['status']
    # The restricted alternative leaves every sender information set intact, and
    # removes only the receiver's observation before its first and final move.
    shadow=deepcopy(s)
    for n in shadow['nodes'].values():
        if n.get('player')=='B':n['info']='B'
    shadow['profile'].pop('B.H');shadow['profile'].pop('B.L');shadow['profile']['B']={'accept':'0','reject':'1'}
    for name,m in shadow['models'].items():
        m['beliefs'].pop('B.H');m['beliefs'].pop('B.L')
        demand('B' in p['models'][name]['beliefs'],'private-assessment-missing')
        m['beliefs']['B']=p['models'][name]['beliefs']['B']
    demand(shadow==p,'not-receiver-only-erasure')
    for I in s['profile']:
        if I.startswith('A.'):
            demand(c['source_warrant']['witness'][I]==c['private_warrant']['witness'].get(I),'sender-witness-changed')
    pr=receive_consistency(p,c['private_warrant'])
    demand(pr['max_gain']=='0','private-incentives')
    # Independently check every pure local action value, rather than just maxima.
    local=[]
    for name,m in s['models'].items():
        for I,row in s['profile'].items():
            J='.'.join(I.split('.')[:2]) if I.startswith('A.') else 'B'
            owner='A' if I.startswith('A.') else 'B'
            for action in row:
                def val(game, model, info):
                    return sum(Q(b)*paths(game,model,h,owner,{info:action}) for h,b in model['beliefs'][info].items())
                sv=val(s,m,I);tv=val(t,t['models'][name],J)
                pv=val(p,p['models'][name],I if owner=='A' else 'B')
                demand(sv==tv==pv,'conditional-action-value-mismatch')
                local.append({'model':name,'info':I,'action':action,'value':str(sv)})
        demand(sum(Q(v) for h,v in p['models'][name]['beliefs']['B'].items() if h.startswith('B.g.'))==Q('1/2'),'private-quality-belief')
    return {'status':'checked-common-consistency-obstruction','query':QUERY,'identity':identity,
            'arbitrary_sequence_required_ratios':{n:str(v) for n,v in required.items()},
            'source_status':sr['status'],'target_assessed_max_gain':tr['max_gain'],
            'individual_target_statuses':individual,'receiver_only_status':pr['status'],
            'source_information_sets':len(s['profile']),'full_erasure_information_sets':len(t['profile']),
            'receiver_only_information_sets':len(p['profile']),'conditional_action_values':local}

if __name__=='__main__':
    with open(sys.argv[1]) as f:c=json.load(f)
    with open(sys.argv[2]) as f:identity=json.load(f)
    print(json.dumps(receive(c,identity),sort_keys=True,indent=2))
