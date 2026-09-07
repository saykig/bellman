"""Exact within-family policy splices and root-cap checks."""
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "persistent_model_families"))
import families as f

r, a = f.r, f.a
EXPECTED_COST_CAP = "worst-model-expected-cost-cap"
REGRET_CAP = "worst-model-regret-cap"
PRESERVED = "preservation-certified"
NOT_ESTABLISHED = "preservation-not-established"
BASELINE_NOT_ESTABLISHED = "baseline-preservation-premise-not-established"
VIOLATION = "supported-exact-violation"
EXACT_SATISFIED = "supported-exact-satisfaction"


def _scalar(value, nonnegative=False):
    r.need(type(value) is F, "exact Fraction threshold required")
    r.need(not nonnegative or value >= 0, "regret threshold must be nonnegative")
    return value


def _prefix(shorter, longer):
    return len(shorter) <= len(longer) and longer[:len(shorter)] == shorter


@dataclass(frozen=True)
class ModelSources:
    member_identity: str
    baseline: a.Source
    replacement: a.Source

    def __post_init__(self):
        f._identity(self.member_identity, "nonempty model identity")
        r.need(type(self.baseline) is a.Source and type(self.replacement) is a.Source,
               "baseline and replacement sources")


@dataclass(frozen=True)
class Request:
    family: f.Family
    baseline_policy: r.Policy
    event: tuple
    replacement_policy: r.Policy
    sources: tuple
    cap: str
    threshold: F
    criterion: str = f.CRITERION

    def __post_init__(self):
        object.__setattr__(self, "event", r.history(self.event))
        r.need(type(self.sources) in (list, tuple), "ordered model sources")
        object.__setattr__(self, "sources", tuple(self.sources))
        object.__setattr__(self, "threshold",
                           _scalar(self.threshold, self.cap == REGRET_CAP))
        self.validate()

    def validate(self):
        r.need(type(self.family) is f.Family and type(self.baseline_policy) is r.Policy and
               type(self.replacement_policy) is r.Policy,
               "persistent family and two common total policies required")
        self.family.validate()
        r.need(type(self.criterion) is str and self.criterion == f.CRITERION,
               "unsupported criterion")
        r.need(type(self.cap) is str and self.cap in (EXPECTED_COST_CAP, REGRET_CAP),
               "unsupported root guarantee")
        _scalar(self.threshold, self.cap == REGRET_CAP)
        histories = {node.h for node in self.family.members[0].subject.nodes}
        r.need(self.event in histories, "unknown splice history")
        r.need(all(type(row) is ModelSources for row in self.sources),
               "model source rows")
        expected = tuple(member.identity for member in self.family.members)
        r.need(tuple(row.member_identity for row in self.sources) == expected,
               "each model must occur exactly once in family order")
        for member, row in zip(self.family.members, self.sources):
            self.baseline_policy.validate(member.subject)
            self.replacement_policy.validate(member.subject)
            r.consume(member.subject, self.baseline_policy, row.baseline.certificate)
            r.consume(member.subject, self.replacement_policy, row.replacement.certificate)
        return self


@dataclass(frozen=True)
class ModelSplice:
    member_identity: str
    certificate: r.Certificate
    path_factors: tuple

    def __post_init__(self):
        f._identity(self.member_identity, "nonempty model identity")
        r.need(type(self.certificate) is r.Certificate, "ordinary splice certificate")
        object.__setattr__(self, "path_factors", r.proof(self.path_factors))


@dataclass(frozen=True)
class Evidence:
    request: Request
    final_policy: r.Policy
    rows: tuple
    baseline_values: tuple
    spliced_values: tuple
    allowances: tuple
    disposition: str

    def __post_init__(self):
        r.need(type(self.request) is Request and type(self.final_policy) is r.Policy,
               "splice evidence request and policy")
        r.need(type(self.rows) in (list, tuple), "splice rows")
        object.__setattr__(self, "rows", tuple(self.rows))
        r.need(all(type(row) is ModelSplice for row in self.rows), "splice row types")
        object.__setattr__(self, "baseline_values", r.proof(self.baseline_values))
        object.__setattr__(self, "spliced_values", r.proof(self.spliced_values))
        r.need(type(self.allowances) in (list, tuple), "continuation allowances")
        allowances = tuple(self.allowances)
        r.need(all(value is None or type(value) is F for value in allowances),
               "exact positive-mass allowance or None")
        object.__setattr__(self, "allowances", allowances)
        r.need(type(self.disposition) is str, "cap disposition")


