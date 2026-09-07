"""Exact finite observable-history certificates. Standard library only."""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product

class Invalid(ValueError):
    pass

def need(ok, message):
    if not ok:
        raise Invalid(message)

def q(x):
    need(type(x) in (int, F), "exact integer/Fraction model coefficient required")
    x = F(x)
    need(max(abs(x.numerator).bit_length(), x.denominator.bit_length()) <= 256,
         "model coefficient limit")
    return x

def proof(values):
    need(type(values) in (tuple, list), "proof vector required")
    need(all(type(x) is F for x in values), "exact Fraction proof values required")
    return tuple(values)

def history(h):
    need(type(h) in (tuple, list), "history sequence required")
    result = []
    for pair in h:
        need(type(pair) in (tuple, list) and len(pair) == 2, "action/observation pair")
        need(all(type(x) is str and x for x in pair), "observable string labels")
        result.append(tuple(pair))
    return tuple(result)

@dataclass(frozen=True)
class Action:
    label: str
    cost: F
    outcomes: tuple = ()  # Empty means STOP: pay cost and terminate.
    def __post_init__(self):
        need(type(self.label) is str and self.label, "action label")
        object.__setattr__(self, "cost", q(self.cost))
        rows = []
        for row in self.outcomes:
            need(type(row) in (tuple, list) and len(row) == 2, "observation/probability row")
            o, p = row
            need(type(o) is str and o, "observation label")
            rows.append((o, q(p)))
        object.__setattr__(self, "outcomes", tuple(rows))
        need(len(rows) <= 4 and len({o for o, _ in rows}) == len(rows), "outcome menu")
        if rows:
            need(all(p >= 0 for _, p in rows) and sum(p for _, p in rows) == 1, "normalized law")

@dataclass(frozen=True)
class Node:
    h: tuple
    terminal: F = F(0)
    actions: tuple = ()
    def __post_init__(self):
        object.__setattr__(self, "h", history(self.h))
        object.__setattr__(self, "terminal", q(self.terminal))
        object.__setattr__(self, "actions", tuple(self.actions))
        need(all(type(a) is Action for a in self.actions), "immutable actions")
        need(len(self.actions) <= 4 and len({a.label for a in self.actions}) == len(self.actions), "action menu")
        need(not self.actions or self.terminal == 0, "terminal cost only on terminal nodes")

@dataclass(frozen=True)
class Subject:
    name: str
    horizon: int
    unit: str
    premises: tuple
    nodes: tuple
    def __post_init__(self):
        object.__setattr__(self, "premises", tuple(self.premises))
        object.__setattr__(self, "nodes", tuple(self.nodes))
        self.validate()
    def validate(self):
        need(type(self.name) is str and type(self.unit) is str and self.name and self.unit, "subject meanings")
        need(all(type(p) is str for p in self.premises), "immutable premise labels")
        need(type(self.horizon) is int and 0 <= self.horizon <= 4, "horizon 0..4")
        need(1 <= len(self.nodes) <= 64 and all(type(n) is Node for n in self.nodes), "node limit")
        hs = [n.h for n in self.nodes]
        need(len(set(hs)) == len(hs) and hs[0] == (), "unique nodes, root first")
        children = []
        for n in self.nodes:
            need(len(n.h) <= self.horizon, "node beyond horizon")
            need(len(n.h) < self.horizon or not n.actions, "no action at horizon")
            for a in n.actions:
                children.extend(n.h + ((a.label, o),) for o, _ in a.outcomes)
        need(len(set(children)) == len(children) and set(children) == set(hs[1:]), "complete tree; no inaccessible or missing histories")
        return self

@dataclass(frozen=True)
class Policy:
    choices: tuple
    def __post_init__(self):
        rows = []
        for row in self.choices:
            need(type(row) in (tuple, list) and len(row) == 2, "policy row")
            h, a = row
            need(type(a) is str, "action label")
            rows.append((history(h), a))
        object.__setattr__(self, "choices", tuple(rows))
    def validate(self, s):
        s.validate()
        d = dict(self.choices)
        need(len(d) == len(self.choices), "duplicate policy history")
        need(set(d) == {n.h for n in s.nodes if n.actions}, "total observable policy required")
        for n in s.nodes:
            if n.actions:
                need(d[n.h] in {a.label for a in n.actions}, "illegal action")
        return d

