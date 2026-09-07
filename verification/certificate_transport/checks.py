"""Fixed exact transport checks. Independent forward oracle; no parameter grid."""
from dataclasses import replace, FrozenInstanceError
from fractions import Fraction as F
from itertools import product
import json, sys, time
import transport as t
r = t.r

def need(ok, why):
    if not ok:
        raise RuntimeError(why)

REJECTIONS = 0
def rejects(fn):
    global REJECTIONS
    try:
        fn()
    except r.Invalid:
        REJECTIONS += 1
        return
    raise RuntimeError("invalid claim accepted")

def oracle(s, pi, start=()):
    """Stack-based paths, without reference backup/evaluation/enumeration."""
    nodes, chosen = {n.h:n for n in s.nodes}, dict(pi.choices)
    stack, total, mass_total = [(start,F(1),F(0))], F(0), F(0)
    while stack:
        h, mass, paid = stack.pop()
        n = nodes[h]
        if not n.actions:
            total += mass*(paid+n.terminal)
            mass_total += mass
            continue
        a = next(a for a in n.actions if a.label==chosen[h])
        if not a.outcomes:
            total += mass*(paid+a.cost)
            mass_total += mass
        for o,p in a.outcomes:
            if p:
                stack.append((h+((a.label,o),),mass*p,paid+a.cost))
    need(mass_total==1,"oracle path mass")
    return total

def policies(s):
    nodes = [n for n in s.nodes if n.actions]
    return [r.Policy([(n.h,a) for n,a in zip(nodes,aa)])
            for aa in product(*[[a.label for a in n.actions] for n in nodes])]

def fixture(prob=F(1,2), name="two step"):
    L,R=(("go","L"),),(("go","R"),)
    s=r.Subject(name,2,"loss",("known controlled model",),[
        r.Node((),actions=[r.Action("stop",F(3,4)),r.Action("go",F(1,8),[("L",1-prob),("R",prob)])]),
        r.Node(L,actions=[r.Action("a",0),r.Action("b",F(1,2))]),
        r.Node(R,actions=[r.Action("a",1),r.Action("b",F(1,4))])])
    return s, r.Policy([((),"go"),(L,"b"),(R,"a")])

def deep():
    x,y,z=((("go",a),) for a in ("x","y","z"))
    u,v=x+(("probe","u"),),x+(("probe","v"),)
    w=u+(("step","w"),); end=w+(("last","done"),)
    return r.Subject("signed depth four",4,"loss",(),[
        r.Node((),actions=[r.Action("stop",F(-1,3)),r.Action("go",F(-1,5),[("x",F(2,3)),("y",F(1,3)),("z",0)])]),
        r.Node(end,terminal=F(-5,2)),
        r.Node(z,actions=[r.Action("a",100),r.Action("b",-100)]),
        r.Node(v,terminal=F(7,4)),
        r.Node(w,actions=[r.Action("stop",F(1,9)),r.Action("last",F(3,5),[("done",1)])]),
        r.Node(y,terminal=F(2,7)),
        r.Node(x,actions=[r.Action("stop",F(-2,3)),r.Action("probe",F(1,10),[("u",F(3,4)),("v",F(1,4))])]),
        r.Node(u,actions=[r.Action("step",F(-1,2),[("w",1)])])])

def request(s, c, target=None, pi=None):
    return t.Request(s,c.policy,c,target or s,pi or c.policy,t.identity(s))

def checked(req):
    evidence=t.transport(req)
    answer=t.consume_transport(req,evidence)
    return evidence, answer

def verify_all_nodes(s,pi,cert):
    pp=policies(s)
    for i,n in enumerate(s.nodes):
        optimum=min(oracle(s,p,n.h) for p in pp)
        actual=oracle(s,pi,n.h)
        need(cert.lower[i]<=optimum<=actual<=cert.upper[i],"independent node inequalities")
    return min(oracle(s,p) for p in pp),oracle(s,pi)

