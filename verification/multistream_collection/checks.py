#!/usr/bin/env python3
"""Independent exact checks for controlled multistream collection."""
from dataclasses import replace
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from verification.multistream_collection import reference as ref  # noqa: E402
from verification.statistical_decision_bridge import reference as scalar  # noqa: E402


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def rejected(operation, message):
    try:
        operation()
    except (ref.Invalid, TypeError, KeyError):
        return
    raise AssertionError(message)


def refused(result, reason):
    check(result == {"status": "unfinished", "kind": "resource-refusal",
                     "reason": reason, "limit": result["limit"],
                     "requested": result["requested"]},
          f"wrong refusal shape for {reason}")


def registry(count=2):
    return tuple(ref.make_stream(f"stream-{index}", f"population-{index}",
                                 f"protocol-{index}")
                 for index in range(1, count + 1))


def round_robin_collection(rows, *, alpha=F(1, 20), precision=16,
                           stopped=False, rule=ref.RULE_ROUND_ROBIN_BUDGET,
                           allocations=None, record="collection", revision="r1",
                           predecessor=None):
    streams = registry(len(rows))
    allocations = (tuple((item.stream_identity, alpha / len(streams))
                         for item in streams) if allocations is None
                   else tuple(allocations))
    transcript = []
    local = [0] * len(streams)
    horizon = sum(len(row) for row in rows)
    for global_index in range(1, horizon + 1):
        index = (global_index - 1) % len(streams)
        check(local[index] < len(rows[index]), "rows must match round-robin schedule")
        local[index] += 1
        transcript.append(ref.make_observation(
            global_index, streams[index].stream_identity, local[index],
            rows[index][local[index] - 1], f"event-{global_index}"))
    return ref.make_collection(
        streams, alpha, allocations, precision_bits=precision, rule=rule,
        transcript=transcript, stopped=stopped, record=record,
        revision=revision, predecessor_digest=predecessor)


def checked_pipeline(collection, actions, intended, **decision_options):
    collection_evidence = ref.produce_collection(collection)
    coverage_evidence = ref.produce_coverage(collection, collection_evidence)
    decision = ref.make_decision(collection, actions, intended_action=intended,
                                 **decision_options)
    decision_evidence = ref.produce_decision(decision, coverage_evidence)
    return (ref.consume_collection(collection, collection_evidence),
            ref.consume_coverage(collection, coverage_evidence),
            ref.consume_decision(decision, decision_evidence),
            collection_evidence, coverage_evidence, decision, decision_evidence)


def independent_corners(action_a, action_b, rectangle):
    """Exhaust all corners without using the production sign formula."""
    bounds = [(stream, (lower, upper)) for stream, lower, upper in rectangle]
    weights_a, weights_b = dict(action_a.weights), dict(action_b.weights)
    values = []
    for coordinates in product(*[pair for _, pair in bounds]):
        parameters = {bounds[index][0]: value
                      for index, value in enumerate(coordinates)}
        risk_a = action_a.intercept + sum(
            (weights_a[stream] * parameters[stream] for stream, _ in bounds), F(0))
        risk_b = action_b.intercept + sum(
            (weights_b[stream] * parameters[stream] for stream, _ in bounds), F(0))
        values.append(risk_a - risk_b)
    return max(values)


