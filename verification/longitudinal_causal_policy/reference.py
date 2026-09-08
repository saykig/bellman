"""Exact two-stage longitudinal causal policy and Bellman bridge checks.

The bounded profile has binary A1, L1, A2, and Y.  It conditions exact
g-formula arithmetic on explicitly supplied causal premises; it does not
learn or empirically validate them.  Policy-specific identification and the
stronger support needed to construct a complete Bellman subject are kept
separate.  Candidate producers and authoritative receivers use distinct
calculation paths.
"""
from dataclasses import asdict, dataclass
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from verification.sequential_certificates import reference as sequential  # noqa: E402


Invalid = sequential.Invalid

POLICY_IDENTIFIED = "identified-dynamic-regime-under-supplied-sequential-premises"
FIRST_STAGE_FAILURE = "first-stage-positivity-failure"
SECOND_STAGE_FAILURE = "second-stage-policy-positivity-failure"
FULL_SUBJECT = "full-two-stage-causal-subject-identified"
POLICY_ONLY = "policy-identified-full-subject-not-supported"
BRIDGE_CHECKED = "causal-to-sequential-bridge-checked"
UNSUPPORTED_QUERY = "unsupported-longitudinal-causal-query"
POLICY_QUERY_KIND = "complete-binary-outcome-distribution-and-exact-additive-loss"
BRIDGE_QUERY_KIND = "full-subject-all-policy-causal-sequential-equivalence"

SUPPLIED_BOUNDARY = (
    "observational law and longitudinal causal premises supplied; exact "
    "identification consequence checked conditionally; no premise discovery, "
    "empirical validation, transport, interference warrant, safety composition, "
    "or authority to act"
)


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
        result = F(value)
    except (ValueError, ZeroDivisionError) as error:
        raise Invalid(message) from error
    need(max(abs(result.numerator).bit_length(),
             result.denominator.bit_length()) <= 256,
         "input rational exceeds 256-bit profile")
    return result


def exact(value, message="exact Fraction required"):
    need(type(value) is F, message)
    return value


def _input_vector(values, size, message):
    need(type(values) in (tuple, list) and len(values) == size, message)
    return tuple(rational(value, message) for value in values)


@dataclass(frozen=True)
class BinaryVariable:
    identity: str
    values: tuple = ("0", "1")

    def __post_init__(self):
        identity(self.identity, "variable identity required")
        values = tuple(self.values)
        need(len(values) == 2 and len(set(values)) == 2 and
             all(type(value) is str and value for value in values),
             "two distinct nonempty binary labels required")
        object.__setattr__(self, "values", values)


@dataclass(frozen=True)
class LongitudinalCoding:
    first_action: BinaryVariable
    intermediate: BinaryVariable
    second_action: BinaryVariable
    outcome: BinaryVariable

    def __post_init__(self):
        variables = (self.first_action, self.intermediate,
                     self.second_action, self.outcome)
        need(all(type(variable) is BinaryVariable for variable in variables),
             "four binary variables required")
        need(len({variable.identity for variable in variables}) == 4,
             "longitudinal variable identities must be distinct")

    @property
    def identities(self):
        return (self.first_action.identity, self.intermediate.identity,
                self.second_action.identity, self.outcome.identity)


@dataclass(frozen=True)
class TemporalOrder:
    identity: str
    variables: tuple

    def __post_init__(self):
        identity(self.identity, "temporal-order identity required")
        variables = tuple(self.variables)
        need(len(variables) == 4 and len(set(variables)) == 4 and
             all(type(value) is str and value for value in variables),
             "four distinct temporal variables required")
        object.__setattr__(self, "variables", variables)


