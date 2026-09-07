"""Fixed accumulation cases, independent complete-path oracle, no search grid."""
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import json,sys
import accumulate as a
r,t=a.r,a.t
count=0
def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def reject(fn):
    global count
    try: fn()
    except r.Invalid:
        count+=1
        return
    raise RuntimeError("invalid warrant accepted")
def value(s,pi,start=()):
    nodes={n.h:n for n in s.nodes};chosen=dict(pi.choices)
    stack=[(start,F(1),F(0))];total=F(0);mass=F(0)
    while stack:
        h,p,c=stack.pop();n=nodes[h]
        if not n.actions:
            total+=p*(c+n.terminal);mass+=p;continue
        ac=next(x for x in n.actions if x.label==chosen[h])
        if not ac.outcomes:
            total+=p*(c+ac.cost);mass+=p
        for o,q in ac.outcomes:
            stack.append((h+((ac.label,o),),p*q,c+ac.cost))
    need(mass==1,"path normalization")
    return total
def exact(s,pi):
    ns=[n for n in s.nodes if n.actions]
    pp=[r.Policy([(n.h,x) for n,x in zip(ns,choices)]) for choices in product(*[[x.label for x in n.actions] for n in ns])]
    return r.Certificate(s,pi,tuple(min(value(s,p,n.h) for p in pp) for n in s.nodes),
                         tuple(value(s,pi,n.h) for n in s.nodes))
def req(s,cs,pi=None,mode="same-policy"):
    return a.Request(s,[a.Source(str(i),c) for i,c in enumerate(cs)],mode,pi)
def run(q):
    e=a.combine(q) if q.mode=="same-policy" else a.select(q)
    return e,a.consume(q,e.certificate.policy,e)
