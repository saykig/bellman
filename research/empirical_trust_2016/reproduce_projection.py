"""Verify original archive CSV and reproduce the selected columns. No live fetch in tests."""
import csv
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: reproduce_projection.py /path/to/daF3661_eng.csv')
    manifest = json.loads((HERE / 'provenance.json').read_text())
    raw = Path(sys.argv[1]).read_bytes()
    if sha256(raw).hexdigest() != manifest['downloaded_files']['daF3661_eng.csv']['sha256']:
        raise SystemExit('original archive CSV identity mismatch; do not silently substitute a newer edition')
    rows = csv.DictReader(StringIO(raw.decode('utf-8-sig')), delimiter=';')
    out = StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=manifest['projection']['columns'], lineterminator='\n')
    writer.writeheader()
    for r in rows:
        writer.writerow({k: r[k] for k in writer.fieldnames})
    if out.getvalue().encode() != (HERE / 'observations.csv').read_bytes():
        raise SystemExit('projection mismatch')
    print('Original CSV hash and exact selected-column projection verified.')