def _producer_policy(request):
    old = request.baseline_policy.validate(request.family.members[0].subject)
    new = request.replacement_policy.validate(request.family.members[0].subject)
    return r.Policy(tuple((node.h, new[node.h] if _prefix(request.event, node.h)
                           else old[node.h])
                          for node in request.family.members[0].subject.nodes if node.actions))


def _producer_factor(subject, policy, start, event):
    if start == event:
        return F(1)
    if not _prefix(start, event):
        return F(0)
    nodes, chosen = {node.h: node for node in subject.nodes}, policy.validate(subject)
    current, mass = start, F(1)
    for action_label, observation in event[len(start):]:
        node = nodes[current]
        if not node.actions or chosen[current] != action_label:
            return F(0)
        action = next(action for action in node.actions if action.label == action_label)
        mass *= dict(action.outcomes).get(observation, F(0))
        current += ((action_label, observation),)
    return mass


def _cap_fields(request, rows):
    baseline_values, spliced_values, allowances = [], [], []
    for member, source, row in zip(request.family.members, request.sources, rows):
        old_lower = r.table(member.subject, source.baseline.certificate.lower)
        old_upper = r.table(member.subject, source.baseline.certificate.upper)
        new_upper = r.table(member.subject, row.certificate.upper)
        mass = row.path_factors[0]
        if request.cap == EXPECTED_COST_CAP:
            baseline_values.append(old_upper[()])
            spliced_values.append(new_upper[()])
            limit = request.threshold
        else:
            baseline_values.append(old_upper[()] - old_lower[()])
            spliced_values.append(new_upper[()] - old_lower[()])
            limit = old_lower[()] + request.threshold
        allowances.append(None if mass == 0 else
                          old_upper[request.event] +
                          (limit - old_upper[()]) / mass)
    baseline_values, spliced_values = tuple(baseline_values), tuple(spliced_values)
    if not all(value <= request.threshold for value in baseline_values):
        disposition = BASELINE_NOT_ESTABLISHED
    elif all(value <= request.threshold for value in spliced_values):
        disposition = PRESERVED
    else:
        disposition = NOT_ESTABLISHED
    return baseline_values, spliced_values, tuple(allowances), disposition


def splice(request):
    """Producer: splice one subtree and form the signed certificate corrections."""
    request.validate()
    final_policy = _producer_policy(request)
    rows = []
    for member, sources in zip(request.family.members, request.sources):
        subject = member.subject
        old_lower = r.table(subject, sources.baseline.certificate.lower)
        old_upper = r.table(subject, sources.baseline.certificate.upper)
        replacement_upper = r.table(subject, sources.replacement.certificate.upper)
        factors = tuple(_producer_factor(subject, request.baseline_policy,
                                         node.h, request.event)
                        for node in subject.nodes)
        upper = []
        for node, factor in zip(subject.nodes, factors):
            if _prefix(request.event, node.h):
                upper.append(replacement_upper[node.h])
            elif _prefix(node.h, request.event):
                upper.append(old_upper[node.h] + factor *
                             (replacement_upper[request.event] - old_upper[request.event]))
            else:
                upper.append(old_upper[node.h])
        certificate = r.Certificate(subject, final_policy,
                                    tuple(old_lower[node.h] for node in subject.nodes), upper)
        rows.append(ModelSplice(member.identity, certificate, factors))
    fields = _cap_fields(request, rows)
    return Evidence(request, final_policy, rows, *fields)


def _receiver_policy(request):
    """Independent splice reconstruction used only by receiving."""
    subject = request.family.members[0].subject
    baseline = dict(request.baseline_policy.choices)
    replacement = dict(request.replacement_policy.choices)
    choices = []
    for node in subject.nodes:
        if node.actions:
            choices.append((node.h, replacement[node.h]
                            if node.h[:len(request.event)] == request.event
                            else baseline[node.h]))
    return r.Policy(choices)


def _receiver_factors(subject, policy, event):
    """Recompute every algebraic path factor without using the producer helper."""
    nodes, chosen = {node.h: node for node in subject.nodes}, policy.validate(subject)
    values = []
    for node in subject.nodes:
        start = node.h
        if start == event:
            values.append(F(1))
            continue
        if len(start) >= len(event) or event[:len(start)] != start:
            values.append(F(0))
            continue
        cursor, probability = start, F(1)
        for required_action, observation in event[len(start):]:
            parent = nodes[cursor]
            if not parent.actions or chosen[cursor] != required_action:
                probability = F(0)
                break
            selected = next(action for action in parent.actions
                            if action.label == required_action)
            probability *= dict(selected.outcomes).get(observation, F(0))
            cursor = cursor + ((required_action, observation),)
        values.append(probability)
    return tuple(values)


