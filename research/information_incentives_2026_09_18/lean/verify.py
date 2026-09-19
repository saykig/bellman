"""Use a matching built Mathlib cache read-only. Prints a source-bound receipt."""
import argparse,hashlib,json,os,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--packages',type=Path,required=True);p.add_argument('--lean',default='lean');a=p.parse_args()
root=Path(__file__).resolve().parent
rev=subprocess.check_output(['git','-C',str(a.packages/'mathlib'),'rev-parse','HEAD'],text=True).strip()
if rev!='0df444a360eaa60ab8c11dca51a86af692955474':raise SystemExit('Wrong Mathlib revision')
paths=[str(x/'.lake/build/lib/lean') for x in a.packages.iterdir() if (x/'.lake/build/lib/lean').is_dir()]
if not paths:raise SystemExit('Missing built dependencies')
cmd=[a.lean,'+leanprover/lean4:v4.33.1']
version=subprocess.check_output(cmd+['--version'],text=True).strip()
r=subprocess.run(cmd+[str(root/'CompositionCore.lean')],env=dict(os.environ,LEAN_PATH=':'.join(paths)),text=True,capture_output=True)
log=r.stdout+r.stderr
if r.returncode or 'sorryAx' in log:raise SystemExit(log or r.returncode)
print(json.dumps({'status':'checked','toolchain':version,'mathlib_revision':rev,
  'source_sha256':hashlib.sha256((root/'CompositionCore.lean').read_bytes()).hexdigest(),
  'output':log},indent=2))
