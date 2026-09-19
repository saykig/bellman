"""Seeded numerical falsification and exact finite checks, not a formal proof.
Run: python check.py > results.json  (numpy/scipy required).
"""
from fractions import Fraction as R
from itertools import product
from pathlib import Path
import hashlib, json, math, platform
import numpy as np
import scipy
from scipy.optimize import brentq, minimize, linprog
from scipy.special import xlogy

P=np.array([.25,.25,.5]); SIGNS=(-1,1)
def entropy(x):
    x=np.asarray(x)
    return .5*(xlogy(1+x,1+x)+xlogy(1-x,1-x))
def support(g,k,p=P,kind='kl'):
    g=np.asarray(g,float)
    cost={'kl':entropy,'chi2':lambda x:np.asarray(x)**2,'tv':lambda x:abs(np.asarray(x))/2}[kind]
    if k==0 or np.all(g==0):return 0.,np.zeros(len(g)),None
    if kind=='tv':
        x=np.zeros(len(g));left=k
        for i in np.argsort(-abs(g)):
            spend=min(left,p[i]/2);x[i]=np.sign(g[i])*2*spend/p[i];left-=spend
        return float(p@(g*x)),x,None
    end=np.sign(g)
    if p@cost(end)<=k:return float(p@abs(g)),end,None
    mapx=(lambda t:np.tanh(t*g)) if kind=='kl' else (lambda t:np.clip(t*g,-1,1))
    hi=1.
    while p@cost(mapx(hi))<k:hi*=2
    beta=brentq(lambda t:p@cost(mapx(t))-k,0,hi,xtol=1e-14)
    x=mapx(beta)
    dual=None
    if kind=='kl':dual=(k+p@(np.logaddexp(beta*g,-beta*g)-math.log(2)))/beta
    return float(p@(g*x)),x,dual

def controlled(k,gamma,b=2.,c=.2):
    def gap(e):
        d=c+e;g=np.array([b-d,-d,-b-d]);return gamma*support(g,k)[0]+P@g
    return 0. if gap(0)<=0 else brentq(gap,0,b-c,xtol=1e-13)

def law(x):return np.array([P[z]*(1+x[z]*r*s)/4 for z,r,s in product(range(3),SIGNS,SIGNS)])
CELLS=list(product(range(3),SIGNS,SIGNS));REF=law([0,0,0])
MAT=[];RHS=[]
for z in range(3):
    for r in SIGNS:
        MAT.append([int(zz==z and rr==r) for zz,rr,ss in CELLS]);RHS.append(P[z]/2)
    MAT.append([int(zz==z and ss==-1) for zz,rr,ss in CELLS]);RHS.append(P[z]/2)
MAT=np.array(MAT);RHS=np.array(RHS)

def direct_support(g,k,kind='kl'):
    obj=np.array([g[z]*r*s for z,r,s in CELLS])
    def cost(q):
        if kind=='kl':return xlogy(q,q/REF).sum()
        if kind=='chi2':return (((q-REF)**2)/REF).sum()
        return abs(q-REF).sum()/2
    # TV is a nonsmooth linear program after introducing 12 absolute-value slacks.
    if kind=='tv':
        res=linprog(np.r_[-obj,np.zeros(12)],
            A_ub=np.vstack([np.c_[np.eye(12),-np.eye(12)],
                            np.c_[-np.eye(12),-np.eye(12)],
                            np.r_[np.zeros(12),np.ones(12)][None,:]]),
            b_ub=np.r_[REF,-REF,2*k],A_eq=np.c_[MAT,np.zeros((9,12))],b_eq=RHS,
            bounds=[(0,None)]*24,method='highs')
        if not res.success:raise RuntimeError(res.message)
        q=res.x[:12]
        return dict(value=float(obj@q),budget=float(cost(q)),
                    marginal_residual=float(max(abs(MAT@q-RHS))),status=True)
    # Original 12 probabilities, not the 3-correlation parameterization.
    res=minimize(lambda q:-obj@q,REF,jac=lambda q:-obj,method='SLSQP',
        bounds=[(1e-14,1)]*12,
        constraints=[{'type':'eq','fun':lambda q:MAT@q-RHS,'jac':lambda q:MAT},
                     {'type':'ineq','fun':lambda q:k-cost(q)}],
        options={'ftol':1e-12,'maxiter':1200})
    return dict(value=float(obj@res.x),budget=float(cost(res.x)),
                marginal_residual=float(max(abs(MAT@res.x-RHS))),status=bool(res.success))

