"""Explicit author-edition acquisition check, design reconstruction and replication.

Raw rows remain outside Git. Run with the separately downloaded source path and an
output JSON path. No fitting or treatment-dependent model selection occurs here.
"""
import hashlib
import io
import json
from pathlib import Path
import sys

import pandas as pd

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read_source(path):
    raw = Path(path).read_bytes()
    spec = json.loads((HERE / 'source-manifest.json').read_text())
    entry = next(s for s in spec['sources'] if s['name'].endswith('_data.txt'))
    need(hashlib.sha256(raw).hexdigest() == entry['sha256'], 'source identity mismatch')
    return pd.read_csv(io.StringIO(raw.decode().split('**************', 1)[1].strip()), sep='\t')


def reconstruct(df):
    keys = ['session', 'id', 'supergame', 'round']
    need(not df.duplicated(keys).any(), 'duplicate subject-time')
    need(set(df.treatment) == {1, 2, 3, 4}, 'treatment domain')
    need(df.groupby('session').treatment.nunique().eq(1).all(), 'treatment drift')
    need(df.beliefon.eq(df.supergame.ge(5).astype(int)).all(), 'elicitation timing')
    need(df.loc[df.beliefon.eq(1), ['belief', 'o_belief']].notna().all().all(), 'missing reports')
    need(df.loc[df.beliefon.eq(0), ['belief', 'o_belief']].isna().all().all(), 'unexpected reports')
    for name in ['coop', 'o_coop']:
        need(df[name].isin([0, 1]).all(), 'action domain')
    for name in ['belief', 'o_belief']:
        need(df[name].dropna().between(0, 1).all(), 'report domain')
    for _, group in df.groupby(['session', 'id', 'supergame']):
        need(sorted(group['round']) == list(range(1, len(group)+1)), 'broken history')
        need(len(group) >= 8, 'short initial block')
    for _, group in df.groupby(['session', 'supergame', 'round']):
        need(int(group.coop.sum()) == int(group.o_coop.sum()), 'unmatched action margins')
        need(int(((group.coop == 1) & (group.o_coop == 0)).sum()) ==
             int(((group.coop == 0) & (group.o_coop == 1)).sum()), 'unbalanced action pairs')
        need(abs(group.belief.sum()-group.o_belief.sum()) < 1e-10, 'unmatched report margins')
        need(group.validround.nunique() <= 1, 'termination draw not common')
    need(df.loc[df.treatment.eq(1), 'validround'].isna().all(), 'finite validity semantics')
    indefinite = df[df.treatment.ne(1)]
    need(indefinite.validround.isin([0, 1]).all(), 'indefinite validity missing')
    need(indefinite.loc[indefinite['round'].gt(8), 'validround'].eq(1).all(), 'post-block invalidity')
    for _, group in indefinite.groupby(['session', 'supergame']):
        flags = group.groupby('round').validround.first().tolist()
        need(flags == sorted(flags, reverse=True), 'validity returns after termination')
    counts = df.groupby(['treatment', 'session']).agg(people=('id', 'nunique'),
             supergames=('supergame', 'nunique'), rows=('id', 'size')).reset_index()
    late = df[df.late.eq(1) & df['round'].le(8)]
    per_round = late.groupby(['treatment', 'round']).agg(coop=('coop', 'mean'),
                  belief=('belief', 'mean'), rows=('id', 'size')).reset_index()
    per_round['belief_minus_coop'] = per_round.belief-per_round.coop
    sessions = late.groupby(['treatment', 'session', 'round']).agg(
        coop=('coop', 'mean'), belief=('belief', 'mean'), rows=('id', 'size')).reset_index()
    return {'schema': 'bellman.afy2024.reconstruction.v1',
            'specification_commit': '4abea07', 'rows': len(df),
            'participants': len(df[['session', 'id']].drop_duplicates()),
            'sessions': counts.to_dict(orient='records'),
            'late_first_eight_pooled_rounds': per_round.to_dict(orient='records'),
            'late_first_eight_session_rounds': sessions.to_dict(orient='records'),
            'validity_counts': {'finite_structural_na': int(df.validround.isna().sum()),
                 'indefinite_valid': int(indefinite.validround.sum()),
                 'indefinite_invalid': int(indefinite.validround.eq(0).sum())},
            'pair_identity': 'not supplied; matching margins do not reconstruct pairs'}


if __name__ == '__main__':
    result = reconstruct(read_source(sys.argv[1]))
    Path(sys.argv[2]).write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps({'rows': result['rows'], 'participants': result['participants'],
                      'rounds': result['late_first_eight_pooled_rounds']}, indent=2))
