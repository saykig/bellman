"""Fixed certificate construction/consumption checks; outputs only on explicit request."""
import argparse
from dataclasses import replace
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import platform
import sys
import joint_law as j

OBS=[]
CERTS={}

def require(ok, message):
    if not ok: raise RuntimeError(message)

def record(name, **values):
    OBS.append({'case':name,'status':'PASS',**values})

def rejects(f):
    try: f()
    except j.Invalid as e: return str(e)
    raise RuntimeError('invalid certificate or input was accepted')

def profile(lo=F(1,4),hi=F(2,5),penalty=F(1)):
    m=j.make_model(('theta','signal'),(('0','not-e'),('0','e'),('1','not-e'),('1','e')),
      [[1,1,1,1],[-1,4,0,0],[0,0,-4,1]],[1,0,0],[[0,0,-1,-1],[0,0,1,1]],[-lo,hi],
      premises=('static prior family','supplied fixed channel','terminal prediction after e'))
    return j.make_task(m,[0,1,0,1],[0,0,0,1],query_label='P(theta=1|e)',unit='zero-one loss',
                      actions=(('a0',[0,0,1,1]),('a1',[penalty,penalty,0,0])))

def optimum(task):
    result=j.propose(task)
    require(result['status']=='certificate','no matching certificate for fixed case')
    cert=result['certificate']
    accepted=j.consume(task,cert)
    require(accepted['status'] in ('original_optimum','outer_optimum_only'),'wrong optimum status')
    return cert,accepted

def snapshot(cert):
    return j.wire(cert)

