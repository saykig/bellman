"""Bounded exact causal identification and one-stage decision certificates.

Route A checks finite covariate adjustment under explicitly supplied causal
premises.  Route B constructs the exact eight-response-type equality fibre.
Candidate construction and authoritative receiving are separate; no causal
premise is learned or empirically validated here.
"""
from dataclasses import asdict, dataclass
from fractions import Fraction as F
from itertools import combinations, product
import re


class Invalid(ValueError):
    pass


ADJUSTED = "identified-under-supplied-adjustment-premise"
POSITIVITY_FAILURE = "positivity-failure-for-adjustment"
PARTIAL = "partially-identified"
POINT = "point-identified-response-fiber"
DECISION_IDENTIFIED = "decision-identified"
DECISION_DESPITE_UNCERTAINTY = (
    "decision-identified-despite-causal-uncertainty")
MODEL_DEPENDENT = "model-dependent-over-causal-fiber"
INCOMPATIBLE = "incompatible-causal-fiber"
UNSUPPORTED = "unsupported-causal-restriction"
OUTER_ONLY = "outer-relaxation-only"

RESPONSE_TYPES = tuple(product((0, 1), repeat=3))
SUPPLIED_BOUNDARY = (
    "observational law and causal assumptions supplied; mathematical consequence "
    "checked conditionally; no graph discovery, empirical premise validation, "
    "measurement/interference/selection/transport warrant, or authority to act")


def need(condition, message):
    if not condition:
        raise Invalid(message)


def identity(value, message="nonempty identity required"):
    need(type(value) is str and bool(value), message)
    return value


def rational(value, message="exact rational required"):
    need(type(value) in (int, str, F) and type(value) is not bool, message)
    if type(value) is str:
        need(re.fullmatch(r"-?[0-9]+(?:/[1-9][0-9]*)?", value) is not None,
             "integer or fraction spelling required")
    try:
        answer = F(value)
    except (ValueError, ZeroDivisionError) as error:
        raise Invalid(message) from error
    need(max(abs(answer.numerator).bit_length(),
             answer.denominator.bit_length()) <= 256,
         "input rational exceeds 256-bit profile")
    return answer


def exact(value, message="exact Fraction required"):
    need(type(value) is F, message)
    return value


def probability(value, message="probability must be an exact Fraction in [0,1]"):
    exact(value, message)
    need(0 <= value <= 1, message)
    return value


def _input_vector(values, length, message):
    need(type(values) in (tuple, list) and len(values) == length, message)
    return tuple(rational(value, message) for value in values)


def _exact_vector(values, length, message):
    need(type(values) in (tuple, list) and len(values) == length, message)
    need(all(type(value) is F for value in values), message)
    return tuple(values)


def dot(left, right):
    need(len(left) == len(right), "vector dimension mismatch")
    return sum((a * b for a, b in zip(left, right)), F(0))


@dataclass(frozen=True)
class BinaryCoding:
    action_identity: str
    outcome_identity: str
    action_values: tuple = ("0", "1")
    outcome_values: tuple = ("0", "1")

    def __post_init__(self):
        identity(self.action_identity, "action variable identity required")
        identity(self.outcome_identity, "outcome variable identity required")
        for name in ("action_values", "outcome_values"):
            values = tuple(getattr(self, name))
            need(len(values) == 2 and len(set(values)) == 2 and
                 all(type(value) is str and value for value in values),
                 "two distinct nonempty binary value labels required")
            object.__setattr__(self, name, values)


@dataclass(frozen=True)
class AdjustmentObservation:
    identity: str
    population_identity: str
    coding: BinaryCoding
    covariate_identity: str
    covariate_values: tuple
    # Order: z major, then a in (0,1), then y in (0,1).
    masses: tuple

    def __post_init__(self):
        identity(self.identity, "observational-law identity required")
        identity(self.population_identity, "population/regime identity required")
        need(type(self.coding) is BinaryCoding, "binary coding required")
        identity(self.covariate_identity, "covariate identity required")
        values = tuple(self.covariate_values)
        need(1 <= len(values) <= 4 and len(set(values)) == len(values) and
             all(type(value) is str and value for value in values),
             "one to four distinct covariate labels required")
        object.__setattr__(self, "covariate_values", values)
        masses = _input_vector(self.masses, 4 * len(values),
                               "complete rational P(A,Y,Z) required")
        need(all(0 <= value <= 1 for value in masses),
             "observational masses must lie in [0,1]")
        need(sum(masses, F(0)) == 1,
             "observational P(A,Y,Z) must normalize exactly")
        object.__setattr__(self, "masses", masses)

    def mass(self, z_index, action, outcome):
        return self.masses[4 * z_index + 2 * action + outcome]


