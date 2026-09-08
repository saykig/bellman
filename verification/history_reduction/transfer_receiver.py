"""Independent map/warrant receiving; no candidate-constructor import."""
import json
import sys
from reduction import verify_map,restrict,digest,demand
from consistency_receiver import receive as consistent_receive
from receiver import paths


def receive(source,target,c,epsilon='0'):
    demand(type(c) is dict and set(c)=={'schema','source_sha256','target_sha256','reduction','source_warrant','target_warrant'},'transfer-warrant-schema')
    demand(c['schema']=='bellman.public-tag-erasure-warrant.v1','transfer-semantics')
    demand(c['source_sha256']==digest(source) and c['target_sha256']==digest(target),'stale-transfer-subject')
    q=c['reduction'];verify_map(source,target,q)
    sr=consistent_receive(source,c['source_warrant'],epsilon)
    tr=consistent_receive(target,c['target_warrant'],epsilon)
    demand(c['target_warrant']['witness']==restrict(c['source_warrant']['witness'],q),'wrong-witness-restriction')
    targetrows={(r['model'],r['info']):r for r in c['target_warrant']['incentives']['rows']}
    sourceinfo={I:J for im in q['infos'].values() for I,J in im.items()}
    for r in c['source_warrant']['incentives']['rows']:
        t=targetrows[(r['model'],sourceinfo[r['info']])]
        demand(all(r[k]==t[k] for k in ('baseline','best','gain','plans')),'continuation-not-preserved')
    root_values={}
    for name,m in source['models'].items():
        root_values[name]={}
        for player in ('A','B'):
            sv=paths(source,m,source['root'],player,{})
            tv=paths(target,target['models'][name],target['root'],player,{})
            demand(sv==tv,'root-value-not-preserved')
            root_values[name][player]=str(tv)
    demand(sr['max_gain']==tr['max_gain'] and sr['status']==tr['status'],'guarantee-not-preserved')
    return {'status':'checked-public-tag-erasure','equilibrium_status':tr['status'],
            'epsilon':epsilon,'max_gain':tr['max_gain'],
            'source_nodes':len(source['nodes']),'target_nodes':len(target['nodes']),
            'source_queries':sr['information_queries'],'target_queries':tr['information_queries'],
            'root_values':root_values,'source_sha256':digest(source),'target_sha256':digest(target),
            'warrant_sha256':digest(c)}

if __name__=='__main__':
    with open(sys.argv[1]) as f: source=json.load(f)
    with open(sys.argv[2]) as f: target=json.load(f)
    with open(sys.argv[3]) as f: c=json.load(f)
    print(json.dumps(receive(source,target,c,sys.argv[4] if len(sys.argv)>4 else '0'),sort_keys=True))
