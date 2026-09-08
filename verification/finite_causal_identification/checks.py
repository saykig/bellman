#!/usr/bin/env python3
"""Exact positive, adversarial, stale-binding, and receiver checks."""
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from verification.finite_causal_identification import reference as ref  # noqa: E402


results = []
rejections = 0


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def reject(operation, message):
    global rejections
    try:
        operation()
    except (ref.Invalid, TypeError, ValueError):
        rejections += 1
        return
    raise AssertionError(message)


def record(case, **values):
    results.append({"case": case, "status": "PASS", **values})


CODING = ref.BinaryCoding("treatment-A", "bad-outcome-Y")
PREMISES = ref.AdjustmentPremises(
    "supplied-backdoor-premises-v1",
    "adjust-exactly-pre-action-Z-v1",
    ("pre-action-Z",),
    "consistency-for-A-and-Y-v1",
    "Y(a)-independent-of-A-given-Z-v1",
    "Z-measured-before-A-v1",
    "do-A-overrides-natural-A-v1")
BAD_LOSS = ref.DecisionTable(
    "bad-outcome-loss-v1", "expected bad-outcome units",
    (F(0), F(0)), ((F(0), F(1)), (F(0), F(1))))


def no_confounding_observation():
    # Within each Z stratum: P(A)=1/2, P(Y=1|A=0)=1/4,
    # P(Y=1|A=1)=3/4.  The two strata are identical.
    return ref.AdjustmentObservation(
        "randomized-observational-law-v1", "population-randomized-v1",
        CODING, "pre-action-Z", ("z0", "z1"),
        (F(3, 16), F(1, 16), F(1, 16), F(3, 16),
         F(3, 16), F(1, 16), F(1, 16), F(3, 16)))


def simpson_observation():
    return ref.AdjustmentObservation(
        "simpson-observational-law-v1", "simpson-population-v1",
        CODING, "pre-action-Z", ("z0", "z1"),
        (F(9, 200), F(1, 200), F(9, 25), F(9, 100),
         F(9, 100), F(9, 25), F(1, 200), F(9, 200)))


def response_observation(masses=(F(1, 4),) * 4):
    return ref.ResponseObservation(
        "symmetric-observational-law-v1", "response-population-v1",
        CODING, masses)


def response_request(*, restrictions=(), outer=False, observation=None,
                     profile="binary-response-types-v1",
                     query="both-binary-intervention-bad-outcome-risks-v1"):
    return ref.ResponseFiberRequest(
        observation or response_observation(), profile, tuple(restrictions),
        query, outer)


def exact_unrestricted_vertices():
    """Independent direct enumeration for four observed cells of mass 1/4."""
    choices = (
        ((0, 0, 0), (0, 0, 1)),
        ((0, 1, 0), (0, 1, 1)),
        ((1, 0, 0), (1, 1, 0)),
        ((1, 0, 1), (1, 1, 1)),
    )
    answer = set()
    for selected in product((0, 1), repeat=4):
        point = [F(0)] * 8
        for cell, choice in enumerate(selected):
            atom = choices[cell][choice]
            point[ref.RESPONSE_TYPES.index(atom)] += F(1, 4)
        answer.add(tuple(point))
    return tuple(sorted(answer))


def route_a_no_confounding():
    observation = no_confounding_observation()
    distributions = []
    for action, expected in ((0, (F(3, 4), F(1, 4))),
                             (1, (F(1, 4), F(3, 4)))):
        request = ref.AdjustmentRequest(
            observation, PREMISES, action, f"randomized-do-{action}-v1")
        evidence = ref.produce_adjustment(request)
        accepted = ref.consume_adjustment(request, evidence)
        check(accepted["status"] == ref.ADJUSTED and
              accepted["distribution"] == expected,
              "valid no-confounding adjustment")
        check(ref.observational_distribution(observation, action) == expected,
              "randomized observational control")
        distributions.append(expected)
    decision_request = ref.AdjustmentDecisionRequest(
        observation, PREMISES, BAD_LOSS, "randomized-causal-decision-v1")
    decision = ref.consume_adjustment_decision(
        decision_request, ref.produce_adjustment_decision(decision_request))
    check(decision["risks"] == (F(1, 4), F(3, 4)) and
          decision["complete_minimizing_set"] == (0,),
          "adjusted decision calculation")
    record("A1_valid_adjustment_no_confounding",
           intervention_distributions=distributions,
           decision_risks=decision["risks"],
           minimizing_actions=decision["complete_minimizing_set"])