def m1_scalar_reduction():
    cases = (
        ((), F(1, 20)),
        ((0,) * 8, F(1, 20)),
        ((1,) * 8, F(1, 20)),
        ((0, 1, 1, 0, 1, 0, 1), F(1, 20)),
        ((0, 1, 0), F(1, 2**200)),
    )
    compared = []
    for index, (values, alpha) in enumerate(cases):
        collection = round_robin_collection((values,), alpha=alpha, precision=12,
                                            record=f"m1-{index}")
        collection_evidence = ref.produce_collection(collection)
        coverage_evidence = ref.produce_coverage(collection, collection_evidence)
        coverage = ref.consume_coverage(collection, coverage_evidence)
        sample = scalar.make_sampling(
            values, alpha, stream="stream-1", population="population-1",
            protocol="protocol-1", precision_bits=12)
        scalar_evidence = scalar.produce_interval(sample)
        scalar_checked = scalar.consume_interval(sample, scalar_evidence)
        check(coverage["rectangle"][0][1:] == scalar_checked["outward_interval"],
              "one-row interval does not reduce to scalar PR12")

        scalar_actions = (
            scalar.make_action("signed", (F(-3, 2), F(5, 4))),
            scalar.make_action("tie-a", (F(1, 3), F(1, 3))),
            scalar.make_action("tie-b", (F(1, 3), F(1, 3))),
        )
        affine_actions = tuple(ref.make_affine_action(
            action.label, action.losses[0],
            {"stream-1": action.losses[1] - action.losses[0]})
            for action in scalar_actions)
        scalar_decision = scalar.make_decision(
            sample, scalar_actions, unit="signed-loss", intended_action="signed")
        scalar_result = scalar.consume_decision(
            scalar_decision, scalar.produce_decision(scalar_decision, scalar_evidence))
        multi_decision = ref.make_decision(
            collection, affine_actions, unit="signed-loss", intended_action="signed")
        multi_result = ref.consume_decision(
            multi_decision, ref.produce_decision(multi_decision, coverage_evidence))
        for key in ("common_minimizers", "uniformly_strict_actions",
                    "named_action_regret"):
            check(multi_result[key] == scalar_result[key],
                  f"one-row decision mismatch for {key}")
        compared.append((len(values), alpha, coverage["rectangle"][0][1:]))
    return {"cases": len(compared), "scalar_reduction": True,
            "includes_no_data_boundaries_ties_signed_and_extreme_alpha": True}


def m2_two_stream_actions():
    actions = (
        ref.make_affine_action("A", 0, {"stream-1": 1, "stream-2": 0}),
        ref.make_affine_action("B", 0, {"stream-1": 0, "stream-2": 1}),
        ref.make_affine_action("C", F(1, 2), {"stream-1": 0, "stream-2": 0}),
    )
    expected = {
        8: ((F(0), F(43333, 65536)), (F(22203, 65536), F(1))),
        16: ((F(0), F(30431, 65536)), (F(35105, 65536), F(1))),
    }
    results = {}
    for count in (8, 16):
        collection = round_robin_collection(((0,) * count, (1,) * count))
        _, coverage, decision, _, coverage_evidence, request, evidence = checked_pipeline(
            collection, actions, "A", regret_cap=F(1))[:7]
        rectangle = tuple(row[1:] for row in coverage["rectangle"])
        check(rectangle == expected[count], "M2 prescribed rectangle mismatch")
        for first in actions:
            for second in actions:
                production = next(row[2] for row in evidence.pairwise_extrema
                                  if row[:2] == (first.label, second.label))
                check(production == independent_corners(
                    first, second, coverage["rectangle"]),
                    "affine sign formula differs from full corner enumeration")
        if count == 8:
            check(decision["common_minimizers"] == (),
                  "M2 n=8 must have no common minimizer")
        else:
            check(decision["uniformly_strict_actions"] == ("A",),
                  "M2 n=16 A must be uniformly strict")
            margin = dict(decision["strict_advantage_margins"])["A"]
            check(margin == F(2337, 65536), "M2 exact strict margin mismatch")
        results[count] = {"rectangle": rectangle,
                          "common": decision["common_minimizers"],
                          "strict": decision["uniformly_strict_actions"]}
    return results


def independent_switch_directive(prefixes, history):
    streams = ("stream-1", "stream-2")
    if len(history) == 12:
        return None
    if all(len(prefixes[stream]) >= 2 for stream in streams):
        means = {stream: F(sum(prefixes[stream]), len(prefixes[stream]))
                 for stream in streams}
        if abs(means[streams[0]] - means[streams[1]]) > F(1, 2):
            return None
    if not history:
        return streams[0]
    last_stream, last_value = history[-1]
    return last_stream if last_value == 0 else next(
        stream for stream in streams if stream != last_stream)


