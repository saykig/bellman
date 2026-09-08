# Bellman finite causal identification and decision certification

**Status:** additive bounded construction, 8 September 2026. This companion does not revise any
earlier mathematical edition, result record, or experiment. Its exact reference is under
[`verification/finite_causal_identification/`](../verification/finite_causal_identification/README.md).

## 1. Question and boundary

The object is a one-stage finite causal decision. The observation law, population or regime,
variable coding, causal premises, intervention query, and loss table are all part of the subject.
Bellman checks what follows mathematically from those supplied objects. It does not discover a
graph, infer an adjustment set from a field name, validate exchangeability in the world, or turn
observational association into intervention.

Two independent routes are supported:

1. exact adjustment for binary action (A), binary outcome (Y), and one supplied pre-action
   covariate (Z) with at most four categories;
2. exact response-type compatibility and partial identification for binary (A,Y), with no
   covariate, over the eight types (	au=(A_{\rm nat},Y_0,Y_1)).

The result is conditional causal mathematics. It supplies no graph discovery, empirical validity,
measurement-error, interference, selection, transport, sequential-treatment, safety, or authority
warrant. In particular, this companion does not compose causal outputs into a sequential policy
tree.

## 2. Route A: finite adjustment

### 2.1 Exact subject

Let (A,Y\in\{0,1\}), let (Z) range over a finite set with at most four named categories, and
let (P(A,Y,Z)) be a normalized exact rational observational law for an identified population or
regime. The subject separately identifies:

- the action, outcome, and covariate variables and their binary/category coding;
- the observational law and population;
- the adjustment set, initially exactly (Z);
- consistency and the meaning of (do(A=a));
- conditional exchangeability (Y(a)\perp A\mid Z);
- the premise that (Z) is pre-action;
- the requested intervention and query.

These are mathematical premises, not bare Boolean assertions. Matching their identities is not
evidence that they are true.

### 2.2 Adjustment theorem

**Theorem A (finite adjustment under supplied premises).** Suppose the preceding consistency,
exchangeability, and pre-action premises hold. For a requested (a\in\{0,1\}), also suppose

\[
P(A=a,Z=z)>0\qquad\text{whenever }P(Z=z)>0.
\tag{A1}
\]

Then, for (y\in\{0,1\}),

\[
P(Y=y\mid do(A=a))
=\sum_z P(Y=y\mid A=a,Z=z)P(Z=z).
\tag{A2}
\]

**Proof.** The law of total probability in the intervention regime gives

\[
P(Y(a)=y)=\sum_z P(Y(a)=y\mid Z=z)P(Z=z).
\]

Pre-action status keeps the distribution of (Z) fixed by the intervention. Conditional
exchangeability replaces each positive-support term by
(P(Y(a)=y\mid A=a,Z=z)). Consistency replaces that conditional counterfactual distribution by
the observed (P(Y=y\mid A=a,Z=z)). Condition (A1) makes every required conditional defined.
This proves (A2). Summing over (y) gives one, so the construction returns the complete binary
intervention distribution. (square)

The checker establishes only this implication. The observational bytes do not establish the
premises. A named (Z) column is not proof of valid adjustment.

### 2.3 Positivity boundary

If (P(Z=z)>0) but (P(A=a,Z=z)=0), the required conditional in (A2) is unavailable from the
supplied law. The exact status is `positivity-failure-for-adjustment`. This is neither an empty
causal model nor proof that an effect is zero or nonexistent. The bounded route refuses to borrow a
different stratum, average across groups, or extrapolate.

### 2.4 Confounding reversal

The fixed control has (P(Z=0)=P(Z=1)=1/2), treatment probabilities (9/10) and (1/10), and
bad-outcome probabilities

| (z) | (P(Y=1\mid A=0,z)) | (P(Y=1\mid A=1,z)) |
|---|---:|---:|
| 0 | (1/10) | (1/5) |
| 1 | (4/5) | (9/10) |

Direct observational conditioning gives

\[
P(Y=1\mid A=0)=73/100,
\qquad P(Y=1\mid A=1)=27/100.
\]

Thus a naive association-based bad-outcome decision selects action 1. Under the separately
supplied valid adjustment premises, (A2) gives

\[
P(Y=1\mid do(A=0))=9/20,
\qquad P(Y=1\mid do(A=1))=11/20,
\]

so the causal decision selects action 0. No numerical ambiguity is involved: the two queries have
different meanings.

## 3. Route B: exact response-type fibre

### 3.1 Subject and observational constraints

With no observed covariate in this first profile, enumerate

\[
\tau=(A_{\rm nat},Y_0,Y_1)\in\{0,1\}^3
\]

and assign exact masses (w_\tau\ge0), with (sum_\tau w_\tau=1). Observed consistency maps a
type to

