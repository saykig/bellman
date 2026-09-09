"""Standard-library receiver: exact data/score reconstruction, numerical fit residual audit.
Does not import or execute analyze.py, numpy, scipy, pandas, sklearn or statsmodels.
It checks retained arithmetic, not physical randomization, fitted utility or causal validity.
"""
import csv
from fractions import Fraction as F
from hashlib import sha256
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
LABELS = ('reduced', 'full', 'treatment_mean', 'persistence')


def need(value, message):
    if not value:
        raise ValueError(message)


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def close(a, b, message, tol=F(1, 10**12)):
    need(abs(F(str(a)) - F(str(b))) <= tol, message)


def read_rows(path):
    with path.open() as f:
        rows = [{k: int(v) for k, v in r.items()} for r in csv.DictReader(f)]
    need(len(rows) == 1296, 'row count')
    keys = [(r['ID'], r['Period']) for r in rows]
    need(len(set(keys)) == len(keys), 'duplicate participant round')
    for r in rows:
        need(1 <= r['give'] <= 12 or r['give'] == 0, 'sent range')
        need(0 <= r['returned'] <= 84, 'return range')
    for person in {r['ID'] for r in rows}:
        group = [r for r in rows if r['ID'] == person]
        need(sorted(r['Period'] for r in group) == list(range(1, 7)), 'missing round')
        need(len({(r['Session'], r['Treatment'], r['Rank'] == 1, r['Subject']) for r in group}) == 1, 'identity changed')
    for session in range(1, 13):
        group = [r for r in rows if r['Session'] == session]
        need(len(group) == 108 and len({r['ID'] for r in group}) == 18, 'session size')
        need(len({r['Treatment'] for r in group}) == 1, 'mixed treatment session')
        for period in range(1, 7):
            current = [r for r in group if r['Period'] == period]
            for g in {r['Group'] for r in current}:
                trio = [r for r in current if r['Group'] == g]
                need(sorted(r['Rank'] for r in trio) == [1, 2, 3], 'group roles')
                recipient = next(r for r in trio if r['Rank'] == 1)
                senders = [r for r in trio if r['Rank'] != 1]
                need(sum(r['give'] for r in senders) == recipient['receive1'] + recipient['receive2'], 'transfer mapping')
                need(sum(r['returned'] for r in senders) == recipient['return1'] + recipient['return2'], 'return mapping')
                for r in senders:
                    other = next(o for o in senders if o['ID'] != r['ID'])
                    need(r['give_o'] == other['give'] and r['returned_other'] == other['returned'], 'other sender mapping')
                need(recipient['return1'] + recipient['return2'] <= 12 + 3 * sum(r['give'] for r in senders), 'resource constraint')
    return rows


