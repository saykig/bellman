"""Finite rational certificate reference. No external solver, network, or file writes.

Producer: bounded active-set proposals. Consumer: exact subject and inequality checks.
No failed search is interpreted as infeasibility. See the additive mathematical note.
"""
from dataclasses import dataclass, replace, asdict
from fractions import Fraction as F
from itertools import combinations
import re


class Invalid(ValueError):
    pass


def need(ok, message):
    if not ok:
        raise Invalid(message)


def rational(x):
    need(type(x) in (int, str, F), 'rational input required; floats/bools excluded')
    if isinstance(x, str):
        need(re.fullmatch(r'-?[0-9]+(?:/[1-9][0-9]*)?', x) is not None, 'integer or fraction spelling required')
    x = F(x)
    need(max(abs(x.numerator).bit_length(), x.denominator.bit_length()) <= 256, 'input coefficient limit')
    return x


def vector(v):
    return tuple(rational(x) for x in v)


def dot(a, b):
    need(len(a) == len(b), 'dimension mismatch')
    return sum((x*y for x, y in zip(a, b)), F(0))


@dataclass(frozen=True)
class Polynomial:
    # Each term is (rational coefficient, tuple of nonnegative integer exponents).
    label: str
    terms: tuple
    relation: str = 'eq'

    def holds(self, p):
        need(self.relation in ('eq', 'le'), 'unsupported original predicate')
        value = F(0)
        for c, exponents in self.terms:
            c = rational(c)
            need(len(exponents) == len(p) and all(type(k) is int and 0 <= k <= 8 for k in exponents), 'invalid polynomial term')
            for x, k in zip(p, exponents):
                c *= x**k
            value += c
        return value == 0 if self.relation == 'eq' else value <= 0


@dataclass(frozen=True)
class Model:
    variable_order: tuple
    atom_order: tuple
    A: tuple
    b: tuple
    C: tuple
    d: tuple
    premises: tuple
    extra_original: tuple = ()

    def validate(self):
        n = len(self.atom_order)
        need(1 <= n <= 8, 'reference limit: 1..8 atoms')
        need(len(set(self.atom_order)) == n and all(len(a) == len(self.variable_order) for a in self.atom_order), 'atom order')
        need(len(set(self.variable_order)) == len(self.variable_order), 'variable order')
        need(len(self.A) == len(self.b) and len(self.C) == len(self.d), 'row count')
        need(len(self.A)+len(self.C) <= 16, 'reference row limit')
        need(all(len(r) == n for r in self.A+self.C), 'matrix dimensions')
        for r in self.A+self.C+(self.b,self.d):
            for v in r:
                rational(v)
                need(type(v) is F, 'use make_model to normalize coefficients')
        need(any(r == (F(1),)*n and b == 1 for r,b in zip(self.A,self.b)), 'explicit normalization required')
        need(len(self.extra_original) <= 8, 'original-predicate limit')
        for p in self.extra_original:
            need(len(p.terms) <= 32, 'polynomial term limit')
            p.holds((F(0),)*n)  # validates the point-checkable predicate, not its truth.
        return self


def make_model(variables, atoms, A, b, C=(), d=(), premises=(), extra=()):
    return Model(tuple(variables), tuple(tuple(a) for a in atoms), tuple(vector(r) for r in A), vector(b),
                 tuple(vector(r) for r in C), vector(d), tuple(premises), tuple(extra)).validate()


@dataclass(frozen=True)
class Task:
    model: Model
    event_label: str
    event: tuple
    numerator: tuple
    conditional: bool
    query_label: str
    loss_unit: str
    actions: tuple = ()
    direction: str = 'max'

    def validate(self):
        self.model.validate()
        n = len(self.model.atom_order)
        need(type(self.conditional) is bool and self.direction in ('max','min'), 'task mode')
        need(len(self.event) == len(self.numerator) == n, 'task dimensions')
        need(all(type(v) is F for v in self.event+self.numerator), 'normalized rational task required')
        need(all(v in (0,1) for v in self.event), 'event indicator')
        if self.conditional:
            need(all(e or u == 0 for e,u in zip(self.event,self.numerator)), 'conditional numerator must vanish outside event')
        else:
            need(all(e == 1 for e in self.event), 'unconditional task uses whole space')
        need(len(self.actions) <= 8 and len({a for a,_ in self.actions}) == len(self.actions), 'action limit or duplicate labels')
        for _,r in self.actions:
            need(len(r) == n, 'loss dimensions')
            for x in r:
                need(type(x) is F, 'normalized rational losses required')
                rational(x)
        for x in self.numerator:
            rational(x)
        return self


def make_task(model, event, numerator, conditional=True, event_label='e', query_label='query', unit='loss', actions=(), direction='max'):
    return Task(model,event_label,vector(event),vector(numerator),conditional,query_label,unit,
                tuple((a,vector(r)) for a,r in actions),direction).validate()


