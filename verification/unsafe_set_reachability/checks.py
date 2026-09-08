#!/usr/bin/env python3
"""Exact positive, negative, and composition checks for unsafe reachability."""
from dataclasses import replace
from fractions import Fraction as F
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from verification.unsafe_set_reachability import reference as ref  # noqa: E402


corners, statistics, families, r = (
    ref.corners, ref.statistics, ref.families, ref.r)
rejections = 0


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def reject(operation, message):
    global rejections
    try:
        operation()
    except (ref.Invalid, statistics.Invalid, TypeError, KeyError):
        rejections += 1
        return
    raise AssertionError(message)


def collection(rows, *, precision=16, record="unsafe-statistics", revision="r1"):
    registry = tuple(statistics.make_stream(
        f"stream-{index}", f"population-{index}", f"protocol-{index}")
        for index in range(1, len(rows) + 1))
    transcript = []
    local = [0] * len(rows)
    for global_index in range(1, sum(len(row) for row in rows) + 1):
        index = (global_index - 1) % len(rows)
        check(local[index] < len(rows[index]),
              "fixture rows must fit round-robin collection")
        local[index] += 1
        transcript.append(statistics.make_observation(
            global_index, registry[index].stream_identity, local[index],
            rows[index][local[index] - 1],
            f"{record}-event-{global_index}"))
    alpha = F(1, 20)
    allocations = tuple((item.stream_identity, alpha / len(registry))
                        for item in registry)
    return statistics.make_collection(
        registry, alpha, allocations, precision_bits=precision,
        transcript=transcript, stopped=False, record=record,
        revision=revision)


def coverage(request):
    collected = statistics.produce_collection(request)
    check(statistics.consume_collection(request, collected)["status"] ==
          "checked-collection-transcript", "collection replay failed")
    evidence = statistics.produce_coverage(request, collected)
    return evidence, statistics.consume_coverage(request, evidence)


def widen_coverage(evidence):
    rows = []
    rectangle = []
    for stream, scalar in evidence.scalar_evidence:
        if scalar.claimed_k == 0:
            scalar = replace(scalar, upper_bracket=(F(0), F(1)),
                             outward_interval=(F(0), F(1)),
                             precision_claimed=False)
        elif scalar.claimed_k == scalar.claimed_n:
            scalar = replace(scalar, lower_bracket=(F(0), F(1)),
                             outward_interval=(F(0), F(1)),
                             precision_claimed=False)
        else:
            raise AssertionError("widening helper expects boundary rows")
        rows.append((stream, scalar))
        rectangle.append((stream, F(0), F(1)))
    return replace(evidence, scalar_evidence=tuple(rows),
                   rectangle=tuple(rectangle))


def policy_entries(subject, labels=None):
    policies = r.enumerate_policies(subject)
    if labels is None:
        labels = tuple(f"policy-{index}" for index in range(len(policies)))
    check(len(labels) == len(policies), "policy label count")
    return tuple(families.PolicyEntry(label, policy)
                 for label, policy in zip(labels, policies))


def risk_family():
    bad = (("aggressive", "bad"),)
    safe = (("aggressive", "safe"),)

    def subject(name, chance):
        return r.Subject(name, 1, "signed expected loss points",
                         ("supplied exact transition model",), (
            r.Node((), actions=(
                r.Action("aggressive", -2,
                         (("bad", chance), ("safe", F(1) - chance))),
                r.Action("cautious", -1),
            )),
            r.Node(bad, terminal=0),
            r.Node(safe, terminal=0),
        ))

    first = subject("risk model zero", F(0))
    second = subject("risk model positive", F(1, 10))
    family = families.Family("two persistent risk models", (
        families.Member("zero-hazard", first),
        families.Member("positive-hazard", second),
    ))
    entries = policy_entries(first, ("aggressive", "cautious"))
    return family, entries, ref.UnsafeSet("bad outcome histories", (bad,))


