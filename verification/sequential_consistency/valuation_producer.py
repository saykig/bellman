"""Candidate construction by forward leading orders and coefficients."""
from fractions import Fraction as F
from witness import validate_witness, rational, digest, demand, SEMANTICS
from producer import produce as incentive_produce


def produce(s, w, epsilon='0'):
    infos = validate_witness(s, w)
    rows = []
    for name, m in sorted(s['models'].items()):
        leading = {}
        frontier = [(s['root'], 0, F(1))]
        while frontier:
            v, order, coefficient = frontier.pop()
            leading[v] = (order, coefficient)
            n = s['nodes'][v]
            for a, child in n.get('edges', {}).items():
                k, c = 0, F(1)
                if n['kind'] == 'chance':
                    c = rational(m['chance'][v][a])
                else:
                    c = rational(s['profile'][n['info']][a])
                    if c == 0:
                        term = w[n['info']][a]
                        k, c = term['order'], rational(term['coefficient'])
                frontier.append((child, order + k, coefficient * c))
        for I, info in sorted(infos.items()):
            live = [v for v in info['nodes'] if leading[v][1] > 0]
            demand(bool(live), 'unsupported-structurally-unreachable-information', name + '/' + I)
            k = min(leading[v][0] for v in live)
            total = sum(leading[v][1] for v in live if leading[v][0] == k)
            beliefs = {v: str(leading[v][1] / total if leading[v][0] == k else F(0))
                       for v in info['nodes']}
            # An unsuccessful candidate is not promoted to a global impossibility.
            rows.append({'model': name, 'info': I, 'beliefs': beliefs})
    C = max(sum((rational(t['coefficient']) for t in row.values()), F(0)) for row in w.values())
    return {'schema': 'bellman.shared-consistency-warrant.v1',
            'semantics': SEMANTICS, 'subject_sha256': digest(s), 'witness': w,
            't_max': str(1 / (1 + C)), 'belief_rows': rows,
            'incentives': incentive_produce(s, epsilon)}