@dataclass(frozen=True)
class AdjustmentPremises:
    identity: str
    adjustment_set_identity: str
    adjustment_variables: tuple
    consistency_identity: str
    exchangeability_identity: str
    pre_action_identity: str
    intervention_identity: str

    def __post_init__(self):
        for value in (self.identity, self.adjustment_set_identity,
                      self.consistency_identity, self.exchangeability_identity,
                      self.pre_action_identity, self.intervention_identity):
            identity(value, "explicit causal-premise identities required")
        values = tuple(self.adjustment_variables)
        need(len(values) == 1 and all(type(value) is str and value for value in values),
             "first profile requires exactly one identified adjustment variable")
        object.__setattr__(self, "adjustment_variables", values)


@dataclass(frozen=True)
class AdjustmentRequest:
    observation: AdjustmentObservation
    premises: AdjustmentPremises
    intervention: int
    query_identity: str

    def __post_init__(self):
        need(type(self.observation) is AdjustmentObservation and
             type(self.premises) is AdjustmentPremises,
             "adjustment observation and premises required")
        need(type(self.intervention) is int and type(self.intervention) is not bool and
             self.intervention in (0, 1), "binary intervention required")
        identity(self.query_identity, "intervention query identity required")
        need(self.premises.adjustment_variables ==
             (self.observation.covariate_identity,),
             "declared adjustment set must be exactly the observed pre-action Z")


@dataclass(frozen=True)
class AdjustmentEvidence:
    request: AdjustmentRequest
    status: str
    distribution: tuple = ()
    # (z label, P(z), P(Y=0|a,z), P(Y=1|a,z))
    stratum_terms: tuple = ()
    missing_strata: tuple = ()
    supplied_boundary: str = SUPPLIED_BOUNDARY

    def __post_init__(self):
        need(type(self.request) is AdjustmentRequest,
             "adjustment request binding required")
        object.__setattr__(self, "distribution", tuple(self.distribution))
        object.__setattr__(self, "stratum_terms",
                           tuple(tuple(row) for row in self.stratum_terms))
        object.__setattr__(self, "missing_strata", tuple(self.missing_strata))
        need(self.status in (ADJUSTED, POSITIVITY_FAILURE),
             "invalid adjustment status")
        need(self.supplied_boundary == SUPPLIED_BOUNDARY,
             "causal/empirical boundary changed")


def _producer_adjustment(request):
    missing, terms = [], []
    for z_index, z_label in enumerate(request.observation.covariate_values):
        pz = sum((request.observation.mass(z_index, a, y)
                  for a in (0, 1) for y in (0, 1)), F(0))
        support = sum((request.observation.mass(
            z_index, request.intervention, y) for y in (0, 1)), F(0))
        if pz > 0 and support == 0:
            missing.append(z_label)
        elif pz > 0:
            terms.append((z_label, pz,
                          request.observation.mass(
                              z_index, request.intervention, 0) / support,
                          request.observation.mass(
                              z_index, request.intervention, 1) / support))
    if missing:
        return tuple(missing), (), ()
    distribution = tuple(sum((row[1] * row[2 + y] for row in terms), F(0))
                         for y in (0, 1))
    return (), tuple(terms), distribution


def produce_adjustment(request):
    """Producer: propose an adjustment result or exact positivity boundary."""
    need(type(request) is AdjustmentRequest, "adjustment request required")
    missing, terms, distribution = _producer_adjustment(request)
    if missing:
        return AdjustmentEvidence(request, POSITIVITY_FAILURE,
                                  missing_strata=missing)
    return AdjustmentEvidence(request, ADJUSTED, distribution, terms)


def _receiver_adjustment(request):
    """Independent cell-wise recomputation used only by the receiver."""
    missing = []
    rows = []
    result = [F(0), F(0)]
    obs = request.observation
    for i, label in enumerate(obs.covariate_values):
        p_z = sum(obs.masses[4 * i:4 * i + 4], F(0))
        start = 4 * i + 2 * request.intervention
        p_az = obs.masses[start] + obs.masses[start + 1]
        if p_z != 0 and p_az == 0:
            missing.append(label)
            continue
        if p_z != 0:
            row = (label, p_z, obs.masses[start] / p_az,
                   obs.masses[start + 1] / p_az)
            rows.append(row)
            result[0] += row[1] * row[2]
            result[1] += row[1] * row[3]
    return tuple(missing), tuple(rows), tuple(result)


