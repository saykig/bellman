# Declared finite-catalogue calculation

9 September 2026; companion to PLAN.md, fixed before human-data fitting.

## Subject and query

The subject is a supplied finite catalogue of deterministic Moore automata, a population
mixture p, binary opponent flip probability q in (0,1), a within-game action prefix h,
stage utility u, and discount δ=7/8. A state emits C or D and transitions on the actual
(own,opponent) action pair. A player's automaton always receives its own action first.
All states start anew at each supergame. These are hypotheses about behavior, not an
assessment of sequential equilibrium or a measurement of a participant's preferences.

For each opponent type k, reconstruct its state along h, multiplying probabilities
of the observed opponent actions: 1-q for its prescribed action and q otherwise.
Write the product L_k(h)>0. The posterior is w_k=p_k L_k / sum_l p_l L_l.
This conditions on the subject's past actions as inputs, without assigning their
likelihood to an opponent type. It does not condition on the subject's current action
or report. Assuming an exogenous opponent type and this response model is substantive.

For each own continuation plan j and opponent type k, the joint finite state is (s,t).
The subject emits its prescribed action without flips; the opponent follows its
prescription with probability 1-q. Each realized pair determines the next two states,
with reversed input order for the opponent. The resulting stochastic matrix is P_jk.
Use r_g(a,b)=(u(payment_g(a,b))-u(39))/(u(51)-u(39)); the denominator is fixed across
treatments and positive for the three declared utilities. Expected stage reward forms r.
The normalized discounted value is

    V_jk = (1-δ) r + δ P_jk V_jk.

Because a stochastic matrix has infinity norm one, the Neumann series converges and
I-δP is invertible. Its unique solution equals the expected discounted reward, by
finite-horizon expansion and a remainder bounded by δ^n ||V||∞. This is the standard
finite Markov reward calculation, specialized here; it establishes no optimality
outside the catalogue. State reconstruction permits evaluating a plan after an actual
prefix that the plan itself would not have generated.

At h let v_jk be the value at the reconstructed joint state. Define C(h),D(h) by
current own-plan prescriptions, and

    d_g(h;w) = max_{j in C(h)} sum_k w_k v_jk - max_{l in D(h)} sum_k w_k v_lk.

AC and AD make both sets nonempty. The response is the sigmoid specified in PLAN.md.
The fixed and updated predictors have identical scores and fitted coefficients under
base payments, hence are observationally identical there for every history. This
identity alone does not identify their behavior in a changed treatment.

They can disagree: against a memoryless AC opponent with flip q<1/2, defection has
stage advantage D=(1-q)(T-R)+q(P-S)>0. AD attains the maximum value. Every plan
prescribing C now has positive normalized expected C occupancy m_j≥1-δ. Its loss
relative to AD is D m_j. Thus d=-D min_j m_j. Occupancies depend on automata and q,
not payments. High T increases D by 10(1-q) in raw linear utility; Low R increases it
by 6(1-q). After the fixed positive normalization, d strictly decreases. For b>0,
updated and fixed probabilities differ. For general history-dependent opponent types,
no universal direction follows from this argument. For b=0 the predictors coincide.

## Numerical receiving and exact scope

Use existing dense linear algebra to produce Vhat. Interpreting stored decimal values,
q and utility entries as rationals, calculate the exact residual

    ρ = ||Vhat - ((1-δ)r + δP Vhat)||∞.

Subtracting the fixed-point equation gives ||Vhat-V||∞≤ρ/(1-δ)=8ρ, since the
inverse has infinity norm at most 1/(1-δ). A convex mixture of values inherits the
maximum bound E; maximizing over a finite nonempty set preserves that bound. The
score error is at most 2E. The sigmoid derivative is at most 1/4, so with a fixed
coefficient b≥0 the resulting probability error is at most bE/2. This certificate
checks a specified rational model; it does not certify fitted parameters, global
mixture likelihood optimality, empirical preferences, sampling inference or unrestricted
best responses. Independent receiving must not invoke the fitting procedure.

## Prior sensitivity: finite LP, not vertex enumeration

Fix a history and numerical value vectors v_j. All posterior weights w in the simplex
are attainable from some prior: choose p_k proportional to w_k/L_k(h). Zero weights
are allowed in this sensitivity, although the primary operational prior is smoothed.
This is an enlarged hypothesis family, not an estimated confidence set.

The maximum score over the simplex is the maximum, over j in C, of the LP

    maximize z over w≥0, sum w=1,
    subject to z ≤ w·(v_j-v_l) for every l in D.

For fixed j, the optimized expression is w·v_j-max_l w·v_l. Taking max over j
and w commutes, proving the formula. The minimum score is the minimum, over l in D,
of the LP

    minimize z over w≥0, sum w=1,
    subject to z ≥ w·(v_j-v_l) for every j in C.

Here min over l and w commutes in max_j w·v_j-w·v_l. These formulas prove sharpness
for the supplied finite value vectors. Use SciPy/HiGHS rather than a new LP solver.
Floating optimality labels alone are numerical evidence, not exact rational certificates.
A simple always-valid outer range is [min_{j,k} v_jk-max_{l,k} v_lk,
max_{j,k} v_jk-min_{l,k} v_lk], with j in C and l in D. Report such a range as
outer if sharp extrema have not been certified. Residual errors enlarge numerical
score ranges by 2E before making a claim about exact Markov values.

History-wise extrema need not coexist under one common prior. For example, two queries
w and 1-w each range over [0,1], while their equal-weight average is always 1/2.
Combining their endpoints yields only an outer [0,1] interval. Consequently averaging
per-history response bounds does not solve shared-prior target transport. Neither this
obstruction nor a failed numerical fit proves a general psychological nonidentification
theorem. The final audit must distinguish the hypotheses rejected by observation from
those left compatible, and from larger families that were never tested.

## Reuse boundary

The query identity includes source edition, eligible times, histories, catalogue, noise,
prior, utility, discount, coefficients, metric and dependence unit. Changing any of these
requires recomputation or an explicitly justified transport. Current reports cannot be
relabelled pre-action beliefs. Session bootstrap intervals require their stated sampling
premises. No participation, commitment, sequential-equilibrium or causal welfare claim
is supplied by a prediction score. Lean or a language migration is not warranted for
these standard finite calculations; exact residual receiving supplies the relevant
additional assurance at substantially smaller scope.
