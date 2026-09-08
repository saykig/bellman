"""Exact saturated longitudinal causal-kernel fibres and bounded decisions.

The profile retains the binary two-stage variables from the preceding
longitudinal bridge.  Missing *second-stage outcome* rows are independent
Bernoulli coordinates only because the request explicitly supplies the
saturated, no-cross-row-restriction completion profile.  The continuous
fibre is not replaced by its corners: corners are exact only for the proved
multi-affine policy-risk, additive-loss, pairwise-difference, and derived
finite-policy decision queries.

Candidate construction and authoritative receiving use separate transition
and policy-evaluation paths.  Every retained ordinary sequential certificate
is checked without invoking its producer.
"""
from dataclasses import asdict, dataclass
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from verification.longitudinal_causal_policy import reference as longitudinal  # noqa: E402

# The historical persistent-family module imports the sequential reference by
# its original top-level name.  Bind that name to the already-loaded canonical
# module while importing it, avoiding a second set of incompatible dataclass
# identities when this file itself is imported as ``reference``.
_prior_reference_module = sys.modules.get("reference")
sys.modules["reference"] = longitudinal.sequential
try:
    from verification.persistent_model_families import families  # noqa: E402
finally:
    if _prior_reference_module is None:
        del sys.modules["reference"]
    else:
        sys.modules["reference"] = _prior_reference_module


sequential = longitudinal.sequential
Invalid = longitudinal.Invalid

SATURATED_PROFILE = "saturated-independent-missing-second-stage-binary-rows-v1"
QUERY_CLASS = "policy-risk-additive-loss-and-finite-deterministic-decisions"
EXACT_FIBRE = "exact-saturated-longitudinal-kernel-fibre"
OUTSIDE_PROFILE = "outside-second-stage-kernel-fibre-profile"
UNSUPPORTED_RESTRICTION = "unsupported-causal-completion-restriction"
UNSUPPORTED_QUERY = "unsupported-kernel-fibre-query"
POINT_POLICY = "point-identified-across-kernel-fibre"
PARTIAL_POLICY = "partially-identified-across-kernel-fibre"
DECISION_IDENTIFIED = "causal-decision-identified-across-every-completion"
DECISION_MODEL_DEPENDENT = "causal-decision-model-dependent-across-completions"
PERSISTENT_REUSED = "existing-persistent-family-receiver-reused"
PERSISTENT_LOCAL = "local-exact-corner-family-existing-persistent-limit"
MAX_MISSING_ROWS = 4
MAX_CORNERS = 16
POLICY_COUNT = 32

SUPPLIED_BOUNDARY = (
    "observational law, longitudinal causal premises, saturated completion "
    "profile, losses, and deterministic policy catalogue supplied; exact "
    "conditional consequences checked; no empirical premise validation, "
    "statistical confidence meaning, stronger SCM or cross-world warrant, "
    "randomized-policy claim, or authority to act"
)


need = longitudinal.need
identity = longitudinal.identity
exact = longitudinal.exact


@dataclass(frozen=True)
class CompletionProfile:
    identity: str
    kind: str = SATURATED_PROFILE
    cross_row_restrictions: tuple = ()

    def __post_init__(self):
        identity(self.identity, "completion-profile identity required")
        identity(self.kind, "completion-profile kind required")
        need(type(self.cross_row_restrictions) in (tuple, list),
             "cross-row restriction sequence required")
        restrictions = tuple(self.cross_row_restrictions)
        need(all(type(item) is str and item for item in restrictions),
             "named cross-row restrictions required")
        need(len(set(restrictions)) == len(restrictions),
             "duplicate cross-row restriction")
        object.__setattr__(self, "cross_row_restrictions", restrictions)


@dataclass(frozen=True)
class MissingRow:
    identity: str
    first_action: int
    intermediate: int
    second_action: int

    def __post_init__(self):
        identity(self.identity, "missing-row identity required")
        for value in (self.first_action, self.intermediate, self.second_action):
            need(type(value) is int and type(value) is not bool and value in (0, 1),
                 "binary missing-row coordinate required")

    @property
    def coordinate(self):
        return (self.first_action, self.intermediate, self.second_action)


def missing_row_identity(observation, a1, intermediate, a2):
    """Stable semantic identity for one absent conditional outcome row."""
    need(type(observation) is longitudinal.LongitudinalObservation,
         "observation required")
    c = observation.coding
    return (f"{observation.identity}:missing:{c.outcome.identity}|"
            f"{c.first_action.identity}={a1}|{c.intermediate.identity}={intermediate}|"
            f"{c.second_action.identity}={a2}")


def derive_missing_rows(observation):
    """Canonical support-derived row order: A1, L1, then A2."""
    need(type(observation) is longitudinal.LongitudinalObservation,
         "observation required")
    answer = []
    for a1, intermediate, a2 in product((0, 1), repeat=3):
        if longitudinal._marginal_a1_l1_a2(observation, a1, intermediate, a2) == 0:
            answer.append(MissingRow(
                missing_row_identity(observation, a1, intermediate, a2),
                a1, intermediate, a2))
    return tuple(answer)


