"""Exact finite certificates for persistent families of whole-episode models."""
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "certificate_accumulation"))
import accumulate as a

r, t = a.r, a.t
CRITERION = t.GUARANTEE
NAMED_POLICY = "one-policy-across-persistent-family"
COMMON_OPTIMAL = "common-modelwise-optimal-policy"
MINIMAX_LOSS = "minimum-worst-model-expected-loss"
MINIMAX_REGRET = "minimum-worst-model-regret"
FULL = "full-deterministic-policy-class"
SUBSET = "requested-candidate-subset"
CONDITIONAL = "support-filtered-continuation-family"
MAX_MODELS = 4
MAX_FULL_POLICIES = 64


class Unfinished(r.Invalid):
    """A stronger requested computation exceeds the declared reference budget."""


class ImpossibleConditioning(r.Invalid):
    """Every member of a valid supplied family gives the event zero mass."""


def _identity(x, message="nonempty identity"):
    r.need(type(x) is str and bool(x), message)
    return x


def _scalar(x):
    r.need(type(x) is F, "exact Fraction proof scalar required")
    return x


@dataclass(frozen=True)
class Member:
    identity: str
    subject: r.Subject

    def __post_init__(self):
        _identity(self.identity, "nonempty model identity")
        r.need(type(self.subject) is r.Subject, "model subject")
        self.subject.validate()


@dataclass(frozen=True)
class Family:
    identity: str
    members: tuple
    criterion: str = CRITERION

    def __post_init__(self):
        _identity(self.identity, "nonempty family identity")
        r.need(type(self.members) in (list, tuple), "ordered model family")
        object.__setattr__(self, "members", tuple(self.members))
        self.validate()

    def validate(self):
        r.need(type(self.criterion) is str and self.criterion == CRITERION,
               "unsupported family criterion")
        r.need(1 <= len(self.members) <= MAX_MODELS,
               "one to four models; otherwise unsupported/unfinished")
        r.need(all(type(x) is Member for x in self.members), "model member types")
        ids = [x.identity for x in self.members]
        r.need(len(set(ids)) == len(ids), "duplicate model identities")
        shared = t.skeleton(self.members[0].subject)
        r.need(all(t.skeleton(x.subject) == shared for x in self.members),
               "models require one ordered history/action/outcome skeleton, horizon and unit")
        return self


def _policy_key(subject, policy):
    chosen = policy.validate(subject)
    return tuple((n.h, chosen[n.h]) for n in subject.nodes if n.actions)


def _member_map(family):
    family.validate()
    return {x.identity: x for x in family.members}


@dataclass(frozen=True)
class ModelSources:
    member_identity: str
    sources: tuple

    def __post_init__(self):
        _identity(self.member_identity, "nonempty model identity")
        r.need(type(self.sources) in (list, tuple), "source sequence")
        object.__setattr__(self, "sources", tuple(self.sources))
        r.need(all(type(x) is a.Source for x in self.sources), "accumulation sources")


@dataclass(frozen=True)
class NamedPolicyRequest:
    family: Family
    policy: r.Policy
    groups: tuple
    claim: str = NAMED_POLICY

    def __post_init__(self):
        r.need(type(self.groups) in (list, tuple), "model-indexed source groups")
        object.__setattr__(self, "groups", tuple(self.groups))
        self.validate()

    def validate(self):
        r.need(type(self.family) is Family and type(self.policy) is r.Policy,
               "family and one common policy required")
        self.family.validate()
        r.need(type(self.claim) is str and self.claim == NAMED_POLICY,
               "wrong named-policy claim")
        r.need(all(type(x) is ModelSources for x in self.groups), "model source groups")
        expected = tuple(x.identity for x in self.family.members)
        r.need(tuple(x.member_identity for x in self.groups) == expected,
               "each requested model must occur exactly once in family order")
        for member, group in zip(self.family.members, self.groups):
            self.policy.validate(member.subject)
            a.Request(member.subject, group.sources, "same-policy", self.policy)
        return self


