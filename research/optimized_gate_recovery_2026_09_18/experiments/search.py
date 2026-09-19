"""Bounded rational search; candidate producer, not a proof of the continuum."""
from fractions import Fraction as F
from pathlib import Path
import json
import hashlib

ROOT = Path(__file__).resolve().parent


def threshold(delta, a, b):
    # Reduced candidate formula, independently tested by check.py from joint cells.
    w, d = (a + b) / 2, a - b
    qs = [F(1, 2) + d * delta / (2 * w),
          F(1, 2) - d * delta / (2 * (1 - w))]
    return max([F(0)] + [2 * q for q in qs if q > F(1, 2)])


def main():
    gates = [(F(i, 32), F(j, 32)) for i in range(8, 25)
             for j in range(8, 25) if i - j >= 8]
    radii = [F(0), F(1, 1024), F(1, 64), F(1, 16), F(1, 4)]
    rows = []
    for t in radii:
        scored = [(max(threshold(t * F(k, 4), a, b) for k in range(-4, 5)), a, b)
                  for a, b in gates]
        value = min(x[0] for x in scored)
        opts = [x for x in scored if x[0] == value]
        rows.append({'t': str(t), 'value': str(value), 'gate_count': len(gates),
                     'minimizers': [[str(a), str(b)] for _, a, b in opts]})
    packet = {'scope': 'finite rational grid, not continuum proof',
              'producer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'law_samples_per_gate': 9, 'rows': rows}
    print(json.dumps(packet, indent=2))


if __name__ == '__main__':
    main()