def receive(result, intended_use='retrospective-mean-prediction.v1', root=HERE):
    need(intended_use == 'retrospective-mean-prediction.v1', 'unsupported intended use; no predictive-to-causal transport')
    need(result['kind'] == intended_use, 'query mismatch')
    expected_inputs = {'PLAN.md', 'observations.csv', 'provenance.json'}
    need(set(result['input_sha256']) == expected_inputs, 'input manifest coverage')
    for p in expected_inputs:
        need(result['input_sha256'][p] == digest(root / p), 'input mismatch: ' + p)
    need(result['producer_sha256'] == digest(root / 'analyze.py'), 'producer source mismatch')
    provenance = json.loads((root / 'provenance.json').read_text())
    need(provenance['projection']['sha256'] == digest(root / 'observations.csv'), 'projection mismatch')
    need(provenance['plan_sha256'] == digest(root / 'PLAN.md'), 'plan mismatch')
    rows = read_rows(root / 'observations.csv')
    bykey = {(r['ID'], r['Period']): r for r in rows}
    sessions = {r['Session']: r['Treatment'] for r in rows}
    test_sessions = [min([s for s in sessions if sessions[s] == t], key=lambda s:
                        sha256(f'bellman-fsd3661-holdout-v1:{s}'.encode()).hexdigest()) for t in range(1, 5)]
    train = [r for r in rows if r['Rank'] != 1 and r['Period'] > 1 and r['Session'] not in test_sessions]
    test = sorted([r for r in rows if r['Rank'] != 1 and r['Period'] > 1 and r['Session'] in test_sessions], key=lambda r: (r['ID'], r['Period']))
    need(result['split'] == {'test_sessions': test_sessions, 'train_sessions': sorted(set(sessions) - set(test_sessions)), 'train_rows': len(train), 'test_rows': len(test)}, 'split mismatch')
    need(len({r['ID'] for r in train} & {r['ID'] for r in test}) == 0, 'participant leakage')

    def features(r, full):
        values = [F(r['Treatment'] == t) for t in range(1, 5)] + [F(r['Period'] == t) for t in range(2, 7)]
        for col, denom in [('give', 12)] + ([('returned', 84)] if full else []):
            for lag in range(1, 6):
                previous = bykey.get((r['ID'], r['Period'] - lag))
                values.append(F(previous[col], denom) if previous else F(0))
        return values

    max_residual = F(0)
    for name in ('reduced', 'full'):
        model = result['models'][name]
        expected = [f'treatment_{t}' for t in range(1, 5)] + [f'round_{t}' for t in range(2, 7)] + [f'sent_lag_{t}' for t in range(1, 6)]
        if name == 'full':
            expected += [f'return_lag_{t}' for t in range(1, 6)]
        need(model['features'] == expected, 'feature contract')
        b = [F(v) for v in model['coefficients']]
        need(len(b) == len(expected), 'coefficient dimension')
        a = F(model['intercept'])
        residuals = [(features(r, name == 'full'), r) for r in train]
        errors = [(x, a + sum(v * w for v, w in zip(b, x)) - F(r['give'], 12)) for x, r in residuals]
        grad = [sum(e for x, e in errors)] + [sum(x[j] * e for x, e in errors) + b[j] for j in range(len(b))]
        max_residual = max(max_residual, *map(abs, grad))
    need(max_residual < F(1, 10**8), 'ridge normal-equation residual')
    need(len(result['predictions']) == len(test), 'prediction count')
    losses = {s: {label: [] for label in LABELS} for s in test_sessions}
    means = {t: sum(F(r['give'], 12) for r in train if r['Treatment'] == t) / len([r for r in train if r['Treatment'] == t]) for t in range(1, 5)}
    for r, claimed in zip(test, result['predictions']):
        need({k: claimed[k] for k in ['id', 'round', 'session', 'treatment', 'sent']} ==
             dict(zip(['id', 'round', 'session', 'treatment', 'sent'], [r[k] for k in ['ID', 'Period', 'Session', 'Treatment', 'give']])), 'prediction subject/outcome')
        need(set(claimed['predictions']) == set(LABELS), 'prediction labels')
        for label in LABELS:
            p = F(claimed['predictions'][label])
            need(0 <= p <= 1, 'prediction range')
            if label in ('full', 'reduced'):
                model = result['models'][label]
                computed = F(model['intercept']) + sum(F(a) * x for a, x in zip(model['coefficients'], features(r, label == 'full')))
                computed = max(F(0), min(F(1), computed))
            elif label == 'persistence':
                computed = F(bykey[(r['ID'], r['Period'] - 1)]['give'], 12)
            else:
                computed = means[r['Treatment']]
            close(p, computed, 'prediction reconstruction')
            losses[r['Session']][label].append((p - F(r['give'], 12)) ** 2)
    scores = {s: {k: sum(v) / len(v) for k, v in kinds.items()} for s, kinds in losses.items()}
    need(len(result['session_scores']) == 4, 'session score count')
    for s, claim in zip(test_sessions, result['session_scores']):
        need(claim['session'] == s and claim['rows'] == 60, 'session score identity')
        for k in LABELS:
            close(claim['mse'][k], scores[s][k], 'session score')
        close(claim['difference'], scores[s]['reduced'] - scores[s]['full'], 'paired session score')
    total = {k: sum(v[k] for v in scores.values()) / 4 for k in LABELS}
    for k in LABELS:
        close(result['scores']['normalized_mse'][k], total[k], 'overall score')
        close(result['scores']['rmse_points'][k] ** 2, 144 * total[k], 'rmse score')
    delta = total['reduced'] - total['full']
    close(result['scores']['reduced_minus_full'], delta, 'comparison')
    half = math.sqrt(2 * math.log(20) / 4)
    close(result['scores']['hoeffding_half_width'], half, 'coverage expression')
    for a, b in zip(result['scores']['hoeffding_90ci'], [max(-1., float(delta) - half), min(1., float(delta) + half)]):
        close(a, b, 'coverage interval')
    need(result['scores']['equivalence_margin'] == .01 and result['scores']['equivalence'] == 'not_established', 'equivalence overclaim')
    targets = [(5.70, 8.00), (6.20, 9.06), (6.89, 9.82), (7.33, 11.73)]
    for t, expected in enumerate(targets, 1):
        group = [r for r in rows if r['Treatment'] == t and r['Rank'] != 1]
        claim = result['reproduction'][t - 1]
        need(claim['treatment'] == t and claim['sender_rounds'] == len(group) == 216, 'reproduction count')
        for col, field, target in [('give', 'mean_sent', expected[0]), ('returned', 'mean_returned', expected[1])]:
            exact = sum(F(r[col]) for r in group) / len(group)
            close(claim[field], exact, 'reproduction arithmetic')
            close(exact, target, 'original rounding discrepancy', F(1, 200))
    return {'status': 'checked_scoped_arithmetic', 'observations': len(rows), 'test_rows': len(test),
            'test_sessions': test_sessions, 'exact_normalized_mse': {k: str(v) for k, v in total.items()},
            'exact_reduced_minus_full': str(delta), 'max_ridge_normal_equation_residual': float(max_residual),
            'not_checked': ['physical randomization', 'sampling exchangeability', 'utility or beliefs',
                            'statistical adequacy', 'bootstrap interval', 'OLS uncertainty', 'equilibrium', 'causality']}


if __name__ == '__main__':
    p = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'results.json'
    print(json.dumps(receive(json.loads(p.read_text())), sort_keys=True, indent=2))