def table(s, values):
    s.validate()
    values = proof(values)
    need(len(values) == len(s.nodes), "complete node table")
    return dict(zip((n.h for n in s.nodes), values))

def _backup_action(n, a, v):
    # Caller has validated subject and tables; zero-mass branches need no posterior.
    return a.cost + sum((p*v[n.h+((a.label,o),)] for o,p in a.outcomes if p), F(0))

@dataclass(frozen=True)
class Certificate:
    subject: Subject
    policy: Policy
    lower: tuple
    upper: tuple
    def __post_init__(self):
        need(type(self.subject) is Subject and type(self.policy) is Policy, "certificate types")
        object.__setattr__(self, "lower", proof(self.lower))
        object.__setattr__(self, "upper", proof(self.upper))

def consume(expected, intended_policy, certificate):
    expected.validate()
    intended_policy.validate(expected)
    certificate.subject.validate()
    certificate.policy.validate(certificate.subject)
    need(expected == certificate.subject and intended_policy == certificate.policy, "stale subject or policy")
    lo, up = table(expected, certificate.lower), table(expected, certificate.upper)
    pi = dict(intended_policy.choices)
    for n in expected.nodes:
        if not n.actions:
            need(lo[n.h] <= n.terminal <= up[n.h], "terminal bounds")
        else:
            need(all(lo[n.h] <= _backup_action(n,a,lo) for a in n.actions), "optimum lower bound needs every action")
            a = next(a for a in n.actions if a.label == pi[n.h])
            need(up[n.h] >= _backup_action(n,a,up), "policy upper bound")
    need(up[()] >= lo[()], "negative certificate gap")
    return {"optimum_lower": lo[()], "policy_upper": up[()], "regret_upper": up[()]-lo[()]}

def root_actions(expected, intended_policy, cert):
    consume(expected, intended_policy, cert)
    n = expected.nodes[0]
    if not n.actions:
        return {"status": "terminal", "minimizers": [], "strict": False}
    lo, up = table(expected,cert.lower), table(expected,cert.upper)
    intervals = {a.label:(_backup_action(n,a,lo),_backup_action(n,a,up)) for a in n.actions}
    if len(intervals) == 1:
        return {"status":"forced_menu", "minimizers":list(intervals), "strict":False}
    if all(l == u for l,u in intervals.values()):
        best = min(l for l,u in intervals.values())
        winners = [a for a,(l,u) in intervals.items() if l == best]
        return {"status":"exact", "minimizers":winners, "strict":len(winners)==1}
    winners = [a for a,(l,u) in intervals.items() if all(u < lb for b,(lb,ub) in intervals.items() if b != a)]
    return {"status":"strict" if winners else "uncertified", "minimizers":winners or None, "strict":bool(winners)}

def residual_certificate(s, pi, values, residuals, greediness):
    s.validate()
    chosen = pi.validate(s)
    v, r, z = table(s,values), table(s,residuals), table(s,greediness)
    need(all(x >= 0 for x in tuple(r.values())+tuple(z.values())), "nonnegative allowances")
    ev, ep = {}, {}
    for n in sorted(s.nodes,key=lambda n:len(n.h),reverse=True):
        if not n.actions:
            need(abs(v[n.h]-n.terminal) <= r[n.h] and z[n.h] == 0, "terminal residual")
            ev[n.h] = ep[n.h] = r[n.h]
        else:
            qs = {a.label:_backup_action(n,a,v) for a in n.actions}
            best = min(qs.values())
            need(abs(v[n.h]-best) <= r[n.h], "understated backup residual")
            need(qs[chosen[n.h]]-best <= z[n.h], "wrong policy/backup pairing")
            future = lambda a,w: sum((p*w[n.h+((a.label,o),)] for o,p in a.outcomes if p),F(0))
            ev[n.h] = r[n.h] + max(future(a,ev) for a in n.actions)
            a = next(a for a in n.actions if a.label==chosen[n.h])
            ep[n.h] = r[n.h]+z[n.h]+future(a,ep)
    cert = Certificate(s,pi,tuple(v[n.h]-ev[n.h] for n in s.nodes),tuple(v[n.h]+ep[n.h] for n in s.nodes))
    consume(s,pi,cert)
    return cert

