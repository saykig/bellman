"""Exact unsafe-history reachability and robust deterministic selection.

The bounded reference composes the existing completed observable-history,
persistent-family, and statistical-corner contracts.  Unsafe histories become
absorbing only for the reachability calculation; supplied subjects are never
rewritten.  All probability and cost calculations use exact Fractions.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from verification.statistical_corner_models import reference as corners  # noqa: E402


families = corners.families
statistics = corners.statistics
r = corners.r
Invalid = r.Invalid

REACHABILITY_QUERY = "ever-hit-declared-unsafe-history-set"
FAMILY_QUERY = "worst-unsafe-reachability-over-persistent-family"
SELECTION_QUERY = "robust-safety-constrained-deterministic-policy-selection"
STATISTICAL_QUERY = "statistical-rectangle-unsafe-reachability"
CHECKED = "checked-unsafe-set-reachability"
FAMILY_CHECKED = "checked-persistent-family-unsafe-reachability"
SELECTION_CHECKED = "checked-robust-safety-constrained-selection"
STATISTICAL_CHECKED = "checked-statistical-corner-unsafe-reachability"
INVALID_CORNER_WARRANT = "invalid-corner-reachability-warrant"
NO_FULL_FEASIBLE = "no-deterministic-policy-in-complete-covered-class-satisfies-cap"
NO_SUPPLIED_FEASIBLE = "no-supplied-policy-satisfies-cap"


def need(condition, message):
    if not condition:
        raise Invalid(message)


def identity(value, message="nonempty identity required"):
    need(type(value) is str and bool(value), message)
    return value


def exact(value, message="exact Fraction required"):
    need(type(value) is F, message)
    return value


def probability(value, message="exact probability required"):
    exact(value, message)
    need(0 <= value <= 1, message)
    return value


@dataclass(frozen=True)
class UnsafeSet:
    """An identified subset of the subject's completed observable histories."""

    identity: str
    histories: tuple

    def __post_init__(self):
        identity(self.identity, "nonempty unsafe-set identity required")
        need(type(self.histories) in (tuple, list), "unsafe-history sequence required")
        object.__setattr__(self, "histories",
                           tuple(r.history(history) for history in self.histories))
        need(len(set(self.histories)) == len(self.histories),
             "duplicate unsafe history")

    def validate(self, subject):
        need(type(subject) is r.Subject, "sequential subject required")
        subject.validate()
        known = {node.h for node in subject.nodes}
        need(set(self.histories) <= known,
             "unsafe set contains a history outside the completed skeleton")
        return self


@dataclass(frozen=True)
class ReachabilityRequest:
    subject: r.Subject
    model_identity: str
    policy: r.Policy
    unsafe_set: UnsafeSet
    cap: object = None
    query: str = REACHABILITY_QUERY

    def __post_init__(self):
        self.validate()

    def validate(self):
        need(type(self.subject) is r.Subject and type(self.policy) is r.Policy,
             "subject and one deterministic policy required")
        self.subject.validate()
        self.policy.validate(self.subject)
        identity(self.model_identity, "nonempty model identity required")
        need(type(self.unsafe_set) is UnsafeSet,
             "identified unsafe-history set required")
        self.unsafe_set.validate(self.subject)
        need(self.query == REACHABILITY_QUERY, "unsupported reachability query")
        need(self.cap is None or type(self.cap) is F,
             "cap must be absent or an exact Fraction")
        if self.cap is not None:
            probability(self.cap, "reachability cap must lie in [0,1]")
        return self


@dataclass(frozen=True)
class ReachabilityCertificate:
    request: ReachabilityRequest
    node_values: tuple
    root_probability: F
    cap_met: object

    def __post_init__(self):
        need(type(self.request) is ReachabilityRequest,
             "reachability request binding required")
        object.__setattr__(self, "node_values", r.proof(self.node_values))
        object.__setattr__(self, "root_probability",
                           probability(self.root_probability))
        need(self.cap_met is None or type(self.cap_met) is bool,
             "cap result must be absent or Boolean")


