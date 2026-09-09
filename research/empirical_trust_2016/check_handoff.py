"""One concrete intended-use revision, not a general Writ adapter."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from receiver import receive, need

HERE = Path(__file__).resolve().parent


def check(case):
    raw = (HERE / 'results.json').read_bytes()
    original = case['original']
    successor = case['successor']
    identity = sha256(raw).hexdigest()
    need(original['result_file'] == 'results.json' and original['result_sha256'] == identity,
         'old evidence mismatch')
    need(original['plan_sha256'] == sha256((HERE / 'PLAN.md').read_bytes()).hexdigest(), 'plan mismatch')
    old = receive(json.loads(raw), original['intended_use'])
    need(successor['parent_result_sha256'] == identity, 'revision parent mismatch')
    need(successor['intended_use'] == 'causal-feedback-erasure.v1', 'revision query mismatch')
    need(successor['disposition'] == 'not_identified_without_additional_assumptions' and
         successor['replay_old_as_new'] == 'reject' and successor['authority_to_intervene'] == 'not_supplied', 'revision overclaim')
    try:
        receive(json.loads(raw), successor['intended_use'])
    except ValueError as error:
        need('unsupported intended use' in str(error), 'wrong revision failure')
    else:
        raise RuntimeError('unsupported transfer accepted')
    return {'old_result': old['status'], 'old_bytes_preserved': True,
            'new_use': 'rejected', 'new_claim': successor['disposition'], 'native_writ_import': 'not_supported'}


if __name__ == '__main__':
    case = json.loads((HERE / 'portable_handoff.json').read_text())
    result = check(case)
    for field in ('parent_result_sha256', 'intended_use', 'disposition'):
        altered = deepcopy(case)
        altered['successor'][field] = 'incorrect'
        try:
            check(altered)
        except ValueError:
            pass
        else:
            raise RuntimeError('altered revision accepted: ' + field)
    result['rejected_revision_controls'] = 3
    print(json.dumps(result, sort_keys=True))
