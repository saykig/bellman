#!/usr/bin/env python3
"""Exact finite experiments. Stdlib only; no stochastic simulations or solver tolerances."""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

BITS = (0, 1)
PAIRS = tuple(product(BITS, repeat=2))
TRIPLES = tuple(product(BITS, repeat=3))
HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def subsets(items):
    return [frozenset(x for i, x in enumerate(items) if mask & (1 << i))
            for mask in range(1 << len(items))]


def project(rows, indices):
    return frozenset(tuple(row[i] for i in indices) for row in rows)


def joint_join(ab, bc, ac=None):
    return frozenset((a, b, c) for a, b, c in TRIPLES
                     if (a, b) in ab and (b, c) in bc
                     and (ac is None or (a, c) in ac))


def kernel(p0, p1):
    return ((1-p0, p0), (1-p1, p1))


def compose(k, ell):
    return tuple(tuple(sum(k[x][y]*ell[y][z] for y in BITS)
                       for z in BITS) for x in BITS)


def chain_product(px, k, ell, intervention):
    """Joint factor product, replacing exactly the factor owned by each target."""
    result = {}
    for x, y, z in TRIPLES:
        factors = (px[x], k[x][y], ell[y][z])
        vals = (x, y, z)
        result[(x, y, z)] = Q(1)
        for owner in range(3):
            result[(x, y, z)] *= (Q(vals[owner] == intervention[owner])
                                      if owner in intervention else factors[owner])
    return result


def sequential_expansion(px, k, ell, intervention):
    """Independent construction: expand partial paths one owned node at a time."""
    paths = {(): Q(1)}
    for owner in range(3):
        extended = {}
        for prefix, mass in paths.items():
            if owner in intervention:
                row = tuple(Q(v == intervention[owner]) for v in BITS)
            elif owner == 0:
                row = px
            elif owner == 1:
                row = k[prefix[0]]
            else:
                row = ell[prefix[1]]
            for value in BITS:
                extended[prefix + (value,)] = mass * row[value]
        paths = extended
    return paths


def probability(law, predicate):
    return sum((p for row, p in law.items() if predicate(row)), Q(0))


