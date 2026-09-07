"""Exact bounded Bernoulli confidence and static-decision certificates.

The producer uses dyadic bisection.  The consumers recompute tail inequalities
and affine risk extrema without calling either producer.  All calculations are
deterministic standard-library Fraction arithmetic; no empirical premise is
validated by this module.
"""
from dataclasses import dataclass, asdict
from fractions import Fraction as F
from math import comb
import hashlib
import json
import re


IID_PREMISE = "iid-bernoulli-one-fixed-real-parameter"
SPENDING_RULE = "alpha/[2*n*(n+1)]-per-tail"
DECISION_QUERY = "outward-interval-and-named-action-regret"
INTERVAL_CLAIM = "outward-enclosure-of-anytime-binomial-interval"
DECISION_CLAIM = "exact-affine-risk-certificate-on-retained-interval"
MAX_N = 128
MAX_ACTIONS = 4
MAX_BISECTION_BITS = 64


class Invalid(ValueError):
    """The subject or proposed certificate is invalid."""


def need(ok, message):
    if not ok:
        raise Invalid(message)


def rational(value):
    """Normalize exact external input; reject floats and Boolean integers."""
    need(type(value) in (int, str, F), "exact rational input required")
    if isinstance(value, str):
        need(re.fullmatch(r"-?[0-9]+(?:/[1-9][0-9]*)?", value) is not None,
             "integer or fraction spelling required")
    result = F(value)
    need(max(abs(result.numerator).bit_length(), result.denominator.bit_length()) <= 256,
         "external rational input bit limit")
    return result


def exact(value, message="exact Fraction proof coordinate required"):
    """Check a derived proof coordinate without an external-input bit cap."""
    need(type(value) is F, message)
    return value


def strict_integer(value, message="strict integer required"):
    need(type(value) is int, message)
    return value


def identity(value, message="nonempty identity required"):
    need(type(value) is str and bool(value), message)
    return value


@dataclass(frozen=True)
class SamplingRequest:
    stream_identity: str
    population_identity: str
    protocol_identity: str
    observations: tuple
    premise: str
    alpha: F
    spending_rule: str
    precision_bits: int

    def __post_init__(self):
        object.__setattr__(self, "observations", tuple(self.observations))

    def validate(self):
        for value in (self.stream_identity, self.population_identity,
                      self.protocol_identity):
            identity(value)
        need(self.premise == IID_PREMISE, "unsupported sampling premise")
        need(self.spending_rule == SPENDING_RULE, "unsupported spending rule")
        need(type(self.alpha) is F and 0 < self.alpha < 1,
             "alpha must be an exact Fraction in (0,1)")
        rational(self.alpha)
        need(all(type(value) is int and value in (0, 1)
                 for value in self.observations),
             "complete ordered binary prefix required")
        strict_integer(self.precision_bits, "strict integer precision required")
        need(self.precision_bits >= 0, "nonnegative precision required")
        return self


def make_sampling(observations, alpha=F(1, 20), *, stream="stream-1",
                  population="population-1", protocol="protocol-1",
                  premise=IID_PREMISE, spending_rule=SPENDING_RULE,
                  precision_bits=16):
    return SamplingRequest(stream, population, protocol, tuple(observations), premise,
                           rational(alpha), spending_rule, precision_bits).validate()


@dataclass(frozen=True)
class Action:
    label: str
    losses: tuple

    def __post_init__(self):
        object.__setattr__(self, "losses", tuple(self.losses))

    def validate(self):
        identity(self.label, "nonempty action label required")
        need(len(self.losses) == 2 and all(type(value) is F for value in self.losses),
             "two normalized exact action losses required")
        for value in self.losses:
            rational(value)
        return self


def make_action(label, losses):
    return Action(label, tuple(rational(value) for value in losses)).validate()