@dataclass(frozen=True)
class FibreRequest:
    observation: longitudinal.LongitudinalObservation
    premises: longitudinal.SequentialCausalPremises
    loss: longitudinal.LongitudinalLoss
    deployment_population_identity: str
    completion_profile: CompletionProfile
    missing_rows: tuple
    policies: tuple
    subject_identity: str
    policy_catalogue_identity: str
    support_query_identity: str
    fibre_identity: str
    corner_family_identity: str
    query_identity: str
    query_class: str = QUERY_CLASS

    def __post_init__(self):
        need(type(self.observation) is longitudinal.LongitudinalObservation and
             type(self.premises) is longitudinal.SequentialCausalPremises and
             type(self.loss) is longitudinal.LongitudinalLoss and
             type(self.completion_profile) is CompletionProfile,
             "complete longitudinal kernel-fibre request required")
        for value in (self.deployment_population_identity, self.subject_identity,
                      self.policy_catalogue_identity, self.support_query_identity,
                      self.fibre_identity, self.corner_family_identity,
                      self.query_identity, self.query_class):
            identity(value, "explicit kernel-fibre identities required")
        need(self.deployment_population_identity ==
             self.observation.population_identity,
             "kernel-fibre profile does not supply population transport")
        need(type(self.missing_rows) in (tuple, list) and
             all(type(row) is MissingRow for row in self.missing_rows),
             "ordered explicit missing-row mapping required")
        rows = tuple(self.missing_rows)
        need(len(rows) <= MAX_MISSING_ROWS,
             "more than four missing rows are outside the bounded profile")
        need(len({row.identity for row in rows}) == len(rows) and
             len({row.coordinate for row in rows}) == len(rows),
             "duplicate missing-row identity or coordinate")
        object.__setattr__(self, "missing_rows", rows)
        need(type(self.policies) in (tuple, list) and
             all(type(policy) is longitudinal.DynamicPolicy
                 for policy in self.policies),
             "one common ordered deterministic policy catalogue required")
        policies = tuple(self.policies)
        need(len(policies) == POLICY_COUNT and
             len({policy.identity for policy in policies}) == POLICY_COUNT and
             policies == longitudinal.complete_policies(),
             "exact complete 32-policy structural catalogue required")
        object.__setattr__(self, "policies", policies)


@dataclass(frozen=True)
class ParameterInterval:
    row: MissingRow
    lower: F = F(0)
    upper: F = F(1)

    def __post_init__(self):
        need(type(self.row) is MissingRow, "missing row required")
        exact(self.lower)
        exact(self.upper)
        need(self.lower == 0 and self.upper == 1,
             "saturated missing binary row must range over [0,1]")


@dataclass(frozen=True)
class ContinuousFibre:
    identity: str
    profile: CompletionProfile
    parameters: tuple
    exact_for_profile: bool = True

    def __post_init__(self):
        identity(self.identity, "fibre identity required")
        need(type(self.profile) is CompletionProfile,
             "completion profile required")
        need(type(self.parameters) in (tuple, list) and
             all(type(parameter) is ParameterInterval
                 for parameter in self.parameters),
             "ordered parameter intervals required")
        object.__setattr__(self, "parameters", tuple(self.parameters))
        need(self.exact_for_profile is True,
             "continuous fibre is exact only for its stated profile")


@dataclass(frozen=True)
class CornerAssignment:
    identity: str
    # Ordered (missing-row identity, exact bit) pairs.
    coordinates: tuple

    def __post_init__(self):
        identity(self.identity, "corner identity required")
        need(type(self.coordinates) in (tuple, list),
             "ordered corner coordinates required")
        coordinates = tuple(tuple(pair) for pair in self.coordinates)
        need(all(len(pair) == 2 and type(pair[0]) is str and pair[0] and
                 type(pair[1]) is F and pair[1] in (0, 1)
                 for pair in coordinates),
             "corner coordinates require exact ordered bits")
        need(len({pair[0] for pair in coordinates}) == len(coordinates),
             "duplicate corner coordinate")
        object.__setattr__(self, "coordinates", coordinates)


@dataclass(frozen=True)
class CompletionPoint:
    """An exact point used only for independent interior evaluation."""
    identity: str
    coordinates: tuple

    def __post_init__(self):
        identity(self.identity, "completion-point identity required")
        coordinates = tuple(tuple(pair) for pair in self.coordinates)
        need(all(len(pair) == 2 and type(pair[0]) is str and pair[0] and
                 type(pair[1]) is F and 0 <= pair[1] <= 1
                 for pair in coordinates),
             "completion coordinates require exact values in [0,1]")
        need(len({pair[0] for pair in coordinates}) == len(coordinates),
             "duplicate completion coordinate")
        object.__setattr__(self, "coordinates", coordinates)


@dataclass(frozen=True)
class CornerMember:
    assignment: CornerAssignment
    subject: sequential.Subject

    def __post_init__(self):
        need(type(self.assignment) is CornerAssignment and
             type(self.subject) is sequential.Subject,
             "corner assignment and completed subject required")
        self.subject.validate()


@dataclass(frozen=True)
class CornerFamily:
    identity: str
    continuous_fibre_identity: str
    query_class: str
    members: tuple
    equals_continuous_fibre: bool = False

    def __post_init__(self):
        for value in (self.identity, self.continuous_fibre_identity,
                      self.query_class):
            identity(value, "corner-family identities required")
        need(type(self.members) in (tuple, list) and
             all(type(member) is CornerMember for member in self.members),
             "ordered corner members required")
        members = tuple(self.members)
        need(1 <= len(members) <= MAX_CORNERS and
             len({member.assignment.identity for member in members}) == len(members),
             "one to sixteen distinct corners required")
        object.__setattr__(self, "members", members)
        need(type(self.equals_continuous_fibre) is bool,
             "corner/fibre equality flag required")