def _producer_values(request):
    """Candidate backward construction.  The receiver does not call this."""
    request.validate()
    unsafe = set(request.unsafe_set.histories)
    selected = request.policy.validate(request.subject)
    values = {}
    for node in sorted(request.subject.nodes, key=lambda item: len(item.h),
                       reverse=True):
        if node.h in unsafe:
            values[node.h] = F(1)
        elif not node.actions:
            values[node.h] = F(0)
        else:
            action = next(item for item in node.actions
                          if item.label == selected[node.h])
            if not action.outcomes:
                values[node.h] = F(0)
            else:
                values[node.h] = sum(
                    (chance * values[node.h + ((action.label, observation),)]
                     for observation, chance in action.outcomes), F(0))
    return values


def produce_reachability(request):
    """Producer: construct an exact nodewise reachability table."""
    values = _producer_values(request)
    root = values[()]
    cap_met = None if request.cap is None else root <= request.cap
    return ReachabilityCertificate(
        request, tuple(values[node.h] for node in request.subject.nodes),
        root, cap_met)


def first_hit_paths(subject, policy, unsafe_set):
    """Independent forward first-hit expansion; unsafe prefixes stop traversal."""
    subject.validate()
    policy.validate(subject)
    unsafe_set.validate(subject)
    selected = dict(policy.choices)
    nodes = {node.h: node for node in subject.nodes}
    pending = [((), F(1))]
    hits = []
    while pending:
        history, mass = pending.pop()
        if history in set(unsafe_set.histories):
            hits.append((history, mass))
            continue
        node = nodes[history]
        if not node.actions:
            continue
        action = next(item for item in node.actions
                      if item.label == selected[history])
        for observation, chance in action.outcomes:
            if chance:
                pending.append((history + ((action.label, observation),),
                                mass * chance))
    total = sum((mass for _, mass in hits), F(0))
    need(0 <= total <= 1, "first-hit mass outside [0,1]")
    return tuple(hits)


def first_hit_probability(subject, policy, unsafe_set):
    return sum((mass for _, mass in first_hit_paths(subject, policy, unsafe_set)),
               F(0))


def node_marginal_sum(subject, policy, unsafe_set):
    """Deliberately non-certificate audit of the unsafe-node summing shortcut."""
    subject.validate()
    selected = policy.validate(subject)
    unsafe_set.validate(subject)
    nodes = {node.h: node for node in subject.nodes}
    masses = {node.h: F(0) for node in subject.nodes}
    masses[()] = F(1)
    for node in sorted(subject.nodes, key=lambda item: len(item.h)):
        if not node.actions:
            continue
        action = next(item for item in node.actions
                      if item.label == selected[node.h])
        for observation, chance in action.outcomes:
            child = node.h + ((action.label, observation),)
            masses[child] += masses[node.h] * chance
    return sum((masses[history] for history in unsafe_set.histories), F(0))


def terminal_only_unsafe_probability(subject, policy, unsafe_set):
    """Deliberately invalid shortcut retained only for the transient-hit control."""
    terminal = {node.h for node in subject.nodes if not node.actions}
    restricted = UnsafeSet(unsafe_set.identity + " terminal-only",
                           tuple(history for history in unsafe_set.histories
                                 if history in terminal))
    return first_hit_probability(subject, policy, restricted)


def consume_reachability(expected, certificate):
    """Receiver: independently check recurrence, first-hit expansion, and cap."""
    need(type(expected) is ReachabilityRequest and
         type(certificate) is ReachabilityCertificate,
         "reachability request and certificate required")
    expected.validate()
    certificate.request.validate()
    need(certificate.request == expected,
         "stale model, policy, unsafe set, cap, or query")
    need(len(certificate.node_values) == len(expected.subject.nodes),
         "complete nodewise reachability table required")
    supplied = dict(zip((node.h for node in expected.subject.nodes),
                        certificate.node_values))
    unsafe = set(expected.unsafe_set.histories)
    selected = expected.policy.validate(expected.subject)
    recomputed = {}
    for node in sorted(expected.subject.nodes, key=lambda item: len(item.h),
                       reverse=True):
        if node.h in unsafe:
            value = F(1)
        elif not node.actions:
            value = F(0)
        else:
            action = next(item for item in node.actions
                          if item.label == selected[node.h])
            value = sum((chance * recomputed[
                node.h + ((action.label, observation),)]
                         for observation, chance in action.outcomes), F(0))
        need(supplied[node.h] == value,
             "false nodewise unsafe-set reachability value")
        recomputed[node.h] = value
    root = recomputed[()]
    need(certificate.root_probability == root,
         "false root unsafe-set reachability probability")
    cap_met = None if expected.cap is None else root <= expected.cap
    need(certificate.cap_met == cap_met, "false reachability-cap result")
    paths = first_hit_paths(expected.subject, expected.policy,
                            expected.unsafe_set)
    need(sum((mass for _, mass in paths), F(0)) == root,
         "backward recurrence disagrees with independent first-hit paths")
    return {
        "status": CHECKED,
        "model_identity": expected.model_identity,
        "subject_identity": expected.subject.name,
        "policy": expected.policy,
        "unsafe_set_identity": expected.unsafe_set.identity,
        "unsafe_histories": expected.unsafe_set.histories,
        "root_probability": root,
        "node_values": tuple(recomputed[node.h]
                             for node in expected.subject.nodes),
        "first_hit_paths": paths,
        "cap": expected.cap,
        "cap_met": cap_met,
        "meaning": "model-implied-probability-of-ever-entering-declared-unsafe-set",
        "empirical_model_validity_established": False,
        "unsafe_set_normative_validity_established": False,
        "authority_to_act_established": False,
    }