def consume(expected, intended_final_policy, evidence):
    """Receiver: check sources, derivation, cap claim and ordinary target validity."""
    r.need(type(expected) is Request and type(intended_final_policy) is r.Policy and
           type(evidence) is Evidence, "expected request, final policy and splice evidence")
    expected.validate()
    evidence.request.validate()
    r.need(expected == evidence.request, "wrong family, event, sources, cap or threshold")
    independently_spliced = _receiver_policy(expected)
    r.need(intended_final_policy == independently_spliced and
           evidence.final_policy == independently_spliced,
           "final policy is not the complete requested subtree splice")
    expected_ids = tuple(member.identity for member in expected.family.members)
    r.need(tuple(row.member_identity for row in evidence.rows) == expected_ids,
           "wrong model splice coverage or order")
    for member, sources, row in zip(expected.family.members, expected.sources, evidence.rows):
        subject = member.subject
        factors = _receiver_factors(subject, expected.baseline_policy, expected.event)
        r.need(row.path_factors == factors, "false algebraic path factor")
        old_lower = r.table(subject, sources.baseline.certificate.lower)
        old_upper = r.table(subject, sources.baseline.certificate.upper)
        replacement_upper = r.table(subject, sources.replacement.certificate.upper)
        lower = r.table(subject, row.certificate.lower)
        upper = r.table(subject, row.certificate.upper)
        for node, factor in zip(subject.nodes, factors):
            if node.h[:len(expected.event)] == expected.event:
                wanted = replacement_upper[node.h]
            elif (len(node.h) < len(expected.event) and
                  expected.event[:len(node.h)] == node.h):
                wanted = old_upper[node.h] + factor * (
                    replacement_upper[expected.event] - old_upper[expected.event])
            else:
                wanted = old_upper[node.h]
            r.need(lower[node.h] == old_lower[node.h], "changed optimum comparator")
            r.need(upper[node.h] == wanted, "false certificate-splice derivation")
        r.consume(subject, intended_final_policy, row.certificate)
    baseline, spliced, allowances, disposition = _cap_fields(expected, evidence.rows)
    r.need(evidence.baseline_values == baseline, "false baseline cap values")
    r.need(evidence.spliced_values == spliced, "false spliced cap values")
    r.need(evidence.allowances == allowances, "false continuation allowance")
    r.need(evidence.disposition == disposition, "false preservation disposition")
    within_allowance = []
    for member, sources, allowance in zip(expected.family.members,
                                          expected.sources, allowances):
        replacement_upper = r.table(
            member.subject, sources.replacement.certificate.upper)[expected.event]
        within_allowance.append(None if allowance is None else
                                replacement_upper <= allowance)
    return {"cap": expected.cap, "threshold": expected.threshold,
            "baseline_values": baseline, "spliced_values": spliced,
            "allowances": allowances,
            "continuation_within_allowance": tuple(within_allowance),
            "disposition": disposition,
            "member_masses": tuple(row.path_factors[0] for row in evidence.rows)}


@dataclass(frozen=True)
class ExactRow:
    member_identity: str
    baseline: r.Certificate
    replacement: r.Certificate
    final: r.Certificate

    def __post_init__(self):
        f._identity(self.member_identity, "nonempty model identity")
        r.need(all(type(value) is r.Certificate for value in
                   (self.baseline, self.replacement, self.final)),
               "three exact ordinary certificates required")


@dataclass(frozen=True)
class ExactEvidence:
    request: Request
    final_policy: r.Policy
    rows: tuple
    claimed_root_deltas: tuple

    def __post_init__(self):
        r.need(type(self.request) is Request and type(self.final_policy) is r.Policy,
               "exact evidence request and final policy")
        r.need(type(self.rows) in (list, tuple), "exact model rows")
        object.__setattr__(self, "rows", tuple(self.rows))
        r.need(all(type(row) is ExactRow for row in self.rows), "exact row types")
        object.__setattr__(self, "claimed_root_deltas", r.proof(self.claimed_root_deltas))


