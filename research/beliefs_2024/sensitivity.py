"""Predeclared prior ranges and labelled investigation of first utility sensitivity.

HiGHS proposes simplex witnesses. Exact rational primal/dual inequalities enclose
extrema for retained value vectors. No fitting, target tuning or raw-row retention.
"""
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog
from scipy.special import expit

from analyze import features, design, session_metrics, uncertainty, INDEX
from reconstruct import read_source, need
from receiver import residual_bounds

HERE=Path(__file__).resolve().parent


def simplex(numbers):
    values=[F(str(max(0,float(x)))) for x in numbers]
    total=sum(values); need(total>0,'empty LP witness')
    return [x/total for x in values]


def dot(a,b): return sum(x*y for x,y in zip(a,b))


def solve_range(matrix,actions):
    K=matrix.shape[1]; C=[j for j,a in enumerate(actions) if a==1]; D=[j for j,a in enumerate(actions) if a==0]
    exact=[[F(str(x)) for x in row] for row in matrix.tolist()]
    maxima=[]; minima=[]
    for side,indices,opposites in [('max',C,D),('min',D,C)]:
        for index in indices:
            differences=[matrix[index]-matrix[other] if side=='max' else matrix[other]-matrix[index] for other in opposites]
            diffs=[[exact[index][k]-exact[other][k] if side=='max' else exact[other][k]-exact[index][k] for k in range(K)] for other in opposites]
            sign=1 if side=='max' else -1
            objective=np.r_[np.zeros(K),-sign]
            constraints=np.array([np.r_[-sign*d,sign] for d in differences])
            fit=linprog(objective,A_ub=constraints,b_ub=np.zeros(len(opposites)),
                A_eq=[np.r_[np.ones(K),0]],b_eq=[1],bounds=[(0,None)]*K+[(None,None)],method='highs')
            need(fit.success,'LP unresolved: '+fit.message)
            w=simplex(fit.x[:K]); dual=simplex(-fit.ineqlin.marginals)
            primal_values=[dot(w,d) for d in diffs]
            dual_values=[sum(dual[l]*d[k] for l,d in enumerate(diffs)) for k in range(K)]
            lower,upper=(min(primal_values),max(dual_values)) if side=='max' else (min(dual_values),max(primal_values))
            need(lower<=upper,'invalid weak duality')
            certificate={'plan':index,'posterior':[str(x) for x in w],'dual':[str(x) for x in dual],
                         'lower':str(lower),'upper':str(upper)}
            (maxima if side=='max' else minima).append(certificate)
    lo=[min(F(c['lower']) for c in minima),min(F(c['upper']) for c in minima)]
    hi=[max(F(c['lower']) for c in maxima),max(F(c['upper']) for c in maxima)]
    need(max(lo[1]-lo[0],hi[1]-hi[0])<F(1,10**8),'LP enclosure insufficiently tight')
    return {'minimum_enclosure':list(map(str,lo)),'maximum_enclosure':list(map(str,hi)),
            'max_certificates':maxima,'min_certificates':minima}