def difference(task, a, b):
    losses = dict(task.actions)
    need(a in losses and b in losses and a != b, 'distinct declared actions required')
    return replace(task, numerator=tuple(e*(x-y) for e,x,y in zip(task.event,losses[a],losses[b])),
                   query_label='risk difference: '+a+' minus '+b,direction='max').validate()


@dataclass(frozen=True)
class LP:
    A: tuple
    b: tuple
    C: tuple
    d: tuple
    objective: tuple


def lp(task):
    task.validate()
    m = task.model
    r = task.numerator if task.direction == 'max' else tuple(-x for x in task.numerator)
    if not task.conditional:
        return LP(m.A,m.b,m.C,m.d,r)
    return LP(tuple(row+(-b,) for row,b in zip(m.A,m.b))+(task.event+(F(0),),),
              (F(0),)*len(m.A)+(F(1),), tuple(row+(-d,) for row,d in zip(m.C,m.d)),
              (F(0),)*len(m.C), r+(F(0),))


def feasible(L, p):
    return len(p) == len(L.objective) and all(x >= 0 for x in p) and all(dot(r,p) == b for r,b in zip(L.A,L.b)) and all(dot(r,p) <= d for r,d in zip(L.C,L.d))


def original_member(model, p):
    model.validate()
    L = LP(model.A,model.b,model.C,model.d,(F(0),)*len(model.atom_order))
    return feasible(L,p) and all(extra.holds(p) for extra in model.extra_original)


def recover(task, p):
    need(feasible(lp(task),p), 'not a feasible analyzed point')
    if task.conditional:
        need(p[-1] > 0, 'positive inverse scale required')
        x = tuple(v/p[-1] for v in p[:-1])
        need(dot(task.event,x) > 0, 'positive original event mass required')
        need(p[-1]*dot(task.event,x) == 1, 'inverse consistency')
        return x
    return p


def forward(task, x):
    need(original_member(task.model,x), 'original-model witness required')
    if not task.conditional:
        return x
    mass=dot(task.event,x)
    need(mass > 0, 'undefined conditioning')
    return tuple(v/mass for v in x)+(1/mass,)


@dataclass(frozen=True)
class Certificate:
    kind: str
    subject: Task
    point: tuple = ()
    y: tuple = ()
    z: tuple = ()
    signed_bound: F = F(0)


def consume(expected, cert):
    """Check a certificate against independently supplied intended mathematical subject.

    This checker never invokes the search procedure. Bounds alone do not certify
    nonemptiness. 'original' means all encoded premises, not empirical truth.
    """
    expected.validate()
    need(cert.subject == expected, 'subject_mismatch')
    need(cert.kind in ('witness','upper','optimum','infeasible'), 'certificate kind')
    for v in cert.point+cert.y+cert.z+(cert.signed_bound,):
        need(type(v) is F, 'rational certificate required')
    L=lp(expected)
    x=None
    original=False
    if cert.kind in ('witness','optimum'):
        x=recover(expected,cert.point)
        original=original_member(expected.model,x)
    if cert.kind in ('upper','optimum','infeasible'):
        need(len(cert.y)==len(L.A) and len(cert.z)==len(L.C), 'dual dimensions')
        need(all(v>=0 for v in cert.z), 'negative inequality multiplier')
        target=(F(0),)*len(L.objective) if cert.kind=='infeasible' else L.objective
        need(all(sum((cert.y[j]*L.A[j][i] for j in range(len(L.A))),F(0))+
                     sum((cert.z[j]*L.C[j][i] for j in range(len(L.C))),F(0))>=target[i]
                 for i in range(len(target))), 'dual dominance failure')
        bound=dot(L.b,cert.y)+dot(L.d,cert.z)
        need(bound==cert.signed_bound, 'bound value mismatch')
        if cert.kind=='infeasible':
            need(bound<0, 'Farkas strict sign required')
            return {'status':'no_eligible_original_model' if expected.conditional else 'original_infeasible',
                    'analyzed_domain':'outer' if expected.model.extra_original else 'exact'}
        if cert.kind=='optimum':
            need(dot(L.objective,cert.point)==bound, 'primal_dual_gap')
        value=bound if expected.direction=='max' else -bound
    else:
        value=dot(L.objective,cert.point)
        if expected.direction=='min': value=-value
    if cert.kind=='witness':
        return {'status':'original_attained' if original else 'outer_attained_only','value':value,'original_point':x}
    if cert.kind=='upper':
        return {'status':'bound_only_nonemptiness_unestablished','value':value,'direction':expected.direction}
    return {'status':'original_optimum' if original else 'outer_optimum_only','value':value,'original_point':x}


