"""Targeted public-entry regressions for PR4 boundary repairs; no new experiments."""
import argparse
from dataclasses import replace
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import platform
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'joint_law_completion'))
import joint_law as j


def require(ok, why):
    if not ok: raise RuntimeError(why)


def rejects(fn):
    try: fn()
    except j.Invalid: return
    raise RuntimeError('Invalid input produced a mathematical result')


def main():
    results=[]
    def passed(name, **details): results.append(dict(case=name,status='PASS',**details))
    half=F(1,2); eps=F(1,2**60); exact=(half,half); rounded=(0.5,0.5)
    p1=j.Polynomial('p0=half',[(1,[1,0]),(-half,[0,0])])
    p2=j.Polynomial('p0=half+epsilon',[(1,[1,0]),(-half-eps,[0,0])])
    empty=j.make_model(['state'],[['0'],['1']],[[1,1]],[1],extra=[p1,p2])
    t=j.make_task(empty,[1,1],[0,0],conditional=False,actions=[('a0',[0,0]),('a1',[1,1])])
    require(not j.original_member(empty,exact),'exact empty-family control')
    for bad in (rounded,(True,False),(F(1),False),(1,0),('1/2','1/2')):
        rejects(lambda:j.original_member(empty,bad))
        rejects(lambda:p1.holds(bad))
    passed('original_membership_and_polynomial_reject_inexact_witnesses',false_exact_witness=False)

    for conditional in (False,True):
        task=replace(t,conditional=conditional)
        comp=j.difference(task,'a0','a1')
        y=(F(0),F(-1)) if conditional else (F(-1),)
        cert=j.Certificate('upper',comp,y=y,signed_bound=F(-1))
        require(j.consume(comp,cert)['status']=='bound_only_nonemptiness_unestablished','bound is not nonemptiness')
        for bad in (rounded,(True,False),exact):
            rejects(lambda:j.forward(task,bad))
            rejects(lambda:j.decide(task,'a0',bad,{'a1':cert}))
            rejects(lambda:j.fixed_minimizing_set(task,['a0'],bad,{('a0','a1'):cert}))
        passed('empty_original_decision_paths_'+str(conditional),outer_bound=-1,original_nonemptiness_established=False)

    one=j.Polynomial('p0=1',[(1,[1,0]),(-1,[0,0])])
    plus=j.Polynomial('p0=1+epsilon',[(1,[1,0]),(-1-eps,[0,0])])
    im=j.make_model(['state'],[['0'],['1']],[[1,1],[0,1]],[1,0],extra=[one,plus])
    it=j.make_task(im,[0,1],[0,1])
    ic=j.Certificate('infeasible',it,y=(F(0),F(1),F(-1)),signed_bound=F(-1))
    require(j.consume(it,ic)['status']=='no_eligible_original_model','eligible infeasibility only')
    for bad in ((1.0,0.0),(True,False),(F(1),F(0))):
        rejects(lambda:j.impossible_event(it,bad,ic))
    valid_im=replace(im,extra_original=())
    valid_it=replace(it,model=valid_im)
    valid_ic=replace(ic,subject=valid_it)
    require(j.impossible_event(valid_it,(F(1),F(0)),valid_ic)['original_nonempty'],'true impossible-event control')
    passed('impossible_conditioning_requires_true_original_nonemptiness')

    normal=j.make_model(['state'],[['0'],['1']],[[1,1]],[1])
    good=j.make_task(normal,[1,1],[0,0],conditional=False,actions=[('a0',[0,0])])
    malformed=[replace(good,event=(F(0),F(0))),replace(good,numerator=(0.0,F(0))),
               replace(good,actions=(('a0',(False,F(0))),)),replace(good,direction='wrong'),
               replace(good,model=replace(normal,A=((True,F(1)),)))]
    for bad in malformed:
        rejects(lambda:j.forward(bad,exact))
        rejects(lambda:j.decide(bad,'a0',exact,{}))
        rejects(lambda:j.fixed_minimizing_set(bad,['a0'],exact,{}))
        rejects(lambda:j.propose(bad,max_bases=0))
    require(j.decide(good,'a0',exact,{})['complete_minimizing_set']==['a0'],'valid singleton')
    require(j.fixed_minimizing_set(good,['a0'],exact,{})['complete_minimizing_set']==['a0'],'valid singleton full set')
    passed('full_subject_validation_before_single_action_shortcuts',invalid_subjects=len(malformed))

    for fn in (lambda:j.feasible(j.lp(good),rounded),lambda:j.recover(good,rounded),
               lambda:j.solve_rows([[F(1)]],[True],1),lambda:j.dot([F(1)],[True]),
               lambda:j.Certificate('witness',good,point=rounded)):
        rejects(fn)
    forged=replace(good,event=(True,True))
    cert=j.Certificate('upper',forged,y=(F(0),))
    # Fraction(1)==True: subject equality alone is insufficient validation.
    require(forged==good,'equality collision control')
    rejects(lambda:j.consume(good,cert))
    passed('direct_numeric_helpers_and_equal_but_invalid_certificate_subject')

    # Deep-snapshot every public subject constructor, including direct dataclass paths.
    powers=[1,0]; terms=[[F(1),powers],[-half,[0,0]]]
    poly=j.Polynomial('half',terms)
    variables=['state']; atoms=[['0'],['1']]; A=[[F(1),F(1)]]; b=[F(1)]; extra=[poly]; premises=['original']
    model=j.Model(variables,atoms,A,b,[],[],premises,extra)
    event=[F(1),F(1)]; numerator=[F(1),F(0)]; losses=[F(0),F(0)]; actions=[['a0',losses]]
    task=j.Task(model,'whole',event,numerator,False,'x0','loss',actions)
    point=[half,half]; certificate=j.Certificate('witness',task,point=point)
    baseline=j.wire(certificate)
    powers[0]=0;terms[1][0]=-F(1,3);variables[0]='changed';atoms[0][0]='changed'
    A[0][0]=F(7);b[0]=F(8);extra.clear();premises[0]='changed'
    event[0]=F(0);numerator[0]=F(0);losses[0]=F(9);actions[0][0]='changed';point[0]=F(0)
    require(j.wire(certificate)==baseline,'caller mutation altered subject or witness')
    require(j.consume(task,certificate)['status']=='original_attained','stable original membership')
    changed=replace(task,model=replace(model,extra_original=(j.Polynomial('third',[(1,[1,0]),(-F(1,3),[0,0])]),)))
    rejects(lambda:j.consume(changed,certificate))
    passed('deep_subject_and_certificate_snapshot_with_changed_subject_negative_control')

    y=[F(1)]; z=[]; upper=j.Certificate('upper',good,y=y,z=z,signed_bound=F(1))
    y[0]=F(-1);z.append(F(-1))
    require(j.consume(good,upper)['value']==1,'mutated dual vector')
    rows=[[F(1),F(1)]];rhs=[F(1)];obj=[F(0),F(0)]
    L=j.LP(rows,rhs,[],[],obj);rows[0][0]=F(9);rhs[0]=F(2);obj[0]=F(8)
    require(j.feasible(L,exact),'LP alias mutation')
    passed('dual_and_linear_system_container_snapshot')

    tiny=F(1,2**300); large=(tiny,1-tiny)
    task=j.make_task(normal,[1,0],[1,0],actions=[('a0',[0,0])])
    transformed=j.forward(task,large)
    require(transformed[-1]==2**300,'derived inverse magnitude')
    require(j.recover(task,transformed)==large,'large exact inverse roundtrip')
    require(j.consume(task,j.Certificate('witness',task,point=transformed))['status']=='original_attained','large derived witness')
    require(j.decide(task,'a0',large,{})['complete_minimizing_set']==['a0'],'large witness singleton')
    rejects(lambda:j.rational(tiny))
    passed('derived_witness_not_subject_to_input_coefficient_bit_limit',inverse_scale_bits=301)

    # Governing prompt's distinct linear rounding failure and exact Farkas control.
    N=2**54+1
    linear=j.make_model(('s',),(('0',),('1',)),[[1,1],[N,N]],[1,N-1])
    lt=j.make_task(linear,[1,1],[0,0],conditional=False,actions=(('a0',[0,0]),('a1',[1,1])))
    lf=j.Certificate('infeasible',lt,y=(F(-N),F(1)),signed_bound=F(-1))
    require(j.consume(lt,lf)['status']=='original_infeasible','linear exact Farkas')
    require(not j.original_member(linear,exact),'linear rational witness is false')
    for conditional in (False,True):
        subject=replace(lt,conditional=conditional)
        comp=j.difference(subject,'a0','a1')
        yy=(F(0),F(0),F(-1)) if conditional else (F(-1),F(0))
        bound=j.Certificate('upper',comp,y=yy,signed_bound=F(-1))
        for bad in (rounded,(True,False),exact):
            if bad is not exact:
                rejects(lambda:j.original_member(linear,bad))
            rejects(lambda:j.forward(subject,bad))
            rejects(lambda:j.decide(subject,'a0',bad,{'a1':bound}))
            rejects(lambda:j.fixed_minimizing_set(subject,['a0'],bad,{('a0','a1'):bound}))
    impossible=j.make_task(linear,[0,0],[0,0])
    fi=j.Certificate('infeasible',impossible,y=(F(0),F(0),F(-1)),signed_bound=F(-1))
    for bad in (rounded,(True,False),exact):
        rejects(lambda:j.impossible_event(impossible,bad,fi))
    passed('prompt_linear_contradiction_all_original_witness_routes',farkas_bound=-1)

    terms=[(F(1),[1,0]),(-F(1,3),[0,0])]
    poly=j.Polynomial('third',terms)
    model=j.make_model(('s',),(('0',),('1',)),[[1,1]],[1],extra=[poly])
    subject=j.make_task(model,[1,1],[1,0],conditional=False)
    cert=j.Certificate('witness',subject,point=exact)
    require(j.consume(subject,cert)['status']=='outer_attained_only','initial outer witness')
    terms.clear()
    require(j.consume(subject,cert)['status']=='outer_attained_only','clear promoted original membership')
    new=replace(subject,model=replace(model,extra_original=()))
    rejects(lambda:j.consume(new,cert))
    require(j.consume(new,replace(cert,subject=new))['status']=='original_attained','explicit revised subject')
    passed('prompt_cleared_term_list_cannot_promote_original_membership')

    huge=2**500
    task=j.make_task(normal,[0,1],[0,1])
    point=(F(huge-1),F(1),F(huge))
    require(j.consume(task,j.Certificate('witness',task,point=point))['status']=='original_attained','500-bit derived point')
    require(j.forward(task,j.recover(task,point))==point,'500-bit exact inverse')
    passed('prompt_500_bit_transformed_point_positive_control',scale_bits=501)

    j.propose=lambda *a,**k:(_ for _ in ()).throw(RuntimeError('producer disabled'))
    j.solve_rows=j.propose
    require(j.decide(good,'a0',exact,{})['complete_minimizing_set']==['a0'],'consumer separation')
    passed('valid_exact_consumer_without_producer')
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    payload={'python':platform.python_version(),'optimized':sys.flags.optimize,'passed_cases':len(results),'results':results,
        'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(j.__file__),Path(__file__))}}
    args.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:payload[k] for k in ('python','optimized','passed_cases')}))

if __name__=='__main__':main()