@dataclass(frozen=True)
class LongitudinalObservation:
    identity: str
    population_identity: str
    coding: LongitudinalCoding
    temporal_order: TemporalOrder
    # Order: a1 major, then l1, a2, y; each coordinate in (0, 1).
    masses: tuple

    def __post_init__(self):
        identity(self.identity, "observational-law identity required")
        identity(self.population_identity, "population/regime identity required")
        need(type(self.coding) is LongitudinalCoding and
             type(self.temporal_order) is TemporalOrder,
             "longitudinal coding and temporal order required")
        need(self.temporal_order.variables == self.coding.identities,
             "temporal order must be exactly A1, L1, A2, Y")
        masses = _input_vector(self.masses, 16,
                               "complete exact 16-cell law required")
        need(all(0 <= value <= 1 for value in masses),
             "observational masses must lie in [0,1]")
        need(sum(masses, F(0)) == 1,
             "observational P(A1,L1,A2,Y) must normalize exactly")
        object.__setattr__(self, "masses", masses)

    def mass(self, a1, intermediate, a2, y):
        return self.masses[8 * a1 + 4 * intermediate + 2 * a2 + y]


@dataclass(frozen=True)
class SequentialCausalPremises:
    identity: str
    consistency_identity: str
    intervention_identity: str
    first_stage_exchangeability_identity: str
    second_stage_exchangeability_identity: str
    adapted_policy_identity: str
    no_interference_identity: str

    def __post_init__(self):
        values = (self.identity, self.consistency_identity,
                  self.intervention_identity,
                  self.first_stage_exchangeability_identity,
                  self.second_stage_exchangeability_identity,
                  self.adapted_policy_identity, self.no_interference_identity)
        for value in values:
            identity(value, "explicit longitudinal causal-premise identities required")
        need(len(set(values[1:])) == len(values[1:]),
             "causal-premise identities must remain distinct")


@dataclass(frozen=True)
class LongitudinalLoss:
    identity: str
    unit: str
    first_stage_costs: tuple
    # Order: a1 major, then l1, a2.
    second_stage_costs: tuple
    # Order: a1 major, then l1, a2, y.
    terminal_losses: tuple

    def __post_init__(self):
        identity(self.identity, "loss-table identity required")
        identity(self.unit, "loss unit required")
        object.__setattr__(self, "first_stage_costs", _input_vector(
            self.first_stage_costs, 2, "two exact first-stage costs required"))
        object.__setattr__(self, "second_stage_costs", _input_vector(
            self.second_stage_costs, 8, "eight exact second-stage costs required"))
        object.__setattr__(self, "terminal_losses", _input_vector(
            self.terminal_losses, 16, "sixteen exact terminal losses required"))

    def second(self, a1, intermediate, a2):
        return self.second_stage_costs[4 * a1 + 2 * intermediate + a2]

    def terminal(self, a1, intermediate, a2, y):
        return self.terminal_losses[8 * a1 + 4 * intermediate + 2 * a2 + y]


@dataclass(frozen=True)
class DynamicPolicy:
    identity: str
    first_action: int
    # Complete structural table in order (a1,l1)=(0,0),(0,1),(1,0),(1,1).
    second_actions: tuple

    def __post_init__(self):
        identity(self.identity, "policy identity required")
        need(type(self.first_action) is int and type(self.first_action) is not bool and
             self.first_action in (0, 1), "binary first-stage policy action required")
        actions = tuple(self.second_actions)
        need(len(actions) == 4 and all(type(action) is int and
             type(action) is not bool and action in (0, 1) for action in actions),
             "complete four-history binary second-stage policy required")
        object.__setattr__(self, "second_actions", actions)

    def second(self, a1, intermediate):
        return self.second_actions[2 * a1 + intermediate]


@dataclass(frozen=True)
class PolicyRequest:
    observation: LongitudinalObservation
    premises: SequentialCausalPremises
    loss: LongitudinalLoss
    policy: DynamicPolicy
    deployment_population_identity: str
    support_query_identity: str
    query_identity: str
    query_kind: str = POLICY_QUERY_KIND

    def __post_init__(self):
        need(type(self.observation) is LongitudinalObservation and
             type(self.premises) is SequentialCausalPremises and
             type(self.loss) is LongitudinalLoss and
             type(self.policy) is DynamicPolicy,
             "complete longitudinal causal policy request required")
        identity(self.deployment_population_identity,
                 "deployment population identity required")
        identity(self.support_query_identity, "support-query identity required")
        identity(self.query_identity, "policy causal-query identity required")
        identity(self.query_kind, "longitudinal causal-query kind required")
        need(self.deployment_population_identity ==
             self.observation.population_identity,
             "first bridge profile does not supply population transport")