def transient_subject():
    middle = (("enter", "inside"),)
    end = middle + (("recover", "safe"),)
    subject = r.Subject("transient unsafe then safe terminal", 2, "loss", (), (
        r.Node((), actions=(r.Action("enter", 0, (("inside", F(1)),)),)),
        r.Node(middle, actions=(r.Action("recover", 0,
                                        (("safe", F(1)),)),)),
        r.Node(end, terminal=0),
    ))
    policy = r.Policy((((), "enter"), (middle, "recover")))
    return subject, policy, middle, end


def forced_unsafe_family():
    bad = (("go", "bad"),)
    subject = r.Subject("forced unsafe", 1, "loss", (), (
        r.Node((), actions=(r.Action("go", 0, (("bad", F(1)),)),)),
        r.Node(bad, terminal=0),
    ))
    family = families.Family("forced unsafe singleton", (
        families.Member("forced", subject),))
    entries = policy_entries(subject, ("only",))
    return family, entries, ref.UnsafeSet("forced bad", (bad,))


def hidden_oracle_family():
    first = r.Subject("hidden model A", 1, "loss", (), (
        r.Node((), actions=(r.Action("a", 0), r.Action("b", 1))),))
    second = r.Subject("hidden model B", 1, "loss", (), (
        r.Node((), actions=(r.Action("a", 1), r.Action("b", 0))),))
    family = families.Family("hidden model family", (
        families.Member("A", first), families.Member("B", second)))
    return family, policy_entries(first, ("a", "b")), ref.UnsafeSet("none", ())


def interaction_template():
    exposed = (("route", "exposed"),)
    bypass = (("route", "bypass"),)
    bad = exposed + (("risky", "bad"),)
    safe = exposed + (("risky", "safe"),)
    template = corners.Template(
        "two-parameter unsafe interaction", 2, "signed expected loss points",
        ("fixed completed observable-history skeleton",
         "parameter-independent signed costs"),
        ("p-exposure", "q-protection"), (
            corners.node((), actions=(corners.action("route", 0, (
                corners.outcome("exposed", 0, 1, "p-exposure"),
                corners.outcome("bypass", 1, -1, "p-exposure"),
            )),)),
            corners.node(exposed, actions=(
                corners.action("risky", -2, (
                    corners.outcome("bad", 1, -1, "q-protection"),
                    corners.outcome("safe", 0, 1, "q-protection"),
                )),
                corners.action("guard", -1),
            )),
            corners.node(bypass, terminal=0),
            corners.node(bad, terminal=0),
            corners.node(safe, terminal=0),
        )).validate()
    return template, ref.UnsafeSet("bad after exposure", (bad,))


def interaction_request(data, cap=F(1, 2)):
    template, unsafe = interaction_template()
    nominal = corners.instantiate(template,
                                  {"p-exposure": F(0),
                                   "q-protection": F(0)})
    entries = policy_entries(nominal, ("risky", "guard"))
    corner_request = corners.Request(
        data, template,
        # Deliberate permutation: registry order is not parameter order.
        (corners.MappingRow("stream-2", "p-exposure"),
         corners.MappingRow("stream-1", "q-protection")),
        entries, "risky", families.FULL)
    return ref.StatisticalRequest(corner_request, unsafe, cap)


def one_parameter_template():
    bad = (("test", "bad"),)
    safe = (("test", "safe"),)
    template = corners.Template("one uncertain hazard", 1, "loss", (),
                                ("p",), (
        corners.node((), actions=(corners.action("test", 0, (
            corners.outcome("bad", 0, 1, "p"),
            corners.outcome("safe", 1, -1, "p"),
        )),)),
        corners.node(bad, terminal=0),
        corners.node(safe, terminal=0),
    )).validate()
    return template, ref.UnsafeSet("bad", (bad,))


def repeated_template():
    first = (("first", "A"),)
    other = (("first", "B"),)
    bad = first + (("second", "bad"),)
    safe = first + (("second", "safe"),)
    template = corners.Template("repeated hazard parameter", 2, "loss", (),
                                ("p",), (
        corners.node((), actions=(corners.action("first", 0, (
            corners.outcome("A", 0, 1, "p"),
            corners.outcome("B", 1, -1, "p"),
        )),)),
        corners.node(first, actions=(corners.action("second", 0, (
            corners.outcome("bad", 1, -1, "p"),
            corners.outcome("safe", 0, 1, "p"),
        )),)),
        corners.node(other, terminal=0),
        corners.node(bad, terminal=0),
        corners.node(safe, terminal=0),
    )).validate()
    return template, ref.UnsafeSet("repeated bad", (bad,))


