"""Declared AFY challenge producer. No raw outcome or report columns are retained.

Inputs: independently acquired source, directory of four source-only stratEst fits,
and a new output directory. Reusing an output directory is rejected.
"""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, logsumexp
from scipy.stats import t as student_t

from reconstruct import read_source, reconstruct, need

SPEC = '4abea07'
PAIRS = [(1, 1), (1, 0), (0, 1), (0, 0)]
INDEX = {pair: i for i, pair in enumerate(PAIRS)}
TAUS = [0, .001, .01, .1]


def load_fit(directory):
    directory = Path(directory)
    with (directory/'shares.csv').open() as f:
        reader = csv.reader(f); names = next(reader)[1:]; shares = np.array(next(reader)[1:], float)
    with (directory/'trembles.csv').open() as f:
        reader = csv.reader(f); next(reader); noises = np.array([row[1] for row in reader], float)
    need(np.ptp(noises) < 1e-12, 'non-global noise')
    automata = []
    for name in names:
        with (directory/f'automaton-{name}.csv').open() as f:
            rows = list(csv.DictReader(f))
        outputs = [int(row['prob.c']) for row in rows]
        transitions = [[int(row[f'tr({a}{b})'])-1 for a,b in [('c','c'),('c','d'),('d','c'),('d','d')]] for row in rows]
        automata.append({'name': name, 'outputs': outputs, 'transitions': transitions})
    dput = (directory/'diagnostics.R').read_text()
    loglike = float(re.search(r'loglike = ([^,]+)', dput).group(1))
    return {'names': names, 'raw_shares': shares.tolist(), 'raw_noise': float(noises[0]),
            'prior': ((shares+.001)/(shares.sum()+.001*len(shares))).tolist(),
            'noise': float(np.clip(noises[0], .01, .49)), 'automata': automata,
            'package_loglike': loglike,
            'source_files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in directory.iterdir() if p.is_file()}}


def likelihood(df, fit):
    logs = []
    q = fit['raw_noise']; automata = fit['automata']
    for _, subject in df.groupby(['session', 'id']):
        lp = np.zeros(len(automata))
        for _, game in subject.groupby('supergame'):
            states = [0]*len(automata)
            for row in game.sort_values('round').itertuples():
                for k, auto in enumerate(automata):
                    lp[k] += np.log(1-q if auto['outputs'][states[k]] == row.coop else q)
                    states[k] = auto['transitions'][states[k]][INDEX[row.coop,row.o_coop]]
        logs.append(logsumexp(np.log(fit['raw_shares'])+lp))
    result = float(sum(logs))
    need(abs(result-fit['package_loglike']) < 1e-7, 'independent package likelihood mismatch')
    return result


def values(fit, treatment, utility):
    q = fit['noise']; autos = fit['automata']; result = []
    pay = {(1,1): 45 if treatment == 4 else 51, (1,0):22,
           (0,1):73 if treatment == 3 else 63, (0,0):39}
    fun = {'linear': lambda x:x, 'reciprocal':lambda x:-1/x, 'square':lambda x:x*x}[utility]
    norm = {pair: (fun(x)-fun(39))/(fun(51)-fun(39)) for pair,x in pay.items()}
    max_residual = 0.0
    for own in autos:
        current = []
        for other in autos:
            n,m = len(own['outputs']),len(other['outputs'])
            P = np.zeros((n*m,n*m)); r = np.zeros(n*m)
            for s,a in enumerate(own['outputs']):
                for t,best in enumerate(other['outputs']):
                    for b,prob in [(best,1-q),(1-best,q)]:
                        ns=own['transitions'][s][INDEX[a,b]]
                        nt=other['transitions'][t][INDEX[b,a]]
                        P[s*m+t,ns*m+nt] += prob
                        r[s*m+t] += prob*norm[a,b]
            v = np.linalg.solve(np.eye(n*m)-.875*P,.125*r)
            max_residual = max(max_residual,float(np.max(abs(v-(.125*r+.875*P@v)))))
            current.append(v.reshape(n,m).tolist())
        result.append(current)
    return result,max_residual


def features(df, fit, tables):
    autos=fit['automata']; K=len(autos); prior=np.array(fit['prior']); q=fit['noise']
    rows=[]
    for _, game in df.groupby(['session','id','supergame'],sort=True):
        own=[0]*K; other=[0]*K; w=prior.copy(); history=[]
        for row in game.sort_values('round').itertuples():
            if row.round >= 2:
                prescriptions=np.array([auto['outputs'][own[j]] for j,auto in enumerate(autos)])
                ds={}
                for treatment,table in tables.items():
                    matrix=np.array([[table[j][k][own[j]][other[k]] for k in range(K)] for j in range(K)])
                    uv=matrix@w
                    ds[treatment]=float(max(uv[prescriptions==1])-max(uv[prescriptions==0]))
                forecast=sum(w[k]*(1-q if auto['outputs'][other[k]] else q) for k,auto in enumerate(autos))
                prev=history[-1]
                rows.append({'key':[int(row.session),int(row.id),int(row.supergame),int(row.round)],
                    'treatment':int(row.treatment),'y':row.coop,'opponent':row.o_coop,'report':row.belief,
                    'forecast':float(forecast),'d':ds,'previous':prev[0],
                    'common':[prev[0],prev[2],(row.round-2)/6],
                    'markov':[prev[0],prev[1],prev[2],sum(z[1] for z in history)/len(history),(row.round-2)/6],
                    'history2': ''.join('C' if a else 'D' for a in prev[:2]) if row.round==2 else None})
            for k,auto in enumerate(autos):
                w[k] *= 1-q if auto['outputs'][other[k]]==row.o_coop else q
                own[k]=auto['transitions'][own[k]][INDEX[row.coop,row.o_coop]]
                other[k]=auto['transitions'][other[k]][INDEX[row.o_coop,row.coop]]
            w /= w.sum()
            history.append((row.coop,row.o_coop,row.belief))
    return rows


def design(rows, kind, actual=False):
    if kind=='markov': return np.array([[1]+r['markov'] for r in rows])
    return np.array([[1,r['d'][r['treatment'] if actual else 2]]+r['common'] for r in rows])


def weights(rows):
    sessions=np.array([r['key'][0] for r in rows]); unique,counts=np.unique(sessions,return_counts=True)
    return np.array([1/(len(unique)*counts[np.where(unique==s)[0][0]]) for s in sessions])


def fit_logistic(rows,kind,tau):
    X=design(rows,kind); y=np.array([r['y'] for r in rows]); wt=weights(rows)
    def objective(beta):
        eta=X@beta
        loss=float(wt@(np.logaddexp(0,eta)-y*eta)+tau/2*(beta[1:]@beta[1:]))
        grad=X.T@(wt*(expit(eta)-y)); grad[1:]+=tau*beta[1:]
        return loss,grad
    bounds=[(None,None)]*X.shape[1]
    if kind=='candidate': bounds[1]=(0,None)
    result=minimize(objective,np.zeros(X.shape[1]),jac=True,method='L-BFGS-B',bounds=bounds,
                    options={'maxiter':10000,'gtol':1e-8,'ftol':1e-14})
    grad=objective(result.x)[1]
    if kind=='candidate' and result.x[1]<1e-10 and grad[1]>0: grad[1]=0
    need(result.success and max(abs(grad))<1e-6,'response fit did not converge')
    return {'coefficients':result.x.tolist(),'tau':tau,'loss':float(result.fun),
            'projected_gradient':float(max(abs(grad))),'iterations':int(result.nit),'message':result.message}


def select(train,validation,kind):
    fits=[]; y=np.array([r['y'] for r in validation]); wt=weights(validation)
    for tau in TAUS:
        fit=fit_logistic(train,kind,tau)
        fit['validation_brier']=float(wt@((expit(design(validation,kind)@fit['coefficients'])-y)**2))
        fits.append(fit)
    best=min(f['validation_brier'] for f in fits)
    chosen=max((f for f in fits if f['validation_brier']<=best+1e-12),key=lambda f:f['tau'])
    return chosen['tau'],fits


def session_metrics(rows,predictions):
    sessions=sorted(set(r['key'][0] for r in rows)); result=[]
    for s in sessions:
        ids=[i for i,r in enumerate(rows) if r['key'][0]==s]; y=np.array([rows[i]['y'] for i in ids])
        item={'session':s,'treatment':rows[ids[0]]['treatment'],'n':len(ids),'observed_cooperation':float(y.mean()),'models':{}}
        for name,ps in predictions.items():
            p=np.array(ps)[ids]; clipped=np.clip(p,1e-6,1-1e-6)
            item['models'][name]={'brier':float(np.mean((p-y)**2)),
                'logscore':float(-np.mean(y*np.log(clipped)+(1-y)*np.log(1-clipped))),
                'mean_prediction':float(p.mean())}
        item['delta_brier']=item['models']['updated']['brier']-item['models']['fixed']['brier']
        result.append(item)
    return result


def uncertainty(metrics):
    groups=[np.array([r['delta_brier'] for r in metrics if r['treatment']==t]) for t in (3,4)]
    need(all(len(g)==8 for g in groups),'target session domain')
    means=[float(g.mean()) for g in groups]; delta=float(np.mean(means))
    rng=np.random.default_rng(20260910)
    boot=np.mean([g[rng.integers(0,8,size=(9999,8))].mean(axis=1) for g in groups],axis=0)
    components=np.array([g.var(ddof=1)/len(g)/4 for g in groups]); se=float(np.sqrt(components.sum()))
    df=float(components.sum()**2/sum(components**2/7)) if se else None
    radius=float(student_t.ppf(.975,df)*se) if se else 0
    hoeffding=float(np.sqrt(2*np.log(40)/16))
    return {'delta_brier':delta,'arm_deltas':dict(zip(['high_t','low_r'],means)),
        'bootstrap_95':np.quantile(boot,[.025,.975]).tolist(),'bootstrap_draws':9999,
        'standard_error':se,'welch_df':df,'welch_95':[delta-radius,delta+radius],
        'hoeffding_95':[max(-1,delta-hoeffding),min(1,delta+hoeffding)],
        'scope':'conditional on source fitting; session sampling assumptions supplied'}


def run(source,fits_dir,out):
    out=Path(out); need(not out.exists(),'refusing to overwrite first results'); out.mkdir(parents=True)
    df=read_source(source); replication=reconstruct(df)
    (out/'reconstruction.json').write_text(json.dumps(replication,indent=2)+'\n')
    eligible=df[df.treatment.ne(1)&df.supergame.ge(5)&df['round'].le(8)]
    source_df=eligible[eligible.treatment.eq(2)]; train_df=source_df[~source_df.session.isin([1,14])]
    validation_df=source_df[source_df.session.isin([1,14])]; target_df=eligible[eligible.treatment.isin([3,4])]
    bundles={}; summaries={}
    for catalogue,utility in [('ten','linear'),('six','linear'),('ten','reciprocal'),('ten','square')]:
        label=catalogue+'-'+utility
        train_fit=load_fit(Path(fits_dir)/('train-'+catalogue)); full_fit=load_fit(Path(fits_dir)/('all-'+catalogue))
        train_fit['reconstructed_loglike']=likelihood(train_df,train_fit)
        full_fit['reconstructed_loglike']=likelihood(source_df,full_fit)
        tb,tr=values(train_fit,2,utility)
        train=features(train_df,train_fit,{2:tb}); validation=features(validation_df,train_fit,{2:tb})
        tables={}; residuals={}
        for t in [2,3,4]: tables[t],residuals[t]=values(full_fit,t,utility)
        all_source=features(source_df,full_fit,{2:tables[2]})
        tau,selection=select(train,validation,'candidate')
        final=fit_logistic(all_source,'candidate',tau)
        # All source-only fitting and tuning above completes before target feature/scoring access.
        target=features(target_df,full_fit,tables)
        beta=np.array(final['coefficients'])
        predictions={'fixed':expit(design(target,'candidate')@beta),
                     'updated':expit(design(target,'candidate',True)@beta)}
        mark_tau,mark_select=select(train,validation,'markov')
        mark=fit_logistic(all_source,'markov',mark_tau)
        constant=float(weights(all_source)@np.array([r['y'] for r in all_source]))
        predictions.update({'markov':expit(design(target,'markov')@mark['coefficients']),
            'constant':np.full(len(target),constant),'persistence':np.array([r['previous'] for r in target])})
        metrics=session_metrics(target,predictions)
        diagnostics={}
        for group in ['all','CC','CD','DC','DD']:
            subset=[r for r in target if group=='all' or r['history2']==group]
            diagnostics[group]={'n':len(subset),'opponent_forecast':float(np.mean([r['forecast'] for r in subset])),
                'actual_opponent':float(np.mean([r['opponent'] for r in subset])),
                'reported_belief':float(np.mean([r['report'] for r in subset])),
                'opponent_brier':float(np.mean([(r['forecast']-r['opponent'])**2 for r in subset])),
                'report_squared_gap':float(np.mean([(r['forecast']-r['report'])**2 for r in subset]))}
        # Persistence copies a raw lagged action: receiver reconstructs it; never serialize that column.
        retained=[{'key':r['key'],'fixed':float(predictions['fixed'][i]),'updated':float(predictions['updated'][i]),
                   'markov':float(predictions['markov'][i]),'constant':constant,'opponent_forecast':r['forecast']}
                  for i,r in enumerate(target)]
        (out/(label+'-predictions.json')).write_text(json.dumps(retained,separators=(',',':'))+'\n')
        bundles[label]={'train_mixture':train_fit,'mixture':full_fit,'utility':utility,
            'selection':selection,'response':final,'markov_selection':mark_select,'markov':mark,
            'constant':constant,'values':tables,'floating_residuals':residuals}
        summaries[label]={'sessions':metrics,'comparison':uncertainty(metrics),'opponent_diagnostics':diagnostics}
        print(label,json.dumps(summaries[label]['comparison']),flush=True)
    (out/'parameters.json').write_text(json.dumps(bundles,indent=2)+'\n')
    (out/'results.json').write_text(json.dumps({'schema':'bellman.afy2024.challenge.v1','specification_commit':SPEC,
        'comparisons':summaries},indent=2)+'\n')


if __name__=='__main__': run(*sys.argv[1:])
