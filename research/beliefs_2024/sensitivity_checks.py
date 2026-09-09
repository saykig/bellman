"""Producer-disabled rational sensitivity receiving and rejection controls."""
import copy
import importlib.abc
import json
from pathlib import Path
import sys

class Block(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0] in {'analyze','sensitivity','numpy','scipy','pandas','rpy2'}:
            raise ImportError('producer disabled')
        return None
sys.meta_path.insert(0,Block())
from sensitivity_receiver import verify,check_range,F,need


def run(raw,evidence):
    result=json.loads(Path(evidence).read_text()); positive=verify(raw,result); rejected=[]
    def reject(name,data):
        try: verify(raw,data)
        except (ValueError,KeyError): rejected.append(name)
        else: raise RuntimeError('accepted '+name)
    bad=copy.deepcopy(result); bad['states'][0]['treatments']['2']['max_certificates'][0]['upper']='-999'
    reject('false dual bound',bad)
    bad=copy.deepcopy(result); bad['states'][0]['treatments']['2']['min_certificates'][0]['posterior'][0]='-1'
    reject('negative posterior witness',bad)
    bad=copy.deepcopy(result); bad['states'][0]['treatments']['2']['max_certificates'].pop()
    reject('omitted continuation alternative',bad)
    bad=copy.deepcopy(result); bad['states'].pop()
    reject('uncovered history state',bad)
    bad=copy.deepcopy(result); bad['exact_value_error_bound']='0'
    reject('erased numerical residual allowance',bad)
    bad=copy.deepcopy(result); bad['session_response_outer_ranges']['17']['mean_probability_outer'][0]+=.1
    reject('false aggregate outer bound',bad)
    bad=copy.deepcopy(result); bad['shared_pure_priors']['AC']['comparison']['delta_brier']+=.1
    reject('false shared-prior contrast',bad)
    return {'positive':positive,'producer_disabled':True,'rejections':rejected}

if __name__=='__main__': print(json.dumps(run(*sys.argv[1:]),indent=2))