def main():
    out=[]
    def record(name,**kw):out.append(dict(case=name,status="PASS",**kw))
    L,R=(("go","L"),),(("go","R"),)
    s=r.Subject("PR5 fixed tree",2,"loss",(),[
        r.Node((),actions=[r.Action("stop",F(3,4)),r.Action("go",F(1,8),[("L",F(1,2)),("R",F(1,2))])]),
        r.Node(L,actions=[r.Action("a",0),r.Action("b",F(1,2))]),
        r.Node(R,actions=[r.Action("a",1),r.Action("b",F(1,4))])])
    pi=r.Policy([((),"go"),(L,"b"),(R,"a")]);c=exact(s,pi)
    c1=replace(c,upper=tuple(x+1 for x in c.upper))
    c2=replace(c,lower=tuple(x-1 for x in c.lower))
    q=req(s,[c1,c2],pi);e,ans=run(q)
    need(e.certificate==c and ans["regret_upper"]==F(5,8),"complementary evidence")
    need(all(r.consume(s,pi,x)["regret_upper"]==F(13,8) for x in (c1,c2)),"input gaps")
    need(value(s,pi)==F(7,8) and c.lower[0]==F(1,4),"independent exact values")
    record("complementary_same_policy",input_gap=F(13,8),combined_gap=F(5,8),actual_cost=F(7,8))

    c3=replace(c,lower=tuple(x-2 for x in c.lower),upper=tuple(x+2 for x in c.upper))
    reversed_e,_=run(replace(q,sources=tuple(reversed(q.sources))))
    dup,_=run(req(s,[c1,c1],pi))
    left,_=run(req(s,[e.certificate,c3],pi))
    bc,_=run(req(s,[c2,c3],pi));right,_=run(req(s,[c1,bc.certificate],pi))
    need(reversed_e.certificate==e.certificate==left.certificate==right.certificate,"commutative associative")
    need(dup.certificate==c1 and len(dup.request.sources)==2,"idempotent tables distinct warrants")
    record("table_laws_and_monotone_addition_provenance_retained")

    home=r.Subject("home",1,"loss",(),[r.Node((),actions=[r.Action("a",0),r.Action("b",1)])])
    away=replace(home,name="away",nodes=(r.Node((),actions=[r.Action("a",2),r.Action("b",1)]),))
    pa=r.Policy([((),"a")]);hc=exact(home,pa)
    def send(g,c,f):
        tr=t.Request(g,c.policy,c,f,c.policy,t.identity(g));te=t.transport(tr)
        t.consume_transport(tr,te);return te.certificate
    mid=send(home,hc,away);back=send(away,mid,home);direct=send(home,hc,home)
    restored,ra=run(req(home,[back,hc],pa))
    need((mid.lower,mid.upper,back.lower,back.upper)==((F(0),),(F(2),),(F(0),),(F(2),)),"round trip")
    need(restored.certificate==direct==hc and value(home,pa)==0,"retained warrant")
    reject(lambda:req(away,[mid,hc],pa))
    reject(lambda:req(replace(home,unit="other"),[hc],pa))
    record("round_trip_slack_removed_on_exact_restored_subject",before=2,after=0,actual_regret=0)

    split=r.Subject("split",2,"loss",(),[
        r.Node((),actions=[r.Action("go",0,[("L",F(1,2)),("R",F(1,2))])]),
        r.Node(L,actions=[r.Action("a",0),r.Action("b",2)]),
        r.Node(R,actions=[r.Action("a",2),r.Action("b",0)])])
    pA=r.Policy([((),"go"),(L,"a"),(R,"a")]);pB=r.Policy([((),"go"),(L,"b"),(R,"b")])
    ca,cb=exact(split,pA),exact(split,pB)
    sq=req(split,[ca,cb],mode="selection");se,sa=run(sq)
    reject(lambda:r.consume(split,pA,replace(se.certificate,policy=pA)))
    reject(lambda:req(split,[ca,cb],pA))
    a.consume_exact_selection(sq,se.certificate.policy,se)
    need(value(split,se.certificate.policy)==0 and sa["policy_upper"]==1,"selector bound not attained")
    need(value(split,pA)==value(split,pB)==1,"source costs")
    reject(lambda:a.consume(sq,pA,se))
    badsel=list(se.selector);badsel[-1]=(R,"0")
    reject(lambda:a.consume(sq,se.certificate.policy,replace(se,selector=badsel)))
    reject(lambda:a.consume(sq,se.certificate.policy,replace(se,selector=se.selector[:-1])))
    record("different_policy_selector_and_exact_value_dominance",source_costs=[1,1],selected_cost=0,upper=1)

    pb=r.Policy([((),"b")]);bcert=exact(home,pb);loose=replace(hc,upper=(F(2),))
    lq=req(home,[loose,bcert],mode="selection");le,la=run(lq)
    need(le.certificate.policy==pb and value(home,pb)>value(home,pa),"loose not dominance")
    reject(lambda:a.consume_exact_selection(lq,pb,le))
    record("loose_upper_selection_not_actual_dominance",selected_cost=1,other_cost=0)

    other=replace(home,name="other model",nodes=(r.Node((),actions=[r.Action("a",1),r.Action("b",0)]),))
    oc=exact(other,pb)
    reject(lambda:req(home,[hc,oc],mode="selection"))
    need([(value(home,p),value(other,p)) for p in (pa,pb)]==[(F(0),F(1)),(F(1),F(0))],"no common zero policy")
    reject(lambda:r.Policy([((("model","other"),),"b")]).validate(home))
    record("mixed_models_rejected_not_hidden_model_selector")

    reject(lambda:req(s,[],pi))
    reject(lambda:req(s,[replace(c,lower=c.upper)],pi))
    reject(lambda:req(s,[replace(c,lower=c.lower[:-1])],pi))
    reject(lambda:replace(q,criterion="tail-risk"))
    reject(lambda:replace(q,policy=pA))
    reject(lambda:replace(q,sources=(q.sources[0],q.sources[0])))
    reject(lambda:a.consume(replace(q,sources=q.sources[:1]),pi,e))
    renamed=replace(q,sources=(replace(q.sources[0],identity="false identity"),q.sources[1]))
    reject(lambda:a.consume(renamed,pi,e))
    # Standalone valid but not the claimed extrema.
    stand=replace(c,lower=tuple(x-1 for x in c.lower))
    r.consume(s,pi,stand)
    reject(lambda:a.consume(q,pi,replace(e,certificate=stand)))
    reject(lambda:a.consume(q,pi,replace(e,certificate=replace(c,lower=c.upper,upper=c.lower))))
    a.consume(q,pi,e)
    record("whole_collection_rejection_identity_direction_and_false_derivation")

    for x in (True,0.0,0):
        reject(lambda:replace(c,lower=(x,)+c.lower[1:]))
    huge=F(2**1024)
    large=replace(hc,lower=(-huge,),upper=(huge,))
    big,_=run(req(home,[large,large],pa))
    need(big.certificate==large,"large proof values")
    src=list(q.sources);mq=replace(q,sources=src);me,_=run(mq);src.clear()
    lows=list(c.lower);mc=replace(c,lower=lows);lows.clear()
    need(mc==c and a.consume(mq,pi,me)==ans,"mutation detached")
    choices=[[[],"a"]];mp=r.Policy(choices);mh=exact(home,mp)
    choices[0][1]="b";need(mh.policy==pa,"policy detached")
    record("exact_proofs_large_fractions_immutable_containers",derived_bits=1025)

    zero=r.Subject("terminal",0,"loss",(),[r.Node((),terminal=-2)])
    zc=exact(zero,r.Policy([]));ze,_=run(req(zero,[zc,zc],mode="selection"))
    need(ze.selector==() and r.root_actions(zero,zc.policy,ze.certificate)["status"]=="terminal","H0")
    one=r.Subject("singleton",1,"loss",(),[r.Node((),actions=[r.Action("a",-1)])])
    on=exact(one,pa);oe,_=run(req(one,[on],pa))
    need(r.root_actions(one,pa,oe.certificate)["status"]=="forced_menu","singleton")
    tq=replace(sq,sources=(a.Source("z",ca),a.Source("a",cb)))
    tie,_=run(tq)
    need(dict(tie.selector)[()]=="a","lexical source tie")
    reorder,_=run(replace(tq,sources=tuple(reversed(tq.sources))))
    need(tie.selector==reorder.selector and tie.certificate==reorder.certificate,"tie independent of input order")
    reject(lambda:a.consume(tq,tie.certificate.policy,replace(tie,selector=(((),"z"),)+tie.selector[1:])))
    reject(lambda:replace(req(zero,[zc],zc.policy),criterion="unsupported"))
    record("terminal_singleton_tied_selector_shortcuts")

    off=replace(split,name="zero branch",nodes=(replace(split.nodes[0],actions=(r.Action("go",0,[("L",1),("R",0)]),)),split.nodes[2],split.nodes[1]))
    oca,ocb=exact(off,pA),exact(off,pB);oq=req(off,[oca,ocb],mode="selection");oo,_=run(oq)
    need(len(oo.selector)==3,"zero branch selector coverage")
    reject(lambda:a.consume(oq,oo.certificate.policy,replace(oo,selector=oo.selector[:-1])))
    cq=t.ContinuationQuery(off,pA,oo.certificate.policy,L)
    need(t.consume_continuation(cq,t.ContinuationEvidence(cq,oo.certificate,F(1)))["prefix_mass"]==1,"positive prefix")
    zr=replace(cq,event=R)
    reject(lambda:t.consume_continuation(zr,t.ContinuationEvidence(zr,oo.certificate,F(0))))
    record("zero_support_nontopological_storage_and_conditioning")

    saved=(a.combine,a.select,a._produce,r.produce,t.transport)
    def disabled(*args,**kwargs):raise RuntimeError("producer invoked")
    a.combine=a.select=a._produce=r.produce=t.transport=disabled
    a.consume(q,pi,e);a.consume_exact_selection(sq,se.certificate.policy,se)
    r.consume(s,pi,e.certificate)
    reject(lambda:a.consume(q,pi,replace(e,certificate=stand)))
    a.combine,a.select,a._produce,r.produce,t.transport=saved
    record("ordinary_combination_and_selection_receivers_without_producers")
    print(json.dumps(r.wire(dict(passed=len(out),failed=0,rejections=count,results=out,optimized=sys.flags.optimize)),sort_keys=True))
if __name__=="__main__":main()
