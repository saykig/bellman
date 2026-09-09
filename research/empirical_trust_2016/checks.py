"""Decisive receiving controls, no producer imports. Run normally and under -O."""
import builtins
from copy import deepcopy
from fractions import Fraction as F
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
import sys

original_import = builtins.__import__
def no_producer(name, *args, **kwargs):
    if name.split('.')[0] in {'analyze', 'numpy', 'scipy', 'pandas', 'sklearn', 'statsmodels'}:
        raise ImportError('producer/statistical stack disabled')
    return original_import(name, *args, **kwargs)
builtins.__import__ = no_producer
from receiver import receive, read_rows, need

HERE = Path(__file__).resolve().parent


def run(path):
    evidence = json.loads(path.read_text())
    positive = receive(evidence)
    rejected = []
    def reject(label, mutate, expected):
        bad = deepcopy(evidence)
        mutate(bad)
        try:
            receive(bad)
        except ValueError as e:
            need(expected in str(e), label + ': wrong rejection ' + str(e))
            rejected.append(label)
        else:
            raise RuntimeError(label + ' accepted')
    reject('stale data', lambda r: r['input_sha256'].__setitem__('observations.csv', '0' * 64), 'input mismatch')
    reject('missing premise binding', lambda r: r['input_sha256'].pop('PLAN.md'), 'manifest coverage')
    reject('changed query', lambda r: r.__setitem__('kind', 'causal-feedback-erasure.v1'), 'query mismatch')
    reject('participant leakage', lambda r: r['split']['train_sessions'].append(1), 'split mismatch')
    reject('altered outcome', lambda r: r['predictions'][0].__setitem__('sent', 999), 'subject/outcome')
    reject('altered prediction', lambda r: r['predictions'][0]['predictions'].__setitem__('full', '0.123456'), 'prediction reconstruction')
    reject('score forgery', lambda r: r['scores']['normalized_mse'].__setitem__('full', 0), 'overall score')
    reject('false equivalence', lambda r: r['scores'].__setitem__('equivalence', 'established'), 'equivalence overclaim')
    reject('erased feature relabelled', lambda r: r['models']['full']['features'].__setitem__(14, 'future_return'), 'feature contract')
    reject('false fitted coefficient', lambda r: r['models']['full']['coefficients'].__setitem__(0, '100'), 'normal-equation residual')
    reject('training mean altered', lambda r: r['predictions'][0]['predictions'].__setitem__('treatment_mean', '0'), 'prediction reconstruction')
    reject('original result mismatch', lambda r: r['reproduction'][0].__setitem__('mean_sent', 6), 'reproduction arithmetic')
    try:
        receive(evidence, intended_use='causal-feedback-erasure.v1')
    except ValueError as e:
        need('unsupported intended use' in str(e), 'wrong revision rejection')
        rejected.append('prediction-to-intervention revision')
    else:
        raise RuntimeError('causal transport accepted')
    with TemporaryDirectory() as d:
        root = Path(d)
        for p in ['PLAN.md', 'observations.csv', 'provenance.json', 'analyze.py']:
            shutil.copyfile(HERE / p, root / p)
        with (root / 'PLAN.md').open('a') as f:
            f.write('\nChanged margin after evaluation.\n')
        try:
            receive(evidence, root=root)
        except ValueError as e:
            need('input mismatch: PLAN.md' in str(e), 'wrong changed-plan rejection')
            rejected.append('changed plan bytes')
        else:
            raise RuntimeError('changed plan accepted')
    # Analytical nonidentification construction specialized to empirical *plug-in* law.
    # Outcomes here are existing observations; counterfactual endpoints are constructions.
    rows = [r for r in read_rows(HERE / 'observations.csv') if r['Rank'] != 1 and r['Period'] > 1]
    mu = sum(F(r['give'], 12) for r in rows) / len(rows)
    # Two SCM extensions agree at the sole observed visibility value; differ at hidden feedback.
    model_visible = [[F(r['give'], 12) for r in rows] for _ in range(2)]
    model_hidden = [[F(0) for r in rows], [F(1) for r in rows]]
    need(model_visible[0] == model_visible[1], 'observed extension mismatch')
    effects = [sum(h - v for h, v in zip(hidden, visible)) / len(rows)
               for hidden, visible in zip(model_hidden, model_visible)]
    need(effects == [-mu, 1 - mu], 'sharp endpoint construction')
    return {'receiving': positive, 'producer_disabled': True, 'rejected_controls': rejected,
            'nonidentification_plug_in_illustration': {'observed_sender_rounds': len(rows),
                'visible_mean_normalized': str(mu), 'hidden_mean_endpoints': ['0', '1'],
                'effect_endpoints': list(map(str, effects)),
                'status': 'mathematical extensions of empirical law; not fitted psychological models or population confidence set'}}


if __name__ == '__main__':
    p = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'results.json'
    print(json.dumps(run(p), sort_keys=True, indent=2))