@dataclass(frozen=True)
class PolicyEvidence:
    request: PolicyRequest
    status: str
    distribution: tuple = ()
    value: object = None
    # (l1, P(l1|a1), selected a2, P(Y=0|...), P(Y=1|...)).
    stratum_terms: tuple = ()
    missing_histories: tuple = ()
    full_subject_status: object = None
    supplied_boundary: str = SUPPLIED_BOUNDARY

    def __post_init__(self):
        need(type(self.request) is PolicyRequest,
             "policy request binding required")
        object.__setattr__(self, "distribution", tuple(self.distribution))
        object.__setattr__(self, "stratum_terms",
                           tuple(tuple(row) for row in self.stratum_terms))
        object.__setattr__(self, "missing_histories",
                           tuple(tuple(row) for row in self.missing_histories))
        need(self.status in (POLICY_IDENTIFIED, FIRST_STAGE_FAILURE,
                             SECOND_STAGE_FAILURE, UNSUPPORTED_QUERY),
             "invalid policy status")
        need(self.full_subject_status in (None, FULL_SUBJECT, POLICY_ONLY),
             "invalid full-subject support status")
        need(self.supplied_boundary == SUPPLIED_BOUNDARY,
             "causal/empirical boundary changed")


def _marginal_a1(observation, a1):
    return sum((observation.mass(a1, l1, a2, y)
                for l1, a2, y in product((0, 1), repeat=3)), F(0))


def _marginal_a1_l1(observation, a1, l1):
    return sum((observation.mass(a1, l1, a2, y)
                for a2, y in product((0, 1), repeat=2)), F(0))


def _marginal_a1_l1_a2(observation, a1, l1, a2):
    return observation.mass(a1, l1, a2, 0) + observation.mass(a1, l1, a2, 1)


def full_subject_support(observation):
    """Strong support for every structural action-history transition."""
    need(type(observation) is LongitudinalObservation, "observation required")
    return (all(_marginal_a1(observation, a1) > 0 for a1 in (0, 1)) and
            all(_marginal_a1_l1(observation, a1, l1) > 0
                for a1, l1 in product((0, 1), repeat=2)) and
            all(_marginal_a1_l1_a2(observation, a1, l1, a2) > 0
                for a1, l1, a2 in product((0, 1), repeat=3)))


def _producer_policy(request):
    """Candidate g-formula path, intentionally distinct from the receiver."""
    observation, policy = request.observation, request.policy
    a1 = policy.first_action
    p_a1 = _marginal_a1(observation, a1)
    if p_a1 == 0:
        return FIRST_STAGE_FAILURE, (), None, (), ((a1,),)
    rows, distribution, missing = [], [F(0), F(0)], []
    value = request.loss.first_stage_costs[a1]
    for l1 in (0, 1):
        p_a1_l1 = _marginal_a1_l1(observation, a1, l1)
        if p_a1_l1 == 0:
            continue
        p_l1 = p_a1_l1 / p_a1
        a2 = policy.second(a1, l1)
        support = _marginal_a1_l1_a2(observation, a1, l1, a2)
        if support == 0:
            missing.append((a1, l1, a2))
            continue
        outcome = (observation.mass(a1, l1, a2, 0) / support,
                   observation.mass(a1, l1, a2, 1) / support)
        rows.append((l1, p_l1, a2, outcome[0], outcome[1]))
        for y in (0, 1):
            distribution[y] += p_l1 * outcome[y]
        value += p_l1 * (request.loss.second(a1, l1, a2) +
                         sum((request.loss.terminal(a1, l1, a2, y) * outcome[y]
                              for y in (0, 1)), F(0)))
    if missing:
        return SECOND_STAGE_FAILURE, (), None, (), tuple(missing)
    return POLICY_IDENTIFIED, tuple(distribution), value, tuple(rows), ()