@dataclass(frozen=True)
class FamilyReachabilityRequest:
    family: families.Family
    policy: r.Policy
    unsafe_set: UnsafeSet
    cap: F
    query: str = FAMILY_QUERY

    def __post_init__(self):
        self.validate()

    def validate(self):
        need(type(self.family) is families.Family and
             type(self.policy) is r.Policy,
             "persistent family and one common policy required")
        self.family.validate()
        need(type(self.unsafe_set) is UnsafeSet,
             "identified unsafe set required")
        for member in self.family.members:
            self.policy.validate(member.subject)
            self.unsafe_set.validate(member.subject)
        probability(self.cap, "robust reachability cap must lie in [0,1]")
        need(self.query == FAMILY_QUERY, "unsupported family reachability query")
        return self


@dataclass(frozen=True)
class FamilyReachabilityRow:
    member_identity: str
    certificate: ReachabilityCertificate

    def __post_init__(self):
        identity(self.member_identity, "nonempty family member identity required")
        need(type(self.certificate) is ReachabilityCertificate,
             "member reachability certificate required")


@dataclass(frozen=True)
class FamilyReachabilityEvidence:
    request: FamilyReachabilityRequest
    rows: tuple
    worst_probability: F
    robust_cap_met: bool

    def __post_init__(self):
        need(type(self.request) is FamilyReachabilityRequest,
             "family reachability request binding required")
        object.__setattr__(self, "rows", tuple(self.rows))
        need(all(type(row) is FamilyReachabilityRow for row in self.rows),
             "typed family reachability rows required")
        object.__setattr__(self, "worst_probability",
                           probability(self.worst_probability))
        need(type(self.robust_cap_met) is bool,
             "robust cap result must be Boolean")


def produce_family_reachability(request):
    request.validate()
    rows = []
    values = []
    for member in request.family.members:
        local = ReachabilityRequest(member.subject, member.identity,
                                    request.policy, request.unsafe_set,
                                    request.cap)
        certificate = produce_reachability(local)
        rows.append(FamilyReachabilityRow(member.identity, certificate))
        values.append(certificate.root_probability)
    worst = max(values)
    return FamilyReachabilityEvidence(request, rows, worst, worst <= request.cap)


def consume_family_reachability(expected, evidence):
    need(type(expected) is FamilyReachabilityRequest and
         type(evidence) is FamilyReachabilityEvidence,
         "family reachability request and evidence required")
    expected.validate()
    evidence.request.validate()
    need(evidence.request == expected,
         "stale family, policy, unsafe set, cap, or query")
    need(tuple(row.member_identity for row in evidence.rows) ==
         tuple(member.identity for member in expected.family.members),
         "each family member must occur exactly once in order")
    modelwise = []
    for member, row in zip(expected.family.members, evidence.rows):
        local = ReachabilityRequest(member.subject, member.identity,
                                    expected.policy, expected.unsafe_set,
                                    expected.cap)
        answer = consume_reachability(local, row.certificate)
        modelwise.append((member.identity, answer["root_probability"],
                          answer["cap_met"]))
    worst = max(value for _, value, _ in modelwise)
    need(evidence.worst_probability == worst and
         evidence.robust_cap_met == (worst <= expected.cap),
         "false worst-family reachability or robust cap result")
    return {
        "status": FAMILY_CHECKED,
        "family_identity": expected.family.identity,
        "modelwise": tuple(modelwise),
        "worst_probability": worst,
        "cap": expected.cap,
        "robust_cap_met": worst <= expected.cap,
        "model_weights": None,
        "one_common_policy": True,
    }


