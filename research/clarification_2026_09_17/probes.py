"""Small exact discriminating examples; no imports from frozen Bellman experiments."""
from fractions import Fraction
from itertools import product, combinations
from pathlib import Path
import hashlib
import json

OMEGA = tuple(product((0,1), repeat=3))  # original flip choices a,b; independent W=c
RULES = {
    'coupled': lambda a,b,c: a == b,
    'a0': lambda a,b,c: a == 0,
    'w0': lambda a,b,c: c == 0,
    'other_a0': lambda a,b,c: a == 0,
    'opposite': lambda a,b,c: a != b,
}


def family(active):
    return frozenset(m for m in OMEGA if all(RULES[j](*m) for j in active))


def signature(m, replacement=None):
    a,b,c = m
    b = b if replacement is None else replacement
    # external Z at X=0,1; Z after do(Y=0),do(Y=1); W
    return (a ^ b, 1 ^ a ^ b, b, 1 ^ b, c)


def answers(active, replacement=None):
    return sorted({signature(m, replacement) for m in family(active)})


def entails(active, claim, replacement=None):
    f = family(active)
    return bool(f) and all(claim(signature(m, replacement)) for m in f)


def main():
    do_y1_is_one = lambda s: s[3] == 1
    assert not entails({'coupled'}, do_y1_is_one)
    assert not entails({'a0'}, do_y1_is_one)
    assert entails({'coupled','a0'}, do_y1_is_one)
    active = {'coupled','a0','w0'}
    after = active - {'a0'}
    assert not entails(after, do_y1_is_one)
    assert entails(after, lambda s:s[:2] == (0,1))
    assert entails(after, lambda s:s[4] == 0)
    assert entails(active, lambda s:s[:2] == (1,0), replacement=1)
    assert entails(active, lambda s:s[4] == 0, replacement=1)
    assert not family({'coupled','opposite'})
    # Same model family cannot determine named withdrawal.
    s1, s2 = {'a0'}, {'a0','other_a0'}
    assert family(s1) == family(s2)
    assert family(s1-{'a0'}) != family(s2-{'a0'})
    # One support is insufficient: all minimal alternative supports are needed.
    labels = tuple(RULES)
    supports = []
    for size in range(len(labels)+1):
        for subset in combinations(labels,size):
            subset = set(subset)
            if entails(subset,do_y1_is_one) and not any(set(t) <= subset for t in supports):
                supports.append(sorted(subset))
    assert supports == [['a0','coupled'],['coupled','other_a0']]
    assert entails({'coupled','other_a0'},do_y1_is_one)
    # One source event repeated: the likelihood occurs once.
    prior_odds = Fraction(1)
    likelihood_ratio = Fraction(3)
    odds = prior_odds * likelihood_ratio
    once = odds/(1+odds)
    wrong_odds = odds*likelihood_ratio
    wrong = wrong_odds/(1+wrong_odds)
    assert once == Fraction(3,4) and wrong == Fraction(9,10)
    assert family(['a0','a0']) == family(['a0'])
    # Reproduce the coordinator's count on all 16 unary Boolean chains.
    fs = tuple(product((0,1),repeat=2))
    models = tuple(product(fs,repeat=2))
    def io(m):
        k,l=m
        return tuple(l[k[x]] for x in (0,1))
    same=downstream=internal=0
    for m,n in combinations(models,2):
        if io(m)!=io(n): continue
        same+=1
        downstream+=any(tuple(h[z] for z in io(m)) != tuple(h[z] for z in io(n)) for h in fs)
        internal+=any(m[1][y]!=n[1][y] for y in (0,1))
    assert (same,downstream,internal)==(32,0,20)
    m,n=((0,0),(0,0)),((0,0),(0,1))
    assert io(m)==io(n)==(0,0) and (m[1][1],n[1][1])==(0,1)
    results={
        'joint_new_consequence': {'neither_alone_entails_do_Y1_Z1':True,'together_entail':True},
        'revision': {'before':answers(active),'withdraw_a0':answers(after),'replace_L_flip1':answers(active,1),
                     'minimal_supports_do_Y1_Z1':supports,'empty_family_not_certified':True},
        'withdrawal_collision': {'same_before':sorted(family(s1)),
                                'first_after':sorted(family(s1-{'a0'})),
                                'second_after':sorted(family(s2-{'a0'}))},
        'repeated_event':{'posterior_once':str(once),'incorrect_independent_copy':str(wrong),
                         'constraint_repetition_idempotent':True},
        'interface_access':{'same_external_pairs':same,'distinguished_by_output_only_postprocessing':downstream,
                            'distinguished_by_internal_do':internal,'witness_do_Y1':[0,1]},
    }
    print(json.dumps({'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'results':results},indent=2,sort_keys=True))


if __name__=='__main__':
    main()
