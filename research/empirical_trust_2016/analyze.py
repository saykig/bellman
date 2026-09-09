"""Fixed retrospective analysis. Candidate producer; receiver.py does not import this file."""
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import sys

import numpy as np
import pandas as pd
from scipy.stats import bootstrap
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
import statsmodels.formula.api as smf

HERE = Path(__file__).resolve().parent
INPUTS = ('PLAN.md', 'observations.csv', 'provenance.json')
NAMES = ['treatment_' + str(t) for t in range(1, 5)] + ['round_' + str(t) for t in range(2, 7)]
NAMES += ['sent_lag_' + str(i) for i in range(1, 6)]
FULL_NAMES = NAMES + ['return_lag_' + str(i) for i in range(1, 6)]


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def data():
    d = pd.read_csv(HERE / 'observations.csv')
    s = d[d.Rank.isin([2, 3])].sort_values(['ID', 'Period']).copy()
    for k in range(1, 6):
        s['sent_lag_' + str(k)] = s.groupby('ID').give.shift(k).fillna(0) / 12
        s['return_lag_' + str(k)] = s.groupby('ID').returned.shift(k).fillna(0) / 84
    s = s[s.Period > 1].copy()
    for t in range(1, 5):
        s['treatment_' + str(t)] = (s.Treatment == t).astype(int)
    for t in range(2, 7):
        s['round_' + str(t)] = (s.Period == t).astype(int)
    return d, s


def produce():
    d, s = data()
    test_sessions = []
    for t in range(1, 5):
        sessions = sorted(d.loc[d.Treatment == t, 'Session'].unique())
        test_sessions.append(int(min(sessions, key=lambda z: hashlib.sha256(
            f'bellman-fsd3661-holdout-v1:{z}'.encode()).hexdigest())))
    test = s[s.Session.isin(test_sessions)]
    train = s[~s.Session.isin(test_sessions)]
    y = train.give.to_numpy() / 12
    models = {}
    pred = {}
    for label, names in [('reduced', NAMES), ('full', FULL_NAMES)]:
        fit = Ridge(alpha=1, fit_intercept=True, solver='svd').fit(train[names], y)
        pred[label] = np.clip(fit.predict(test[names]), 0, 1)
        models[label] = {'features': names, 'intercept': repr(float(fit.intercept_)),
                         'coefficients': [repr(float(v)) for v in fit.coef_]}
    means = train.groupby('Treatment').give.mean() / 12
    pred['treatment_mean'] = test.Treatment.map(means).to_numpy()
    pred['persistence'] = test.sent_lag_1.to_numpy()
    records = []
    for j, row in enumerate(test.itertuples()):
        records.append({'id': int(row.ID), 'round': int(row.Period), 'session': int(row.Session),
                        'treatment': int(row.Treatment), 'sent': int(row.give),
                        'predictions': {name: repr(float(p[j])) for name, p in pred.items()}})
    per_session = []
    actual = test.give.to_numpy() / 12
    for session in test_sessions:
        mask = (test.Session == session).to_numpy()
        mse = {k: float(mean_squared_error(actual[mask], p[mask])) for k, p in pred.items()}
        per_session.append({'session': session, 'rows': int(mask.sum()), 'mse': mse,
                            'difference': mse['reduced'] - mse['full']})
    delta = np.array([s['difference'] for s in per_session])
    half = float(np.sqrt(2 * np.log(20) / len(test_sessions)))
    interval = [max(-1., float(delta.mean()) - half), min(1., float(delta.mean()) + half)]
    boot = bootstrap((delta,), np.mean, confidence_level=.9, method='percentile',
                     n_resamples=9999, rng=np.random.default_rng(20260909))
    replication = []
    senders = d[d.Rank.isin([2, 3])]
    for t, rows in senders.groupby('Treatment'):
        replication.append({'treatment': int(t), 'sender_rounds': len(rows),
                            'mean_sent': float(rows.give.mean()),
                            'mean_returned': float(rows.returned.mean())})
    sessions = senders.groupby(['Session', 'Treatment']).give.mean().reset_index()
    fit = smf.ols('give ~ C(Treatment)', data=sessions).fit()
    # (J+P - J) - (P - B): coefficient 4 - coefficient 3 - coefficient 2.
    contrast = fit.t_test([0, -1, -1, 1])
    treatment = {'session_means': sessions.to_dict('records'), 'residual_df': int(fit.df_resid),
                 'interaction_points': float(contrast.effect[0]),
                 'interaction_standard_error': float(contrast.sd[0, 0]),
                 'interaction_95ci': contrast.conf_int().tolist()[0],
                 'interaction_p_two_sided_model_based': float(contrast.pvalue)}
    mse = {k: float(np.mean([v['mse'][k] for v in per_session])) for k in pred}
    return {'kind': 'retrospective-mean-prediction.v1',
            'input_sha256': {p: digest(HERE / p) for p in INPUTS},
            'producer_sha256': digest(Path(__file__)),
            'runtime': {'python': platform.python_version(), 'packages': {
                p: importlib.metadata.version(p) for p in ['numpy', 'pandas', 'scipy', 'scikit-learn', 'statsmodels']}},
            'split': {'test_sessions': test_sessions, 'train_sessions': sorted(map(int, train.Session.unique())),
                      'train_rows': len(train), 'test_rows': len(test)},
            'models': models, 'predictions': records, 'reproduction': replication,
            'treatment_comparison': treatment, 'session_scores': per_session,
            'scores': {'normalized_mse': mse, 'rmse_points': {k: 12 * float(np.sqrt(v)) for k, v in mse.items()},
                       'reduced_minus_full': float(delta.mean()), 'equivalence_margin': .01,
                       'hoeffding_90ci': interval, 'hoeffding_half_width': half,
                       'equivalence': 'not_established',
                       'descriptive_cluster_bootstrap_90ci': [float(boot.confidence_interval.low), float(boot.confidence_interval.high)],
                       'bootstrap_warning': 'Four heterogeneous clusters; sensitivity only, not primary inference.'}}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: analyze.py NEW_OUTPUT.json (refuses overwrite)')
    result = produce()
    with Path(sys.argv[1]).open('x') as f:
        json.dump(result, f, sort_keys=True, indent=2, allow_nan=False)
        f.write('\n')
    print(json.dumps({k: result[k] for k in ['split', 'reproduction', 'treatment_comparison', 'scores']}, indent=2))
