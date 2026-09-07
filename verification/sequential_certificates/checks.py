"""Fixed sequential certificate examples; no search grid or external dependencies."""
from fractions import Fraction as F
from dataclasses import replace
from itertools import product
from pathlib import Path
import hashlib, json, platform, sys
import reference as r

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def rejects(call):
    try:
        call()
    except r.Invalid:
        return
    raise RuntimeError("expected invalid mathematical claim was accepted")

def fixture():
    left=(("go","L"),); right=(("go","R"),)
    s=r.Subject("two decision dates",2,"loss",("known model","full observed history"),[
        r.Node((),actions=[r.Action("stop",F(3,4)),r.Action("go",F(1,8),[("L",F(1,2)),("R",F(1,2))])]),
        r.Node(left,actions=[r.Action("a",0),r.Action("b",F(1,2))]),
        r.Node(right,actions=[r.Action("a",1),r.Action("b",F(1,4))])])
    bad=r.Policy([((),"go"),(left,"b"),(right,"a")])
    return s,bad

def main():
    results=[]
    def record(name,**data):
        results.append(dict(case=name,status="PASS",**data))
    s,bad=fixture()
    cert=r.produce(s,bad); good=r.produce(s)
    answer=r.consume(s,bad,cert)
    require(answer==dict(optimum_lower=F(1,4),policy_upper=F(7,8),regret_upper=F(5,8)),"positive package")
    policies=r.enumerate_policies(s)
    totals=[r.path_cost(s,p) for p in policies]
    require(len(policies)==8 and min(totals)==F(1,4) and r.path_cost(s,bad)==F(7,8),"independent full paths/policy enumeration")
    record("complete_nonzero_regret_and_independent_paths",**answer,legal_policies=8,paths=r.paths(s,bad))

    # Lower bounds must check competitors, not just the chosen action.
    forged=replace(cert,lower=cert.upper)
    rejects(lambda:r.consume(s,bad,forged))
    r.consume(s,bad,cert)
    record("selected_action_only_is_not_optimum_lower_bound")

    zeros=(F(0),)*3
    rc=r.residual_certificate(s,bad,good.lower,zeros,(F(0),F(1,2),F(3,4)))
    require(r.consume(s,bad,rc)["regret_upper"]==F(5,8),"greediness allowance propagation")
    rejects(lambda:r.residual_certificate(s,bad,good.lower,zeros,zeros))
    # Residuals for one value table cannot authorize another table.
    shifted=(F(3,8),F(0),F(1,4))
    rejects(lambda:r.residual_certificate(s,good.policy,shifted,zeros,zeros))
    r.residual_certificate(s,good.policy,shifted,(F(1,8),F(0),F(0)),zeros)
    record("actual_residual_and_same_backup_policy_checks",checked_greediness_regret=F(5,8))

    stop=r.Policy([((),"stop"),(s.nodes[1].h,"a"),(s.nodes[2].h,"b")])
    greedy=r.residual_certificate(s,stop,(F(3,4),F(1),F(1)),(F(0),F(1),F(3,4)),zeros)
    require(r.path_cost(s,stop)-good.lower[0]==F(1,2),"nonzero approximate-greedy regret")
    require(r.consume(s,stop,greedy)["regret_upper"]==F(7,8),"nonuniform residual bound")
    record("nonzero_approximate_greedy_regret",actual=F(1,2),certified=F(7,8))

    terminal=r.Subject("terminal residual",1,"loss",(),[
        r.Node((),actions=[r.Action("go",0,[("done",1)])]),
        r.Node((("go","done"),),terminal=1)])
    tc=r.produce(terminal)
    rejects(lambda:r.residual_certificate(terminal,tc.policy,(F(1),F(3,2)),(F(1,2),F(0)),(F(0),F(0))))
    r.residual_certificate(terminal,tc.policy,(F(1),F(3,2)),(F(1,2),F(1,2)),(F(0),F(0)))
    record("terminal_residual_is_load_bearing")

    changed_cost=replace(s,nodes=(replace(s.nodes[0],actions=(r.Action("stop",0),s.nodes[0].actions[1])),)+s.nodes[1:])
    changed_horizon=replace(s,horizon=3)
    for other in (changed_cost,changed_horizon):
        rejects(lambda:r.consume(other,bad,cert))
        r.consume(other,bad,r.produce(other,bad))
    inaccessible=r.Policy([((),"go"),((("hidden","state0"),),"a"),(s.nodes[2].h,"a")])
    rejects(lambda:r.consume(s,inaccessible,cert))
    r.consume(s,bad,cert)
    rejects(lambda:r.consume(s,bad,good))
    r.consume(s,bad,cert)
    record("stale_cost_horizon_inaccessible_and_changed_continuation",valid_controls=True)

    require(r.telescoping(s,bad,good.lower)==F(5,8),"actual-trajectory telescoping")
    wrong_values=(F(7,8),F(1,2),F(1))
    rejects(lambda:r.telescoping(s,bad,wrong_values))
    # In unrelated continuation tasks, the bad choices can be optimal; their zero
    # local regrets are not Bellman disadvantages in the original subject.
    alternate=replace(s,nodes=(s.nodes[0],
        replace(s.nodes[1],actions=(r.Action("a",1),r.Action("b",0))),
        replace(s.nodes[2],actions=(r.Action("a",0),r.Action("b",1)))))
    alt=r.produce(alternate,bad)
    require(alt.lower[0]==alt.upper[0] and cert.upper[0]>cert.lower[0],"unrelated local regrets fail")
    one_change=r.Policy([((),"go"),(s.nodes[1].h,"b"),(s.nodes[2].h,"b")])
    require(r.path_cost(s,one_change)-r.path_cost(s,good.policy)==F(1,2)*F(1,2),"single replacement visit weighting")
    require(r.telescoping(s,one_change,good.lower)==F(1,4),"single replacement comparator")
    record("replanning_common_comparator_not_unrelated_local_optima",actual_regret=F(5,8),unrelated_regret=0,single_replacement_cost=F(1,4))

    # Conditional TV uses a common space/event with positive masses.
    P=(F(1,100),F(0),F(99,100)); Q=(F(0),F(1,100),F(99,100))
    a,b,d,c,e=r.conditioning(P,Q,(1,1,0))
    require((d,c,e)==(F(1,100),F(1),F(1)),"rare-event amplification")
    P2=(F(1,10),F(1,10),F(4,5));Q2=(F(1,5),F(1,10),F(7,10))
    require(r.conditioning(P2,Q2,(1,1,0))[3:]==(F(1,6),F(1,3)),"unequal masses")
    rejects(lambda:r.conditioning(P,Q,(0,0,0)))
    r.conditioning(P,Q,(1,1,1))
    record("rare_event_and_unequal_mass_conditioning",joint_TV=d,conditional_TV=c,rare_expected_loss=F(1,100),rare_conditional_loss=1)

    def with_probability(prob,name):
        go=r.Action("go",F(1,8),[("L",1-prob),("R",prob)])
        return replace(s,name=name,nodes=(replace(s.nodes[0],actions=(s.nodes[0].actions[0],go)),)+s.nodes[1:])
    nominal=with_probability(F(0),"surrogate"); actual=with_probability(F(1,100),"actual")
    fallback=r.Policy([((),"go"),(s.nodes[1].h,"a"),(s.nodes[2].h,"a")])
    missing=r.Policy(fallback.choices[:-1])
    rejects(lambda:r.produce(nominal,missing))
    nc,ac=r.produce(nominal,fallback),r.produce(actual,fallback)
    require(nc.upper[0]==F(1,8) and ac.upper[0]==F(27,200) and ac.upper[0]-ac.lower[0]==F(3,400),"off-support loss")
    rejects(lambda:r.conditioning((F(99,100),F(1,100)),(F(1),F(0)),(0,1)))
    r.consume(actual,fallback,ac)
    record("off_support_total_fallback_no_invented_posterior",surrogate_cost=nc.upper[0],actual_cost=ac.upper[0],actual_regret=F(3,400),fallback_loss_contribution=F(1,100))

    tie=r.Subject("tie",1,"loss",(),[r.Node((),actions=[r.Action("a",-1),r.Action("b",-1)])])
    tied=r.produce(tie)
    require(r.root_actions(tie,tied.policy,tied)["minimizers"]==["a","b"],"preserve ties")
    loose=replace(tied,lower=(F(-2),),upper=(F(0),))
    # Immediate stopping action values remain exact; use a continuation for uncertain sign.
    uncertain=r.root_actions(s,bad,cert)
    require(uncertain["status"]=="uncertified","root overlap not tie")
    require(r.root_actions(s,good.policy,good)["minimizers"]==["go"],"strict root action")
    zero=r.Subject("zero remaining horizon",0,"loss",(),[r.Node((),terminal=-2)])
    zc=r.produce(zero)
    require(r.root_actions(zero,zc.policy,zc)["status"]=="terminal","zero horizon not strict")
    rejects(lambda:replace(zero,nodes=(r.Node((),actions=[r.Action("a",0)]),)))
    r.consume(zero,zc.policy,zc)
    record("root_action_whole_policy_tie_overlap_zero_horizon",exact_tie=["a","b"],overlap="uncertified",zero_horizon="terminal")

    # Uniform transfer from SAME available policy class, evaluated memberwise.
    nominal_cost=[r.path_cost(nominal,p) for p in policies]
    actual_cost=[r.path_cost(actual,p) for p in policies]
    model_error=max(abs(a-b) for a,b in zip(nominal_cost,actual_cost))
    eta=nc.upper[0]-nc.lower[0]
    require(ac.upper[0]-ac.lower[0] <= 2*model_error+eta,"uniform transfer")
    # Equal optimal values alone: action losses (0,1) versus (1,0).
    first=r.Subject("first",1,"loss",(),[r.Node((),actions=[r.Action("a",0),r.Action("b",1)])])
    second=replace(first,name="second",nodes=(r.Node((),actions=[r.Action("a",1),r.Action("b",0)]),))
    fc,sc=r.produce(first),r.produce(second)
    require(fc.lower[0]==sc.lower[0]==0 and r.path_cost(second,fc.policy)==1,"value closeness not regret")
    record("uniform_model_error_plus_calculation_error",uniform_e=model_error,eta=eta,actual_regret=F(3,400),transfer_bound=2*model_error+eta,value_closeness_counterexample_regret=1)

    # Fixed model identity versus independently choosing each date's row.
    def fixed(name,c0,c1):
        return r.Subject(name,2,"loss",(),[r.Node((),actions=[r.Action("tick",c0,[("same",1)])]),
            r.Node((("tick","same"),),actions=[r.Action("end",c1)])])
    A,B,sw=fixed("A",0,1),fixed("B",1,0),fixed("switch",1,1)
    common=r.produce(A).policy
    require(r.path_cost(A,common)==r.path_cost(B,common)==1 and r.path_cost(sw,common)==2,"persistent identity")
    # Oracle model-dependent choice is not one policy: there is no shared zero-cost rule.
    family_policies=r.enumerate_policies(first)
    costs=[(r.path_cost(first,p),r.path_cost(second,p)) for p in family_policies]
    require(costs==[(F(0),F(1)),(F(1),F(0))],"common policy family")
    rejects(lambda:r.Policy([((("model","A"),),"a")]).validate(first))
    family_policies[0].validate(first);family_policies[0].validate(second)
    record("persistent_models_and_recipient_policy_access",fixed_worst=1,switching=2,modelwise_costs=costs,oracle_zero_not_common=True)

    # B13's independent-observation premise cannot be inferred from one-date marginals.
    independent=(F(1,4),)*4
    biased=(F(9,16),F(3,16),F(3,16),F(1,16))
    row_d=F(1,4); product_bound=1-(1-row_d)**2
    tv=sum(abs(a-b) for a,b in zip(independent,biased))/2
    require(tv==F(5,16) and tv<=product_bound==F(7,16),"valid independent product control")
    correlated=(F(1,2),F(0),F(0),F(1,2))
    anticorrelated=(F(0),F(1,2),F(1,2),F(0))
    require(sum(correlated[i] for i in (0,1))==sum(anticorrelated[i] for i in (0,1))==F(1,2),"equal first marginal")
    require(correlated[0]+correlated[2]==anticorrelated[0]+anticorrelated[2]==F(1,2),"equal second marginal")
    require(correlated[0]+correlated[3]-(anticorrelated[0]+anticorrelated[3])==1,"dependence counterexample")
    record("independent_product_bound_and_dependence_failure",independent_TV=tv,bound=product_bound,marginal_only_claim=0,dependent_policy_loss_difference=1)

    # Explicit hidden joint: posterior and history-dependent next prediction.
    joint={(0,0,0):F(1,4),(0,1,1):F(1,4),(1,0,0):F(1,4),(1,1,1):F(1,4)}
    mass=sum(p for (theta,x,y),p in joint.items() if x==0)
    posterior=sum(p for (theta,x,y),p in joint.items() if x==0 and theta==1)/mass
    prediction=sum(p for (theta,x,y),p in joint.items() if x==0 and y==0)/mass
    require(posterior==F(1,2) and prediction==1,"retain history for dependent observations")
    # Selecting a later action based on X must not replace its chronological likelihood.
    controlled={(0,0):F(3,8),(0,1):F(1,8),(1,0):F(1,8),(1,1):F(3,8)}
    selected_mass=controlled[0,0]+controlled[1,0]
    true_posterior=controlled[1,0]/selected_mass
    selected_likelihoods=(controlled[0,0]/controlled[0,0],controlled[1,0]/controlled[1,0])
    naive=selected_likelihoods[1]/sum(selected_likelihoods)
    chronological=F(1,4)/(F(3,4)+F(1,4))
    require(true_posterior==chronological==F(1,4) and naive==F(1,2),"adaptive selection likelihood control")
    record("hidden_state_conditioning_retains_predictive_history",posterior=posterior,next_zero_given_first_zero=prediction,adaptive_correct_posterior=true_posterior,selected_action_naive_posterior=naive)

    for x in (0.5,True):
        rejects(lambda:r.Action("a",x))
        rejects(lambda:replace(cert,lower=(x,)+cert.lower[1:]))
        rejects(lambda:r.residual_certificate(s,bad,good.lower,(x,F(0),F(0)),zeros))
    huge=F(2**500)
    large=replace(cert,lower=tuple(x-huge for x in cert.lower),upper=tuple(x+huge for x in cert.upper))
    r.consume(s,bad,large)
    rejects(lambda:replace(s,horizon=True))
    r.consume(s,bad,cert)
    record("exact_numbers_and_large_derived_proofs",derived_bits=501)

    outcomes=[["L",F(1,2)],["R",F(1,2)]]
    actions=[r.Action("stop",F(3,4)),r.Action("go",F(1,8),outcomes)]
    nodes=[r.Node([],actions=actions),s.nodes[1],s.nodes[2]];premises=["known"]
    mutable=r.Subject("immutable",2,"loss",premises,nodes)
    choices=[[[], "go"],[[["go","L"]],"b"],[[["go","R"]],"a"]]
    pi=r.Policy(choices);mc=r.produce(mutable,pi);before=r.consume(mutable,pi,mc)
    outcomes.clear();actions.clear();nodes.clear();premises[0]="changed";choices[1][0][0][1]="hidden"
    require(r.consume(mutable,pi,mc)==before,"caller aliases changed subject")
    rejects(lambda:r.Policy([((),"go")]).validate(mutable))
    r.consume(mutable,pi,mc)
    record("deep_immutable_subject_policy_and_complete_coverage")

    saved=r.produce
    def disabled(*args,**kwargs):
        raise RuntimeError("producer disabled")
    r.produce=disabled
    r.consume(s,bad,cert)
    r.residual_certificate(s,bad,good.lower,zeros,(F(0),F(1,2),F(3,4)))
    require(r.path_cost(s,bad)==F(7,8),"independent path evaluator")
    r.produce=saved
    record("consumer_does_not_call_producer")
    sources={n:hashlib.sha256(Path(__file__).with_name(n).read_bytes()).hexdigest() for n in ("reference.py","checks.py")}
    output={"python":platform.python_version(),"optimized":sys.flags.optimize,"passed":len(results),"failed":0,
            "results":r.wire(results),"source_sha256":sources}
    print(json.dumps(output,sort_keys=True))

if __name__=="__main__":
    main()