@dataclass(frozen=True)
class PolicyCell:
    corner_identity: str
    policy_identity: str
    distribution: tuple
    expected_loss: F
    sequential_policy: sequential.Policy
    certificate: sequential.Certificate

    def __post_init__(self):
        identity(self.corner_identity, "corner identity required")
        identity(self.policy_identity, "policy identity required")
        distribution = tuple(self.distribution)
        need(len(distribution) == 2 and all(type(value) is F and 0 <= value <= 1
                                           for value in distribution) and
             sum(distribution, F(0)) == 1,
             "exact normalized binary policy distribution required")
        object.__setattr__(self, "distribution", distribution)
        exact(self.expected_loss)
        need(type(self.sequential_policy) is sequential.Policy and
             type(self.certificate) is sequential.Certificate,
             "ordinary sequential policy and certificate required")


@dataclass(frozen=True)
class ExactInterval:
    lower: F
    upper: F
    lower_witnesses: tuple
    upper_witnesses: tuple

    def __post_init__(self):
        exact(self.lower)
        exact(self.upper)
        need(self.lower <= self.upper, "ordered exact interval required")
        for field in ("lower_witnesses", "upper_witnesses"):
            values = tuple(getattr(self, field))
            need(values and all(type(value) is str and value for value in values),
                 "attaining corner witnesses required")
            object.__setattr__(self, field, values)


@dataclass(frozen=True)
class PolicyFibreResult:
    policy: longitudinal.DynamicPolicy
    bad_outcome_probability: ExactInterval
    expected_loss: ExactInterval
    status: str

    def __post_init__(self):
        need(type(self.policy) is longitudinal.DynamicPolicy and
             type(self.bad_outcome_probability) is ExactInterval and
             type(self.expected_loss) is ExactInterval,
             "complete policy-fibre result required")
        need(self.status in (POINT_POLICY, PARTIAL_POLICY),
             "invalid policy identification status")


@dataclass(frozen=True)
class PairwiseMaximum:
    candidate_policy_identity: str
    comparator_policy_identity: str
    maximum_difference: F
    corner_witnesses: tuple

    def __post_init__(self):
        identity(self.candidate_policy_identity)
        identity(self.comparator_policy_identity)
        exact(self.maximum_difference)
        need(type(self.corner_witnesses) in (tuple, list) and
             bool(self.corner_witnesses), "pairwise maximum witnesses required")
        object.__setattr__(self, "corner_witnesses",
                           tuple(self.corner_witnesses))


@dataclass(frozen=True)
class CornerDecision:
    corner_identity: str
    minimum_loss: F
    minimizers: tuple

    def __post_init__(self):
        identity(self.corner_identity)
        exact(self.minimum_loss)
        need(type(self.minimizers) in (tuple, list) and bool(self.minimizers),
             "complete corner minimizing set required")
        object.__setattr__(self, "minimizers", tuple(self.minimizers))


@dataclass(frozen=True)
class DecisionSummary:
    status: str
    common_minimizers: tuple
    corner_decisions: tuple
    pairwise_maxima: tuple

    def __post_init__(self):
        need(self.status in (DECISION_IDENTIFIED, DECISION_MODEL_DEPENDENT),
             "invalid causal decision status")
        object.__setattr__(self, "common_minimizers",
                           tuple(self.common_minimizers))
        object.__setattr__(self, "corner_decisions",
                           tuple(self.corner_decisions))
        object.__setattr__(self, "pairwise_maxima",
                           tuple(self.pairwise_maxima))


@dataclass(frozen=True)
class RobustSummary:
    criterion_identity: str
    worst_losses: tuple
    minimax_loss_winners: tuple
    same_model_worst_regrets: tuple
    minimax_regret_winners: tuple

    def __post_init__(self):
        identity(self.criterion_identity, "robust criterion identity required")
        object.__setattr__(self, "worst_losses", tuple(self.worst_losses))
        object.__setattr__(self, "minimax_loss_winners",
                           tuple(self.minimax_loss_winners))
        object.__setattr__(self, "same_model_worst_regrets",
                           tuple(self.same_model_worst_regrets))
        object.__setattr__(self, "minimax_regret_winners",
                           tuple(self.minimax_regret_winners))


@dataclass(frozen=True)
class PersistentReuse:
    status: str
    model_limit: int
    family: object = None
    common_evidence: object = None
    minimax_loss_evidence: object = None
    minimax_regret_evidence: object = None

    def __post_init__(self):
        need(self.status in (PERSISTENT_REUSED, PERSISTENT_LOCAL),
             "invalid persistent composition status")
        need(type(self.model_limit) is int and self.model_limit == families.MAX_MODELS,
             "existing persistent-family limit changed")


