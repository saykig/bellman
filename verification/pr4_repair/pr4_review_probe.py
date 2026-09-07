"""Pinned-source review probes for Bellman PR #4.

Records original defects and positive controls. This is not a post-repair
acceptance suite: the source guards deliberately require the reviewed bytes.
No repository writes, network access, parameter grid, or formal proof claim.
Run with --repo PATH --output NEW_FILE, normally and with python -O.
"""
from __future__ import annotations
import argparse
from dataclasses import replace
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import platform
import sys

PIN = '81fbcc4d503275f091c8c31588ac02d3abf14466'
SOURCE = 'verification/joint_law_completion/joint_law.py'
DIGEST = '26c33ca45eaae4db31530f47e816687ac0d372cb02ea3ea7abece815e149a1d2'


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    path = args.repo / SOURCE
    require(sha256(path.read_bytes()).hexdigest() == DIGEST, 'Source differs from pinned review; use repaired regressions, not this old-source probe.')
    spec = importlib.util.spec_from_file_location('reviewed_joint_law', path)
    require(spec is not None and spec.loader is not None, 'Cannot load reviewed source')
    j = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = j
    spec.loader.exec_module(j)
    observations = []

    def add(name, classification, **data):
        observations.append({'name': name, 'classification': classification, **data})

    def refuses(call):
        try:
            call()
        except j.Invalid as e:
            return str(e)
        return None

    # All model coefficients below enter through the advertised exact constructors.
    half, eps = F(1, 2), F(1, 2**60)
    p1 = j.Polynomial('p0=half', ((F(1), (1, 0)), (-half, (0, 0))))
    p2 = j.Polynomial('p0=half+epsilon', ((F(1), (1, 0)), (-half-eps, (0, 0))))
    model = j.make_model(('state',), (('0',), ('1',)), ((1, 1),), (1,), extra=(p1, p2))
    task = j.make_task(model, (1, 1), (0, 0), conditional=False,
                       actions=(('a0', (0, 0)), ('a1', (1, 1))))
    comparison = j.difference(task, 'a0', 'a1')
    upper = j.Certificate('upper', comparison, y=(F(-1),), signed_bound=F(-1))
    exact, rounded = (half, half), (0.5, 0.5)
    require(not j.original_member(model, exact), 'Exact control must fail the second predicate')
    require(j.original_member(model, rounded), 'Expected pinned float-witness defect')
    add('R1a_original_membership_float_rounding', 'DEFECT_REPRODUCED',
        original_domain='empty: p0=1/2 and p0=1/2+1/2^60 cannot both hold',
        epsilon=str(eps), exact_point_is_member=False, float_point_is_member=True,
        helper_float_rejection=refuses(lambda: j.rational(0.5)))

    bound = j.consume(comparison, upper)
    require(bound['status'] == 'bound_only_nonemptiness_unestablished', 'Bound alone must not infer existence')
    add('bound_alone_does_not_infer_existence', 'CONTROL_PASSED', result=bound)

    for conditional in (False, True):
        t = replace(task, conditional=conditional)
        d = j.difference(t, 'a0', 'a1')
        y = (F(0), F(-1)) if conditional else (F(-1),)
        c = j.Certificate('upper', d, y=y, signed_bound=F(-1))
        result = j.decide(t, 'a0', rounded, {'a1': c})
        require(result['uniformly_strict_against_other_actions'], 'Expected false decision certification')
        require(refuses(lambda: j.decide(t, 'a0', exact, {'a1': c})) is not None, 'Exact witness must fail')
        add('R1b_decide_' + ('conditional' if conditional else 'unconditional'), 'DEFECT_REPRODUCED', result=result,
            exact_original_nonemptiness=False, exact_point_refused=True)

    fixed = j.fixed_minimizing_set(task, ['a0'], rounded, {('a0', 'a1'): upper})
    require(fixed['complete_minimizing_set'] == ['a0'], 'Expected false fixed-set certification')
    add('R1c_fixed_minimizing_set_float_witness', 'DEFECT_REPRODUCED', result=fixed, exact_original_nonemptiness=False)

    # The same missing witness-number guard misstates unconditional nonemptiness.
    one = j.Polynomial('p0=one', ((F(1), (1, 0)), (F(-1), (0, 0))))
    oneplus = j.Polynomial('p0=one+epsilon', ((F(1), (1, 0)), (-1-eps, (0, 0))))
    impossible = j.make_model(('state',), (('0',), ('1',)), ((1, 1), (0, 1)), (1, 0), extra=(one, oneplus))
    itask = j.make_task(impossible, (0, 1), (0, 1))
    farkas = j.Certificate('infeasible', itask, y=(F(0), F(1), F(-1)), signed_bound=F(-1))
    result = j.impossible_event(itask, (1.0, 0.0), farkas)
    require(result['original_nonempty'] is True, 'Expected false original_nonempty')
    require(not j.original_member(impossible, (F(1), F(0))), 'Exact infeasible control')
    add('R1d_impossible_event_false_original_nonemptiness', 'DEFECT_REPRODUCED', result=result, actual_original_nonempty=False)

    # This is not a blanket failure of consume's certificate-vector validation.
    normal = j.make_model(('state',), (('0',), ('1',)), ((1, 1),), (1,))
    goodtask = j.make_task(normal, (1, 1), (0, 0), conditional=False,
                          actions=(('a0', (0, 0)), ('a1', (1, 1))))
    gooddiff = j.difference(goodtask, 'a0', 'a1')
    goodcert = j.Certificate('upper', gooddiff, y=(F(-1),), signed_bound=F(-1))
    require(refuses(lambda: j.consume(goodtask, j.Certificate('witness', goodtask, point=rounded))) is not None,
            'consume correctly rejects floats in certificate point')
    result = j.decide(goodtask, 'a0', exact, {'a1': goodcert})
    require(result['complete_minimizing_set'] == ['a0'], 'Genuine exact decision control')
    add('exact_decision_and_certificate_float_rejection', 'CONTROL_PASSED', result=result)

    # A related early-return validation gap on a one-action menu.
    single = replace(goodtask, actions=(('a0', (F(0), F(0))),))
    invalid_task = replace(single, event=(F(0), F(0)))
    require(refuses(invalid_task.validate) is not None, 'The task must fail its own validator')
    a = j.decide(invalid_task, 'a0', exact, {})
    b = j.fixed_minimizing_set(invalid_task, ['a0'], exact, {})
    require(a['complete_minimizing_set'] == b['complete_minimizing_set'] == ['a0'], 'Expected unchecked shortcut')
    add('R2_single_action_task_validation_shortcut', 'DEFECT_REPRODUCED',
        task_validator_refuses=True, decide_returns=a, fixed_minimizing_set_returns=b,
        scope='invalid-task acceptance; no separate false numeric optimum claimed')

    # Actual callable separation, rather than a source-code string search.
    def disabled(*_a, **_k):
        raise RuntimeError('Producer helper deliberately disabled')
    j.propose = disabled
    j.solve_rows = disabled
    result = j.decide(goodtask, 'a0', exact, {'a1': goodcert})
    require(result['complete_minimizing_set'] == ['a0'], 'Consumer must not need producer helpers')
    add('producer_helpers_disabled', 'CONTROL_PASSED', result=result)

    payload = {
        'reviewed_commit': PIN, 'source': SOURCE, 'source_sha256': DIGEST,
        'python': platform.python_version(), 'optimized': sys.flags.optimize,
        'scope': 'Pinned-source defect reproductions and exact controls; not post-repair acceptance or formal verification',
        'observations': j.wire(observations),
    }
    with args.output.open('x', encoding='utf-8') as out:
        out.write(json.dumps(payload, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'groups': len(observations), 'defect_reproductions': sum(r['classification'] == 'DEFECT_REPRODUCED' for r in observations),
                      'controls': sum(r['classification'] == 'CONTROL_PASSED' for r in observations), 'optimized': sys.flags.optimize}))


if __name__ == '__main__':
    main()
