"""Receiving needs no producer. Evaluates explicit terminal paths iteratively."""
from fractions import Fraction as F
from itertools import product
import json
import sys
from subject import validate, rational, digest, require

def paths(s,m,start,player,plan):
    stack=[(start,F(1))]
    answer=F(0)
    while stack:
        v,w=stack.pop()
        n=s['nodes'][v]
        if n['kind']=='terminal':
            answer+=w*rational(m['payoffs'][v][player])
            continue
        for a,z in n['edges'].items():
            if n['kind']=='chance': p=rational(m['chance'][v][a])
            elif n['player']==player and n['info'] in plan: p=F(int(plan[n['info']]==a))
            else: p=rational(s['profile'][n['info']][a])
            stack.append((z,w*p))
    return answer

def receive(s,c,expected_epsilon='0'):
    infos=validate(s)
    require(type(c) is dict and set(c)=={'schema','subject_sha256','epsilon','status','max_gain','rows'}, 'certificate schema')
    require(c['schema']=='bellman.assessed-credibility-certificate.v1' and c['subject_sha256']==digest(s), 'stale subject')
    require(c['epsilon']==expected_epsilon, 'query epsilon mismatch')
    eps=rational(c['epsilon'])
    require(eps>=0,'negative epsilon')
    require(type(c['rows']) is list and len(c['rows'])==len(infos)*len(s['models']), 'incomplete certificate')
    entries={}
    for row in c['rows']:
        require(type(row) is dict and set(row)=={'model','info','baseline','best','gain','witness','plans'},'row schema')
        key=(row['model'],row['info'])
        require(key not in entries and key[0] in s['models'] and key[1] in infos,'duplicate/unknown row')
        entries[key]=row
    maximum=F(0)
    for name,m in s['models'].items():
        for I,x in infos.items():
            row=entries[(name,I)]
            player=x['signature'][0]
            reachable=set()
            frontier=list(x['nodes'])
            while frontier:
                v=frontier.pop()
                reachable.add(v)
                frontier.extend(s['nodes'][v].get('edges',{}).values())
            Is=sorted({s['nodes'][v]['info'] for v in reachable if s['nodes'][v]['kind']=='player' and s['nodes'][v]['player']==player})
            menus=[infos[J]['signature'][1] for J in Is]
            size=1
            for menu in menus: size*=len(menu)
            require(size<=4096,'unsupported continuation count')
            def evaluate(plan):
                return sum((rational(m['beliefs'][I][v])*paths(s,m,v,player,plan) for v in x['nodes']),F(0))
            base=evaluate({})
            best=max(evaluate(dict(zip(Is,actions))) for actions in product(*menus))
            witness=row['witness']
            require(type(witness) is dict and set(witness)==set(Is),'witness information coverage')
            require(all(witness[J] in infos[J]['signature'][1] for J in Is),'illegal witness action')
            require(evaluate(witness)==best,'witness not maximizing')
            require(type(row['plans']) is int and row['plans']==size,'plan coverage')
            require(rational(row['baseline'])==base and rational(row['best'])==best and rational(row['gain'])==best-base,'false value/bound')
            maximum=max(maximum,best-base)
    require(rational(c['max_gain'])==maximum,'false maximum')
    expected='assessment-relative-pass' if maximum<=eps else 'profitable-deviation'
    require(c['status']==expected,'false result status')
    return {'status':expected,'max_gain':str(maximum),'rows':len(entries),'subject_sha256':digest(s)}

if __name__=='__main__':
    with open(sys.argv[1]) as f: s=json.load(f)
    with open(sys.argv[2]) as f: c=json.load(f)
    print(json.dumps(receive(s,c,sys.argv[3] if len(sys.argv)>3 else '0'),sort_keys=True))