@dataclass(frozen=True)
class FibreEvidence:
    request: FibreRequest
    status: str
    fibre: ContinuousFibre
    corner_family: CornerFamily
    cells: tuple
    policy_results: tuple
    decision: DecisionSummary
    robust: RobustSummary
    persistent_reuse: PersistentReuse
    pr20_bridge: object = None
    supplied_boundary: str = SUPPLIED_BOUNDARY

    def __post_init__(self):
        need(type(self.request) is FibreRequest and self.status == EXACT_FIBRE and
             type(self.fibre) is ContinuousFibre and
             type(self.corner_family) is CornerFamily and
             type(self.decision) is DecisionSummary and
             type(self.robust) is RobustSummary and
             type(self.persistent_reuse) is PersistentReuse,
             "complete exact fibre evidence required")
        object.__setattr__(self, "cells", tuple(self.cells))
        object.__setattr__(self, "policy_results", tuple(self.policy_results))
        need(self.supplied_boundary == SUPPLIED_BOUNDARY,
             "causal and empirical boundary changed")


@dataclass(frozen=True)
class BoundaryEvidence:
    request: FibreRequest
    status: str
    missing_earlier_histories: tuple = ()
    unsupported_restrictions: tuple = ()

    def __post_init__(self):
        need(type(self.request) is FibreRequest,
             "boundary request binding required")
        need(self.status in (OUTSIDE_PROFILE, UNSUPPORTED_RESTRICTION,
                             UNSUPPORTED_QUERY), "invalid boundary status")
        object.__setattr__(self, "missing_earlier_histories",
                           tuple(tuple(row) for row in self.missing_earlier_histories))
        object.__setattr__(self, "unsupported_restrictions",
                           tuple(self.unsupported_restrictions))


def _earlier_support_failures(observation):
    failures = []
    for a1 in (0, 1):
        if longitudinal._marginal_a1(observation, a1) == 0:
            failures.append(("A1", a1))
    for a1, intermediate in product((0, 1), repeat=2):
        if longitudinal._marginal_a1_l1(observation, a1, intermediate) == 0:
            failures.append(("A1,L1", a1, intermediate))
    return tuple(failures)


def _validate_supported_request(request):
    if request.query_class != QUERY_CLASS:
        return UNSUPPORTED_QUERY, (), ()
    failures = _earlier_support_failures(request.observation)
    if failures:
        return OUTSIDE_PROFILE, failures, ()
    profile = request.completion_profile
    if (profile.kind != SATURATED_PROFILE or
            profile.cross_row_restrictions):
        restrictions = profile.cross_row_restrictions or (profile.kind,)
        return UNSUPPORTED_RESTRICTION, (), restrictions
    expected = derive_missing_rows(request.observation)
    need(request.missing_rows == expected,
         "missing, extra, reordered, renamed, or stale support-derived row mapping")
    need(len(expected) <= MAX_MISSING_ROWS,
         "missing-row dimension exceeds bounded profile")
    return EXACT_FIBRE, (), ()


def _bridge_request(request):
    return longitudinal.BridgeRequest(
        request.observation, request.premises, request.loss,
        request.deployment_population_identity, request.subject_identity,
        request.policy_catalogue_identity, request.support_query_identity,
        request.query_identity + ":pr20-full-support-collapse")


def _corner_identity(request, bits):
    order = ",".join(row.identity for row in request.missing_rows) or "none"
    assignment = "".join(str(bit) for bit in bits) or "point"
    return (f"{request.corner_family_identity}:observation={request.observation.identity}:"
            f"rows={order}:assignment={assignment}")


def _assignments(request):
    bit_rows = product((0, 1), repeat=len(request.missing_rows))
    answer = []
    for bits in bit_rows:
        coordinates = tuple((row.identity, F(bit))
                            for row, bit in zip(request.missing_rows, bits))
        answer.append(CornerAssignment(_corner_identity(request, bits), coordinates))
    return tuple(answer)


def _fibre_premises(request, assignment):
    bridge = _bridge_request(request)
    base = longitudinal._subject_premises(bridge)
    return (
        "exact-saturated-longitudinal-kernel-completion",
        *base[1:],
        f"completion-profile:{request.completion_profile.identity}",
        f"fibre:{request.fibre_identity}",
        "ordered-missing-rows:" + "|".join(row.identity for row in request.missing_rows),
        "corner-assignment:" + "|".join(
            f"{name}={value}" for name, value in assignment.coordinates),
        f"corner-query-class:{request.query_class}",
    )


def _producer_subject(request, assignment):
    """Candidate completed subject using marginal helpers."""
    if not request.missing_rows:
        return longitudinal._producer_subject(_bridge_request(request))
    obs, loss, coding = request.observation, request.loss, request.observation.coding
    theta = dict(assignment.coordinates)
    row_ids = {row.coordinate: row.identity for row in request.missing_rows}
    nodes, root_actions = [], []
    for a1 in (0, 1):
        total = longitudinal._marginal_a1(obs, a1)
        outcomes = tuple(
            (f"{coding.intermediate.identity}={l1}",
             longitudinal._marginal_a1_l1(obs, a1, l1) / total)
            for l1 in (0, 1))
        root_actions.append(sequential.Action(
            f"{coding.first_action.identity}={a1}",
            loss.first_stage_costs[a1], outcomes))
    nodes.append(sequential.Node((), actions=root_actions))
    for a1, l1 in product((0, 1), repeat=2):
        history = ((f"{coding.first_action.identity}={a1}",
                    f"{coding.intermediate.identity}={l1}"),)
        actions = []
        for a2 in (0, 1):
            support = longitudinal._marginal_a1_l1_a2(obs, a1, l1, a2)
            if support:
                q = obs.mass(a1, l1, a2, 1) / support
            else:
                q = theta[row_ids[a1, l1, a2]]
            actions.append(sequential.Action(
                f"{coding.second_action.identity}={a2}",
                loss.second(a1, l1, a2),
                ((f"{coding.outcome.identity}=0", 1 - q),
                 (f"{coding.outcome.identity}=1", q))))
        nodes.append(sequential.Node(history, actions=actions))
    for a1, l1, a2, y in product((0, 1), repeat=4):
        history = ((f"{coding.first_action.identity}={a1}",
                    f"{coding.intermediate.identity}={l1}"),
                   (f"{coding.second_action.identity}={a2}",
                    f"{coding.outcome.identity}={y}"))
        nodes.append(sequential.Node(history,
                                     terminal=loss.terminal(a1, l1, a2, y)))
    return sequential.Subject(assignment.identity, 2, loss.unit,
                              _fibre_premises(request, assignment), nodes)


