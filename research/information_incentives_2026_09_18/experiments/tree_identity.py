"""Check the augmented-tree KL identity on a nonbinary hidden-star example."""
from collections import defaultdict
import hashlib,itertools,json,math
from pathlib import Path
import numpy as np

ATOMS=list(itertools.product(range(2),range(3),range(3)))
def marginal(q,indices):
    result=defaultdict(float)
    for a,v in q.items():result[tuple(a[i] for i in indices)]+=v
    return dict(result)
def KL(q,r):return sum(v*math.log(v/r[a]) for a,v in q.items() if v>0)
def lift(q):return {(h,x,y,int(x==0 and y==0),int(y==0)):v for (h,x,y),v in q.items()}
def check(c,s):
    if not c:raise AssertionError(s)
def main():
    rng=np.random.default_rng(9182026);records=[]
    for case in range(50):
        counts=rng.integers(1,50,len(ATOMS));q=dict(zip(ATOMS,counts/counts.sum()))
        ph=marginal(q,[0]);hx=marginal(q,[0,1]);hy=marginal(q,[0,2])
        r={(h,x,y):hx[h,x]*hy[h,y]/ph[h,] for h,x,y in ATOMS}
        lq=lift(q);lr=lift(r)
        bags=([0,1,3,4],[0,2,4]);sep=[0,4]
        root=marginal(lq,bags[0]);child=marginal(lq,bags[1]);shared=marginal(lq,sep)
        qt={}
        for h,x,y in ATOMS:
            ff=int(y==0);fr=int(x==0 and y==0)
            qt[h,x,y]=root[h,x,fr,ff]*child[h,y,ff]/shared[h,ff]
        tree=sum(KL(marginal(lq,b),marginal(lr,b)) for b in bags)-KL(marginal(lq,sep),marginal(lr,sep))
        remainder=KL(q,qt)
        error=max(abs(KL(q,r)-remainder-tree),abs(tree-KL(qt,r)))
        check(error<1e-12,'tree identity')
        check(max(abs(marginal(qt,b)[a]-v) for b in ([0,1],[0,2]) for a,v in marginal(q,b).items())<1e-12,'original marginals')
        check(abs(sum(q[a] for a in ATOMS if a[1:]==(0,0))-sum(qt[a] for a in ATOMS if a[1:]==(0,0)))<1e-12,'event preserved')
        records.append({'full_KL':KL(q,r),'projected_KL':tree,'discarded_KL':remainder,'identity_error':error})
    print(json.dumps({'cases':50,'seed':9182026,'alphabet':[2,3,3],
        'max_identity_error':max(r['identity_error'] for r in records),
        'first_witness':records[0],
        'original_clique_KL':0,'all_cases_have_positive_discarded_KL':all(r['discarded_KL']>0 for r in records),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
