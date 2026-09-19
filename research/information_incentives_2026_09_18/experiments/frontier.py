"""Analytically derived support evaluator. Floating evaluations, not formal proofs."""
import math
import numpy as np
from scipy.optimize import brentq
from scipy.special import xlogy

LN2=math.log(2)

def F(x):
    if abs(x)>1+1e-12: raise ValueError('correlation outside [-1,1]')
    x=max(-1.,min(1.,float(x)))
    return float((xlogy(1+x,1+x)+xlogy(1-x,1-x))/2)

def invF(k):
    if not 0<=k<=LN2: raise ValueError('cost outside [0,log2]')
    return brentq(lambda x:F(x)-k,0,1,xtol=1e-14)

def cost(u,v): return (F(u+v)+F(u-v))/2

def support(k,A,B):
    """max Au+Bv on full signed Cκ; for A,B>=0 witness is in positive quadrant.
    Returns primal, u, v, dual, inverse multiplier beta.
    """
    d=np.array([A+B,A-B],dtype=float)
    if k==0 or max(abs(d))==0: return (0.,0.,0.,0.,0.)
    sat=sum(LN2/2 for x in d if abs(x)>1e-15)
    if k>=sat-1e-14:
        x=np.sign(d); u,v=(x[0]+x[1])/2,(x[0]-x[1])/2
        value=A*u+B*v
        return value,float(u),float(v),value,None
    def point(beta): return np.tanh(beta*d)
    def residual(beta):
        x=point(beta); return (F(x[0])+F(x[1]))/2-k
    hi=1.
    while residual(hi)<0: hi*=2
    beta=brentq(residual,0,hi,xtol=1e-13)
    x=point(beta); u,v=(x[0]+x[1])/2,(x[0]-x[1])/2
    logcosh=lambda t:np.logaddexp(t,-t)-LN2
    dual=(k+sum(logcosh(beta*d))/2)/beta
    return float(A*u+B*v),float(u),float(v),float(dual),float(beta)

def gamma_op(k,ell,box=False):
    z=invF(min(2*k,LN2) if box else k)
    return max(0.,(z-ell)/(1-ell*z))

def penalty(k,g,b=2.,c=1.,box=False):
    if box:return max(0.,b*g*invF(min(2*k,LN2))-c)
    def res(e):
        a=(c+e)/b
        return g*support(k,a,1)[0]-a
    return 0. if res(0)<=0 else brentq(res,0,b-c,xtol=1e-13)

def branches(g,e,b=2.,c=1.,L=.1,w=1.):
    d=c+e
    P=[(0.,0.,0.),(-d/4,d*g/4,b*g/4),(-d/2,0.,b*g/2)]
    O=(-(L+w*g)/2,(w+L*g)/2,0.)
    return [(j,k,tuple(P[j][i]+k*O[i] for i in range(3)))
            for j in range(3) for k in range(2)]

def joint_worst(k,g,e,b=2.,c=1.,L=.1,w=1.):
    records=[]
    for j,h,(C,A,B) in branches(g,e,b,c,L,w):
        val,u,v,dual,beta=support(k,A,B)
        records.append(dict(branch=[j,h],value=C+val,u=u,v=v,
                            upper=C+dual,beta=beta,coeff=[C,A,B]))
    return max(records,key=lambda z:z['value']),records
