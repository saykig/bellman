"""Explicit acquisition and end-to-end reproduction; external working files only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.request

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def need(ok,message):
    if not ok: raise RuntimeError(message)


def external(path):
    resolved=Path(path).resolve()
    need(not resolved.is_relative_to(ROOT),'raw/intermediate outputs must remain outside the repository')
    return resolved


def acquire(path):
    target=external(path); need(not target.exists(),'refusing to overwrite acquisition')
    entry=next(s for s in json.loads((HERE/'source-manifest.json').read_text())['sources'] if s['name'].endswith('_data.txt'))
    with urllib.request.urlopen(entry['url'],timeout=60) as response: raw=response.read()
    need(hashlib.sha256(raw).hexdigest()==entry['sha256'],'download edition mismatch')
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as f:f.write(raw)
    return {'source_sha256':entry['sha256'],'bytes':len(raw),'raw_redistributed':False}


def execute(args,log):
    result=subprocess.run(args,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
    log.write_text(result.stdout+result.stderr)
    need(result.returncode==0,'execution failed; inspect '+str(log))


def run(raw,out,refit,optimized):
    import numpy,pandas,scipy
    need([numpy.__version__,pandas.__version__,scipy.__version__]==['2.2.6','2.2.3','1.15.3'],'statistical package version mismatch')
    from reconstruct import read_source
    from receiver import source_rows,residual_bounds,verify_predictions
    raw=external(raw); out=external(out); need(not out.exists(),'refusing to overwrite reproduction')
    data=read_source(raw); out.mkdir(parents=True)
    fits=out/'fits'
    if refit:
        rscript=shutil.which('Rscript'); need(rscript is not None,'Rscript required for mixture refit')
        fits.mkdir(); base=data[data.treatment.eq(2)&data.supergame.ge(5)&data['round'].le(8)]
        columns=['treatment','session','id','supergame','round','coop','o_coop']
        for split in ('train','all'):
            frame=base[~base.session.isin([1,14])] if split=='train' else base
            csv=out/(split+'-source.csv'); frame[columns].to_csv(csv,index=False)
            for catalogue in ('ten','six'):
                name=split+'-'+catalogue
                execute([rscript,str(HERE/'fit_mixture.R'),str(csv),str(fits/name),catalogue],out/(name+'.log'))
    else: shutil.copytree(HERE/'mixture-fits',fits)
    flags=['-O'] if optimized else []
    execute([sys.executable,*flags,str(HERE/'analyze.py'),str(raw),str(fits),str(out/'results')],out/'analysis.log')
    fresh=json.loads((out/'results/parameters.json').read_text())
    summaries=json.loads((out/'results/results.json').read_text())['comparisons']
    observations=source_rows(raw); receiving={}; max_difference=0
    for label,bundle in fresh.items():
        predictions=json.loads((out/'results'/f'{label}-predictions.json').read_text())
        retained=json.loads((HERE/'first-results'/f'{label}-predictions.json').read_text())
        need(len(predictions)==len(retained),'fresh query count mismatch')
        for a,b in zip(predictions,retained):
            need(a['key']==b['key'] and set(a)==set(b),'fresh query identity mismatch')
            for key in a:
                if key!='key': max_difference=max(max_difference,abs(a[key]-b[key]))
        receiving[label]={**residual_bounds(bundle),**verify_predictions(observations,bundle,predictions,summaries[label])}
    need(max_difference<=1e-7,'fresh predictions differ materially from first results')
    result={'mixtures_refitted':refit,'optimized':optimized,'max_prediction_difference_from_first':max_difference,
        'fresh_receiving':receiving,'scope':'fresh source-only fitting/scoring and independent numerical receiving; not global optimizer or sampling validity proof'}
    (out/'reproduction.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('acquire');a.add_argument('path')
    r=sub.add_parser('run');r.add_argument('source');r.add_argument('output');r.add_argument('--refit-mixtures',action='store_true');r.add_argument('--optimized',action='store_true')
    args=p.parse_args()
    result=acquire(args.path) if args.command=='acquire' else run(args.source,args.output,args.refit_mixtures,args.optimized)
    print(json.dumps(result,indent=2))
