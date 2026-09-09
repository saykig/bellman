"""Candidate producer: recursive conditional utility evaluation."""
from fractions import Fraction as F
from subject import validate, plans, rational, digest, require

def value(s,m,v,player,plan):
    n=s['nodes'][v]
    if n['kind']=='terminal': return rational(m['payoffs'][v][player])
    if n['kind']=='player' and n['player']==player and n['info'] in plan:
        return value(s,m,n['edges'][plan[n['info']]],player,plan)
    d=m['chance'][v] if n['kind']=='chance' else s['profile'][n['info']]
    return sum((rational(d[a])*value(s,m,w,player,plan) for a,w in n['edges'].items()),F(0))

def produce(s, epsilon='0'):
    eps=rational(epsilon)
    require(eps>=0, 'negative epsilon')
    infos=validate(s)
    rows=[]
    for name,m in sorted(s['models'].items()):
        for I,x in sorted(infos.items()):
            player=x['signature'][0]
            def cond(plan):
                return sum((rational(m['beliefs'][I][v])*value(s,m,v,player,plan) for v in x['nodes']),F(0))
            baseline=cond({})
            best=None
            winner=None
            count=0
            for plan in plans(s,infos,I):
                count+=1
                u=cond(plan)
                if best is None or u>best:
                    best,winner=u,plan
            rows.append({'model':name,'info':I,'baseline':str(baseline),'best':str(best),'gain':str(best-baseline),'witness':winner,'plans':count})
    maximum=max(rational(r['gain']) for r in rows)
    return {'schema':'bellman.assessed-credibility-certificate.v1','subject_sha256':digest(s),'epsilon':epsilon,'status':'assessment-relative-pass' if maximum<=eps else 'profitable-deviation','max_gain':str(maximum),'rows':rows}