def route_a_simpson_reversal():
    observation = simpson_observation()
    association = tuple(ref.observational_distribution(observation, action)[1]
                        for action in (0, 1))
    check(association == (F(73, 100), F(27, 100)),
          "mandatory observational Simpson values")
    intervention = []
    for action in (0, 1):
        request = ref.AdjustmentRequest(
            observation, PREMISES, action, f"simpson-do-{action}-v1")
        intervention.append(ref.consume_adjustment(
            request, ref.produce_adjustment(request))["distribution"][1])
    check(tuple(intervention) == (F(9, 20), F(11, 20)),
          "mandatory adjusted Simpson values")
    request = ref.AdjustmentDecisionRequest(
        observation, PREMISES, BAD_LOSS, "simpson-causal-decision-v1")
    decision = ref.consume_adjustment_decision(
        request, ref.produce_adjustment_decision(request))
    check(association[1] < association[0] and
          decision["risks"][0] < decision["risks"][1] and
          decision["complete_minimizing_set"] == (0,),
          "observational and interventional recommendations must reverse")
    record("A2_simpson_observation_is_not_intervention",
           observational_bad_outcome_by_action=association,
           adjusted_bad_outcome_by_action=tuple(intervention),
           naive_observational_choice=1, causal_choice=0)


def route_a_positivity_and_staleness():
    positivity = ref.AdjustmentObservation(
        "positivity-control-v1", "positivity-population-v1", CODING,
        "pre-action-Z", ("supported", "missing-A0"),
        (F(1, 8), F(1, 8), F(1, 8), F(1, 8),
         F(0), F(0), F(1, 4), F(1, 4)))
    request = ref.AdjustmentRequest(
        positivity, PREMISES, 0, "positivity-do-0-v1")
    evidence = ref.produce_adjustment(request)
    accepted = ref.consume_adjustment(request, evidence)
    check(accepted["status"] == ref.POSITIVITY_FAILURE and
          accepted["missing_strata"] == ("missing-A0",),
          "positivity failure classification")
    check("not declared absent" in accepted["checked"],
          "positivity failure cannot mean no causal effect")

    base = simpson_observation()
    intended = ref.AdjustmentRequest(base, PREMISES, 0, "stale-do-0-v1")
    old = ref.produce_adjustment(intended)
    changed_masses = list(base.masses)
    changed_masses[0], changed_masses[1] = changed_masses[1], changed_masses[0]
    changed_observation = replace(base, identity="simpson-observation-v2",
                                  masses=tuple(changed_masses))
    changes = (
        replace(intended, observation=changed_observation),
        replace(intended, premises=replace(
            PREMISES, identity="different-causal-premise-v2")),
        replace(intended, premises=replace(
            PREMISES, adjustment_set_identity="same-Z-new-adjustment-claim-v2")),
        replace(intended, observation=replace(
            base, coding=replace(CODING,
                                 action_values=("untreated", "treated")))),
        replace(intended, query_identity="different-intervention-query-v2"),
    )
    for changed in changes:
        reject(lambda changed=changed: ref.consume_adjustment(changed, old),
               "stale adjustment evidence accepted")
    record("A3_positivity_boundary_and_stale_adjustment",
           outcome_status=accepted["status"],
           missing_strata=accepted["missing_strata"],
           stale_mutations_rejected=len(changes))