def original_gains(x,gamma,e,b=2.,c=.2,L=.1,w=1.):
    """Enumerate original cells, both players, and all 6 unilateral product actions."""
    out=[];q=law(x);pref=((0,1,2),(1,0,2))
    for r,t,player in product(SIGNS,SIGNS,range(2)):
        joint=np.array([q[j]*(1+gamma*s*t)/2 if rr==r else 0 for j,(z,rr,s) in enumerate(CELLS)])
        mass=joint.sum()
        if mass<1e-14:continue
        for a,y in product(range(3),SIGNS):
            gain=0.
            for j,(z,rr,s) in enumerate(CELLS):
                target=c+b*(pref[player][z]==2)+L+w*(t==s)
                dev=c*(a==2)+b*(pref[player][z]==a)-e*(a!=2)+L*(y==t)+w*(y==s)
                gain+=joint[j]*(dev-target)
            out.append(gain/mass)
    return max(out)

def policy_matrix(mu,e,b=2.,c=.2):
    prob=(mu,1-mu,0);pref=((0,1,2),(1,0,2));ans=[]
    for i in range(2):
        ans.append(np.array([[c*(a==other)+b*sum(prob[z]*(a==pref[i][z]) for z in range(3))-e*(a!=2)
                             for other in range(3)] for a in range(3)]))
    return ans

def nash_residual(mu,e,mix1,mix2):
    A,B=policy_matrix(mu,e);v1=A@mix2;v2=B@mix1
    return max(max(v1)-mix1@v1,max(v2)-mix2@v2)

def exact_checks():
    # All scalar-cost profiles on tiny fibres, including nonconvex costs.
    checks=0
    maps=[[(0,2),(0,0),(1,3)],[(0,1),(1,0),(1,4)]]
    for a in product((0,1),repeat=2):
        costs=[[cost for label,cost in local if label==label_wanted] for local,label_wanted in zip(maps,a)]
        for budget in range(9):
            direct=any(x+y<=budget for x,y in product(*costs))
            assert direct==(sum(min(c) for c in costs)<=budget);checks+=1
    # Conditional composition with retained interface versus direct witness search.
    K={0:[(0,2),(2,0)],1:[(1,1)]};J={0:[(2,1)],1:[(0,0),(2,2)]}
    for threshold in product(range(6),repeat=2):
        direct=any(all(x[i]+y[i]<=threshold[i] for i in range(2)) for u in K for x in K[u] for y in J[u])
        # Split upper budgets independently, checking the actual upper-image formula.
        composed=any(any(all(x[i]<=a[i] for i in range(2)) for x in K[u]) and
                     any(all(y[i]<=threshold[i]-a[i] for i in range(2)) for y in J[u])
                     for u in K for a in product(range(6),repeat=2))
        assert direct==composed;checks+=1
    # Erasing the interface BEFORE connection admits an impossible zero total.
    left={0:[0],1:[1]};right={0:[1],1:[0]}
    assert min(x+y for u in left for x in left[u] for y in right[u])==1
    assert min(x+y for xs in left.values() for ys in right.values() for x in xs for y in ys)==0
    eta=R(1);v=R(1,5);k=eta/2-v;assert k==R(3,10)
    assert eta*R(1,2)-k==v
    assert not any(q<=v and 1-q<=v for q in [R(i,100) for i in range(101)])
    a=b=R(1,4);add={(x,y):(1+a*x+b*y)/4 for x,y in product(SIGNS,repeat=2)}
    prodq={(x,y):(1+a*x)*(1+b*y)/4 for x,y in product(SIGNS,repeat=2)}
    chi=lambda q:sum((val-R(1,4))**2/R(1,4) for val in q.values())
    assert chi(add)==R(1,8) and chi(prodq)==R(33,256)
    assert all(sum(add[x,y] for y in SIGNS)==sum(prodq[x,y] for y in SIGNS) for x in SIGNS)
    Kpay=[(R(1),R(0)),(R(0),R(1)),(R(3,4),R(3,4))]
    assert not any(max(point)<=R(1,2) for point in Kpay)
    assert tuple((Kpay[0][i]+Kpay[1][i])/2 for i in range(2))==(R(1,2),R(1,2))
    # Search finds the first small non-product joint table with uniform marginals.
    bad=[]
    for counts in product(range(3),repeat=4):
        if sum(counts)!=2:continue
        mu=[R(x,2) for x in counts]
        if mu[0]+mu[1]==R(1,2) and mu[0]+mu[2]==R(1,2) and mu[0]*mu[3]!=mu[1]*mu[2]:bad.append(counts)
    assert (1,0,0,1) in bad
    return {'finite_profile_and_composition_queries':checks,'partial_cost_threshold':str(k),
            'chi2_glue':str(chi(prodq)),'chi2_true_minimum':str(chi(add)),
            'nonconvex_payoffs':[[str(x) for x in v] for v in Kpay],
            'two_sender_counterexamples_half_grid':bad,'all_assertions_passed':True}

