"""Integrated witness and small counterexamples with explicit rational premises."""
from copy import deepcopy
from witness import rational
from fixtures import fixture


def unit_witness(s):
    return {I: {a: {'coefficient': '1', 'order': 1} for a, q in row.items() if rational(q) == 0}
            for I, row in s['profile'].items()}


def evidence_case(**kwargs):
    s = fixture(**kwargs)
    w = unit_witness(s)
    w['disclose.good']['N']['order'] = 2
    return s, w


def incompatible_routes():
    nodes = {'root': {'kind': 'player', 'player': 'A', 'info': 'root',
                      'edges': {'O': 'out', 'L': 'route.L', 'R': 'route.R'}},
             'out': {'kind': 'terminal'}}
    chance, payoffs = {}, {'out': {'A': '1', 'B': '0'}}
    for side in ('L', 'R'):
        v = 'route.' + side
        nodes[v] = {'kind': 'chance', 'edges': {j: j + '.' + side for j in ('J', 'K')}}
        chance[v] = {'J': '1/2', 'K': '1/2'}
        for j in ('J', 'K'):
            v = j + '.' + side
            nodes[v] = {'kind': 'player', 'player': 'B', 'info': j,
                        'edges': {a: v + '.' + a for a in ('left', 'right')}}
            for a, z in nodes[v]['edges'].items():
                nodes[z] = {'kind': 'terminal'}
                payoffs[z] = {'A': '0', 'B': str(int((a == 'left') == (side == 'L')))}
    return {'schema': 'bellman.assessed-credibility.v1', 'root': 'root', 'nodes': nodes,
            'profile': {'root': {'O': '1', 'L': '0', 'R': '0'},
                        'J': {'left': '1', 'right': '0'}, 'K': {'left': '0', 'right': '1'}},
            'models': {'m': {'chance': chance, 'payoffs': payoffs,
                            'beliefs': {'root': {'root': '1'},
                                       'J': {'J.L': '1', 'J.R': '0'},
                                       'K': {'K.L': '0', 'K.R': '1'}}}}}


def modelwise_not_shared():
    nodes = {'root': {'kind': 'chance', 'edges': {'g': 'A.g', 'b': 'A.b'}}}
    profile, payoffs = {'entry': {'continue': '1'}}, {}
    for q in ('g', 'b'):
        nodes['A.' + q] = {'kind': 'player', 'player': 'A', 'info': 'A.' + q,
                           'edges': {'exit': 'out.' + q, 'enter': 'entry.' + q}}
        nodes['entry.' + q] = {'kind': 'player', 'player': 'B', 'info': 'entry',
                               'edges': {'continue': 'end.' + q}}
        profile['A.' + q] = {'exit': '1', 'enter': '0'}
        for v, u in [('out.' + q, '1'), ('end.' + q, '0')]:
            nodes[v] = {'kind': 'terminal'}
            payoffs[v] = {'A': u, 'B': '0'}
    models = {}
    for name, g, b in [('half', '1/2', '1/2'), ('quarter', '1/4', '3/4')]:
        models[name] = {'chance': {'root': {'g': g, 'b': b}}, 'payoffs': deepcopy(payoffs),
                        'beliefs': {'A.g': {'A.g': '1'}, 'A.b': {'A.b': '1'},
                                   'entry': {'entry.g': '1/2', 'entry.b': '1/2'}}}
    return {'schema': 'bellman.assessed-credibility.v1', 'root': 'root', 'nodes': nodes,
            'profile': profile, 'models': models}
