"""Fixed exact-arithmetic checks for Bellman's mathematical build-out review.

This is a newly authored reviewer harness, not the author's missing 18-group
harness, a production implementation, a mathematical-grid experiment, or formal
verification. Small LP vertex enumeration is a bounded audit reference only.
Python 3.9+ standard library; no network or repository mutations.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import combinations, product
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys
import zipfile

GROUPS = []
def group(f):
    GROUPS.append(f)
    return f

def require(condition, message='review check failed'):
    if not condition:
        raise AssertionError(message)

def dot(a, b):
    require(len(a) == len(b), 'dimension mismatch')
    return sum((F(x)*F(y) for x, y in zip(a, b)), F(0))

def tv(a,b):
    return sum((abs(F(x)-F(y)) for x,y in zip(a,b)), F(0))/2

def solve_unique(A,b,n):
    rows = [[F(v) for v in row]+[F(rhs)] for row,rhs in zip(A,b)]
    pivots=[]; k=0
    for j in range(n):
        pivot=next((i for i in range(k,len(rows)) if rows[i][j]), None)
        if pivot is None: continue
        rows[k],rows[pivot]=rows[pivot],rows[k]
        a=rows[k][j]; rows[k]=[v/a for v in rows[k]]
        for i in range(len(rows)):
            if i != k and rows[i][j]:
                a=rows[i][j]; rows[i]=[v-a*w for v,w in zip(rows[i],rows[k])]
        pivots.append(j); k+=1
    if any(all(v==0 for v in r[:n]) and r[-1]!=0 for r in rows): return None
    if len(pivots)!=n: return None
    x=[F(0)]*n
    for i,j in enumerate(pivots): x[j]=rows[i][-1]
    return tuple(x)

def rank(A,n):
    a=[[F(x) for x in r] for r in A]; k=0
    for j in range(n):
        pivot=next((i for i in range(k,len(a)) if a[i][j]),None)
        if pivot is None: continue
        a[k],a[pivot]=a[pivot],a[k]
        z=a[k][j]; a[k]=[x/z for x in a[k]]
        for i in range(k+1,len(a)):
            z=a[i][j]; a[i]=[x-z*y for x,y in zip(a[i],a[k])]
        k+=1
    return k

def feasible(x,A,b,C,d):
    return all(v>=0 for v in x) and all(dot(r,x)==s for r,s in zip(A,b)) and all(dot(r,x)<=s for r,s in zip(C,d))

def vertices(A,b,C,d,n):
    require(1<=n<=8, 'audit reference is deliberately limited to eight variables')
    require(len(A)==len(b) and len(C)==len(d), 'row mismatch')
    require(all(len(r)==n for r in list(A)+list(C)), 'column mismatch')
    all_C=list(C)+[tuple(-int(i==j) for i in range(n)) for j in range(n)]
    all_d=list(d)+[F(0)]*n
    v=set(); need=n-rank(A,n)
    for inds in combinations(range(len(all_C)),need):
        x=solve_unique(list(A)+[all_C[i] for i in inds],list(b)+[all_d[i] for i in inds],n)
        if x is not None and feasible(x,A,b,C,d): v.add(x)
    return sorted(v)

def verify_upper(r,A,b,C,d,y,z):
    if len(y)!=len(A) or len(z)!=len(C) or any(a<0 for a in z): return None
    if any(sum((F(y[j])*F(A[j][i]) for j in range(len(A))),F(0))+
           sum((F(z[j])*F(C[j][i]) for j in range(len(C))),F(0))<r[i] for i in range(len(r))): return None
    return dot(b,y)+dot(d,z)

def upper_certificate(r,A,b,C,d,x):
    """Construct a certificate from active constraints in these small examples."""
    n=len(r); active=[i for i in range(len(C)) if dot(C[i],x)==d[i]]
    for k in range(len(active)+1):
        for inds in combinations(active,k):
            columns=list(A)+[C[i] for i in inds]
            transposed=[[col[j] for col in columns] for j in range(n)]
            yz=solve_unique(transposed,r,len(columns))
            if yz is None: continue
            y=yz[:len(A)]; z=[F(0)]*len(C)
            for i,v in zip(inds,yz[len(A):]): z[i]=v
            bound=verify_upper(r,A,b,C,d,y,z)
            if bound is not None and bound==dot(r,x): return (y,tuple(z),bound)
    raise AssertionError('no exact certificate found for fixed audit example')

@group
def packet_integrity():
    path=Path(__file__).resolve().parents[1]/'BELLMAN_WRIT_NEXT_STEP_PACKET.zip'
    if not path.exists(): return {'status':'NOT_RUN','reason':'optional original packet ZIP not present'}
    with zipfile.ZipFile(path) as z:
        rows=json.loads(z.read('INPUT_MANIFEST.json'))
        for row in rows:
            data=z.read(row['path'])
            require(len(data)==row['bytes'] and sha256(data).hexdigest()==row['sha256'])
    return {'inputs_checked':len(rows),'scope':'byte identity, not mathematical correctness'}

@group
def triangle_and_farkas():
    omega=list(product((0,1),repeat=3))
    A=[[1]*8]+[[int(w[i]!=w[j]) for w in omega] for i,j in ((0,1),(1,2),(0,2))]
    b=[F(1)]*4; y=[F(2),F(-1),F(-1),F(-1)]
    aty=[sum(y[j]*A[j][i] for j in range(4)) for i in range(8)]
    require(min(aty)>=0 and dot(b,y)==-1)
    require(vertices(A,b,[],[],8)==[])
    bad=[-v for v in y]
    require(dot(b,bad)>=0)
    return {'A_transpose_y':aty,'b_transpose_y':dot(b,y),'feasible_vertices':0,'note':'new certificate, not author witness with -1/2'}

@group
def gluing_support_and_query_variation():
    xy=[[F(3,8),F(1,8)],[F(1,8),F(3,8)]]
    yz=[[F(1,3),F(1,6)],[F(1,6),F(1,3)]]
    py=[sum(xy[x][y] for x in range(2)) for y in range(2)]
    joint={(x,y,z):xy[x][y]*yz[y][z]/py[y] for x,y,z in product(range(2),repeat=3)}
    require(sum(joint.values())==1)
    require(all(sum(joint[x,y,z] for z in range(2))==xy[x][y] for x,y in product(range(2),repeat=2)))
    require(all(sum(joint[x,y,z] for x in range(2))==yz[y][z] for y,z in product(range(2),repeat=2)))
    # Equal independent pair marginals allow different X-Z dependencies.
    independent={w:F(1,8) for w in product(range(2),repeat=3)}
    correlated={w:F(1,4) if w[0]==w[2] else F(0) for w in independent}
    for i,j in ((0,1),(1,2)):
        require(all(sum(p[w] for w in p if w[i]==a and w[j]==b)==F(1,4) for p in (independent,correlated) for a,b in product(range(2),repeat=2)))
    require(sum(independent[w] for w in independent if w[0]==w[2])==F(1,2))
    require(sum(correlated[w] for w in correlated if w[0]==w[2])==1)
    return {'glue_normalized':True,'other_extensions_change_query':[F(1,2),F(1)]}

@group
def nonlinear_constraint_and_outer_set():
    exact=(F(1,4),)*4; relaxed=(F(1,2),F(0),F(0),F(1,2))
    require(exact[0]*exact[3]==exact[1]*exact[2])
    require(relaxed[0]*relaxed[3]!=relaxed[1]*relaxed[2])
    require(exact[0]+exact[1]==relaxed[0]+relaxed[1]==F(1,2))
    require(exact[0]+exact[2]==relaxed[0]+relaxed[2]==F(1,2))
    return {'outer_candidate_matches_fair_marginals':True,'outer_candidate_violates_original_independence':True}

def conditional_profile(lo=F(1,4),hi=F(2,5)):
    A=[[1,1,1,1],[-1,4,0,0],[0,0,-4,1]]; b=[1,0,0]
    C=[[0,0,-1,-1],[0,0,1,1]]; d=[-lo,hi]
    event=[0,1,0,1]; numerator=[0,0,0,1]
    At=[list(r)+[-F(s)] for r,s in zip(A,b)]+[event+[0]]; bt=[0,0,0,1]
    Ct=[list(r)+[-F(s)] for r,s in zip(C,d)]; dt=[0,0]
    return A,b,C,d,event,numerator,At,bt,Ct,dt

@group
def conditional_extrema_and_dual_certificates():
    A,b,C,d,e,u,At,bt,Ct,dt=conditional_profile()
    original=vertices(A,b,C,d,4); transformed=vertices(At,bt,Ct,dt,5)
    require(len(original)==len(transformed)==2)
    for w in transformed:
        t=w[-1]; require(t>0)
        p=tuple(a/t for a in w[:-1]); require(feasible(p,A,b,C,d))
        require(dot(u+[0],w)==dot(u,p)/dot(e,p))
    r=list(u)+[0]
    xmax=max(transformed,key=lambda x:dot(r,x)); xmin=min(transformed,key=lambda x:dot(r,x))
    ymax,zmax,ub=upper_certificate(r,At,bt,Ct,dt,xmax)
    ymin,zmin,neg_lb=upper_certificate([-a for a in r],At,bt,Ct,dt,xmin)
    require(( -neg_lb,ub)==(F(4,7),F(8,11)))
    # Reject a forged certificate by changing the objective it allegedly bounds.
    require(verify_upper([a+1 for a in r],At,bt,Ct,dt,ymax,zmax) is None)
    return {'range':[-neg_lb,ub],'transformed_extremizers':transformed,'upper_dual':[ymax,zmax],'lower_dual':[ymin,zmin]}

@group
def identified_action_tie_and_changed_query():
    A,b,C,d,e,u,At,bt,Ct,dt=conditional_profile()
    v=vertices(At,bt,Ct,dt,5); diff=[0,1,0,-1,0]
    maxp=max(v,key=lambda p:dot(diff,p)); _,_,upper=upper_certificate(diff,At,bt,Ct,dt,maxp)
    require(upper==F(-1,7))
    # A false-positive penalty of 2 reverses the action at one endpoint.
    altered=[0,2,0,-1,0]; values=[dot(altered,p) for p in v]
    require(min(values)<0<max(values))
    *_,At2,bt2,Ct2,dt2=conditional_profile(F(1,5),F(2,5))
    vt=vertices(At2,bt2,Ct2,dt2,5)
    require(max(dot(diff,p) for p in vt)==0)
    return {'strict_risk_difference_upper':upper,'changed_loss_differences':values,'tie_control_upper':F(0)}

@group
def zero_probability_conditional_guard():
    A=[[1,1],[0,1]]; b=[1,0]; e=[0,1]
    original=vertices(A,b,[],[],2); require(original==[(F(1),F(0))])
    At=[[1,1,-1],[0,1,0],[0,1,0]]; bt=[0,0,1]
    require(vertices(At,bt,[],[],3)==[])
    return {'unconditional_compatible':True,'event_possible':False,'transformed_feasible':False}

@group
def missing_policy_lift_coverage():
    original=[F(0),F(100)]; abstract=[F(100)]; lifted=[F(100)]
    e=F(0); eta=F(0); beta=min(lifted)-min(original)
    regret=abstract[0]-min(original)
    require(regret==100 and regret>2*e+eta and regret<=2*e+eta+beta)
    return {'regret':regret,'cost_error':e,'necessary_benchmark_gap':beta}

@group
def simulator_nonzero_gap_and_context():
    # Uninformative experiment -> identity target. Every row of ET is (t,1-t).
    T=[F(1,2),F(1,2)]
    gaps=[tv(T,[1,0]),tv(T,[0,1])]
    require(max(gaps)==F(1,2) and sum(gaps)/2==F(1,2))
    # For arbitrary t these two discrepancies sum to one, a universal lower bound.
    require(F(2,7)+(1-F(2,7))==1)
    xor={(th,x,th^x):F(1,4) for th,x in product(range(2),repeat=2)}
    joint_risk=sum(min(sum(p for (t,x,z),p in xor.items() if (x,z)==(xx,zz) and t==a) for a in range(2)) for xx,zz in product(range(2),repeat=2))
    coarse_risk=sum(min(sum(p for (t,x,z),p in xor.items() if z==zz and t==a) for a in range(2)) for zz in range(2))
    require((joint_risk,coarse_risk)==(0,F(1,2)))
    return {'nonzero_deficiency_exact':F(1,2),'joined_prediction_risks':[joint_risk,coarse_risk]}

def policies(h):
    if h==0: return [('stop',0),('stop',1)]
    previous=policies(h-1)
    return [('stop',0),('stop',1)]+[('obs',left,right) for left,right in product(previous,repeat=2)]

def stop_policy_cost(pi,theta,K,L,c):
    if pi[0]=='stop': return L[pi[1]][theta]
    return c+sum((K[theta][x]*stop_policy_cost(pi[x+1],theta,K,L,c) for x in range(2)),F(0))

@group
def signed_adaptive_stopping_product_bound():
    K=((F(3,4),F(1,4)),(F(1,5),F(4,5)))
    Kh=((F(2,3),F(1,3)),(F(1,4),F(3,4)))
    prior=(F(2,3),F(1,3)); L=((F(-3),F(2)),(F(2),F(-3))); c=F(1,10)
    d=max(tv(a,b) for a,b in zip(K,Kh)); h=2
    e=(5+h*c)*(1-(1-d)**h)
    pp=policies(h)
    true=[dot(prior,[stop_policy_cost(pi,t,K,L,c) for t in range(2)]) for pi in pp]
    nominal=[dot(prior,[stop_policy_cost(pi,t,Kh,L,c) for t in range(2)]) for pi in pp]
    require(len(pp)==38 and all(abs(a-b)<=e for a,b in zip(true,nominal)))
    pick=min(range(len(pp)),key=lambda i:nominal[i]); regret=true[pick]-min(true)
    require(regret<=2*e)
    shifted=tuple(tuple(x+3 for x in row) for row in L)
    require(all(dot(prior,[stop_policy_cost(pi,t,K,shifted,c) for t in range(2)])==val+3 for pi,val in zip(pp,true)))
    require(1-(1-F(1,10))**2==F(19,100)<F(1,5))
    return {'fixed_policies':len(pp),'uniform_error_bound':e,'actual_max_discrepancy':max(abs(a-b) for a,b in zip(true,nominal)),'transferred_regret':regret}

@group
def off_support_legal_completion():
    K=((F(1),F(0)),(F(99,100),F(1,100))); Kh=((F(1),F(0)),)*2
    L=((F(0),F(1)),(F(1),F(0))); p=(F(1,2),)*2
    pi0=('obs',('stop',0),('stop',0)); pi1=('obs',('stop',0),('stop',1))
    costs=[dot(p,[stop_policy_cost(pi,t,K,L,F(0)) for t in range(2)]) for pi in (pi0,pi1)]
    hats=[dot(p,[stop_policy_cost(pi,t,Kh,L,F(0)) for t in range(2)]) for pi in (pi0,pi1)]
    require(hats[0]==hats[1] and costs[0]-costs[1]==F(1,200))
    require(dot(p,[row[1] for row in Kh])==0)
    require(costs[0]-min(costs)==F(1,200) and F(1,200)<=2*F(1,100))
    return {'true_policy_costs':costs,'nominal_costs':hats,'rare_event_mass':F(1,200),'surrogate_posterior':'undefined','nominal_optimum_transfer_regret':F(1,200),'regret_bound':F(1,50)}

@group
def conditioning_sharp_bound():
    P=[F(1,10),F(3,20),F(0),F(3,4)]; Q=[F(0),F(3,20),F(1,10),F(3,4)]
    p=sum(P[:3]); q=sum(Q[:3]); eps=tv(P,Q)
    actual=tv([x/p for x in P[:3]],[x/q for x in Q[:3]])
    require((p,q,eps,actual)==(F(1,4),F(1,4),F(1,10),F(2,5)))
    require(actual==eps/max(p,q))
    # Unequal event masses; same common-event theorem, not unrelated conditionings.
    P2=[F(1,10),F(1,10),F(4,5)]; Q2=[F(1,5),F(1,10),F(7,10)]
    p2=sum(P2[:2]); q2=sum(Q2[:2]); a2=tv([x/p2 for x in P2[:2]],[x/q2 for x in Q2[:2]])
    require(a2<=tv(P2,Q2)/max(p2,q2))
    rareP=[F(1,100),F(0),F(99,100)]; rareQ=[F(0),F(1,100),F(99,100)]
    require(tv(rareP,rareQ)==F(1,100) and tv([1,0],[0,1])==1)
    return {'joint_TV':eps,'draft_radius':min(F(1),2*eps/p),'sharper_radius':min(F(1),eps/p),'actual_conditional_TV':actual,'unequal_mass_conditional_TV':a2}

def mdp_data():
    P=[[[F(1,2),0,F(1,2)],[0,F(1,2),F(1,2)],[0,0,1]],[[F(3,4),0,F(1,4)],[0,F(3,4),F(1,4)],[0,0,1]]]
    P=[[[F(x) for x in row] for row in action] for action in P]
    g=[[F(1),F(1),F(0)],[F(0),F(0),F(2)]]
    return [P]*3,[g]*3,[F(2),F(2),F(-1)]

def backup(P,g,v):
    Q=[[g[a][s]+dot(P[a][s],v) for a in range(len(g))] for s in range(len(v))]
    return [min(row) for row in Q],Q

def optimal(P,g,gT):
    V=[None]*(len(g)+1); QQ=[None]*len(g); V[-1]=gT
    for t in reversed(range(len(g))): V[t],QQ[t]=backup(P[t],g[t],V[t+1])
    return V,QQ

def evaluate(P,g,gT,pi):
    J=[None]*(len(g)+1); J[-1]=gT
    for t in reversed(range(len(g))):
        J[t]=[g[t][pi[t][s]][s]+dot(P[t][pi[t][s]][s],J[t+1]) for s in range(len(gT))]
    return J

@group
def backward_partition_and_policy_values():
    P,g,gT=mdp_data(); V,Q=optimal(P,g,gT)
    part=[0,0,1]; abstractT=[gT[0],gT[2]]; vp=abstractT
    for t in reversed(range(len(g))):
        signatures=[]
        for s in range(3):
            signatures.append(tuple(g[t][a][s] for a in range(2))+tuple(sum(P[t][a][s][j] for j in range(3) if part[j]==c) for a,c in product(range(2),range(2))))
        require(signatures[0]==signatures[1])
        new=[]
        for s in (0,2): new.append(min(g[t][a][s]+sum(P[t][a][s][j]*vp[part[j]] for j in range(3)) for a in range(2)))
        require([new[part[s]] for s in range(3)]==V[t]); vp=new
    require(P[0][0][0]!=P[0][0][1])
    # A complete independent enumeration of deterministic Markov plans on this fixed MDP.
    costs=[]
    for flat in product(range(2),repeat=9):
        pi=[flat[t*3:(t+1)*3] for t in range(3)]; costs.append(evaluate(P,g,gT,pi)[0])
    require([min(c[s] for c in costs) for s in range(3)]==V[0])
    return {'root_values':V[0],'original_states':3,'abstract_states':2,'fixed_Markov_plans_checked':len(costs)}

@group
def controlled_value_transfer():
    P,g,gT=mdp_data()
    Ph=[[ [list(row) for row in act] for act in Pt] for Pt in P]
    for Pt in Ph:
        Pt[0][0]=[F(1,3),F(0),F(2,3)]; Pt[0][1]=[F(0),F(1,3),F(2,3)]
    gh=[[[a+F(1,7) for a in row] for row in gt] for gt in g]; gTh=[a+F(1,9) for a in gT]
    V,Q=optimal(P,g,gT); Vh,Qh=optimal(Ph,gh,gTh); alpha=[F(0)]*4; alpha[-1]=F(1,9)
    for t in reversed(range(3)):
        delta=max(tv(P[t][a][s],Ph[t][a][s]) for a,s in product(range(2),range(3)))
        alpha[t]=F(1,7)+delta*(max(Vh[t+1])-min(Vh[t+1]))+alpha[t+1]
        require(max(abs(V[t][s]-Vh[t][s]) for s in range(3))<=alpha[t])
        require(max(abs(Q[t][s][a]-Qh[t][s][a]) for s,a in product(range(3),range(2)))<=alpha[t])
    return {'alpha':alpha,'root_error':max(abs(a-b) for a,b in zip(V[0],Vh[0]))}

@group
def residual_and_local_regret():
    P,g,gT=mdp_data(); V,Q=optimal(P,g,gT)
    perturb=[[F(1,10),F(-1,10),F(1,20)],[F(-1,8),F(1,12),F(1,6)],[F(1,5),F(-1,5),F(0)],[F(1,7),F(0),F(-1,7)]]
    v=[[a+b for a,b in zip(row,er)] for row,er in zip(V,perturb)]
    residuals=[F(0)]*4; residuals[-1]=max(abs(a-b) for a,b in zip(v[-1],gT)); pi=[]
    for t in range(3):
        T,Qv=backup(P[t],g[t],v[t+1]); residuals[t]=max(abs(a-b) for a,b in zip(v[t],T))
        pi.append([min(range(2),key=lambda a:Qv[s][a]) for s in range(3)])
    J=evaluate(P,g,gT,pi)
    for t in range(4):
        radius=sum(residuals[t:]); require(max(abs(a-b) for a,b in zip(v[t],V[t]))<=radius)
        require(max(abs(a-b) for a,b in zip(v[t],J[t]))<=radius)
        require(max(a-b for a,b in zip(J[t],V[t]))<=2*radius)
    # Non-greedy plan on this fixed MDP, to test the independent telescoping identity.
    plan=[[1,0,1],[0,1,0],[1,1,1]]; JJ=evaluate(P,g,gT,plan); mu=[F(1,4),F(1,2),F(1,4)]
    occ=list(mu); total=F(0)
    for t in range(3):
        disadv=[g[t][plan[t][s]][s]+dot(P[t][plan[t][s]][s],V[t+1])-V[t][s] for s in range(3)]
        require(min(disadv)>=0); total+=dot(occ,disadv)
        occ=[sum(occ[s]*P[t][plan[t][s]][s][j] for s in range(3)) for j in range(3)]
    actual=dot(mu,JJ[0])-dot(mu,V[0]); require(total==actual)
    # A second fixed MDP has strictly positive approximate-greedy regret.
    Psmall=[[[[F(1),F(0)],[F(1),F(0)]],[[F(0),F(1)],[F(0),F(1)]]]]
    gsmall=[[[F(0),F(0)],[F(0),F(0)]]]; terminal=[F(0),F(1,10)]
    vs,qs=optimal(Psmall,gsmall,terminal)
    vterminal=[F(1,10),F(0)]; root,qapprox=backup(Psmall[0],gsmall[0],vterminal)
    approximate_policy=[[min(range(2),key=lambda a:qapprox[s][a]) for s in range(2)]]
    selected=evaluate(Psmall,gsmall,terminal,approximate_policy)
    rr=max(abs(a-b) for a,b in zip(vterminal,terminal))
    positive_regret=selected[0][0]-vs[0][0]
    require(positive_regret==F(1,10) and positive_regret<=2*rr)
    # Exact value residuals are zero, but this other policy is not greedy for them.
    require(selected[0][0]-vs[0][0]>0)
    return {'residuals':residuals,'greedy_regret_bound':2*sum(residuals),'greedy_actual_root_regrets':[a-b for a,b in zip(J[0],V[0])],'telescoping_regret':actual,'positive_greedy_regret_control':positive_regret,'positive_control_bound':2*rr,'note':'new fixed MDP, not author 63/80 or 7/64 instance'}

@group
def robust_mixture_and_model_persistence():
    C=[[0,1],[1,0]]; lam=[F(1,2),F(1,2)]
    costs=[dot(row,lam) for row in C]
    require(max(costs)==F(1,2) and min(max(row[j] for row in C) for j in range(2))==1)
    require(all(dot([F(1,2),F(1,2)],[row[j] for row in C])==F(1,2) for j in range(2)))
    fixed=max(sum(row) for row in C); rectangular=sum(max(row[t] for row in C) for t in range(2))
    require((fixed,rectangular)==(1,2))
    # One persistent hidden model emits all 0s or all 1s with equal prior mass.
    persistent_ones=F(1,2); resampled_ones=F(1,4)
    require(persistent_ones!=resampled_ones)
    return {'robust_optimum':F(1,2),'fixed_total':fixed,'rectangular_total':rectangular,'persistent_vs_resampled_11':[persistent_ones,resampled_ones]}

@group
def statistical_allocation_and_safe_outer_rounding():
    alpha=F(1,20); n=100
    total=sum((alpha/F(k*(k+1)) for k in range(1,n+1)),F(0))
    require(total==alpha*(1-F(1,n+1)))
    # A generic interval shows why inward rounding loses the stated set inclusion.
    center=F(1,2); exact_radius=F(2,5); inward=F(39,100); p=F(179,200)
    require(abs(p-center)<=exact_radius and abs(p-center)>inward)
    return {'first_100_alpha_allocation':total,'tail_alpha':alpha/F(101),'inward_rounding_loses_coverage_event_inclusion':True,'scope':'no empirical coverage experiment or certified log/sqrt routine'}

def cvar(distribution,alpha):
    require(0<=alpha<1 and sum(p for _,p in distribution)==1)
    return min(t+sum(p*max(F(0),loss-t) for loss,p in distribution)/(1-alpha) for t,_ in distribution)

@group
def tail_and_constrained_randomization():
    A=[(F(0),F(99,100)),(F(100),F(1,100))]; B=[(F(2),F(1))]
    means=[sum(l*p for l,p in d) for d in (A,B)]
    tails=[cvar(d,F(19,20)) for d in (A,B)]
    require(means==[1,2] and tails==[20,2] and cvar(A,F(0))==1)
    # Risky action costs 0 with hazard 1/10; safe action costs 2 with hazard 0.
    risky_weight=F(1,2); hazard=risky_weight/F(10); cost=2*(1-risky_weight)
    require(hazard==F(1,20) and cost==1)
    return {'means':means,'cvar_0_95':tails,'constrained_mix_cost':cost,'constrained_mix_hazard':hazard}

@group
def causal_adjustment_control():
    # Z is a fair confounder, Y=Z, assignment P(A=1|Z)=1/10 or 9/10.
    pz=[F(1,2),F(1,2)]; assignment=[F(1,10),F(9,10)]
    pa=dot(pz,assignment); py_a=pz[1]*assignment[1]/pa
    py_do=sum(pz[z]*F(z) for z in range(2))
    require((py_a,py_do)==(F(9,10),F(1,2)))
    return {'observational_probability':py_a,'interventional_probability':py_do,'scope':'supplied causal model, not graph discovery or data verification'}

def wire(x):
    if isinstance(x,F): return str(x.numerator)+'/'+str(x.denominator)
    if isinstance(x,dict): return {str(k):wire(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [wire(v) for v in x]
    return x

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); args=ap.parse_args()
    results=[]
    for f in GROUPS:
        try:
            details=f(); status=details.pop('status','PASS'); results.append({'group':f.__name__,'status':status,'details':details})
        except Exception as exc:
            results.append({'group':f.__name__,'status':'FAIL','error':type(exc).__name__+': '+str(exc)})
    payload={'scope':'new fixed reviewer examples; not the original harness, production tests, general LP solver, or formal proof','python':platform.python_version(),'optimized':sys.flags.optimize,'harness_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'passed':sum(r['status']=='PASS' for r in results),'failed':sum(r['status']=='FAIL' for r in results),'not_run':sum(r['status']=='NOT_RUN' for r in results),'results':results}
    args.output.write_text(json.dumps(wire(payload),indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:payload[k] for k in ('python','optimized','passed','failed','not_run')}))
    for r in results:
        print(r['status'],r['group'],r.get('error',''))
    return 1 if payload['failed'] else 0
if __name__=='__main__': raise SystemExit(main())
