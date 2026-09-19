"""Independent original-cell/payoff checks plus three-representation experiments.
Run with numpy/scipy. Explicit failures remain active under python -O.
"""
import hashlib,itertools,json,math,platform
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import minimize,brentq
from scipy.linalg import qr
from scipy.special import xlogy
from frontier import F,invF,cost,support,penalty,gamma_op,joint_worst,LN2

ATOMS=np.array(list(itertools.product((-1,1),repeat=3)))
TH,R,S=ATOMS.T
ALL=np.array([((TH==t)&(R==r)).astype(float) for t in (-1,1) for r in (-1,1)]+
             [((TH==t)&(S==s)).astype(float) for t in (-1,1) for s in (-1,1)])
_,_,piv=qr(ALL.T,pivoting=True)
A=ALL[piv[:np.linalg.matrix_rank(ALL)]]

def check(ok,msg):
    if not ok:raise AssertionError(msg)

def law(u,v):return (1+u*R*S+v*TH*R*S)/8

def kl(q):return float(sum(xlogy(q,8*q)))

def direct_support(k,Acoef,Bcoef):
    coeff=Acoef*R*S+Bcoef*TH*R*S
    result=minimize(lambda q:-coeff@q,np.full(8,.125),jac=lambda q:-coeff,
        constraints=[{'type':'eq','fun':lambda q:A@q-.25,'jac':lambda q:A},
                     {'type':'ineq','fun':lambda q:k-kl(q),
                      'jac':lambda q:-(np.log(8*q)+1)}],
        bounds=[(1e-12,1)]*8,method='SLSQP',options={'ftol':1e-12,'maxiter':1500})
    return {'value':float(coeff@result.x),'kl':kl(result.x),
            'marginal_error':float(max(abs(ALL@result.x-.25))),
            'success':bool(result.success),'message':str(result.message)}

def utility(player,theta,s,r,x1,x2,y1,y2,e,b,c,L,w):
    xi,xj=(x1,x2) if player==0 else (x2,x1)
    yi,yj=(y1,y2) if player==0 else (y2,y1)
    pref=theta if player==0 else -theta
    return c*(xi==xj)+b*(xi==pref)+L*(yi==yj)+w*(yi==s)-e*(xi!=r)

def payoff_gain(q,g,e,b=2,c=1,L=.1,w=1):
    totals=[]
    for player in (0,1):
        total=0.
        for r,t in itertools.product((-1,1),repeat=2):
            deviations=[]
            for xx,yy in itertools.product((-1,1),repeat=2):
                val=0.
                for mass,(th,rr,s) in zip(q,ATOMS):
                    if rr!=r:continue
                    prob=mass*(1+g*s*t)/2
                    x=[r,r];y=[t,t];x[player]=xx;y[player]=yy
                    val+=prob*(utility(player,th,s,r,*x,*y,e,b,c,L,w)-
                               utility(player,th,s,r,r,r,t,t,e,b,c,L,w))
                deviations.append(val)
            total+=max(deviations)
        totals.append(total)
    return totals

def reduced_gain(u,v,g,e,b,c,L,w):
    u,v=abs(u),abs(v);d=c+e
    return max(0,(b*g*v+d*g*u-d)/4,(b*g*v-d)/2)+max(0,(u*(w+L*g)-L-w*g)/2)

