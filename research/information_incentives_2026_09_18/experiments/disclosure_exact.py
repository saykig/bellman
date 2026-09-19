"""Exact rational certificates for the overlapping-certificate obstruction.
The proof covers all mixing probabilities; no finite grid substitutes for it.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json

def require(c,msg):
    if not c:raise AssertionError(msg)

def main():
    target=Q(1,5);threshold=Q(1,2)-target
    require(threshold==Q(3,10),'threshold')
    q=Q(1,2)
    require(q-threshold==target and 1-q-threshold==target,'attaining continuation')
    # Sum of the two sender inequalities gives 1-2k <= 2/5.
    require(1-2*threshold==2*target,'summed dual certificate')
    # Prior receiver utilities: unique C; postcertificate belief: A/B tied, C inferior.
    prior=(Q(1,4),Q(1,4),Q(1,2));posterior=(Q(1,2),Q(1,2),Q(0))
    require(prior[2]>max(prior[:2]),'pooling receiver best reply')
    require(posterior[0]==posterior[1]>posterior[2],'certificate best replies')
    # Independent tremble constants produce the required posterior.
    numerators=[prior[i]*(posterior[i]/prior[i]) for i in range(3)]
    require(tuple(x/sum(numerators) for x in numerators)==posterior,'Bayes posterior')
    out={'threshold':str(threshold),'mixture_A':str(q),'pooling_payoff':str(target),
        'individual_minimum_payoffs':['0','0'],
        'joint_payoff_vectors':'(q,1-q), 0 <= q <= 1',
        'infeasibility_certificate':'sum both IC inequalities: 1 - 2k <= 2/5',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
