"""Independent standard-library receiver. Never imports producer or fitting libraries.

Exact rational residuals bind the finite reward calculation. Prediction and score
reconstruction uses floats with a declared tolerance; statistical inference is not
certified by this receiver. A separately acquired, hash-verified author file is needed.
"""
from collections import defaultdict
import csv
from fractions import Fraction as F
import hashlib
import io
import json
import math
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
PAIRS=((1,1),(1,0),(0,1),(0,0))


def need(ok,message):
    if not ok: raise ValueError(message)


def close(a,b,message,tolerance=1e-10):
    need(math.isfinite(float(a)) and math.isfinite(float(b)) and abs(a-b)<=tolerance,message)


def sigmoid(x):
    return 1/(1+math.exp(-x)) if x>=0 else math.exp(x)/(1+math.exp(x))


def source_rows(path):
    raw=Path(path).read_bytes()
    manifest=json.loads((HERE/'source-manifest.json').read_text())
    expected=next(s['sha256'] for s in manifest['sources'] if s['name'].endswith('_data.txt'))
    need(hashlib.sha256(raw).hexdigest()==expected,'source identity mismatch')
    reader=csv.DictReader(io.StringIO(raw.decode().split('**************',1)[1].strip()),delimiter='\t')
    result=[]; keys=set()
    for item in reader:
        row={k:None if v=='' else float(v) if k in ('belief','o_belief') else int(v) for k,v in item.items()}
        key=tuple(row[k] for k in ('session','id','supergame','round'))
        need(key not in keys,'duplicate source key'); keys.add(key)
        need(row['beliefon']==int(row['supergame']>=5),'source timing mismatch')
        result.append(row)
    return result


def canonical(name):
    if name in ('AC','AD'): return ([int(name=='AC')],[[0,0,0,0]])
    if name=='GRIM': return ([1,0],[[0,1,1,1],[1,1,1,1]])
    if name=='GRIM2': return ([1,1,0],[[0,1,1,1],[0,2,2,2],[2,2,2,2]])
    if name=='TFT': return ([1,0],[[0,1,0,1],[0,1,0,1]])
    if name=='STFT': return ([0,1],[[1,0,1,0],[1,0,1,0]])
    if name=='TF2T': return ([1,1,0],[[0,1,0,1],[0,2,0,2],[0,2,0,2]])
    need(name in ('T6','T7','T8'),'unknown catalogue member')
    k=int(name[1:]); return ([1]*(k-1)+[0],[[min(s+1,k-1),k-1,k-1,k-1] for s in range(k)])


def validate_mixture(mix):
    need(len(mix['names'])==len(set(mix['names'])),'duplicate strategy')
    need(len(mix['automata'])==len(mix['names']),'catalogue size')
    for name,auto in zip(mix['names'],mix['automata']):
        outputs,transitions=canonical(name)
        need(auto=={'name':name,'outputs':outputs,'transitions':transitions},'automaton definition mismatch')
    close(sum(mix['raw_shares']),1,'shares not normalized')
    need(all(p>=0 for p in mix['raw_shares']),'negative share')
    expected=[(p+.001)/(sum(mix['raw_shares'])+.001*len(mix['names'])) for p in mix['raw_shares']]
    need(len(mix['prior'])==len(expected),'prior dimension')
    for p,e in zip(mix['prior'],expected): close(p,e,'prior smoothing mismatch')
    close(mix['noise'],min(.49,max(.01,mix['raw_noise'])),'noise clipping mismatch')
    need(0<mix['raw_noise']<1,'likelihood noise unsupported')


def residual_bounds(bundle):
    mix=bundle['mixture']; validate_mixture(mix)
    q=F(str(mix['noise'])); delta=F(7,8); autos=mix['automata']; residual=F(0); count=0
    utility=bundle['utility']
    need(utility in ('linear','reciprocal','square'),'unsupported utility')
    def u(x): return F(x) if utility=='linear' else -F(1,x) if utility=='reciprocal' else F(x*x)
    for treatment,table in bundle['values'].items():
        t=int(treatment); need(t in (2,3,4),'unknown treatment')
        payments={(1,1):45 if t==4 else 51,(1,0):22,(0,1):73 if t==3 else 63,(0,0):39}
        reward={pair:(u(x)-u(39))/(u(51)-u(39)) for pair,x in payments.items()}
        need(len(table)==len(autos),'value own dimension')
        for j,own in enumerate(autos):
            need(len(table[j])==len(autos),'value opponent dimension')
            for k,other in enumerate(autos):
                v=[[F(str(x)) for x in line] for line in table[j][k]]
                need(len(v)==len(own['outputs']) and all(len(line)==len(other['outputs']) for line in v),'value state dimension')
                for s,a in enumerate(own['outputs']):
                    for z,expected_b in enumerate(other['outputs']):
                        rhs=F(0)
                        for b,prob in [(expected_b,1-q),(1-expected_b,q)]:
                            ns=own['transitions'][s][PAIRS.index((a,b))]
                            nz=other['transitions'][z][PAIRS.index((b,a))]
                            rhs+=prob*((1-delta)*reward[a,b]+delta*v[ns][nz])
                        residual=max(residual,abs(v[s][z]-rhs)); count+=1
    need(residual<F(1,10**11),'value residual too large')
    return {'states_checked':count,'exact_max_residual':str(residual),
            'exact_value_error_bound':str(8*residual),
            'exact_response_error_bound':str(F(str(bundle['response']['coefficients'][1]))*4*residual)}


