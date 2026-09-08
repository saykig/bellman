#!/usr/bin/env python3
"""Independent exact cases for statistical rectangle/corner composition."""
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from verification.statistical_corner_models import reference as ref


s, f, r = ref.statistics, ref.families, ref.r
rejections = 0
unfinished = 0


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def reject(operation, message):
    global rejections
    try:
        operation()
    except (ref.Invalid, s.Invalid, TypeError, KeyError):
        rejections += 1
        return
    raise AssertionError(message)


def expect_unfinished(value, reason):
    global unfinished
    check(value["status"] == "unfinished" and value["kind"] == "resource-refusal" and
          value["reason"] == reason, f"wrong unfinished result: {reason}")
    unfinished += 1


def collection(rows, *, precision=16, record="corner-data", revision="r1"):
    registry = tuple(s.make_stream(f"stream-{index}", f"population-{index}",
                                   f"protocol-{index}")
                     for index in range(1, len(rows) + 1))
    transcript = []
    local = [0] * len(rows)
    for global_index in range(1, sum(len(row) for row in rows) + 1):
        index = (global_index - 1) % len(rows)
        check(local[index] < len(rows[index]), "rows must fit round-robin order")
        local[index] += 1
        transcript.append(s.make_observation(
            global_index, registry[index].stream_identity, local[index],
            rows[index][local[index] - 1], f"{record}-event-{global_index}"))
    alpha = F(1, 20)
    allocations = tuple((item.stream_identity, alpha / len(registry))
                        for item in registry)
    return s.make_collection(registry, alpha, allocations,
                             precision_bits=precision, transcript=transcript,
                             stopped=False, record=record, revision=revision)


def coverage(request):
    collected = s.produce_collection(request)
    checked = s.consume_collection(request, collected)
    check(checked["status"] == "checked-collection-transcript",
          "collection did not replay")
    evidence = s.produce_coverage(request, collected)
    return evidence, s.consume_coverage(request, evidence)


def headline_template():
    L = (("route", "L"),)
    R = (("route", "R"),)
    return ref.Template(
        "two-parameter follow-up", 2, "signed expected loss points",
        ("fixed observable-history skeleton", "parameter-independent costs"),
        ("p-route", "p-followup"),
        (
            ref.node((), actions=(ref.action("route", 2, (
                ref.outcome("L", 0, 1, "p-route"),
                ref.outcome("R", 1, -1, "p-route"),
            )),)),
            ref.node(L, actions=(
                ref.action("hold", -2),
                ref.action("inspect", -2, (
                    ref.outcome("hit", 0, 1, "p-followup"),
                    ref.outcome("miss", 1, -1, "p-followup"),
                )),
            )),
            ref.node(R, actions=(
                ref.action("hold", -1),
                ref.action("inspect", -2, (
                    ref.outcome("hit", 0, 1, "p-followup"),
                    ref.outcome("miss", 1, -1, "p-followup"),
                )),
            )),
            ref.node(L + (("inspect", "hit"),), terminal=1),
            ref.node(L + (("inspect", "miss"),), terminal=0),
            ref.node(R + (("inspect", "hit"),), terminal=2),
            ref.node(R + (("inspect", "miss"),), terminal=0),
        )).validate()


def policy_entries(template):
    subject = ref.instantiate(template, {parameter: F(0)
                                         for parameter in template.parameters})
    entries = []
    for policy in r.enumerate_policies(subject):
        chosen = dict(policy.choices)
        left = chosen[(("route", "L"),)]
        right = chosen[(("route", "R"),)]
        entries.append(f.PolicyEntry(f"{left}-{right}", policy))
    return tuple(entries)


def headline_request(data):
    template = headline_template()
    return ref.Request(
        data, template,
        # Registry order is deliberately not parameter order.
        (ref.MappingRow("stream-2", "p-route"),
         ref.MappingRow("stream-1", "p-followup")),
        policy_entries(template), "hold-inspect", f.FULL,
        expected_loss_cap=F(1), regret_cap=F(1, 4))


