"""Explicit public-copy quotient validation; identities are supplied, not guessed."""
from copy import deepcopy
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'sequential_consistency'))
from witness import validate, rational, digest, demand

SCHEMA='bellman.public-tag-erasure.v1'

def verify_map(source,target,q):
    si,ti=validate(source),validate(target)
    demand(type(q) is dict and set(q)=={'schema','representative','nodes','infos'},'reduction-schema')
    demand(q['schema']==SCHEMA,'reduction-semantics')
    root=source['nodes'][source['root']]
    demand(root['kind']=='chance','unsupported-reduction-root')
    tags=set(root['edges'])
    demand(2<=len(tags)<=4,'unsupported-tag-count')
    demand(q['representative'] in tags,'representative-tag')
    demand(type(q['nodes']) is dict and type(q['infos']) is dict and set(q['nodes'])==tags and set(q['infos'])==tags,'tag-coverage')
    demand(set(source['models'])==set(target['models']),'model-identity')
    allnodes=set();allinfos=set()
    for tag in sorted(tags):
        subtree=set();todo=[root['edges'][tag]]
        while todo:
            v=todo.pop();subtree.add(v);todo.extend(source['nodes'][v].get('edges',{}).values())
        nm,im=q['nodes'][tag],q['infos'][tag]
        localinfos={source['nodes'][v]['info'] for v in subtree if source['nodes'][v]['kind']=='player'}
        demand(type(nm) is dict and set(nm)==subtree and len(nm)==len(target['nodes']) and set(nm.values())==set(target['nodes']),'node-bijection')
        demand(type(im) is dict and set(im)==localinfos and len(im)==len(ti) and set(im.values())==set(ti),'information-bijection')
        demand(not allnodes.intersection(subtree) and not allinfos.intersection(localinfos),'tag-not-public')
        allnodes.update(subtree);allinfos.update(localinfos)
        demand(nm[root['edges'][tag]]==target['root'],'copy-root')
        for v,tv in nm.items():
            sn,tn=source['nodes'][v],target['nodes'][tv]
            demand(sn['kind']==tn['kind'],'node-role')
            if sn['kind']!='terminal':
                demand({a:nm[z] for a,z in sn['edges'].items()}==tn['edges'],'action-edge-map')
            if sn['kind']=='player':
                demand(sn['player']==tn['player'] and im[sn['info']]==tn['info'],'player-information-map')
        for I,J in im.items():
            demand(source['profile'][I]==target['profile'][J],'profile-not-invariant')
            demand({nm[v] for v in si[I]['nodes']}==set(ti[J]['nodes']),'information-node-map')
        for name,sm in source['models'].items():
            tm=target['models'][name]
            demand(rational(sm['chance'][source['root']][tag])>0,'unsupported-zero-tag')
            for v,tv in nm.items():
                n=source['nodes'][v]
                if n['kind']=='chance': demand(sm['chance'][v]==tm['chance'][tv],'conditional-chance-mismatch')
                if n['kind']=='terminal': demand(sm['payoffs'][v]==tm['payoffs'][tv],'payoff-mismatch')
            for I,J in im.items():
                demand({nm[v]:p for v,p in sm['beliefs'][I].items()}==tm['beliefs'][J],'assessment-not-invariant')
    demand(allnodes==set(source['nodes'])-{source['root']} and allinfos==set(si),'incomplete-reduction')
    return si,ti

def restrict(w,q):
    return {J:deepcopy(w[I]) for I,J in q['infos'][q['representative']].items()}
