"""Decisive receiving controls, including producer-disabled execution."""
import copy
import importlib.abc
import json
from pathlib import Path
import sys
import tempfile


class NoProducers(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0] in {'analyze','reconstruct','numpy','scipy','pandas','sklearn','rpy2'}:
            raise ImportError('producer disabled: '+fullname)
        return None


sys.meta_path.insert(0,NoProducers())
import receiver as r


def run(raw):
    positive=r.run(raw)
    source=r.source_rows(raw)
    bundle=json.loads((r.HERE/'first-results/parameters.json').read_text())['ten-linear']
    predictions=json.loads((r.HERE/'first-results/ten-linear-predictions.json').read_text())
    summary=json.loads((r.HERE/'first-results/results.json').read_text())['comparisons']['ten-linear']
    rejected=[]
    def reject(name,fn):
        try: fn()
        except (ValueError,KeyError): rejected.append(name)
        else: raise RuntimeError('negative control accepted: '+name)
    bad=copy.deepcopy(bundle); bad['values']['2'][0][0][0][0]+=.01
    reject('false Markov value',lambda:r.residual_bounds(bad))
    bad=copy.deepcopy(bundle); bad['mixture']['automata'][3]['transitions'][0][1]=0
    reject('TFT orientation changed',lambda:r.residual_bounds(bad))
    bad=copy.deepcopy(bundle); bad['mixture']['noise']=.2
    reject('noise rebound',lambda:r.residual_bounds(bad))
    bad=copy.deepcopy(bundle); bad['utility']='unrestricted human utility'
    reject('unsupported utility authority',lambda:r.residual_bounds(bad))
    bad=copy.deepcopy(bundle); bad['response']['coefficients'][1]=-1
    reject('negative incentive response outside class',lambda:r.verify_predictions(source,bad,predictions,summary))
    bad=copy.deepcopy(predictions); bad.pop()
    reject('missing target query',lambda:r.verify_predictions(source,bundle,bad,summary))
    bad=copy.deepcopy(predictions); bad.append(copy.deepcopy(bad[0]))
    reject('duplicate target query',lambda:r.verify_predictions(source,bundle,bad,summary))
    bad=copy.deepcopy(predictions); bad[0]['key'][3]=1
    reject('wrong decision time',lambda:r.verify_predictions(source,bundle,bad,summary))
    bad=copy.deepcopy(predictions); bad[0]['updated']+=.01
    reject('changed prediction',lambda:r.verify_predictions(source,bundle,bad,summary))
    bad=copy.deepcopy(predictions); bad[0]['current_belief']=.5
    reject('unregistered current-report feature',lambda:r.verify_predictions(source,bundle,bad,summary))
    bad=copy.deepcopy(summary); bad['sessions'][0]['models']['fixed']['brier']+=.01
    reject('false Brier score',lambda:r.verify_predictions(source,bundle,predictions,bad))
    bad=copy.deepcopy(summary); bad['comparison']['delta_brier']+=.01
    reject('false primary contrast',lambda:r.verify_predictions(source,bundle,predictions,bad))
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'changed-source.txt'; path.write_bytes(Path(raw).read_bytes()+b'\n')
        reject('source byte mismatch',lambda:r.source_rows(path))
    return {'positive':positive,'rejections':rejected,'producer_disabled':True,
            'not_checked':'global mixture optimum, bootstrap coverage, human preferences, causal treatment assignment'}


if __name__=='__main__': print(json.dumps(run(sys.argv[1]),indent=2))