def route_b_partial_and_independent_enumeration():
    request = response_request()
    evidence = ref.produce_response_fiber(request)
    accepted = ref.consume_response_fiber(request, evidence)
    direct = exact_unrestricted_vertices()
    check(accepted["status"] == ref.PARTIAL and
          accepted["vertices"] == direct and len(direct) == 16,
          "complete unrestricted response-type fiber")
    bounds = accepted["intervention_bounds"]
    check(tuple((bound.lower, bound.upper) for bound in bounds) ==
          ((F(1, 4), F(3, 4)), (F(1, 4), F(3, 4))),
          "unrestricted intervention bounds")
    check(bounds[0].lower_witness != bounds[0].upper_witness and
          ref.dot(ref.intervention_coefficients(0),
                  bounds[0].lower_witness) == F(1, 4) and
          ref.dot(ref.intervention_coefficients(0),
                  bounds[0].upper_witness) == F(3, 4),
          "two exact nonidentification witnesses")
    record("B1_exact_partial_identification",
           vertex_count=len(direct),
           intervention_bounds=tuple((item.lower, item.upper)
                                     for item in bounds),
           do0_lower_witness=bounds[0].lower_witness,
           do0_upper_witness=bounds[0].upper_witness,
           distinct_attaining_witnesses=True)


def route_b_supported_restrictions_and_point_id():
    monotone = ref.MonotonicityRestriction(
        "MTR-Y1-at-least-Y0-v1", "nondecreasing")
    monotone_request = response_request(restrictions=(monotone,))
    monotone_result = ref.consume_response_fiber(
        monotone_request, ref.produce_response_fiber(monotone_request))
    check(monotone_result["status"] == ref.PARTIAL and
          all(not (y0 == 1 and y1 == 0) or vertex[index] == 0
              for vertex in monotone_result["vertices"]
              for index, (_, y0, y1) in enumerate(ref.RESPONSE_TYPES)),
          "typed monotone response restriction")
    harm_prevention = ref.MonotonicityRestriction(
        "MHP-Y1-at-most-Y0-v1", "nonincreasing")
    prevention_request = response_request(restrictions=(harm_prevention,))
    prevention_result = ref.consume_response_fiber(
        prevention_request, ref.produce_response_fiber(prevention_request))
    check(prevention_result["status"] == ref.PARTIAL and
          all(not (y0 == 0 and y1 == 1) or vertex[index] == 0
              for vertex in prevention_result["vertices"]
              for index, (_, y0, y1) in enumerate(ref.RESPONSE_TYPES)),
          "typed monotone harm-prevention restriction")

    calibrations = (
        ref.LinearEqualityRestriction(
            "calibrate-do0-bad-to-half-v1",
            ref.intervention_coefficients(0), F(1, 2)),
        ref.LinearEqualityRestriction(
            "calibrate-do1-bad-to-half-v1",
            ref.intervention_coefficients(1), F(1, 2)),
    )
    point_request = response_request(restrictions=calibrations,
                                     query="calibrated-point-effects-v1")
    point = ref.consume_response_fiber(
        point_request, ref.produce_response_fiber(point_request))
    check(point["status"] == ref.POINT and
          tuple((item.lower, item.upper) for item in
                point["intervention_bounds"]) ==
          ((F(1, 2), F(1, 2)), (F(1, 2), F(1, 2))),
          "supported equalities must point-identify both marginals")
    record("B2_typed_restrictions_and_point_identification",
           monotone_vertex_count=len(monotone_result["vertices"]),
           harm_prevention_vertex_count=len(prevention_result["vertices"]),
           point_intervention_probabilities=(F(1, 2), F(1, 2)))