\[
(A,Y)=
\begin{cases}
(0,Y_0),&A_{\rm nat}=0,\\
(1,Y_1),&A_{\rm nat}=1.
\end{cases}
\]

Hence each supplied cell (P(A=a,Y=y)) gives the exact equality

\[
\sum_\tau
\mathbf 1\{A_{\rm nat}=a,\;Y_a=y\}w_\tau=P(A=a,Y=y).
\tag{B1}
\]

The supported structural library is deliberately small. Monotone response (Y_1\ge Y_0) sets
the total mass of types with ((Y_0,Y_1)=(1,0)) to zero; monotone harm prevention (Y_1\le Y_0)
does the analogous thing for ((0,1)). A named exact linear equality may be supplied directly in
the documented eight-type order. Arbitrary prose is not a restriction.

For the supported restrictions, the exact causal fibre is

\[
\mathcal W=\{w\in\mathbb Q^8_{\ge0}: Ew=f\},
\tag{B2}
\]

where (Ew=f) contains normalization, (B1), and every declared supported equality. Its rational
points represent the exact executable profile; the corresponding real polytope is the theorem's
domain.

An independent-exogenous-noise factorization or other nonlinear restriction is not silently
dropped. Without an explicit relaxation request its status is `unsupported-causal-restriction`.
With such a request, dropping only the unsupported restriction produces a labeled outer
relaxation. An outer range is not evidence that the smaller exact original fibre is nonpoint.

### 3.2 Exact compatibility and extrema

**Theorem B (bounded complete vertex procedure).** For (B2), exact row reduction decides equality
inconsistency. If the equalities have rank (r), enumerate every (r)-element candidate support,
solve the corresponding square rational system, and retain precisely its nonnegative feasible
solutions. This list contains every vertex of (mathcal W). Because normalization makes
(mathcal W) bounded, it is nonempty if and only if the list contains a vertex. Every linear
query attains its minimum and maximum on that list.

**Proof.** Equality row reduction is exact. At any vertex, the equality rows together with active
nonnegativity constraints have rank eight. Therefore at most (r) coordinates can be positive,
and the point occurs in at least one enumerated basic support (degenerate zero basic variables are
allowed). Conversely, every retained point satisfies all equalities and nonnegativity. A nonempty
bounded polyhedron has a vertex, and a linear functional on a nonempty compact polytope attains an
extremum at a vertex. (square)

This specialized complete procedure is used instead of treating the existing generic joint-law
producer's unsuccessful bounded active-set search as an infeasibility result. It inherits the
existing exact rational and 256-bit input discipline. At eight variables there are at most
(\binom 8r\le70) candidate supports. Producer and receiver enumerate them through separately
implemented support/zero-set paths; the receiver checks the entire vertex set and every claimed
attaining witness.

The intervention bad-outcome probability is the linear query

\[
q_a(w)=P_w(Y=1\mid do(A=a))
=\sum_\tau\mathbf 1\{Y_a=1\}w_\tau.
\tag{B3}
\]

If (mathcal W=\varnothing), the status is `incompatible-causal-fiber`. If both extrema of a
query agree, it is point identified in the supplied exact fibre; otherwise it is partially
identified and the two exact attaining witnesses establish genuine variation.

### 3.3 Fixed response-type controls

For the symmetric observational law (P(A=a,Y=y)=1/4) in every cell, the unrestricted exact fibre
has 16 vertices. Direct enumeration by choosing the one unobserved potential outcome in each
observed cell agrees with the receiver's vertex list. Both intervention marginals have exact
attained range

\[
q_0(\mathcal W)=q_1(\mathcal W)=[1/4,3/4].
\tag{B4}
\]

Distinct retained vertices attain each end. Thus this is exact partial identification, not a
claim inferred from an outer set. Adding the supported equalities (q_0=1/2) and (q_1=1/2)
gives a nonempty fibre in which both displayed queries are point identified. Adding instead the
supported equality that the observed (A=0,Y=1) type mass is zero contradicts its observational
mass (1/4); exact row reduction returns `incompatible-causal-fiber`.

## 4. One-stage decisions

For exact costs (c(a)) and outcome losses (L(a,y)), define on one and the same causal law

\[
r_a(w)=c(a)+\sum_y L(a,y)P_w(Y=y\mid do(A=a)).
\tag{D1}
\]

An adjustment result makes (D1) a direct exact sum. The checker returns both risks and the complete
minimizing set. On a response-type fibre, every (r_a) is linear, so its descriptive range is
attained at vertices.

Descriptive marginal ranges are not the action certificate. For distinct actions (a,b), define

\[
D_{ab}=\max_{w\in\mathcal W}[r_a(w)-r_b(w)].
\tag{D2}
\]