@dataclass(frozen=True)
class ModelAccumulation:
    member_identity: str
    evidence: a.Evidence

    def __post_init__(self):
        _identity(self.member_identity, "nonempty model identity")
        r.need(type(self.evidence) is a.Evidence, "accumulation evidence")


@dataclass(frozen=True)
class NamedPolicyEvidence:
    request: NamedPolicyRequest
    combined: tuple
    worst_policy_upper: F
    worst_regret_upper: F

    def __post_init__(self):
        r.need(type(self.request) is NamedPolicyRequest, "named-policy request")
        r.need(type(self.combined) in (list, tuple), "model evidence sequence")
        object.__setattr__(self, "combined", tuple(self.combined))
        r.need(all(type(x) is ModelAccumulation for x in self.combined),
               "model accumulation evidence")
        object.__setattr__(self, "worst_policy_upper", _scalar(self.worst_policy_upper))
        object.__setattr__(self, "worst_regret_upper", _scalar(self.worst_regret_upper))


def bound_named_policy(request):
    """Producer: accumulate only inside each exact model, then take paired maxima."""
    request.validate()
    rows, uppers, regrets = [], [], []
    for member, group in zip(request.family.members, request.groups):
        q = a.Request(member.subject, group.sources, "same-policy", request.policy)
        evidence = a.combine(q)
        answer = a.consume(q, request.policy, evidence)
        rows.append(ModelAccumulation(member.identity, evidence))
        uppers.append(answer["policy_upper"])
        regrets.append(answer["regret_upper"])
    return NamedPolicyEvidence(request, rows, max(uppers), max(regrets))


def consume_named_policy(expected, evidence):
    """Receiver: validate every source/group before aggregating modelwise pairs."""
    r.need(type(expected) is NamedPolicyRequest and type(evidence) is NamedPolicyEvidence,
           "expected named-policy request and evidence")
    expected.validate()
    evidence.request.validate()
    r.need(expected == evidence.request, "wrong family, policy, criterion or sources")
    r.need(tuple(x.member_identity for x in evidence.combined) ==
           tuple(x.identity for x in expected.family.members),
           "wrong model evidence coverage")
    modelwise, uppers, regrets = [], [], []
    for member, group, row in zip(expected.family.members, expected.groups, evidence.combined):
        q = a.Request(member.subject, group.sources, "same-policy", expected.policy)
        answer = a.consume(q, expected.policy, row.evidence)
        modelwise.append((member.identity, answer["optimum_lower"],
                          answer["policy_upper"], answer["regret_upper"]))
        uppers.append(answer["policy_upper"])
        regrets.append(answer["regret_upper"])
    r.need(evidence.worst_policy_upper == max(uppers), "false worst-model policy bound")
    r.need(evidence.worst_regret_upper == max(regrets), "false paired regret bound")
    return {"claim": NAMED_POLICY, "modelwise": tuple(modelwise),
            "worst_policy_upper": evidence.worst_policy_upper,
            "worst_regret_upper": evidence.worst_regret_upper}


@dataclass(frozen=True)
class PolicyEntry:
    identity: str
    policy: r.Policy

    def __post_init__(self):
        _identity(self.identity, "nonempty policy identity")
        r.need(type(self.policy) is r.Policy, "total deterministic policy")