def direct_family_matrix(evidence, entries):
    return tuple(tuple(r.path_cost(member.subject, entry.policy)
                       for entry in entries)
                 for member in evidence.family.members)


def widen_coverage(evidence):
    widened = []
    rectangle = []
    for stream, scalar_evidence in evidence.scalar_evidence:
        if scalar_evidence.claimed_k == 0:
            scalar_evidence = replace(
                scalar_evidence, upper_bracket=(F(0), F(1)),
                outward_interval=(F(0), F(1)), precision_claimed=False)
        elif scalar_evidence.claimed_k == scalar_evidence.claimed_n:
            scalar_evidence = replace(
                scalar_evidence, lower_bracket=(F(0), F(1)),
                outward_interval=(F(0), F(1)), precision_claimed=False)
        else:
            raise AssertionError("widening helper expects boundary rows")
        widened.append((stream, scalar_evidence))
        rectangle.append((stream, F(0), F(1)))
    return replace(evidence, scalar_evidence=tuple(widened),
                   rectangle=tuple(rectangle))


def one_parameter_template(parameter="p"):
    return ref.Template("one-parameter", 1, "loss", (), (parameter,), (
        ref.node((), actions=(
            ref.action("stop", 1),
            ref.action("try", 0, (
                ref.outcome("good", 0, 1, parameter),
                ref.outcome("bad", 1, -1, parameter),
            )),
        )),
        ref.node((("try", "good"),), terminal=-1),
        ref.node((("try", "bad"),), terminal=1),
    )).validate()


def repeated_template():
    A = (("first", "A"),)
    B = (("first", "B"),)
    return ref.Template("repeated parameter", 2, "loss", (), ("p",), (
        ref.node((), actions=(ref.action("first", 0, (
            ref.outcome("A", 0, 1, "p"),
            ref.outcome("B", 1, -1, "p"),
        )),)),
        ref.node(A, actions=(ref.action("second", 0, (
            ref.outcome("hit", 1, -1, "p"),
            ref.outcome("miss", 0, 1, "p"),
        )),)),
        ref.node(B, terminal=0),
        ref.node(A + (("second", "hit"),), terminal=1),
        ref.node(A + (("second", "miss"),), terminal=0),
    )).validate()