**Theorem C (decision-relative identification).** Action (a) minimizes risk at every
(w\in\mathcal W) if and only if (D_{ab}\le0) for every competitor (b). It is strictly better
than every competitor throughout the fibre if every inequality is strict. The complete common
minimizing set consists exactly of the actions satisfying all non-strict inequalities.

**Proof.** For fixed (w), (a) is a minimizer exactly when
(r_a(w)-r_b(w)\le0) for every (b). Requiring this for all (w) is equivalent to the maxima in
(D2) being nonpositive. The strict statement is identical with strict inequalities; finite vertex
enumeration attains every maximum. (square)

Every subtraction in (D2) uses the same (w). The expression
(max_w r_a(w)-\min_v r_b(v)) generally splices two causal models and is not (D2). The reference
API rejects a two-witness subtraction unless both supplied witnesses are exactly identical.

### 4.1 Decision identified despite causal uncertainty

Use the nonpoint fibre (B4), bad-outcome loss (L(a,y)=y), and costs (c(0)=0,c(1)=1). Then

\[
r_0(\mathcal W)=[1/4,3/4],\qquad
r_1(\mathcal W)=[5/4,7/4].
\]

The exact paired maximum is (D_{01}=-1/2<0). Action 0 is strictly optimal throughout the exact
fibre even though both intervention probabilities have nonzero ranges. The status is
`decision-identified-despite-causal-uncertainty`.

### 4.2 Model-dependent decision

Remove the action cost and retain bad-outcome loss. The same exact fibre contains one retained
witness with (q_0<q_1), which prefers action 0, and another with (q_1<q_0), which prefers action
1. Exact paired maxima are

\[
D_{01}=D_{10}=1/2.
\]

No action is a common minimizer. The status is `model-dependent-over-causal-fiber`, with the two
opposite-preference witnesses retained. The implementation does not force consensus.

## 5. Certificate and receiver contract

Adjustment evidence binds the full observation law, population, coding, adjustment/premise
identities, intervention, query, exact stratum terms, distribution, and support status. The
receiver independently reconstructs marginals, conditionals, positivity, (A2), risks, and
minimizers.

Response-type evidence binds the observation law, population, coding, profile, ordered typed
restrictions, outer-relaxation request, and query. It contains the complete proposed vertex list,
exact bounds, and attaining witnesses. The receiver rebuilds (B1)–(B2), enumerates all vertices by
its own zero-set loop, and recomputes every optimum. Decision evidence additionally binds the
cost/loss identity and decision query, and the receiver recomputes risk ranges, paired differences,
common minimizers, strictness, and opposite witnesses. Candidate producers can be disabled while
all receiver paths continue to work.

Any changed observational probability, population, causal premise, adjustment-set identity,
variable coding, response-type profile, restriction, intervention query, cost, loss, or decision
query is a new mathematical subject. Old evidence rejects instead of being reinterpreted.

The statuses remain distinct:

- `identified-under-supplied-adjustment-premise` — exact adjustment consequence conditional on
  the supplied causal premises;
- `positivity-failure-for-adjustment` — a required observed conditional is unavailable;
- `point-identified-response-fiber` and `partially-identified` — nonempty exact response fibres
  with zero or nonzero query ranges;
- `decision-identified-despite-causal-uncertainty` — a common action exists in a nonpoint fibre;
- `model-dependent-over-causal-fiber` — retained exact models prefer opposite actions;
- `incompatible-causal-fiber` — no response-type mass vector satisfies the supported exact rows;
- `unsupported-causal-restriction` — an original restriction has no exact implementation;
- `outer-relaxation-only` — only an explicitly requested superset was analyzed.

## 6. Limits, composition, and next bridge

The executable limits are binary (A,Y); one (Z) with at most four categories for adjustment;
exactly eight response types for Route B; at most six typed structural restrictions; exact rational
input coefficients of at most 256 bits; and two deterministic one-stage actions. Signed exact
costs and losses are allowed. No floating result is mathematical authority.

The complete largest vertex loop is at most 70 square systems, so neither a solver nor language
trigger was reached. Larger causal polytopes, inequality-rich assumptions, nonlinear exact fibres,
continuous variables, or adjustment search should use an established optimization or causal
identification route instead of enlarging bespoke enumeration indefinitely.

The outputs are typed enough to state a future interface from an identified intervention kernel or
an exact causal fibre to a transition subject. They are not yet enough to justify that composition:
transport between populations, time-varying interventions, sequential exchangeability, support
under adaptive policies, and cross-time counterfactual compatibility remain undeveloped. The next
causal-to-sequential bridge is therefore a candidate, not earned implementation authority; its
first task must make those temporal/transport premises explicit rather than inserting the present
one-stage marginals into a policy tree.

Analytical proofs plus fixed exact checks are not formal verification. A checked conditional
consequence is not empirical proof and does not authorize action.