@dataclass(frozen=True)
class SelectionRequest:
    family: families.Family
    unsafe_set: UnsafeSet
    policies: tuple
    scope: str
    cap: F
    named_policy_identity: object = None
    query: str = SELECTION_QUERY

    def __post_init__(self):
        object.__setattr__(self, "policies", tuple(self.policies))
        self.validate()

    def validate(self):
        need(type(self.family) is families.Family,
             "persistent family required")
        self.family.validate()
        need(type(self.unsafe_set) is UnsafeSet,
             "identified unsafe set required")
        for member in self.family.members:
            self.unsafe_set.validate(member.subject)
        probability(self.cap, "selection cap must lie in [0,1]")
        need(self.scope in (families.FULL, families.SUBSET),
             "explicit deterministic policy coverage required")
        need(self.query == SELECTION_QUERY,
             "unsupported constrained-selection query")
        # This reuses the existing exact policy-class and FULL-coverage checks.
        families.ChoiceRequest(self.family, self.policies, self.scope,
                               families.MINIMAX_LOSS)
        if self.named_policy_identity is not None:
            identity(self.named_policy_identity,
                     "named policy identity must be absent or nonempty")
            need(self.named_policy_identity in
                 {entry.identity for entry in self.policies},
                 "named comparator policy is outside the supplied catalogue")
        return self


@dataclass(frozen=True)
class PolicyReachabilityCell:
    member_identity: str
    policy_identity: str
    certificate: ReachabilityCertificate

    def __post_init__(self):
        identity(self.member_identity, "nonempty model identity required")
        identity(self.policy_identity, "nonempty policy identity required")
        need(type(self.certificate) is ReachabilityCertificate,
             "reachability matrix certificate required")


@dataclass(frozen=True)
class SelectionEvidence:
    request: SelectionRequest
    loss_evidence: families.ChoiceEvidence
    reachability_cells: tuple
    reachability_matrix: tuple
    worst_reachabilities: tuple
    feasible_policies: tuple
    minimax_loss_winners: tuple
    constrained_comparators: tuple
    constrained_regrets: tuple
    minimax_regret_winners: tuple
    named_constrained_regret: object
    empty_disposition: object

    def __post_init__(self):
        need(type(self.request) is SelectionRequest,
             "selection request binding required")
        need(type(self.loss_evidence) is families.ChoiceEvidence,
             "exact expected-loss matrix evidence required")
        object.__setattr__(self, "reachability_cells",
                           tuple(self.reachability_cells))
        need(all(type(cell) is PolicyReachabilityCell
                 for cell in self.reachability_cells),
             "typed reachability cells required")
        object.__setattr__(self, "reachability_matrix",
                           tuple(r.proof(row) for row in self.reachability_matrix))
        object.__setattr__(self, "worst_reachabilities",
                           r.proof(self.worst_reachabilities))
        for field in ("feasible_policies", "minimax_loss_winners",
                      "minimax_regret_winners"):
            value = tuple(getattr(self, field))
            need(all(type(item) is str and item for item in value),
                 "policy identity sequence required")
            object.__setattr__(self, field, value)
        object.__setattr__(self, "constrained_comparators",
                           r.proof(self.constrained_comparators))
        regrets = tuple(self.constrained_regrets)
        need(all(type(row) in (tuple, list) and len(row) == 2 and
                 type(row[0]) is str and row[0] and type(row[1]) is F
                 for row in regrets),
             "exact constrained-regret rows required")
        object.__setattr__(self, "constrained_regrets",
                           tuple((row[0], row[1]) for row in regrets))
        need(self.named_constrained_regret is None or
             type(self.named_constrained_regret) is F,
             "named constrained regret must be absent or exact")
        need(self.empty_disposition is None or
             self.empty_disposition in (NO_FULL_FEASIBLE, NO_SUPPLIED_FEASIBLE),
             "invalid empty-feasible-class disposition")