def run():
    results = []

    def record(name, **values):
        results.append({"case": name, "status": "PASS", **values})

    # C1: a retained PR14 rectangle maps explicitly to four completed models.
    data = collection(((0,) * 8, (1,) * 8))
    coverage_evidence, checked_coverage = coverage(data)
    check(checked_coverage["rectangle"] == (
        ("stream-1", F(0), F(43333, 65536)),
        ("stream-2", F(22203, 65536), F(1))),
        "unexpected retained PR14 rectangle")
    request = headline_request(data)
    evidence = ref.produce(request, coverage_evidence)
    answer = ref.consume(request, evidence)
    check(answer["corner_count"] == 4 and len(evidence.family.members) == 4,
          "four completed corners required")
    check(answer["mapped_rectangle"] == (
        ("p-route", F(22203, 65536), F(1)),
        ("p-followup", F(0), F(43333, 65536))),
        "explicit mapping permutation not respected")
    check(answer["path_count"] == 6 and
          answer["mutually_exclusive_reuse_allowed"] and
          answer["mutually_exclusive_reused_parameters"] == ("p-followup",),
          "mutually exclusive repeated node use should remain admissible")
    check(answer["direct_path_matrix_equal"] and
          direct_family_matrix(evidence, request.policies) ==
          evidence.loss_evidence.matrix,
          "independent complete paths disagree with family checker")
    check(any(probability == 0 for member in evidence.family.members
              for item in member.subject.nodes for action in item.actions
              for _, probability in action.outcomes),
          "headline family should exercise exact zero-probability branches")
    named_policy = next(entry.policy for entry in request.policies
                        if entry.identity == request.named_policy_identity)
    check(all(cell.certificate.policy == named_policy
              for cell in evidence.loss_evidence.cells
              if cell.policy_identity == request.named_policy_identity),
          "named policy changed across corner models")
    check(answer["minimax_loss_winners"] == ("hold-hold",) and
          answer["minimax_regret_winners"] == ("hold-inspect",),
          "loss and regret selection should distinguish criteria")
    check(answer["named_worst_expected_loss"] == F(1877748889, 2147483648) and
          answer["named_worst_regret"] == F(457813145, 2147483648),
          "headline exact named-policy values changed")
    check(answer["expected_loss_cap_met"] and answer["regret_cap_met"],
          "headline caps should hold")
    check(answer["rational_interior_audit_points"] == 289 and
          answer["rational_interior_audit_equal"],
          "complete dyadic interior audit disagrees")
    check(answer["statistical"] == {
        "simultaneous_coverage_lower": F(19, 20),
        "failure_probability_upper": F(1, 20),
        "declared_total_alpha": F(1, 20),
        "precision_bits": 16,
        "sampling_premises_supplied_not_empirically_validated": True,
        "outward_rectangle_may_be_conservative": True,
    }, "statistical meanings were mixed")
    cross_model = (answer["named_worst_expected_loss"] -
                   min(min(row) for row in evidence.loss_evidence.matrix))
    check(cross_model != answer["named_worst_regret"],
          "modelwise regret was replaced by a cross-model subtraction")
    record("C1_two_parameter_statistical_corner_family",
           rectangle=answer["mapped_rectangle"], corners=4, paths=6,
           named_policy=answer["named_policy"],
           worst_expected_loss=answer["named_worst_expected_loss"],
           worst_regret=answer["named_worst_regret"],
           minimax_loss=answer["minimax_loss_winners"],
           minimax_regret=answer["minimax_regret_winners"],
           audit_points=answer["rational_interior_audit_points"])

    # C2: no observations retain [0,1], one parameter, signed loss, and STOP.
    one_data = collection(((),), record="unobserved")
    one_coverage_evidence, one_coverage = coverage(one_data)
    check(one_coverage["rectangle"] == (("stream-1", F(0), F(1)),),
          "unobserved parameter must remain [0,1]")
    one_template = one_parameter_template()
    nominal = ref.instantiate(one_template, {"p": F(0)})
    one_entries = tuple(f.PolicyEntry(label, policy) for label, policy in zip(
        ("stop", "try"), r.enumerate_policies(nominal)))
    one_request = ref.Request(
        one_data, one_template, (ref.MappingRow("stream-1", "p"),),
        one_entries, "try", f.FULL)
    one_evidence = ref.produce(one_request, one_coverage_evidence)
    one_answer = ref.consume(one_request, one_evidence)
    check(one_answer["corner_count"] == 2 and
          one_answer["named_corner_costs"] == (F(1), F(-1)),
          "one-parameter boundary values changed")
    record("C2_one_unobserved_parameter_signed_stop",
           rectangle=one_answer["mapped_rectangle"],
           named_costs=one_answer["named_corner_costs"])

    # C3: valid deliberately loose outward evidence remains exact over its export.
    loose_coverage = widen_coverage(coverage_evidence)
    loose_checked = s.consume_coverage(data, loose_coverage)
    check(all(row[1:] == (F(0), F(1)) for row in loose_checked["rectangle"]),
          "loose outward rectangle did not survive receiving")
    loose_evidence = ref.produce(request, loose_coverage)
    loose_answer = ref.consume(request, loose_evidence)
    check(loose_answer["corner_count"] == 4 and
          loose_answer["statistical"]["outward_rectangle_may_be_conservative"],
          "loose rectangle not handled as conservative export")
    record("C3_loose_outward_rectangle_exact_over_export",
           rectangle=loose_answer["mapped_rectangle"], corners=4)

    # C4: repeated use along one path is a valid sequential model but no corner theorem.
    repeated = repeated_template()
    repeated_subject = ref.instantiate(repeated, {"p": F(0)})
    repeated_policy = r.enumerate_policies(repeated_subject)[0]
    repeated_request = ref.Request(
        one_data, repeated, (ref.MappingRow("stream-1", "p"),),
        (f.PolicyEntry("only", repeated_policy),), "only", f.FULL)
    boundary = ref.produce(repeated_request, one_coverage_evidence)
    boundary_answer = ref.consume(repeated_request, boundary)
    check(boundary_answer["status"] == ref.INVALID_WARRANT and
          boundary_answer["sequential_model_status"].startswith("valid") and
          not boundary_answer["mathematical_impossibility_claimed"],
          "repeated parameter boundary misclassified")
    values = tuple(ref.direct_value(repeated, repeated_policy, {"p": value})
                   for value in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)))
    check(values == (F(0), F(3, 16), F(1, 4), F(3, 16), F(0)),
          "p(1-p) counterexample changed")
    reject(lambda: ref.consume(repeated_request,
                               replace(boundary, status=ref.EXACT_WARRANT)),
           "inadmissible subject received exact corner warrant")
    record("C4_repeated_parameter_counterexample",
           unit_interval_endpoints=(values[0], values[-1]),
           quarter_interval_endpoints=(values[1], values[3]),
           interior=values[2], disposition=boundary_answer["status"])

    # C5: mappings are identities, not positional guesses.
    reject(lambda: replace(request, mapping=(
        ref.MappingRow("stream-1", "p-followup"),)),
        "missing stream/parameter mapping accepted")
    reject(lambda: replace(request, mapping=(
        ref.MappingRow("stream-1", "p-followup"),
        ref.MappingRow("stream-1", "p-route"))),
        "duplicate stream mapping accepted")
    reject(lambda: replace(request, mapping=(
        ref.MappingRow("stream-1", "p-route"),
        ref.MappingRow("stream-2", "p-route"))),
        "duplicate parameter mapping accepted")
    reject(lambda: replace(request, mapping=(
        ref.MappingRow("stream-1", "p-followup"),
        ref.MappingRow("stream-2", "p-route"),
        ref.MappingRow("ghost", "ghost-parameter"))),
        "extra mapping identities accepted")
    record("C5_mapping_permutation_and_exact_coverage",
           mapped_parameter_order=tuple(row[0] for row in answer["mapped_rectangle"]))

    # C6: old statistical or sequential subjects cannot borrow a result.
    successor_data = replace(data, revision_identity="r2")
    stale_request = headline_request(successor_data)
    reject(lambda: ref.produce(stale_request, coverage_evidence),
           "stale statistical evidence accepted")
    changed_nodes = list(request.template.nodes)
    changed_nodes[3] = replace(changed_nodes[3], terminal=F(2))
    changed_template = replace(request.template, nodes=tuple(changed_nodes))
    changed_request = replace(request, template=changed_template)
    reject(lambda: ref.consume(changed_request, evidence),
           "changed loss/model borrowed old corner evidence")
    forged_loss = replace(evidence.loss_evidence,
                          worst_regrets=tuple(F(0) for _ in request.policies))
    reject(lambda: ref.consume(request, replace(evidence,
                                               loss_evidence=forged_loss)),
           "false family regret vector accepted")
    reject(lambda: f.NamedPolicyRequest(
        evidence.family, [request.policies[0].policy, request.policies[1].policy], ()),
        "hidden-model-indexed policy accepted")
    record("C6_stale_subject_and_hidden_model_controls")

    # C7: general multi-affine extrema include minima and signed coefficients.
    rectangle = ((F(-1, 3), F(2, 3)), (F(1, 4), F(3, 4)))
    function = lambda x, y: F(-2) + F(3) * x - F(5) * y + F(7) * x * y
    corners = tuple(function(x, y) for x, y in product(*rectangle))
    audit = tuple(function(rectangle[0][0] +
                           (rectangle[0][1] - rectangle[0][0]) * F(i, 32),
                           rectangle[1][0] +
                           (rectangle[1][1] - rectangle[1][0]) * F(j, 32))
                  for i in range(33) for j in range(33))
    check((min(audit), max(audit)) == (min(corners), max(corners)),
          "signed multi-affine min/max escaped the corners")
    record("C7_signed_multi_affine_minimum_and_maximum",
           minimum=min(corners), maximum=max(corners), audit_points=len(audit))

    # C8: three parameters are well-formed mathematics but outside this receiver budget.
    three_data = collection(((), (), ()), record="three-stream")
    three_coverage_evidence, _ = coverage(three_data)
    base = one_parameter_template("p1")
    three_template = replace(base, parameters=("p1", "p2", "p3"))
    three_subject = ref.instantiate(three_template,
                                    {"p1": F(0), "p2": F(0), "p3": F(0)})
    three_entries = tuple(f.PolicyEntry(label, policy) for label, policy in zip(
        ("stop", "try"), r.enumerate_policies(three_subject)))
    three_request = ref.Request(
        three_data, three_template,
        tuple(ref.MappingRow(f"stream-{index}", f"p{index}")
              for index in range(1, 4)),
        three_entries, "try", f.FULL)
    refusal = ref.produce(three_request, three_coverage_evidence)
    expect_unfinished(refusal, "parameter-count-limit")
    expect_unfinished(ref.consume(three_request, refusal), "parameter-count-limit")
    record("C8_bounded_profile_refusal",
           parameter_limit=ref.MAX_PARAMETERS, requested=3)

    # C9: receiving uses existing consumers but no candidate producer.
    saved = (ref.produce, s.produce_collection, s.produce_coverage,
             f.choose, r.produce)

    def disabled(*args, **kwargs):
        raise RuntimeError("candidate producer invoked")

    try:
        ref.produce = s.produce_collection = s.produce_coverage = disabled
        f.choose = r.produce = disabled
        repeated_answer = ref.consume(repeated_request, boundary)
        checked_again = ref.consume(request, evidence)
        check(checked_again == answer and
              repeated_answer["status"] == ref.INVALID_WARRANT,
              "producer-disabled receiver changed result")
        reject(lambda: ref.consume(request, replace(
            evidence, rectangle=tuple(reversed(evidence.rectangle)))),
            "producer-disabled receiver accepted reordered rectangle")
    finally:
        (ref.produce, s.produce_collection, s.produce_coverage,
         f.choose, r.produce) = saved
    record("C9_receivers_run_with_candidate_producers_disabled")

    # Cross-cutting exactness and immutable-subject controls.
    reject(lambda: ref.OutcomeLaw("x", F(0), F(1), None).validate(),
           "unidentified transition coefficient accepted")
    reject(lambda: ref.outcome("x", True),
           "boolean transition probability accepted as exact rational")
    reject(lambda: ref.Template("bad", 1, "loss", (), ("p",), (
        ref.node((), actions=(ref.action("a", 0, (
            ref.outcome("x", 0, 1, "p"), ref.outcome("y", 1, -2, "p"))),)),
        ref.node((("a", "x"),), terminal=0),
        ref.node((("a", "y"),), terminal=0),
    )).validate(), "nonnormalized affine transition accepted")
    reject(lambda: replace(request, named_policy_identity="model-indexed-oracle"),
           "uncovered named policy accepted")
    record("C10_exact_inputs_and_immutable_subject_binding")

    print(json.dumps(ref.wire({
        "status": "passed", "passed": len(results), "failed": 0,
        "rejections": rejections, "unfinished": unfinished,
        "optimized": sys.flags.optimize, "results": results,
    }), sort_keys=True))


if __name__ == "__main__":
    run()