# Producer only: exact Gaussian elimination and finite active-set enumeration.
def solve_rows(rows, rhs, n):
    M=[list(row)+[b] for row,b in zip(rows,rhs)]
    k=0
    pivots=[]
    for j in range(n):
        hit=next((i for i in range(k,len(M)) if M[i][j]),None)
        if hit is None: continue
        M[k],M[hit]=M[hit],M[k]
        divisor=M[k][j]
        M[k]=[v/divisor for v in M[k]]
        for i in range(len(M)):
            if i!=k:
                factor=M[i][j]
                M[i]=[x-factor*y for x,y in zip(M[i],M[k])]
        pivots.append(j); k+=1
    if any(all(v==0 for v in row[:n]) and row[-1]!=0 for row in M): return k,None
    if k<n: return k,None
    result=[F(0)]*n
    for i,j in enumerate(pivots): result[j]=M[i][-1]
    return k,tuple(result)


def propose(task, max_bases=25000):
    """Return a checked matching primal/dual certificate or unfinished; never infer
    infeasibility from an empty vertex list. Supplied Farkas witnesses use consume.
    """
    L=lp(task); n=len(L.objective)
    need(type(max_bases) is int and 0<=max_bases<=25000,'basis budget limit')
    ids=[]; rank=0
    for j,row in enumerate(L.A):
        newrank,_=solve_rows([L.A[i] for i in ids]+[row],[F(0)]*(len(ids)+1),n)
        if newrank>rank: ids.append(j); rank=newrank
    equalities=[L.A[i] for i in ids]; rhs=[L.b[i] for i in ids]
    inequalities=list(L.C)+[tuple(-F(i==j) for i in range(n)) for j in range(n)]
    bounds=list(L.d)+[F(0)]*n
    tested=0
    for selected in combinations(range(len(inequalities)),n-rank):
        if tested==max_bases: return {'status':'unfinished','reason':'basis_budget','bases':tested}
        tested+=1
        active=equalities+[inequalities[i] for i in selected]
        _,p=solve_rows(active,rhs+[bounds[i] for i in selected],n)
        if p is None or not feasible(L,p): continue
        _,dual=solve_rows(list(zip(*active)),L.objective,n)
        if dual is None or any(v<0 for v in dual[rank:]): continue
        y=[F(0)]*len(L.A); z=[F(0)]*len(L.C)
        for i,v in zip(ids,dual[:rank]): y[i]=v
        for i,v in zip(selected,dual[rank:]):
            if i<len(L.C): z[i]=v
        cert=Certificate('optimum',task,p,tuple(y),tuple(z),dot(L.b,y)+dot(L.d,z))
        consume(task,cert)
        return {'status':'certificate','certificate':cert,'bases':tested}
    return {'status':'unfinished','reason':'no_checked_certificate','bases':tested}


def impossible_event(task, original_point, cert):
    need(task.conditional and cert.kind == 'infeasible', 'conditional infeasibility certificate required')
    need(original_member(task.model, original_point), 'original nonemptiness witness required')
    need(consume(task, cert)['status'] == 'no_eligible_original_model', 'eligible-domain check')
    return {'status': 'impossible_conditioning', 'original_nonempty': True}


def decide(task, action, original_point, pair_certificates):
    """Certify common optimality/strictness after this exact task's event."""
    forward(task,original_point)  # establishes original compatibility AND event support.
    labels=tuple(a for a,_ in task.actions)
    need(action in labels, 'unknown action')
    others=[a for a in labels if a!=action]
    need(set(pair_certificates)==set(others), 'all action comparisons required')
    uppers={}
    for other in others:
        comparison=difference(task,action,other)
        cert=pair_certificates[other]
        need(cert.kind in ('upper','optimum'), 'upper certificate needed')
        result=consume(comparison,cert)
        need(result['value']<=0, 'common optimum not certified')
        uppers[other]=result['value']
    strict=all(v<0 for v in uppers.values())
    return {'common_optimal_action':action,'uniformly_strict_against_other_actions':strict,
            'complete_minimizing_set':[action] if strict else None,'upper_differences':uppers}


def fixed_minimizing_set(task, selected, original_point, certificates):
    """All selected actions tied globally, representative strictly beats outsiders."""
    forward(task,original_point)
    labels={a for a,_ in task.actions}
    need(bool(selected) and len(set(selected))==len(selected) and set(selected)<=labels,'selected action set')
    representative=selected[0]
    required={(representative,a) for a in labels if a!=representative}
    required|={(a,representative) for a in selected if a!=representative}
    need(set(certificates)==required,'exact comparison coverage')
    for a,b in required:
        cert=certificates[a,b]
        need(cert.kind in ('upper','optimum'),'upper certificate needed')
        upper=consume(difference(task,a,b),cert)['value']
        need(upper<=0 if b in selected else upper<0,'minimizer-set comparison fails')
    return {'complete_minimizing_set':list(selected)}


def wire(x):
    if isinstance(x,F): return str(x.numerator)+'/'+str(x.denominator)
    if hasattr(x,'__dataclass_fields__'): return wire(asdict(x))
    if isinstance(x,dict): return {str(k):wire(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [wire(v) for v in x]
    return x
