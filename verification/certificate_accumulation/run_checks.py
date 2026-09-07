"""Run exact cases and the unchanged transport/preservation command."""
import hashlib,json,os,platform,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE="cd649db893c70bbce4891c8f526a27aaf1bcda1b"
def run():
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1")
    def call(args):
        start=time.perf_counter()
        out=subprocess.check_output([sys.executable]+args,cwd=ROOT,env=env,text=True)
        return out,time.perf_counter()-start
    runs=[];times=[]
    for flag in ([],["-O"]):
        raw,elapsed=call(flag+["verification/certificate_accumulation/checks.py"])
        runs.append(json.loads(raw));times.append(elapsed)
    if runs[0]["results"]!=runs[1]["results"] or runs[0]["rejections"]!=runs[1]["rejections"]:
        raise RuntimeError("mode disagreement")
    raw,seconds=call(["verification/certificate_transport/run_checks.py"])
    old=json.loads(raw.split("BELLMAN_TRANSPORT_RESULT_BEGIN\n")[1].split("\nBELLMAN_TRANSPORT_RESULT_END")[0])
    paths=subprocess.check_output(["git","ls-tree","-r","--name-only",BASE],cwd=ROOT,text=True).splitlines()
    for p in paths:
        before=subprocess.check_output(["git","show",BASE+":"+p],cwd=ROOT)
        now=(ROOT/p).read_bytes()
        if p not in ("README.md","SUBSTRATE_LEDGER.md","FINDINGS_LEDGER.md") and before!=now:
            raise RuntimeError("historical change: "+p)
        if p.endswith("LEDGER.md") and not now.startswith(before):
            raise RuntimeError("ledger rewrite")
    sources=["verification/certificate_accumulation/"+p for p in ("accumulate.py","checks.py","run_checks.py","README.md")]
    sources+=["foundations/BELLMAN_CERTIFICATE_ACCUMULATION_AND_POLICY_SELECTION.md",".github/workflows/certificate-accumulation.yml"]
    result=dict(base_commit=BASE,executed_commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        runtime=platform.python_version(),execution="GitHub Actions",modes=["normal","-O"],failed=0,
        passed_per_mode=runs[0]["passed"],rejections_per_mode=runs[0]["rejections"],seconds_by_mode=times,
        preservation_seconds=seconds,results=runs[0]["results"],normal_optimized_equal=True,
        source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources},
        historical_files_preserved=True,
        preservation={k:old[k] for k in ("passed_per_mode","rejections_per_mode","sequential_passed_per_mode","pr4_repair_passed_per_mode","joint_law_passed_per_mode","historical_joint_law_observations_and_certificates_equal")},
        limitations=["Fixed cases and analytical proofs, not formal verification or statistical coverage.",
                     "Attached reviewer executions are separately attributed, not replayed here."])
    print("ACCUMULATION_RESULT_BEGIN")
    print(json.dumps(result,sort_keys=True))
    print("ACCUMULATION_RESULT_END")
if __name__=="__main__":run()