def _selection_values(request, cost_matrix, reachability_matrix):
    worst_reachabilities = tuple(max(row[index]
                                     for row in reachability_matrix)
                                 for index in range(len(request.policies)))
    feasible_indexes = tuple(index for index, value
                             in enumerate(worst_reachabilities)
                             if value <= request.cap)
    feasible = tuple(request.policies[index].identity
                     for index in feasible_indexes)
    if not feasible_indexes:
        disposition = (NO_FULL_FEASIBLE if request.scope == families.FULL
                       else NO_SUPPLIED_FEASIBLE)
        return (worst_reachabilities, feasible, (), (), (), (), None,
                disposition)
    worst_costs = tuple(max(row[index] for row in cost_matrix)
                        for index in feasible_indexes)
    best_cost = min(worst_costs)
    loss_winners = tuple(request.policies[index].identity
                         for index, value in zip(feasible_indexes, worst_costs)
                         if value == best_cost)
    comparators = tuple(min(row[index] for index in feasible_indexes)
                        for row in cost_matrix)
    regret_rows = []
    for index in feasible_indexes:
        value = max(cost_matrix[model][index] - comparators[model]
                    for model in range(len(cost_matrix)))
        regret_rows.append((request.policies[index].identity, value))
    best_regret = min(value for _, value in regret_rows)
    regret_winners = tuple(name for name, value in regret_rows
                           if value == best_regret)
    named = None
    if request.named_policy_identity in feasible:
        named = dict(regret_rows)[request.named_policy_identity]
    return (worst_reachabilities, feasible, loss_winners, comparators,
            tuple(regret_rows), regret_winners, named, None)


def produce_selection(request):
    """Producer: exact cost and hit-probability matrices for a catalogue."""
    request.validate()
    loss_request = families.ChoiceRequest(
        request.family, request.policies, request.scope, families.MINIMAX_LOSS)
    loss_evidence = families.choose(loss_request)
    cells = []
    reachability = []
    for member in request.family.members:
        row = []
        for entry in request.policies:
            local = ReachabilityRequest(member.subject, member.identity,
                                        entry.policy, request.unsafe_set,
                                        request.cap)
            certificate = produce_reachability(local)
            cells.append(PolicyReachabilityCell(
                member.identity, entry.identity, certificate))
            row.append(certificate.root_probability)
        reachability.append(tuple(row))
    values = _selection_values(request, loss_evidence.matrix,
                               tuple(reachability))
    return SelectionEvidence(request, loss_evidence, cells, reachability,
                             *values)