def run():
    results = {}
    relations = subsets(PAIRS)
    tree_count = 0
    for ab, bc in product(relations, repeat=2):
        if project(ab, (1,)) == project(bc, (0,)):
            joined = joint_join(ab, bc)
            require(project(joined, (0, 1)) == ab, 'two-bag left extension')
            require(project(joined, (1, 2)) == bc, 'two-bag right extension')
            tree_count += 1
    # Independent existence oracle: enumerate ALL global relations, not just joins.
    possible_marginals = {(project(g, (0, 1)), project(g, (1, 2)), project(g, (0, 2)))
                          for g in subsets(TRIPLES)}
    counts = dict(total=0, locally_agreeing=0, locally_agreeing_empty_join=0,
                  locally_agreeing_nonempty_lossy_join=0, exact_extension=0)
    first_empty = None
    for ab, bc, ac in product(relations, repeat=3):
        counts['total'] += 1
        j = joint_join(ab, bc, ac)
        recovered = (project(j, (0, 1)), project(j, (1, 2)), project(j, (0, 2)))
        exact = recovered == (ab, bc, ac)
        require(exact == ((ab, bc, ac) in possible_marginals), 'T1 versus all-global oracle')
        counts['exact_extension'] += int(exact)
        local = (project(ab, (1,)) == project(bc, (0,))
                 and project(ab, (0,)) == project(ac, (0,))
                 and project(bc, (1,)) == project(ac, (1,)))
        if local:
            counts['locally_agreeing'] += 1
            if not j and any((ab, bc, ac)):
                counts['locally_agreeing_empty_join'] += 1
                if first_empty is None:
                    first_empty = [sorted(ab), sorted(bc), sorted(ac)]
            if j and not exact:
                counts['locally_agreeing_nonempty_lossy_join'] += 1
    results['relational_search'] = {'two_bag_overlap_matches': tree_count,
                                    'counts': counts, 'first_empty_witness': first_empty,
                                    'global_relations_oracle_size': 256}
    eq = frozenset(((0, 0), (1, 1)))
    ne = frozenset(((0, 1), (1, 0)))
    require(not joint_join(eq, eq, ne), 'parity counterexample')
    lossy = joint_join(frozenset(PAIRS), eq, eq)
    require(lossy == frozenset(((0, 0, 0), (1, 1, 1))), 'nonempty lossy witness')
    # Probability-marginal fusion counterexample.
    p = (Q(3, 4), Q(1, 4))
    norm = sum(v*v for v in p)
    naive = tuple(v*v/norm for v in p)
    require(naive == (Q(9, 10), Q(1, 10)) and naive != p, 'double counting')
    results['separator_double_counting'] = {'supplied': p, 'normalized_product': naive}
    # Complete ternary-row grid: every 2x2 kernel with probabilities in {0,1/2,1}.
    grid = (Q(0), Q(1, 2), Q(1))
    kernels = tuple(kernel(a, b) for a, b in product(grid, repeat=2))
    assoc_count = 0
    for k, ell, m in product(kernels, repeat=3):
        require(compose(compose(k, ell), m) == compose(k, compose(ell, m)), 'associativity')
        assoc_count += 1
    px = (Q(3, 4), Q(1, 4))
    surgery_count = 0
    for k, ell in product(kernels, repeat=2):
        for targets in product((None, 0, 1), repeat=3):
            intervention = {i: v for i, v in enumerate(targets) if v is not None}
            full = chain_product(px, k, ell, intervention)
            require(full == sequential_expansion(px, k, ell, intervention), 'T3 surgery')
            require(sum(full.values()) == 1 and min(full.values()) >= 0, 'normalization')
            surgery_count += 1
    results['kernel_grid'] = {'kernels': 9, 'associativity_triples': assoc_count,
                               'surgery_cases': surgery_count, 'all_exact': True}
    k, ell = kernel(Q(1, 5), Q(4, 5)), kernel(Q(1, 10), Q(9, 10))
    obs = chain_product(px, k, ell, {})
    dox = chain_product(px, k, ell, {0: 1})
    doy = chain_product(px, k, ell, {1: 1})
    example = {
        'P_Y1': probability(obs, lambda v: v[1] == 1),
        'P_Z1': probability(obs, lambda v: v[2] == 1),
        'P_Z1_do_X1': probability(dox, lambda v: v[2] == 1),
        'P_Z1_do_Y1': probability(doy, lambda v: v[2] == 1),
        'P_X1_do_Y1': probability(doy, lambda v: v[0] == 1),
        'P_X1_given_Y1': probability(obs, lambda v: v[0] == v[1] == 1)
                              / probability(obs, lambda v: v[1] == 1)}
    require(tuple(example.values()) == (Q(7,20), Q(19,50), Q(37,50), Q(9,10), Q(1,4), Q(4,7)),
            'successful example')
    require(compose(k, ell)[1][1] == example['P_Z1_do_X1'], 'independent kernel computation')
    results['successful_example'] = example
    # Search every knowledge relation on the two binary flip parameters.
    widened = 0
    for c in relations:
        rectangle = frozenset(product((a for (a,) in project(c, (0,))),
                                      (b for (b,) in project(c, (1,)))))
        require(c <= rectangle, 'T4 outer inclusion')
        exact_answers = {a ^ b for a, b in c}
        relaxed_answers = {a ^ b for a, b in rectangle}
        require(exact_answers <= relaxed_answers, 'T4 query inclusion')
        widened += int(exact_answers != relaxed_answers)
    exact_answers = sorted({a ^ b for a, b in eq})
    relaxed_answers = sorted({a ^ b for a, b in PAIRS})
    require(exact_answers == [0] and relaxed_answers == [0, 1], 'coupled flips')
    results['coupled_choices'] = {'relations_searched': 16, 'strict_query_widenings': widened,
                                  'exact_do_X0_Z1': exact_answers,
                                  'rectangular_do_X0_Z1': relaxed_answers}
    # Distinct SCMs: enumerate exogenous root and replace only the targeted equation.
    def scm(reverse, do_x=None):
        law = {(x,y): Q(0) for x,y in PAIRS}
        for u in BITS:
            if reverse:
                y = u
                x = y if do_x is None else do_x
            else:
                x = u if do_x is None else do_x
                y = x
            law[(x,y)] += Q(1,2)
        return law
    require(scm(False) == scm(True), 'observational equivalence')
    effects = tuple(sum(v for (x,y),v in scm(r, 1).items() if y == 1) for r in (False,True))
    require(effects == (Q(1), Q(1,2)), 'causal inequivalence')
    results['observational_equivalence'] = {'P_Y1_do_X1_forward_reverse': effects}
    off_support = [tuple((x, x if identity else 0) for x in (0,)) for identity in (True,False)]
    require(off_support[0] == off_support[1], 'off-support observations')
    results['off_support'] = {'observed_XY': off_support[0], 'do_X1_Y_identity_constant': [1,0]}
    independent_eq = sum(Q(1,4) for x,y in PAIRS if x == y)
    shared_eq = sum(Q(1,2) for u in BITS if u == u)
    require((independent_eq, shared_eq) == (Q(1,2), Q(1)), 'hidden noise')
    results['hidden_noise'] = {'P_equal_independent_shared': (independent_eq, shared_eq)}
    cycle_masses = [sum(int(x == y and y == (x ^ flip)) for x,y in PAIRS) for flip in BITS]
    require(cycle_masses == [2,0], 'cycle normalization obstruction')
    results['cycles'] = {'unnormalized_masses_equality_opposite': cycle_masses}
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true', help='write a new evidence edition')
    args = parser.parse_args()
    result = {'schema': 'bellman-foundations-exact-v1',
              'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'evidence': run()}
    encoded = json.dumps(result, indent=2, sort_keys=True, default=str) + '\n'
    target = HERE / 'results-v1.json'
    if args.write:
        require(not target.exists(), 'refuse to overwrite retained evidence; create a new edition')
        target.write_text(encoded)
    else:
        require(target.read_text() == encoded, 'fresh results differ from retained evidence')
    print(encoded)


if __name__ == '__main__':
    main()