def consume_adjustment(expected, evidence):
    """Receiver: bind subject and independently check support and adjustment."""
    need(type(expected) is AdjustmentRequest and
         type(evidence) is AdjustmentEvidence,
         "adjustment request and evidence required")
    need(evidence.request == expected,
         "stale observation, population, coding, premise, adjustment set, or query")
    missing, terms, distribution = _receiver_adjustment(expected)
    status = POSITIVITY_FAILURE if missing else ADJUSTED
    need(evidence.status == status, "false adjustment status")
    need(evidence.missing_strata == missing, "false positivity support claim")
    if missing:
        need(not evidence.distribution and not evidence.stratum_terms,
             "positivity failure cannot carry an adjusted distribution")
        return {"status": status, "missing_strata": missing,
                "checked": "support only; causal effect not declared absent"}
    need(evidence.stratum_terms == terms and evidence.distribution == distribution,
         "adjustment arithmetic mismatch")
    need(len(distribution) == 2 and sum(distribution, F(0)) == 1 and
         all(probability(value) == value for value in distribution),
         "invalid intervention distribution")
    return {"status": status, "distribution": distribution,
            "checked": "finite adjustment implication under supplied premises",
            "supplied_boundary": SUPPLIED_BOUNDARY}


def observational_distribution(observation, action):
    """Descriptive P(Y|A); deliberately not an intervention operation."""
    need(type(observation) is AdjustmentObservation, "observation required")
    need(type(action) is int and type(action) is not bool and action in (0, 1),
         "binary action required")
    cells = [sum((observation.mass(z, action, y)
                  for z in range(len(observation.covariate_values))), F(0))
             for y in (0, 1)]
    total = sum(cells, F(0))
    need(total > 0, "observational conditional lacks action support")
    return tuple(value / total for value in cells)


@dataclass(frozen=True)
class DecisionTable:
    identity: str
    unit: str
    costs: tuple
    losses: tuple

    def __post_init__(self):
        identity(self.identity, "decision-table identity required")
        identity(self.unit, "loss unit required")
        object.__setattr__(self, "costs", _input_vector(
            self.costs, 2, "two exact action costs required"))
        need(type(self.losses) in (tuple, list) and len(self.losses) == 2,
             "two action loss rows required")
        object.__setattr__(self, "losses", tuple(
            _input_vector(row, 2, "two exact outcome losses per action required")
            for row in self.losses))


@dataclass(frozen=True)
class AdjustmentDecisionRequest:
    observation: AdjustmentObservation
    premises: AdjustmentPremises
    decision: DecisionTable
    query_identity: str

    def __post_init__(self):
        need(type(self.observation) is AdjustmentObservation and
             type(self.premises) is AdjustmentPremises and
             type(self.decision) is DecisionTable,
             "adjustment decision subject required")
        identity(self.query_identity, "decision query identity required")
        need(self.premises.adjustment_variables ==
             (self.observation.covariate_identity,),
             "declared adjustment set must be exactly the observed pre-action Z")


@dataclass(frozen=True)
class AdjustmentDecisionEvidence:
    request: AdjustmentDecisionRequest
    interventions: tuple
    risks: tuple
    minimizing_actions: tuple
    status: str = "decision-identified-under-supplied-adjustment-premise"

    def __post_init__(self):
        need(type(self.request) is AdjustmentDecisionRequest,
             "decision request binding required")
        object.__setattr__(self, "interventions", tuple(self.interventions))
        object.__setattr__(self, "risks", tuple(self.risks))
        object.__setattr__(self, "minimizing_actions",
                           tuple(self.minimizing_actions))
        need(self.status ==
             "decision-identified-under-supplied-adjustment-premise",
             "invalid adjustment-decision status")


def produce_adjustment_decision(request):
    need(type(request) is AdjustmentDecisionRequest,
         "adjustment decision request required")
    interventions = tuple(produce_adjustment(AdjustmentRequest(
        request.observation, request.premises, action,
        request.query_identity + f":do-{action}")) for action in (0, 1))
    need(all(item.status == ADJUSTED for item in interventions),
         "decision adjustment lacks positivity")
    risks = tuple(request.decision.costs[action] + dot(
        request.decision.losses[action], interventions[action].distribution)
                  for action in (0, 1))
    best = min(risks)
    return AdjustmentDecisionEvidence(
        request, interventions, risks,
        tuple(action for action, value in enumerate(risks) if value == best))