def consume_selection(expected, evidence):
    """Receiver: check fixed robust feasibility and same-model comparators."""
    need(type(expected) is SelectionRequest and
         type(evidence) is SelectionEvidence,
         "selection request and evidence required")
    expected.validate()
    evidence.request.validate()
    need(evidence.request == expected,
         "stale family, unsafe set, catalogue, cap, or query")
    loss_request = families.ChoiceRequest(
        expected.family, expected.policies, expected.scope,
        families.MINIMAX_LOSS)
    loss = families.consume_choice(loss_request, evidence.loss_evidence)
    m, n = len(expected.family.members), len(expected.policies)
    need(len(evidence.reachability_cells) == m * n and
         len(evidence.reachability_matrix) == m and
         all(len(row) == n for row in evidence.reachability_matrix),
         "incomplete reachability matrix")
    matrix = []
    cursor = 0
    for member in expected.family.members:
        row = []
        for entry in expected.policies:
            cell = evidence.reachability_cells[cursor]
            cursor += 1
            need((cell.member_identity, cell.policy_identity) ==
                 (member.identity, entry.identity),
                 "wrong reachability matrix cell pairing")
            local = ReachabilityRequest(member.subject, member.identity,
                                        entry.policy, expected.unsafe_set,
                                        expected.cap)
            answer = consume_reachability(local, cell.certificate)
            row.append(answer["root_probability"])
        matrix.append(tuple(row))
    matrix = tuple(matrix)
    need(evidence.reachability_matrix == matrix,
         "false reachability matrix")
    direct_costs = tuple(tuple(r.path_cost(member.subject, entry.policy)
                               for entry in expected.policies)
                         for member in expected.family.members)
    need(loss["matrix"] == direct_costs,
         "expected-cost matrix disagrees with independent complete paths")
    direct_hits = tuple(tuple(first_hit_probability(
        member.subject, entry.policy, expected.unsafe_set)
                              for entry in expected.policies)
                        for member in expected.family.members)
    need(matrix == direct_hits,
         "reachability recurrence disagrees with independent first-hit matrix")
    values = _selection_values(expected, loss["matrix"], matrix)
    supplied = (evidence.worst_reachabilities, evidence.feasible_policies,
                evidence.minimax_loss_winners,
                evidence.constrained_comparators,
                evidence.constrained_regrets,
                evidence.minimax_regret_winners,
                evidence.named_constrained_regret,
                evidence.empty_disposition)
    need(supplied == values,
         "false feasible class, constrained comparator, regret, or winner")
    (worst, feasible, loss_winners, comparators, regret_rows,
     regret_winners, named, disposition) = values
    named_status = None
    if expected.named_policy_identity is not None:
        named_status = ("checked-within-fixed-robust-feasible-class"
                        if expected.named_policy_identity in feasible else
                        "named-policy-not-robustly-feasible")
    return {
        "status": SELECTION_CHECKED,
        "scope": expected.scope,
        "coverage": ("complete-bounded-deterministic-policy-class"
                     if expected.scope == families.FULL else
                     "supplied-policy-subset-only"),
        "cost_matrix": loss["matrix"],
        "reachability_matrix": matrix,
        "worst_reachabilities": worst,
        "cap": expected.cap,
        "feasible_policies": feasible,
        "empty_disposition": disposition,
        "minimax_loss_winners": loss_winners,
        "fixed_robust_feasible_comparators": comparators,
        "constrained_regrets": regret_rows,
        "minimax_regret_winners": regret_winners,
        "named_policy": expected.named_policy_identity,
        "named_policy_status": named_status,
        "named_constrained_regret": named,
        "model_dependent_feasibility_used": False,
        "randomized_policy_claim": False,
        "direct_cost_paths_equal": True,
        "direct_first_hit_paths_equal": True,
    }


@dataclass(frozen=True)
class StatisticalRequest:
    corner_request: corners.Request
    unsafe_set: UnsafeSet
    cap: F
    query: str = STATISTICAL_QUERY

    def __post_init__(self):
        self.validate()

    def validate(self):
        need(type(self.corner_request) is corners.Request,
             "PR16 statistical-corner request required")
        self.corner_request.validate()
        need(type(self.unsafe_set) is UnsafeSet,
             "identified unsafe set required")
        nominal = corners.instantiate(
            self.corner_request.template,
            {parameter: F(0)
             for parameter in self.corner_request.template.parameters})
        self.unsafe_set.validate(nominal)
        probability(self.cap, "statistical robust-safety cap must lie in [0,1]")
        need(self.query == STATISTICAL_QUERY,
             "unsupported statistical reachability query")
        return self


@dataclass(frozen=True)
class StatisticalBoundaryEvidence:
    request: StatisticalRequest
    corner_evidence: corners.BoundaryEvidence
    status: str = INVALID_CORNER_WARRANT


@dataclass(frozen=True)
class StatisticalEvidence:
    request: StatisticalRequest
    corner_evidence: corners.Evidence
    selection_evidence: SelectionEvidence


def produce_statistical(request, coverage_evidence):
    """Producer: PR16 warrant first, then reachability on its corner family."""
    request.validate()
    corner_evidence = corners.produce(request.corner_request, coverage_evidence)
    if type(corner_evidence) is dict:
        return corner_evidence
    if type(corner_evidence) is corners.BoundaryEvidence:
        return StatisticalBoundaryEvidence(request, corner_evidence)
    selection = SelectionRequest(
        corner_evidence.family, request.unsafe_set,
        request.corner_request.policies, request.corner_request.scope,
        request.cap, request.corner_request.named_policy_identity)
    return StatisticalEvidence(request, corner_evidence,
                               produce_selection(selection))


