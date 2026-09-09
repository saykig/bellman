"""Read-only normal/optimized comparison and retained evidence verification."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from subject import require
from receiver import receive

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='cea4e1a47cb91c1f3917490350deab53d2976908'
ALLOWED={'README.md','docs/programme/ROADMAP.md','docs/programme/ARCHITECTURE.md'}

def sha(path): return sha256(path.read_bytes()).hexdigest()

def run():
    if '--verify-retained' in sys.argv:
        result=json.loads((HERE/'results.json').read_text())
        for rel,wanted in result['source_files'].items():
            require(sha(ROOT/rel)==wanted,'retained source changed: '+rel)
            committed=subprocess.run(['git','show',result['source_commit']+':'+rel],cwd=ROOT,capture_output=True,check=True).stdout
            require(sha256(committed).hexdigest()==wanted,'source commit mismatch: '+rel)
        received=receive(json.loads((HERE/'example_subject.json').read_text()),json.loads((HERE/'example_certificate.json').read_text()))
        require(received==result['checks']['positive'],'retained example does not match recorded query')
    outputs=[]
    for flags in ([],['-O']):
        r=subprocess.run([sys.executable,*flags,str(HERE/'checks.py')],capture_output=True,text=True,check=True)
        outputs.append(json.loads(r.stdout))
    require(outputs[0]==outputs[1],'normal/optimized semantic mismatch')
    listing=subprocess.run(['git','ls-tree','-r','--name-only',BASE],cwd=ROOT,capture_output=True,text=True,check=True).stdout.splitlines()
    preserved=0
    for rel in listing:
        if rel in ALLOWED: continue
        original=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True,check=True).stdout
        require((ROOT/rel).read_bytes()==original,'changed inherited file: '+rel)
        preserved+=1
    return {'base_commit':BASE,'normal_optimized_equal':True,'preserved_base_files':preserved,'old_historical_suites':'not rerun; no dependency/import or inherited implementation change','checks':outputs[0]}

if __name__=='__main__': print(json.dumps(run(),sort_keys=True,indent=2))
