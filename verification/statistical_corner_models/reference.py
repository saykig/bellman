"""Exact composition of statistical rectangles with persistent corner families.

This bounded reference reuses the PR14 coverage receiver and the PR8 exact
persistent-family receiver.  It supports one or two named Bernoulli parameters,
parameter-independent costs, and affine binary transition laws.  A corner
family is constructed only when no parameter occurs in two transition factors
on one complete skeleton path.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from verification.multistream_collection import reference as statistics  # noqa: E402
from verification.persistent_model_families import families  # noqa: E402


r = families.r
EXACT_WARRANT = "exact-multi-affine-corner-reduction"
INVALID_WARRANT = "invalid-corner-reduction-warrant"
QUERY = "whole-policy-cost-and-regret-over-statistical-rectangle"
MAX_PARAMETERS = 2
MAX_CORNERS = 4
AUDIT_SUBDIVISIONS = 16


Invalid = r.Invalid


def need(condition, message):
    if not condition:
        raise Invalid(message)


def identity(value, message="nonempty identity required"):
    need(type(value) is str and bool(value), message)
    return value


def exact(value, message="exact Fraction required"):
    need(type(value) is F, message)
    r.q(value)
    return value


def unfinished(reason, limit, requested):
    return {"status": "unfinished", "kind": "resource-refusal",
            "reason": reason, "limit": limit, "requested": requested}


@dataclass(frozen=True)
class OutcomeLaw:
    observation: str
    intercept: F
    coefficient: F = F(0)
    parameter_identity: object = None

    def validate(self):
        identity(self.observation, "nonempty observation label required")
        exact(self.intercept, "exact outcome intercept required")
        exact(self.coefficient, "exact outcome coefficient required")
        need(self.parameter_identity is None or
             (type(self.parameter_identity) is str and self.parameter_identity),
             "parameter identity must be absent or nonempty")
        need((self.parameter_identity is None) == (self.coefficient == 0),
             "parameter identity and nonzero coefficient must occur together")
        return self


def outcome(observation, intercept, coefficient=0, parameter=None):
    return OutcomeLaw(observation, r.q(intercept), r.q(coefficient), parameter).validate()


@dataclass(frozen=True)
class ActionSpec:
    label: str
    cost: F
    outcomes: tuple = ()

    def __post_init__(self):
        object.__setattr__(self, "outcomes", tuple(self.outcomes))

    def validate(self, parameters):
        identity(self.label, "nonempty action label required")
        exact(self.cost, "exact parameter-independent action cost required")
        need(len(self.outcomes) <= 4 and
             all(type(row) is OutcomeLaw for row in self.outcomes),
             "zero to four typed outcome laws required")
        for row in self.outcomes:
            row.validate()
        labels = tuple(row.observation for row in self.outcomes)
        need(len(set(labels)) == len(labels), "duplicate outcome label")
        dependent = tuple(row for row in self.outcomes
                          if row.parameter_identity is not None)
        if dependent:
            ids = {row.parameter_identity for row in dependent}
            need(len(self.outcomes) == 2 and len(dependent) == 2 and len(ids) == 1,
                 "a parameter-dependent transition must be one binary affine law")
            parameter = next(iter(ids))
            need(parameter in parameters, "transition uses an undeclared parameter")
            need(sum((row.intercept for row in self.outcomes), F(0)) == 1 and
                 sum((row.coefficient for row in self.outcomes), F(0)) == 0,
                 "affine Bernoulli probabilities must normalize identically")
            for endpoint in (F(0), F(1)):
                need(all(0 <= row.intercept + row.coefficient * endpoint <= 1
                         for row in self.outcomes),
                     "affine transition is not a probability on [0,1]")
        elif self.outcomes:
            need(sum((row.intercept for row in self.outcomes), F(0)) == 1,
                 "fixed transition probabilities must normalize")
            need(all(0 <= row.intercept <= 1 for row in self.outcomes),
                 "fixed transition probability outside [0,1]")
        return self


def action(label, cost, outcomes=()):
    return ActionSpec(label, r.q(cost), tuple(outcomes))


@dataclass(frozen=True)
class NodeSpec:
    history: tuple
    terminal: F = F(0)
    actions: tuple = ()

    def __post_init__(self):
        object.__setattr__(self, "history", r.history(self.history))
        object.__setattr__(self, "actions", tuple(self.actions))

    def validate(self, parameters):
        exact(self.terminal, "exact parameter-independent terminal cost required")
        need(all(type(item) is ActionSpec for item in self.actions),
             "typed action specifications required")
        for item in self.actions:
            item.validate(parameters)
        labels = tuple(item.label for item in self.actions)
        need(len(labels) <= 4 and len(set(labels)) == len(labels),
             "action menu must contain at most four unique labels")
        need(not self.actions or self.terminal == 0,
             "terminal cost is permitted only at a terminal node")
        return self


def node(history, terminal=0, actions=()):
    return NodeSpec(history, r.q(terminal), tuple(actions))


@dataclass(frozen=True)
class Template:
    identity: str
    horizon: int
    unit: str
    premises: tuple
    parameters: tuple
    nodes: tuple

    def __post_init__(self):
        object.__setattr__(self, "premises", tuple(self.premises))
        object.__setattr__(self, "parameters", tuple(self.parameters))
        object.__setattr__(self, "nodes", tuple(self.nodes))

    def validate(self):
        identity(self.identity, "nonempty template identity required")
        identity(self.unit, "nonempty loss unit required")
        need(type(self.horizon) is int and type(self.horizon) is not bool,
             "strict integer horizon required")
        need(all(type(item) is str for item in self.premises),
             "immutable string premises required")
        need(bool(self.parameters) and
             all(type(item) is str and item for item in self.parameters),
             "one or more named parameters required")
        need(len(set(self.parameters)) == len(self.parameters),
             "duplicate parameter identity")
        need(bool(self.nodes) and all(type(item) is NodeSpec for item in self.nodes),
             "nonempty typed node skeleton required")
        for item in self.nodes:
            item.validate(set(self.parameters))
        _instantiate(self, {parameter: F(0) for parameter in self.parameters},
                     self.identity)
        return self


def action_parameter(item):
    ids = {row.parameter_identity for row in item.outcomes
           if row.parameter_identity is not None}
    need(len(ids) <= 1, "transition contains more than one parameter")
    return next(iter(ids)) if ids else None


def _instantiate(template, parameter_values, name):
    """Instantiate after structural validation; callers bind/check coordinates."""
    converted = []
    for item in template.nodes:
        actions = []
        for specification in item.actions:
            probabilities = []
            for law in specification.outcomes:
                value = law.intercept
                if law.parameter_identity is not None:
                    value += law.coefficient * parameter_values[law.parameter_identity]
                probabilities.append((law.observation, value))
            actions.append(r.Action(specification.label, specification.cost, probabilities))
        converted.append(r.Node(item.history, item.terminal, actions))
    return r.Subject(name, template.horizon, template.unit, template.premises, converted)


def instantiate(template, parameter_values, name=None):
    template.validate()
    need(type(parameter_values) is dict and
         set(parameter_values) == set(template.parameters),
         "one exact coordinate per declared parameter required")
    values = {}
    for parameter in template.parameters:
        value = exact(parameter_values[parameter], "exact parameter coordinate required")
        need(0 <= value <= 1, "parameter coordinate outside [0,1]")
        values[parameter] = value
    return _instantiate(template, values, name or template.identity)


def template_payload(template):
    template.validate()
    return {
        "identity": template.identity,
        "horizon": template.horizon,
        "unit": template.unit,
        "premises": template.premises,
        "parameters": template.parameters,
        "nodes": tuple((item.history, str(item.terminal), tuple(
            (action.label, str(action.cost), tuple(
                (law.observation, str(law.intercept), str(law.coefficient),
                 law.parameter_identity) for law in action.outcomes))
            for action in item.actions)) for item in template.nodes),
    }


def template_digest(template):
    return statistics.digest_payload(template_payload(template))


@dataclass(frozen=True)
class MappingRow:
    stream_identity: str
    parameter_identity: str

    def __post_init__(self):
        identity(self.stream_identity, "nonempty mapped stream identity required")
        identity(self.parameter_identity, "nonempty mapped parameter identity required")


@dataclass(frozen=True)
class Request:
    collection: statistics.CollectionRequest
    template: Template
    mapping: tuple
    policies: tuple
    named_policy_identity: str
    scope: str
    expected_loss_cap: object = None
    regret_cap: object = None
    query: str = QUERY

    def __post_init__(self):
        object.__setattr__(self, "mapping", tuple(self.mapping))
        object.__setattr__(self, "policies", tuple(self.policies))
        self.validate()

    def validate(self):
        need(type(self.collection) is statistics.CollectionRequest,
             "multistream collection subject required")
        self.collection.validate()
        need(type(self.template) is Template, "parametric sequential template required")
        self.template.validate()
        need(self.query == QUERY, "unsupported rectangle-to-family query")
        need(all(type(row) is MappingRow for row in self.mapping),
             "typed stream-to-parameter mapping required")
        streams = tuple(row.stream_identity for row in self.mapping)
        parameters = tuple(row.parameter_identity for row in self.mapping)
        registry = tuple(row.stream_identity for row in self.collection.registry)
        need(len(streams) == len(set(streams)) and
             len(parameters) == len(set(parameters)),
             "duplicate stream or parameter mapping identity")
        need(set(streams) == set(registry) and len(streams) == len(registry),
             "mapping must cover every and only statistical stream identity")
        need(set(parameters) == set(self.template.parameters) and
             len(parameters) == len(self.template.parameters),
             "mapping must cover every and only transition parameter identity")
        need(self.scope in (families.FULL, families.SUBSET),
             "explicit deterministic policy-class scope required")
        need(bool(self.policies) and
             all(type(item) is families.PolicyEntry for item in self.policies),
             "nonempty explicit deterministic policy class required")
        identity(self.named_policy_identity, "named policy identity required")
        entries = {entry.identity: entry for entry in self.policies}
        need(len(entries) == len(self.policies), "duplicate policy identity")
        need(self.named_policy_identity in entries,
             "named policy must occur in the explicit policy class")
        nominal = instantiate(self.template,
                              {parameter: F(0) for parameter in self.template.parameters})
        for entry in self.policies:
            entry.policy.validate(nominal)
        # Reuse the persistent checker to enforce exact FULL coverage and its budget.
        if len(self.template.parameters) <= MAX_PARAMETERS:
            singleton = families.Family("request-validation", [
                families.Member("nominal", nominal)
            ])
            families.ChoiceRequest(singleton, self.policies, self.scope,
                                   families.MINIMAX_LOSS)
        for value, label in ((self.expected_loss_cap, "expected-loss cap"),
                             (self.regret_cap, "regret cap")):
            need(value is None or type(value) is F,
                 f"{label} must be absent or exact Fraction")
            if value is not None:
                exact(value, f"exact {label} required")
        need(self.regret_cap is None or self.regret_cap >= 0,
             "regret cap must be nonnegative")
        return self


def request_budget(request):
    request.validate()
    count = len(request.template.parameters)
    if count > MAX_PARAMETERS:
        return unfinished("parameter-count-limit", MAX_PARAMETERS, count)
    corners = 2 ** count
    if corners > MAX_CORNERS:
        return unfinished("corner-count-limit", MAX_CORNERS, corners)
    return None


@dataclass(frozen=True)
class PathUse:
    path: tuple
    parameter_uses: tuple
    stop_action: object = None

    def __post_init__(self):
        object.__setattr__(self, "path", r.history(self.path))
        object.__setattr__(self, "parameter_uses", tuple(self.parameter_uses))
        need(all(type(item) is str and item for item in self.parameter_uses),
             "path parameter identities required")
        need(self.stop_action is None or
             (type(self.stop_action) is str and self.stop_action),
             "early-stop action must be absent or identified")


def complete_path_uses(template):
    """List structural paths, including early STOP leaves, and factor identities."""
    template.validate()
    by_history = {item.history: item for item in template.nodes}
    complete = [(item.history, None) for item in template.nodes if not item.actions]
    for item in template.nodes:
        for specification in item.actions:
            if not specification.outcomes:
                complete.append((item.history, specification.label))
    rows = []
    for path, stop_action in complete:
        uses = []
        cursor = ()
        for label, observation in path:
            specification = next(action for action in by_history[cursor].actions
                                 if action.label == label)
            parameter = action_parameter(specification)
            if parameter is not None:
                uses.append(parameter)
            cursor += ((label, observation),)
        rows.append(PathUse(path, tuple(uses), stop_action))
    return tuple(rows)


def admissible(path_uses):
    return all(len(set(row.parameter_uses)) == len(row.parameter_uses)
               for row in path_uses)


def parameter_locations(template):
    template.validate()
    locations = {parameter: [] for parameter in template.parameters}
    for item in template.nodes:
        for specification in item.actions:
            parameter = action_parameter(specification)
            if parameter is not None:
                locations[parameter].append((item.history, specification.label))
    return {parameter: tuple(rows) for parameter, rows in locations.items()}


def mapped_rectangle(request, checked_coverage):
    by_stream = {stream: (lower, upper)
                 for stream, lower, upper in checked_coverage["rectangle"]}
    stream_for_parameter = {row.parameter_identity: row.stream_identity
                            for row in request.mapping}
    return tuple((parameter, *by_stream[stream_for_parameter[parameter]])
                 for parameter in request.template.parameters)


def corner_coordinates(rectangle):
    rows = []
    for coordinates in product(*(bounds[1:] for bounds in rectangle)):
        point = tuple((rectangle[index][0], value)
                      for index, value in enumerate(coordinates))
        if point not in rows:
            rows.append(point)
    return tuple(rows)


def construct_family(request, coordinates):
    members = []
    for index, point in enumerate(coordinates, 1):
        values = dict(point)
        subject = instantiate(request.template, values,
                              f"{request.template.identity} corner {index}")
        members.append(families.Member(f"corner-{index}", subject))
    return families.Family(f"{request.template.identity} statistical corners", members)


def direct_value(template, policy, parameters):
    """Independent complete-path sum; does not instantiate or use Bellman backups."""
    template.validate()
    subject = _instantiate(template, parameters, template.identity)
    chosen = policy.validate(subject)
    nodes = {item.history: item for item in template.nodes}
    pending = [((), F(1), F(0))]
    total = F(0)
    final_mass = F(0)
    while pending:
        history, mass, paid = pending.pop()
        item = nodes[history]
        if not item.actions:
            total += mass * (paid + item.terminal)
            final_mass += mass
            continue
        specification = next(action for action in item.actions
                             if action.label == chosen[history])
        if not specification.outcomes:
            total += mass * (paid + specification.cost)
            final_mass += mass
            continue
        for law in specification.outcomes:
            probability = law.intercept
            if law.parameter_identity is not None:
                probability += law.coefficient * parameters[law.parameter_identity]
            if probability:
                pending.append((history + ((specification.label, law.observation),),
                                mass * probability, paid + specification.cost))
    need(final_mass == 1, "independent complete-path mass does not sum to one")
    return total


@dataclass(frozen=True)
class BoundaryEvidence:
    request: Request
    coverage_evidence: statistics.CoverageEvidence
    path_uses: tuple
    status: str = INVALID_WARRANT

    def __post_init__(self):
        object.__setattr__(self, "path_uses", tuple(self.path_uses))


@dataclass(frozen=True)
class Evidence:
    request: Request
    coverage_evidence: statistics.CoverageEvidence
    path_uses: tuple
    rectangle: tuple
    coordinates: tuple
    family: families.Family
    loss_evidence: families.ChoiceEvidence
    regret_evidence: object
    warrant: str = EXACT_WARRANT

    def __post_init__(self):
        object.__setattr__(self, "path_uses", tuple(self.path_uses))
        object.__setattr__(self, "rectangle", tuple(tuple(row) for row in self.rectangle))
        object.__setattr__(self, "coordinates",
                           tuple(tuple(tuple(row) for row in point)
                                 for point in self.coordinates))


def produce(request, coverage_evidence):
    """Candidate construction. Receiving performs every substantive check again."""
    request.validate()
    refusal = request_budget(request)
    if refusal:
        return refusal
    checked = statistics.consume_coverage(request.collection, coverage_evidence)
    if checked.get("status") == "unfinished":
        return checked
    paths = complete_path_uses(request.template)
    if not admissible(paths):
        return BoundaryEvidence(request, coverage_evidence, paths)
    rectangle = mapped_rectangle(request, checked)
    coordinates = corner_coordinates(rectangle)
    family = construct_family(request, coordinates)
    loss_request = families.ChoiceRequest(
        family, request.policies, request.scope, families.MINIMAX_LOSS)
    loss_evidence = families.choose(loss_request)
    regret_evidence = None
    if request.scope == families.FULL:
        regret_request = families.ChoiceRequest(
            family, request.policies, request.scope, families.MINIMAX_REGRET)
        regret_evidence = families.choose(regret_request)
    return Evidence(request, coverage_evidence, paths, rectangle, coordinates,
                    family, loss_evidence, regret_evidence)


def grid(rectangle):
    axes = []
    for _, lower, upper in rectangle:
        axes.append(tuple(lower + (upper - lower) * F(index, AUDIT_SUBDIVISIONS)
                          for index in range(AUDIT_SUBDIVISIONS + 1)))
    return tuple(tuple((rectangle[index][0], value)
                       for index, value in enumerate(coordinates))
                 for coordinates in product(*axes))


def _class_values(matrix):
    comparators = tuple(min(row) for row in matrix)
    regrets = tuple(tuple(value - comparators[index] for value in row)
                    for index, row in enumerate(matrix))
    return comparators, regrets


def consume(expected, evidence):
    """Check evidence, admissibility, corners, exact family, and path oracle."""
    expected.validate()
    refusal = request_budget(expected)
    if refusal:
        need(evidence == refusal, "wrong out-of-profile refusal")
        return refusal
    need(type(evidence) in (Evidence, BoundaryEvidence),
         "corner-composition or boundary evidence required")
    evidence.request.validate()
    need(evidence.request == expected, "stale statistics, mapping, model, loss or policy")
    coverage = statistics.consume_coverage(expected.collection,
                                           evidence.coverage_evidence)
    need(coverage.get("status") != "unfinished",
         "unexpected in-profile coverage refusal")
    paths = complete_path_uses(expected.template)
    need(evidence.path_uses == paths, "false or incomplete structural path-use claim")
    if not admissible(paths):
        need(type(evidence) is BoundaryEvidence and evidence.status == INVALID_WARRANT,
             "inadmissible subject received an exact corner warrant")
        repeated = tuple((row.path, row.stop_action, row.parameter_uses) for row in paths
                         if len(set(row.parameter_uses)) < len(row.parameter_uses))
        return {
            "status": INVALID_WARRANT,
            "statistical_evidence_status": coverage["status"],
            "mapped_rectangle": mapped_rectangle(expected, coverage),
            "repeated_parameter_paths": repeated,
            "sequential_model_status": "valid-at-each-specified-parameter-point",
            "required_next_method": "optimization-other-than-exact-corner-reduction",
            "mathematical_impossibility_claimed": False,
        }

    need(type(evidence) is Evidence and evidence.warrant == EXACT_WARRANT,
         "admissible subject lacks exact corner evidence")
    rectangle = mapped_rectangle(expected, coverage)
    coordinates = corner_coordinates(rectangle)
    family = construct_family(expected, coordinates)
    need(evidence.rectangle == rectangle and evidence.coordinates == coordinates,
         "false mapped rectangle or corner coordinates")
    need(evidence.family == family, "corner family not reconstructed from intended subject")

    loss_request = families.ChoiceRequest(
        family, expected.policies, expected.scope, families.MINIMAX_LOSS)
    loss_answer = families.consume_choice(loss_request, evidence.loss_evidence)
    regret_answer = None
    if expected.scope == families.FULL:
        need(type(evidence.regret_evidence) is families.ChoiceEvidence,
             "complete-class regret evidence required")
        regret_request = families.ChoiceRequest(
            family, expected.policies, expected.scope, families.MINIMAX_REGRET)
        regret_answer = families.consume_choice(regret_request,
                                                evidence.regret_evidence)
        need(regret_answer["matrix"] == loss_answer["matrix"],
             "loss and regret evidence disagree on exact policy matrix")
    else:
        need(evidence.regret_evidence is None,
             "subset evidence must not claim complete-class minimax regret")

    matrix = loss_answer["matrix"]
    direct_matrix = tuple(tuple(direct_value(expected.template, entry.policy,
                                             dict(point))
                                for entry in expected.policies)
                          for point in coordinates)
    need(matrix == direct_matrix,
         "persistent-family values disagree with independent complete paths")
    class_comparators, class_regrets = _class_values(matrix)
    named_index = next(index for index, entry in enumerate(expected.policies)
                       if entry.identity == expected.named_policy_identity)
    named_costs = tuple(row[named_index] for row in matrix)
    named_regrets = tuple(row[named_index] for row in class_regrets)
    worst_cost, worst_regret = max(named_costs), max(named_regrets)

    audit_points = grid(rectangle)
    audit_matrix = tuple(tuple(direct_value(expected.template, entry.policy,
                                            dict(point))
                               for entry in expected.policies)
                         for point in audit_points)
    audit_worst_costs = tuple(max(row[index] for row in audit_matrix)
                              for index in range(len(expected.policies)))
    audit_regrets = []
    for row in audit_matrix:
        optimum = min(row)
        audit_regrets.append(tuple(value - optimum for value in row))
    audit_worst_regrets = tuple(max(row[index] for row in audit_regrets)
                                for index in range(len(expected.policies)))
    corner_worst_costs = tuple(max(row[index] for row in matrix)
                               for index in range(len(expected.policies)))
    corner_worst_regrets = tuple(max(row[index] for row in class_regrets)
                                 for index in range(len(expected.policies)))
    need(audit_worst_costs == corner_worst_costs and
         audit_worst_regrets == corner_worst_regrets,
         "independent rational interior audit disagrees with corners")

    full = expected.scope == families.FULL
    if full:
        loss_winners = loss_answer["winners"]
        regret_winners = regret_answer["winners"]
        need(corner_worst_regrets == regret_answer["worst_regrets"],
             "covered-class regret differs from persistent-family comparator")
    else:
        loss_winners = regret_winners = None
    locations = parameter_locations(expected.template)
    exclusive_reuse = tuple(parameter for parameter, rows in locations.items()
                            if len(rows) > 1)

    return {
        "status": "checked-statistical-corner-model-composition",
        "warrant": EXACT_WARRANT,
        "mapped_rectangle": rectangle,
        "corner_coordinates": coordinates,
        "corner_count": len(coordinates),
        "path_count": len(paths),
        "mutually_exclusive_reuse_allowed": bool(exclusive_reuse),
        "mutually_exclusive_reused_parameters": exclusive_reuse,
        "named_policy": expected.named_policy_identity,
        "common_policy_across_corner_models": True,
        "named_corner_costs": named_costs,
        "named_corner_regrets": named_regrets,
        "named_worst_expected_loss": worst_cost,
        "named_worst_regret": worst_regret,
        "expected_loss_cap": expected.expected_loss_cap,
        "expected_loss_cap_met": (None if expected.expected_loss_cap is None else
                                   worst_cost <= expected.expected_loss_cap),
        "regret_cap": expected.regret_cap,
        "regret_cap_met": (None if expected.regret_cap is None else
                            worst_regret <= expected.regret_cap),
        "policy_scope": expected.scope,
        "policy_count": len(expected.policies),
        "minimax_loss_winners": loss_winners,
        "minimax_regret_winners": regret_winners,
        "corner_worst_costs": corner_worst_costs,
        "corner_worst_regrets": corner_worst_regrets,
        "direct_path_matrix_equal": True,
        "rational_interior_audit_points": len(audit_points),
        "rational_interior_audit_equal": True,
        "statistical": {
            "simultaneous_coverage_lower": coverage["simultaneous_coverage_lower"],
            "failure_probability_upper": coverage["allocation_sum"],
            "declared_total_alpha": expected.collection.total_alpha,
            "precision_bits": expected.collection.precision_bits,
            "sampling_premises_supplied_not_empirically_validated": True,
            "outward_rectangle_may_be_conservative": True,
        },
        "composed_guarantee": {
            "rule": ("on-the-simultaneous-coverage-event-any-established-"
                     "rectangle-cap-applies-to-the-true-parameter-vector"),
            "expected_loss_cap_established": (
                None if expected.expected_loss_cap is None else
                worst_cost <= expected.expected_loss_cap),
            "regret_cap_established": (
                None if expected.regret_cap is None else
                worst_regret <= expected.regret_cap),
        },
        "coverage_loss_regret_and_precision_not_combined": True,
        "randomized_policy_claimed": False,
        "corner_probabilities_claimed": False,
        "provenance": {
            "collection_record_identity": expected.collection.record_identity,
            "collection_revision_identity": expected.collection.revision_identity,
            "collection_subject_digest": statistics.collection_digest(expected.collection),
            "template_digest": template_digest(expected.template),
            "mapping": tuple((row.stream_identity, row.parameter_identity)
                             for row in expected.mapping),
        },
    }


def wire(value):
    return statistics.wire(value)