@lru_cache(maxsize=None)
def excluded_at_prefix(n, k, probability, alpha):
    if n == 0:
        return False
    allowance = alpha / (2 * n * (n + 1))
    upper_tail = sum((F(__import__("math").comb(n, x)) * probability**x *
                      (1 - probability)**(n - x) for x in range(k, n + 1)), F(0))
    lower_tail = sum((F(__import__("math").comb(n, x)) * probability**x *
                      (1 - probability)**(n - x) for x in range(k + 1)), F(0))
    return upper_tail < allowance or lower_tail < allowance


def enumerate_switch(parameters, allocations):
    terminal_count = 0
    total_mass = F(0)
    excluded_mass = F(0)
    length_counts = {}

    def visit(prefixes, history, mass, excluded):
        nonlocal terminal_count, total_mass, excluded_mass
        selected = independent_switch_directive(prefixes, history)
        if selected is None:
            terminal_count += 1
            total_mass += mass
            excluded_mass += mass if excluded else F(0)
            length_counts[len(history)] = length_counts.get(len(history), 0) + 1
            return
        probability = parameters[selected]
        for value, chance in ((0, 1 - probability), (1, probability)):
            next_prefixes = {key: tuple(row) for key, row in prefixes.items()}
            next_prefixes[selected] += (value,)
            newly_excluded = excluded or excluded_at_prefix(
                len(next_prefixes[selected]), sum(next_prefixes[selected]),
                probability, allocations[selected])
            visit(next_prefixes, history + ((selected, value),),
                  mass * chance, newly_excluded)

    visit({"stream-1": (), "stream-2": ()}, (), F(1), False)
    return terminal_count, total_mass, excluded_mass, length_counts


def transcript_from_global_values(values):
    prefixes = {"stream-1": (), "stream-2": ()}
    history = ()
    transcript = []
    for value in values:
        selected = independent_switch_directive(prefixes, history)
        if selected is None:
            break
        prefixes[selected] += (value,)
        history += ((selected, value),)
        transcript.append(ref.make_observation(
            len(transcript) + 1, selected, len(prefixes[selected]), value,
            f"adaptive-event-{len(transcript) + 1}"))
    return tuple(transcript), independent_switch_directive(prefixes, history) is None


def m3_adaptive_collection():
    allocations = {"stream-1": F(1, 40), "stream-2": F(1, 40)}
    first = enumerate_switch(
        {"stream-1": F(1, 2), "stream-2": F(1, 2)}, allocations)
    second = enumerate_switch(
        {"stream-1": F(1, 3), "stream-2": F(2, 3)}, allocations)
    for result in (first, second):
        check(result[0] == 3013 and result[1] == 1,
              "adaptive path count or mass conservation mismatch")
    check(first[2] == 0, "fair-pair exclusion mismatch")
    check(second[2] == F(65, 531441), "asymmetric-pair exclusion mismatch")

    transcript, stopped = transcript_from_global_values((0, 1, 1, 0, 0, 1,
                                                          0, 1, 0, 1, 0, 1))
    collection = ref.make_collection(
        registry(), F(1, 20), tuple(allocations.items()),
        rule=ref.RULE_SWITCH_AFTER_ONE, transcript=transcript, stopped=stopped)
    replay = ref.consume_collection(collection, ref.produce_collection(collection))
    counts = dict(replay["counts"])
    check(len(set(counts.values())) > 1, "adaptive example should have unequal counts")

    rr = round_robin_collection(((0, 1, 0), (1, 0, 1)), stopped=True,
                                rule=ref.RULE_ROUND_ROBIN_SIX)
    check(ref.consume_collection(rr, ref.produce_collection(rr))["status"] ==
          "checked-collection-transcript", "second legal rule failed")
    unobserved = round_robin_collection(((), ()), stopped=False)
    coverage = ref.consume_coverage(
        unobserved, ref.produce_coverage(unobserved,
                                         ref.produce_collection(unobserved)))
    check(all(row[1:] == (F(0), F(1)) for row in coverage["rectangle"]),
          "unobserved streams must retain [0,1]")

    bad_global = replace(rr, transcript=(replace(rr.transcript[0], global_index=2),) +
                         rr.transcript[1:])
    rejected(lambda: ref.produce_collection(bad_global),
             "global clock mistake accepted")
    bad_local = replace(rr, transcript=(replace(rr.transcript[0], local_index=2),) +
                        rr.transcript[1:])
    rejected(lambda: ref.produce_collection(bad_local),
             "local clock mistake accepted")
    return {"terminal_histories": first[0], "fair_exclusion": first[2],
            "asymmetric_exclusion": second[2], "mass": first[1],
            "terminal_length_counts": first[3], "unequal_counts": counts}


