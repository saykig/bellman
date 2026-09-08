"""Trusted exact subject validation and identity; no candidate-bound calculation."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json

class Invalid(ValueError):
    pass

def require(ok, message):
    if not ok:
        raise Invalid(message)

def rational(x):
    require(type(x) is str, 'rational must be a string')
    try:
        q = F(x)
    except (ValueError, ZeroDivisionError):
        raise Invalid('invalid rational') from None
    require(str(q) == x, 'rational must be canonical')
    return q

def digest(s):
    return sha256(json.dumps(s, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def dist(d, keys):
    require(type(d) is dict and set(d) == set(keys), 'distribution support mismatch')
    qs = {k: rational(v) for k, v in d.items()}
    require(all(v >= 0 for v in qs.values()) and sum(qs.values()) == 1, 'invalid distribution')
    return qs

def structure(s):
    require(type(s) is dict and set(s) == {'schema','root','nodes','models','profile'}, 'subject schema')
    require(s['schema'] == 'bellman.assessed-credibility.v1', 'unsupported schema')
    nodes, models, profile = s['nodes'], s['models'], s['profile']
    require(type(nodes) is dict and nodes and len(nodes) <= 300, 'unsupported node count')
    require(type(models) is dict and 0 < len(models) <= 16, 'unsupported model count')
    require(all(type(x) is str for x in nodes) and s['root'] in nodes, 'node identity')
    infos, seen, parents = {}, set(), {}
    def visit(v, memories, depth):
        require(depth <= 24 and v not in seen, 'not a bounded rooted tree')
        seen.add(v)
        n = nodes[v]
        require(type(n) is dict and 'kind' in n, 'node shape')
        if n['kind'] == 'terminal':
            require(set(n) == {'kind'}, 'terminal shape')
            return
        if n['kind'] == 'chance':
            require(set(n) == {'kind','edges'}, 'chance shape')
        else:
            require(n['kind'] == 'player' and set(n) == {'kind','edges','player','info'}, 'player shape')
            i, I = n['player'], n['info']
            require(i in ('A','B') and type(I) is str, 'player/info identity')
            sig = (i, tuple(sorted(n['edges'])), tuple(memories[i]))
            if I in infos:
                require(infos[I]['signature'] == sig, 'action/owner/perfect-recall mismatch')
            else:
                infos[I] = {'signature': sig, 'nodes': []}
            infos[I]['nodes'].append(v)
        require(type(n['edges']) is dict and 0 < len(n['edges']) <= 4, 'action count')
        for a,w in n['edges'].items():
            require(type(a) is str and type(w) is str and w in nodes, 'edge identity')
            mm = {i: list(h) for i,h in memories.items()}
            if n['kind'] == 'player':
                mm[n['player']].append((n['info'],a))
            parents[w] = (v,a)
            visit(w,mm,depth+1)
    visit(s['root'], {'A': [], 'B': []}, 0)
    require(seen == set(nodes), 'disconnected nodes')
    require(bool(infos), 'unsupported game without player decisions')
    require(type(profile) is dict and set(profile) == set(infos), 'profile information coverage')
    for I,x in infos.items():
        dist(profile[I], x['signature'][1])
    terminals = {v for v,n in nodes.items() if n['kind']=='terminal'}
    chances = {v for v,n in nodes.items() if n['kind']=='chance'}
    for name,m in models.items():
        require(type(name) is str and type(m) is dict and set(m)=={'chance','payoffs','beliefs'}, 'model schema')
        require(type(m['chance']) is dict and set(m['chance'])==chances, 'chance coverage')
        require(type(m['payoffs']) is dict and set(m['payoffs'])==terminals, 'payoff coverage')
        for v in chances:
            dist(m['chance'][v], nodes[v]['edges'])
        for v in terminals:
            require(type(m['payoffs'][v]) is dict and set(m['payoffs'][v])=={'A','B'}, 'utility coverage')
            for z in m['payoffs'][v].values(): rational(z)
        require(type(m['beliefs']) is dict and set(m['beliefs'])==set(infos), 'assessment coverage')
        for I,x in infos.items(): dist(m['beliefs'][I], x['nodes'])
    return infos

def reach(s,m):
    masses = {}
    def go(v,w):
        masses[v] = w
        n=s['nodes'][v]
        if n['kind']=='terminal': return
        d=m['chance'][v] if n['kind']=='chance' else s['profile'][n['info']]
        for a,z in n['edges'].items(): go(z,w*rational(d[a]))
    go(s['root'],F(1))
    return masses

def validate(s):
    infos = structure(s)
    for m in s['models'].values():
        r = reach(s,m)
        for I,x in infos.items():
            total = sum(r[v] for v in x['nodes'])
            if total:
                require(all(rational(m['beliefs'][I][v]) == r[v]/total for v in x['nodes']), 'on-path Bayes mismatch')
    return infos

def plans(s, infos, I):
    player=infos[I]['signature'][0]
    choices={}
    def collect(v):
        n=s['nodes'][v]
        if n['kind']=='terminal': return
        if n['kind']=='player' and n['player']==player:
            choices[n['info']] = tuple(sorted(n['edges']))
        for w in n['edges'].values(): collect(w)
    for v in infos[I]['nodes']: collect(v)
    ordered=sorted(choices)
    size=1
    for J in ordered: size *= len(choices[J])
    require(size <= 4096, 'unsupported continuation count')
    for acts in product(*(choices[J] for J in ordered)):
        yield dict(zip(ordered,acts))