def consume_statistical(expected, evidence):
    """Receiver: check coverage/mapping/warrant before the safety family."""
    expected.validate()
    refusal = corners.request_budget(expected.corner_request)
    if refusal:
        need(evidence == refusal, "wrong statistical profile refusal")
        return refusal
    need(type(evidence) in (StatisticalEvidence, StatisticalBoundaryEvidence),
         "statistical reachability or boundary evidence required")
    need(evidence.request == expected,
         "stale statistics, mapping, skeleton, unsafe set, cap, or policy")
    corner_answer = corners.consume(expected.corner_request,
                                    evidence.corner_evidence)
    if corner_answer["status"] == corners.INVALID_WARRANT:
        need(type(evidence) is StatisticalBoundaryEvidence and
             evidence.status == INVALID_CORNER_WARRANT,
             "inadmissible subject received a corner reachability warrant")
        return {
            "status": INVALID_CORNER_WARRANT,
            "mapped_rectangle": corner_answer["mapped_rectangle"],
            "repeated_parameter_paths":
                corner_answer["repeated_parameter_paths"],
            "sequential_model_status":
                corner_answer["sequential_model_status"],
            "required_next_method":
                "optimization-other-than-exact-corner-reduction",
            "mathematical_impossibility_claimed": False,
        }
    need(type(evidence) is StatisticalEvidence,
         "admissible subject lacks statistical reachability evidence")
    family = evidence.corner_evidence.family
    selection_request = SelectionRequest(
        family, expected.unsafe_set, expected.corner_request.policies,
        expected.corner_request.scope, expected.cap,
        expected.corner_request.named_policy_identity)
    selection = consume_selection(selection_request,
                                  evidence.selection_evidence)
    corner_matrix = selection["reachability_matrix"]
    audit_points = corners.grid(corner_answer["mapped_rectangle"])
    audit_matrix = []
    for point in audit_points:
        subject = corners.instantiate(expected.corner_request.template,
                                      dict(point), "interior audit")
        audit_matrix.append(tuple(first_hit_probability(
            subject, entry.policy, expected.unsafe_set)
                                  for entry in expected.corner_request.policies))
    audit_matrix = tuple(audit_matrix)
    audit_worst = tuple(max(row[index] for row in audit_matrix)
                        for index in range(len(expected.corner_request.policies)))
    corner_worst = tuple(max(row[index] for row in corner_matrix)
                         for index in range(len(expected.corner_request.policies)))
    need(audit_worst == corner_worst,
         "exact rational interior reachability audit escaped the corners")
    named_index = next(index for index, entry
                       in enumerate(expected.corner_request.policies)
                       if entry.identity ==
                       expected.corner_request.named_policy_identity)
    named_corner = tuple(row[named_index] for row in corner_matrix)
    worst = max(named_corner)
    statistical = corner_answer["statistical"]
    return {
        "status": STATISTICAL_CHECKED,
        "warrant": "first-hit-multi-affine-corner-reduction",
        "mapped_rectangle": corner_answer["mapped_rectangle"],
        "corner_coordinates": corner_answer["corner_coordinates"],
        "corner_count": corner_answer["corner_count"],
        "named_policy": expected.corner_request.named_policy_identity,
        "named_corner_reachabilities": named_corner,
        "named_worst_reachability": worst,
        "cap": expected.cap,
        "cap_met": worst <= expected.cap,
        "selection": selection,
        "rational_interior_audit_points": len(audit_points),
        "rational_interior_audit_equal": True,
        "statistical": {
            "simultaneous_coverage_lower":
                statistical["simultaneous_coverage_lower"],
            "coverage_failure_probability_upper":
                statistical["failure_probability_upper"],
            "sampling_premises_supplied_not_empirically_validated": True,
            "outward_rectangle_may_be_conservative": True,
        },
        "composed_guarantee": {
            "rule": ("on-the-simultaneous-coverage-event-the-true-parameter-"
                     "lies-in-the-exported-rectangle-and-any-established-"
                     "rectangle-wide-reachability-cap-applies"),
            "true_model_cap_on_coverage_event": worst <= expected.cap,
        },
        "coverage_failure_and_harm_probability_not_combined": True,
    }


def reject_probability_merge(coverage_failure_probability,
                             reachability_probability):
    """There is no generic arithmetic join for these differently typed events."""
    probability(coverage_failure_probability)
    probability(reachability_probability)
    raise Invalid("coverage failure and unsafe reachability are different events; "
                  "no unlabeled sum or merged uncertainty is supported")


def wire(value):
    return corners.wire(value)