def run(raw,out):
    out=Path(out); need(not out.exists(),'preserve previous sensitivity evidence'); out.mkdir()
    bundles=json.loads((HERE/'first-results/parameters.json').read_text())
    bundle=bundles['ten-linear']; autos=bundle['mixture']['automata']; tables=bundle['values']
    df=read_source(raw); target=df[df.treatment.isin([3,4])&df.supergame.ge(5)&df['round'].le(8)]
    signatures={}; queries=[]
    for _,game in target.groupby(['session','id','supergame']):
        own=[0]*len(autos); other=[0]*len(autos); past=[]
        for r in game.sort_values('round').itertuples():
            if past:
                signature=(tuple(own),tuple(other))
                if signature not in signatures: signatures[signature]=len(signatures)
                queries.append({'session':r.session,'treatment':r.treatment,'state':signatures[signature],
                    'shift':bundle['response']['coefficients'][0]+bundle['response']['coefficients'][2]*past[-1][0]+
                       bundle['response']['coefficients'][3]*past[-1][2]+bundle['response']['coefficients'][4]*(r.round-2)/6})
            for k,a in enumerate(autos):
                own[k]=a['transitions'][own[k]][INDEX[r.coop,r.o_coop]]
                other[k]=a['transitions'][other[k]][INDEX[r.o_coop,r.coop]]
            past.append((r.coop,r.o_coop,r.belief))
    states=[]
    for (own,other),index in signatures.items():
        entry={'id':index,'own_states':list(own),'opponent_states':list(other),'treatments':{}}
        actions=[a['outputs'][own[j]] for j,a in enumerate(autos)]
        for treatment,table in tables.items():
            matrix=np.array([[table[j][k][own[j]][other[k]] for k in range(len(autos))] for j in range(len(autos))])
            entry['treatments'][treatment]=solve_range(matrix,actions)
        states.append(entry)
    E=F(residual_bounds(bundle)['exact_value_error_bound']); b=bundle['response']['coefficients'][1]
    session_ranges={}
    for session in sorted({q['session'] for q in queries}):
        selected=[q for q in queries if q['session']==session]; lows=[]; highs=[]
        for q in selected:
            enclosure=states[q['state']]['treatments'][str(q['treatment'])]
            lower=F(enclosure['minimum_enclosure'][0])-2*E
            upper=F(enclosure['maximum_enclosure'][1])+2*E
            lows.append(float(expit(q['shift']+b*float(lower))))
            highs.append(float(expit(q['shift']+b*float(upper))))
        session_ranges[str(session)]={'n':len(selected),'mean_probability_outer':[float(np.mean(lows)),float(np.mean(highs))]}
    # Feasible shared priors, not independently chosen posterior extrema. No refitting.
    shared={}
    for k,name in enumerate(bundle['mixture']['names']):
        mix=copy.deepcopy(bundle['mixture']); mix['prior']=[float(j==k) for j in range(len(autos))]
        rows=features(target,mix,{int(t):v for t,v in tables.items()})
        beta=bundle['response']['coefficients']
        pred={'fixed':expit(design(rows,'candidate')@beta),'updated':expit(design(rows,'candidate',True)@beta)}
        metrics=session_metrics(rows,pred)
        shared[name]={'sessions':metrics,'comparison':uncertainty(metrics)}
    # Labelled explanation of already observed sensitivity; all fits remain frozen.
    utilities={}
    for label,par in bundles.items():
        rows=features(target,par['mixture'],{int(t):v for t,v in par['values'].items()})
        beta=par['response']['coefficients']; utility_arms={}
        for treatment in (3,4):
            session_stats=[]
            for session in sorted({r['key'][0] for r in rows if r['treatment']==treatment}):
                subset=[r for r in rows if r['key'][0]==session]
                ds=np.array([r['d'][treatment]-r['d'][2] for r in subset])
                fixed=expit(design(subset,'candidate')@beta); updated=expit(design(subset,'candidate',True)@beta)
                session_stats.append({'session':session,'mean_score_change':float(ds.mean()),
                    'mean_logit_change':float(beta[1]*ds.mean()),'mean_probability_change':float((updated-fixed).mean()),
                    'positive_score_changes':int(sum(ds>1e-12)),'negative_score_changes':int(sum(ds< -1e-12)),'n':len(ds)})
            utility_arms[str(treatment)]=session_stats
        utilities[label]={'b':beta[1],'arms':utility_arms}
    result={'schema':'bellman.afy2024.prior-sensitivity.v1','parameter_edition':'f541369',
        'states':states,'target_queries':len(queries),'exact_value_error_bound':str(E),
        'session_response_outer_ranges':session_ranges,'shared_pure_priors':shared,
        'utility_investigation':utilities,
        'scope':'exact primal/dual enclosures for rounded value vectors, enlarged by exact Markov residual bound; session probability ranges are outer for a shared prior; pure-prior contrasts are feasible witnesses, not full prior extrema; no target fitting'}
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'states':len(states),'queries':len(queries),'shared_prior_deltas':{k:v['comparison']['delta_brier'] for k,v in shared.items()}},indent=2))


if __name__=='__main__': run(*sys.argv[1:])