def consume_adjustment_decision(expected, evidence):
    need(type(expected) is AdjustmentDecisionRequest and
         type(evidence) is AdjustmentDecisionEvidence,
         "adjustment decision request and evidence required")
    need(evidence.request == expected,
         "stale observation, premise, coding, cost, loss, or decision query")
    need(evidence.status ==
         "decision-identified-under-supplied-adjustment-premise",
         "false adjustment-decision status")
    need(len(evidence.interventions) == 2,
         "both binary interventions required")
    distributions = []
    for action, item in enumerate(evidence.interventions):
        intended = AdjustmentRequest(expected.observation, expected.premises,
                                     action,
                                     expected.query_identity + f":do-{action}")
        result = consume_adjustment(intended, item)
        need(result["status"] == ADJUSTED, "decision lacks adjusted intervention")
        distributions.append(result["distribution"])
    risks = tuple(expected.decision.costs[action] + dot(
        expected.decision.losses[action], distributions[action])
                  for action in (0, 1))
    best = min(risks)
    minimizers = tuple(action for action, value in enumerate(risks)
                       if value == best)
    need(evidence.risks == risks and evidence.minimizing_actions == minimizers,
         "false adjusted decision claim")
    return {"status": evidence.status, "risks": risks,
            "complete_minimizing_set": minimizers,
            "supplied_boundary": SUPPLIED_BOUNDARY}


@dataclass(frozen=True)
class MonotonicityRestriction:
    identity: str
    direction: str

    def __post_init__(self):
        identity(self.identity, "restriction identity required")
        need(self.direction in ("nondecreasing", "nonincreasing"),
             "supported monotonicity direction required")


@dataclass(frozen=True)
class LinearEqualityRestriction:
    identity: str
    coefficients: tuple
    rhs: F

    def __post_init__(self):
        identity(self.identity, "restriction identity required")
        object.__setattr__(self, "coefficients", _input_vector(
            self.coefficients, 8, "eight exact response-type coefficients required"))
        object.__setattr__(self, "rhs", rational(
            self.rhs, "exact response-type equality rhs required"))


@dataclass(frozen=True)
class UnsupportedRestriction:
    identity: str
    kind: str

    def __post_init__(self):
        identity(self.identity, "restriction identity required")
        identity(self.kind, "unsupported restriction kind required")


SUPPORTED_RESTRICTIONS = (MonotonicityRestriction, LinearEqualityRestriction)
RESTRICTIONS = SUPPORTED_RESTRICTIONS + (UnsupportedRestriction,)


@dataclass(frozen=True)
class ResponseObservation:
    identity: str
    population_identity: str
    coding: BinaryCoding
    # Order: (A=0,Y=0),(0,1),(1,0),(1,1).
    masses: tuple

    def __post_init__(self):
        identity(self.identity, "observational-law identity required")
        identity(self.population_identity, "population/regime identity required")
        need(type(self.coding) is BinaryCoding, "binary coding required")
        masses = _input_vector(self.masses, 4,
                               "complete rational P(A,Y) required")
        need(all(0 <= value <= 1 for value in masses),
             "observational masses must lie in [0,1]")
        need(sum(masses, F(0)) == 1,
             "observational P(A,Y) must normalize exactly")
        object.__setattr__(self, "masses", masses)


@dataclass(frozen=True)
class ResponseFiberRequest:
    observation: ResponseObservation
    profile_identity: str
    restrictions: tuple
    query_identity: str
    outer_relaxation_requested: bool = False

    def __post_init__(self):
        need(type(self.observation) is ResponseObservation,
             "response observation required")
        identity(self.profile_identity, "response-type profile identity required")
        identity(self.query_identity, "causal query identity required")
        values = tuple(self.restrictions)
        need(len(values) <= 6 and all(type(value) in RESTRICTIONS for value in values),
             "at most six typed causal restrictions required")
        need(len({value.identity for value in values}) == len(values),
             "duplicate causal restriction identity")
        need(type(self.outer_relaxation_requested) is bool,
             "outer-relaxation request must be Boolean")
        object.__setattr__(self, "restrictions", values)