def exact_evidence(request):
    """Producer for bounded checks: exact certificates for the three named policies."""
    request.validate()
    final_policy = _producer_policy(request)
    rows = tuple(
        ExactRow(member.identity,
                 r.produce(member.subject, request.baseline_policy),
                 r.produce(member.subject, request.replacement_policy),
                 r.produce(member.subject, final_policy))
        for member in request.family.members)
    deltas = tuple(row.final.upper[0] - row.baseline.upper[0] for row in rows)
    return ExactEvidence(request, final_policy, rows, deltas)


def _exact_values(subject, policy, certificate):
    """Check optimum and policy equalities; never invoke an evidence producer."""
    r.consume(subject, policy, certificate)
    lower = r.table(subject, certificate.lower)
    upper = r.table(subject, certificate.upper)
    chosen = policy.validate(subject)
    for node in subject.nodes:
        if not node.actions:
            r.need(lower[node.h] == node.terminal == upper[node.h],
                   "terminal equality required for exact performance")
            continue
        backups = []
        selected = None
        for action in node.actions:
            value = action.cost + sum((probability * lower[
                node.h + ((action.label, observation),)]
                for observation, probability in action.outcomes), F(0))
            backups.append(value)
            if action.label == chosen[node.h]:
                selected = action.cost + sum((probability * upper[
                    node.h + ((action.label, observation),)]
                    for observation, probability in action.outcomes), F(0))
        r.need(lower[node.h] == min(backups), "exact modelwise optimum required")
        r.need(upper[node.h] == selected, "exact policy evaluation required")
    return lower, upper


def consume_exact(expected, intended_final_policy, evidence):
    """Check exact policy change, S17, and any claimed actual cap violation."""
    r.need(type(expected) is Request and type(intended_final_policy) is r.Policy and
           type(evidence) is ExactEvidence,
           "expected request, final policy and exact evidence")
    expected.validate()
    evidence.request.validate()
    r.need(expected == evidence.request, "wrong exact-performance request")
    final_policy = _receiver_policy(expected)
    r.need(intended_final_policy == final_policy and evidence.final_policy == final_policy,
           "wrong exact final policy")
    r.need(tuple(row.member_identity for row in evidence.rows) ==
           tuple(member.identity for member in expected.family.members),
           "wrong exact model coverage or order")
    r.need(len(evidence.claimed_root_deltas) == len(evidence.rows),
           "wrong exact delta coverage")
    modelwise, baseline_metrics, final_metrics = [], [], []
    for member, row, claimed_delta in zip(expected.family.members, evidence.rows,
                                          evidence.claimed_root_deltas):
        old_lower, old_upper = _exact_values(member.subject, expected.baseline_policy,
                                             row.baseline)
        replacement_lower, replacement_upper = _exact_values(
            member.subject, expected.replacement_policy, row.replacement)
        final_lower, final_upper = _exact_values(member.subject, final_policy, row.final)
        r.need(old_lower == replacement_lower == final_lower,
               "changed exact modelwise comparator")
        mass = _receiver_factors(member.subject, expected.baseline_policy,
                                 expected.event)[0]
        actual_delta = final_upper[()] - old_upper[()]
        r.need(claimed_delta == actual_delta, "false claimed actual policy-cost change")
        conditional_delta = replacement_upper[expected.event] - old_upper[expected.event]
        r.need(actual_delta == mass * conditional_delta,
               "single-splice actual-performance identity failed")
        if expected.cap == EXPECTED_COST_CAP:
            old_metric, final_metric = old_upper[()], final_upper[()]
        else:
            old_metric = old_upper[()] - old_lower[()]
            final_metric = final_upper[()] - final_lower[()]
        baseline_metrics.append(old_metric)
        final_metrics.append(final_metric)
        modelwise.append((member.identity, mass, old_upper[()], final_upper[()],
                          conditional_delta, actual_delta))
    violated = any(value > expected.threshold for value in final_metrics)
    return {"modelwise": tuple(modelwise),
            "baseline_metrics": tuple(baseline_metrics),
            "final_metrics": tuple(final_metrics),
            "baseline_worst": max(baseline_metrics),
            "final_worst": max(final_metrics),
            "all_members_nonworsening": all(row[5] <= 0 for row in modelwise),
            "aggregate_nonworsening": max(final_metrics) <= max(baseline_metrics),
            "cap_disposition": VIOLATION if violated else EXACT_SATISFIED}