def _receiver_subject(request, assignment):
    """Receiver reconstruction using direct 16-cell slices."""
    if not request.missing_rows:
        return longitudinal._receiver_subject(_bridge_request(request))
    obs, loss, coding = request.observation, request.loss, request.observation.coding
    theta = {name: value for name, value in assignment.coordinates}
    row_ids = {row.coordinate: row.identity for row in request.missing_rows}
    root = []
    for a in (0, 1):
        base = 8 * a
        denominator = sum(obs.masses[base:base + 8], F(0))
        outcomes = []
        for l in (0, 1):
            offset = base + 4 * l
            outcomes.append((f"{coding.intermediate.identity}={l}",
                             sum(obs.masses[offset:offset + 4], F(0)) /
                             denominator))
        root.append(sequential.Action(f"{coding.first_action.identity}={a}",
                                      loss.first_stage_costs[a], outcomes))
    nodes = [sequential.Node((), actions=root)]
    for a, l in product((0, 1), repeat=2):
        history = ((f"{coding.first_action.identity}={a}",
                    f"{coding.intermediate.identity}={l}"),)
        menu = []
        for second in (0, 1):
            cell = 8 * a + 4 * l + 2 * second
            denominator = obs.masses[cell] + obs.masses[cell + 1]
            if denominator:
                q = obs.masses[cell + 1] / denominator
            else:
                q = theta[row_ids[a, l, second]]
            menu.append(sequential.Action(
                f"{coding.second_action.identity}={second}",
                loss.second_stage_costs[4 * a + 2 * l + second],
                ((f"{coding.outcome.identity}=0", 1 - q),
                 (f"{coding.outcome.identity}=1", q))))
        nodes.append(sequential.Node(history, actions=menu))
    for a, l, second, y in product((0, 1), repeat=4):
        history = ((f"{coding.first_action.identity}={a}",
                    f"{coding.intermediate.identity}={l}"),
                   (f"{coding.second_action.identity}={second}",
                    f"{coding.outcome.identity}={y}"))
        nodes.append(sequential.Node(
            history,
            terminal=loss.terminal_losses[8 * a + 4 * l + 2 * second + y]))
    return sequential.Subject(assignment.identity, 2, loss.unit,
                              _fibre_premises(request, assignment), nodes)


def _producer_policy_value(request, policy, assignment):
    """Candidate direct g-formula evaluation at one completion."""
    obs, loss = request.observation, request.loss
    theta = dict(assignment.coordinates)
    row_ids = {row.coordinate: row.identity for row in request.missing_rows}
    a = policy.first_action
    p_a = longitudinal._marginal_a1(obs, a)
    risk = F(0)
    value = loss.first_stage_costs[a]
    for l in (0, 1):
        p_l = longitudinal._marginal_a1_l1(obs, a, l) / p_a
        second = policy.second(a, l)
        support = longitudinal._marginal_a1_l1_a2(obs, a, l, second)
        q = (obs.mass(a, l, second, 1) / support if support else
             theta[row_ids[a, l, second]])
        risk += p_l * q
        value += p_l * (loss.second(a, l, second) +
                        (1 - q) * loss.terminal(a, l, second, 0) +
                        q * loss.terminal(a, l, second, 1))
    return (1 - risk, risk), value


def _receiver_policy_value(request, policy, assignment):
    """Independent cell-index evaluation of the same completion."""
    obs, loss = request.observation, request.loss
    theta = {name: value for name, value in assignment.coordinates}
    row_ids = {row.coordinate: row.identity for row in request.missing_rows}
    a = policy.first_action
    base = 8 * a
    first_mass = sum(obs.masses[base:base + 8], F(0))
    bad = F(0)
    total = loss.first_stage_costs[a]
    for l in (0, 1):
        offset = base + 4 * l
        history_mass = sum(obs.masses[offset:offset + 4], F(0))
        history_probability = history_mass / first_mass
        second = policy.second_actions[2 * a + l]
        cell = offset + 2 * second
        supported = obs.masses[cell] + obs.masses[cell + 1]
        q = (obs.masses[cell + 1] / supported if supported else
             theta[row_ids[a, l, second]])
        bad += history_probability * q
        terminal = loss.terminal_losses[cell] * (1 - q) + \
            loss.terminal_losses[cell + 1] * q
        total += history_probability * (
            loss.second_stage_costs[4 * a + 2 * l + second] + terminal)
    return (1 - bad, bad), total


def _interval(values, corner_ids):
    lower, upper = min(values), max(values)
    return ExactInterval(lower, upper,
                         tuple(name for name, value in zip(corner_ids, values)
                               if value == lower),
                         tuple(name for name, value in zip(corner_ids, values)
                               if value == upper))