def produce_policy(request):
    """Producer: propose a policy-specific g-formula result."""
    need(type(request) is PolicyRequest, "policy request required")
    if request.query_kind != POLICY_QUERY_KIND:
        return PolicyEvidence(request, UNSUPPORTED_QUERY)
    status, distribution, value, rows, missing = _producer_policy(request)
    subject_status = None
    if status == POLICY_IDENTIFIED:
        subject_status = (FULL_SUBJECT if full_subject_support(request.observation)
                          else POLICY_ONLY)
    return PolicyEvidence(request, status, distribution, value, rows, missing,
                          subject_status)


def _receiver_policy(request):
    """Receiver-only cell-index recomputation of support, law, and value."""
    obs, policy, loss = request.observation, request.policy, request.loss
    a = policy.first_action
    first = sum(obs.masses[8 * a:8 * a + 8], F(0))
    if first == 0:
        return FIRST_STAGE_FAILURE, (), None, (), ((a,),)
    output = [F(0), F(0)]
    terms, missing = [], []
    total_loss = loss.first_stage_costs[a]
    for l in (0, 1):
        offset = 8 * a + 4 * l
        history_mass = sum(obs.masses[offset:offset + 4], F(0))
        if history_mass == 0:
            continue
        history_probability = history_mass / first
        action = policy.second_actions[2 * a + l]
        cell = offset + 2 * action
        action_mass = obs.masses[cell] + obs.masses[cell + 1]
        if action_mass == 0:
            missing.append((a, l, action))
            continue
        p0 = obs.masses[cell] / action_mass
        p1 = obs.masses[cell + 1] / action_mass
        terms.append((l, history_probability, action, p0, p1))
        output[0] += history_probability * p0
        output[1] += history_probability * p1
        terminal = loss.terminal_losses[cell] * p0 + loss.terminal_losses[cell + 1] * p1
        total_loss += history_probability * (
            loss.second_stage_costs[4 * a + 2 * l + action] + terminal)
    if missing:
        return SECOND_STAGE_FAILURE, (), None, (), tuple(missing)
    return POLICY_IDENTIFIED, tuple(output), total_loss, tuple(terms), ()


def consume_policy(expected, evidence):
    """Receiver: bind and independently verify a policy-specific result."""
    need(type(expected) is PolicyRequest and type(evidence) is PolicyEvidence,
         "policy request and evidence required")
    need(evidence.request == expected,
         "stale observation, population, coding, temporal order, premise, policy, cost, loss, support query, or causal query")
    if expected.query_kind != POLICY_QUERY_KIND:
        need(evidence.status == UNSUPPORTED_QUERY and not evidence.distribution and
             evidence.value is None and not evidence.stratum_terms and
             not evidence.missing_histories and evidence.full_subject_status is None,
             "unsupported longitudinal query received a result")
        return {"status": UNSUPPORTED_QUERY,
                "unsupported_query_kind": expected.query_kind}
    status, distribution, value, rows, missing = _receiver_policy(expected)
    need(evidence.status == status, "false longitudinal policy status")
    need(evidence.missing_histories == missing, "false policy support claim")
    if status != POLICY_IDENTIFIED:
        need(not evidence.distribution and evidence.value is None and
             not evidence.stratum_terms and evidence.full_subject_status is None,
             "positivity failure cannot carry an identified policy result")
        return {"status": status, "missing_histories": missing,
                "checked": "support boundary; no zero effect or incompatibility claim"}
    expected_subject_status = (FULL_SUBJECT if
                               full_subject_support(expected.observation)
                               else POLICY_ONLY)
    need(evidence.distribution == distribution and evidence.value == value and
         evidence.stratum_terms == rows,
         "false longitudinal g-formula distribution or value")
    need(evidence.full_subject_status == expected_subject_status,
         "policy-specific and full-subject support were conflated")
    need(len(distribution) == 2 and sum(distribution, F(0)) == 1 and
         all(type(item) is F and 0 <= item <= 1 for item in distribution),
         "invalid identified binary regime distribution")
    return {"status": status, "distribution": distribution, "value": value,
            "full_subject_status": expected_subject_status,
            "premise_identities": premise_identities(expected.premises),
            "supplied_boundary": SUPPLIED_BOUNDARY}