@dataclass(frozen=True)
class ExactBound:
    lower: F
    upper: F
    lower_witness: tuple
    upper_witness: tuple

    def __post_init__(self):
        exact(self.lower)
        exact(self.upper)
        need(self.lower <= self.upper, "reversed exact bound")
        object.__setattr__(self, "lower_witness", _exact_vector(
            self.lower_witness, 8, "exact lower response-type witness required"))
        object.__setattr__(self, "upper_witness", _exact_vector(
            self.upper_witness, 8, "exact upper response-type witness required"))


@dataclass(frozen=True)
class ResponseFiberEvidence:
    request: ResponseFiberRequest
    status: str
    analyzed_domain: str
    vertices: tuple = ()
    intervention_bounds: tuple = ()
    exact_fiber_status: str = "checked"
    supplied_boundary: str = SUPPLIED_BOUNDARY

    def __post_init__(self):
        need(type(self.request) is ResponseFiberRequest,
             "response-fiber request binding required")
        object.__setattr__(self, "vertices",
                           tuple(tuple(vertex) for vertex in self.vertices))
        object.__setattr__(self, "intervention_bounds",
                           tuple(self.intervention_bounds))
        need(self.status in (POINT, PARTIAL, INCOMPATIBLE, UNSUPPORTED,
                             OUTER_ONLY), "invalid response-fiber status")
        need(self.analyzed_domain in ("exact", "outer", "unsupported"),
             "invalid analyzed domain")
        need(self.supplied_boundary == SUPPLIED_BOUNDARY,
             "causal/empirical boundary changed")


def _constraint_system(request, *, drop_unsupported=False):
    rows = [(F(1),) * 8]
    rhs = [F(1)]
    for action, outcome in product((0, 1), repeat=2):
        rows.append(tuple(F(a_nat == action and
                            (y0 if a_nat == 0 else y1) == outcome)
                          for a_nat, y0, y1 in RESPONSE_TYPES))
        rhs.append(request.observation.masses[2 * action + outcome])
    unsupported = []
    for restriction in request.restrictions:
        if type(restriction) is UnsupportedRestriction:
            unsupported.append(restriction)
            if not drop_unsupported:
                continue
        elif type(restriction) is MonotonicityRestriction:
            if restriction.direction == "nondecreasing":
                rows.append(tuple(F(y0 == 1 and y1 == 0)
                                  for _, y0, y1 in RESPONSE_TYPES))
            else:
                rows.append(tuple(F(y0 == 0 and y1 == 1)
                                  for _, y0, y1 in RESPONSE_TYPES))
            rhs.append(F(0))
        elif type(restriction) is LinearEqualityRestriction:
            rows.append(restriction.coefficients)
            rhs.append(restriction.rhs)
    return tuple(rows), tuple(rhs), tuple(unsupported)


def _rref(rows, rhs):
    matrix = [list(row) + [value] for row, value in zip(rows, rhs)]
    pivot_row = 0
    for column in range(8):
        hit = next((i for i in range(pivot_row, len(matrix))
                    if matrix[i][column] != 0), None)
        if hit is None:
            continue
        matrix[pivot_row], matrix[hit] = matrix[hit], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for i in range(len(matrix)):
            if i == pivot_row:
                continue
            scale = matrix[i][column]
            if scale:
                matrix[i] = [value - scale * pivot
                             for value, pivot in
                             zip(matrix[i], matrix[pivot_row])]
        pivot_row += 1
    inconsistent = any(all(value == 0 for value in row[:8]) and row[8] != 0
                       for row in matrix)
    reduced = tuple(tuple(row[:8]) for row in matrix
                    if any(value != 0 for value in row[:8]))
    reduced_rhs = tuple(row[8] for row in matrix
                        if any(value != 0 for value in row[:8]))
    return reduced, reduced_rhs, inconsistent


def _solve_square(rows, rhs):
    n = len(rows)
    matrix = [list(row) + [value] for row, value in zip(rows, rhs)]
    for column in range(n):
        hit = next((i for i in range(column, n)
                    if matrix[i][column] != 0), None)
        if hit is None:
            return None
        matrix[column], matrix[hit] = matrix[hit], matrix[column]
        scale = matrix[column][column]
        matrix[column] = [value / scale for value in matrix[column]]
        for i in range(n):
            if i != column and matrix[i][column]:
                scale = matrix[i][column]
                matrix[i] = [value - scale * pivot for value, pivot in
                             zip(matrix[i], matrix[column])]
    return tuple(matrix[i][-1] for i in range(n))