def produce(s, pi=None):
    """Producer only. Exact backward optimization and separate policy evaluation."""
    s.validate()
    v, choices = {}, {}
    for n in sorted(s.nodes,key=lambda n:len(n.h),reverse=True):
        if not n.actions:
            v[n.h] = n.terminal
        else:
            qs = [(_backup_action(n,a,v),a.label) for a in n.actions]
            v[n.h], choices[n.h] = min(qs)
    if pi is None:
        pi = Policy(tuple((n.h,choices[n.h]) for n in s.nodes if n.actions))
    selected = pi.validate(s)
    j = {}
    for n in sorted(s.nodes,key=lambda n:len(n.h),reverse=True):
        if not n.actions:
            j[n.h] = n.terminal
        else:
            a = next(a for a in n.actions if a.label==selected[n.h])
            j[n.h] = _backup_action(n,a,j)
    return Certificate(s,pi,tuple(v[n.h] for n in s.nodes),tuple(j[n.h] for n in s.nodes))

def paths(s, pi):
    """Independent forward complete-path cost sums; no backup/producer calls."""
    chosen = pi.validate(s)
    nodes = {n.h:n for n in s.nodes}
    leaves = []
    def visit(h,mass,cost):
        n = nodes[h]
        if not n.actions:
            leaves.append((h,mass,cost+n.terminal))
            return
        a = next(a for a in n.actions if a.label==chosen[h])
        if not a.outcomes:
            leaves.append((h+((a.label,"STOP"),),mass,cost+a.cost))
        for o,p in a.outcomes:
            if p:
                visit(h+((a.label,o),),mass*p,cost+a.cost)
    visit((),F(1),F(0))
    need(sum(p for _,p,_ in leaves)==1,"path mass")
    return tuple(leaves)

def path_cost(s,pi):
    return sum((mass*cost for _,mass,cost in paths(s,pi)),F(0))

def enumerate_policies(s):
    s.validate()
    nodes = [n for n in s.nodes if n.actions]
    size = 1
    for n in nodes:
        size *= len(n.actions)
    need(size <= 4096, "policy enumeration budget; unfinished")
    return tuple(Policy(tuple((n.h,a) for n,a in zip(nodes,aa))) for aa in product(*(tuple(a.label for a in n.actions) for n in nodes)))

def telescoping(s,pi,optimum):
    chosen = pi.validate(s)
    v = table(s,optimum)
    for n in s.nodes:
        target = min(_backup_action(n,a,v) for a in n.actions) if n.actions else n.terminal
        need(v[n.h] == target, "comparator must be same exact optimum")
    mass = {n.h:F(0) for n in s.nodes}
    mass[()] = F(1)
    total = F(0)
    for n in sorted(s.nodes,key=lambda n:len(n.h)):
        if n.actions:
            a = next(a for a in n.actions if a.label==chosen[n.h])
            d = _backup_action(n,a,v)-v[n.h]
            need(d >= 0,"negative Bellman disadvantage")
            total += mass[n.h]*d
            for o,p in a.outcomes:
                mass[n.h+((a.label,o),)] += mass[n.h]*p
    need(total == path_cost(s,pi)-v[()],"telescoping identity")
    return total

def conditioning(P,Q,event):
    P,Q = proof(P),proof(Q)
    need(0 < len(P)==len(Q)==len(event),"common space")
    need(all(type(e) is int and e in (0,1) for e in event),"event indicator")
    need(min(P+Q)>=0 and sum(P)==sum(Q)==1,"probability laws")
    a,b = sum(p*e for p,e in zip(P,event)),sum(q*e for q,e in zip(Q,event))
    need(a>0 and b>0,"undefined zero-mass conditioning")
    delta = sum(abs(p-q) for p,q in zip(P,Q))/2
    conditional = sum(abs(p/a-q/b) for p,q,e in zip(P,Q,event) if e)/2
    radius = min(F(1),delta/max(a,b))
    need(conditional <= radius,"conditioning inequality")
    return a,b,delta,conditional,radius

def wire(x):
    if type(x) is F:
        return str(x)
    if isinstance(x,dict):
        return {str(k):wire(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):
        return [wire(v) for v in x]
    return x