@dataclass(frozen=True)
class DecisionRequest:
    sampling: SamplingRequest
    actions: tuple
    loss_unit: str
    intended_action: str
    query: str = DECISION_QUERY

    def __post_init__(self):
        object.__setattr__(self, "actions", tuple(self.actions))

    def validate(self):
        need(type(self.sampling) is SamplingRequest, "sampling request required")
        self.sampling.validate()
        identity(self.loss_unit, "nonempty loss unit required")
        need(self.query == DECISION_QUERY, "unsupported decision query")
        need(bool(self.actions) and all(type(action) is Action for action in self.actions),
             "nonempty exact action table required")
        for action in self.actions:
            action.validate()
        labels = tuple(action.label for action in self.actions)
        need(len(set(labels)) == len(labels), "duplicate action label")
        need(type(self.intended_action) is str and self.intended_action in labels,
             "independently intended action required")
        return self


def make_decision(sampling, actions, *, unit="loss", intended_action,
                  query=DECISION_QUERY):
    normalized = tuple(action if type(action) is Action
                       else make_action(action[0], action[1]) for action in actions)
    return DecisionRequest(sampling, normalized, unit, intended_action, query).validate()


def sampling_budget(request):
    request.validate()
    if len(request.observations) > MAX_N:
        return {"status": "unfinished", "reason": "sample-size-limit",
                "limit": MAX_N, "requested": len(request.observations)}
    if request.precision_bits > MAX_BISECTION_BITS:
        return {"status": "unfinished", "reason": "bisection-precision-limit",
                "limit": MAX_BISECTION_BITS, "requested": request.precision_bits}
    return None


def decision_budget(request):
    request.validate()
    prior = sampling_budget(request.sampling)
    if prior:
        return prior
    if len(request.actions) > MAX_ACTIONS:
        return {"status": "unfinished", "reason": "action-count-limit",
                "limit": MAX_ACTIONS, "requested": len(request.actions)}
    return None


def epsilon(alpha, n):
    alpha = exact(alpha, "exact Fraction alpha required")
    strict_integer(n)
    need(0 < alpha < 1 and n >= 1, "positive time and valid alpha required")
    return alpha / (2 * n * (n + 1))


def _tail_inputs(n, k, q):
    strict_integer(n)
    strict_integer(k)
    q = exact(q)
    need(n >= 0 and 0 <= k <= n and 0 <= q <= 1, "invalid binomial tail input")
    return q


def tail_plus(n, k, q):
    """P_q(K >= k), evaluated by the direct binomial sum."""
    q = _tail_inputs(n, k, q)
    return sum((F(comb(n, j)) * q**j * (1 - q)**(n - j)
                for j in range(k, n + 1)), F(0))


def tail_minus(n, k, q):
    """P_q(K <= k), evaluated by the direct binomial sum."""
    q = _tail_inputs(n, k, q)
    return sum((F(comb(n, j)) * q**j * (1 - q)**(n - j)
                for j in range(k + 1)), F(0))