@dataclass(frozen=True)
class ChoiceRequest:
    family: Family
    policies: tuple
    scope: str
    claim: str

    def __post_init__(self):
        r.need(type(self.policies) in (list, tuple), "ordered policy catalogue")
        object.__setattr__(self, "policies", tuple(self.policies))
        self.validate()

    def validate(self):
        r.need(type(self.family) is Family, "model family")
        self.family.validate()
        r.need(type(self.scope) is str and self.scope in (FULL, SUBSET), "policy scope")
        r.need(type(self.claim) is str and self.claim in
               (COMMON_OPTIMAL, MINIMAX_LOSS, MINIMAX_REGRET), "choice claim")
        r.need(1 <= len(self.policies) <= MAX_FULL_POLICIES, "one to sixty-four policies")
        r.need(all(type(x) is PolicyEntry for x in self.policies), "policy entries")
        ids = [x.identity for x in self.policies]
        r.need(len(set(ids)) == len(ids), "duplicate policy identities")
        first = self.family.members[0].subject
        keys = []
        for entry in self.policies:
            keys.append(_policy_key(first, entry.policy))
            for member in self.family.members[1:]:
                entry.policy.validate(member.subject)
        r.need(len(set(keys)) == len(keys), "duplicate policy columns")
        if self.scope == FULL:
            size = 1
            for node in first.nodes:
                if node.actions:
                    size *= len(node.actions)
            if size > MAX_FULL_POLICIES:
                raise Unfinished("full deterministic coverage exceeds sixty-four policies")
            complete = {_policy_key(first, x) for x in r.enumerate_policies(first)}
            r.need(len(keys) == size and set(keys) == complete,
                   "full-class coverage is false or incomplete")
        return self


@dataclass(frozen=True)
class MatrixCell:
    member_identity: str
    policy_identity: str
    certificate: r.Certificate

    def __post_init__(self):
        _identity(self.member_identity, "nonempty model identity")
        _identity(self.policy_identity, "nonempty policy identity")
        r.need(type(self.certificate) is r.Certificate, "ordinary exact certificate")


@dataclass(frozen=True)
class ChoiceEvidence:
    request: ChoiceRequest
    cells: tuple
    matrix: tuple
    comparators: tuple
    worst_costs: tuple
    worst_regrets: tuple
    winners: tuple
    policy_count: int

    def __post_init__(self):
        r.need(type(self.request) is ChoiceRequest, "choice request")
        r.need(type(self.cells) in (list, tuple), "matrix cell sequence")
        object.__setattr__(self, "cells", tuple(self.cells))
        r.need(all(type(x) is MatrixCell for x in self.cells), "matrix cells")
        r.need(type(self.matrix) in (list, tuple), "exact matrix")
        rows = []
        for row in self.matrix:
            rows.append(r.proof(row))
        object.__setattr__(self, "matrix", tuple(rows))
        object.__setattr__(self, "comparators", r.proof(self.comparators))
        object.__setattr__(self, "worst_costs", r.proof(self.worst_costs))
        object.__setattr__(self, "worst_regrets", r.proof(self.worst_regrets))
        r.need(type(self.winners) in (list, tuple) and
               all(type(x) is str and x for x in self.winners), "winner identities")
        object.__setattr__(self, "winners", tuple(self.winners))
        r.need(type(self.policy_count) is int and type(self.policy_count) is not bool,
               "claimed policy count")


def _backup(node, action, values):
    return action.cost + sum((p * values[node.h + ((action.label, o),)]
                              for o, p in action.outcomes), F(0))


def _exact_certificate(subject, policy, certificate):
    """Check Bellman optimum and policy-evaluation equalities; no producer call."""
    r.consume(subject, policy, certificate)
    lower = r.table(subject, certificate.lower)
    upper = r.table(subject, certificate.upper)
    chosen = policy.validate(subject)
    for node in subject.nodes:
        if not node.actions:
            r.need(lower[node.h] == node.terminal == upper[node.h],
                   "terminal equality required for exact matrix")
        else:
            r.need(lower[node.h] == min(_backup(node, action, lower)
                                        for action in node.actions),
                   "modelwise optimum equality required")
            action = next(x for x in node.actions if x.label == chosen[node.h])
            r.need(upper[node.h] == _backup(node, action, upper),
                   "policy-evaluation equality required")
    return lower[()], upper[()]


