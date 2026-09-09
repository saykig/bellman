"""Exact controls, including producer-disabled receiving, with retained identities."""
from copy import deepcopy
from pathlib import Path
from fractions import Fraction as F
import json
import shutil
import subprocess
import sys
import tempfile
from candidate import build
from receive_case import receive, digest, QUERY
from witness import Invalid
from cases import unit_witness
from valuation_producer import produce as consistency_produce
from consistency_receiver import receive as consistency_receive

ROOT=Path(__file__).resolve().parents[2]

def need(ok,why):
    if not ok:raise RuntimeError(why)


def run():
    c=json.loads((ROOT/'verification/diagnostic_erasure/example_case.json').read_text())
    need(c==build(),'retained candidate differs')
    expected=dict(c['identity']);answer=receive(c,expected);rejections=[]
    def reject(label,fn):
        try:fn()
        except Invalid:rejections.append(label)
        else:raise RuntimeError('accepted '+label)
    for label,change in [
        ('false obstruction ratio',lambda x:x['obstruction']['required_ratios'].__setitem__(0,'1')),
        ('same model is not an obstruction',lambda x:x.update(obstruction={'models':['high','high'],'required_ratios':['3/5','3/5']})),
        ('unknown model',lambda x:x['obstruction']['models'].__setitem__(0,'missing')),
        ('missing individual model warrant',lambda x:x['individual_targets'].pop('low')),
        ('modelwise witness swapped',lambda x:x['individual_targets']['low'].update(warrant=x['individual_targets']['high']['warrant'])),
        ('missing continuation row',lambda x:x['target_incentives']['rows'].pop()),
        ('false value with valid odds',lambda x:x['target_incentives']['rows'][0].update(best='99')),
        ('false source limiting belief',lambda x:x['source_warrant']['belief_rows'][0]['beliefs'].update({'missing':'1'})),
        ('model-indexed tremble injection',lambda x:x['source_warrant']['witness'].update(high={})),
        ('receiver repair changes sender tremble',lambda x:x['private_warrant']['witness']['A.g.H']['N'].update(coefficient='2')),
        ('extra acceptance flag',lambda x:x.update(accepted=True)),
        ('wrong query',lambda x:x.update(query='root-value-only'))]:
        bad=deepcopy(c);change(bad);reject(label,lambda:receive(bad,expected))
    bad=deepcopy(c);bad['target']['models']['high']['payoffs']['accept.g']['B']='2'
    reject('stale caller subject binding',lambda:receive(bad,expected))
    for label,mutate in [
        ('freshly bound payoff outside proved class',lambda x:x['target']['models']['high']['payoffs']['accept.g'].update(B='2')),
        ('freshly bound changed marginal',lambda x:x['target']['models']['high']['chance']['root'].update(g='1/2',b='1/2')),
        ('freshly bound changed assessment',lambda x:x['target']['models']['high']['beliefs']['B'].update({'B.g':'1/3','B.b':'2/3'})),
        ('freshly bound private information change',lambda x:x['sender_retains_signal']['nodes']['A.g.H'].update(info='A.g.L'))]:
        bad=deepcopy(c);mutate(bad);bad['identity']={k:digest(bad[k]) for k in expected}
        reject(label,lambda:receive(bad,bad['identity']))
    same=deepcopy(c)
    for key in expected:
        same[key]['models']['low']=deepcopy(same[key]['models']['high'])
    same['identity']={k:digest(same[k]) for k in expected}
    same['obstruction']['required_ratios']=['3/5','3/5']
    reject('compatible odds family cannot prove impossibility',lambda:receive(same,same['identity']))
    reject('caller query rebinding',lambda:receive(c,expected,'root-value-only'))
    revised=deepcopy(c['target'])
    for m in revised['models'].values():m['beliefs']['B']={'B.g':'0','B.b':'1'}
    rw=unit_witness(revised);rw['A.g']['N']['order']=2
    revised_result=consistency_receive(revised,consistency_produce(revised,rw))
    need(revised_result['status']=='shared-consistent-modelwise-sequential-equilibrium','revised belief alternative')
    # Independent symbolic necessity: solve the two exact Bayes equations, not
    # enumerate the receiver's allowed power witnesses.
    import sympy as sp
    x,y=sp.symbols('x y')
    equations=[sp.Rational(5,8)*x-sp.Rational(3,8)*y,
               sp.Rational(3,8)*x-sp.Rational(5,8)*y]
    need(sp.linsolve(equations,(x,y))==sp.FiniteSet((0,0)),'odds equations not independent')
    # This rank check corroborates the limit-ratio proof; it alone would not
    # justify passing from approximate equations to impossibility of sequences.
    # First boundary: equal immediate choices discard later monitoring incentives.
    gain_high=F(3,2)-F(1)*2;gain_low=F(3,2)-F(1,2)*2
    need((gain_high,gain_low)==(F(-1,2),F(1,2)),'monitoring control')
    # Chance reveal after an initial Continue: remembering a fair diagnostic bit
    # allows the later correct bit choice always; every signal-blind mixture wins half.
    later={'remembered_correct_probability':'1','erased_correct_probability':'1/2',
           'comply_to_defect_gain_high_monitor':str(gain_high),'comply_to_defect_gain_low_monitor':str(gain_low)}
    a=sp.Symbol('a')
    need(sp.simplify(sp.Rational(1,2)*a+sp.Rational(1,2)*(1-a))==sp.Rational(1,2),'all signal-blind mixtures control')
    with tempfile.TemporaryDirectory() as folder:
        root=Path(folder)
        for path in ['diagnostic_erasure/receive_case.py','sequential_consistency/consistency_receiver.py',
                     'sequential_consistency/witness.py','sequential_credibility/receiver.py','sequential_credibility/subject.py']:
            dest=root/'verification'/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/'verification'/path,dest)
        (root/'case.json').write_text(json.dumps(c));(root/'identity.json').write_text(json.dumps(expected))
        output=subprocess.check_output([sys.executable,str(root/'verification/diagnostic_erasure/receive_case.py'),str(root/'case.json'),str(root/'identity.json')],text=True)
        need(json.loads(output)==answer,'producer-disabled disagreement')
        need(not list(root.rglob('*producer*')) and not list(root.rglob('candidate.py')),'producer present')
    return {'received':answer,'rejections':rejections,'producer_disabled':True,
            'changed_belief_alternative':revised_result,'independent_exact_linear_solution':'x=y=0','later_incentive_controls':later}

if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
