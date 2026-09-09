"""Additive source replication audit and explicit first-result decomposition."""
from collections import defaultdict
from fractions import Fraction as F
import json
from pathlib import Path
import sys
import numpy as np
from scipy.stats import t as student_t
from receiver import source_rows,HERE


def run(raw):
    source=source_rows(raw); rounds=defaultdict(list); sessions=defaultdict(list)
    for row in source:
        if row['late']==1 and row['round']<=8:
            rounds[row['treatment'],row['round']].append(row)
            sessions[row['treatment'],row['session']].append(row)
    pooled=[]
    for (t,r),rows in sorted(rounds.items()):
        coop=sum(F(x['coop']) for x in rows)/len(rows); belief=sum(F(str(x['belief'])) for x in rows)/len(rows)
        pooled.append({'treatment':t,'round':r,'n':len(rows),'cooperation':str(coop),'report':str(belief),'gap':str(belief-coop)})
    intervals={}
    for treatment in (1,2,3,4):
        means=[]
        for (t,s),rows in sorted(sessions.items()):
            if t==treatment: means.append({'session':s,'cooperation':sum(x['coop'] for x in rows)/len(rows),
                                          'report':sum(x['belief'] for x in rows)/len(rows)})
        summary={}
        for field in ('cooperation','report'):
            values=np.array([r[field] for r in means]); estimate=float(values.mean()); se=float(values.std(ddof=1)/len(values)**.5)
            radius=float(student_t.ppf(.975,len(values)-1)*se)
            summary[field]={'mean':estimate,'session_t_95':[estimate-radius,estimate+radius]}
        intervals[str(treatment)]={'sessions':means,'summary':summary}
    contrasts={}
    for treatment in (3,4):
        contrasts[str(treatment)]={}
        for field in ('cooperation','report'):
            a=np.array([x[field] for x in intervals[str(treatment)]['sessions']]); b=np.array([x[field] for x in intervals['2']['sessions']])
            va=a.var(ddof=1)/8; vb=b.var(ddof=1)/8; se=float((va+vb)**.5); dfree=float((va+vb)**2/(va*va/7+vb*vb/7))
            estimate=float(a.mean()-b.mean()); radius=float(student_t.ppf(.975,dfree)*se)
            contrasts[str(treatment)][field]={'target_minus_base':estimate,'welch_95':[estimate-radius,estimate+radius],'df':dfree}
    indexed={tuple(row[k] for k in ('session','id','supergame','round')):row for row in source}
    decomposition={}
    for label in ('ten-linear','six-linear','ten-reciprocal','ten-square'):
        predictions=json.loads((HERE/'first-results'/f'{label}-predictions.json').read_text()); terms=defaultdict(list)
        for p in predictions:
            row=indexed[tuple(p['key'])]; change=p['updated']-p['fixed']; y=row['coop']
            terms[row['session']].append((2*(p['fixed']-y)*change,change*change))
        decomposition[label]=[{'session':s,'linear_alignment':sum(t[0] for t in ts)/len(ts),
                               'squared_adjustment':sum(t[1] for t in ts)/len(ts)} for s,ts in sorted(terms.items())]
    return {'schema':'bellman.afy2024.replication-review.v1','pooled_rounds_exact':pooled,
        'late_first_eight_session_inference':intervals,'target_base_descriptive_contrasts':contrasts,'brier_decomposition':decomposition,
        'figure_reference_correction':'Frozen PLAN/SOURCES say Figure 11 for the descriptive comparison; it is Figure 9 in the hash-bound author paper. Figure 11 is a separate type/belief best-response analysis, not reproduced here.',
        'interval_scope':'our equal-session t intervals, not reproduction of the authors regression standard errors or p-values'}

if __name__=='__main__': print(json.dumps(run(sys.argv[1]),indent=2))