def _producer_summaries(request, assignments, cells):
    corner_ids = tuple(assignment.identity for assignment in assignments)
    matrix = []
    risks = []
    for i in range(len(assignments)):
        row = cells[i * POLICY_COUNT:(i + 1) * POLICY_COUNT]
        matrix.append(tuple(cell.expected_loss for cell in row))
        risks.append(tuple(cell.distribution[1] for cell in row))
    matrix, risks = tuple(matrix), tuple(risks)
    policy_results = []
    for j, policy in enumerate(request.policies):
        risk_interval = _interval(tuple(row[j] for row in risks), corner_ids)
        loss_interval = _interval(tuple(row[j] for row in matrix), corner_ids)
        status = (POINT_POLICY if risk_interval.lower == risk_interval.upper and
                  loss_interval.lower == loss_interval.upper else PARTIAL_POLICY)
        policy_results.append(PolicyFibreResult(policy, risk_interval,
                                                loss_interval, status))
    corner_decisions = []
    for corner_id, row in zip(corner_ids, matrix):
        minimum = min(row)
        corner_decisions.append(CornerDecision(
            corner_id, minimum,
            tuple(policy.identity for policy, value in zip(request.policies, row)
                  if value == minimum)))
    pairwise = []
    common = []
    for j, candidate in enumerate(request.policies):
        dominates = True
        for k, comparator in enumerate(request.policies):
            differences = tuple(row[j] - row[k] for row in matrix)
            maximum = max(differences)
            witnesses = tuple(name for name, value in zip(corner_ids, differences)
                              if value == maximum)
            pairwise.append(PairwiseMaximum(candidate.identity,
                                            comparator.identity,
                                            maximum, witnesses))
            if maximum > 0:
                dominates = False
        if dominates:
            common.append(candidate.identity)
    decision = DecisionSummary(
        DECISION_IDENTIFIED if common else DECISION_MODEL_DEPENDENT,
        tuple(common), tuple(corner_decisions), tuple(pairwise))
    worst_losses = tuple((policy.identity, max(row[j] for row in matrix))
                         for j, policy in enumerate(request.policies))
    best_worst = min(value for _, value in worst_losses)
    minimax = tuple(name for name, value in worst_losses if value == best_worst)
    regrets = []
    for j, policy in enumerate(request.policies):
        value = max(row[j] - min(row) for row in matrix)
        regrets.append((policy.identity, value))
    best_regret = min(value for _, value in regrets)
    minimax_regret = tuple(name for name, value in regrets
                           if value == best_regret)
    robust = RobustSummary(
        request.query_identity + ":supplied-minimax-over-exact-fibre",
        worst_losses, minimax, tuple(regrets), minimax_regret)
    return tuple(policy_results), decision, robust, matrix


def _persistent_reuse(request, members):
    if len(members) > families.MAX_MODELS:
        return PersistentReuse(PERSISTENT_LOCAL, families.MAX_MODELS)
    family = families.Family(
        request.corner_family_identity,
        tuple(families.Member(member.assignment.identity, member.subject)
              for member in members))
    entries = tuple(families.PolicyEntry(
        policy.identity,
        longitudinal.to_sequential_policy(members[0].subject, policy,
                                          request.observation.coding))
                    for policy in request.policies)
    def evidence(claim):
        return families.choose(families.ChoiceRequest(
            family, entries, families.FULL, claim))
    return PersistentReuse(PERSISTENT_REUSED, families.MAX_MODELS, family,
                           evidence(families.COMMON_OPTIMAL),
                           evidence(families.MINIMAX_LOSS),
                           evidence(families.MINIMAX_REGRET))


def produce(request):
    """Candidate producer for the exact bounded saturated fibre."""
    need(type(request) is FibreRequest, "kernel-fibre request required")
    status, failures, restrictions = _validate_supported_request(request)
    if status != EXACT_FIBRE:
        return BoundaryEvidence(request, status, failures, restrictions)
    fibre = ContinuousFibre(
        request.fibre_identity, request.completion_profile,
        tuple(ParameterInterval(row) for row in request.missing_rows))
    assignments = _assignments(request)
    members = tuple(CornerMember(assignment,
                                 _producer_subject(request, assignment))
                    for assignment in assignments)
    corner_family = CornerFamily(
        request.corner_family_identity, request.fibre_identity,
        request.query_class, members, not request.missing_rows)
    cells = []
    for member in members:
        for policy in request.policies:
            distribution, value = _producer_policy_value(
                request, policy, member.assignment)
            seq_policy = longitudinal.to_sequential_policy(
                member.subject, policy, request.observation.coding)
            certificate = sequential.produce(member.subject, seq_policy)
            cells.append(PolicyCell(member.assignment.identity, policy.identity,
                                    distribution, value, seq_policy, certificate))
    policy_results, decision, robust, _ = _producer_summaries(
        request, assignments, tuple(cells))
    pr20 = (longitudinal.produce_bridge(_bridge_request(request))
            if not request.missing_rows else None)
    return FibreEvidence(
        request, EXACT_FIBRE, fibre, corner_family, tuple(cells),
        policy_results, decision, robust, _persistent_reuse(request, members),
        pr20)


