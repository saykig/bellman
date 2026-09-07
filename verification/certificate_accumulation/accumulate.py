"""Finite same-policy accumulation and separately warranted policy selection."""
from dataclasses import dataclass
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"certificate_transport"))
import transport as t
r=t.r

@dataclass(frozen=True)
class Source:
    identity: str
    certificate: r.Certificate
    def __post_init__(self):
        r.need(type(self.identity) is str and bool(self.identity),"nonempty source identity")
        r.need(type(self.certificate) is r.Certificate,"source certificate")

@dataclass(frozen=True)
class Request:
    subject: r.Subject
    sources: tuple
    mode: str
    policy: object = None
    criterion: str = t.GUARANTEE
    def __post_init__(self):
        r.need(type(self.sources) in (list,tuple),"source sequence")
        object.__setattr__(self,"sources",tuple(self.sources))
        self.validate()
    def validate(self):
        t.skeleton(self.subject)
        r.need(type(self.criterion) is str and self.criterion==t.GUARANTEE,"unsupported criterion")
        r.need(type(self.mode) is str and self.mode in ("same-policy","selection"),"operation")
        r.need(1<=len(self.sources)<=16,"one to sixteen sources; otherwise unsupported/unfinished")
        r.need(all(type(x) is Source for x in self.sources),"source types")
        ids=[x.identity for x in self.sources]
        r.need(len(set(ids))==len(ids),"duplicate source identities")
        if self.mode=="same-policy":
            r.need(type(self.policy) is r.Policy,"expected policy")
            self.policy.validate(self.subject)
        else:
            r.need(self.policy is None,"selection creates a new policy")
        for x in self.sources:
            c=x.certificate
            r.consume(self.subject,c.policy,c)
            if self.mode=="same-policy":
                r.need(c.policy==self.policy,"different policies require selection")
        return self

@dataclass(frozen=True)
class Evidence:
    request: Request
    certificate: r.Certificate
    selector: tuple = ()
    def __post_init__(self):
        r.need(type(self.request) is Request and type(self.certificate) is r.Certificate,"evidence types")
        r.need(type(self.selector) in (list,tuple),"selector sequence")
        rows=[]
        for row in self.selector:
            r.need(type(row) in (list,tuple) and len(row)==2,"selector row")
            h,i=row
            r.need(type(i) is str and i,"selector identity")
            rows.append((r.history(h),i))
        object.__setattr__(self,"selector",tuple(rows))

def _produce(req):
    req.validate()
    cs=[x.certificate for x in req.sources]
    lo=tuple(max(c.lower[k] for c in cs) for k in range(len(req.subject.nodes)))
    up=tuple(min(c.upper[k] for c in cs) for k in range(len(req.subject.nodes)))
    selector=[]
    if req.mode=="same-policy":
        pi=req.policy
    else:
        choices=[]
        for k,n in enumerate(req.subject.nodes):
            if n.actions:
                winner=min(req.sources,key=lambda x:(x.certificate.upper[k],x.identity))
                selector.append((n.h,winner.identity))
                choices.append((n.h,dict(winner.certificate.policy.choices)[n.h]))
        pi=r.Policy(choices)
    return Evidence(req,r.Certificate(req.subject,pi,lo,up),selector)

def combine(req):
    r.need(type(req) is Request and req.mode=="same-policy","same-policy operation")
    return _produce(req)

def select(req):
    r.need(type(req) is Request and req.mode=="selection","selection operation")
    return _produce(req)

def consume(expected,intended_policy,evidence):
    r.need(type(expected) is Request and type(evidence) is Evidence,"expected request and evidence")
    r.need(type(intended_policy) is r.Policy,"independently intended output policy")
    expected.validate();evidence.request.validate()
    r.need(expected==evidence.request,"wrong collection or source identity")
    s=expected.subject
    answer=r.consume(s,intended_policy,evidence.certificate)
    # Receiver checks each coordinate against every source and an attaining source.
    c=evidence.certificate
    for k in range(len(s.nodes)):
        lows=[x.certificate.lower[k] for x in expected.sources]
        ups=[x.certificate.upper[k] for x in expected.sources]
        r.need(all(c.lower[k]>=v for v in lows) and c.lower[k] in lows,"false lower maximum")
        r.need(all(c.upper[k]<=v for v in ups) and c.upper[k] in ups,"false upper minimum")
    if expected.mode=="same-policy":
        r.need(intended_policy==expected.policy and evidence.selector==(),"wrong same-policy output")
    else:
        nodes=[n for n in s.nodes if n.actions]
        r.need(tuple(h for h,_ in evidence.selector)==tuple(n.h for n in nodes),"total ordered selector")
        chosen=dict(intended_policy.choices)
        for h,identity in evidence.selector:
            k=next(k for k,n in enumerate(s.nodes) if n.h==h)
            winners=[x for x in expected.sources if x.certificate.upper[k]==c.upper[k]]
            winner=min(winners,key=lambda x:x.identity)
            r.need(identity==winner.identity,"wrong selector or deterministic tie")
            r.need(chosen[h]==dict(winner.certificate.policy.choices)[h],"selector/policy mismatch")
    return dict(answer,warrant=expected.mode,source_identities=tuple(x.identity for x in expected.sources))

def consume_exact_selection(expected,intended_policy,evidence):
    """Additional warrant: source upper tables equal their full policy values."""
    r.need(type(expected) is Request and expected.mode=="selection","selection required")
    answer=consume(expected,intended_policy,evidence)
    for x in expected.sources:
        c=x.certificate
        up=r.table(expected.subject,c.upper)
        chosen=dict(c.policy.choices)
        for n in expected.subject.nodes:
            if not n.actions:
                value=n.terminal
            else:
                a=next(a for a in n.actions if a.label==chosen[n.h])
                value=a.cost+sum((p*up[n.h+((a.label,o),)] for o,p in a.outcomes),r.F(0))
            r.need(up[n.h]==value,"upper bound is not exact policy value")
    return dict(answer,actual_dominance="no worse than every source policy at every completed node")