def route_b_decision_identified_despite_uncertainty():
    fiber = response_request()
    decision = ref.DecisionTable(
        "dominant-cost-decision-v1", "expected loss points", (F(0), F(1)),
        ((F(0), F(1)), (F(0), F(1))))
    request = ref.ResponseDecisionRequest(
        fiber, decision, "uniform-causal-action-query-v1")
    evidence = ref.produce_response_decision(request)
    accepted = ref.consume_response_decision(request, evidence)
    ranges = tuple((item.lower, item.upper) for item in
                   accepted["risk_bounds"])
    differences = {(item.candidate, item.competitor): item.maximum
                   for item in accepted["paired_differences"]}
    check(accepted["status"] == ref.DECISION_DESPITE_UNCERTAINTY and
          ranges == ((F(1, 4), F(3, 4)), (F(5, 4), F(7, 4))) and
          accepted["complete_common_minimizing_set"] == (0,) and
          accepted["strictly_common_actions"] == (0,) and
          differences[0, 1] < 0,
          "decision identification across a nonpoint exact causal fiber")
    record("B3_decision_identified_despite_causal_uncertainty",
           causal_probability_ranges=((F(1, 4), F(3, 4)),) * 2,
           action_risk_ranges=ranges,
           paired_difference_maxima=differences,
           common_minimizing_set=(0,))


def route_b_model_dependent_and_same_fiber_guard():
    request = ref.ResponseDecisionRequest(
        response_request(), BAD_LOSS, "model-dependent-causal-action-query-v1")
    evidence = ref.produce_response_decision(request)
    accepted = ref.consume_response_decision(request, evidence)
    differences = {(item.candidate, item.competitor): item.maximum
                   for item in accepted["paired_differences"]}
    opposite = accepted["opposite_preference_witnesses"]
    check(accepted["status"] == ref.MODEL_DEPENDENT and
          not accepted["complete_common_minimizing_set"] and
          differences == {(0, 1): F(1, 2), (1, 0): F(1, 2)} and
          tuple(item[0] for item in opposite) == (0, 1),
          "opposite action optima require model-dependent status")
    for preferred, witness in opposite:
        check(ref.same_fiber_difference(
            request, preferred, 1 - preferred, witness) < 0,
            "stored witness does not prefer its recorded action")
    reject(lambda: ref.cross_witness_difference(
        request, 0, opposite[0][1], 1, opposite[1][1]),
        "cross-witness action-risk subtraction accepted")
    check(ref.cross_witness_difference(
        request, 0, opposite[0][1], 1, opposite[0][1]) ==
          ref.same_fiber_difference(request, 0, 1, opposite[0][1]),
          "same-witness guard changed valid difference")
    record("B4_model_dependent_decision_and_paired_difference_guard",
           paired_difference_maxima=differences,
           opposite_preference_witnesses=opposite,
           cross_witness_subtraction="rejected")


def route_b_incompatible_and_unsupported():
    observed_a0_y1 = tuple(F(a_nat == 0 and y0 == 1)
                           for a_nat, y0, _ in ref.RESPONSE_TYPES)
    contradiction = ref.LinearEqualityRestriction(
        "force-observed-A0-Y1-mass-zero-v1", observed_a0_y1, F(0))
    impossible_request = response_request(
        restrictions=(contradiction,), query="incompatible-fiber-query-v1")
    impossible = ref.consume_response_fiber(
        impossible_request, ref.produce_response_fiber(impossible_request))
    check(impossible["status"] == ref.INCOMPATIBLE and
          not impossible["vertices"], "causal-fiber incompatibility")

    nonlinear = ref.UnsupportedRestriction(
        "independent-exogenous-errors-v1", "nonlinear-factorization")
    unsupported_request = response_request(
        restrictions=(nonlinear,), query="nonlinear-exact-fiber-v1")
    unsupported = ref.consume_response_fiber(
        unsupported_request, ref.produce_response_fiber(unsupported_request))
    check(unsupported["status"] == ref.UNSUPPORTED,
          "unsupported nonlinear restriction classification")
    outer_request = replace(unsupported_request,
                            outer_relaxation_requested=True)
    outer = ref.consume_response_fiber(
        outer_request, ref.produce_response_fiber(outer_request))
    check(outer["status"] == ref.OUTER_ONLY and
          outer["analyzed_domain"] == "outer" and
          outer["exact_fiber_status"] == ref.UNSUPPORTED and
          any(item.lower < item.upper for item in
              outer["intervention_bounds"]),
          "explicit outer relaxation labeling")
    outer_decision_request = ref.ResponseDecisionRequest(
        outer_request, BAD_LOSS, "outer-decision-not-earned-v1")
    outer_decision = ref.consume_response_decision(
        outer_decision_request,
        ref.produce_response_decision(outer_decision_request))
    check(outer_decision["status"] == ref.OUTER_ONLY,
          "outer relaxation silently earned exact decision")
    record("B5_incompatibility_unsupported_and_outer_distinction",
           incompatible_status=impossible["status"],
           unsupported_status=unsupported["status"],
           outer_status=outer["status"],
           outer_range_is_not_exact_nonidentification=True)


