"""A fixed two-player evidence/bond game; no inference of empirical premises."""
from fractions import Fraction as F
from copy import deepcopy
from subject import structure, reach

def fixture(bond=6,fee=F(0),gain_values=(1,3),detect_values=(F(1,2),F(1))):
    nodes={}; profile={}; model_data={}
    def add(v,kind,**kw): nodes[v]={'kind':kind,**kw}
    def player(v,i,I,edges,chosen):
        add(v,'player',player=i,info=I,edges=edges)
        row={a:str(int(a==chosen)) for a in edges}
        if I in profile and profile[I]!=row: raise ValueError('inconsistent fixture')
        profile[I]=row
    add('root','chance',edges={'good':'disclose.good','bad':'disclose.bad'})
    for t in ('good','bad'):
        evidence='G' if t=='good' else 'B'
        player('disclose.'+t,'A','disclose.'+t,{evidence:f'bond.{t}.{evidence}','N':f'bond.{t}.N'},evidence)
        for msg in (evidence,'N'):
            v=f'bond.{t}.{msg}'
            player(v,'A',v,{b:f'receive.{t}.{msg}.{b}' for b in ('zero','bond')},'bond' if msg=='G' else 'zero')
            for b in ('zero','bond'):
                r=f'receive.{t}.{msg}.{b}'
                I=f'receive.{msg}.{b}'
                player(r,'B',I,{'accept':f'act.{t}.{msg}.{b}','reject':f'reject.{t}.{msg}.{b}'},'accept' if msg=='G' and b=='bond' else 'reject')
                add(f'reject.{t}.{msg}.{b}','terminal')
                player(f'act.{t}.{msg}.{b}','A',f'act.{t}.{msg}.{b}',{'comply':f'comply.{t}.{msg}.{b}','defect':f'monitor.{t}.{msg}.{b}'},'comply' if b=='bond' else 'defect')
                add(f'comply.{t}.{msg}.{b}','terminal')
                add(f'monitor.{t}.{msg}.{b}','chance',edges={d:f'{d}.{t}.{msg}.{b}' for d in ('caught','missed')})
                for d in ('caught','missed'): add(f'{d}.{t}.{msg}.{b}','terminal')
    for g in gain_values:
        for p in detect_values:
            name=f'g={g},p={p}'
            chance={'root':{'good':'1/2','bad':'1/2'}}
            payoffs={}
            for v,n in nodes.items():
                if v.startswith('monitor.'):
                    chance[v]={'caught':str(p),'missed':str(1-p)}
                if n['kind']!='terminal': continue
                outcome,t,msg,b=v.split('.')
                amount=F(bond) if b=='bond' else F(0)
                cost=amount/10
                if outcome=='reject': a,z=-cost,F(0)
                elif outcome=='comply': a,z=2-cost-fee,F(2 if t=='good' else -1)
                else: a,z=2+F(g)-cost-fee-(amount if outcome=='caught' else 0),F(-2)
                payoffs[v]={'A':str(a),'B':str(z)}
            model_data[name]={'chance':chance,'payoffs':payoffs,'beliefs':{}}
    s={'schema':'bellman.assessed-credibility.v1','root':'root','nodes':nodes,'models':model_data,'profile':profile}
    # Structure uses belief distributions; initialize support before the Bayes pass.
    groups={}
    for v,n in nodes.items():
        if n['kind']=='player': groups.setdefault(n['info'],[]).append(v)
    for m in model_data.values():
        r=reach(s,m)
        for I,vs in groups.items():
            total=sum(r[v] for v in vs)
            if total: d={v:str(r[v]/total) for v in vs}
            else:
                chosen=next((v for v in vs if '.bad.' in v),vs[0])
                d={v:str(int(v==chosen)) for v in vs}
            m['beliefs'][I]=d
    structure(s)
    return s

def renamed(s):
    out=deepcopy(s)
    mapping={v:'node'+str(j) for j,v in enumerate(sorted(s['nodes']))}
    imap={I:'info'+str(j) for j,I in enumerate(sorted(s['profile']))}
    out['root']=mapping[s['root']]
    out['nodes']={mapping[v]:deepcopy(n) for v,n in s['nodes'].items()}
    for n in out['nodes'].values():
        if 'edges' in n: n['edges']={a:mapping[z] for a,z in n['edges'].items()}
        if 'info' in n: n['info']=imap[n['info']]
    out['profile']={imap[I]:v for I,v in out['profile'].items()}
    for m in out['models'].values():
        m['chance']={mapping[v]:d for v,d in m['chance'].items()}
        m['payoffs']={mapping[v]:d for v,d in m['payoffs'].items()}
        m['beliefs']={imap[I]:{mapping[v]:p for v,p in d.items()} for I,d in m['beliefs'].items()}
    return out