def static_second_stage_distribution(observation, action):
    """One-stage do(A2=action) margin, retaining the natural A1,L1 mix.

    This deliberately discards history-stratified response information and is
    provided only for the mandatory insufficiency counterexample.
    """
    need(type(observation) is LongitudinalObservation, "observation required")
    need(type(action) is int and type(action) is not bool and action in (0, 1),
         "binary second-stage intervention required")
    answer = [F(0), F(0)]
    for a1, l1 in product((0, 1), repeat=2):
        history_mass = _marginal_a1_l1(observation, a1, l1)
        if history_mass == 0:
            continue
        support = _marginal_a1_l1_a2(observation, a1, l1, action)
        need(support > 0, "static A2 intervention lacks positivity")
        for y in (0, 1):
            answer[y] += (history_mass *
                          observation.mass(a1, l1, action, y) / support)
    need(sum(answer, F(0)) == 1, "static intervention did not normalize")
    return tuple(answer)


def complete_policies():
    """All 32 complete policies; off-root histories are never quotiented."""
    answer = []
    for a1 in (0, 1):
        for actions in product((0, 1), repeat=4):
            suffix = "".join(str(action) for action in actions)
            answer.append(DynamicPolicy(f"policy-a1-{a1}-a2-{suffix}",
                                        a1, actions))
    return tuple(answer)


@dataclass(frozen=True)
class BridgeRequest:
    observation: LongitudinalObservation
    premises: SequentialCausalPremises
    loss: LongitudinalLoss
    deployment_population_identity: str
    subject_identity: str
    policy_catalogue_identity: str
    support_query_identity: str
    query_identity: str
    query_kind: str = BRIDGE_QUERY_KIND

    def __post_init__(self):
        need(type(self.observation) is LongitudinalObservation and
             type(self.premises) is SequentialCausalPremises and
             type(self.loss) is LongitudinalLoss,
             "complete full-subject bridge request required")
        for value in (self.deployment_population_identity,
                      self.subject_identity, self.policy_catalogue_identity,
                      self.support_query_identity, self.query_identity,
                      self.query_kind):
            identity(value, "explicit bridge identities required")
        need(self.deployment_population_identity ==
             self.observation.population_identity,
             "first bridge profile does not supply population transport")


@dataclass(frozen=True)
class BridgePolicyRow:
    policy: DynamicPolicy
    distribution: tuple
    causal_value: F
    sequential_policy: sequential.Policy
    sequential_certificate: sequential.Certificate

    def __post_init__(self):
        need(type(self.policy) is DynamicPolicy and
             type(self.sequential_policy) is sequential.Policy and
             type(self.sequential_certificate) is sequential.Certificate,
             "complete causal and sequential policy evidence required")
        object.__setattr__(self, "distribution", tuple(self.distribution))
        need(len(self.distribution) == 2 and
             all(type(value) is F for value in self.distribution),
             "exact binary policy distribution required")
        exact(self.causal_value, "exact causal policy value required")


@dataclass(frozen=True)
class BridgeEvidence:
    request: BridgeRequest
    status: str
    subject_status: object
    subject: object = None
    policy_rows: tuple = ()
    causal_minimizers: tuple = ()
    sequential_minimizers: tuple = ()
    supplied_boundary: str = SUPPLIED_BOUNDARY

    def __post_init__(self):
        need(type(self.request) is BridgeRequest,
             "bridge request binding required")
        need(self.status in (BRIDGE_CHECKED, POLICY_ONLY, UNSUPPORTED_QUERY),
             "invalid bridge status")
        need(self.subject_status in (None, FULL_SUBJECT, POLICY_ONLY),
             "invalid bridge subject status")
        object.__setattr__(self, "policy_rows", tuple(self.policy_rows))
        object.__setattr__(self, "causal_minimizers",
                           tuple(self.causal_minimizers))
        object.__setattr__(self, "sequential_minimizers",
                           tuple(self.sequential_minimizers))
        need(self.supplied_boundary == SUPPLIED_BOUNDARY,
             "causal/empirical boundary changed")