def stale_response_and_decision_evidence():
    base = response_request()
    evidence = ref.produce_response_fiber(base)
    changed_observation = response_observation(
        (F(1, 8), F(3, 8), F(1, 4), F(1, 4)))
    changed_observation = replace(
        changed_observation, identity="changed-response-observation-v2")
    changes = (
        replace(base, observation=changed_observation),
        replace(base, observation=replace(
            base.observation, coding=replace(
                CODING, action_values=("untreated", "treated"),
                outcome_values=("not-bad", "bad")))),
        replace(base, observation=replace(
            base.observation, population_identity="changed-population-v2")),
        replace(base, profile_identity="changed-response-profile-v2"),
        replace(base, restrictions=(ref.MonotonicityRestriction(
            "new-MTR-v2", "nondecreasing"),)),
        replace(base, query_identity="changed-causal-query-v2"),
    )
    for changed in changes:
        reject(lambda changed=changed: ref.consume_response_fiber(
            changed, evidence), "stale response-fiber evidence accepted")

    request = ref.ResponseDecisionRequest(
        base, BAD_LOSS, "stale-decision-query-v1")
    decision_evidence = ref.produce_response_decision(request)
    decision_changes = (
        replace(request, decision=replace(
            BAD_LOSS, identity="changed-cost-v2",
            costs=(F(1, 10), F(0)))),
        replace(request, decision=replace(
            BAD_LOSS, identity="changed-loss-v2",
            losses=((F(0), F(2)), (F(0), F(1))))),
        replace(request, query_identity="changed-decision-query-v2"),
    )
    for changed in decision_changes:
        reject(lambda changed=changed: ref.consume_response_decision(
            changed, decision_evidence), "stale decision evidence accepted")
    record("B6_complete_stale_subject_binding",
           response_mutations_rejected=len(changes),
           decision_mutations_rejected=len(decision_changes))