def _path_distribution(subject, policy, outcome_identity):
    answer = [F(0), F(0)]
    for history, mass, _cost in sequential.paths(subject, policy):
        label = history[-1][1]
        for y in (0, 1):
            if label == f"{outcome_identity}={y}":
                answer[y] += mass
    need(sum(answer, F(0)) == 1,
         "independent complete-path distribution must normalize")
    return tuple(answer)


def _receiver_summaries(request, assignments, matrix, risks):
    corner_ids = tuple(assignment.identity for assignment in assignments)
    expected_policy_results = []
    for column, policy in enumerate(request.policies):
        risk_values = tuple(risks[row][column]
                            for row in range(len(assignments)))
        loss_values = tuple(matrix[row][column]
                            for row in range(len(assignments)))
        risk_bounds = _interval(risk_values, corner_ids)
        loss_bounds = _interval(loss_values, corner_ids)
        point = (risk_bounds.lower == risk_bounds.upper and
                 loss_bounds.lower == loss_bounds.upper)
        expected_policy_results.append(PolicyFibreResult(
            policy, risk_bounds, loss_bounds,
            POINT_POLICY if point else PARTIAL_POLICY))
    expected_corners = []
    for corner_id, values in zip(corner_ids, matrix):
        best = min(values)
        expected_corners.append(CornerDecision(
            corner_id, best,
            tuple(request.policies[index].identity
                  for index, value in enumerate(values) if value == best)))
    expected_pairwise = []
    common = []
    for candidate_index, candidate in enumerate(request.policies):
        candidate_common = True
        for comparator_index, comparator in enumerate(request.policies):
            differences = tuple(
                values[candidate_index] - values[comparator_index]
                for values in matrix)
            greatest = max(differences)
            expected_pairwise.append(PairwiseMaximum(
                candidate.identity, comparator.identity, greatest,
                tuple(corner_ids[index] for index, value in enumerate(differences)
                      if value == greatest)))
            candidate_common = candidate_common and greatest <= 0
        if candidate_common:
            common.append(candidate.identity)
    expected_decision = DecisionSummary(
        DECISION_IDENTIFIED if common else DECISION_MODEL_DEPENDENT,
        tuple(common), tuple(expected_corners), tuple(expected_pairwise))
    worst = tuple((policy.identity,
                   max(matrix[row][index] for row in range(len(matrix))))
                  for index, policy in enumerate(request.policies))
    least_worst = min(value for _name, value in worst)
    minimax = tuple(name for name, value in worst if value == least_worst)
    regret = []
    for index, policy in enumerate(request.policies):
        regret.append((policy.identity,
                       max(values[index] - min(values) for values in matrix)))
    least_regret = min(value for _name, value in regret)
    minimax_regret = tuple(name for name, value in regret
                           if value == least_regret)
    expected_robust = RobustSummary(
        request.query_identity + ":supplied-minimax-over-exact-fibre",
        worst, minimax, tuple(regret), minimax_regret)
    return tuple(expected_policy_results), expected_decision, expected_robust


