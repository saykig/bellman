"""Cloud fixed checks and preservation; existing Python, standard library only."""
import hashlib, json, os, platform, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE="e4139b6c68f0386b62bf6332b12d2f654c1d4faf"

def need(ok, why):
    if not ok:
        raise RuntimeError(why)

def run():
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1")
    results=[]
    durations=[]
    for optimized in (False,True):
        start=time.perf_counter()
        args=[sys.executable]+(["-O"] if optimized else [])
        raw=subprocess.check_output(args+["verification/certificate_transport/checks.py"],cwd=ROOT,env=env,text=True)
        durations.append(time.perf_counter()-start)
        results.append(json.loads(raw))
    need(results[0]["results"]==results[1]["results"],"normal/-O observations differ")
    need(results[0]["rejections"]==results[1]["rejections"],"normal/-O rejections differ")
    need(results[0]["failed"]==results[1]["failed"]==0,"failed transport cases")
    start=time.perf_counter()
    raw=subprocess.check_output([sys.executable,"verification/sequential_certificates/run_checks.py"],cwd=ROOT,env=env,text=True)
    old=json.loads(raw.split("BELLMAN_RESULT_BEGIN\n",1)[1].split("\nBELLMAN_RESULT_END",1)[0])
    preservation_seconds=time.perf_counter()-start
    need(old["failed"]==0,"preservation failed")
    names=subprocess.check_output(["git","ls-tree","-r","--name-only",BASE],cwd=ROOT,text=True).splitlines()
    allowed={"README.md","SUBSTRATE_LEDGER.md","FINDINGS_LEDGER.md"}
    for name in names:
        original=subprocess.check_output(["git","show",BASE+":"+name],cwd=ROOT)
        now=(ROOT/name).read_bytes()
        if name not in allowed:
            need(now==original,"base file changed: "+name)
        elif name!="README.md":
            need(now.startswith(original),"ledger historical text changed")
    paths=["verification/certificate_transport/"+p for p in ("transport.py","checks.py","run_checks.py","README.md")]
    paths+=["foundations/BELLMAN_CERTIFICATE_TRANSPORT_AND_REVALIDATION.md",
            ".github/workflows/certificate-transport.yml","verification/sequential_certificates/reference.py"]
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    need(hashes["verification/sequential_certificates/reference.py"]==
         "99d0f1a3a32334cce826a7a582502122bc25e195f7024ed40f0c45753cbde1df","reviewed source identity")
    out=dict(base_commit=BASE,executed_commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
             runtime=platform.python_version(),execution="GitHub Actions" if os.getenv("GITHUB_ACTIONS") else "selected runtime",
             modes=["normal","-O"],passed_per_mode=results[0]["passed"],rejections_per_mode=results[0]["rejections"],
             failed=0,transport_seconds_by_mode=durations,preservation_seconds=preservation_seconds,
             normal_optimized_observations_equal=True,results=results[0]["results"],source_sha256=hashes,
             base_files_byte_identical_except_current_pointers=True,
             sequential_passed_per_mode=old["sequential_passed_per_mode"],
             pr4_repair_passed_per_mode=old["pr4_repair_passed_per_mode"],
             joint_law_passed_per_mode=old["joint_law_passed_per_mode"],
             historical_joint_law_observations_and_certificates_equal=old["historical_joint_law_observations_and_certificates_equal"],
             limits=["Fixed instances and analytical proofs, not formal verification or empirical coverage.",
                     "Shared Fraction arithmetic; separate forward oracle is not independent authorship.",
                     "Supplied reviewer runs remain attributed; no missing historical harness replay claimed."])
    print("BELLMAN_TRANSPORT_RESULT_BEGIN")
    print(json.dumps(out,sort_keys=True))
    print("BELLMAN_TRANSPORT_RESULT_END")

if __name__=="__main__":
    run()
