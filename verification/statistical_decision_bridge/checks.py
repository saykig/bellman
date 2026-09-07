"""Authored exact cases and independent arithmetic for the statistical bridge."""
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys

import reference as r

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "joint_law_completion"))
import joint_law as j


rejections = 0
unfinished = 0


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def reject(operation):
    global rejections
    try:
        operation()
    except r.Invalid:
        rejections += 1
        return
    raise RuntimeError("invalid statistical or decision claim accepted")


def refuse(result, reason):
    global unfinished
    need(type(result) is dict and result.get("status") == "unfinished" and
         result.get("reason") == reason, "wrong resource-refusal disposition")
    unfinished += 1


def sampling(observations, alpha=F(1, 20), bits=16, **kwargs):
    return r.make_sampling(observations, alpha, precision_bits=bits, **kwargs)


def zero_one(request, intended="predict1"):
    return r.make_decision(request,
                           (("predict0", (0, 1)), ("predict1", (1, 0))),
                           intended_action=intended, unit="misclassification-loss")


def recurrence_distribution(n, probability):
    """Independent Pascal recursion; no binomial coefficients or reference tails."""
    distribution = [F(1)]
    for _ in range(n):
        next_distribution = [F(0)] * (len(distribution) + 1)
        for k, mass in enumerate(distribution):
            next_distribution[k] += mass * (1 - probability)
            next_distribution[k + 1] += mass * probability
        distribution = next_distribution
    return tuple(distribution)


def recurrence_tail(n, k, probability, upper):
    distribution = recurrence_distribution(n, probability)
    return sum(distribution[k:] if upper else distribution[:k + 1], F(0))


def direct_path_exclusion(horizon, probability, alpha, allocation):
    """Independent full binary-path enumeration for a small horizon."""
    total = F(0)
    for path in product((0, 1), repeat=horizon):
        path_mass = probability**sum(path) * (1 - probability)**(horizon - sum(path))
        k = 0
        for n, observation in enumerate(path, 1):
            k += observation
            allowance = (alpha / 2 if allocation == "fixed-equal-tailed"
                          else alpha / (2 * n * (n + 1)))
            if (recurrence_tail(n, k, probability, True) < allowance or
                    recurrence_tail(n, k, probability, False) < allowance):
                total += path_mass
                break
    return total


def pairwise_map(evidence):
    return {(first, second): value for first, second, value in evidence.pairwise_extrema}