def prefix_digest(request):
    request.validate()
    payload = {
        "stream": request.stream_identity,
        "population": request.population_identity,
        "protocol": request.protocol_identity,
        "observations": request.observations,
        "premise": request.premise,
        "alpha": str(request.alpha),
        "spending": request.spending_rule,
        "precision_bits": request.precision_bits,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def decision_digest(request):
    request.validate()
    payload = {
        "sampling": prefix_digest(request.sampling),
        "actions": tuple((action.label, tuple(str(x) for x in action.losses))
                         for action in request.actions),
        "unit": request.loss_unit,
        "intended_action": request.intended_action,
        "query": request.query,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class IntervalEvidence:
    subject: SamplingRequest
    claimed_n: int
    claimed_k: int
    per_tail_allowance: object
    lower_bracket: tuple
    upper_bracket: tuple
    outward_interval: tuple
    precision_claimed: bool
    subject_digest: str
    claim: str = INTERVAL_CLAIM

    def __post_init__(self):
        for name in ("lower_bracket", "upper_bracket", "outward_interval"):
            object.__setattr__(self, name, tuple(getattr(self, name)))


def _bisect_lower(n, k, allowance, bits):
    lower, upper = F(0), F(1)
    for _ in range(bits):
        middle = (lower + upper) / 2
        if tail_plus(n, k, middle) <= allowance:
            lower = middle
        else:
            upper = middle
    return lower, upper


def _bisect_upper(n, k, allowance, bits):
    lower, upper = F(0), F(1)
    for _ in range(bits):
        middle = (lower + upper) / 2
        if tail_minus(n, k, middle) >= allowance:
            lower = middle
        else:
            upper = middle
    return lower, upper


def produce_interval(request):
    """Produce dyadic root brackets or a typed resource refusal."""
    request.validate()
    refusal = sampling_budget(request)
    if refusal:
        return refusal
    n = len(request.observations)
    k = sum(request.observations)
    if n == 0:
        allowance = None
        lower, upper = (F(0), F(0)), (F(1), F(1))
    else:
        allowance = epsilon(request.alpha, n)
        lower = (F(0), F(0)) if k == 0 else _bisect_lower(
            n, k, allowance, request.precision_bits)
        upper = (F(1), F(1)) if k == n else _bisect_upper(
            n, k, allowance, request.precision_bits)
    return IntervalEvidence(request, n, k, allowance, lower, upper,
                            (lower[0], upper[1]), True,
                            prefix_digest(request))


def _proof_pair(values, message):
    need(type(values) is tuple and len(values) == 2, message)
    return exact(values[0]), exact(values[1])


def consume_interval(expected, evidence):
    """Verify outward root brackets exactly without invoking bisection."""
    expected.validate()
    need(type(evidence) is IntervalEvidence, "interval evidence required")
    need(type(evidence.subject) is SamplingRequest, "sampling subject required")
    evidence.subject.validate()
    need(evidence.subject == expected, "sampling subject mismatch")
    need(evidence.claim == INTERVAL_CLAIM, "unsupported interval claim")
    need(type(evidence.subject_digest) is str and
         evidence.subject_digest == prefix_digest(expected), "sampling digest mismatch")
    n, k = len(expected.observations), sum(expected.observations)
    strict_integer(evidence.claimed_n, "strict claimed n required")
    strict_integer(evidence.claimed_k, "strict claimed k required")
    need((evidence.claimed_n, evidence.claimed_k) == (n, k),
         "candidate counts do not match complete prefix")
    need(type(evidence.precision_claimed) is bool, "precision claim flag required")
    a, b = _proof_pair(evidence.lower_bracket, "complete lower root bracket required")
    c, d = _proof_pair(evidence.upper_bracket, "complete upper root bracket required")
    left, right = _proof_pair(evidence.outward_interval,
                              "complete outward interval required")
    need(all(0 <= value <= 1 for value in (a, b, c, d, left, right)),
         "probability coordinate outside [0,1]")
    need(a <= b and c <= d and left <= right, "reversed interval or bracket")
    need((left, right) == (a, d), "outward interval does not match root witnesses")
    if n == 0:
        need(evidence.per_tail_allowance is None, "n=0 has no tail allocation")
        need((a, b, c, d, left, right) ==
             (F(0), F(0), F(1), F(1), F(0), F(1)),
             "n=0 boundary interval must be [0,1]")
        widths = ()
    else:
        allowance = epsilon(expected.alpha, n)
        need(type(evidence.per_tail_allowance) is F and
             evidence.per_tail_allowance == allowance, "wrong per-tail allocation")
        if k == 0:
            need((a, b) == (F(0), F(0)), "zero-success lower boundary must be zero")
        else:
            need(tail_plus(n, k, a) <= allowance <= tail_plus(n, k, b),
                 "invalid lower outward root bracket")
        if k == n:
            need((c, d) == (F(1), F(1)), "all-success upper boundary must be one")
        else:
            need(tail_minus(n, k, c) >= allowance >= tail_minus(n, k, d),
                 "invalid upper outward root bracket")
        widths = tuple(width for width, nontrivial in
                       ((b - a, k > 0), (d - c, k < n)) if nontrivial)
    obligation = F(1, 2**expected.precision_bits)
    precision_met = all(width <= obligation for width in widths)
    if evidence.precision_claimed:
        need(precision_met, "false bracket-precision claim")
    status = ("outward-enclosure-precision-certified" if precision_met
              else "valid-coarse-outward-enclosure")
    return {
        "status": status,
        "n": n,
        "k": k,
        "per_tail_allowance": evidence.per_tail_allowance,
        "fixed_time_exclusion_upper": (F(0) if n == 0
                                         else 2 * evidence.per_tail_allowance),
        "simultaneous_coverage_lower": 1 - expected.alpha,
        "outward_interval": (left, right),
        "requested_precision_met": precision_met,
        "precision_claimed": evidence.precision_claimed,
        "sampling_premise_checked_as_input_not_empirically_validated": True,
    }


def risk(action, probability):
    action.validate()
    probability = exact(probability)
    need(0 <= probability <= 1, "probability outside [0,1]")
    return (1 - probability) * action.losses[0] + probability * action.losses[1]


def pairwise_extreme(request, interval, first, second):
    request.validate()
    interval = _proof_pair(tuple(interval), "probability interval required")
    need(interval[0] <= interval[1], "empty probability interval")
    actions = {action.label: action for action in request.actions}
    need(first in actions and second in actions, "unknown action comparison")
    differences = tuple(risk(actions[first], endpoint) - risk(actions[second], endpoint)
                        for endpoint in interval)
    return max(differences)


@dataclass(frozen=True)
class DecisionEvidence:
    subject: DecisionRequest
    interval_evidence: IntervalEvidence
    pairwise_extrema: tuple
    common_minimizers: tuple
    uniformly_strict_actions: tuple
    named_action: str
    named_action_regret: F
    subject_digest: str
    claim: str = DECISION_CLAIM

    def __post_init__(self):
        object.__setattr__(self, "pairwise_extrema",
                           tuple(tuple(row) for row in self.pairwise_extrema))
        object.__setattr__(self, "common_minimizers", tuple(self.common_minimizers))
        object.__setattr__(self, "uniformly_strict_actions",
                           tuple(self.uniformly_strict_actions))


def _decision_values(request, interval):
    labels = tuple(action.label for action in request.actions)
    rows = tuple((first, second,
                  pairwise_extreme(request, interval, first, second))
                 for first in labels for second in labels)
    values = {(first, second): value for first, second, value in rows}
    common = tuple(first for first in labels
                   if all(values[first, second] <= 0 for second in labels))
    strict = tuple(first for first in labels
                   if all(values[first, second] < 0
                          for second in labels if second != first))
    regret = max(values[request.intended_action, second] for second in labels)
    need(regret >= 0, "self-comparison must make regret nonnegative")
    return rows, common, strict, regret


def produce_decision(request, interval_evidence):
    request.validate()
    refusal = decision_budget(request)
    if refusal:
        return refusal
    checked = consume_interval(request.sampling, interval_evidence)
    rows, common, strict, regret = _decision_values(
        request, checked["outward_interval"])
    return DecisionEvidence(request, interval_evidence, rows, common, strict,
                            request.intended_action, regret,
                            decision_digest(request))


def consume_decision(expected, evidence):
    """Recompute all affine endpoint extrema and the complete common set."""
    expected.validate()
    need(type(evidence) is DecisionEvidence, "decision evidence required")
    need(type(evidence.subject) is DecisionRequest, "decision subject required")
    evidence.subject.validate()
    need(evidence.subject == expected, "decision subject mismatch")
    need(evidence.claim == DECISION_CLAIM, "unsupported decision claim")
    need(evidence.subject_digest == decision_digest(expected), "decision digest mismatch")
    checked = consume_interval(expected.sampling, evidence.interval_evidence)
    expected_rows, common, strict, regret = _decision_values(
        expected, checked["outward_interval"])
    need(len(evidence.pairwise_extrema) == len(expected_rows),
         "incomplete pairwise action coverage")
    for row in evidence.pairwise_extrema:
        need(len(row) == 3 and type(row[0]) is str and type(row[1]) is str and
             type(row[2]) is F, "exact pairwise row required")
    need(evidence.pairwise_extrema == expected_rows,
         "false or reordered pairwise extrema")
    need(evidence.common_minimizers == common,
         "false complete common-minimizer set")
    need(evidence.uniformly_strict_actions == strict,
         "false uniform-strictness claim")
    need(evidence.named_action == expected.intended_action,
         "wrong named action")
    need(type(evidence.named_action_regret) is F and
         evidence.named_action_regret == regret,
         "false named-action regret")
    labels = tuple(action.label for action in expected.actions)
    return {
        "status": "checked-decision-certificate",
        "outward_interval": checked["outward_interval"],
        "common_minimizers": common,
        "uniformly_strict_actions": strict,
        "strictness_vacuous_for_singleton": len(labels) == 1,
        "intended_action": expected.intended_action,
        "intended_action_uniformly_optimal": expected.intended_action in common,
        "intended_action_uniformly_strict": expected.intended_action in strict,
        "named_action_regret": regret,
        "loss_unit": expected.loss_unit,
        "coverage_alpha": expected.sampling.alpha,
        "coverage_and_loss_not_combined": True,
    }


def first_exclusion_probability(horizon, probability, alpha, allocation):
    """Exact dynamic recursion over paths not previously excluded."""
    strict_integer(horizon, "strict integer horizon required")
    probability, alpha = exact(probability), exact(alpha)
    need(0 <= horizon <= MAX_N and 0 <= probability <= 1 and 0 < alpha < 1,
         "invalid repeated-inspection input")
    need(allocation in ("fixed-equal-tailed", SPENDING_RULE),
         "unknown tail allocation")
    alive = {0: F(1)}
    excluded = F(0)
    first_by_time = []
    for n in range(1, horizon + 1):
        next_alive = {}
        first = F(0)
        allowance = alpha / 2 if allocation == "fixed-equal-tailed" else epsilon(alpha, n)
        for k, mass in alive.items():
            for observation, chance in ((0, 1 - probability), (1, probability)):
                new_k, new_mass = k + observation, mass * chance
                if (tail_plus(n, new_k, probability) < allowance or
                        tail_minus(n, new_k, probability) < allowance):
                    first += new_mass
                else:
                    next_alive[new_k] = next_alive.get(new_k, F(0)) + new_mass
        excluded += first
        first_by_time.append(first)
        alive = next_alive
    surviving = sum(alive.values(), F(0))
    need(excluded + surviving == 1, "probability conservation failure")
    return {"excluded": excluded, "surviving": surviving,
            "first_exclusion_by_time": tuple(first_by_time)}


def allocated_failure(alpha, horizon):
    alpha = exact(alpha)
    strict_integer(horizon)
    need(0 < alpha < 1 and horizon >= 0, "invalid allocation request")
    return sum((2 * epsilon(alpha, n) for n in range(1, horizon + 1)), F(0))


def classify_sampling_revision(previous, current):
    previous.validate()
    current.validate()
    identities = ("stream_identity", "population_identity", "protocol_identity", "premise")
    if any(getattr(previous, name) != getattr(current, name) for name in identities):
        return "new-sampling-subject"
    if (previous.alpha, previous.spending_rule) != (current.alpha, current.spending_rule):
        return "new-coverage-specification"
    if current.observations == previous.observations:
        return "same-prefix-recalculation-no-new-evidence"
    if (len(current.observations) > len(previous.observations) and
            current.observations[:len(previous.observations)] == previous.observations):
        return "append-only-observation-extension"
    return "corrected-or-retroselected-history-new-claim"


def classify_decision_revision(previous, current):
    previous.validate()
    current.validate()
    sample = classify_sampling_revision(previous.sampling, current.sampling)
    if sample != "same-prefix-recalculation-no-new-evidence":
        return sample
    if (previous.actions, previous.loss_unit, previous.intended_action,
            previous.query) != (current.actions, current.loss_unit,
                                current.intended_action, current.query):
        return "same-data-new-decision-query"
    return "same-subject-recalculation-no-new-evidence"


def wire(value):
    if isinstance(value, F):
        return str(value)
    if hasattr(value, "__dataclass_fields__"):
        return wire(asdict(value))
    if isinstance(value, dict):
        return {str(key): wire(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [wire(item) for item in value]
    return value