def main():
    task=profile(); upper,u=optimum(task); lower,l=optimum(replace(task,direction='min'))
    require((l['value'],u['value'])==(F(4,7),F(8,11)),'conditional extrema')
    expected_points={j.vector([F(12,7),F(3,7),F(1,7),F(4,7),F(20,7)]),
                     j.vector([F(12,11),F(3,11),F(2,11),F(8,11),F(25,11)])}
    require({lower.point,upper.point}==expected_points,'transformed extremizers')
    for c in (lower,upper):
        recovered=j.recover(c.subject,c.point)
        require(j.forward(c.subject,recovered)==c.point,'inverse round trip')
    CERTS['posterior_upper']=snapshot(upper); CERTS['posterior_lower']=snapshot(lower)
    record('integrated_primal_dual_extrema',lower=l['value'],upper=u['value'],original_extremizers=[l['original_point'],u['original_point']])

    # Verify reviewer-supplied duals directly; no imported reviewer solver.
    supplied_up=j.Certificate('optimum',task,upper.point,j.vector(['-8/55','-8/55','3/55','8/11']),j.vector([0,'4/11']),F(8,11))
    supplied_lo=j.Certificate('optimum',lower.subject,lower.point,j.vector(['4/35','4/35','-3/35','-4/7']),j.vector(['16/35',0]),F(-4,7))
    require(j.consume(task,supplied_up)['value']==F(8,11) and j.consume(lower.subject,supplied_lo)['value']==F(4,7),'reviewer duals')
    record('reviewer_literal_dual_witnesses',checked=True)

    # A feasible value is not an optimum; a loose dual remains a valid bound.
    interior_p=F(1,3)
    x=j.vector([F(4,5)*(1-interior_p),F(1,5)*(1-interior_p),F(1,5)*interior_p,F(4,5)*interior_p])
    interior=j.forward(task,x)
    attained=j.consume(task,j.Certificate('witness',task,point=interior))
    loose=j.Certificate('upper',task,y=j.vector([0,0,0,1]),z=j.vector([0,0]),signed_bound=F(1))
    bound=j.consume(task,loose)
    require(attained['value']==F(2,3) and bound['status']=='bound_only_nonemptiness_unestablished','bound distinction')
    gap=rejects(lambda:j.consume(task,replace(loose,kind='optimum',point=interior)))
    record('attainment_bound_optimum_distinctions',attained=attained['value'],loose_upper=bound['value'],false_optimum_rejected=gap)

    comp=j.difference(task,'a1','a0'); c,cr=optimum(comp)
    chosen=j.decide(task,'a1',l['original_point'],{'a0':c})
    require(cr['value']==F(-1,7) and chosen['complete_minimizing_set']==['a1'],'strict action')
    literal_strict=j.Certificate('optimum',comp,c.point,j.vector(['8/35','8/35','-6/35','-1/7']),j.vector(['32/35',0]),F(-1,7))
    require(j.consume(comp,literal_strict)['value']==F(-1,7),'literal strict dual')
    CERTS['strict_action']=snapshot(c)
    record('strict_common_action',**chosen)

    changed=profile(penalty=F(2)); d=j.difference(changed,'a1','a0'); dc,dr=optimum(d)
    _,dl=optimum(replace(d,direction='min'))
    require((dl['value'],dr['value'])==(F(-2,11),F(2,7)),'changed losses')
    stale=rejects(lambda:j.consume(d,c))
    rejects(lambda:j.decide(changed,'a1',l['original_point'],{'a0':dc}))
    record('changed_loss_and_stale_subject',difference_range=[dl['value'],dr['value']],old_certificate=stale)

    tie=profile(lo=F(1,5)); tiec,tc=optimum(j.difference(tie,'a1','a0'))
    _,tie_low=optimum(replace(tie,direction='min'))
    tie_result=j.decide(tie,'a1',tie_low['original_point'],{'a0':tiec})
    require(tc['value']==0 and not tie_result['uniformly_strict_against_other_actions'] and tie_result['complete_minimizing_set'] is None,'tie distinction')
    require(tie_low['value']==F(1,2),'attained tie posterior')
    record('tie_common_without_uniform_strictness',**tie_result,tie_posterior=tie_low['value'])

    # Constant tied pair across the entire original integrated family.
    tied=replace(task,actions=(('a0',j.vector([0,0,0,0])),('a1',j.vector([0,0,0,0])),('a2',j.vector([1,1,1,1]))))
    keys=[('a0','a1'),('a1','a0'),('a0','a2')]
    pair={key:optimum(j.difference(tied,*key))[0] for key in keys}
    complete=j.fixed_minimizing_set(tied,['a0','a1'],l['original_point'],pair)
    require(complete['complete_minimizing_set']==['a0','a1'],'complete tied set')
    record('complete_minimizing_set',**complete)

    mutations={
      'wrong_bound':replace(upper,signed_bound=upper.signed_bound-F(1,100)),
      'negative_multiplier':replace(upper,z=tuple(-z for z in upper.z)),
      'wrong_primal':replace(upper,point=interior),
    }
    refused={name:rejects(lambda cc=cc:j.consume(task,cc)) for name,cc in mutations.items()}
    permuted=replace(task,model=replace(task.model,atom_order=tuple(reversed(task.model.atom_order))))
    refused['atom_order']=rejects(lambda:j.consume(permuted,upper))
    refused['premise_change']=rejects(lambda:j.consume(replace(task,model=replace(task.model,premises=('different regime',))),upper))
    forged=replace(task,numerator=tuple(u+e for u,e in zip(task.numerator,task.event)))
    refused['rebound_forged_objective']=rejects(lambda:j.consume(forged,replace(upper,subject=forged)))
    event_changed=j.make_task(task.model,[1,0,1,0],[0,0,1,0],event_label='not-e',query_label='changed event',actions=task.actions)
    refused['event']=rejects(lambda:j.consume(event_changed,upper))
    record('forged_and_wrong_subject_certificates',rejections=refused)

    # Demonstrate the consumer has no solver dependency.
    saved=j.propose
    def disabled(*a,**k): raise RuntimeError('producer disabled')
    j.propose=disabled
    try:
        require(j.consume(task,upper)['value']==F(8,11),'independent consumption')
        j.decide(task,'a1',l['original_point'],{'a0':c})
    finally: j.propose=saved
    record('consumer_without_producer',accepted_checked_certificates=True)

    omega=list(product(('0','1'),repeat=3))
    A=[[1]*8]+[[int(w[i]!=w[k]) for w in omega] for i,k in ((0,1),(1,2),(0,2))]
    triangle=j.make_model(('X','Y','Z'),omega,A,[1]*4,premises=('three pairwise disagreements almost surely',))
    ttask=j.make_task(triangle,[1]*8,[0]*8,conditional=False,event_label='whole space')
    farkas=j.Certificate('infeasible',ttask,y=j.vector([2,-1,-1,-1]),signed_bound=F(-1))
    require(j.consume(ttask,farkas)['status']=='original_infeasible','triangle Farkas')
    rejects(lambda:j.consume(ttask,replace(farkas,y=tuple(-v for v in farkas.y),signed_bound=F(1))))
    nosearch=j.propose(ttask,max_bases=0)
    require(nosearch['status']=='unfinished','empty search is no contradiction certificate')
    CERTS['triangle_infeasible']=snapshot(farkas)
    record('triangle_and_unfinished_search',farkas_value=-1,search=nosearch)

    impossible=j.make_model(('state',),(('0',),('1',)),[[1,1],[0,1]],[1,0])
    etask=j.make_task(impossible,[0,1],[0,1])
    ec=j.Certificate('infeasible',etask,y=j.vector([0,1,-1]),signed_bound=F(-1))
    require(j.original_member(impossible,j.vector([1,0])),'original nonempty')
    require(j.consume(etask,ec)['status']=='no_eligible_original_model','impossible support')
    rejects(lambda:j.forward(etask,j.vector([1,0])))
    require(j.impossible_event(etask,j.vector([1,0]),ec)['status']=='impossible_conditioning','impossible event conclusion')
    record('impossible_event_in_nonempty_original_family',witness=[1,0],conditional_farkas=-1,posterior=None)

    # Gluing uses the review's literal marginals, then checks all original rows.
    xy=[[F(3,8),F(1,8)],[F(1,8),F(3,8)]]
    yz=[[F(1,3),F(1,6)],[F(1,6),F(1,3)]]
    rows=[[F(1)]*8]; rhs=[F(1)]
    for axes,table in [((0,1),xy),((1,2),yz)]:
        for a,b in product(range(2),repeat=2):
            rows.append([F(w[axes[0]]==str(a) and w[axes[1]]==str(b)) for w in omega]); rhs.append(table[a][b])
    gm=j.make_model(('X','Y','Z'),omega,rows,rhs)
    glue=j.vector([xy[int(x)][int(y)]*yz[int(y)][int(z)]/F(1,2) for x,y,z in omega])
    require(j.original_member(gm,glue),'glued original witness')
    record('compatible_join',joint=glue)
    # A zero separator cell is assigned joint mass zero, never divided by zero.
    degenerate=j.vector([F(1,4) if y=='0' else F(0) for x,y,z in omega])
    require(sum(degenerate)==1,'zero separator glue')
    for x,y in product(('0','1'),repeat=2):
        require(sum(m for atom,m in zip(omega,degenerate) if atom[:2]==(x,y))==(F(1,2) if y=='0' else F(0)),'zero separator marginal')
    record('zero_separator_glue',joint=degenerate,zero_separator_mass=0)

    poly=j.Polynomial('X independent Y',((F(1),(1,0,0,1)),(F(-1),(0,1,1,0))))
    om=j.make_model(('X','Y'),list(product(('0','1'),repeat=2)),[[1]*4,[1,1,0,0],[1,0,1,0]],[1,F(1,2),F(1,2)],extra=(poly,))
    outer=j.make_task(om,[1]*4,[1,0,0,0],conditional=False,event_label='whole space')
    oc,orr=optimum(outer); uniform=j.vector([F(1,4)]*4)
    require(orr['status']=='outer_optimum_only' and orr['value']==F(1,2) and j.original_member(om,uniform),'outer distinction')
    rejects(lambda:j.forward(outer,orr['original_point']))
    loose_result=j.consume(outer,replace(oc,kind='upper',point=()))
    require(loose_result['status']=='bound_only_nonemptiness_unestablished','outer bound status')
    # A matching original witness can make an outer bound exact for the original query.
    marginal=replace(outer,numerator=j.vector([1,1,0,0]))
    mc,_=optimum(marginal)
    matched=j.consume(marginal,replace(mc,point=uniform))
    require(matched['status']=='original_optimum' and matched['value']==F(1,2),'matching original witness')
    record('missing_independence_and_outer_certificate',outer_p00=orr['value'],original_uniform_p00=uniform[0],matched_original_marginal=matched['value'])

    # Exact extrema need not fill their interval when original constraints disconnect it.
    disconnected=j.make_model(('state',),(('0',),('1',)),[[1,1]],[1],
        extra=(j.Polynomial('endpoint support only',((F(1),(1,1)),)),))
    disq=j.make_task(disconnected,[1,1],[1,0],conditional=False,event_label='whole space')
    _,dislo=optimum(replace(disq,direction='min')); _,dishi=optimum(disq)
    require(dislo['status']==dishi['status']=='original_optimum' and (dislo['value'],dishi['value'])==(0,1),'disconnected extrema')
    require(not j.original_member(disconnected,j.vector(['1/2','1/2'])),'interior unattainability')
    record('exact_extrema_not_full_attainable_interval',minimum=0,maximum=1,attainable_values=[0,1],half_attainable=False)

    # Prior endpoint explanations may be alternatives; simultaneous equality is inconsistent.
    base=task.model
    extra_rows=(j.vector([0,0,1,1]),)*2
    intersection=replace(base,A=base.A+extra_rows,b=base.b+(F(1,4),F(2,5)),C=(),d=())
    it=j.make_task(intersection,[1]*4,[0]*4,conditional=False,event_label='whole space')
    ic=j.Certificate('infeasible',it,y=j.vector([0,0,0,1,-1]),signed_bound=F(-3,20))
    j.consume(it,ic)
    require(j.original_member(task.model,l['original_point']) and j.original_member(task.model,u['original_point']),'alternative endpoint witnesses')
    record('alternatives_vs_asserted_intersection',alternative_answers=[l['value'],u['value']],intersection_farkas=F(-3,20))

    # Independent set-form TV proof evaluated on the review's fixed examples.
    examples=[(j.vector(['1/10','3/20',0,'3/4']),j.vector([0,'3/20','1/10','3/4']),3),
              (j.vector(['1/10','1/10','4/5']),j.vector(['1/5','1/10','7/10']),2),
              (j.vector(['1/100',0,'99/100']),j.vector([0,'1/100','99/100']),2)]
    tv=lambda x,y:sum(abs(a-b) for a,b in zip(x,y))/2
    proofs=[]
    for P,Q,k in examples:
        a,b=sum(P[:k]),sum(Q[:k])
        if a>b: P,Q,a,b=Q,P,b,a
        delta=tv(P,Q); cond=tv([v/a for v in P[:k]],[v/b for v in Q[:k]])
        indices=[i for i in range(k) if Q[i]/b>P[i]/a]
        numerator=sum((Q[i]-F(b,a)*P[i] for i in indices),F(0))
        difference=sum((Q[i]-P[i] for i in indices),F(0))
        overlap=sum(min(P[i]/a,Q[i]/b) for i in range(k))
        require(b*cond==numerator and numerator<=difference<=delta and cond==1-overlap,'independent TV proof chain')
        proofs.append({'event_masses':[a,b],'joint_TV':delta,'conditional_TV':cond,'new_bound':min(1,delta/b)})
    require(proofs[0]['new_bound']==proofs[0]['conditional_TV']==F(2,5),'sharp example')
    record('conditioning_overlap_and_independent_event_proof',examples=proofs)

    bad_numbers=[rejects(lambda:j.rational(x)) for x in (0.1,True,'0.1','1/0')]
    record('exact_numeric_profile',rejections=bad_numbers)
    require(F(179,200)-F(1,2)<=F(2,5) and F(179,200)-F(1,2)>F(39,100),'inward enclosure failure')
    record('symbolic_radius_vs_computed_enclosure',inside_exact_radius=True,outside_inward_radius=True,log_sqrt_evaluator_implemented=False)

    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); args=ap.parse_args()
    payload={'python':platform.python_version(),'optimized':sys.flags.optimize,'passed_cases':len(OBS),
             'scope':'fixed finite rational certificate examples; not formal verification or a general solver',
             'source_sha256':{name:sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ('joint_law.py','module_checks.py')},
             'results':j.wire(OBS),'certificates':CERTS}
    args.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'python':payload['python'],'optimized':payload['optimized'],'passed_cases':len(OBS)}))

if __name__=='__main__': main()