def _choice_values(request, matrix, comparators):
    worst_costs = tuple(max(row[j] for row in matrix)
                        for j in range(len(request.policies)))
    worst_regrets = tuple(max(matrix[i][j] - comparators[i]
                              for i in range(len(request.family.members)))
                            for j in range(len(request.policies)))
    if request.claim == COMMON_OPTIMAL:
        winner_indexes = [j for j in range(len(request.policies))
                          if all(matrix[i][j] == comparators[i]
                                 for i in range(len(request.family.members)))]
    else:
        values = worst_costs if request.claim == MINIMAX_LOSS else worst_regrets
        best = min(values)
        winner_indexes = [j for j, value in enumerate(values) if value == best]
    winners = tuple(request.policies[j].identity for j in winner_indexes)
    return worst_costs, worst_regrets, winners


def choose(request):
    """Producer: construct an exact policy-by-model matrix for the requested catalogue."""
    request.validate()
    cells, matrix, comparators = [], [], []
    for member in request.family.members:
        row, optimum = [], None
        for policy in request.policies:
            certificate = r.produce(member.subject, policy.policy)
            lower, value = _exact_certificate(member.subject, policy.policy, certificate)
            optimum = lower if optimum is None else optimum
            r.need(lower == optimum, "inconsistent exact modelwise comparator")
            cells.append(MatrixCell(member.identity, policy.identity, certificate))
            row.append(value)
        matrix.append(tuple(row))
        comparators.append(optimum)
    worst_costs, worst_regrets, winners = _choice_values(request, matrix, comparators)
    return ChoiceEvidence(request, cells, matrix, tuple(comparators), worst_costs,
                          worst_regrets, winners, len(request.policies))


def consume_choice(expected, evidence):
    """Receiver: check exact matrix, optimum witnesses, coverage and requested choice."""
    r.need(type(expected) is ChoiceRequest and type(evidence) is ChoiceEvidence,
           "expected choice request and evidence")
    expected.validate()
    evidence.request.validate()
    r.need(expected == evidence.request, "wrong family, policy catalogue, scope or claim")
    m, n = len(expected.family.members), len(expected.policies)
    r.need(evidence.policy_count == n, "false policy count")
    r.need(len(evidence.cells) == m * n and len(evidence.matrix) == m and
           all(len(row) == n for row in evidence.matrix), "incomplete exact matrix")
    matrix, comparators, k = [], [], 0
    for member in expected.family.members:
        row, optimum = [], None
        for policy in expected.policies:
            cell = evidence.cells[k]
            k += 1
            r.need((cell.member_identity, cell.policy_identity) ==
                   (member.identity, policy.identity), "wrong matrix cell pairing")
            lower, value = _exact_certificate(member.subject, policy.policy, cell.certificate)
            optimum = lower if optimum is None else optimum
            r.need(lower == optimum, "inconsistent modelwise comparator")
            row.append(value)
        matrix.append(tuple(row))
        comparators.append(optimum)
    matrix, comparators = tuple(matrix), tuple(comparators)
    r.need(evidence.matrix == matrix, "false policy-value matrix")
    r.need(evidence.comparators == comparators, "false modelwise optimum comparator")
    worst_costs, worst_regrets, winners = _choice_values(expected, matrix, comparators)
    r.need(evidence.worst_costs == worst_costs, "false worst-model loss vector")
    r.need(evidence.worst_regrets == worst_regrets, "false paired regret vector")
    r.need(evidence.winners == winners, "false choice or incomplete ties")
    return {"claim": expected.claim, "scope": expected.scope, "matrix": matrix,
            "comparators": comparators, "worst_costs": worst_costs,
            "worst_regrets": worst_regrets, "winners": winners}


@dataclass(frozen=True)
class ContinuationRequest:
    family: Family
    prefix_policy: r.Policy
    continuation_policy: r.Policy
    event: tuple
    claim: str = CONDITIONAL

    def __post_init__(self):
        object.__setattr__(self, "event", r.history(self.event))
        self.validate()

    def validate(self):
        r.need(type(self.family) is Family and type(self.prefix_policy) is r.Policy and
               type(self.continuation_policy) is r.Policy, "family and accessible policies")
        self.family.validate()
        r.need(type(self.claim) is str and self.claim == CONDITIONAL,
               "wrong continuation claim")
        histories = {n.h for n in self.family.members[0].subject.nodes}
        r.need(self.event in histories, "unknown family event")
        for member in self.family.members:
            self.prefix_policy.validate(member.subject)
            self.continuation_policy.validate(member.subject)
        return self