def consume(expected, evidence):
    """Authoritative receiver; reconstructs rows, subjects, paths, and decisions."""
    need(type(expected) is FibreRequest and
         type(evidence) in (FibreEvidence, BoundaryEvidence),
         "request and kernel-fibre evidence required")
    need(evidence.request == expected,
         "stale observation, support map, premises, profile, loss, policy catalogue, population, subject, fibre, family, or query")
    status, failures, restrictions = _validate_supported_request(expected)
    if status != EXACT_FIBRE:
        need(type(evidence) is BoundaryEvidence and evidence.status == status and
             evidence.missing_earlier_histories == failures and
             evidence.unsupported_restrictions == restrictions,
             "false or stale kernel-fibre boundary classification")
        return {"status": status, "missing_earlier_histories": failures,
                "unsupported_restrictions": restrictions,
                "checked": "bounded support/restriction boundary; no incompatibility or impossibility claim"}
    need(type(evidence) is FibreEvidence and evidence.status == EXACT_FIBRE,
         "supported exact fibre received no complete result")
    parameters = tuple(ParameterInterval(row) for row in expected.missing_rows)
    need(evidence.fibre == ContinuousFibre(
        expected.fibre_identity, expected.completion_profile, parameters),
         "false continuous saturated fibre")
    assignments = _assignments(expected)
    need(len(assignments) == 2 ** len(expected.missing_rows) <= MAX_CORNERS,
         "corner count mismatch")
    members = tuple(CornerMember(assignment,
                                 _receiver_subject(expected, assignment))
                    for assignment in assignments)
    expected_family = CornerFamily(
        expected.corner_family_identity, expected.fibre_identity,
        expected.query_class, members, not expected.missing_rows)
    need(evidence.corner_family == expected_family,
         "missing, duplicate, reordered, stale, or forged corner subject")
    need(len(evidence.cells) == len(members) * POLICY_COUNT,
         "incomplete corner-by-policy evidence matrix")
    matrix, risks, cell_index = [], [], 0
    for member in members:
        value_row, risk_row = [], []
        for policy in expected.policies:
            cell = evidence.cells[cell_index]
            cell_index += 1
            need(type(cell) is PolicyCell and
                 (cell.corner_identity, cell.policy_identity) ==
                 (member.assignment.identity, policy.identity),
                 "wrong or reordered corner-policy cell")
            distribution, value = _receiver_policy_value(
                expected, policy, member.assignment)
            seq_policy = longitudinal.to_sequential_policy(
                member.subject, policy, expected.observation.coding)
            need(cell.distribution == distribution and
                 cell.expected_loss == value and
                 cell.sequential_policy == seq_policy,
                 "false causal policy distribution, loss, or common policy")
            checked = sequential.consume(member.subject, seq_policy,
                                         cell.certificate)
            path_value = sequential.path_cost(member.subject, seq_policy)
            path_distribution = _path_distribution(
                member.subject, seq_policy,
                expected.observation.coding.outcome.identity)
            need(checked["policy_upper"] == path_value == value and
                 path_distribution == distribution,
                 "causal formula, certificate, and independent paths disagree")
            value_row.append(value)
            risk_row.append(distribution[1])
        matrix.append(tuple(value_row))
        risks.append(tuple(risk_row))
    matrix, risks = tuple(matrix), tuple(risks)
    policy_results, decision, robust = _receiver_summaries(
        expected, assignments, matrix, risks)
    need(evidence.policy_results == policy_results,
         "false policy identification interval or corner witness")
    need(evidence.decision == decision,
         "false common-optimum classification, completion witness, or pairwise maximum")
    need(evidence.robust == robust,
         "false supplied minimax-loss or same-model regret result")
    reuse = evidence.persistent_reuse
    if len(members) <= families.MAX_MODELS:
        persistent_family = families.Family(
            expected.corner_family_identity,
            tuple(families.Member(member.assignment.identity, member.subject)
                  for member in members))
        need(reuse.status == PERSISTENT_REUSED and
             reuse.model_limit == families.MAX_MODELS and
             reuse.family == persistent_family,
             "existing persistent-family composition missing")
        entries = tuple(families.PolicyEntry(
            policy.identity,
            longitudinal.to_sequential_policy(members[0].subject, policy,
                                              expected.observation.coding))
                        for policy in expected.policies)
        claims = (
            (families.COMMON_OPTIMAL, reuse.common_evidence),
            (families.MINIMAX_LOSS, reuse.minimax_loss_evidence),
            (families.MINIMAX_REGRET, reuse.minimax_regret_evidence),
        )
        checked_choices = {}
        for claim, retained in claims:
            request = families.ChoiceRequest(reuse.family, entries,
                                             families.FULL, claim)
            checked_choices[claim] = families.consume_choice(request, retained)
        need(checked_choices[families.COMMON_OPTIMAL]["winners"] ==
             decision.common_minimizers and
             checked_choices[families.MINIMAX_LOSS]["winners"] ==
             robust.minimax_loss_winners and
             checked_choices[families.MINIMAX_REGRET]["winners"] ==
             robust.minimax_regret_winners,
             "persistent-family and local exact decision results disagree")
    else:
        need(reuse == PersistentReuse(PERSISTENT_LOCAL, families.MAX_MODELS),
             "larger bounded corner family must expose frozen family-checker limit")
    if not expected.missing_rows:
        bridge_request = _bridge_request(expected)
        bridge = longitudinal.consume_bridge(bridge_request,
                                              evidence.pr20_bridge)
        need(members[0].subject == evidence.pr20_bridge.subject and
             bridge["policies_checked"] == POLICY_COUNT,
             "zero-gap fibre did not collapse byte-for-byte to PR20 subject")
    else:
        need(evidence.pr20_bridge is None,
             "positive-dimensional fibre cannot carry point-subject PR20 evidence")
    return {
        "status": EXACT_FIBRE,
        "dimension": len(parameters),
        "continuous_fibre": True,
        "corners_checked": len(members),
        "policies_checked": POLICY_COUNT,
        "cells_checked": len(evidence.cells),
        "decision_status": decision.status,
        "common_minimizers": decision.common_minimizers,
        "minimax_loss_winners": robust.minimax_loss_winners,
        "minimax_regret_winners": robust.minimax_regret_winners,
        "persistent_composition": reuse.status,
        "premise_identities": longitudinal.premise_identities(expected.premises),
        "supplied_boundary": SUPPLIED_BOUNDARY,
    }


def policy_at_completion(request, policy, coordinates):
    """Exact interior audit; not an optimization method or finite-fibre claim."""
    need(type(request) is FibreRequest and type(policy) is longitudinal.DynamicPolicy,
         "request and one common policy required")
    status, _, _ = _validate_supported_request(request)
    need(status == EXACT_FIBRE, "interior audit requires a supported exact fibre")
    need(type(coordinates) in (tuple, list) and
         len(coordinates) == len(request.missing_rows),
         "one exact coordinate per ordered missing row required")
    values = tuple(longitudinal.rational(value) for value in coordinates)
    need(all(0 <= value <= 1 for value in values),
         "interior fibre coordinates must lie in [0,1]")
    assignment = CompletionPoint(
        request.fibre_identity + ":interior-audit",
        tuple((row.identity, value)
              for row, value in zip(request.missing_rows, values)))
    return _receiver_policy_value(request, policy, assignment)


def same_model_regret(candidate_corner_identity, comparator_corner_identity,
                      candidate_value, comparator_value):
    """Reject the tempting cross-completion regret subtraction."""
    identity(candidate_corner_identity, "candidate completion identity required")
    identity(comparator_corner_identity, "comparator completion identity required")
    need(candidate_corner_identity == comparator_corner_identity,
         "regret subtraction requires one and the same causal completion")
    return exact(candidate_value) - exact(comparator_value)


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
