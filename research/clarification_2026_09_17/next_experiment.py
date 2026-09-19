"""Prepared next experiment; not run in the clarification goal. Requires --run."""
from collections import deque
from itertools import product, combinations
import json
import sys
from probes import RULES, family, signature

LABELS = tuple(RULES)
STATES = tuple(product(range(1 << len(LABELS)), (None, 0, 1)))
OPS = tuple((op,j) for op in ('add','drop') for j in range(len(LABELS))) + (('replace',0),('replace',1))


def active(e):
    return {label for i,label in enumerate(LABELS) if e[0] & (1 << i)}


def obs(e):
    return tuple(sorted({signature(m,e[1]) for m in family(active(e))}))


def models(e):
    return tuple(sorted({(a,b if e[1] is None else e[1],c) for a,b,c in family(active(e))}))


def step(e,op):
    kind,j=op
    if kind=='add': return (e[0] | (1 << j),e[1])
    if kind=='drop': return (e[0] & ~(1 << j),e[1])
    return (e[0],j)


def partition(key):
    seen={}
    return {e:seen.setdefault(key(e),len(seen)) for e in STATES}


def witness(p):
    for e,d in combinations(STATES,2):
        if p[e]!=p[d]: continue
        pending=deque([(e,d,[])])
        visited=set()
        while pending:
            x,y,trace=pending.popleft()
            if (x,y) in visited: continue
            visited.add((x,y))
            if obs(x)!=obs(y):
                return {'initial':[e,d],'trace':trace,'final_answers':[obs(x),obs(y)]}
            for op in OPS:
                pending.append((step(x,op),step(y,op),trace+[op]))
    return None


def main():
    if sys.argv[1:] != ['--run']:
        raise SystemExit('Prepared, not executed. Read EXPERIMENT_SPEC.md; pass --run to execute.')
    p=partition(obs)
    rounds=0
    while True:
        new=partition(lambda e:(p[e],tuple(p[step(e,op)] for op in OPS)))
        if all((p[x]==p[y])==(new[x]==new[y]) for x,y in combinations(STATES,2)):
            p=new
            break
        p=new
        rounds+=1
        if rounds>95: raise AssertionError('refinement bound')
    # Independent conformance check of the induction premises.
    for x,y in combinations(STATES,2):
        if p[x]==p[y]:
            if obs(x)!=obs(y): raise AssertionError('observation mismatch')
            if any(p[step(x,op)]!=p[step(y,op)] for op in OPS):
                raise AssertionError('transition mismatch')
    result={'state_count':len(STATES),'operations':OPS,'strict_refinement_rounds':rounds,
            'candidates':{}}
    for name,q in [('answer_only',partition(obs)),('family_only',partition(models)),('operation_stable',p)]:
        result['candidates'][name]={'block_count':len(set(q.values())),
            'blocks':[[e for e in STATES if q[e]==i] for i in sorted(set(q.values()))],
            'separating_trace':None if name=='operation_stable' else witness(q)}
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
