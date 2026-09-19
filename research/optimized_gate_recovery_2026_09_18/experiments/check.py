"""Receiver: never imports or executes search.py; reconstructs original cells."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
PRIOR = (F(1, 4), F(1, 4), F(1, 2))
RECEIVER = ((F(2), F(1), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(3)))
SENDER = (F(1), F(0), F(1, 5))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def posterior(delta, a, b, output, certificate=False):
    # Sum theta/S/T joint cells; do not use the candidate's posterior formula.
    source = (F(1, 2) + delta, F(1, 2) - delta, F(1, 4))
    mass = []
    for state in range(3):
        total = F(0)
        for s in (0, 1):
            ps = source[state] if s == 1 else 1 - source[state]
            pt = a if s == 1 else b
            if output == 0:
                pt = 1 - pt
            total += PRIOR[state] * ps * pt
        mass.append(F(0) if certificate and state == 2 else total)
    denom = sum(mass)
    require(denom > 0, 'zero history mass')
    return tuple(x / denom for x in mass)


def utilities(mu, fine):
    return tuple(sum(mu[s] * RECEIVER[s][action] for s in range(3))
                 - (fine if action != 2 else 0) for action in range(3))


def feasible(delta, a, b, fine):
    for h in (0, 1):
        on = utilities(posterior(delta, a, b, h), fine)
        if on[2] < max(on):
            return False
        off = utilities(posterior(delta, a, b, h, True), fine)
        best = [i for i in range(3) if off[i] == max(off)]
        # All mixtures lie in the convex hull of best pure actions. One sender
        # information type has this same utility vector at both eligible states.
        if min(SENDER[i] for i in best) > F(1, 5):
            return False
    return True


def direct_minimum(delta, a, b):
    # Receiver best responses can change only where C meets a penalized action.
    # A-B is independent of fine. Include on-path C constraints as well.
    critical = {F(0)}
    for h in (0, 1):
        for cert in (False, True):
            u = utilities(posterior(delta, a, b, h, cert), F(0))
            critical.update(max(F(0), u[i] - u[2]) for i in (0, 1))
    ordered = sorted(critical)
    hits = [e for e in ordered if feasible(delta, a, b, e)]
    require(bool(hits), 'no feasible critical fine')
    answer = min(hits)
    # Cell interiors below the candidate, plus endpoints, must fail.
    for left, right in zip(ordered, ordered[1:]):
        if right <= answer and right > left:
            require(not feasible(delta, a, b, (left + right) / 2),
                    'unexpected feasible interior below minimum')
    return answer


def verify(packet):
    # Identity binding is an integrity check; producer execution is not trusted.
    require(packet['producer_sha256'] == hashlib.sha256((ROOT / 'search.py').read_bytes()).hexdigest(),
            'stale producer identity')
    require(packet['law_samples_per_gate'] == 9, 'changed source grid')
    gates = [(F(i, 32), F(j, 32)) for i in range(8, 25)
             for j in range(8, 25) if i - j >= 8]
    expected_radii = [F(0), F(1, 1024), F(1, 64), F(1, 16), F(1, 4)]
    require([F(row['t']) for row in packet['rows']] == expected_radii, 'changed radius grid')
    laws_checked = 0
    min_public, min_certificate = F(1), F(1)
    for row in packet['rows']:
        t = F(row['t'])
        values = []
        for a, b in gates:
            needed = F(0)
            for k in range(-4, 5):
                delta = t * F(k, 4)
                needed = max(needed, direct_minimum(delta, a, b))
                laws_checked += 1
                for h in (0, 1):
                    public = posterior(delta, a, b, h)
                    cert = posterior(delta, a, b, h, True)
                    min_public = min(min_public, *public)
                    min_certificate = min(min_certificate, *cert[:2])
                    require(cert[2] == 0, 'certificate leaked excluded state')
                    require(min(public) >= F(1, 12), 'public support bound')
                    require(min(cert[:2]) >= F(3, 8), 'certificate support bound')
                    on = utilities(public, F(0))
                    require(on[2] > max(on[:2]), 'silent target not strictly optimal')
            values.append((needed, a, b))
            # Exact grid check of the analytically derived continuum envelope.
            w, d = (a + b) / 2, a - b
            formula = F(0) if t == 0 else 1 + d * t / min(w, 1 - w)
            require(needed == formula, 'gate envelope mismatch')
        optimum = min(x[0] for x in values)
        opts = [[str(a), str(b)] for val, a, b in values if val == optimum]
        require(row['gate_count'] == len(gates), 'changed gate count')
        require(F(row['value']) == optimum, 'wrong optimum')
        require(row['minimizers'] == opts, 'wrong minimizer set')
        require(optimum == (0 if t == 0 else 1 + t / 2), 'claimed formula mismatch')
    # Decisive model controls, evaluated without the reduced producer.
    for delta in (F(-1, 4), F(0), F(1, 4)):
        require(direct_minimum(delta, F(1, 2), F(1, 2)) == 0, 'erasure control failed')
    # Full-information sender: equal posterior is consistent by typewise trembles;
    # verify its B payoff and sender deterrence directly.
    tied = utilities((F(1, 2), F(1, 2), F(0)), F(0))
    require(tied[1] == max(tied) and SENDER[1] < F(1, 5), 'full-information control failed')
    return {'original_cell_law_gate_checks': laws_checked, 'gates_per_radius': len(gates),
            'radii': len(expected_radii), 'minimum_public_probability_observed': str(min_public),
            'minimum_certificate_probability_observed': str(min_certificate),
            'erasure_and_full_information_controls': 'pass'}


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'candidates.json'
    packet = json.loads(path.read_text())
    outcome = verify(packet)
    # Negative controls: wrong value and stale binding must both be rejected.
    rejected = []
    for mutation in ('wrong_value', 'stale_identity'):
        bad = json.loads(json.dumps(packet))
        if mutation == 'wrong_value':
            bad['rows'][0]['value'] = '1'
        else:
            bad['producer_sha256'] = '0' * 64
        try:
            verify(bad)
        except ValueError:
            rejected.append(mutation)
    require(len(rejected) == 2, 'negative control accepted')
    outcome['negative_controls_rejected'] = rejected
    outcome['status'] = 'exact finite checks passed; continuum claims require written proofs'
    outcome['checker_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    outcome['candidate_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps(outcome, indent=2))


if __name__ == '__main__':
    main()