def exclusive_reuse_template():
    left = (("route", "L"),)
    right = (("route", "R"),)
    nodes = [corners.node((), actions=(corners.action("route", 0, (
        corners.outcome("L", 0, 1, "p-route"),
        corners.outcome("R", 1, -1, "p-route"),
    )),))]
    unsafe = []
    for branch in (left, right):
        bad = branch + (("hazard", "bad"),)
        safe = branch + (("hazard", "safe"),)
        nodes.append(corners.node(branch, actions=(corners.action("hazard", 0, (
            corners.outcome("bad", 0, 1, "p-hazard"),
            corners.outcome("safe", 1, -1, "p-hazard"),
        )),)))
        nodes.extend((corners.node(bad, terminal=0),
                      corners.node(safe, terminal=0)))
        unsafe.append(bad)
    template = corners.Template(
        "mutually exclusive hazard reuse", 2, "loss", (),
        ("p-route", "p-hazard"), tuple(nodes)).validate()
    return template, ref.UnsafeSet("either bad branch", tuple(unsafe))


def run():
    results = []

    def record(name, **values):
        results.append({"case": name, "status": "PASS", **values})

    # R1: backward recurrence equals a forward first-hit expansion.
    subject, policy, middle, end = transient_subject()
    unsafe = ref.UnsafeSet("transient unsafe", (middle,))
    request = ref.ReachabilityRequest(subject, "transient-model", policy,
                                      unsafe, F(1))
    certificate = ref.produce_reachability(request)
    answer = ref.consume_reachability(request, certificate)
    check(answer["root_probability"] == 1 and
          answer["first_hit_paths"] == ((middle, F(1)),),
          "transient first-hit recurrence changed")
    check(subject.nodes[1].actions,
          "reachability calculation rewrote the underlying unsafe node")
    record("R1_exact_recurrence_and_first_hit_paths",
           probability=answer["root_probability"],
           node_values=answer["node_values"])

    # R2: terminal-only inspection misses a transient unsafe visit.
    terminal_shortcut = ref.terminal_only_unsafe_probability(
        subject, policy, unsafe)
    check(terminal_shortcut == 0 and answer["root_probability"] == 1 and
          end not in unsafe.histories,
          "terminal-only shortcut did not expose transient harm")
    record("R2_terminal_only_shortcut_fails",
           exact=answer["root_probability"], terminal_only=terminal_shortcut)

    # R3: summing unsafe-node marginals double-counts the same episode.
    two_unsafe = ref.UnsafeSet("two visited unsafe histories", (middle, end))
    double_request = replace(request, unsafe_set=two_unsafe)
    double_answer = ref.consume_reachability(
        double_request, ref.produce_reachability(double_request))
    marginal_sum = ref.node_marginal_sum(subject, policy, two_unsafe)
    check(double_answer["root_probability"] == 1 and marginal_sum == 2,
          "unsafe-node marginal double-count control changed")
    record("R3_unsafe_node_sum_double_counts",
           ever_hit=double_answer["root_probability"],
           invalid_node_sum=marginal_sum)

    # R4: expected additive cost and reachability probability are distinct.
    family, entries, risk_unsafe = risk_family()
    aggressive = entries[0].policy
    model = family.members[1]
    risk_request = ref.ReachabilityRequest(
        model.subject, model.identity, aggressive, risk_unsafe, F(1, 20))
    risk_certificate = ref.produce_reachability(risk_request)
    risk_answer = ref.consume_reachability(risk_request, risk_certificate)
    expected_cost = r.path_cost(model.subject, aggressive)
    check(expected_cost == -2 and risk_answer["root_probability"] == F(1, 10)
          and not risk_answer["cap_met"],
          "expected loss was confused with unsafe reachability")
    reject(lambda: ref.consume_reachability(
        risk_request, replace(risk_certificate,
                              root_probability=F(0), cap_met=True)),
           "expected-cost-like forged reachability accepted")
    record("R4_expected_loss_is_not_reachability",
           signed_expected_cost=expected_cost,
           unsafe_probability=risk_answer["root_probability"],
           cap=risk_request.cap)

    # R5: one common policy is checked modelwise with no model weights.
    aggressive_family_request = ref.FamilyReachabilityRequest(
        family, aggressive, risk_unsafe, F(1, 20))
    aggressive_family_evidence = ref.produce_family_reachability(
        aggressive_family_request)
    aggressive_family = ref.consume_family_reachability(
        aggressive_family_request, aggressive_family_evidence)
    cautious = entries[1].policy
    cautious_request = ref.FamilyReachabilityRequest(
        family, cautious, risk_unsafe, F(1, 20))
    cautious_evidence = ref.produce_family_reachability(cautious_request)
    cautious_answer = ref.consume_family_reachability(
        cautious_request, cautious_evidence)
    check(aggressive_family["modelwise"] == (
        ("zero-hazard", F(0), True),
        ("positive-hazard", F(1, 10), False)) and
        not aggressive_family["robust_cap_met"] and
        cautious_answer["worst_probability"] == 0 and
        cautious_answer["robust_cap_met"] and
        aggressive_family["model_weights"] is None,
        "persistent-family safety semantics changed")
    reject(lambda: ref.FamilyReachabilityRequest(
        family, [aggressive, cautious], risk_unsafe, F(1, 20)),
           "hidden model-indexed policy vector accepted")
    record("R5_persistent_family_robust_cap",
           aggressive=aggressive_family["modelwise"],
           cautious=cautious_answer["modelwise"])

    # R6: the active cap changes the deterministic expected-loss winner.
    constrained_request = ref.SelectionRequest(
        family, risk_unsafe, entries, families.FULL, F(1, 20), "cautious")
    constrained_evidence = ref.produce_selection(constrained_request)
    constrained = ref.consume_selection(constrained_request,
                                        constrained_evidence)
    relaxed_request = replace(constrained_request, cap=F(1, 10),
                              named_policy_identity="aggressive")
    relaxed_evidence = ref.produce_selection(relaxed_request)
    relaxed = ref.consume_selection(relaxed_request, relaxed_evidence)
    check(constrained["cost_matrix"] == ((F(-2), F(-1)),
                                          (F(-2), F(-1))) and
          constrained["feasible_policies"] == ("cautious",) and
          constrained["minimax_loss_winners"] == ("cautious",) and
          constrained["fixed_robust_feasible_comparators"] ==
          (F(-1), F(-1)) and
          constrained["named_constrained_regret"] == 0,
          "strict-cap constrained selection changed")
    check(relaxed["feasible_policies"] == ("aggressive", "cautious") and
          relaxed["minimax_loss_winners"] == ("aggressive",) and
          relaxed["minimax_regret_winners"] == ("aggressive",) and
          relaxed["named_constrained_regret"] == 0,
          "relaxed cap did not restore lower-cost policy")
    record("R6_operational_cap_changes_policy_winner",
           strict_winner=constrained["minimax_loss_winners"],
           relaxed_winner=relaxed["minimax_loss_winners"],
           strict_feasible=constrained["feasible_policies"])

    # R7: hidden-model best actions do not form an accessible policy.
    hidden_family, hidden_entries, empty_unsafe = hidden_oracle_family()
    hidden_request = ref.SelectionRequest(
        hidden_family, empty_unsafe, hidden_entries, families.FULL, F(0), "a")
    hidden_evidence = ref.produce_selection(hidden_request)
    hidden = ref.consume_selection(hidden_request, hidden_evidence)
    check(hidden["cost_matrix"] == ((F(0), F(1)), (F(1), F(0))) and
          hidden["minimax_loss_winners"] == ("a", "b") and
          hidden["constrained_regrets"] == (("a", F(1)), ("b", F(1))) and
          not hidden["model_dependent_feasibility_used"],
          "hidden-model action control changed")
    reject(lambda: ref.FamilyReachabilityRequest(
        hidden_family, (hidden_entries[0].policy, hidden_entries[1].policy),
        empty_unsafe, F(0)), "model-indexed vector passed as one policy")
    record("R7_hidden_model_oracle_rejected",
           modelwise_best=("a", "b"), accessible_winners=("a", "b"))

    # R8: empty classes retain FULL versus subset scope.
    forced_family, forced_entries, forced_unsafe = forced_unsafe_family()
    full_empty_request = ref.SelectionRequest(
        forced_family, forced_unsafe, forced_entries, families.FULL, F(0))
    full_empty_evidence = ref.produce_selection(full_empty_request)
    full_empty = ref.consume_selection(full_empty_request, full_empty_evidence)
    subset_empty_request = replace(full_empty_request, scope=families.SUBSET)
    subset_empty_evidence = ref.produce_selection(subset_empty_request)
    subset_empty = ref.consume_selection(subset_empty_request,
                                         subset_empty_evidence)
    check(full_empty["empty_disposition"] == ref.NO_FULL_FEASIBLE and
          subset_empty["empty_disposition"] == ref.NO_SUPPLIED_FEASIBLE and
          not full_empty["feasible_policies"] and
          not subset_empty["feasible_policies"],
          "empty-class scope distinction changed")
    record("R8_empty_feasible_class_scope",
           full=full_empty["empty_disposition"],
           subset=subset_empty["empty_disposition"])

    # R9: certificate identity binds model, policy, unsafe set, and cap.
    renamed_unsafe = ref.UnsafeSet("renamed unsafe definition",
                                   risk_unsafe.histories)
    reject(lambda: ref.consume_reachability(
        replace(risk_request, unsafe_set=renamed_unsafe), risk_certificate),
           "changed unsafe-set identity borrowed old evidence")
    changed_membership = ref.UnsafeSet(
        "safe outcome reclassified unsafe", ((('aggressive', 'safe'),),))
    reject(lambda: ref.consume_reachability(
        replace(risk_request, unsafe_set=changed_membership), risk_certificate),
           "changed unsafe-set membership borrowed old evidence")
    changed_subject = replace(model.subject, name="revised risk model")
    reject(lambda: ref.consume_reachability(
        replace(risk_request, subject=changed_subject), risk_certificate),
           "changed model borrowed old reachability evidence")
    reject(lambda: ref.consume_reachability(
        replace(risk_request, policy=cautious), risk_certificate),
           "changed policy borrowed old reachability evidence")
    reject(lambda: ref.consume_reachability(
        replace(risk_request, cap=F(1, 10)), risk_certificate),
           "changed cap borrowed old cap evidence")
    record("R9_subject_policy_unsafe_set_and_cap_binding")

    # R10: two statistical parameters yield q = p(1-q), exactly at corners.
    data = collection(((0,) * 8, (1,) * 8))
    coverage_evidence, checked_coverage = coverage(data)
    check(checked_coverage["rectangle"] == (
        ("stream-1", F(0), F(43333, 65536)),
        ("stream-2", F(22203, 65536), F(1))),
        "retained PR14 rectangle changed")
    statistical_request = interaction_request(data)
    statistical_evidence = ref.produce_statistical(
        statistical_request, coverage_evidence)
    statistical = ref.consume_statistical(statistical_request,
                                          statistical_evidence)
    expected_corners = tuple(
        dict(point)["p-exposure"] * (1 - dict(point)["q-protection"])
        for point in statistical["corner_coordinates"])
    check(statistical["named_corner_reachabilities"] == expected_corners and
          max(expected_corners) == 1 and
          statistical["named_worst_reachability"] == 1 and
          not statistical["cap_met"] and
          all(row[1] == 0 for row in
              statistical["selection"]["reachability_matrix"]) and
          statistical["selection"]["feasible_policies"] == ("guard",) and
          statistical["selection"]["minimax_loss_winners"] == ("guard",) and
          statistical["rational_interior_audit_points"] == 289,
          "two-parameter first-hit corner result changed")
    check(all(cell.certificate.request.policy ==
              statistical_request.corner_request.policies[
                  0 if cell.policy_identity == "risky" else 1].policy
              for cell in statistical_evidence.selection_evidence.
              reachability_cells), "policy changed across corners")
    relaxed_stat_request = replace(statistical_request, cap=F(1))
    relaxed_stat_evidence = ref.produce_statistical(
        relaxed_stat_request, coverage_evidence)
    relaxed_stat = ref.consume_statistical(relaxed_stat_request,
                                           relaxed_stat_evidence)
    check(relaxed_stat["cap_met"] and
          relaxed_stat["selection"]["minimax_loss_winners"] == ("risky",),
          "rectangle cap was not operative in policy selection")
    record("R10_two_parameter_statistical_corner_safety",
           rectangle=statistical["mapped_rectangle"],
           corner_reachabilities=expected_corners,
           strict_winner=statistical["selection"]["minimax_loss_winners"],
           relaxed_winner=relaxed_stat["selection"]["minimax_loss_winners"],
           audit_points=statistical["rational_interior_audit_points"])

    # R11: one unconstrained parameter retains [0,1] and exact endpoint hits.
    one_data = collection(((),), record="one-unobserved")
    one_coverage_evidence, one_coverage = coverage(one_data)
    template, one_unsafe = one_parameter_template()
    nominal = corners.instantiate(template, {"p": F(0)})
    one_entries = policy_entries(nominal, ("only",))
    one_corner_request = corners.Request(
        one_data, template, (corners.MappingRow("stream-1", "p"),),
        one_entries, "only", families.FULL)
    one_request = ref.StatisticalRequest(one_corner_request, one_unsafe, F(1))
    one_evidence = ref.produce_statistical(one_request, one_coverage_evidence)
    one = ref.consume_statistical(one_request, one_evidence)
    check(one_coverage["rectangle"] == (("stream-1", F(0), F(1)),) and
          one["named_corner_reachabilities"] == (F(0), F(1)) and
          one["cap_met"], "one-parameter [0,1] safety result changed")
    record("R11_one_unobserved_parameter",
           rectangle=one["mapped_rectangle"],
           corners=one["named_corner_reachabilities"])

    # R12: same parameter at mutually exclusive nodes remains admissible.
    exclusive_data = collection(((), ()), record="exclusive-unobserved")
    exclusive_coverage_evidence, _ = coverage(exclusive_data)
    exclusive_template, exclusive_unsafe = exclusive_reuse_template()
    exclusive_nominal = corners.instantiate(
        exclusive_template, {"p-route": F(0), "p-hazard": F(0)})
    exclusive_entries = policy_entries(exclusive_nominal, ("only",))
    exclusive_corner_request = corners.Request(
        exclusive_data, exclusive_template,
        (corners.MappingRow("stream-2", "p-route"),
         corners.MappingRow("stream-1", "p-hazard")),
        exclusive_entries, "only", families.FULL)
    exclusive_request = ref.StatisticalRequest(
        exclusive_corner_request, exclusive_unsafe, F(1))
    exclusive_evidence = ref.produce_statistical(
        exclusive_request, exclusive_coverage_evidence)
    exclusive = ref.consume_statistical(exclusive_request,
                                        exclusive_evidence)
    uses = corners.complete_path_uses(exclusive_template)
    check(corners.admissible(uses) and
          len(corners.parameter_locations(exclusive_template)["p-hazard"]) == 2 and
          exclusive["named_worst_reachability"] == 1,
          "mutually exclusive parameter reuse was rejected")
    record("R12_mutually_exclusive_parameter_reuse",
           occurrences=2, warrant=exclusive["warrant"])

    # R13: repeated same-path use has p(1-p), so corner reachability fails.
    repeated, repeated_unsafe = repeated_template()
    repeated_subject = corners.instantiate(repeated, {"p": F(0)})
    repeated_entries = policy_entries(repeated_subject, ("only",))
    repeated_corner_request = corners.Request(
        one_data, repeated, (corners.MappingRow("stream-1", "p"),),
        repeated_entries, "only", families.FULL)
    repeated_request = ref.StatisticalRequest(
        repeated_corner_request, repeated_unsafe, F(1))
    repeated_evidence = ref.produce_statistical(
        repeated_request, one_coverage_evidence)
    repeated_answer = ref.consume_statistical(repeated_request,
                                              repeated_evidence)
    values = tuple(ref.first_hit_probability(
        corners.instantiate(repeated, {"p": value}),
        repeated_entries[0].policy, repeated_unsafe)
                   for value in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)))
    check(repeated_answer["status"] == ref.INVALID_CORNER_WARRANT and
          values == (F(0), F(3, 16), F(1, 4), F(3, 16), F(0)) and
          not repeated_answer["mathematical_impossibility_claimed"],
          "repeated-parameter reachability boundary changed")
    reject(lambda: ref.consume_statistical(
        repeated_request, replace(repeated_evidence,
                                  status=ref.STATISTICAL_CHECKED)),
           "repeated parameter received an exact safety corner warrant")
    record("R13_repeated_parameter_interior_maximum",
           unit_endpoints=(values[0], values[-1]),
           quarter_endpoints=(values[1], values[3]), interior=values[2],
           disposition=repeated_answer["status"])

    # R14: a loose outward rectangle is conservative yet exact over its export.
    loose_coverage = widen_coverage(coverage_evidence)
    loose_checked = statistics.consume_coverage(data, loose_coverage)
    check(all(row[1:] == (F(0), F(1)) for row in loose_checked["rectangle"]),
          "loose coverage rectangle rejected")
    loose_evidence = ref.produce_statistical(
        replace(statistical_request, cap=F(1)), loose_coverage)
    loose = ref.consume_statistical(replace(statistical_request, cap=F(1)),
                                    loose_evidence)
    check(loose["statistical"]["outward_rectangle_may_be_conservative"] and
          loose["named_worst_reachability"] == 1,
          "loose exported rectangle did not retain exact corner maximum")
    record("R14_loose_outward_rectangle",
           rectangle=loose["mapped_rectangle"], exact_over_export=True)

    # R15: mapping and statistical/subject revisions are exact bindings.
    corner_request = statistical_request.corner_request
    reject(lambda: replace(corner_request, mapping=(
        corners.MappingRow("stream-1", "q-protection"),)),
           "missing stream/parameter mapping accepted")
    reject(lambda: replace(corner_request, mapping=(
        corners.MappingRow("stream-1", "q-protection"),
        corners.MappingRow("stream-1", "p-exposure"))),
           "duplicate stream mapping accepted")
    reject(lambda: replace(corner_request, mapping=(
        corners.MappingRow("stream-1", "q-protection"),
        corners.MappingRow("stream-2", "q-protection"))),
           "duplicate parameter mapping accepted")
    reject(lambda: replace(corner_request, mapping=corner_request.mapping + (
        corners.MappingRow("ghost", "ghost"),)),
           "extra mapping identities accepted")
    successor_data = replace(data, revision_identity="r2")
    stale_stat_request = interaction_request(successor_data)
    reject(lambda: ref.produce_statistical(stale_stat_request,
                                           coverage_evidence),
           "stale statistical evidence accepted")
    changed_nodes = list(corner_request.template.nodes)
    changed_nodes[1] = replace(
        changed_nodes[1], actions=(
            replace(changed_nodes[1].actions[0], cost=F(-1)),
            changed_nodes[1].actions[1]))
    changed_template = replace(corner_request.template,
                               nodes=tuple(changed_nodes))
    changed_composition = replace(
        statistical_request,
        corner_request=replace(corner_request, template=changed_template))
    reject(lambda: ref.consume_statistical(changed_composition,
                                           statistical_evidence),
           "changed sequential model borrowed old statistical safety result")
    record("R15_mapping_revision_and_model_binding")

    # R16: alpha and delta can share a number without sharing an event.
    alpha_bad = (("act", "bad"),)
    alpha_safe = (("act", "safe"),)
    alpha_subject = r.Subject("equal-number distinction", 1, "loss", (), (
        r.Node((), actions=(r.Action("act", 0, (
            ("bad", F(1, 20)), ("safe", F(19, 20)))),)),
        r.Node(alpha_bad, terminal=0), r.Node(alpha_safe, terminal=0)))
    alpha_policy = r.Policy((((), "act"),))
    alpha_unsafe = ref.UnsafeSet("bad", (alpha_bad,))
    alpha_request = ref.ReachabilityRequest(
        alpha_subject, "equal-number model", alpha_policy, alpha_unsafe,
        F(1, 20))
    alpha_answer = ref.consume_reachability(
        alpha_request, ref.produce_reachability(alpha_request))
    check(data.total_alpha == F(1, 20) and
          alpha_answer["root_probability"] == F(1, 20),
          "equal-number probability control changed")
    reject(lambda: ref.reject_probability_merge(
        data.total_alpha, alpha_answer["root_probability"]),
           "coverage failure and harm probability were merged")
    record("R16_alpha_and_delta_are_different_events",
           coverage_failure_alpha=data.total_alpha,
           unsafe_reachability_delta=alpha_answer["root_probability"],
           sum_not_certified=True)

    # R17: retained evidence checks with every candidate producer disabled.
    saved = (ref.produce_reachability, ref.produce_family_reachability,
             ref.produce_selection, ref.produce_statistical,
             corners.produce, families.choose, r.produce,
             statistics.produce_collection, statistics.produce_coverage)

    def disabled(*args, **kwargs):
        raise RuntimeError("candidate producer invoked")

    try:
        ref.produce_reachability = ref.produce_family_reachability = disabled
        ref.produce_selection = ref.produce_statistical = disabled
        corners.produce = families.choose = r.produce = disabled
        statistics.produce_collection = statistics.produce_coverage = disabled
        check(ref.consume_reachability(request, certificate) == answer,
              "producer-disabled reachability receiver changed")
        check(ref.consume_family_reachability(
            cautious_request, cautious_evidence) == cautious_answer,
            "producer-disabled family receiver changed")
        check(ref.consume_selection(constrained_request,
                                    constrained_evidence) == constrained,
              "producer-disabled selection receiver changed")
        check(ref.consume_statistical(statistical_request,
                                      statistical_evidence) == statistical,
              "producer-disabled statistical receiver changed")
        check(ref.consume_statistical(repeated_request, repeated_evidence) ==
              repeated_answer,
              "producer-disabled boundary receiver changed")
    finally:
        (ref.produce_reachability, ref.produce_family_reachability,
         ref.produce_selection, ref.produce_statistical,
         corners.produce, families.choose, r.produce,
         statistics.produce_collection,
         statistics.produce_coverage) = saved
    record("R17_receivers_run_with_candidate_producers_disabled")

    # Cross-cutting exactness and stale-result forgeries.
    reject(lambda: ref.ReachabilityRequest(
        subject, "model", policy, unsafe, 0.1), "float cap accepted")
    reject(lambda: ref.UnsafeSet("unknown", (("ghost", "history"),)).validate(
        subject), "unknown unsafe history accepted")
    reject(lambda: ref.UnsafeSet("duplicate", (middle, middle)),
           "duplicate unsafe history accepted")
    reject(lambda: ref.consume_selection(
        constrained_request, replace(constrained_evidence,
                                     feasible_policies=("aggressive",))),
           "forged robust-feasible class accepted")
    reject(lambda: ref.consume_selection(
        constrained_request, replace(
            constrained_evidence,
            constrained_comparators=(F(-2), F(-2)))),
           "model-dependent or wrong constrained comparator accepted")
    record("R18_exact_inputs_and_forged_claim_rejections")

    print(json.dumps(ref.wire({
        "status": "passed", "passed": len(results), "failed": 0,
        "rejections": rejections, "optimized": sys.flags.optimize,
        "results": results,
    }), sort_keys=True))


if __name__ == "__main__":
    run()
