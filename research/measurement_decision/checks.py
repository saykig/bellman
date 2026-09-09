"""Independent exact menu checks; optional full donor receiving in a separate process."""
import argparse
import copy
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import menu

BASE=Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def direct(data, retained):
    """Recompute claimed operation by exhaustive signal-only policies, without donor imports."""
    pairs=menu.inputs(data)
    case=menu.strict(data)
    require(retained['subject_sha256']==menu.digest(data),'subject binding')
    require(retained['engine_commit']==menu.PIN,'engine pin')
    require(set(retained['results'])=={n for n,_,_ in pairs},'complete menu')
    p=list(map(menu.rational,case['prior']))
    states=case['states']; actions=case['actions']
    require(1<=len(states)<=8 and len(set(states))==len(states),'state labels')
    require(1<=len(actions)<=8 and len(set(actions))==len(actions),'action labels')
    require(len(p)==len(states) and all(v>=0 for v in p) and sum(p)==1,'prior')
    losses=[list(map(menu.rational,row)) for row in case['losses']]
    require(len(losses)==len(actions) and all(len(row)==len(p) for row in losses),'loss dimensions')
    r0=min(sum(p[s]*row[s] for s in range(len(p))) for row in losses)
    risks={}; policies={}; counts={}
    for m,(name,mb,qb) in zip(case['measurements'],pairs):
        k=[list(map(menu.rational,row)) for row in m['likelihood']]
        nx=len(m['outcomes']); na=len(actions)
        require(1<=nx<=6 and na**nx<=4096 and len(set(m['outcomes']))==nx,'outcome bounds')
        require(len(k)==len(p) and all(len(row)==nx and all(v>=0 for v in row) and sum(row)==1 for row in k),'channel')
        cost=menu.rational(m['cost']);require(cost>=0,'cost')
        values=[]
        for policy in product(range(na),repeat=nx):
            value=cost+sum(p[s]*k[s][x]*losses[policy[x]][s] for s in range(len(p)) for x in range(nx))
            values.append((value,policy))
        best=min(v for v,_ in values);risks[name]=best
        policies[name]=[pol for v,pol in values if v==best];counts[name]=len(values)
        raw=retained['results'][name].encode(); record=menu.strict(raw);answer=record['answer']
        require(record['input_bindings']=={'model_sha256':'sha256:'+menu.digest(mb),'query_sha256':'sha256:'+menu.digest(qb)},'component bindings')
        require(F(answer['current_risk'])==r0 and F(answer['observed_risk'])==best-cost,'conditional risk')
        require(F(answer['acquisition_risks']['observe_once'])==best and F(answer['acquisition_risks']['act_now'])==r0,'cost risk')
        require(F(answer['evsi'])==r0-best+cost and F(answer['net_value'])==r0-best,'benefit')
        # Check returned branch action sets, including ties, against direct joint losses.
        require(len(answer['branches'])==nx,'branch coverage')
        for x,branch in enumerate(answer['branches']):
            require(branch['outcome']==m['outcomes'][x],'outcome identity')
            mass=sum(p[s]*k[s][x] for s in range(len(p)))
            require(F(branch['mass'])==mass,'branch mass')
            if mass==0:
                require(branch['argmin'] is None and branch['status']=='impossible','impossible branch')
            else:
                jr=[sum(p[s]*k[s][x]*row[s] for s in range(len(p))) for row in losses]
                require(branch['argmin']==[a for a,v in zip(actions,jr) if v==min(jr)],'signal-only action sets')
        require(len(answer['branches'])==nx,'branch coverage')
    expected={n for n,r in risks.items() if r==min(risks.values())}
    rank=retained['ranking']
    require(set(rank['minimizers'])==expected and len(rank['minimizers'])==len(expected),'ranking')
    require(set(rank['forced_risks'])==set(risks) and set(rank['net_benefits'])==set(risks),'ranking coverage')
    for n,r in risks.items():
        require(F(rank['forced_risks'][n])==r and F(rank['net_benefits'][n])==r0-r,'ranked values')
    return {'policies_enumerated':counts,'minimizers':sorted(expected)}