def main():
    out={'runtime':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__}}
    regression=[]
    for k,g in [(.2,.8),(.2,1.),(.3,gamma_op(.3,.1))]:
        e=penalty(k,g);eb=penalty(k,g,box=True);a=(1+e)/2
        val,u,v,dual,beta=support(k,a,1)
        q=law(u,v)
        direct=direct_support(k,a,1)
        check(min(q)>-1e-12 and max(abs(ALL@q-.25))<1e-12,'witness marginal')
        check(abs(kl(q)-k)<1e-10 and abs(val-dual)<1e-10,'primal dual')
        check(abs(g*val-a)<1e-10,'enforcement boundary')
        regression.append(dict(kappa=k,gamma=g,full_penalty=e,profile_penalty=e,
            box_penalty=eb,box_extreme_cost=F(invF(min(2*k,LN2))),
            witness={'u':u,'v':v,'cells':q.tolist(),'cost':kl(q)},
            support_primal=val,support_upper=dual,direct=direct))
    out['three_representations']=regression
    k=.3;g=gamma_op(k,.1);gb=gamma_op(k,.1,box=True)
    out['active_design']={'full_gamma':g,'full_penalty':penalty(k,g),
        'box_gamma':gb,'box_penalty':penalty(k,gb,box=True),
        'quality_floor':.6,'voluntary_costless_penalty':1.}
    rng=np.random.default_rng(20260918);maxerr=0
    for _ in range(300):
        xy=rng.uniform(-1,1,2);u,v=(xy[0]+xy[1])/2,(xy[0]-xy[1])/2
        g=rng.uniform(0,1);e=rng.uniform(0,1.5);b=2.;c=1.;L=rng.uniform(0,1);w=1.
        vals=payoff_gain(law(u,v),g,e,b,c,L,w)
        ref=reduced_gain(u,v,g,e,b,c,L,w)
        maxerr=max(maxerr,max(abs(x-ref) for x in vals))
    check(maxerr<1e-12,'payoff enumeration disagrees')
    out['payoff_enumeration']={'player_cases':600,'maximum_error':maxerr,'seed':20260918}
    k=F(.8);g=.7;e=0.
    best,records=joint_worst(k,g,e)
    policy=max(x['value'] for x in records if x['branch'][1]==0)
    operation=next(x['value'] for x in records if x['branch']==[0,1])
    check(best['value']<policy+operation-1e-7,'expected compatibility gap')
    for r in records:
        q=law(r['u'],r['v'])
        check(kl(q)<=k+1e-10,'branch witness cost')
        check(abs(r['value']-r['upper'])<1e-10,'branch dual')
    check(abs(payoff_gain(law(best['u'],best['v']),g,e)[0]-best['value'])<1e-10,'winning branch')
    out['expected_joint_counterexample']={'kappa':k,'gamma':g,'penalty':e,
       'exact_joint':best['value'],'separate_sum':policy+operation,'branches':records}
    # Test all six branch suprema against independent 8-cell numerical optimization.
    directs=[]
    for r in records:
        C,aa,bb=r['coeff']; obs=direct_support(k,aa,bb)
        directs.append(dict(branch=r['branch'],difference=r['value']-(C+obs['value']),**obs))
        check(obs['value']<=r['upper']-C+1e-8,'numerical solver exceeds proved bound')
    out['six_branch_direct_optimizations']=directs
    k=F(.5)/2;g=.8
    out['exact_local_bound_counterexample']={'kappa':k,'full_penalty':penalty(k,g,c=.5),
        'box_penalty':penalty(k,g,c=.5,box=True),'analytic_lower':'1/30','analytic_box':'3/10',
        'feasible_witness_cost':F(1/3),'box_extreme_cost':F(.5)}
    check(1/30<=out['exact_local_bound_counterexample']['full_penalty']<.3,'exact gap')
    # Enumerate complete-information policy NE, establishing the disclosure continuation.
    disclosure=[]
    for e in [0.,.090179225583,.5,1.,1.1]:
        for th,r in itertools.product((-1,1),repeat=2):
            ne=[]
            for x in itertools.product((-1,1),repeat=2):
                def pol(i,xi,xj):return (xi==xj)+2*(xi==(th if i==0 else -th))-e*(xi!=r)
                if all(pol(i,x[i],x[1-i])>=pol(i,-x[i],x[1-i])-1e-12 for i in (0,1)):ne.append(x)
            if e<1:check(ne==[(th,-th)],'unique revealed policy equilibrium')
            else:check((r,r) in ne,'enforced revealed cooperation')
            disclosure.append(dict(e=e,theta=th,R=r,policy_equilibria=ne))
    out['disclosure_continuations']=disclosure
    out['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                         [Path(__file__),Path(__file__).with_name('frontier.py')]}
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