def main():
    rng=np.random.default_rng(20260918);k=.3;b=2;c=.2;z=brentq(lambda z:entropy(z)-k,0,1)
    gamma=max(.2,(z-.1)/(1-.1*z));e=controlled(k,gamma)
    g=np.array([b-c-e,-c-e,-b-c-e]);val,x,dual=support(g,k)
    gap=original_gains(x,gamma,e);below=original_gains(x,gamma,e-1e-5)
    assert abs(gap)<1e-9 and below>0
    assert original_gains([z]*3,gamma-.01,1.8)>0
    cases=[]
    for kind in ('kl','chi2','tv'):
        for j in range(12):
            direction=rng.normal(size=3);budget=float(rng.uniform(.03,.25))
            expected,wit,bound=support(direction,budget,kind=kind)
            direct=direct_support(direction,budget,kind)
            err=abs(expected-direct['value'])
            assert err<2e-6 and direct['marginal_residual']<1e-8 and direct['budget']<=budget+1e-7,(kind,err,direct)
            if bound is not None:assert abs(bound-expected)<1e-10
            cases.append({'kind':kind,'kappa':budget,'direction':direction.tolist(),
                          'profile_value':expected,'direct':direct,'absolute_gap':err})
    random_residual=0.
    for _ in range(200):
        xx=rng.uniform(-1,1,3)
        if P@entropy(xx)>k:xx*=brentq(lambda scale:P@entropy(scale*xx)-k,0,1)
        random_residual=max(random_residual,original_gains(xx,gamma,e))
    assert random_residual<1e-9
    nr=0.
    for penalty in (0.,.5,.799):
        for qq in np.linspace(0,1,101):
            mu=.5+c/b*(qq-.5)
            nr=max(nr,nash_residual(mu,penalty,np.array([qq,1-qq,0]),np.array([1-qq,qq,0])))
    nr=max(nr,nash_residual(.5,.8,np.array([0,0,1]),np.array([0,0,1])))
    assert nr<1e-12
    endpoint_x=np.array([-1.,0.,0.]);weights=P*(1+endpoint_x);post=weights/weights.sum()
    assert post[0]==0 and post[1]>0 and float(P@entropy(endpoint_x))<k
    endpoint_e=controlled(k,1.)
    result={'status':'checks_passed','python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seed':20260918,
      'benchmark':{'kappa':k,'gamma_opt':gamma,'e_controlled':e,'e_partial_low_disclosure_cost':.8,
        'disclosure_cost_cut':.3,'gamma_one_controlled_penalty':endpoint_e,
        'gamma_one_voluntary_penalty_at_cost_point4':1.8,'policy_witness':x.tolist(),
        'primal_dual_gap':abs(val-dual),'original_game_max_gain':gap,
        'gain_when_fine_decreased_by_1e_5':below,'random_law_max_gain':random_residual,
        'continuation_nash_max_residual':nr},
      'support_loss':{'x':endpoint_x.tolist(),'cost':float(P@entropy(endpoint_x)),
                      'public_posterior':post.tolist(),'certificate_posterior':[0,1,0]},
      'direct_12_cell_comparisons':cases,'exact':exact_checks()}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
