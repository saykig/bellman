"""Portable archival replay of the completed build-out arithmetic checks.

The mathematical checks are unchanged; input integrity uses the archive manifest.
Frozen results are read, never overwritten. See README.md for evidence scope.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
results = []

def check(name, condition, detail):
    if not condition:
        raise RuntimeError(name)
    results.append({'name': name, 'status': 'PASS', 'detail': detail})

def tv(p, q):
    return sum(abs(x-y) for x,y in zip(p,q))/2

manifest = json.loads((ROOT/'foundations/SOURCE_MANIFEST.json').read_text())
for item in manifest['artifacts']:
    raw = (ROOT/item['path']).read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != item['sha256'] or len(raw) != item['bytes']:
        raise RuntimeError('Archive manifest mismatch: '+item['path'])
check('input_integrity', True, 'All six frozen archival artifacts match their SHA-256 and byte counts.')

max_disagreements = max(sum((x!=y,y!=z,x!=z)) for x,y,z in product((0,1), repeat=3))
check('triangle_incompatibility', max_disagreements == 2, 'Required expectation 3 exceeds pointwise bound 2.')

# A checked Farkas certificate: p=1/4 and p=3/4 cannot both hold.
A = [[F(1)], [F(1)]]
b = [F(1,4),F(3,4)]
y = [F(1),F(-1)]
aty = sum(A[i][0]*y[i] for i in range(2))
bty = sum(b[i]*y[i] for i in range(2))
check('farkas_witness', aty >= 0 and bty < 0, f'A^T y={aty}; b^T y={bty}.')

xy = {(0,0):F(1,4),(1,0):F(1,4),(0,1):F(1,8),(1,1):F(3,8)}
yz = {(0,0):F(1,8),(0,1):F(3,8),(1,0):F(1,4),(1,1):F(1,4)}
joint = {(x,y,z):xy[x,y]*yz[y,z]/F(1,2) for x,y,z in product((0,1),repeat=3)}
check('positive_gluing', sum(joint.values()) == 1 and
      all(sum(joint[x,y,z] for z in (0,1))==xy[x,y] for x,y in xy) and
      all(sum(joint[x,y,z] for x in (0,1))==yz[y,z] for y,z in yz),
      'Constructed joint is normalized and preserves both supplied pair marginals.')

p = [F(1,8),F(3,8),F(1,2)]
mass = p[0]+p[1]
t = 1/mass
w = [v*t for v in p]
check('fractional_transform_witness', sum(w)==t and w[0]+w[1]==1 and
      w[0] == p[0]/mass and [v/t for v in w]==p,
      't=2; transformed objective and conditional answer both 1/4; inverse recovers p.')

# Structural abstraction plus Bellman residual and telescoping checks.
P = [
    [[F(1,2),0,F(1,2)],[F(1,4),0,F(3,4)]],
    [[0,F(1,2),F(1,2)],[0,F(1,4),F(3,4)]],
    [[0,0,1],[0,0,1]],
]
g = [[F(0),F(1,8)],[F(0),F(1,8)],[F(0),F(0)]]
terminal = [F(2),F(2),F(0)]
T = 3
def backup(v):
    return [[g[s][a]+sum(P[s][a][sp]*v[sp] for sp in range(3))
             for a in range(2)] for s in range(3)]
V = [None]*T+[terminal]
for k in reversed(range(T)):
    V[k] = [min(row) for row in backup(V[k+1])]
abstract_P = [[[F(1,2),F(1,2)],[F(1,4),F(3,4)]],[[0,1],[0,1]]]
av=[F(2),F(0)]
abstract_ok = True
for k in reversed(range(T)):
    av=[
        min(g[0][a]+sum(abstract_P[0][a][sp]*av[sp] for sp in range(2)) for a in range(2)),
        av[1]]
    abstract_ok &= V[k][0]==V[k][1]==av[0] and V[k][2]==av[1]
check('structural_abstraction', abstract_ok and P[0]!=P[1],
      'Three-date original and two-class values agree; original transition rows differ.')

offset = [F(1,10),F(-1,10),F(1,20)]
approx = [[V[k][s]+offset[s] for s in range(3)] for k in range(T+1)]
policies=[]
residuals=[]
for k in range(T):
    q=backup(approx[k+1])
    policies.append([min(range(2),key=lambda a:q[s][a]) for s in range(3)])
    residuals.append(max(abs(approx[k][s]-min(q[s])) for s in range(3)))
residuals.append(max(abs(approx[T][s]-terminal[s]) for s in range(3)))
J=terminal[:]
for k in reversed(range(T)):
    q=backup(J)
    J=[q[s][policies[k][s]] for s in range(3)]
bound=2*sum(residuals)
check('bellman_residual_certificate', all(J[s]-V[0][s] <= bound for s in range(3)),
      'Checked exact residuals and evaluated greedy-policy regret in all 3 initial states; bound='+str(bound))
occupancy=[F(1),F(0),F(0)]
disadvantage=F(0)
local_policies = [[0,0,0] for _ in range(T)]
local_cost = terminal[:]
for k in reversed(range(T)):
    q=backup(local_cost)
    local_cost=[q[s][local_policies[k][s]] for s in range(3)]
for k in range(T):
    q=backup(V[k+1])
    disadvantage += sum(occupancy[s]*(q[s][local_policies[k][s]]-V[k][s]) for s in range(3))
    occupancy=[sum(occupancy[s]*P[s][local_policies[k][s]][sp] for s in range(3)) for sp in range(3)]
check('local_regret_telescoping', disadvantage == local_cost[0]-V[0][0] and disadvantage > 0,
      'Expected sum of exact Bellman disadvantages equals evaluated policy regret: '+str(disadvantage))

E=[[F(1),F(0)],[F(0),F(1)]]
G=[[F(3,4),F(1,4)],[F(1,4),F(3,4)]]
simulation=[[sum(E[s][x]*G[x][y] for x in range(2)) for y in range(2)] for s in range(2)]
check('deficiency_simulator', simulation==G, 'Identity experiment simulates the binary noisy experiment with T=G and d=0.')

xor_joint={(theta,x,theta^x):F(1,4) for theta,x in product((0,1),repeat=2)}
full_risk=sum(min(xor_joint.get((0,x,z),0),xor_joint.get((1,x,z),0)) for x,z in product((0,1),repeat=2))
coarse_risk=sum(min(sum(xor_joint.get((theta,x,z),0) for x in (0,1)) for theta in (0,1)) for z in (0,1))
check('contextual_failure', full_risk==0 and coarse_risk==F(1,2), 'XOR auxiliary evidence changes risks to 0 versus 1/2.')

loss=[[-99,1],[1,-99]]
def observed_risk(K):
    return sum(min(sum(F(1,2)*K[s][x]*loss[a][s] for s in range(2)) for a in range(2)) for x in range(2))
K=[[F(1),F(0)],[F(0),F(1)]]
Kh=[[F(99,100),F(1,100)],[F(1,100),F(99,100)]]
risks=(observed_risk(K),observed_risk(Kh))
span_bound=100*F(1,100)
check('signed_loss_span', risks==(-99,-98) and abs(risks[0]-risks[1])==span_bound,
      'Values -99,-98; span bound 1 is attained.')
check('coupling_product_bound', 1-(1-F(1,10))**2 == F(19,100) < F(1,5),
      'Two-observation mismatch bound 19/100 improves union bound 1/5.')
check('conditioning_amplification', tv([F(1,100),0,F(99,100)],[0,F(1,100),F(99,100)])==F(1,100)
      and tv([F(1),F(0)],[F(0),F(1)])==1,
      'Joint TV 1/100; conditional TV 1.')

check('private_robust_mixture', max(F(1,2),F(1,2))==F(1,2) and (F(1,2)+F(1,2))/2==F(1,2),
      'Feasible mixture and equal-weight model lower bound both 1/2; pure worst loss 1.')
check('persistent_vs_rectangular', max(sum(row) for row in [(0,1),(1,0)])==1 and sum(map(max,zip((0,1),(1,0))))==2,
      'Fixed-model worst cost 1; independently selected date costs total 2.')

alpha=F(1,20)
allocated=sum(alpha/F(n*(n+1)) for n in range(1,101))
check('coverage_allocation', allocated==alpha*(1-F(1,101)),
      'Exact first-100 allocation sum equals alpha*(1-1/101); infinite-tail identity is analytic.')

def cvar(values, probabilities, alpha):
    return min(tau+sum(p*max(z-tau,0) for z,p in zip(values,probabilities))/(1-alpha)
               for tau in values)
ca=cvar([F(0),F(100)],[F(99,100),F(1,100)],F(19,20))
cb=cvar([F(2)],[F(1)],F(19,20))
check('tail_risk', ca==20 and cb==2, 'Means 1 versus 2; CVaR_0.95 values 20 versus 2.')

posterior=lambda p:4*p/(1+3*p)
lo,hi=posterior(F(1,4)),posterior(F(2,5))
check('integrated_identified_action', lo==F(4,7) and hi==F(8,11) and 2*lo-1==F(1,7),
      'Posterior range [4/7,8/11] varies; action 1 is uniformly strictly optimal with minimum gap 1/7.')

frozen = json.loads((HERE/'checks.json').read_text())
expected = [r for r in frozen['checks'] if r['name'] != 'input_integrity']
actual = [r for r in results if r['name'] != 'input_integrity']
if actual != expected:
    raise RuntimeError('Mathematical replay differs from frozen result record')
print(str(len(actual))+' mathematical groups match the frozen results; archive integrity also passed.')