def m4_adaptive_count_counterexample():
    paths = (((1,), F(1, 2)), ((0, 1), F(1, 4)), ((0, 0), F(1, 4)))
    expected_mean = sum((F(sum(path), len(path)) * mass for path, mass in paths), F(0))
    conditional_success = sum(mass for path, mass in paths
                              if len(path) == 1 and sum(path) == 1) / sum(
                                  mass for path, mass in paths if len(path) == 1)
    check(expected_mean == F(5, 8), "adaptive sample-mean expectation mismatch")
    check(conditional_success == 1, "conditional N=1 count mismatch")
    return {"expected_sample_mean": expected_mean,
            "conditional_success_given_n_1": conditional_success,
            "all_prefix_event_still_implies_random_prefix_membership": True}


def m5_omission_and_copying():
    legal = round_robin_collection(((1, 1, 1),), precision=8)
    check(ref.consume_collection(legal, ref.produce_collection(legal))["status"] ==
          "checked-collection-transcript", "equal values with unique events rejected")
    copied = replace(legal, transcript=(legal.transcript[0],
                     replace(legal.transcript[1], event_identity="event-1"),
                     legal.transcript[2]))
    rejected(lambda: ref.produce_collection(copied), "copied event accepted")
    omitted = replace(legal, transcript=(legal.transcript[0],
                      replace(legal.transcript[1], local_index=3), legal.transcript[2]))
    rejected(lambda: ref.produce_collection(omitted), "omitted local event accepted")
    reordered = replace(legal, transcript=(legal.transcript[1], legal.transcript[0],
                        legal.transcript[2]))
    rejected(lambda: ref.produce_collection(reordered), "reordered events accepted")

    all_success = scalar.make_sampling((1,) * 16, F(1, 20))
    interval = scalar.consume_interval(all_success,
                                       scalar.produce_interval(all_success))["outward_interval"]
    check(not (interval[0] <= F(1, 2) <= interval[1]),
          "sixteen retained successes should exclude one half")
    return {"eventual_sixteen_successes_probability": F(1),
            "false_iid_interval_excludes_true_half": True,
            "visible_omission_copy_reorder_rejected": True,
            "concealed_omission_diagnosable": False}