def _member(rows, rhs, point):
    return (len(point) == 8 and all(type(value) is F and value >= 0
                                    for value in point) and
            all(dot(row, point) == value for row, value in zip(rows, rhs)))


def _producer_vertices(rows, rhs):
    """Candidate complete basic-feasible-point enumeration."""
    reduced, values, inconsistent = _rref(rows, rhs)
    if inconsistent:
        return ()
    rank = len(reduced)
    answer = set()
    for live in combinations(range(8), rank):
        solved = _solve_square(tuple(tuple(row[j] for j in live)
                                     for row in reduced), values)
        if solved is None:
            continue
        point = [F(0)] * 8
        for j, value in zip(live, solved):
            point[j] = value
        point = tuple(point)
        if _member(rows, rhs, point):
            answer.add(point)
    return tuple(sorted(answer))


def _receiver_vertices(rows, rhs):
    """Authoritative independent zero-set enumeration of every vertex."""
    reduced, values, inconsistent = _rref(rows, rhs)
    if inconsistent:
        return ()
    rank = len(reduced)
    answer = set()
    for zero in combinations(range(8), 8 - rank):
        zero = set(zero)
        live = tuple(index for index in range(8) if index not in zero)
        coefficient_matrix = tuple(tuple(row[index] for index in live)
                                   for row in reduced)
        solved = _solve_square(coefficient_matrix, values)
        if solved is None:
            continue
        point = tuple(F(0) if index in zero else solved[live.index(index)]
                      for index in range(8))
        if _member(rows, rhs, point):
            answer.add(point)
    return tuple(sorted(answer))


def _bounds(vertices, coefficients):
    values = tuple(dot(coefficients, vertex) for vertex in vertices)
    lower, upper = min(values), max(values)
    return ExactBound(lower, upper, vertices[values.index(lower)],
                      vertices[values.index(upper)])


def intervention_coefficients(action):
    need(type(action) is int and type(action) is not bool and action in (0, 1),
         "binary intervention required")
    return tuple(F((y0 if action == 0 else y1) == 1)
                 for _, y0, y1 in RESPONSE_TYPES)


def produce_response_fiber(request):
    """Producer: enumerate exact/outer vertices and propose exact extrema."""
    need(type(request) is ResponseFiberRequest, "response-fiber request required")
    _, _, unsupported = _constraint_system(request)
    if unsupported and not request.outer_relaxation_requested:
        return ResponseFiberEvidence(request, UNSUPPORTED, "unsupported",
                                     exact_fiber_status=UNSUPPORTED)
    rows, rhs, _ = _constraint_system(request, drop_unsupported=True)
    vertices = _producer_vertices(rows, rhs)
    domain = "outer" if unsupported else "exact"
    if not vertices:
        return ResponseFiberEvidence(request, INCOMPATIBLE, domain,
                                     exact_fiber_status=INCOMPATIBLE)
    bounds = tuple(_bounds(vertices, intervention_coefficients(action))
                   for action in (0, 1))
    if unsupported:
        return ResponseFiberEvidence(request, OUTER_ONLY, domain, vertices,
                                     bounds, UNSUPPORTED)
    status = POINT if all(item.lower == item.upper for item in bounds) else PARTIAL
    return ResponseFiberEvidence(request, status, domain, vertices, bounds,
                                 status)