def verify_predictions(source,bundle,predictions,summary):
    autos=bundle['mixture']['automata']; prior=bundle['mixture']['prior']; q=bundle['mixture']['noise']
    beta=bundle['response']['coefficients']; mark=bundle['markov']['coefficients']
    need(len(beta)==5 and beta[1]>=0 and len(mark)==6,'response class mismatch')
    target=[r for r in source if r['treatment'] in (3,4) and r['supergame']>=5 and r['round']<=8]
    games=defaultdict(list)
    for row in target: games[(row['session'],row['id'],row['supergame'])].append(row)
    retained={tuple(r['key']):r for r in predictions}
    need(len(retained)==len(predictions),'duplicate prediction key')
    expected_keys={tuple(r[k] for k in ('session','id','supergame','round')) for r in target if r['round']>=2}
    need(set(retained)==expected_keys,'prediction query mismatch')
    measurements=defaultdict(list); maxdiff=0
    for prefix,game in sorted(games.items()):
        own=[0]*len(autos); other=[0]*len(autos); w=list(prior); past=[]
        for row in sorted(game,key=lambda r:r['round']):
            a,b=row['coop'],row['o_coop']
            if row['round']>=2:
                key=prefix+(row['round'],); stored=retained[key]
                need(set(stored)=={'key','fixed','updated','markov','constant','opponent_forecast'},'unexpected prediction fields')
                scores={}
                for treatment in (2,row['treatment']):
                    vals=bundle['values'][str(treatment)]; best={0:-math.inf,1:-math.inf}
                    for j,auto in enumerate(autos):
                        value=sum(w[k]*vals[j][k][own[j]][other[k]] for k in range(len(autos)))
                        action=auto['outputs'][own[j]]; best[action]=max(best[action],value)
                    scores[treatment]=best[1]-best[0]
                prev=past[-1]; round_feature=(row['round']-2)/6
                common=beta[0]+beta[2]*prev[0]+beta[3]*prev[2]+beta[4]*round_feature
                computed={'fixed':sigmoid(common+beta[1]*scores[2]),
                    'updated':sigmoid(common+beta[1]*scores[row['treatment']]),
                    'markov':sigmoid(sum(c*x for c,x in zip(mark,[1,prev[0],prev[1],prev[2],sum(p[1] for p in past)/len(past),round_feature]))),
                    'constant':bundle['constant'],
                    'opponent_forecast':sum(w[k]*(1-q if auto['outputs'][other[k]] else q) for k,auto in enumerate(autos))}
                for name,value in computed.items():
                    close(stored[name],value,'prediction mismatch: '+name)
                    maxdiff=max(maxdiff,abs(stored[name]-value))
                computed['persistence']=prev[0]
                measurements[row['session']].append((a,computed))
            for k,auto in enumerate(autos):
                w[k]*=1-q if auto['outputs'][other[k]]==b else q
                own[k]=auto['transitions'][own[k]][PAIRS.index((a,b))]
                other[k]=auto['transitions'][other[k]][PAIRS.index((b,a))]
            total=sum(w); w=[x/total for x in w]
            past.append((a,b,row['belief']))
    deltas={}
    need({s['session'] for s in summary['sessions']}==set(measurements),'session score query mismatch')
    for session in summary['sessions']:
        s=session['session']; observations=measurements[s]; n=len(observations)
        need(n==session['n'],'session count mismatch')
        close(sum(y for y,_ in observations)/n,session['observed_cooperation'],'cooperation mean mismatch')
        for model,record in session['models'].items():
            need(model in ('fixed','updated','markov','constant','persistence'),'unknown scored model')
            brier=sum((p[model]-y)**2 for y,p in observations)/n
            logscore=-sum(y*math.log(min(1-1e-6,max(1e-6,p[model])))+(1-y)*math.log(1-min(1-1e-6,max(1e-6,p[model])) ) for y,p in observations)/n
            close(brier,record['brier'],'Brier mismatch')
            close(logscore,record['logscore'],'log score mismatch')
            close(sum(p[model] for _,p in observations)/n,record['mean_prediction'],'prediction mean mismatch')
        delta=session['models']['updated']['brier']-session['models']['fixed']['brier']
        close(delta,session['delta_brier'],'session contrast mismatch'); deltas[s]=delta
    close(sum(deltas.values())/16,summary['comparison']['delta_brier'],'primary contrast mismatch')
    return {'predictions_checked':len(predictions),'session_scores_checked':len(deltas),
            'max_prediction_reconstruction_difference':maxdiff,
            'sampling_inference':'not certified by arithmetic receiving'}


def run(raw_path):
    manifest=json.loads((HERE/'first-run-manifest.json').read_text())
    for rel,digest in {**manifest['source_hashes'],**manifest['outputs']}.items():
        need(hashlib.sha256((HERE/rel).read_bytes()).hexdigest()==digest,'frozen output mismatch: '+rel)
    source=source_rows(raw_path)
    parameters=json.loads((HERE/'first-results/parameters.json').read_text())
    results=json.loads((HERE/'first-results/results.json').read_text())
    need(results['specification_commit']=='4abea07','specification identity mismatch')
    report={}
    for label,bundle in parameters.items():
        bounds=residual_bounds(bundle)
        predictions=json.loads((HERE/'first-results'/f'{label}-predictions.json').read_text())
        report[label]={**bounds,**verify_predictions(source,bundle,predictions,results['comparisons'][label])}
    return {'schema':'bellman.afy2024.receiving.v1','checks':report,
        'implementation':'standard library; no producer, R, NumPy, SciPy or fitting imports',
        'scope':'exact rational residual assurance; numerical prediction and score reconstruction; no statistical or preference certification'}


if __name__=='__main__':
    print(json.dumps(run(sys.argv[1]),indent=2))
