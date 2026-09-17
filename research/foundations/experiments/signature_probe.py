#!/usr/bin/env python3
"""Exhaustive finite paper-question probe; exact deterministic mechanisms only."""
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
FUNCTIONS = tuple(product((0, 1), repeat=2))  # constant 0, identity, flip, constant 1
MODELS = tuple(product(range(4), repeat=2))


def signature(model, rich):
    a, b = model
    k, ell = FUNCTIONS[a], FUNCTIONS[b]
    io = (ell[k[0]], ell[k[1]])
    return io + ell if rich else io  # extra queries: do(Y=0), do(Y=1)


def main():
    summaries = {}
    for rich in (False, True):
        sigs = [signature(m, rich) for m in MODELS]
        counts = dict(nonempty_relations=0, nonrectangular=0,
                      nonrectangular_signature_preserved=0,
                      scalar_ranges_preserved_but_signature_changed=0)
        witness = None
        harmless = None
        for mask in range(1, 1 << 16):
            selected = [i for i in range(16) if mask & (1 << i)]
            aset = {MODELS[i][0] for i in selected}
            bset = {MODELS[i][1] for i in selected}
            rectangle = [i for i,m in enumerate(MODELS) if m[0] in aset and m[1] in bset]
            original = {sigs[i] for i in selected}
            relaxed = {sigs[i] for i in rectangle}
            if not original <= relaxed:
                raise AssertionError('outer signature inclusion')
            counts['nonempty_relations'] += 1
            nonrect = len(rectangle) != len(selected)
            counts['nonrectangular'] += nonrect
            if nonrect and original == relaxed:
                counts['nonrectangular_signature_preserved'] += 1
                if harmless is None:
                    harmless = {'model_indices': selected, 'rectangle_indices': rectangle,
                                'signatures': sorted(original)}
            same_scalars = all({s[j] for s in original} == {s[j] for s in relaxed}
                               for j in range(len(sigs[0])))
            if same_scalars and original != relaxed:
                counts['scalar_ranges_preserved_but_signature_changed'] += 1
                if witness is None:
                    witness = {'model_indices': selected, 'rectangle_indices': rectangle,
                               'original_signatures': sorted(original),
                               'spurious_signatures': sorted(relaxed-original)}
        summaries['input_output_plus_do_Y' if rich else 'input_output_only'] = {
            'counts': counts, 'harmless_nonrectangular_witness': harmless,
            'scalar_vs_joint_witness': witness}
    result = {'schema': 'bellman-foundations-signatures-v1',
              'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'functions_by_index': FUNCTIONS, 'models_by_index': MODELS,
              'evidence': summaries}
    encoded = json.dumps(result, sort_keys=True, indent=2) + '\n'
    target = HERE / 'signature-results-v1.json'
    if sys.argv[1:] == ['--write']:
        if target.exists():
            raise RuntimeError('refuse to overwrite evidence')
        target.write_text(encoded)
    elif sys.argv[1:]:
        raise RuntimeError('usage: signature_probe.py [--write]')
    elif target.read_text() != encoded:
        raise AssertionError('fresh evidence differs')
    print(encoded)


if __name__ == '__main__':
    main()