def controls(data,retained):
    rejected=[]
    def reject(name,case=None,result=None):
        try:
            direct(data if case is None else menu.wire(case),retained if result is None else result)
        except (ValueError,KeyError,TypeError,ZeroDivisionError):
            rejected.append(name)
        else:
            raise RuntimeError('accepted false control: '+name)
    # Rebind mutated input identities so malformed-input controls reach arithmetic validation.
    for name,mutate in [
        ('invalid_channel',lambda c:c['measurements'][1]['likelihood'][0].__setitem__(0,'2/1')),
        ('malformed_prior',lambda c:c['prior'].__setitem__(0,'2/1')),
        ('negative_cost',lambda c:c['measurements'][1].__setitem__('cost','-1/1')),
        ('missing_baseline',lambda c:c['measurements'].pop(0)),
        ('hidden_model_policy_field',lambda c:c.__setitem__('model_policy',['commit_C','commit_D'])),
        ('state_changing_measurement',lambda c:c['measurements'][1].__setitem__('transition',[])),
    ]:
        c=menu.strict(data);mutate(c);r=copy.deepcopy(retained);r['subject_sha256']=menu.digest(menu.wire(c));reject(name,c,r)
    r=copy.deepcopy(retained);r['subject_sha256']='0'*64;reject('stale_subject',result=r)
    r=copy.deepcopy(retained);del r['results']['no_measurement'];reject('omitted_result',result=r)
    r=copy.deepcopy(retained);r['ranking']['minimizers']=['no_measurement'];reject('false_ranking',result=r)
    for label,mutate in [
        ('hidden_state_oracle',lambda a:a.__setitem__('observed_risk','-100/1')),
        ('cost_omitted',lambda a:a['acquisition_risks'].__setitem__('observe_once',a['observed_risk'])),
        ('wrong_action',lambda a:a['branches'][0].__setitem__('argmin',['commit_C'])),
        ('relabelled_signal',lambda a:a['branches'][0].__setitem__('outcome','T')),
    ]:
        r=copy.deepcopy(retained);obj=menu.strict(r['results']['conditional']);mutate(obj['answer']);r['results']['conditional']=menu.wire(obj).decode();reject(label,result=r)
    c=menu.strict(data);c['measurements'][1]['cost']='3/1';reject('changed_cost_old_receipt',c)
    c=menu.strict(data);c['losses'][0][0]='1/1';reject('changed_decision_old_receipt',c)
    return rejected

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--engine-repository',type=Path);args=ap.parse_args()
    observations={}
    for name in ('afy','maintenance','tie'):
        data=(BASE/(name+'-design.json')).read_bytes();result=menu.strict((BASE/(name+'-result.json')).read_bytes())
        observations[name]=direct(data,result)
        if name=='afy':
            observations['rejection_controls']=controls(data,result)
            rank=result['ranking']
            require(rank['net_benefits']['weak_conditional']=='-1/1000','informative zero-value control')
            require(rank['net_benefits']['conditional']=='2491/84000','conditional positive')
            require(rank['net_benefits']['utility']=='97/2800','utility value')
            require(rank['minimizers']==['utility'],'utility winner')
        if name=='tie':
            require(result['ranking']['minimizers']==['no_measurement','free_signal'],'preserve acquisition ties')
        if args.engine_repository:
            for opt in ([],['-O']):
                subprocess.run([sys.executable,*opt,str(BASE/'menu.py'),'receive',str(BASE/(name+'-design.json')),str(BASE/(name+'-result.json')),'--engine-repository',str(args.engine_repository)],check=True,stdout=subprocess.PIPE)
    observations['donor_receiving']='normal and optimized, producer imports blocked' if args.engine_repository else 'not executed; independent direct enumeration only'
    print(json.dumps(observations,sort_keys=True))
if __name__=='__main__':main()