def _subject_premises(request):
    coding = request.observation.coding
    encoded_coding = tuple(
        f"coding:{variable.identity}:{variable.values[0]}|{variable.values[1]}"
        for variable in (coding.first_action, coding.intermediate,
                         coding.second_action, coding.outcome))
    p = request.premises
    return (
        "identified-two-stage-longitudinal-causal-subject",
        f"observation:{request.observation.identity}",
        f"population:{request.observation.population_identity}",
        f"temporal-order:{request.observation.temporal_order.identity}",
        *encoded_coding,
        f"premise-bundle:{p.identity}",
        f"consistency:{p.consistency_identity}",
        f"intervention:{p.intervention_identity}",
        f"first-exchangeability:{p.first_stage_exchangeability_identity}",
        f"second-exchangeability:{p.second_stage_exchangeability_identity}",
        f"adapted-policy:{p.adapted_policy_identity}",
        f"no-interference:{p.no_interference_identity}",
        f"loss:{request.loss.identity}",
        f"catalogue:{request.policy_catalogue_identity}",
    )


def premise_identities(premises):
    """Expose every supplied causal-premise identity without validating truth."""
    need(type(premises) is SequentialCausalPremises,
         "sequential causal premises required")
    return {
        "bundle": premises.identity,
        "consistency": premises.consistency_identity,
        "intervention": premises.intervention_identity,
        "first_stage_exchangeability":
            premises.first_stage_exchangeability_identity,
        "second_stage_exchangeability":
            premises.second_stage_exchangeability_identity,
        "adapted_policy": premises.adapted_policy_identity,
        "no_interference": premises.no_interference_identity,
        "empirically_validated": False,
    }


def _producer_subject(request):
    observation, loss = request.observation, request.loss
    coding = observation.coding
    nodes = []
    root_actions = []
    for a1 in (0, 1):
        first = _marginal_a1(observation, a1)
        outcomes = tuple((f"{coding.intermediate.identity}={l1}",
                          _marginal_a1_l1(observation, a1, l1) / first)
                         for l1 in (0, 1))
        root_actions.append(sequential.Action(
            f"{coding.first_action.identity}={a1}",
            loss.first_stage_costs[a1], outcomes))
    nodes.append(sequential.Node((), actions=tuple(root_actions)))
    for a1, l1 in product((0, 1), repeat=2):
        history = ((f"{coding.first_action.identity}={a1}",
                    f"{coding.intermediate.identity}={l1}"),)
        actions = []
        for a2 in (0, 1):
            support = _marginal_a1_l1_a2(observation, a1, l1, a2)
            outcomes = tuple((f"{coding.outcome.identity}={y}",
                              observation.mass(a1, l1, a2, y) / support)
                             for y in (0, 1))
            actions.append(sequential.Action(
                f"{coding.second_action.identity}={a2}",
                loss.second(a1, l1, a2), outcomes))
        nodes.append(sequential.Node(history, actions=tuple(actions)))
    for a1, l1, a2, y in product((0, 1), repeat=4):
        history = (
            (f"{coding.first_action.identity}={a1}",
             f"{coding.intermediate.identity}={l1}"),
            (f"{coding.second_action.identity}={a2}",
             f"{coding.outcome.identity}={y}"),
        )
        nodes.append(sequential.Node(
            history, terminal=loss.terminal(a1, l1, a2, y)))
    return sequential.Subject(request.subject_identity, 2, loss.unit,
                              _subject_premises(request), tuple(nodes))


