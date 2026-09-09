"""Exact symbolic receiving without importing the valuation or incentive producer."""
import json
import sys
import sympy as sp
from witness import validate_witness, rational, digest, demand, SEMANTICS
from receiver import receive as receive_incentives


def symbolic_beliefs(s, w):
    """Rebuild complete normalized prefix polynomials, including higher terms."""
    infos = validate_witness(s, w)
    t = sp.Symbol('t', positive=True)
    strategy = {}
    maximum = sp.Rational(0)
    for I, row in s['profile'].items():
        zero_sum = sum((sp.Rational(z['coefficient']) * t ** z['order']
                        for z in w[I].values()), sp.Integer(0))
        C = sum((sp.Rational(z['coefficient']) for z in w[I].values()), sp.Rational(0))
        maximum = max(maximum, C)
        strategy[I] = {a: sp.Poly(sp.Rational(w[I][a]['coefficient']) * t ** w[I][a]['order']
                                  if a in w[I] else sp.Rational(q) * (1 - zero_sum), t, domain=sp.QQ)
                       for a, q in row.items()}
        demand(sum(strategy[I].values(), sp.Poly(0, t, domain=sp.QQ)) == sp.Poly(1, t, domain=sp.QQ),
               'internal-polynomial-normalization')
    # Unlike the forward producer, reconstruct each root prefix from parent links.
    parents = {child: (v, a) for v, n in s['nodes'].items()
               for a, child in n.get('edges', {}).items()}
    rows = []
    for name, model in sorted(s['models'].items()):
        for I, info in sorted(infos.items()):
            prefixes = {}
            for h in info['nodes']:
                polynomial = sp.Poly(1, t, domain=sp.QQ)
                v = h
                while v != s['root']:
                    parent, action = parents[v]
                    node = s['nodes'][parent]
                    if node['kind'] == 'chance':
                        polynomial *= sp.Rational(model['chance'][parent][action])
                    else:
                        polynomial *= strategy[node['info']][action]
                    v = parent
                prefixes[h] = polynomial
            denominator = sum(prefixes.values(), sp.Poly(0, t, domain=sp.QQ))
            demand(not denominator.is_zero, 'unsupported-structurally-unreachable-information', name + '/' + I)
            (den_degree,), den_coeff = denominator.terms()[-1]
            beliefs = {}
            for h, numerator in prefixes.items():
                if numerator.is_zero:
                    answer = sp.Rational(0)
                else:
                    (degree,), coefficient = numerator.terms()[-1]
                    demand(degree >= den_degree, 'internal-polynomial-order')
                    answer = coefficient / den_coeff if degree == den_degree else sp.Rational(0)
                beliefs[h] = str(answer)
            rows.append({'model': name, 'info': I, 'beliefs': beliefs})
    return rows, str(1 / (1 + maximum))


def receive(s, c, expected_epsilon='0'):
    demand(type(c) is dict and set(c) == {'schema', 'semantics', 'subject_sha256',
           'witness', 't_max', 'belief_rows', 'incentives'}, 'warrant-schema')
    demand(c['schema'] == 'bellman.shared-consistency-warrant.v1' and c['semantics'] == SEMANTICS,
           'warrant-semantics-mismatch')
    demand(c['subject_sha256'] == digest(s), 'stale-subject')
    rows, t_max = symbolic_beliefs(s, c['witness'])
    demand(c['t_max'] == t_max, 'false-positivity-radius')
    demand(c['belief_rows'] == rows, 'false-limiting-beliefs')
    for row in rows:
        demand(row['beliefs'] == s['models'][row['model']]['beliefs'][row['info']],
               'witness-limit-mismatch', row['model'] + '/' + row['info'])
    incentive = receive_incentives(s, c['incentives'], expected_epsilon)
    if incentive['status'] == 'profitable-deviation':
        status = 'shared-consistent-profitable-deviation'
    elif rational(expected_epsilon) == 0:
        status = 'shared-consistent-modelwise-sequential-equilibrium'
    else:
        status = 'shared-consistent-continuation-bound'
    return {'status': status, 'max_gain': incentive['max_gain'], 'epsilon': expected_epsilon,
            'information_queries': len(rows), 'subject_sha256': digest(s),
            'warrant_sha256': digest(c), 'semantics': SEMANTICS}


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        subject = json.load(f)
    with open(sys.argv[2]) as f:
        certificate = json.load(f)
    print(json.dumps(receive(subject, certificate, sys.argv[3] if len(sys.argv) > 3 else '0'), sort_keys=True))