def consume_response_fiber(expected, evidence):
    """Receiver: rebuild the exact constraints and exhaust every bounded vertex."""
    need(type(expected) is ResponseFiberRequest and
         type(evidence) is ResponseFiberEvidence,
         "response-fiber request and evidence required")
    need(evidence.request == expected,
         "stale observation, population, coding, restriction, profile, or query")
    _, _, unsupported = _constraint_system(expected)
    if unsupported and not expected.outer_relaxation_requested:
        need(evidence.status == evidence.exact_fiber_status == UNSUPPORTED and
             evidence.analyzed_domain == "unsupported" and not evidence.vertices and
             not evidence.intervention_bounds,
             "unsupported restriction was silently relaxed")
        return {"status": UNSUPPORTED,
                "unsupported_restrictions": tuple(item.identity for item in unsupported)}
    rows, rhs, _ = _constraint_system(expected, drop_unsupported=True)
    vertices = _receiver_vertices(rows, rhs)
    need(evidence.vertices == vertices, "incomplete or false response-fiber vertices")
    if not vertices:
        expected_domain = "outer" if unsupported else "exact"
        need(evidence.status == evidence.exact_fiber_status ==
             INCOMPATIBLE and evidence.analyzed_domain == expected_domain and
             not evidence.intervention_bounds,
             "false incompatible-fiber classification")
        return {"status": INCOMPATIBLE, "vertices": (),
                "analyzed_domain": expected_domain,
                "warrant": ("empty checked outer relaxation" if unsupported else
                            "empty exact supported fiber")}
    bounds = tuple(_bounds(vertices, intervention_coefficients(action))
                   for action in (0, 1))
    need(evidence.intervention_bounds == bounds,
         "false response-type intervention extrema")
    if unsupported:
        need(evidence.status == OUTER_ONLY and evidence.analyzed_domain == "outer" and
             evidence.exact_fiber_status == UNSUPPORTED,
             "outer relaxation mislabeled as exact causal fiber")
        return {"status": OUTER_ONLY, "analyzed_domain": "outer",
                "exact_fiber_status": UNSUPPORTED,
                "intervention_bounds": bounds, "vertices": vertices}
    status = POINT if all(item.lower == item.upper for item in bounds) else PARTIAL
    need(evidence.status == evidence.exact_fiber_status == status and
         evidence.analyzed_domain == "exact", "false point/partial status")
    return {"status": status, "analyzed_domain": "exact",
            "intervention_bounds": bounds, "vertices": vertices,
            "supplied_boundary": SUPPLIED_BOUNDARY}


def risk_coefficients(decision, action):
    need(type(decision) is DecisionTable, "decision table required")
    need(type(action) is int and type(action) is not bool and action in (0, 1),
         "binary action required")
    return tuple(decision.costs[action] + decision.losses[action][
        y0 if action == 0 else y1] for _, y0, y1 in RESPONSE_TYPES)


@dataclass(frozen=True)
class ResponseDecisionRequest:
    fiber: ResponseFiberRequest
    decision: DecisionTable
    query_identity: str

    def __post_init__(self):
        need(type(self.fiber) is ResponseFiberRequest and
             type(self.decision) is DecisionTable,
             "response-fiber decision subject required")
        identity(self.query_identity, "decision query identity required")


@dataclass(frozen=True)
class DifferenceMaximum:
    candidate: int
    competitor: int
    maximum: F
    witness: tuple

    def __post_init__(self):
        need((self.candidate, self.competitor) in ((0, 1), (1, 0)),
             "ordered distinct binary action pair required")
        exact(self.maximum)
        object.__setattr__(self, "witness", _exact_vector(
            self.witness, 8, "exact paired-difference witness required"))


@dataclass(frozen=True)
class ResponseDecisionEvidence:
    request: ResponseDecisionRequest
    fiber_evidence: ResponseFiberEvidence
    status: str
    risk_bounds: tuple = ()
    paired_differences: tuple = ()
    common_minimizing_actions: tuple = ()
    strictly_common_actions: tuple = ()
    opposite_preference_witnesses: tuple = ()

    def __post_init__(self):
        need(type(self.request) is ResponseDecisionRequest and
             type(self.fiber_evidence) is ResponseFiberEvidence,
             "response decision evidence binding required")
        for name in ("risk_bounds", "paired_differences",
                     "common_minimizing_actions", "strictly_common_actions",
                     "opposite_preference_witnesses"):
            object.__setattr__(self, name, tuple(getattr(self, name)))
        need(self.status in (DECISION_IDENTIFIED, DECISION_DESPITE_UNCERTAINTY,
                             MODEL_DEPENDENT, UNSUPPORTED, INCOMPATIBLE,
                             OUTER_ONLY), "invalid response-decision status")