def run():
    results = []

    def record(name, **values):
        results.append(dict(case=name, status="PASS", **values))

    # S1: boundary conventions, non-default alpha, equality witnesses and exact tails.
    empty_request = sampling([], bits=16)
    empty_evidence = r.produce_interval(empty_request)
    empty = r.consume_interval(empty_request, empty_evidence)
    need(empty["outward_interval"] == (F(0), F(1)) and empty["k"] == empty["n"] == 0,
         "n=0 interval")
    empty_decision_request = zero_one(empty_request)
    empty_decision = r.consume_decision(
        empty_decision_request,
        r.produce_decision(empty_decision_request, empty_evidence))
    need(empty_decision["common_minimizers"] == () and
         empty_decision["named_action_regret"] == 1, "n=0 trivial decision bounds")

    zero_request = sampling([0] * 5)
    one_request = sampling([1] * 5)
    zero_interval = r.consume_interval(zero_request, r.produce_interval(zero_request))
    one_interval = r.consume_interval(one_request, r.produce_interval(one_request))
    need(zero_interval["outward_interval"][0] == 0 and
         one_interval["outward_interval"][1] == 1 and
         zero_interval["outward_interval"][0] <= 0 <= zero_interval["outward_interval"][1] and
         one_interval["outward_interval"][0] <= 1 <= one_interval["outward_interval"][1],
         "p=0 and p=1 boundaries")

    interior_request = sampling([1, 0, 1, 0], alpha=F(1, 7), bits=12)
    interior_evidence = r.produce_interval(interior_request)
    interior = r.consume_interval(interior_request, interior_evidence)
    n, k, allowance = 4, 2, F(1, 7) / 40
    need(interior["per_tail_allowance"] == allowance and
         r.tail_plus(n, k, interior_evidence.lower_bracket[0]) ==
         recurrence_tail(n, k, interior_evidence.lower_bracket[0], True) and
         r.tail_minus(n, k, interior_evidence.upper_bracket[1]) ==
         recurrence_tail(n, k, interior_evidence.upper_bracket[1], False),
         "interior exact-tail cross-check")

    lower_subject = sampling([1], alpha=F(1, 2), bits=16)
    lower_equality = r.IntervalEvidence(
        lower_subject, 1, 1, F(1, 8), (F(1, 8), F(1, 8)),
        (F(1), F(1)), (F(1, 8), F(1)), True,
        r.prefix_digest(lower_subject))
    r.consume_interval(lower_subject, lower_equality)
    upper_subject = sampling([0], alpha=F(1, 2), bits=16)
    upper_equality = r.IntervalEvidence(
        upper_subject, 1, 0, F(1, 8), (F(0), F(0)),
        (F(7, 8), F(7, 8)), (F(0), F(7, 8)), True,
        r.prefix_digest(upper_subject))
    r.consume_interval(upper_subject, upper_equality)

    # Derived proof coordinates are not subject to the external 256-bit input cap.
    huge_upper = F(1, 8) + F(1, 2**300)
    huge_coordinate = replace(lower_equality,
                              lower_bracket=(F(1, 8), huge_upper),
                              outward_interval=(F(1, 8), F(1)))
    r.consume_interval(lower_subject, huge_coordinate)
    need(huge_upper.numerator.bit_length() > 256, "large derived proof coordinate")
    record("S1_boundaries_brackets_and_exact_tails",
           empty_interval=empty["outward_interval"],
           zero_success_interval=zero_interval["outward_interval"],
           all_success_interval=one_interval["outward_interval"],
           interior_interval=interior["outward_interval"],
           equality_roots=(F(1, 8), F(7, 8)),
           derived_coordinate_bits=huge_upper.numerator.bit_length())

    # S1 adversarial controls and a mathematically valid but under-precise witness.
    fine_subject = sampling([1] * 16)
    fine_evidence = r.produce_interval(fine_subject)
    fine = r.consume_interval(fine_subject, fine_evidence)
    coarse = r.IntervalEvidence(
        fine_subject, 16, 16, r.epsilon(fine_subject.alpha, 16),
        (F(0), F(1)), (F(1), F(1)), (F(0), F(1)), False,
        r.prefix_digest(fine_subject))
    coarse_result = r.consume_interval(fine_subject, coarse)
    need(coarse_result["status"] == "valid-coarse-outward-enclosure" and
         not coarse_result["requested_precision_met"], "coarse witness disposition")
    coarse_decision_request = zero_one(fine_subject)
    coarse_decision = r.consume_decision(
        coarse_decision_request,
        r.produce_decision(coarse_decision_request, coarse))
    need(coarse_decision["common_minimizers"] == (),
         "coarse interval should leave zero-one choice uncertified")

    reject(lambda: r.consume_interval(fine_subject,
                                      replace(fine_evidence, claimed_n=15)))
    reject(lambda: r.consume_interval(fine_subject,
                                      replace(fine_evidence, claimed_k=15)))
    reject(lambda: r.consume_interval(
        fine_subject, replace(fine_evidence,
                              per_tail_allowance=2 * fine_evidence.per_tail_allowance)))
    reject(lambda: r.consume_interval(
        fine_subject, replace(fine_evidence, per_tail_allowance=False)))
    reject(lambda: r.consume_interval(
        sampling([1] * 16, stream="other-stream"), fine_evidence))
    reject(lambda: r.consume_interval(
        fine_subject, replace(fine_evidence,
                              lower_bracket=tuple(reversed(fine_evidence.lower_bracket)))))
    reject(lambda: r.consume_interval(
        fine_subject, replace(fine_evidence,
                              lower_bracket=(fine_evidence.lower_bracket[1],
                                             fine_evidence.lower_bracket[1]))))
    reject(lambda: r.consume_interval(
        fine_subject, replace(fine_evidence, upper_bracket=(F(0), F(1)))))
    reject(lambda: r.consume_interval(
        fine_subject, replace(fine_evidence, outward_interval=(F(0), F(1)))))
    reject(lambda: r.consume_interval(fine_subject,
                                      replace(coarse, precision_claimed=True)))
    reject(lambda: r.consume_interval(
        fine_subject, replace(fine_evidence, lower_bracket=())))
    reject(lambda: r.consume_interval(
        fine_subject, replace(fine_evidence,
                              lower_bracket=(0.0, fine_evidence.lower_bracket[1]))))
    reject(lambda: r.consume_interval(
        fine_subject, replace(fine_evidence, subject_digest="same-looking-label")))
    reject(lambda: r.make_sampling([True]))
    reject(lambda: r.make_sampling([0], alpha=0.05))
    reject(lambda: r.make_sampling([0], alpha=F(0)))
    reject(lambda: r.make_sampling([0], alpha=F(1)))
    reject(lambda: r.make_sampling([0], precision_bits=True))
    reject(lambda: r.make_sampling([0], premise="exchangeable"))
    reject(lambda: r.make_sampling([0], spending_rule="fixed-time"))
    reject(lambda: r.make_action("bad-float", (0.0, 1)))
    reject(lambda: r.make_action("bad-bool", (False, 1)))
    reject(lambda: r.make_decision(fine_subject,
                                   (("a", (0, 1)),), intended_action="a",
                                   query="midpoint-choice"))
    record("S1_adversarial_witness_and_input_controls",
           fine_interval=fine["outward_interval"],
           coarse_interval=coarse_result["outward_interval"],
           coarse_decision="not-certified")

    # S2: exact repeated-inspection arithmetic, plus independent small-path enumeration.
    alpha = F(1, 20)
    probability = F(1, 2)
    fixed = r.first_exclusion_probability(
        32, probability, alpha, "fixed-equal-tailed")
    anytime = r.first_exclusion_probability(
        32, probability, alpha, r.SPENDING_RULE)
    need(fixed["excluded"] == F(8962675, 67108864), "fixed-time benchmark")
    need(anytime["excluded"] == F(444183, 1073741824), "anytime benchmark")
    need(fixed["excluded"] + fixed["surviving"] == 1 and
         anytime["excluded"] + anytime["surviving"] == 1,
         "dynamic probability conservation")
    for allocation in ("fixed-equal-tailed", r.SPENDING_RULE):
        dynamic_small = r.first_exclusion_probability(
            10, probability, alpha, allocation)["excluded"]
        need(dynamic_small == direct_path_exclusion(
            10, probability, alpha, allocation), "dynamic versus path recursion")
    first32 = r.allocated_failure(alpha, 32)
    need(first32 == F(8, 165), "first-32 spending allocation")
    record("S2_repeated_inspection_exact_recursion",
           fixed_time_exclusion=fixed["excluded"],
           anytime_exclusion=anytime["excluded"],
           anytime_first32_allocation=first32,
           fixed_exceeds_nominal_alpha=fixed["excluded"] > alpha)

    # S3: exact outward endpoints and a decision certified without a point estimate.
    sample8, sample16 = sampling([1] * 8), sampling([1] * 16)
    evidence8, evidence16 = r.produce_interval(sample8), r.produce_interval(sample16)
    checked8 = r.consume_interval(sample8, evidence8)
    checked16 = r.consume_interval(sample16, evidence16)
    need(checked8["outward_interval"] == (F(24213, 65536), F(1)) and
         checked16["outward_interval"] == (F(36659, 65536), F(1)),
         "S3 dyadic enclosures")
    decision8_request, decision16_request = zero_one(sample8), zero_one(sample16)
    decision8_evidence = r.produce_decision(decision8_request, evidence8)
    decision16_evidence = r.produce_decision(decision16_request, evidence16)
    decision8 = r.consume_decision(decision8_request, decision8_evidence)
    decision16 = r.consume_decision(decision16_request, decision16_evidence)
    difference16 = pairwise_map(decision16_evidence)[("predict1", "predict0")]
    need(decision8["common_minimizers"] == () and
         decision16["common_minimizers"] == ("predict1",) and
         decision16["uniformly_strict_actions"] == ("predict1",) and
         difference16 == F(-3891, 32768) and
         decision16["named_action_regret"] == 0,
         "S3 zero-one decision")
    record("S3_decision_without_point_estimate",
           n8_interval=checked8["outward_interval"],
           n8_common_minimizers=decision8["common_minimizers"],
           n16_interval=checked16["outward_interval"],
           n16_common_minimizers=decision16["common_minimizers"],
           n16_minimum_advantage=-difference16)

    # Changed losses reuse the sampling evidence but receive a new decision result.
    changed_request = r.make_decision(
        sample16, (("predict0", (0, 1)), ("predict1", (4, 0))),
        intended_action="predict1", unit="changed-loss")
    changed = r.consume_decision(
        changed_request, r.produce_decision(changed_request, evidence16))
    need(changed["common_minimizers"] == () and
         r.consume_interval(sample16, evidence16)["outward_interval"] ==
         checked16["outward_interval"], "changed decision versus unchanged sampling result")

    tie_request = r.make_decision(
        sample16, (("a", (0, 0)), ("b", (0, 0)), ("worse", (1, 1))),
        intended_action="a", unit="signed-loss")
    tie = r.consume_decision(tie_request,
                             r.produce_decision(tie_request, evidence16))
    need(tie["common_minimizers"] == ("a", "b") and
         tie["uniformly_strict_actions"] == (), "complete tie set")
    singleton_request = r.make_decision(
        sample16, (("only", (-2, 3)),), intended_action="only", unit="signed-loss")
    singleton = r.consume_decision(
        singleton_request, r.produce_decision(singleton_request, evidence16))
    need(singleton["common_minimizers"] == ("only",) and
         singleton["uniformly_strict_actions"] == ("only",) and
         singleton["strictness_vacuous_for_singleton"] and
         singleton["named_action_regret"] == 0, "singleton decision semantics")
    record("S3_changed_losses_ties_and_singleton",
           changed_loss_common_minimizers=changed["common_minimizers"],
           tied_complete_set=tie["common_minimizers"],
           singleton_strictness="vacuous-against-no-distinct-action")

    # S4: copied data expose a false IID premise, not a detectable byte pattern.
    copied_zero, copied_one = sampling([0] * 16), sampling([1] * 16)
    copied_zero_interval = r.consume_interval(
        copied_zero, r.produce_interval(copied_zero))["outward_interval"]
    copied_one_interval = r.consume_interval(
        copied_one, r.produce_interval(copied_one))["outward_interval"]
    copied_allowance = r.epsilon(alpha, 16)
    need(copied_zero_interval[1] < F(1, 2) < copied_one_interval[0] and
         r.tail_minus(16, 0, F(1, 2)) < copied_allowance and
         r.tail_plus(16, 16, F(1, 2)) < copied_allowance and
         F(1, 2) + F(1, 2) == 1, "copied fair outcome excludes with probability one")
    reject(lambda: sampling([0] * 16, premise="copied-dependent-sequence"))
    copied_other_id = sampling([0] * 16, stream="different-byte-identity")
    need(r.prefix_digest(copied_zero) != r.prefix_digest(copied_other_id) and
         r.consume_interval(copied_other_id,
                            r.produce_interval(copied_other_id))["outward_interval"] ==
         copied_zero_interval, "identity binds data but cannot prove independence")
    record("S4_dependence_and_duplicate_evidence_boundary",
           copied_zero_interval=copied_zero_interval,
           copied_one_interval=copied_one_interval,
           exclusion_probability_under_copying=F(1),
           iid_premise_false_in_control=True,
           byte_identity_proves_independence=False)

    # S5: revisions, stale subjects, immutable inputs and resource refusal.
    observations = [1, 0]
    loss0, loss1 = [0, 1], [1, 0]
    immutable_sample = sampling(observations)
    immutable_decision = r.make_decision(
        immutable_sample, (("p0", loss0), ("p1", loss1)),
        intended_action="p1", unit="loss")
    observations[0], loss0[0], loss1[1] = 0, 99, 99
    need(immutable_sample.observations == (1, 0) and
         immutable_decision.actions[0].losses == (F(0), F(1)) and
         immutable_decision.actions[1].losses == (F(1), F(0)),
         "caller containers were not snapshotted")

    base_sample = sampling([1, 0, 1])
    same_sample = sampling([1, 0, 1])
    appended_sample = sampling([1, 0, 1, 1])
    corrected_sample = sampling([1, 1, 1])
    retroselected_sample = sampling([1, 0])
    changed_alpha_sample = sampling([1, 0, 1], alpha=F(1, 10))
    changed_population_sample = sampling([1, 0, 1], population="population-2")
    need(r.classify_sampling_revision(base_sample, same_sample) ==
         "same-prefix-recalculation-no-new-evidence" and
         r.classify_sampling_revision(base_sample, appended_sample) ==
         "append-only-observation-extension" and
         r.classify_sampling_revision(base_sample, corrected_sample) ==
         "corrected-or-retroselected-history-new-claim" and
         r.classify_sampling_revision(base_sample, retroselected_sample) ==
         "corrected-or-retroselected-history-new-claim" and
         r.classify_sampling_revision(base_sample, changed_alpha_sample) ==
         "new-coverage-specification" and
         r.classify_sampling_revision(base_sample, changed_population_sample) ==
         "new-sampling-subject", "sampling revision semantics")
    base_interval_evidence = r.produce_interval(base_sample)
    reject(lambda: r.consume_interval(appended_sample, base_interval_evidence))

    base_decision_request = zero_one(base_sample)
    base_decision_evidence = r.produce_decision(
        base_decision_request, base_interval_evidence)
    changed_decision_request = r.make_decision(
        base_sample, (("predict0", (0, 1)), ("predict1", (2, 0))),
        intended_action="predict1", unit="loss")
    need(r.classify_decision_revision(base_decision_request,
                                      changed_decision_request) ==
         "same-data-new-decision-query", "decision revision semantics")
    reject(lambda: r.consume_decision(changed_decision_request,
                                      base_decision_evidence))
    changed_unit_request = r.make_decision(
        base_sample, (("predict0", (0, 1)), ("predict1", (1, 0))),
        intended_action="predict1", unit="utility")
    reject(lambda: r.consume_decision(changed_unit_request,
                                      base_decision_evidence))
    reject(lambda: r.consume_decision(
        base_decision_request,
        replace(base_decision_evidence, uniformly_strict_actions=("predict1",))))
    reject(lambda: r.consume_decision(
        base_decision_request,
        replace(base_decision_evidence, named_action_regret=F(99))))
    reject(lambda: r.consume_decision(
        base_decision_request,
        replace(base_decision_evidence, pairwise_extrema=
                base_decision_evidence.pairwise_extrema[:-1])))

    refuse(r.produce_interval(sampling([0] * 129)), "sample-size-limit")
    refuse(r.produce_interval(sampling([0], bits=65)),
           "bisection-precision-limit")
    five_action_request = r.make_decision(
        sampling([0]), tuple((f"a{i}", (i, i + 1)) for i in range(5)),
        intended_action="a0")
    refuse(r.produce_decision(five_action_request,
                              r.produce_interval(five_action_request.sampling)),
           "action-count-limit")
    record("S5_revision_binding_immutability_and_resources",
           same_prefix="not-new-evidence",
           append="new-prefix-claim",
           correction="not-an-append",
           changed_loss="new-decision-certificate",
           resource_refusals=3)

    # S6: the retained interval is the two-atom joint-law polytope p=(1-q,q).
    lower, upper = checked16["outward_interval"]
    model = j.make_model(
        ("future-outcome",), (("0",), ("1",)),
        ((1, 1),), (1,), ((0, 1), (0, -1)), (upper, -lower),
        premises=("retained outward Bernoulli interval",))
    task = j.make_task(
        model, (1, 1), (0, 0), conditional=False, event_label="whole-space",
        query_label="affine action-risk difference", unit="misclassification-loss",
        actions=tuple((action.label, action.losses)
                      for action in decision16_request.actions))
    comparison = j.difference(task, "predict1", "predict0")
    proposed = j.propose(comparison)
    need(proposed["status"] == "certificate", "joint-law cross-check construction")
    joint_result = j.consume(comparison, proposed["certificate"])
    need(joint_result["status"] == "original_optimum" and
         joint_result["value"] == difference16 and
         j.original_member(model, (1 - lower, lower)) and
         j.original_member(model, (1 - upper, upper)),
         "joint-law risk-difference cross-check")
    record("S6_existing_joint_law_cross_check",
           probability_vector="(1-p,p)",
           interval_constraints=(lower, upper),
           risk_difference_maximum=joint_result["value"],
           existing_receiver_status=joint_result["status"])

    # Receiving remains valid with all candidate/root-search producers disabled.
    manual = lower_equality
    retained_interval = evidence16
    retained_decision = decision16_evidence
    old_interval_producer, old_decision_producer = r.produce_interval, r.produce_decision
    old_lower_search, old_upper_search = r._bisect_lower, r._bisect_upper

    def disabled(*_args, **_kwargs):
        raise RuntimeError("producer called during receiving")

    try:
        r.produce_interval = disabled
        r.produce_decision = disabled
        r._bisect_lower = disabled
        r._bisect_upper = disabled
        manual_result = r.consume_interval(lower_subject, manual)
        retained_interval_result = r.consume_interval(sample16, retained_interval)
        retained_decision_result = r.consume_decision(
            decision16_request, retained_decision)
    finally:
        r.produce_interval = old_interval_producer
        r.produce_decision = old_decision_producer
        r._bisect_lower = old_lower_search
        r._bisect_upper = old_upper_search
    need(manual_result["outward_interval"] == (F(1, 8), F(1)) and
         retained_interval_result["outward_interval"] == (lower, upper) and
         retained_decision_result["common_minimizers"] == ("predict1",),
         "producer-independent receiving")
    record("S6_producer_independent_receiving",
           implementation_independent_witness=True,
           candidate_and_root_search_disabled=True,
           shared_fraction_arithmetic=True)

    output = {
        "passed": len(results),
        "failed": 0,
        "rejections": rejections,
        "unfinished": unfinished,
        "results": results,
    }
    print(json.dumps(r.wire(output), sort_keys=True))


if __name__ == "__main__":
    run()