def m6_allocation_identity_and_revisions():
    streams = registry()
    rejected(lambda: ref.make_collection(
        streams, F(1, 20), (("stream-1", F(1, 20)),
                            ("stream-2", F(1, 20)))),
        "allocation overspend accepted")
    rejected(lambda: ref.make_collection(
        streams, F(1, 20), (("stream-1", F(1, 40)),)),
        "missing allocation accepted")
    rejected(lambda: ref.make_collection(
        streams, F(1, 20), (("stream-1", F(1, 80)),
                            ("stream-1", F(1, 80)))),
        "duplicate allocation accepted")
    rejected(lambda: ref.make_collection(
        (streams[0], streams[0]), F(1, 20),
        (("stream-1", F(1, 40)), ("stream-1", F(1, 40)))),
        "duplicate stream accepted")

    base = round_robin_collection(((0, 1), (1, 0)))
    base_collection = ref.produce_collection(base)
    base_coverage = ref.produce_coverage(base, base_collection)
    changed_allocation = replace(base, allocations=(("stream-1", F(1, 80)),
                                                     ("stream-2", F(3, 80))))
    rejected(lambda: ref.consume_coverage(changed_allocation, base_coverage),
             "changed allocation accepted stale coverage")
    wrong_source = replace(base, registry=(replace(base.registry[0],
                                                   population_identity="wrong"),
                                           base.registry[1]))
    rejected(lambda: ref.consume_collection(wrong_source, base_collection),
             "wrong source accepted stale transcript")
    stale_prefix = round_robin_collection(((0, 1, 0), (1, 0, 1)))
    rejected(lambda: ref.consume_coverage(stale_prefix, base_coverage),
             "stale shorter-prefix evidence accepted")
    missing_row = replace(base_coverage,
                          scalar_evidence=base_coverage.scalar_evidence[:1])
    rejected(lambda: ref.consume_coverage(base, missing_row),
             "missing registered scalar row accepted")
    duplicate_row = replace(base_coverage,
                            scalar_evidence=(base_coverage.scalar_evidence[0],) * 2)
    rejected(lambda: ref.consume_coverage(base, duplicate_row),
             "duplicate registered scalar row accepted")
    reordered_rows = replace(base_coverage,
                             scalar_evidence=tuple(reversed(
                                 base_coverage.scalar_evidence)))
    check(ref.consume_coverage(base, reordered_rows)["status"] ==
          "checked-multistream-coverage",
          "explicit stream correspondence should survive evidence-row reorder")
    reset = replace(base, transcript=base.transcript[:2] +
                    (replace(base.transcript[2], local_index=1),) + base.transcript[3:])
    rejected(lambda: ref.produce_collection(reset), "local count reset accepted")
    switched = replace(base, transcript=(replace(base.transcript[0],
                                                  stream_identity="stream-2"),) +
                       base.transcript[1:])
    rejected(lambda: ref.produce_collection(switched),
             "switched stream association accepted")
    rejected(lambda: ref.make_collection(
        streams, F(1, 20), (("stream-1", F(1, 40)),
                            ("stream-2", F(1, 40))),
        rule="choose-hidden-parameter-key"), "hidden-parameter rule accepted")
    stop_mismatch = replace(base, stopped=True)
    rejected(lambda: ref.produce_collection(stop_mismatch),
             "mismatched stopping status accepted")

    extended = round_robin_collection(((0, 1, 0), (1, 0, 1)),
                                      record=base.record_identity, revision="r2",
                                      predecessor=ref.collection_digest(base))
    check(ref.classify_collection_revision(base, extended) ==
          "append-only-transcript-extension", "append-only revision misclassified")
    action1 = (ref.make_affine_action("keep", 0,
                                     {"stream-1": 1, "stream-2": 0}),)
    first = ref.make_decision(base, action1, intended_action="keep")
    action2 = (ref.make_affine_action("keep", 1,
                                     {"stream-1": -1, "stream-2": 2}),)
    changed = ref.make_decision(base, action2, intended_action="keep")
    check(ref.classify_decision_revision(first, changed) ==
          "same-data-new-decision-query", "changed loss query misclassified")
    checked = ref.consume_decision(
        changed, ref.produce_decision(changed, base_coverage))
    check(checked["status"] == "checked-multistream-decision",
          "fresh check of changed loss query failed")
    return {"allocation_and_identity_failures_rejected": True,
            "append_only_revision": True, "changed_loss_freshly_checked": True}


