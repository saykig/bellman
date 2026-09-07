"""Anchored certificate transport on identical completed observable-history trees."""
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "sequential_certificates"))
import reference as r

GUARANTEE = "expected-additive-total-cost-regret"

def skeleton(s):
    r.need(type(s) is r.Subject, "exact subject required")
    s.validate()
    return (s.horizon, s.unit, tuple(
        (n.h, tuple((a.label, tuple(o for o, _ in a.outcomes)) for a in n.actions))
        for n in s.nodes))

@dataclass(frozen=True)
class Correspondence:
    pairs: tuple
    def __post_init__(self):
        r.need(type(self.pairs) in (list, tuple), "correspondence rows")
        rows = []
        for row in self.pairs:
            r.need(type(row) in (list, tuple) and len(row) == 2, "history correspondence pair")
            rows.append((r.history(row[0]), r.history(row[1])))
        object.__setattr__(self, "pairs", tuple(rows))

def identity(s):
    skeleton(s)
    return Correspondence(tuple((n.h, n.h) for n in s.nodes))

@dataclass(frozen=True)
class Request:
    source: r.Subject
    source_policy: r.Policy
    source_certificate: r.Certificate
    target: r.Subject
    target_policy: r.Policy
    correspondence: Correspondence
    guarantee: str = GUARANTEE
    def __post_init__(self):
        self.validate()
    def validate(self):
        r.need(type(self.source_policy) is r.Policy and type(self.target_policy) is r.Policy,
               "total deterministic policies required")
        r.need(type(self.source_certificate) is r.Certificate, "source certificate required")
        r.need(type(self.correspondence) is Correspondence, "explicit correspondence required")
        r.need(type(self.guarantee) is str and self.guarantee == GUARANTEE, "unsupported criterion")
        sk = skeleton(self.source)
        tk = skeleton(self.target)
        self.source_policy.validate(self.source)
        self.target_policy.validate(self.target)
        r.consume(self.source, self.source_policy, self.source_certificate)
        r.need(sk == tk, "unsupported structure, information keys, menus, order, horizon or unit")
        r.need(self.correspondence.pairs == tuple((n.h, n.h) for n in self.source.nodes),
               "only complete ordered identity correspondence supported")
        return self

@dataclass(frozen=True)
class Transport:
    request: Request
    certificate: r.Certificate
    alpha: tuple
    beta: tuple
    def __post_init__(self):
        r.need(type(self.request) is Request and type(self.certificate) is r.Certificate, "transport types")
        object.__setattr__(self, "alpha", r.proof(self.alpha))
        object.__setattr__(self, "beta", r.proof(self.beta))

def transport(request):
    """Producer: correction recurrence. Does not replace receiver checking."""
    request.validate()
    s, old = request.target, request.source_certificate
    L, U = r.table(s, old.lower), r.table(s, old.upper)
    chosen = request.target_policy.validate(s)
    alpha, beta = {}, {}
    for n in sorted(s.nodes, key=lambda n: len(n.h), reverse=True):
        if not n.actions:
            alpha[n.h] = max(F(0), L[n.h] - n.terminal)
            beta[n.h] = max(F(0), n.terminal - U[n.h])
        else:
            def expectation(a, values):
                return sum((p * values[n.h + ((a.label, o),)] for o, p in a.outcomes), F(0))
            alpha[n.h] = max([F(0)] + [
                L[n.h] - a.cost - expectation(a, L) + expectation(a, alpha) for a in n.actions])
            a = next(a for a in n.actions if a.label == chosen[n.h])
            beta[n.h] = max(F(0), a.cost + expectation(a, U) - U[n.h] + expectation(a, beta))
    aa = tuple(alpha[n.h] for n in s.nodes)
    bb = tuple(beta[n.h] for n in s.nodes)
    cert = r.Certificate(s, request.target_policy,
                         tuple(x-a for x,a in zip(old.lower, aa)),
                         tuple(x+b for x,b in zip(old.upper, bb)))
    return Transport(request, cert, aa, bb)

