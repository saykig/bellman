"""Standard-library primal/dual receiving for all observed catalogue states."""
from collections import defaultdict
from fractions import Fraction as F
import json
from pathlib import Path
import sys

from receiver import HERE, PAIRS, source_rows, residual_bounds, need, close, sigmoid


def simplex(values,n):
    need(len(values)==n,'simplex dimension')
    result=list(map(F,values)); need(min(result)>=0 and sum(result)==1,'invalid simplex witness')
    return result


def check_range(matrix,actions,claim):
    K=len(matrix[0]); C=[j for j,a in enumerate(actions) if a]; D=[j for j,a in enumerate(actions) if not a]
    limits={}; certificates=0
    for side,indices,opposites in [('max',C,D),('min',D,C)]:
        claims=claim[side+'_certificates']
        need([c['plan'] for c in claims]==indices,'missing or reordered LP alternatives')
        intervals=[]
        for item in claims:
            j=item['plan']; w=simplex(item['posterior'],K); dual=simplex(item['dual'],len(opposites))
            differences=[[matrix[j][k]-matrix[l][k] if side=='max' else matrix[l][k]-matrix[j][k] for k in range(K)] for l in opposites]
            primal=[sum(w[k]*d[k] for k in range(K)) for d in differences]
            duals=[sum(dual[l]*d[k] for l,d in enumerate(differences)) for k in range(K)]
            interval=(min(primal),max(duals)) if side=='max' else (min(duals),max(primal))
            need(interval[0]<=interval[1],'weak duality violated')
            need(interval==(F(item['lower']),F(item['upper'])),'false LP bound')
            intervals.append(interval); certificates+=1
        aggregate=(max(x[0] for x in intervals),max(x[1] for x in intervals)) if side=='max' else (min(x[0] for x in intervals),min(x[1] for x in intervals))
        field='maximum_enclosure' if side=='max' else 'minimum_enclosure'
        need(tuple(map(F,claim[field]))==aggregate,'false global LP extrema')
        limits[side]=aggregate
    return limits,certificates


def verify(raw,results):
    source=source_rows(raw)
    parameters=json.loads((HERE/'first-results/parameters.json').read_text())['ten-linear']
    E=F(residual_bounds(parameters)['exact_value_error_bound']); need(E==F(results['exact_value_error_bound']),'residual identity mismatch')
    autos=parameters['mixture']['automata']; tables=parameters['values']; beta=parameters['response']['coefficients']
    states=results['states']; need([s['id'] for s in states]==list(range(len(states))),'state index mismatch')
    lookup={}; count=0; maxgap=F(0)
    for state in states:
        own=state['own_states']; other=state['opponent_states']; signature=(tuple(own),tuple(other))
        need(signature not in lookup,'duplicate catalogue state'); lookup[signature]=state
        need(len(own)==len(autos)==len(other),'state dimension')
        for k,auto in enumerate(autos):
            need(0<=own[k]<len(auto['outputs']) and 0<=other[k]<len(auto['outputs']),'state outside automaton')
        actions=[a['outputs'][own[j]] for j,a in enumerate(autos)]
        need(set(state['treatments'])=={'2','3','4'},'treatment coverage')
        for treatment,table in tables.items():
            matrix=[[F(str(table[j][k][own[j]][other[k]])) for k in range(len(autos))] for j in range(len(autos))]
            bounds,n=check_range(matrix,actions,state['treatments'][treatment]); count+=n
            maxgap=max(maxgap,*(z[1]-z[0] for z in bounds.values()))
    games=defaultdict(list)
    for row in source:
        if row['treatment'] in (3,4) and row['supergame']>=5 and row['round']<=8:
            games[tuple(row[k] for k in ('session','id','supergame'))].append(row)
    ranges=defaultdict(list); pure=defaultdict(lambda:defaultdict(list)); visited=set(); query_count=0
    for _,game in sorted(games.items()):
        own=[0]*len(autos); other=[0]*len(autos); past=[]
        for row in sorted(game,key=lambda r:r['round']):
            a,b=row['coop'],row['o_coop']; t=str(row['treatment'])
            if past:
                signature=(tuple(own),tuple(other)); need(signature in lookup,'uncovered observed history'); visited.add(signature)
                state=lookup[signature]; bound=state['treatments'][t]
                shift=beta[0]+beta[2]*past[-1][0]+beta[3]*past[-1][2]+beta[4]*(row['round']-2)/6
                low=F(bound['minimum_enclosure'][0])-2*E; high=F(bound['maximum_enclosure'][1])+2*E
                ranges[row['session']].append((sigmoid(shift+beta[1]*float(low)),sigmoid(shift+beta[1]*float(high))))
                # For each pure type, positive observation likelihood leaves the same pure posterior.
                for k,name in enumerate(parameters['mixture']['names']):
                    probabilities={}
                    for treatment in ('2',t):
                        table=tables[treatment]; byaction={0:[],1:[]}
                        for j,auto in enumerate(autos):
                            byaction[auto['outputs'][own[j]]].append(table[j][k][own[j]][other[k]])
                        probabilities[treatment]=sigmoid(shift+beta[1]*(max(byaction[1])-max(byaction[0])))
                    pure[name][row['session']].append((a,probabilities['2'],probabilities[t]))
                query_count+=1
            for k,auto in enumerate(autos):
                own[k]=auto['transitions'][own[k]][PAIRS.index((a,b))]
                other[k]=auto['transitions'][other[k]][PAIRS.index((b,a))]
            past.append((a,b,row['belief']))
    need(visited==set(lookup),'unobserved states included in query claim')
    need(query_count==results['target_queries'],'query count mismatch')
    for session,values in ranges.items():
        claimed=results['session_response_outer_ranges'][str(session)]
        need(len(values)==claimed['n'],'range session count')
        for k in (0,1): close(sum(v[k] for v in values)/len(values),claimed['mean_probability_outer'][k],'outer mean mismatch')
    for name,sessions in pure.items():
        claim=results['shared_pure_priors'][name]; deltas=[]
        for s in claim['sessions']:
            observations=sessions[s['session']]; n=len(observations); need(n==s['n'],'pure prior count')
            for index,model in [(1,'fixed'),(2,'updated')]:
                value=sum((r[index]-r[0])**2 for r in observations)/n
                close(value,s['models'][model]['brier'],'pure-prior score mismatch')
            delta=sum((r[2]-r[0])**2-(r[1]-r[0])**2 for r in observations)/n
            close(delta,s['delta_brier'],'pure-prior contrast mismatch'); deltas.append(delta)
        close(sum(deltas)/16,claim['comparison']['delta_brier'],'pure-prior aggregate mismatch')
    return {'observed_state_pairs':len(lookup),'queries_checked':query_count,'rational_lp_certificates':count,
        'largest_exact_extremum_enclosure_width':str(maxgap),'shared_pure_priors_checked':len(pure),
        'scope':'sharp extrema enclosed for each retained finite value query; residual enlargement covers exact reward values; aggregate intervals are outer for a shared prior; pure-prior contrast arithmetic checked, sampling intervals not certified'}


if __name__=='__main__':
    result=verify(sys.argv[1],json.loads(Path(sys.argv[2]).read_text()))
    print(json.dumps(result,indent=2))