def forged_claims_and_malformed_inputs():
    fiber_request = response_request()
    fiber = ref.produce_response_fiber(fiber_request)
    forged_bound = replace(fiber.intervention_bounds[0], upper=F(1))
    reject(lambda: ref.consume_response_fiber(
        fiber_request, replace(
            fiber, intervention_bounds=(forged_bound,
                                        fiber.intervention_bounds[1]))),
        "forged causal bound accepted")
    reject(lambda: ref.consume_response_fiber(
        fiber_request, replace(fiber, vertices=fiber.vertices[:-1])),
        "incomplete vertex set accepted")
    decision_request = ref.ResponseDecisionRequest(
        fiber_request, BAD_LOSS, "forgery-decision-v1")
    decision = ref.produce_response_decision(decision_request)
    forged_difference = replace(decision.paired_differences[0], maximum=F(0))
    reject(lambda: ref.consume_response_decision(
        decision_request, replace(
            decision, paired_differences=(forged_difference,
                                          decision.paired_differences[1]))),
        "forged paired difference accepted")

    reject(lambda: ref.ResponseObservation(
        "bad-normalization", "population", CODING,
        (F(1, 4), F(1, 4), F(1, 4), F(1, 8))),
        "nonnormalized response observation accepted")
    reject(lambda: ref.AdjustmentObservation(
        "too-many-Z", "population", CODING, "pre-action-Z",
        tuple(f"z{i}" for i in range(5)), (F(1, 20),) * 20),
        "more than four covariate strata accepted")
    reject(lambda: ref.ResponseObservation(
        "float-observation", "population", CODING,
        (0.25, F(1, 4), F(1, 4), F(1, 4))),
        "floating input accepted")
    reject(lambda: ref.DecisionTable(
        "decimal-string-input", "loss", ("0.1", F(0)),
        ((F(0), F(0)), (F(0), F(0)))),
        "decimal string outside exact spelling profile accepted")
    reject(lambda: ref.ResponseFiberRequest(
        response_observation(), "profile",
        tuple(ref.MonotonicityRestriction(
            f"restriction-{i}", "nondecreasing") for i in range(7)),
        "query"), "restriction resource cap not enforced")
    huge = F(2**257)
    reject(lambda: ref.DecisionTable(
        "huge-input", "loss", (huge, F(0)),
        ((F(0), F(0)), (F(0), F(0)))),
        "256-bit input cap not enforced")
    record("B7_forged_claims_and_resource_limits",
           exact_rational_only=True, response_types=8,
           maximum_covariate_categories=4,
           maximum_restrictions=6, coefficient_bits=256)


def producer_disabled_receiving():
    adjustment_request = ref.AdjustmentRequest(
        simpson_observation(), PREMISES, 0, "disabled-adjustment-v1")
    adjustment_evidence = ref.produce_adjustment(adjustment_request)
    fiber_request = response_request()
    fiber_evidence = ref.produce_response_fiber(fiber_request)
    decision_request = ref.ResponseDecisionRequest(
        fiber_request, BAD_LOSS, "disabled-decision-v1")
    decision_evidence = ref.produce_response_decision(decision_request)
    saved = (ref.produce_adjustment, ref.produce_response_fiber,
             ref.produce_response_decision)

    def disabled(*_args, **_kwargs):
        raise RuntimeError("candidate producer disabled")

    ref.produce_adjustment = disabled
    ref.produce_response_fiber = disabled
    ref.produce_response_decision = disabled
    try:
        check(ref.consume_adjustment(
            adjustment_request, adjustment_evidence)["status"] == ref.ADJUSTED,
            "adjustment receiver called producer")
        check(ref.consume_response_fiber(
            fiber_request, fiber_evidence)["status"] == ref.PARTIAL,
            "fiber receiver called producer")
        check(ref.consume_response_decision(
            decision_request, decision_evidence)["status"] ==
              ref.MODEL_DEPENDENT,
              "decision receiver called producer")
    finally:
        (ref.produce_adjustment, ref.produce_response_fiber,
         ref.produce_response_decision) = saved
    record("B8_authoritative_receivers_with_producers_disabled",
           adjustment=True, response_fiber=True, decision=True)


def main():
    route_a_no_confounding()
    route_a_simpson_reversal()
    route_a_positivity_and_staleness()
    route_b_partial_and_independent_enumeration()
    route_b_supported_restrictions_and_point_id()
    route_b_decision_identified_despite_uncertainty()
    route_b_model_dependent_and_same_fiber_guard()
    route_b_incompatible_and_unsupported()
    stale_response_and_decision_evidence()
    forged_claims_and_malformed_inputs()
    producer_disabled_receiving()
    payload = {
        "status": "passed",
        "failed": 0,
        "optimized": sys.flags.optimize,
        "passed": len(results),
        "rejections": rejections,
        "results": ref.wire(results),
        "scope": ("bounded exact one-stage causal identification and decision "
                  "conformance checks; not formal verification or empirical validation"),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