def consume_transport(expected, evidence):
    """Receiver: original consumer plus local envelope equations; no producer calls."""
    r.need(type(expected) is Request and type(evidence) is Transport, "expected request and evidence")
    expected.validate()
    evidence.request.validate()
    r.need(expected == evidence.request, "wrong transport provenance/request")
    s, pi, cert = expected.target, expected.target_policy, evidence.certificate
    answer = r.consume(s, pi, cert)
    aa, bb = r.table(s, evidence.alpha), r.table(s, evidence.beta)
    L, U = r.table(s, expected.source_certificate.lower), r.table(s, expected.source_certificate.upper)
    lo, up = r.table(s, cert.lower), r.table(s, cert.upper)
    chosen = pi.validate(s)
    for n in s.nodes:
        h = n.h
        r.need(aa[h] >= 0 and bb[h] >= 0, "nonnegative corrections")
        r.need(lo[h] == L[h]-aa[h] and up[h] == U[h]+bb[h], "correction/table binding")
        if not n.actions:
            lower, upper = min(L[h], n.terminal), max(U[h], n.terminal)
        else:
            lows, selected_upper = [], None
            for a in n.actions:
                value = a.cost
                high = a.cost
                for o, p in a.outcomes:
                    child = h + ((a.label, o),)
                    value += p * lo[child]
                    high += p * up[child]
                lows.append(value)
                if a.label == chosen[h]:
                    selected_upper = high
            lower, upper = min([L[h]] + lows), max(U[h], selected_upper)
        r.need(lo[h] == lower and up[h] == upper, "not the anchored extremal envelope")
    return dict(answer, warrant="checked target certificate and anchored transport")

@dataclass(frozen=True)
class ContinuationQuery:
    subject: r.Subject
    prefix_policy: r.Policy
    continuation_policy: r.Policy
    event: tuple  # The event IS this exact action/observation history.
    def __post_init__(self):
        object.__setattr__(self, "event", r.history(self.event))
        self.validate()
    def validate(self):
        skeleton(self.subject)
        r.need(type(self.prefix_policy) is r.Policy and type(self.continuation_policy) is r.Policy,
               "explicit prefix and continuation policies")
        self.prefix_policy.validate(self.subject)
        self.continuation_policy.validate(self.subject)
        r.need(self.event in {n.h for n in self.subject.nodes}, "unknown prefix event")
        return self

@dataclass(frozen=True)
class ContinuationEvidence:
    query: ContinuationQuery
    certificate: r.Certificate
    mass: F
    def __post_init__(self):
        r.need(type(self.query) is ContinuationQuery and type(self.certificate) is r.Certificate,
               "continuation evidence types")
        r.need(type(self.mass) is F, "exact Fraction prefix mass")

def consume_continuation(expected, evidence):
    r.need(type(expected) is ContinuationQuery and type(evidence) is ContinuationEvidence,
           "expected continuation query and evidence")
    expected.validate()
    evidence.query.validate()
    r.need(expected == evidence.query, "different target, event or prefix policy")
    s = expected.subject
    r.consume(s, expected.continuation_policy, evidence.certificate)
    chosen = expected.prefix_policy.validate(s)
    nodes = {n.h:n for n in s.nodes}
    h, mass = (), F(1)
    for action, observation in expected.event:
        n = nodes[h]
        if not n.actions or chosen[h] != action:
            mass = F(0)
            break
        a = next(a for a in n.actions if a.label == action)
        mass *= dict(a.outcomes).get(observation, F(0))
        h += ((action, observation),)
    r.need(mass == evidence.mass, "claimed mass is not induced by target and prefix policy")
    r.need(mass > 0, "impossible conditioning; completed node is not a posterior")
    lo = r.table(s, evidence.certificate.lower)[expected.event]
    up = r.table(s, evidence.certificate.upper)[expected.event]
    return dict(prefix_mass=mass, optimum_lower=lo, policy_upper=up, regret_upper=up-lo)
