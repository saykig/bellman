"""Shared-KL extension of the supplied hidden H-X/H-Y example.
Independent 16-cell optimization, 4-coupling dual, and 2-likelihood profiles.
"""
import itertools,json,math,hashlib
from pathlib import Path
import numpy as np
from scipy.optimize import brentq,minimize,minimize_scalar
from scipy.linalg import qr
from scipy.special import xlogy

PX=(.7,.3)

def cells(t,p):
    q=np.array([t,p-t,.5-t,.5-p+t])
    if min(q)<-1e-12:raise ValueError('infeasible 2x2 table')
    return np.maximum(q,0.)
def bounds(p):return max(0,p-.5),min(p,.5)
def divergence(t,p):
    q=cells(t,p);r=cells(p/2,p)
    return float(sum(xlogy(q,q/r)))
def derivative(t,p):return math.log(t*(.5-p+t)/((p-t)*(.5-t)))
def tilted(d,p):
    lo,hi=bounds(p)
    eps=1e-14
    return brentq(lambda t:derivative(t,p)-d,lo+eps,hi-eps,xtol=1e-14)
def profile(a):
    # min conditional KL at event Pr(X=0,Y=0)=a, H hidden.
    lo=max(.2,2*a-.3);hi=min(.5,2*a)
    if hi<lo-1e-12:return math.inf,None
    fun=lambda t:(divergence(t,.7)+divergence(2*a-t,.3))/2
    if hi-lo<1e-12:return fun((lo+hi)/2),[(lo+hi)/2,2*a-(lo+hi)/2]
    # convex scalar minimization independent of the tilt-based producer.
    res=minimize_scalar(fun,bounds=(lo,hi),method='bounded',options={'xatol':1e-13})
    return float(res.fun),[float(res.x),float(2*a-res.x)]
def dual(k,e):
    gain=(1-e,-3-e)
    def points(beta):return np.array([[tilted(beta*g,p) for p in PX] for g in gain])
    def cost(t):return sum(divergence(t[z,h],p) for z in range(2) for h,p in enumerate(PX))/4
    hi=1.
    while cost(points(hi))<k:hi*=2
    beta=brentq(lambda b:cost(points(b))-k,0,hi,xtol=1e-12)
    t=points(beta);value=sum(gain[z]*t[z,h] for z in range(2) for h in range(2))/4
    upper=k/beta+sum(gain[z]*t[z,h]-divergence(t[z,h],p)/beta
                     for z in range(2) for h,p in enumerate(PX))/4
    return float(value),t,float(upper),float(beta)

def full_check(k,e):
    atoms=list(itertools.product(range(2),repeat=4)) # z,h,x,y
    ref=np.array([.25*(PX[h] if x==0 else 1-PX[h])*.5 for z,h,x,y in atoms])
    rows=[];targets=[]
    for z,h,x in itertools.product(range(2),repeat=3):
        rows.append([int((zz,hh,xx)==(z,h,x)) for zz,hh,xx,yy in atoms]);targets.append(.25*(PX[h] if x==0 else 1-PX[h]))
    for z,h,y in itertools.product(range(2),repeat=3):
        rows.append([int((zz,hh,yy)==(z,h,y)) for zz,hh,xx,yy in atoms]);targets.append(.125)
    rows=np.array(rows,dtype=float);targets=np.array(targets)
    _,_,piv=qr(rows.T,pivoting=True);take=piv[:np.linalg.matrix_rank(rows)]
    A=rows[take];b=targets[take]
    coeff=np.array([(1-e if z==0 else -3-e)*int(x==0 and y==0) for z,h,x,y in atoms])
    kl=lambda q:float(sum(xlogy(q,q/ref)))
    res=minimize(lambda q:-coeff@q,ref,jac=lambda q:-coeff,
        constraints=[{'type':'eq','fun':lambda q:A@q-b,'jac':lambda q:A},
                     {'type':'ineq','fun':lambda q:k-kl(q),'jac':lambda q:-(np.log(q/ref)+1)}],
        bounds=[(1e-12,1)]*16,method='SLSQP',options={'ftol':1e-12,'maxiter':1500})
    return {'value':float(coeff@res.x),'cost':kl(res.x),'cells':res.x.tolist(),
        'marginal_error':float(max(abs(rows@res.x-targets))), 'success':bool(res.success)}
def check(x,s):
    if not x:raise AssertionError(s)
def main():
    out=[]
    for k in (.03,.08,.15):
        value0=dual(k,0)[0]
        e=0. if value0<=0 else brentq(lambda ee:dual(k,ee)[0],0,.2,xtol=1e-12)
        val,t,upper,beta=dual(k,e)
        a=t.mean(axis=1)
        j=[profile(aa)[0] for aa in a]
        # Each individual state can spend twice the total budget while the other stays at reference.
        cap=2*k
        if profile(.4)[0]<=cap: U=.4
        else:U=brentq(lambda aa:profile(aa)[0]-cap,.25,.4,xtol=1e-12)
        L=.5-U;eb=max(0,(U-3*L)/(U+L))
        witness_cost=sum(divergence(t[z,h],p) for z in range(2) for h,p in enumerate(PX))/4
        independent=full_check(k,e)
        check(abs(val-upper)<1e-10,'dual equality')
        check(abs(witness_cost-k)<1e-9,'budget attainment')
        check(abs(sum(j)/2-k)<1e-8,'likelihood profile reconstruction')
        check(abs(independent['value']-val)<1e-7,'full law disagreement')
        check(independent['marginal_error']<1e-9,'marginals')
        out.append(dict(kappa=k,full_penalty=e,profile_penalty=e,box_penalty=eb,
            statewise_interval=[L,U],likelihoods=a.tolist(),couplings=t.tolist(),
            per_state_profile_cost=j,witness_total_cost=witness_cost,
            box_endpoint_total_cost=profile(U)[0],
            numerator=val,dual_upper=upper,beta=beta,full_16_cell_check=independent))
    print(json.dumps({'hidden_separator':out,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