def _receiver_subject(request):
    """Receiver construction using direct slices rather than producer helpers."""
    obs, loss, coding = request.observation, request.loss, request.observation.coding
    root = []
    for a in (0, 1):
        base = 8 * a
        total = sum(obs.masses[base:base + 8], F(0))
        probabilities = []
        for l in (0, 1):
            offset = base + 4 * l
            probabilities.append((f"{coding.intermediate.identity}={l}",
                                  sum(obs.masses[offset:offset + 4], F(0)) / total))
        root.append(sequential.Action(f"{coding.first_action.identity}={a}",
                                      loss.first_stage_costs[a], probabilities))
    nodes = [sequential.Node((), actions=root)]
    for a, l in product((0, 1), repeat=2):
        h = ((f"{coding.first_action.identity}={a}",
              f"{coding.intermediate.identity}={l}"),)
        menu = []
        for second in (0, 1):
            cell = 8 * a + 4 * l + 2 * second
            denominator = obs.masses[cell] + obs.masses[cell + 1]
            row = ((f"{coding.outcome.identity}=0", obs.masses[cell] / denominator),
                   (f"{coding.outcome.identity}=1", obs.masses[cell + 1] / denominator))
            menu.append(sequential.Action(
                f"{coding.second_action.identity}={second}",
                loss.second_stage_costs[4 * a + 2 * l + second], row))
        nodes.append(sequential.Node(h, actions=menu))
    for a, l, second, y in product((0, 1), repeat=4):
        h = ((f"{coding.first_action.identity}={a}",
              f"{coding.intermediate.identity}={l}"),
             (f"{coding.second_action.identity}={second}",
              f"{coding.outcome.identity}={y}"))
        nodes.append(sequential.Node(
            h, terminal=loss.terminal_losses[8 * a + 4 * l + 2 * second + y]))
    return sequential.Subject(request.subject_identity, 2, loss.unit,
                              _subject_premises(request), nodes)


def to_sequential_policy(subject, policy, coding):
    need(type(subject) is sequential.Subject and
         type(policy) is DynamicPolicy and type(coding) is LongitudinalCoding,
         "subject, dynamic policy, and coding required")
    choices = [((), f"{coding.first_action.identity}={policy.first_action}")]
    for a1, l1 in product((0, 1), repeat=2):
        history = ((f"{coding.first_action.identity}={a1}",
                    f"{coding.intermediate.identity}={l1}"),)
        choices.append((history,
                        f"{coding.second_action.identity}={policy.second(a1, l1)}"))
    result = sequential.Policy(choices)
    result.validate(subject)
    return result


def _policy_request(bridge, policy):
    return PolicyRequest(
        bridge.observation, bridge.premises, bridge.loss, policy,
        bridge.deployment_population_identity, bridge.support_query_identity,
        bridge.query_identity + ":" + policy.identity)


def produce_bridge(request):
    """Producer: construct the subject and propose all 32 checked policies."""
    need(type(request) is BridgeRequest, "bridge request required")
    if request.query_kind != BRIDGE_QUERY_KIND:
        return BridgeEvidence(request, UNSUPPORTED_QUERY, None)
    if not full_subject_support(request.observation):
        return BridgeEvidence(request, POLICY_ONLY, POLICY_ONLY)
    subject = _producer_subject(request)
    rows = []
    for policy in complete_policies():
        policy_evidence = produce_policy(_policy_request(request, policy))
        need(policy_evidence.status == POLICY_IDENTIFIED,
             "full support failed to identify one catalogue policy")
        seq_policy = to_sequential_policy(subject, policy,
                                          request.observation.coding)
        certificate = sequential.produce(subject, seq_policy)
        rows.append(BridgePolicyRow(
            policy, policy_evidence.distribution, policy_evidence.value,
            seq_policy, certificate))
    best_causal = min(row.causal_value for row in rows)
    causal_minimizers = tuple(row.policy.identity for row in rows
                              if row.causal_value == best_causal)
    seq_values = tuple(row.sequential_certificate.upper[0] for row in rows)
    best_sequential = min(seq_values)
    sequential_minimizers = tuple(row.policy.identity for row, value in
                                  zip(rows, seq_values)
                                  if value == best_sequential)
    return BridgeEvidence(request, BRIDGE_CHECKED, FULL_SUBJECT, subject,
                          tuple(rows), causal_minimizers,
                          sequential_minimizers)


