"""Bounded shared power-witness input; no posterior computation here."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'sequential_credibility'))
from subject import Invalid, rational, require, validate, digest  # noqa: E402

SEMANTICS = 'one-common-power-sequence-all-models.v1'


class WitnessFailure(Invalid):
    """A failed warrant is not a proof of assessment inconsistency."""

    def __init__(self, code, detail=''):
        self.code = code
        super().__init__(code + (': ' + detail if detail else ''))


def demand(ok, code, detail=''):
    if not ok:
        raise WitnessFailure(code, detail)


def validate_witness(s, w):
    infos = validate(s)
    demand(type(w) is dict and set(w) == set(infos), 'witness-information-coverage')
    for I, row in s['profile'].items():
        zeros = {a for a, q in row.items() if rational(q) == 0}
        demand(type(w[I]) is dict and set(w[I]) == zeros, 'witness-action-coverage', I)
        for a, term in w[I].items():
            demand(type(term) is dict and set(term) == {'coefficient', 'order'},
                   'malformed-witness-term', I + '/' + a)
            try:
                c = rational(term['coefficient'])
            except Invalid as exc:
                raise WitnessFailure('invalid-witness-coefficient', str(exc)) from None
            demand(c > 0, 'nonpositive-witness-coefficient')
            k = term['order']
            demand(type(k) is int and k > 0, 'invalid-witness-order')
            demand(k <= 32, 'unsupported-witness-order')
    return infos
