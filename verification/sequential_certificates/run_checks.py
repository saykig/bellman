"""One cloud/local command; compact outputs, no environment or toolchain setup."""
import hashlib, json, os, platform, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE="b1266137f824dc65e614722f1f0592846b915262"

def need(ok, why):
    if not ok:
        raise RuntimeError(why)

def run():
    mode_results=[]
    preservation=[]
    with tempfile.TemporaryDirectory() as tmp:
        for optimized in (False,True):
            prefix=[sys.executable]+(["-O"] if optimized else [])
            env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1")
            output=subprocess.check_output(prefix+["verification/sequential_certificates/checks.py"],cwd=ROOT,env=env,text=True)
            mode_results.append(json.loads(output))
            old={}
            for name,path in [("pr4_repair","verification/pr4_repair/repair_checks.py"),
                              ("joint_law","verification/joint_law_completion/module_checks.py")]:
                dest=str(Path(tmp)/(name+str(optimized)+".json"))
                subprocess.check_output(prefix+[path,"--output",dest],cwd=ROOT,env=env,text=True)
                old[name]=json.loads(Path(dest).read_text())
            preservation.append(old)
    need(mode_results[0]["results"]==mode_results[1]["results"],"sequential modes disagree")
    need(mode_results[0]["failed"]==mode_results[1]["failed"]==0,"failed cases")
    for name in ("pr4_repair","joint_law"):
        need(preservation[0][name]["results"]==preservation[1][name]["results"],"preservation modes disagree")
    historical=json.loads((ROOT/"verification/joint_law_completion/module_results.json").read_text())
    need(historical["results"]==preservation[0]["joint_law"]["results"],"historical observations changed")
    need(historical["certificates"]==preservation[0]["joint_law"]["certificates"],"historical certificate values changed")
    tracked=subprocess.check_output(["git","ls-tree","-r","--name-only",BASE],cwd=ROOT,text=True).splitlines()
    allowed={"README.md","SUBSTRATE_LEDGER.md","FINDINGS_LEDGER.md"}
    for name in tracked:
        old=subprocess.check_output(["git","show",BASE+":"+name],cwd=ROOT)
        now=(ROOT/name).read_bytes()
        if name not in allowed:
            need(old==now,"historical file changed: "+name)
        elif name!="README.md":
            need(now.startswith(old),"ledger not append-only: "+name)
    source_names=["reference.py","checks.py","run_checks.py"]
    hashes={"verification/sequential_certificates/"+n:hashlib.sha256(Path(__file__).with_name(n).read_bytes()).hexdigest() for n in source_names}
    for name in ("foundations/BELLMAN_SEQUENTIAL_CERTIFICATE_COMPOSITION.md",".github/workflows/sequential-certificates.yml"):
        hashes[name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    result={"base_commit":BASE,"executed_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
            "runtime":platform.python_version(),"execution":"GitHub Actions" if os.getenv("GITHUB_ACTIONS") else "user-selected runtime",
            "modes":["normal","-O"],"sequential_passed_per_mode":mode_results[0]["passed"],
            "sequential_results":mode_results[0]["results"],"failed":0,
            "pr4_repair_passed_per_mode":preservation[0]["pr4_repair"]["passed_cases"],
            "joint_law_passed_per_mode":preservation[0]["joint_law"]["passed_cases"],
            "normal_optimized_observations_equal":True,"historical_joint_law_observations_and_certificates_equal":True,
            "historical_files_byte_identical":True,"source_sha256":hashes,
            "limits":["Fixed instances, not formal verification or empirical premise validation.",
                      "Producer/checker share Fraction arithmetic and schema; forward path checks are a separate calculation.",
                      "No unavailable historical harness or recovery packet used."]}
    print("BELLMAN_RESULT_BEGIN")
    print(json.dumps(result,sort_keys=True))
    print("BELLMAN_RESULT_END")

if __name__=="__main__":
    run()