def _distribution_from_paths(subject, policy, outcome_identity):
    result = [F(0), F(0)]
    for history, mass, _ in sequential.paths(subject, policy):
        final_observation = history[-1][1]
        for y in (0, 1):
            if final_observation == f"{outcome_identity}={y}":
                result[y] += mass
    need(sum(result, F(0)) == 1, "complete Bellman path distribution required")
    return tuple(result)


def consume_bridge(expected, evidence):
    """Receiver: reconstruct every transition and check every complete policy."""
    need(type(expected) is BridgeRequest and type(evidence) is BridgeEvidence,
         "bridge request and evidence required")
    need(evidence.request == expected,
         "stale observation, population, coding, temporal order, premise, loss, catalogue, support query, sequential query, or subject identity")
    if expected.query_kind != BRIDGE_QUERY_KIND:
        need(evidence.status == UNSUPPORTED_QUERY and
             evidence.subject_status is None and evidence.subject is None and
             not evidence.policy_rows and not evidence.causal_minimizers and
             not evidence.sequential_minimizers,
             "unsupported bridge query received a result")
        return {"status": UNSUPPORTED_QUERY,
                "unsupported_query_kind": expected.query_kind}
    if not full_subject_support(expected.observation):
        need(evidence.status == evidence.subject_status == POLICY_ONLY and
             evidence.subject is None and not evidence.policy_rows and
             not evidence.causal_minimizers and not evidence.sequential_minimizers,
             "unsupported full subject was presented as identified")
        return {"status": POLICY_ONLY,
                "checked": "individual policy results may remain separately identifiable"}
    subject = _receiver_subject(expected)
    need(evidence.status == BRIDGE_CHECKED and
         evidence.subject_status == FULL_SUBJECT and
         evidence.subject == subject,
         "false or stale completed sequential subject")
    policies = complete_policies()
    need(len(evidence.policy_rows) == len(policies) == 32,
         "complete 32-policy catalogue required")
    observed_causal = []
    observed_sequential = []
    for expected_policy, row in zip(policies, evidence.policy_rows):
        need(type(row) is BridgePolicyRow and row.policy == expected_policy,
             "missing, reordered, or changed complete policy")
        policy_request = _policy_request(expected, expected_policy)
        status, distribution, value, _, missing = _receiver_policy(policy_request)
        need(status == POLICY_IDENTIFIED and not missing,
             "full subject has an unidentified policy")
        seq_policy = to_sequential_policy(subject, expected_policy,
                                          expected.observation.coding)
        need(row.distribution == distribution and row.causal_value == value and
             row.sequential_policy == seq_policy,
             "causal policy row mismatch")
        checked = sequential.consume(subject, seq_policy,
                                     row.sequential_certificate)
        path_value = sequential.path_cost(subject, seq_policy)
        path_distribution = _distribution_from_paths(
            subject, seq_policy, expected.observation.coding.outcome.identity)
        need(checked["policy_upper"] == path_value == value,
             "g-formula and Bellman complete-path values disagree")
        need(path_distribution == distribution,
             "g-formula and Bellman path distributions disagree")
        observed_causal.append(value)
        observed_sequential.append(path_value)
    causal_best = min(observed_causal)
    sequential_best = min(observed_sequential)
    causal_minimizers = tuple(policy.identity for policy, value in
                              zip(policies, observed_causal)
                              if value == causal_best)
    sequential_minimizers = tuple(policy.identity for policy, value in
                                  zip(policies, observed_sequential)
                                  if value == sequential_best)
    need(evidence.causal_minimizers == causal_minimizers and
         evidence.sequential_minimizers == sequential_minimizers and
         causal_minimizers == sequential_minimizers,
         "causal and sequential complete minimizing sets disagree")
    return {"status": BRIDGE_CHECKED, "subject_status": FULL_SUBJECT,
            "policies_checked": 32, "nodes_checked": len(subject.nodes),
            "complete_minimizing_set": causal_minimizers,
            "minimum_value": causal_best,
            "premise_identities": premise_identities(expected.premises),
            "supplied_boundary": SUPPLIED_BOUNDARY}


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