def m7_dependence_boundary():
    # B=A for one fair bit: exact joint mass, not a product of the marginals.
    joint_both_one = sum((mass for a, b, mass in
                          ((0, 0, F(1, 2)), (1, 1, F(1, 2)))
                          if a == b == 1), F(0))
    check(joint_both_one == F(1, 2) and
          joint_both_one != F(1, 2) * F(1, 2),
          "dependent-stream composition example failed")
    streams = registry()
    collection = ref.make_collection(
        streams, F(1, 20), (("stream-1", F(1, 40)),
                            ("stream-2", F(1, 40))))
    rejected(lambda: ref.make_decision(
        collection, (("joint", 0, {"stream-1": 1, "stream-2": 1}),),
        intended_action="joint", query="probability-both-streams-one"),
        "marginal-only joint-event query accepted")
    rejected(lambda: ref.make_decision(
        collection, (("next", 0, {"stream-1": 1, "stream-2": 0}),),
        intended_action="next", risk_scope=ref.CONDITIONAL_FRESH_DRAW_RISK),
        "conditional next-draw claim accepted without sufficient premise")
    conditional = ref.make_decision(
        collection, (("next", 0, {"stream-1": 1, "stream-2": 0}),),
        intended_action="next", risk_scope=ref.CONDITIONAL_FRESH_DRAW_RISK,
        fresh_draw_premise=ref.FRESH_DRAW_PREMISE)
    check(conditional.fresh_draw_premise == ref.FRESH_DRAW_PREMISE,
          "explicit fresh-draw premise was not retained")
    return {"both_one_probability": joint_both_one,
            "product_of_marginals": F(1, 4),
            "union_bound_requires_cross_stream_independence": False,
            "arbitrary_within_row_dependence_supported": False}


