"""Exact transport checks and decisive falsifications; no assertions as gates."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from transfer_producer import produce
from transfer_receiver import receive
from reduction import verify_map,restrict,digest,rational
from examples import expand,matching,likelihood
from cases import evidence_case,unit_witness
from valuation_producer import produce as consistency_produce
from consistency_receiver import receive as consistent_receive
from receiver import paths
from subject import Invalid

ROOT=Path(__file__).resolve().parents[2]

def need(ok,message):
    if not ok:raise RuntimeError(message)


def run():
    target,w=evidence_case();source,q,sw=expand(target,w)
    c=produce(source,target,q,sw);integrated=receive(source,target,c)
    retained=json.loads((ROOT/'verification/history_reduction/example_transfer.json').read_text())
    need(retained=={'source':source,'target':target,'warrant':c},'retained transfer mismatch')
    need((integrated['source_nodes'],integrated['target_nodes'],integrated['source_queries'],integrated['target_queries'],integrated['max_gain'])==(127,63,160,80,'0'),'integrated expectations')
    positives=['integrated public copy erasure']
    rejected=[]
    def reject(name,fn,code=None):
        try:fn()
        except Invalid as e:
            if code is not None:need(getattr(e,'code',None)==code,name+': unexpected '+str(e))
            rejected.append(name)
        else:raise RuntimeError('accepted '+name)
    # The same map must preserve actual profitable deviations, not award equilibrium.
    for name,kwargs,epsilon,gain in [('weak bond',{'bond':5},'0','1/2'),('participation fee',{'fee':rational('3/2')},'0','1/10'),('positive tolerance',{},'1','0')]:
        t,tw=evidence_case(**kwargs);s,qq,ww=expand(t,tw)
        r=receive(s,t,produce(s,t,qq,ww,epsilon),epsilon)
        need(r['max_gain']==gain,name)
        need(r['equilibrium_status']==('shared-consistent-continuation-bound' if epsilon!='0' else 'shared-consistent-profitable-deviation'),name+' status')
        positives.append(name)
    # A source witness need not use equal coefficients across copies.
    ww=deepcopy(sw)
    for I,row in ww.items():
        if I.startswith('blue/'):
            for term in row.values():term['coefficient']='2'
    unequal=produce(source,target,q,ww);receive(source,target,unequal)
    need(unequal['source_warrant']['t_max']!=unequal['target_warrant']['t_max'],'radius recomputation not exercised')
    qq=deepcopy(q);qq['representative']='blue';receive(source,target,produce(source,target,qq,ww))
    positives+=['unequal source coefficients with recomputed radius','alternate representative']
    # Model-dependent tag probabilities are allowed, but the policy is shared.
    weights={name:({'red':'1/5','blue':'4/5'} if i%2 else {'red':'3/5','blue':'2/5'}) for i,name in enumerate(target['models'])}
    s,qq,ww=expand(target,w,weights);receive(s,target,produce(s,target,qq,ww));positives.append('model-dependent positive tag weights')
    for name,mutation,code in [
        ('unknown representative',lambda x:x.update(representative='missing'),'representative-tag'),
        ('unknown semantics',lambda x:x.update(schema='other'),'reduction-semantics'),
        ('missing tag',lambda x:x['nodes'].pop('blue'),'tag-coverage'),
        ('missing node',lambda x:x['nodes']['red'].pop('red/root'),'node-bijection'),
        ('nonbijective node map',lambda x:x['nodes']['red'].update({'red/root':'disclose.good'}),'node-bijection'),
        ('missing information',lambda x:x['infos']['red'].pop('red/disclose.good'),'information-bijection')]:
        qq=deepcopy(q);mutation(qq);reject(name,lambda:verify_map(source,target,qq),code)
    for name,mutation,code in [
        ('stale source digest',lambda x:x.update(source_sha256='0'*64),'stale-transfer-subject'),
        ('stale target digest',lambda x:x.update(target_sha256='0'*64),'stale-transfer-subject'),
        ('extra warrant field',lambda x:x.update(accepted=True),'transfer-warrant-schema'),
        ('wrong transfer semantics',lambda x:x.update(schema='other'),'transfer-semantics'),
        ('false inner radius',lambda x:x['target_warrant'].update(t_max='1'),'false-positivity-radius'),
        ('missing continuation query',lambda x:x['target_warrant']['incentives']['rows'].pop(),None),
        ('false incentive gain',lambda x:x['target_warrant']['incentives']['rows'][0].update(gain='1'),None)]:
        cc=deepcopy(c);mutation(cc);reject(name,lambda:receive(source,target,cc),code)
    reject('tolerance rebinding',lambda:receive(source,target,c,'1'))
    cc=deepcopy(c)
    other=deepcopy(w)
    for row in other.values():
        for term in row.values():term['coefficient']='2'
    cc['target_warrant']=consistency_produce(target,other)
    reject('individually valid but untransported witness',lambda:receive(source,target,cc),'wrong-witness-restriction')
    s=deepcopy(source)
    for m in s['models'].values():m['beliefs']['blue/receive.N.bond']={'blue/receive.good.N.bond':'1/2','blue/receive.bad.N.bond':'1/2'}
    reject('changed off-path assessment',lambda:verify_map(s,target,q),'assessment-not-invariant')
    # Tampering with supplied game premises must fail even with fresh identities.
    first=next(iter(source['models']))
    s=deepcopy(source);s['models'][first]['payoffs']['red/caught.good.N.bond']['A']='101'
    reject('changed terminal utility',lambda:verify_map(s,target,q),'payoff-mismatch')
    s=deepcopy(source);s['models'][first]['chance']['public-tag']={'red':'0','blue':'1'}
    reject('zero probability representative',lambda:verify_map(s,target,q),'unsupported-zero-tag')
    s=deepcopy(source);s['models']['hidden']=s['models'].pop(first)
    reject('changed model identity',lambda:verify_map(s,target,q),'model-identity')
    # Payoff-irrelevant public randomization can create correlation.
    s,t,qq,ww=matching()
    sc=consistency_produce(s,ww);tc=consistency_produce(t,unit_witness(t))
    sr=consistent_receive(s,sc);tr=consistent_receive(t,tc)
    sv=paths(s,s['models']['m'],s['root'],'A',{});tv=paths(t,t['models']['m'],t['root'],'A',{})
    need(sr['max_gain']==tr['max_gain']=='0' and sv==1 and tv==rational('1/2'),'correlation counterexample')
    reject('payoff irrelevant tag used for coordination',lambda:verify_map(s,t,qq),'profile-not-invariant')
    correlation={'tagged_matching_probability':str(sv),'marginal_product_matching_probability':str(tv),'both_max_gain':'0'}
    # Equal root utilities and zero gain do not preserve off-path likelihoods.
    s,t,qq,ww=likelihood()
    sc=consistency_produce(s,ww);tc=consistency_produce(t,unit_witness(t))
    sr=consistent_receive(s,sc);tr=consistent_receive(t,tc)
    need(sr['max_gain']==tr['max_gain']=='0','likelihood incentives')
    need(paths(s,s['models']['half'],s['root'],'A',{})==paths(t,t['models']['half'],t['root'],'A',{})==1,'likelihood root value')
    reject('changed conditional chance despite equal marginal',lambda:verify_map(s,t,qq),'conditional-chance-mismatch')
    wrong=consistency_produce(t,restrict(ww,qq))
    reject('likelihood-invalid witness restriction',lambda:consistent_receive(t,wrong),'witness-limit-mismatch')
    limit=next(r for r in wrong['belief_rows'] if r['info']=='entry')['beliefs']['entry.g']
    need(limit=='1/4','likelihood exact mismatch')
    likelihood_result={'source_and_target_max_gain':'0','source_and_target_root_A':'1','target_assessed_g':'1/2','incorrectly_restricted_witness_g':limit}
    # The receiving deployment excludes all three candidate producers.
    with tempfile.TemporaryDirectory() as folder:
        base=Path(folder)
        for path in ['history_reduction/transfer_receiver.py','history_reduction/reduction.py','sequential_consistency/consistency_receiver.py','sequential_consistency/witness.py','sequential_credibility/receiver.py','sequential_credibility/subject.py']:
            dest=base/'verification'/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/'verification'/path,dest)
        for name,obj in retained.items(): (base/(name+'.json')).write_text(json.dumps(obj))
        out=subprocess.check_output([sys.executable,str(base/'verification/history_reduction/transfer_receiver.py'),str(base/'source.json'),str(base/'target.json'),str(base/'warrant.json')],text=True)
        need(json.loads(out)==integrated,'producer-disabled receiving mismatch')
    return {'integrated':integrated,'positive_cases':positives,'rejections':rejected,'correlation_counterexample':correlation,'likelihood_counterexample':likelihood_result,'all_three_producers_disabled':True}

if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
