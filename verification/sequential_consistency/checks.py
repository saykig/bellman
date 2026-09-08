"""Exact counterexamples, independent polynomial checks and receiving controls."""
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import sympy as sp
from witness import Invalid, WitnessFailure, demand, digest, rational
from cases import evidence_case, unit_witness, incompatible_routes, modelwise_not_shared
from valuation_producer import produce
from consistency_receiver import receive
from producer import produce as assessed_produce
from receiver import receive as assessed_receive
from subject import reach
from fixtures import renamed

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'sequential_credibility'


def execute():
    facts, rejections = {}, []

    def check(label, ok):
        demand(ok, 'failed-check', label)

    def reject(label, s, c, epsilon='0', code=None):
        try:
            receive(s, c, epsilon)
        except Invalid as error:
            if code is not None:
                check(label + ' diagnostic', isinstance(error, WitnessFailure) and error.code == code)
            rejections.append(label)
        else:
            raise RuntimeError('accepted invalid warrant: ' + label)

    s, w = evidence_case()
    c = produce(s, w)
    facts['integrated'] = receive(s, c)
    check('original exact subject retained', s == json.loads((OLD / 'example_subject.json').read_text()))
    check('80 queries and zero gain', facts['integrated']['information_queries'] == 80 and c['incentives']['max_gain'] == '0')
    check('safe positivity radius', c['t_max'] == '1/2')
    plain = produce(s, unit_witness(s))
    reject('equal-rate noise gives wrong posterior', s, plain, code='witness-limit-mismatch')
    # Third arithmetic route: actual normalized rational strategies at positive t.
    # This is convergence evidence, not a finite-grid proof of the limiting theorem.
    posterior_checks = []
    for t in (F(1, 4), F(1, 8), F(1, 16)):
        perturbed = deepcopy(s)
        for I, row in s['profile'].items():
            z = sum(F(term['coefficient']) * t ** term['order'] for term in w[I].values())
            perturbed['profile'][I] = {a: str(F(w[I][a]['coefficient']) * t ** w[I][a]['order']
                                             if a in w[I] else F(q) * (1 - z))
                                      for a, q in row.items()}
            probs = [F(q) for q in perturbed['profile'][I].values()]
            check('complete mixing', min(probs) > 0 and sum(probs) == 1)
        for m in perturbed['models'].values():
            r = reach(perturbed, m)
            for b in ('zero', 'bond'):
                g, bad = r['receive.good.N.' + b], r['receive.bad.N.' + b]
                check('exact withheld posterior path', g / (g + bad) == t / (1 + t))
        posterior_checks.append({'t': str(t), 'good_given_withheld': str(t / (1 + t))})
    facts['finite_t_path_checks'] = posterior_checks

    for label, options, gain in [('weak_bond', {'bond': 5}, '1/2'),
                                  ('costly_participation', {'fee': F(3, 2)}, '1/10')]:
        changed, cw = evidence_case(**options)
        cc = produce(changed, cw)
        result = receive(changed, cc)
        check(label, result['status'] == 'shared-consistent-profitable-deviation' and result['max_gain'] == gain)
        facts[label] = {'status': result['status'], 'max_gain': gain}
        reject('stale ' + label, changed, c, code='stale-subject')
        forged = deepcopy(c)
        forged['subject_sha256'] = digest(changed)
        reject('stale inner incentives after ' + label, changed, forged)
    weak, ww = evidence_case(bond=5)
    loose = produce(weak, ww, '1/2')
    check('positive epsilon never exact equilibrium', receive(weak, loose, '1/2')['status'] == 'shared-consistent-continuation-bound')
    reject('tolerance controlled by recipient', weak, loose)

    # A globally impossible assessment which the preliminary checker correctly
    # accepts only under its weaker, explicitly assessment-relative semantics.
    bad = incompatible_routes()
    old_pass = assessed_receive(bad, assessed_produce(bad))
    check('inconsistent assessment passes draft', old_pass['status'] == 'assessment-relative-pass')
    reject('incompatible route posteriors', bad, produce(bad, unit_witness(bad)), code='witness-limit-mismatch')
    x, y = sp.symbols('x y', positive=True)
    j = (x / 2) / (x / 2 + y / 2)
    k = (x / 2) / (x / 2 + y / 2)
    check('universal posterior identity', sp.cancel(j - k) == 0)
    check('target contradicts identity', F(bad['models']['m']['beliefs']['J']['J.L']) != F(bad['models']['m']['beliefs']['K']['K.L']))
    facts['incompatible_routes'] = {'draft_max_gain': '0', 'identity': 'mu_J(L)=mu_K(L)',
                                   'target': ['1', '0'], 'conclusion': 'assessment-inconsistent-by-identity'}

    weighted = deepcopy(bad)
    for I in ('J', 'K'):
        weighted['models']['m']['beliefs'][I] = {I + '.L': '1/4', I + '.R': '3/4'}
        weighted['profile'][I] = {'left': '0', 'right': '1'}
    weighted_w = unit_witness(weighted)
    weighted_w['root']['R']['coefficient'] = '3'
    facts['weighted_coefficients'] = receive(weighted, produce(weighted, weighted_w))
    check('coefficient ratios matter', facts['weighted_coefficients']['max_gain'] == '0')
    changed_w = deepcopy(weighted_w)
    changed_w['root']['R']['coefficient'] = '1'
    reject('wrong positive coefficient ratio', weighted, produce(weighted, changed_w), code='witness-limit-mismatch')
    mixed = deepcopy(weighted)
    mixed['profile']['root'] = {'O': '1/2', 'L': '1/8', 'R': '3/8'}
    for I in ('J', 'K'):
        mixed['profile'][I] = {'left': '1/2', 'right': '1/2'}
    mixed_c = produce(mixed, unit_witness(mixed))
    check('fully mixed no trembles', all(not row for row in mixed_c['witness'].values()) and mixed_c['t_max'] == '1')
    facts['fully_mixed'] = receive(mixed, mixed_c)
    check('mixed full-continuation gain', facts['fully_mixed']['max_gain'] == '1/2')

    family = modelwise_not_shared()
    check('family draft passes', assessed_produce(family)['max_gain'] == '0')
    separate = []
    for model, coefficient in [('half', '1'), ('quarter', '3')]:
        one = deepcopy(family)
        one['models'] = {model: one['models'][model]}
        ow = unit_witness(one)
        ow['A.g']['enter']['coefficient'] = coefficient
        single = receive(one, produce(one, ow))
        check('separate model consistency', single['max_gain'] == '0')
        separate.append({'model': model, 'good_coefficient': coefficient})
        reject('separate witness fails shared query ' + model, family, produce(family, ow), code='witness-limit-mismatch')
    # If first posterior ->1/2 then x/y ->1 and second posterior ->1/4,
    # contradicting its target 1/2. No enumeration of candidate orders is used.
    ratio = sp.Symbol('ratio', positive=True)
    check('cross-model rational posterior', (ratio / (ratio + 3)).subs(ratio, 1) == sp.Rational(1, 4))
    facts['modelwise_not_shared'] = {'individual_witnesses': separate,
                                    'shared_limit_for_second_if_first_half': '1/4',
                                    'required_second': '1/2', 'conclusion': 'no-shared-sequence-by-odds'}

    zero = deepcopy(bad)
    zero['models']['m']['chance'] = {'route.L': {'J': '0', 'K': '1'},
                                    'route.R': {'J': '1', 'K': '0'}}
    zero['models']['m']['beliefs']['J'] = {'J.L': '0', 'J.R': '1'}
    zero['models']['m']['beliefs']['K'] = {'K.L': '1', 'K.R': '0'}
    zero['profile']['J'] = {'left': '0', 'right': '1'}
    zero['profile']['K'] = {'left': '1', 'right': '0'}
    facts['partial_structural_zeros'] = receive(zero, produce(zero, unit_witness(zero)))
    dead = deepcopy(bad)
    dead['models']['m']['chance'] = {v: {'J': '0', 'K': '1'} for v in ('route.L', 'route.R')}
    forged = produce(bad, unit_witness(bad))
    forged['subject_sha256'] = digest(dead)
    reject('chance-impossible information set', dead, forged, code='unsupported-structurally-unreachable-information')

    rs = renamed(s)
    imap = {I: 'info' + str(j) for j, I in enumerate(sorted(s['profile']))}
    rw = {imap[I]: deepcopy(row) for I, row in w.items()}
    check('whole-witness renaming', receive(rs, produce(rs, rw))['max_gain'] == '0')
    reject('old witness after renaming', rs, c, code='stale-subject')
    facts['history_transport'] = 'bijective renaming of complete subject and witness only'
    forgotten = deepcopy(s)
    forgotten['nodes']['act.good.N.bond']['info'] = 'act.bad.N.bond'
    fc = deepcopy(c)
    fc['subject_sha256'] = digest(forgotten)
    reject('forgetting private type and own actions', forgotten, fc)

    def mutate(label, change, code=None):
        cc = deepcopy(c)
        change(cc)
        reject(label, s, cc, code=code)

    mutate('model-indexed witness', lambda z: z['witness'].update({'g=1,p=1/2': {}}), 'witness-information-coverage')
    mutate('missing zero action', lambda z: z['witness']['disclose.good'].clear(), 'witness-action-coverage')
    mutate('trembling supported action', lambda z: z['witness']['disclose.good'].update({'G': {'coefficient': '1', 'order': 1}}), 'witness-action-coverage')
    for k, code in [(0, 'invalid-witness-order'), (-1, 'invalid-witness-order'),
                    (True, 'invalid-witness-order'), (1.5, 'invalid-witness-order'), (33, 'unsupported-witness-order')]:
        mutate('order ' + str(k), lambda z, k=k: z['witness']['disclose.good']['N'].update({'order': k}), code)
    for coefficient, code in [('0', 'nonpositive-witness-coefficient'), ('-1', 'nonpositive-witness-coefficient'),
                               ('1.0', 'invalid-witness-coefficient'), (0.1, 'invalid-witness-coefficient')]:
        mutate('coefficient ' + str(coefficient), lambda z, q=coefficient: z['witness']['disclose.good']['N'].update({'coefficient': q}), code)
    mutate('false radius', lambda z: z.update({'t_max': '1'}), 'false-positivity-radius')
    mutate('missing limiting row', lambda z: z['belief_rows'].pop(), 'false-limiting-beliefs')
    mutate('duplicate limiting row', lambda z: z['belief_rows'].__setitem__(0, z['belief_rows'][1]), 'false-limiting-beliefs')
    mutate('forged limiting distribution', lambda z: z['belief_rows'][0].update({'beliefs': {}}), 'false-limiting-beliefs')
    mutate('weaker quantifier substituted', lambda z: z.update({'semantics': 'per-model-sequences'}), 'warrant-semantics-mismatch')
    mutate('forged incentive bound', lambda z: z['incentives'].update({'max_gain': '-1'}))
    mutate('producer success label supplied', lambda z: z.update({'status': 'success'}), 'warrant-schema')
    mutate('stale subject digest', lambda z: z.update({'subject_sha256': '0' * 64}), 'stale-subject')

    # Receiving in a new directory with both candidate producers and fixtures absent.
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        for source, destination, names in [(HERE, 'sequential_consistency', ['witness.py', 'consistency_receiver.py']),
                                          (OLD, 'sequential_credibility', ['subject.py', 'receiver.py'])]:
            (root / destination).mkdir()
            for name in names:
                shutil.copy2(source / name, root / destination / name)
        (root / 'subject.json').write_text(json.dumps(s))
        (root / 'warrant.json').write_text(json.dumps(c))
        command = [sys.executable] + (['-O'] if not __debug__ else []) + [str(root / 'sequential_consistency' / 'consistency_receiver.py'),
                    str(root / 'subject.json'), str(root / 'warrant.json')]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        check('both producers disabled', json.loads(result.stdout) == facts['integrated'])
    facts['both_producers_disabled'] = True
    facts['rejections'] = rejections
    facts['sympy_version'] = sp.__version__
    return facts, s, c


if __name__ == '__main__':
    print(json.dumps(execute()[0], sort_keys=True, indent=2))