def main():
    start=time.perf_counter()
    out=[]
    def record(name,**kw):
        out.append(dict(case=name,status="PASS",**kw))
    s,bad=fixture(); old=r.produce(s); req=request(s,old)
    unchanged,ans=checked(req)
    need(unchanged.certificate==old and set(unchanged.alpha+unchanged.beta)=={F(0)},"identity")
    record("unchanged_subject_policy_tables")

    a=r.Subject("nominal",1,"loss",(),[r.Node((),actions=[r.Action("a",1),r.Action("b",2)])])
    b=replace(a,name="target",nodes=(r.Node((),actions=[r.Action("a",1),r.Action("b",0)]),))
    ac=r.produce(a); rq=request(a,ac,b); ev,ans=checked(rq)
    rejects(lambda:r.consume(b,ac.policy,replace(ac,subject=b)))
    need(ev.certificate.lower==(F(0),) and ev.certificate.upper==(F(1),),"signed comparator repair")
    need(oracle(b,ac.policy)-min(oracle(b,p) for p in policies(b))==1,"true target regret")
    uniform=max(abs(oracle(a,p)-oracle(b,p)) for p in policies(a))
    need(uniform==2 and oracle(a,ac.policy)==oracle(b,ac.policy),"candidate error not comparator error")
    record("comparator_change_candidate_error_zero",alpha=ev.alpha,beta=ev.beta,
           lower=0,upper=1,actual_regret=1,uniform_comparator_error=uniform,uniform_bound=uniform)

    changed,answer=checked(request(s,old,pi=bad))
    optimum,actual=verify_all_nodes(s,bad,changed.certificate)
    need((optimum,actual,answer["regret_upper"])==(F(1,4),F(7,8),F(5,8)),"two step headline")
    rejects(lambda:r.consume(s,bad,old))
    for p in policies(s):
        ee,_=checked(request(s,old,pi=p));verify_all_nodes(s,p,ee.certificate)
    record("new_policy_two_step_all_eight_policies",optimum=optimum,cost=actual,regret=actual-optimum)

    nominal,_=fixture(F(0),"nominal support")
    target,_=fixture(F(1,100),"target support")
    fallback=r.Policy([((),"go"),(s.nodes[1].h,"a"),(s.nodes[2].h,"a")])
    nc=r.produce(nominal,fallback)
    rr=request(nominal,nc,target,fallback); off,offans=checked(rr)
    v,j=verify_all_nodes(target,fallback,off.certificate)
    uniform=max(abs(oracle(nominal,p)-oracle(target,p)) for p in policies(target))
    need((v,j,j-v,offans["regret_upper"],2*uniform)==
         (F(51,400),F(27,200),F(3,400),F(1,100),F(1,50)),"off support")
    rejects(lambda:request(nominal,nc,target,r.Policy(fallback.choices[:-1])))
    record("off_support_union_coverage",optimum=v,cost=j,actual_regret=j-v,
           transport_bound=offans["regret_upper"],symmetric_bound=2*uniform)

    d=deep(); dc=r.produce(d)
    need(len(policies(d))==16 and min(oracle(d,p) for p in policies(d))==F(-53,56),"deep independent optimum")
    # Change signed terminals AND a continuing cost without changing the skeleton.
    dn=list(d.nodes)
    dn[1]=replace(dn[1],terminal=F(-3))
    dn[3]=replace(dn[3],terminal=F(2))
    dn[0]=replace(dn[0],actions=(dn[0].actions[0],replace(dn[0].actions[1],cost=F(-1,4))))
    dt=replace(d,name="revised signed depth four",nodes=dn)
    for p in policies(dt):
        ee,_=checked(request(d,dc,dt,p));verify_all_nodes(dt,p,ee.certificate)
    record("depth_four_signed_early_stop_zero_support_nontopological",policies=16,nodes=8,source_optimum=F(-53,56))

    # Final ordinary checker, not merely a correction helper, catches actual failure paths.
    wrong=replace(ev.certificate,lower=(F(1),))
    rejects(lambda:r.consume(b,ac.policy,wrong))
    rejects(lambda:t.consume_transport(rq,replace(ev,certificate=wrong,alpha=(F(0),))))
    # Understate the changed policy upper repair.
    wrong=replace(changed.certificate,upper=old.upper)
    rejects(lambda:r.consume(s,bad,wrong))
    rejects(lambda:t.consume_transport(request(s,old,pi=bad),replace(changed,certificate=wrong,beta=(F(0),)*3)))
    wrong=replace(changed.certificate,lower=changed.certificate.upper)
    rejects(lambda:r.consume(s,bad,wrong))
    t.consume_transport(rq,ev);r.consume(s,bad,changed.certificate)
    record("understated_corrections_and_missing_competitors_rejected_at_final_consumer")

    # Ordinary target validity does not prove anchored provenance/extremality.
    loose=replace(ev.certificate,lower=(F(-1),))
    r.consume(b,ac.policy,loose)
    rejects(lambda:t.consume_transport(rq,replace(ev,certificate=loose,alpha=(F(2),))))
    rejects(lambda:t.consume_transport(rq,replace(ev,alpha=(F(0),))))
    altered_source=replace(a,name="different source identity")
    other=request(altered_source,r.produce(altered_source),b)
    rejects(lambda:t.consume_transport(other,ev))
    t.consume_transport(rq,ev)
    record("target_only_validity_distinct_from_transport_warrant")

    for other in (replace(s,unit="different unit"),replace(s,horizon=3),
                  replace(s,nodes=(s.nodes[0],s.nodes[2],s.nodes[1]))):
        rejects(lambda:request(s,old,other))
        r.consume(other,old.policy,r.produce(other,old.policy))
    # Changed information/observation and action keys with a valid independent tree.
    renamed=r.Subject("new observed key",2,"loss",(),[
        r.Node((),actions=[r.Action("go",0,[("NEW",1)])]),
        r.Node((("go","NEW"),),terminal=0)])
    rejects(lambda:request(s,old,renamed,r.produce(renamed).policy))
    menu=replace(a,nodes=(r.Node((),actions=[r.Action("a",1)]),))
    rejects(lambda:request(a,ac,menu,ac.policy))
    stop_to_go=r.Subject("changed stop",1,"loss",(),[
        r.Node((),actions=[r.Action("a",1,[("end",1)]),r.Action("b",2)]),
        r.Node((("a","end"),),terminal=0)])
    rejects(lambda:request(a,ac,stop_to_go,ac.policy))
    rejects(lambda:replace(req,correspondence=t.Correspondence(req.correspondence.pairs[:-1])))
    rejects(lambda:replace(req,correspondence=t.Correspondence(list(reversed(req.correspondence.pairs)))))
    rejects(lambda:replace(req,guarantee="tail risk"))
    rejects(lambda:replace(req,target_policy=r.Policy([((),"go")])))
    # Model/premise revision is allowed explicitly, but stale old target consumption fails.
    renamed=replace(s,name="declared revised model",premises=("new supplied premises",))
    nr=request(s,old,renamed); ne,_=checked(nr)
    rejects(lambda:r.consume(s,old.policy,ne.certificate))
    t.consume_transport(nr,ne)
    record("structural_unit_information_criterion_and_identity_boundaries")

    for x in (True,0.0,0):
        rejects(lambda:replace(ev,alpha=(x,)))
        rejects(lambda:replace(ev.certificate,lower=(x,)))
    for x in (True,0.5):
        rejects(lambda:r.Action("x",x))
        rejects(lambda:r.Action("x",0,[("o",x)]))
        rejects(lambda:replace(a,horizon=x))
    huge=F(2**520)
    big=replace(ac,lower=(ac.lower[0]-huge,),upper=(ac.upper[0]+huge,))
    be,_=checked(request(a,big,b))
    need(be.certificate.lower==big.lower and be.certificate.upper==big.upper,"large exact proofs")
    record("exact_fraction_witnesses_no_derived_bit_cap",derived_bits=521)

    pair_rows=[[[],[]],[list(s.nodes[1].h),list(s.nodes[1].h)],[list(s.nodes[2].h),list(s.nodes[2].h)]]
    corr=t.Correspondence(pair_rows)
    proof_rows=list(old.lower); cc=replace(old,lower=proof_rows)
    mr=replace(req,source_certificate=cc,correspondence=corr); me,ma=checked(mr)
    aa=list(me.alpha); mm=replace(me,alpha=aa)
    proof_rows.clear();aa.clear();pair_rows[0][0].append(["hidden","state"]);pair_rows.clear()
    need(t.consume_transport(mr,mm)==ma,"caller aliases")
    try:
        mr.guarantee="changed"
    except FrozenInstanceError:
        pass
    else:
        raise RuntimeError("mutable request")
    record("immutable_request_correspondence_and_proof_aliases")

    q=t.ContinuationQuery(target,fallback,fallback,s.nodes[2].h)
    ce=t.ContinuationEvidence(q,off.certificate,F(1,100))
    ca=t.consume_continuation(q,ce)
    need(ca["regret_upper"]==F(3,4),"conditional gap")
    rejects(lambda:t.consume_continuation(q,replace(ce,mass=F(1,2))))
    qleft=replace(q,event=s.nodes[1].h)
    rejects(lambda:t.consume_continuation(qleft,ce))
    t.consume_continuation(qleft,t.ContinuationEvidence(qleft,off.certificate,F(99,100)))
    prefixstop=r.Policy([((),"stop"),(s.nodes[1].h,"a"),(s.nodes[2].h,"a")])
    qs=replace(q,prefix_policy=prefixstop)
    rejects(lambda:t.consume_continuation(qs,ce))
    rejects(lambda:t.consume_continuation(qs,t.ContinuationEvidence(qs,off.certificate,F(0))))
    qzero=t.ContinuationQuery(nominal,fallback,fallback,s.nodes[2].h)
    rejects(lambda:t.consume_continuation(qzero,t.ContinuationEvidence(qzero,nc,F(0))))
    for x in (True,0.01,1):
        rejects(lambda:t.ContinuationEvidence(q,off.certificate,x))
    rejects(lambda:replace(q,event=(("go","absent"),)))
    # The prefix and continuation need not be the same total rule: bind both.
    qb=replace(q,continuation_policy=bad)
    bc=r.produce(target,bad)
    t.consume_continuation(qb,t.ContinuationEvidence(qb,bc,F(1,100)))
    rejects(lambda:t.consume_continuation(qb,ce))
    record("target_induced_prefix_mass_event_and_policy_binding",
           prefix_mass=ca["prefix_mass"],conditional_regret_bound=ca["regret_upper"],
           zero_mass="impossible conditioning, not empty model")

    child=(("go","child"),)
    repl=r.Subject("overlapping edits",2,"loss",(),[
        r.Node((),actions=[r.Action("stop",2),r.Action("go",0,[("child",1)])]),
        r.Node(child,actions=[r.Action("a",0),r.Action("b",1)])])
    pp=[r.Policy([((),root),(child,action)]) for root,action in
        (("stop","a"),("go","a"),("stop","b"),("go","b"))]
    costs=[oracle(repl,p) for p in pp]
    need(costs==[F(2),F(0),F(2),F(1)],"overlapping replans")
    separate=(costs[1]-costs[0])+(costs[2]-costs[0])
    consecutive=(costs[1]-costs[0])+(costs[3]-costs[1])
    need(separate==-2 and consecutive==costs[3]-costs[0]==-1,"do not add predecessor deltas")
    ee,ra=checked(request(repl,r.produce(repl,pp[0]),pi=pp[3]))
    need(ra["regret_upper"]==2 and costs[3]==1,"anchored upper may keep slack")
    record("overlapping_replans_not_counterexample_to_single_replacement",
           costs=costs,separate_predecessor_sum=separate,consecutive_sum=consecutive,
           final_regret=1,anchored_bound=ra["regret_upper"])

    terminal=r.Subject("H0",0,"loss",(),[r.Node((),terminal=-2)])
    tc=r.produce(terminal);tt=replace(terminal,nodes=(r.Node((),terminal=-3),))
    te,ta=checked(request(terminal,tc,tt))
    need(ta["regret_upper"]==1 and r.root_actions(tt,tc.policy,te.certificate)["status"]=="terminal","terminal")
    tie=replace(a,nodes=(r.Node((),actions=[r.Action("a",-1),r.Action("b",-1)]),))
    ti,ia=checked(request(a,ac,tie))
    need(r.root_actions(tie,ac.policy,ti.certificate)["minimizers"]==["a","b"],"ties")
    singleton=r.Subject("singleton",1,"loss",(),[r.Node((),actions=[r.Action("a",-1)])])
    sc=r.produce(singleton);se,_=checked(request(singleton,sc))
    need(r.root_actions(singleton,sc.policy,se.certificate)["status"]=="forced_menu","singleton")
    for rq0,ev0 in ((request(terminal,tc,tt),te),(request(singleton,sc),se)):
        rejects(lambda:replace(rq0,guarantee="unsupported"))
        rejects(lambda:t.consume_transport(rq0,replace(ev0,alpha=(True,))))
        t.consume_transport(rq0,ev0)
    record("terminal_only_ties_singleton_and_shortcut_validation",terminal_bound=ta["regret_upper"])

    # Reverse comparison: opposite stage shifts cancel for the only full policy.
    h=(("go","x"),)
    cancel=r.Subject("cancellation source",2,"loss",(),[
        r.Node((),actions=[r.Action("go",0,[("x",1)])]),
        r.Node(h,actions=[r.Action("end",0)])])
    targetcancel=replace(cancel,name="cancellation target",nodes=(
        r.Node((),actions=[r.Action("go",100,[("x",1)])]),
        r.Node(h,actions=[r.Action("end",-100)])))
    c0=r.produce(cancel);e0,ca=checked(request(cancel,c0,targetcancel))
    need(oracle(cancel,c0.policy)==oracle(targetcancel,c0.policy)==0 and ca["regret_upper"]==100,"non dominance")
    record("uniform_comparison_can_be_tighter",uniform_error=0,uniform_bound=0,anchored_bound=100)

    # A full direct target certificate can be tighter than the anchored one.
    tight=r.produce(targetcancel,c0.policy)
    r.consume(targetcancel,c0.policy,tight)
    rejects(lambda:t.consume_transport(request(cancel,c0,targetcancel),replace(e0,certificate=tight,beta=(F(0),F(0)))))
    record("extremality_only_with_anchor_constraints")

    saved_t,saved_r=t.transport,r.produce
    def disabled(*args,**kwargs):
        raise RuntimeError("producer invoked by receiver")
    t.transport=disabled;r.produce=disabled
    t.consume_transport(rq,ev)
    r.consume(b,ac.policy,ev.certificate)
    t.consume_continuation(q,ce)
    t.transport=saved_t;r.produce=saved_r
    record("receivers_independent_of_both_producers")

    print(json.dumps(r.wire(dict(passed=len(out),failed=0,rejections=REJECTIONS,
          optimized=sys.flags.optimize,elapsed_seconds=time.perf_counter()-start,results=out)),sort_keys=True))

if __name__=="__main__":
    main()