def _decision_from_vertices(request, fiber_evidence, vertices):
    coefficients = tuple(risk_coefficients(request.decision, action)
                         for action in (0, 1))
    risk_bounds = tuple(_bounds(vertices, row) for row in coefficients)
    differences = []
    for candidate, competitor in ((0, 1), (1, 0)):
        row = tuple(a - b for a, b in
                    zip(coefficients[candidate], coefficients[competitor]))
        values = tuple(dot(row, vertex) for vertex in vertices)
        maximum = max(values)
        differences.append(DifferenceMaximum(
            candidate, competitor, maximum, vertices[values.index(maximum)]))
    common = tuple(item.candidate for item in differences if item.maximum <= 0)
    strict = tuple(item.candidate for item in differences if item.maximum < 0)
    opposite = ()
    if not common:
        witnesses = []
        for preferred in (0, 1):
            row = tuple(a - b for a, b in
                        zip(coefficients[preferred], coefficients[1 - preferred]))
            values = tuple(dot(row, vertex) for vertex in vertices)
            minimum = min(values)
            need(minimum < 0, "model-dependent status lacks opposite preference")
            witnesses.append((preferred, vertices[values.index(minimum)]))
        opposite = tuple(witnesses)
    if not common:
        status = MODEL_DEPENDENT
    elif fiber_evidence.status == PARTIAL:
        status = DECISION_DESPITE_UNCERTAINTY
    else:
        status = DECISION_IDENTIFIED
    return status, risk_bounds, tuple(differences), common, strict, opposite


def produce_response_decision(request):
    """Producer: propose exact same-fibre one-stage decision conclusions."""
    need(type(request) is ResponseDecisionRequest,
         "response decision request required")
    fiber = produce_response_fiber(request.fiber)
    if fiber.status in (UNSUPPORTED, INCOMPATIBLE, OUTER_ONLY):
        return ResponseDecisionEvidence(request, fiber, fiber.status)
    values = _decision_from_vertices(request, fiber, fiber.vertices)
    return ResponseDecisionEvidence(request, fiber, *values)


def consume_response_decision(expected, evidence):
    need(type(expected) is ResponseDecisionRequest and
         type(evidence) is ResponseDecisionEvidence,
         "response decision request and evidence required")
    need(evidence.request == expected,
         "stale observation, coding, restriction, cost, loss, or decision query")
    fiber_result = consume_response_fiber(expected.fiber,
                                          evidence.fiber_evidence)
    if fiber_result["status"] in (UNSUPPORTED, INCOMPATIBLE, OUTER_ONLY):
        need(evidence.status == fiber_result["status"] and not evidence.risk_bounds and
             not evidence.paired_differences and
             not evidence.common_minimizing_actions,
             "unsupported/incompatible/outer fiber cannot earn an exact decision")
        return {"status": evidence.status, "fiber": fiber_result}
    expected_values = _decision_from_vertices(
        expected, evidence.fiber_evidence, fiber_result["vertices"])
    observed_values = (
        evidence.status, evidence.risk_bounds, evidence.paired_differences,
        evidence.common_minimizing_actions, evidence.strictly_common_actions,
        evidence.opposite_preference_witnesses)
    need(observed_values == expected_values,
         "false same-fiber decision classification or extrema")
    return {"status": evidence.status,
            "risk_bounds": evidence.risk_bounds,
            "paired_differences": evidence.paired_differences,
            "complete_common_minimizing_set":
                evidence.common_minimizing_actions,
            "strictly_common_actions": evidence.strictly_common_actions,
            "opposite_preference_witnesses":
                evidence.opposite_preference_witnesses,
            "supplied_boundary": SUPPLIED_BOUNDARY}


def same_fiber_difference(request, candidate, competitor, witness):
    """Evaluate one action difference at one shared causal response-type law."""
    need(type(request) is ResponseDecisionRequest,
         "response decision request required")
    need((candidate, competitor) in ((0, 1), (1, 0)),
         "ordered distinct binary action pair required")
    rows, rhs, unsupported = _constraint_system(request.fiber)
    need(not unsupported, "exact supported causal fiber required")
    witness = _exact_vector(witness, 8, "one exact shared witness required")
    need(_member(rows, rhs, witness), "witness outside exact causal fiber")
    return dot(tuple(a - b for a, b in zip(
        risk_coefficients(request.decision, candidate),
        risk_coefficients(request.decision, competitor))), witness)


def cross_witness_difference(request, candidate, candidate_witness,
                             competitor, competitor_witness):
    """Reject the tempting invalid subtraction unless model identity is shared."""
    need(tuple(candidate_witness) == tuple(competitor_witness),
         "cross-witness subtraction is not a modelwise causal difference")
    return same_fiber_difference(request, candidate, competitor,
                                 tuple(candidate_witness))


def wire(value):
    if isinstance(value, F):
        return str(value.numerator) if value.denominator == 1 else str(value)
    if hasattr(value, "__dataclass_fields__"):
        return wire(asdict(value))
    if isinstance(value, dict):
        return {str(key): wire(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [wire(item) for item in value]
    return value
