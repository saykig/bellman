"""Counterexample search and numerical falsification of proved boundary formulas.
Run with assertions enabled; numpy/scipy. Not a production certificate checker.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib,json,math
import numpy as np
import scipy
from scipy.optimize import brentq,minimize
from scipy.special import xlogy

LN2=math.log(2)
def F(x):
 x=np.asarray(x);return .5*(xlogy(1+x,1+x)+xlogy(1-x,1-x))
def support(p,k,g):
 if k==0:return 0.
 g=np.asarray(g)
 if k>=sum(p[g!=0])*LN2:return p@abs(g)
 hi=1.
 while p@F(np.tanh(hi*g))<k:hi*=2
 t=brentq(lambda t:p@F(np.tanh(t*g))-k,0,hi,xtol=1e-13)
 return p@(g*np.tanh(t*g))
def ctl(p,k,gamma,b=2.,c=.2):
 def residual(e):
  gains=[]
  for j in (0,1):
   g=np.full(3,-c-e);g[j]+=b;g[2]-=b
   gains.append(p@g+gamma*support(p,k,g))
  return max(gains)
 if residual(0)<=0:return 0.
 if residual(b-c)>=-1e-12:return b-c
 return brentq(residual,0,b-c,xtol=1e-12)
def frontier(p,k,gamma,k12=.4,k23=.4,b=2.,c=.2,eta=1.,v=.2):
 C=ctl(p,k,gamma,b,c);H=b-c;a=b/2-c
 trigger=gamma==1 and ((k>=min(p[:2])*LN2 and k12<eta-v) or (k>=p[2]*LN2 and k23<eta-v))
 value=H if trigger else max(C,a if k12<eta/2-v else 0.)
 jump=trigger and k<(1-max(p[:2]))*LN2
 return dict(value=float(value),controlled=float(C),support_trigger=bool(trigger),discontinuous=bool(jump))
def direct_ctl(p,k,gamma):
 # Optimize the ORIGINAL 12 probabilities with fixed conditional marginals.
 cells=list(product(range(3),(-1,1),(-1,1)));ref=np.array([p[z]/4 for z,r,s in cells])
 mat=[];rhs=[]
 for z in range(3):
  for r in (-1,1):mat.append([int(zz==z and rr==r) for zz,rr,ss in cells]);rhs.append(p[z]/2)
  mat.append([int(zz==z and ss==-1) for zz,rr,ss in cells]);rhs.append(p[z]/2)
 mat=np.array(mat);rhs=np.array(rhs)
 best=0.;residual=0.;statuses=[]
 for j,h in product((0,1),(-1,1)):
  # r=1,t=h; sign symmetry covers r=-1 too.
  event=np.array([(1+gamma*s*h)/2 if r==1 else 0 for z,r,s in cells])
  pref=np.array([2*((z==j)-(z==2)) for z,r,s in cells])
  def gain(q):return (q@(event*pref))/(q@event)-.2
  out=minimize(lambda q:-gain(q),ref,method='SLSQP',bounds=[(1e-13,1)]*12,
    constraints=[{'type':'eq','fun':lambda q:mat@q-rhs},
     {'type':'ineq','fun':lambda q:k-xlogy(q,q/ref).sum()}],options={'ftol':1e-11,'maxiter':800})
  residual=max(residual,float(max(abs(mat@out.x-rhs))),max(0,float(xlogy(out.x,out.x/ref).sum()-k)))
  best=max(best,gain(out.x));statuses.append(bool(out.success))
 return best,residual,statuses

def exact_counterexamples():
 p=[Q(1,5),Q(3,10),Q(1,2)];x=[-Q(4,5),Q(4,5),-Q(4,5)];gamma=Q(4,5)
 fine=Q(0);post=[]
 for h in (-1,1):
  masses=[p[z]*(1+gamma*h*x[z]) for z in range(3)];pi=[v/sum(masses) for v in masses];post.append(pi)
  fine=max(fine,*[2*(pi[j]-pi[2])-Q(1,5) for j in (0,1)])
 assert fine==Q(99,155)
 # Information changes neither support nor continuation in this finite-catalogue jump.
 assert all(v>0 for pi in post for v in pi)
 # Search dyadic grids for the simplest cost-threshold impossibility/restoration.
 feasible=[]
 for k in [Q(29,100),Q(3,10),Q(31,100)]:
  qs=[Q(i,100) for i in range(101) if Q(i,100)-k<=Q(1,5) and 1-Q(i,100)-k<=Q(1,5)]
  feasible.append(bool(qs))
 assert feasible==[False,True,True]
 # Equilibrium-driven counterexample: exact best responses after E12, all posteriors.
 eq=[]
 for delta in [Q(-1,100),Q(0),Q(1,100)]:
  e=Q(0) if delta<=0 else 1+delta
  u=[1+delta-e,1-e,Q(0)];best=[i for i,a in enumerate(u) if a==max(u)]
  sender=[Q(1),Q(0),Q(1,5)]
  assert any(sender[i]<=Q(1,5) for i in best)
  if delta>0:
   for gap in [Q(1,1000),Q(1,10),Q(1)]:
    trial=max(Q(0),e-gap);u0=[1+delta-trial,1-trial,Q(0)]
    assert u0[0]>max(u0[1:])
  eq.append({'delta':str(delta),'minimum_fine':str(e),'credible_actions_at_min':best})
 return {'catalogue_jump':str(fine),'catalogue_posteriors':[[str(v) for v in pi] for pi in post],
         'cost_threshold_feasible_029_030_031':feasible,'equilibrium_example':eq}

def main():
 rng=np.random.default_rng(20260919);p=np.array([.2,.3,.5]);cases=[]
 for k,k12,k23 in [(.3,.4,.4),(.4,.9,.4),(.55,.9,.4)]:
  seq=[]
  for gamma in (1-1e-2,1-1e-4,1-1e-6,1.):
   seq.append({'gamma':gamma,**frontier(p,k,gamma,k12,k23)})
  cases.append({'budget':k,'k12':k12,'k23':k23,'gate_sequence':seq})
 assert cases[0]['gate_sequence'][-1]['discontinuous']
 assert cases[1]['gate_sequence'][-1]['discontinuous']
 assert not cases[2]['gate_sequence'][-1]['discontinuous']
 assert cases[2]['gate_sequence'][-1]['value']==1.8
 tests=[]
 for _ in range(14):
  pp=rng.dirichlet([3,3,3]);k=float(rng.uniform(.03,.55));gamma=float(rng.uniform(.7,.99))
  claimed=ctl(pp,k,gamma);direct,res,sts=direct_ctl(pp,k,gamma)
  assert abs(claimed-direct)<2e-6 and res<1e-7,(claimed,direct,res)
  tests.append({'p':pp.tolist(),'budget':k,'gamma':gamma,'formula':claimed,'direct':direct,
                'gap':abs(claimed-direct),'constraint_residual':res,'solver_statuses':sts})
 # Verify predicted saturation/absence of saturation away from their exact boundary.
 saturation=[]
 for pp in [p,np.array([.1,.65,.25]),np.array([.45,.4,.15])]:
  threshold=(1-max(pp[:2]))*LN2
  for offset in (-.01,.01):
   k=threshold+offset;value=ctl(pp,k,1.)
   assert (abs(value-1.8)<1e-9)==(offset>0)
   saturation.append({'p':pp.tolist(),'budget':k,'value':value,'threshold':threshold})
 # Same sender trembles generate BOTH off-path beliefs without type 2 double spending.
 trembles=[]
 for eps in (1e-2,1e-4,1e-6):
  mu12=np.array([.5,.5,0]);mu23=np.array([0,0,1.])
  s12=np.array([eps*mu12[0]/p[0]+eps**2,eps*mu12[1]/p[1]+eps**2,0])
  s23=np.array([0,eps*mu23[1]/p[1]+eps**2,eps*mu23[2]/p[2]+eps**2])
  assert np.all(s12+s23<1)
  b12=p*s12/(p@s12);b23=p*s23/(p@s23)
  trembles.append({'epsilon':eps,'posterior12':b12.tolist(),'posterior23':b23.tolist()})
 assert max(abs(np.array(trembles[-1]['posterior12'])-mu12))<1e-6
 assert max(abs(np.array(trembles[-1]['posterior23'])-mu23))<1e-6
 result={'status':'passed','seed':20260919,'numpy':np.__version__,'scipy':scipy.__version__,
  'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
  'support_cases':cases,'direct_12_cell_checks':tests,'saturation_checks':saturation,
  'common_sender_trembles':trembles,'exact':exact_counterexamples()}
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
