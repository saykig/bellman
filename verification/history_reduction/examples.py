"""Public-copy construction and two exact unsafe-erasure examples."""
from copy import deepcopy
from reduction import SCHEMA
from cases import evidence_case,modelwise_not_shared,unit_witness


def expand(target,w,weights=None):
    tags=('red','blue')
    s={'schema':target['schema'],'root':'public-tag','nodes':{},'profile':{},'models':{}}
    s['nodes']['public-tag']={'kind':'chance','edges':{z:z+'/'+target['root'] for z in tags}}
    q={'schema':SCHEMA,'representative':'red','nodes':{},'infos':{}}
    sw={}
    for z in tags:
        q['nodes'][z]={z+'/'+v:v for v in target['nodes']}
        q['infos'][z]={z+'/'+I:I for I in target['profile']}
        for v,node in target['nodes'].items():
            n=deepcopy(node)
            if 'edges' in n:n['edges']={a:z+'/'+child for a,child in n['edges'].items()}
            if 'info' in n:n['info']=z+'/'+n['info']
            s['nodes'][z+'/'+v]=n
        for I,row in target['profile'].items():
            s['profile'][z+'/'+I]=deepcopy(row);sw[z+'/'+I]=deepcopy(w[I])
    for name,m in target['models'].items():
        sm={'chance':{'public-tag':deepcopy(weights[name] if weights else {'red':'1/3','blue':'2/3'})},'payoffs':{},'beliefs':{}}
        for z in tags:
            for v,row in m['chance'].items():sm['chance'][z+'/'+v]=deepcopy(row)
            for v,row in m['payoffs'].items():sm['payoffs'][z+'/'+v]=deepcopy(row)
            for I,row in m['beliefs'].items():sm['beliefs'][z+'/'+I]={z+'/'+v:p for v,p in row.items()}
        s['models'][name]=sm
    return s,q,sw


def matching():
    nodes={'root':{'kind':'player','player':'A','info':'A','edges':{a:'B.'+a for a in ('L','R')}}}
    payoff={}
    for a in ('L','R'):
        nodes['B.'+a]={'kind':'player','player':'B','info':'B','edges':{b:a+b for b in ('L','R')}}
        for b in ('L','R'):
            nodes[a+b]={'kind':'terminal'};payoff[a+b]={'A':str(int(a==b)),'B':str(int(a==b))}
    target={'schema':'bellman.assessed-credibility.v1','root':'root','nodes':nodes,
            'profile':{'A':{'L':'1/2','R':'1/2'},'B':{'L':'1/2','R':'1/2'}},
            'models':{'m':{'chance':{},'payoffs':payoff,'beliefs':{'A':{'root':'1'},'B':{'B.L':'1/2','B.R':'1/2'}}}}}
    source,q,w=expand(target,unit_witness(target),{'m':{'red':'1/2','blue':'1/2'}})
    for z,chosen in (('red','L'),('blue','R')):
        for I in ('A','B'):source['profile'][z+'/'+I]={a:str(int(a==chosen)) for a in ('L','R')}
        source['models']['m']['beliefs'][z+'/B']={z+'/B.'+a:str(int(a==chosen)) for a in ('L','R')}
    return source,target,q,unit_witness(source)


def likelihood():
    target=modelwise_not_shared();del target['models']['quarter']
    source,q,w=expand(target,unit_witness(target),{'half':{'red':'1/2','blue':'1/2'}})
    for z,g,b,cg,cb in [('red','3/4','1/4','1','3'),('blue','1/4','3/4','3','1')]:
        source['models']['half']['chance'][z+'/root']={'g':g,'b':b}
        w[z+'/A.g']['enter']['coefficient']=cg;w[z+'/A.b']['enter']['coefficient']=cb
    return source,target,q,w