@dataclass(frozen=True)
class ContinuationRow:
    member_identity: str
    certificate: r.Certificate
    mass: F

    def __post_init__(self):
        _identity(self.member_identity, "nonempty model identity")
        r.need(type(self.certificate) is r.Certificate, "ordinary continuation certificate")
        object.__setattr__(self, "mass", _scalar(self.mass))


@dataclass(frozen=True)
class ContinuationEvidence:
    request: ContinuationRequest
    rows: tuple
    retained: tuple
    excluded: tuple

    def __post_init__(self):
        r.need(type(self.request) is ContinuationRequest, "continuation request")
        r.need(type(self.rows) in (list, tuple), "continuation rows")
        object.__setattr__(self, "rows", tuple(self.rows))
        r.need(all(type(x) is ContinuationRow for x in self.rows), "continuation row types")
        for field in ("retained", "excluded"):
            value = getattr(self, field)
            r.need(type(value) in (list, tuple) and all(type(x) is str and x for x in value),
                   "model identity partition")
            object.__setattr__(self, field, tuple(value))


def _prefix_mass(subject, prefix_policy, event):
    chosen = prefix_policy.validate(subject)
    nodes = {n.h: n for n in subject.nodes}
    history, mass = (), F(1)
    for action_label, observation in event:
        node = nodes[history]
        if not node.actions or chosen[history] != action_label:
            return F(0)
        action = next(x for x in node.actions if x.label == action_label)
        mass *= dict(action.outcomes).get(observation, F(0))
        history += ((action_label, observation),)
    return mass


def condition(request):
    """Producer: exact ordinary certificates plus the unweighted support partition."""
    request.validate()
    rows, retained, excluded = [], [], []
    for member in request.family.members:
        mass = _prefix_mass(member.subject, request.prefix_policy, request.event)
        certificate = r.produce(member.subject, request.continuation_policy)
        rows.append(ContinuationRow(member.identity, certificate, mass))
        (retained if mass > 0 else excluded).append(member.identity)
    return ContinuationEvidence(request, rows, retained, excluded)


def consume_condition(expected, evidence):
    """Receiver: recompute support and check each surviving continuation separately."""
    r.need(type(expected) is ContinuationRequest and type(evidence) is ContinuationEvidence,
           "expected continuation request and evidence")
    expected.validate()
    evidence.request.validate()
    r.need(expected == evidence.request,
           "wrong family, prefix, event, continuation or criterion")
    r.need(tuple(row.member_identity for row in evidence.rows) ==
           tuple(member.identity for member in expected.family.members),
           "each model continuation must occur exactly once in family order")
    retained, excluded, modelwise = [], [], []
    for member, row in zip(expected.family.members, evidence.rows):
        mass = _prefix_mass(member.subject, expected.prefix_policy, expected.event)
        r.need(row.mass == mass, "false model prefix mass")
        r.consume(member.subject, expected.continuation_policy, row.certificate)
        if mass > 0:
            query = t.ContinuationQuery(member.subject, expected.prefix_policy,
                                        expected.continuation_policy, expected.event)
            answer = t.consume_continuation(
                query, t.ContinuationEvidence(query, row.certificate, mass))
            retained.append(member.identity)
            modelwise.append((member.identity, mass, answer["optimum_lower"],
                              answer["policy_upper"], answer["regret_upper"]))
        else:
            excluded.append(member.identity)
    r.need(evidence.retained == tuple(retained) and evidence.excluded == tuple(excluded),
           "false retained/excluded support partition")
    if not retained:
        raise ImpossibleConditioning(
            "observed history is impossible under every member of the supplied family")
    return {"claim": CONDITIONAL, "event": expected.event,
            "retained": tuple(retained), "excluded_zero_mass": tuple(excluded),
            "modelwise": tuple(modelwise), "weights": None}