def m8_end_to_end_adversarial():
    # Hand-authored no-data evidence: no producer is called by any receiver.
    collection = round_robin_collection(((), ()))
    empty_digest = ref.digest_payload(ref.collection_payload(collection)["transcript"])
    collection_evidence = ref.CollectionEvidence(
        collection, (("stream-1", ()), ("stream-2", ())),
        (("stream-1", 0), ("stream-2", 0)), "observe", "stream-1",
        empty_digest, ref.collection_digest(collection))
    scalar_rows = []
    for stream in ("stream-1", "stream-2"):
        request = ref.scalar_request(collection, stream, ())
        scalar_rows.append((stream, scalar.IntervalEvidence(
            request, 0, 0, None, (F(0), F(0)), (F(1), F(1)),
            (F(0), F(1)), True, scalar.prefix_digest(request))))
    coverage_evidence = ref.CoverageEvidence(
        collection, collection_evidence, tuple(scalar_rows),
        (("stream-1", F(0), F(1)), ("stream-2", F(0), F(1))),
        F(1, 20), F(19, 20), F(19, 20), ref.collection_digest(collection))
    action = ref.make_affine_action("only", 0,
                                    {"stream-1": 0, "stream-2": 0})
    decision = ref.make_decision(collection, (action,), unit="manual-loss",
                                 intended_action="only", regret_cap=0)
    decision_evidence = ref.DecisionEvidence(
        decision, coverage_evidence,
        (("only", "only", F(0),
          (("stream-1", F(1)), ("stream-2", F(1)))),),
        ("only",), ("only",), (("only", None),), "only", F(0), True,
        ref.decision_digest(decision))
    original_producers = (ref.produce_collection, ref.produce_coverage,
                          ref.produce_decision, scalar.produce_interval)
    def disabled(*_args, **_kwargs):
        raise AssertionError("producer called by receiver")
    ref.produce_collection = ref.produce_coverage = ref.produce_decision = disabled
    scalar.produce_interval = disabled
    try:
        check(ref.consume_decision(decision, decision_evidence)["status"] ==
              "checked-multistream-decision", "manual evidence did not verify")
    finally:
        (ref.produce_collection, ref.produce_coverage,
         ref.produce_decision, scalar.produce_interval) = original_producers

    rejected(lambda: ref.consume_coverage(
        collection, replace(coverage_evidence,
                            simultaneous_coverage_lower=F(999, 1000))),
        "false joint coverage retained correct hash")
    rejected(lambda: ref.consume_decision(
        decision, replace(decision_evidence,
                          pairwise_extrema=(("only", "only", F(1),
                            (("stream-1", F(1)), ("stream-2", F(1)))),))),
        "false affine extremum accepted")

    tie_actions = (
        ref.make_affine_action("tie-1", 0, {"stream-1": 0, "stream-2": 0}),
        ref.make_affine_action("tie-2", 0, {"stream-1": 0, "stream-2": 0}),
    )
    tie_request = ref.make_decision(collection, tie_actions, intended_action="tie-1")
    tie_evidence = ref.produce_decision(tie_request, coverage_evidence)
    rejected(lambda: ref.consume_decision(
        tie_request, replace(tie_evidence, common_minimizers=("tie-1",))),
        "missing tied action accepted")

    interior = round_robin_collection(((0, 1),), precision=16)
    interior_collection = ref.produce_collection(interior)
    interior_coverage = ref.produce_coverage(interior, interior_collection)
    interval_evidence = interior_coverage.scalar_evidence[0][1]
    inward = replace(interval_evidence,
                     outward_interval=(interval_evidence.lower_bracket[1],
                                       interval_evidence.upper_bracket[0]))
    bad_coverage = replace(interior_coverage,
                           scalar_evidence=(("stream-1", inward),))
    rejected(lambda: ref.consume_coverage(interior, bad_coverage),
             "inward scalar bracket accepted")
    coarse_scalar = replace(interval_evidence,
                            lower_bracket=(F(0), F(1)),
                            upper_bracket=(F(0), F(1)),
                            outward_interval=(F(0), F(1)),
                            precision_claimed=False)
    coarse_coverage = replace(
        interior_coverage, scalar_evidence=(("stream-1", coarse_scalar),),
        rectangle=(("stream-1", F(0), F(1)),))
    check(ref.consume_coverage(interior, coarse_coverage)["scalar_statuses"][0][1] ==
          "valid-coarse-outward-enclosure", "valid coarse witness rejected")

    four_rows = tuple((0,) * 128 for _ in range(4))
    boundary = round_robin_collection(four_rows, stopped=True)
    check(ref.consume_collection(boundary, ref.produce_collection(boundary))["status"] ==
          "checked-collection-transcript", "boundary transcript rejected")
    too_many = ref.make_collection(
        registry(5), F(1, 10), tuple((f"stream-{i}", F(1, 100))
                                     for i in range(1, 6)))
    refused(ref.produce_collection(too_many), "stream-count-limit")
    refused(ref.consume_collection(too_many, None), "stream-count-limit")
    refused(ref.produce_coverage(too_many, None), "stream-count-limit")
    refused(ref.consume_coverage(too_many, None), "stream-count-limit")
    too_precise = round_robin_collection(((),), precision=65)
    refused(ref.produce_collection(too_precise), "precision-request-limit")
    per_stream_large = round_robin_collection(((0,) * 129,), precision=1)
    refused(ref.produce_collection(per_stream_large),
            "per-stream-observation-limit")
    oversized_transcript = tuple(ref.make_observation(
        index, f"stream-{(index - 1) % 4 + 1}", (index - 1) // 4 + 1, 0,
        f"large-event-{index}") for index in range(1, 514))
    global_large = ref.make_collection(
        registry(4), F(1, 20), tuple((f"stream-{i}", F(1, 100))
                                     for i in range(1, 5)),
        transcript=oversized_transcript)
    refused(ref.produce_collection(global_large), "transcript-length-limit")
    original_replay = ref.replay_transcript
    ref.replay_transcript = disabled
    try:
        refused(ref.produce_collection(global_large), "transcript-length-limit")
    finally:
        ref.replay_transcript = original_replay

    five_actions = tuple(ref.make_affine_action(
        f"a{i}", i, {"stream-1": 0, "stream-2": 0}) for i in range(5))
    action_large = ref.make_decision(collection, five_actions, intended_action="a0")
    refused(ref.produce_decision(action_large, coverage_evidence),
            "action-count-limit")
    refused(ref.consume_decision(action_large, None), "action-count-limit")
    max_precision = round_robin_collection(((),), precision=64)
    max_coverage = ref.produce_coverage(
        max_precision, ref.produce_collection(max_precision))
    check(ref.consume_coverage(max_precision, max_coverage)["status"] ==
          "checked-multistream-coverage", "precision boundary rejected")
    four_actions = tuple(ref.make_affine_action(
        f"b{i}", i, {"stream-1": 0, "stream-2": 0}) for i in range(4))
    four_request = ref.make_decision(collection, four_actions,
                                     intended_action="b0")
    check(ref.consume_decision(
        four_request, ref.produce_decision(four_request, coverage_evidence))["status"] ==
          "checked-multistream-decision", "action boundary rejected")

    huge = 2**255 - 1
    large_actions = (
        ref.make_affine_action("large", huge,
                               {"stream-1": huge, "stream-2": huge}),
        ref.make_affine_action("zero", -huge,
                               {"stream-1": -huge, "stream-2": -huge}),
    )
    large_request = ref.make_decision(collection, large_actions,
                                      intended_action="large")
    large_result = ref.consume_decision(
        large_request, ref.produce_decision(large_request, coverage_evidence))
    check(large_result["named_action_regret"].numerator.bit_length() > 256,
          "valid derived exact coordinate was capped")

    raw_registry = list(registry())
    raw_transcript = []
    immutable = ref.make_collection(
        raw_registry, F(1, 20), (("stream-1", F(1, 40)),
                                ("stream-2", F(1, 40))),
        transcript=raw_transcript)
    raw_registry.clear(); raw_transcript.append("mutated")
    check(len(immutable.registry) == 2 and immutable.transcript == (),
          "collection snapshot is mutable through caller input")

    stale_unit = replace(decision, loss_unit="other-unit")
    rejected(lambda: ref.consume_decision(stale_unit, decision_evidence),
             "stale loss-unit evidence accepted")
    other = ref.make_affine_action("other", 1,
                                   {"stream-1": 0, "stream-2": 0})
    intended_request = ref.make_decision(collection, (action, other),
                                         unit="manual-loss",
                                         intended_action="other")
    rejected(lambda: ref.consume_decision(intended_request, decision_evidence),
             "stale intended-action evidence accepted")
    unfinished_child = replace(coverage_evidence,
                               scalar_evidence=(("stream-1", {"status": "unfinished"}),
                                                scalar_rows[1]))
    rejected(lambda: ref.consume_coverage(collection, unfinished_child),
             "unfinished scalar child became usable")
    return {"manual_evidence_with_producers_disabled": True,
            "adversarial_mutations_rejected": True,
            "coarse_valid_witness_accepted": True,
            "boundary_transcript": len(boundary.transcript),
            "derived_coordinate_bits":
                large_result["named_action_regret"].numerator.bit_length(),
            "early_refusal_before_replay": True}


def main():
    groups = {
        "M1": m1_scalar_reduction(),
        "M2": m2_two_stream_actions(),
        "M3": m3_adaptive_collection(),
        "M4": m4_adaptive_count_counterexample(),
        "M5": m5_omission_and_copying(),
        "M6": m6_allocation_identity_and_revisions(),
        "M7": m7_dependence_boundary(),
        "M8": m8_end_to_end_adversarial(),
    }
    source_hashes = {}
    for name in ("reference.py", "checks.py"):
        source_hashes[name] = hashlib.sha256(
            (Path(__file__).parent / name).read_bytes()).hexdigest()
    print(json.dumps(ref.wire({"status": "passed", "groups": groups,
                               "source_sha256": source_hashes}),
                     sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
