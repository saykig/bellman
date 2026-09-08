"""Exact positive fixtures, failure witnesses, and adversarial receiving controls."""
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from fixtures import fixture, renamed
from producer import produce, value
from receiver import receive
from subject import Invalid, digest, require, rational, validate

HERE=Path(__file__).resolve().parent

def execute():
    facts={}; rejections=[]
    def check(label,condition): require(condition,'failed check: '+label)
    def reject(label,s,c,epsilon='0'):
        try: receive(s,c,epsilon)
        except Invalid:
            rejections.append(label)
        else: raise RuntimeError('accepted invalid: '+label)
    s=fixture(); c=produce(s)
    facts['positive']=receive(s,c)
    check('all information sets',len(c['rows'])==80 and c['max_gain']=='0')
    for name,m in s['models'].items():
        check('B root participation',value(s,m,s['root'],'B',{})==1)
        for row in c['rows']:
            if row['model']==name and row['info']=='disclose.good': check('A good participation',row['baseline']=='7/5')
            if row['model']==name and row['info']=='disclose.bad': check('A bad participation',row['baseline']=='0')
    facts['participation']={'A_good':'7/5','A_bad':'0','B_root':'1','outside_options':'0'}
    weak=fixture(bond=5); wc=produce(weak); receive(weak,wc)
    check('bond weakness',wc['max_gain']=='1/2' and wc['status']=='profitable-deviation')
    facts['weak_bond']={'max_gain':wc['max_gain'],'witness':next(r for r in wc['rows'] if r['gain']=='1/2')}
    loose=produce(weak,'1/2'); receive(weak,loose,'1/2')
    reject('changed query tolerance',weak,loose)
    costly=fixture(fee=F(3,2)); cc=produce(costly); receive(costly,cc)
    check('participation reversal',cc['max_gain']=='1/10')
    check('deterrence still holds',all(F(r['gain'])==0 for r in cc['rows'] if r['info'].startswith('act.') and r['info'].endswith('.bond')))
    facts['mechanism_cost']={'max_gain':cc['max_gain'],'good_initial':next(r['baseline'] for r in cc['rows'] if r['info']=='disclose.good')}
    subset=deepcopy(weak); subset['models'].pop('g=3,p=1/2'); sc=produce(subset); receive(subset,sc)
    check('model restriction',sc['max_gain']=='0')
    facts['restriction']={'before':wc['max_gain'],'after':sc['max_gain']}
    rs=renamed(s); rc=produce(rs); receive(rs,rc)
    check('renaming rows',sorted((r['model'],r['baseline'],r['best'],r['gain'],r['plans']) for r in rc['rows'])==sorted((r['model'],r['baseline'],r['best'],r['gain'],r['plans']) for r in c['rows']))
    check('identity changed',digest(s)!=digest(rs))
    reject('stale certificate after exact renaming',rs,c)
    perturbed=deepcopy(s)
    for m in perturbed['models'].values():
        for v,u in m['payoffs'].items():
            delta=F(-1,10) if v.startswith('comply.') else F(1,10)
            u['A']=str(F(u['A'])+delta)
    pc=produce(perturbed); receive(perturbed,pc)
    check('two delta bound',pc['max_gain']=='1/5')
    facts['representation']={'exact_renaming_gain':rc['max_gain'],'delta':'1/10','perturbed_max_gain':pc['max_gain'],'bound':'1/5'}
    # An explicit full-continuation example; local root action change alone loses.
    one={'schema':s['schema'],'root':'r','nodes':{'r':{'kind':'player','player':'A','info':'r','edges':{'stay':'z','enter':'h'}},'h':{'kind':'player','player':'A','info':'h','edges':{'exit':'x','take':'t'}},'z':{'kind':'terminal'},'x':{'kind':'terminal'},'t':{'kind':'terminal'}},'profile':{'r':{'stay':'1','enter':'0'},'h':{'exit':'1','take':'0'}},'models':{'only':{'chance':{},'payoffs':{'z':{'A':'0','B':'0'},'x':{'A':'-1','B':'0'},'t':{'A':'1','B':'0'}},'beliefs':{'r':{'r':'1'},'h':{'h':'1'}}}}}
    oc=produce(one); receive(one,oc)
    root=next(r for r in oc['rows'] if r['info']=='r')
    check('whole continuation',root['gain']=='1' and root['witness']=={'h':'take','r':'enter'})
    check('one step misses',value(one,one['models']['only'],'r','A',{'r':'enter'})==-1)
    facts['whole_continuation']={'root_gain':root['gain'],'one_step_value':'-1','off_path_gain':oc['max_gain']}
    threat=deepcopy(one)
    threat['nodes']['h']['player']='B'
    threat['models']['only']['payoffs']={'z':{'A':'0','B':'1'},'x':{'A':'-1','B':'-1'},'t':{'A':'1','B':'0'}}
    tc=produce(threat); receive(threat,tc)
    check('root-Nash threat fails sequential',next(r for r in tc['rows'] if r['info']=='r')['gain']=='0' and next(r for r in tc['rows'] if r['info']=='h')['gain']=='1')
    facts['noncredible_threat']={'A_root_gain':'0','B_off_path_gain':'1'}
    # A maxmin solution is not an every-model best response.
    def worst(x): return min(x,1-x)
    check('robust criterion distinction',worst(F(1,2))==F(1,2) and 1-F(1,2)==F(1,2))
    facts['maxmin_vs_uniform']={'maxmin_mixture':'1/2','modelwise_gain':'1/2','reason':'min(x,1-x)<=1/2 for every x in [0,1]'}
    # Analytic controls; samples are arithmetic checks, not continuous proofs.
    check('repeated parameter corners',F(0)*(1-F(0))==0 and F(1)*(1-F(1))==0 and F(1,2)*(1-F(1,2))==F(1,4))
    check('conditional ratio not affine',F(1,2)/(1+F(1,2))==F(1,3) and F(1,3)!=F(1,4))
    facts['continuous_controls']={'repeated_parameter_endpoints':['0','0'],'interior':'1/4','conditional_ratio_at_half':'1/3','linear_interpolation':'1/4','generic_continuous_check':'unsupported'}
    # Mutations of intended subject; a fresh hash cannot excuse malformed semantics.
    def subject_mutation(label,change):
        q=deepcopy(s); change(q); cert=deepcopy(c); cert['subject_sha256']=digest(q); reject(label,q,cert)
    subject_mutation('on-path false posterior',lambda q:q['models']['g=1,p=1/2']['beliefs']['disclose.good'].update({'disclose.good':'0'}))
    subject_mutation('chance not normalized',lambda q:q['models']['g=1,p=1/2']['chance']['root'].update({'good':'3/4'}))
    subject_mutation('noncanonical rational',lambda q:q['profile']['disclose.good'].update({'G':'1.0'}))
    subject_mutation('profile omits information set',lambda q:q['profile'].pop('disclose.bad'))
    subject_mutation('hidden model indexed strategy',lambda q:q['profile'].update({'model:g=1':{'G':'1'}}))
    subject_mutation('zero event assessment omitted',lambda q:q['models']['g=1,p=1/2']['beliefs'].pop('receive.N.bond'))
    subject_mutation('extra unreachable node',lambda q:q['nodes'].update({'hidden':{'kind':'terminal'}}))
    def merge(q):
        # Both A nodes have the same menu but A would forget its private evidence and own earlier action.
        q['nodes']['act.good.N.bond']['info']='act.bad.N.bond'
    subject_mutation('forgotten private history',merge)
    def erase(q):
        q['nodes']['receive.bad.B.bond']['info']='receive.G.bond'
    subject_mutation('evidence erasure without assessment/profile repair',erase)
    def cert_mutation(label,change):
        k=deepcopy(c); change(k); reject(label,s,k)
    cert_mutation('missing row',lambda k:k['rows'].pop())
    cert_mutation('duplicate row',lambda k:k['rows'].__setitem__(0,deepcopy(k['rows'][1])))
    cert_mutation('false bound',lambda k:k['rows'][0].update({'gain':'-1'}))
    cert_mutation('false best value',lambda k:k['rows'][0].update({'best':'900'}))
    cert_mutation('false aggregate',lambda k:k.update({'max_gain':'1'}))
    cert_mutation('false status',lambda k:k.update({'status':'sequential-equilibrium'}))
    cert_mutation('illegal deviation',lambda k:k['rows'][0]['witness'].update({next(iter(k['rows'][0]['witness'])):'forge'}))
    cert_mutation('missing deviation information',lambda k:k['rows'][0]['witness'].pop(next(iter(k['rows'][0]['witness']))))
    cert_mutation('false enumeration count',lambda k:k['rows'][0].update({'plans':0}))
    cert_mutation('stale identity',lambda k:k.update({'subject_sha256':'0'*64}))
    reject('changed mechanism without revalidation',weak,c)
    # The receiver is launched with only its own source plus subject validation; no producer import exists.
    with tempfile.TemporaryDirectory() as d:
        d=Path(d)
        for name in ('receiver.py','subject.py'): shutil.copy2(HERE/name,d/name)
        (d/'subject.json').write_text(json.dumps(s)); (d/'certificate.json').write_text(json.dumps(c))
        command=[sys.executable]+(['-O'] if not __debug__ else [])+[str(d/'receiver.py'),str(d/'subject.json'),str(d/'certificate.json')]
        result=subprocess.run(command,capture_output=True,text=True,check=True)
        check('producer disabled receiving',json.loads(result.stdout)['max_gain']=='0')
    facts['producer_disabled']=True
    facts['receiver_rejections']=rejections
    return facts,s,c

if __name__=='__main__':
    facts,_,_=execute()
    print(json.dumps(facts,sort_keys=True,indent=2))
