"""Fixed exact checks for the two-stage longitudinal causal bridge."""
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import platform
import sys
from pathlib import Path

import reference as r


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rejects(call):
    try:
        call()
    except r.Invalid:
        return
    raise RuntimeError("expected invalid claim was accepted")


CODING = r.LongitudinalCoding(
    r.BinaryVariable("A1"), r.BinaryVariable("L1"),
    r.BinaryVariable("A2"), r.BinaryVariable("Y"))
ORDER = r.TemporalOrder("A1-before-L1-before-A2-before-Y",
                        ("A1", "L1", "A2", "Y"))
PREMISES = r.SequentialCausalPremises(
    "two-stage-sequential-g-formula-premises-v1",
    "consistency-for-A1-A2-and-Y",
    "do-A1-and-adapted-do-A2-meaning",
    "A1-exchangeable-for-L1-and-downstream-counterfactuals",
    "A2-exchangeable-given-A1-L1",
    "A2-policy-measurable-only-in-A1-L1-history",
    "one-population-no-interference-profile")
BAD_OUTCOME_LOSS = r.LongitudinalLoss(
    "bad-outcome-loss-v1", "expected bad-outcome count",
    (0, 0), (0,) * 8,
    tuple(y for _a1, _l1, _a2, y in product((0, 1), repeat=4)))


def observation_from_factors(identity, p_a1_1, p_l1_1, p_a2_1, p_y_1,
                             *, population="trial-population-v1",
                             coding=CODING, order=ORDER):
    masses = []
    for a1, l1, a2, y in product((0, 1), repeat=4):
        p_a1 = p_a1_1 if a1 else 1 - p_a1_1
        p_l1 = p_l1_1[a1] if l1 else 1 - p_l1_1[a1]
        p_a2 = p_a2_1[a1, l1] if a2 else 1 - p_a2_1[a1, l1]
        p_y = p_y_1[a1, l1, a2] if y else 1 - p_y_1[a1, l1, a2]
        masses.append(p_a1 * p_l1 * p_a2 * p_y)
    return r.LongitudinalObservation(identity, population, coding, order,
                                     tuple(masses))


def positive_observation():
    p_l1 = {0: F(1, 4), 1: F(3, 4)}
    p_a2 = {(a1, l1): (F(9, 10) if l1 == 0 else F(1, 10))
            for a1, l1 in product((0, 1), repeat=2)}
    risk = {}
    for a1 in (0, 1):
        risk[a1, 0, 0] = F(1, 10)
        risk[a1, 0, 1] = F(4, 5)
        risk[a1, 1, 0] = F(9, 10)
        risk[a1, 1, 1] = F(1, 5)
    return observation_from_factors("positive-16-cell-law-v1", F(1, 2),
                                    p_l1, p_a2, risk)


def policy(identity, first, actions=(0, 1, 0, 1)):
    return r.DynamicPolicy(identity, first, actions)


def policy_request(observation, chosen, loss=BAD_OUTCOME_LOSS,
                   query="dynamic-regime-distribution-and-value-v1"):
    return r.PolicyRequest(
        observation, PREMISES, loss, chosen, observation.population_identity,
        "policy-specific-and-full-subject-support-v1", query)


def bridge_request(observation, loss=BAD_OUTCOME_LOSS,
                   query="all-policy-causal-to-sequential-equivalence-v1"):
    return r.BridgeRequest(
        observation, PREMISES, loss, observation.population_identity,
        "identified-two-stage-bellman-subject-v1",
        "all-32-complete-history-policies-v1",
        "strong-all-structural-transitions-support-v1", query)


def counterexample_world(identity, reverse=False):
    p_l1 = {0: F(1, 2), 1: F(1, 2)}
    p_a2 = {(a1, l1): F(1, 2)
            for a1, l1 in product((0, 1), repeat=2)}
    risk = {}
    first = {(0, 0): F(0), (0, 1): F(1),
             (1, 0): F(1), (1, 1): F(0)}
    for a1, l1, a2 in product((0, 1), repeat=3):
        value = first[l1, a2]
        risk[a1, l1, a2] = 1 - value if reverse else value
    return observation_from_factors(identity, F(1, 2), p_l1, p_a2, risk)


def main():
    results = []
    rejections = 0

    def record(case, **values):
        results.append(dict(case=case, status="PASS", **values))

    def reject(call):
        nonlocal rejections
        rejects(call)
        rejections += 1

    observation = positive_observation()
    named = policy("named-dynamic-policy", 0)
    request = policy_request(observation, named)
    evidence = r.produce_policy(request)
    checked = r.consume_policy(request, evidence)
    require(checked["status"] == r.POLICY_IDENTIFIED and
            checked["distribution"] == (F(7, 8), F(1, 8)) and
            checked["value"] == F(1, 8) and
            checked["full_subject_status"] == r.FULL_SUBJECT,
            "positive dynamic g-formula fixture")
    root_one = policy_request(observation, policy("root-one-dynamic", 1))
    require(r.consume_policy(root_one, r.produce_policy(root_one))["value"] ==
            F(7, 40), "second root dynamic value")
    record("positive_policy_specific_g_formula",
           root0_distribution=checked["distribution"], root0_value=checked["value"],
           root1_value=F(7, 40), subject_support=checked["full_subject_status"])

    bridge = bridge_request(observation)
    bridge_evidence = r.produce_bridge(bridge)
    bridge_checked = r.consume_bridge(bridge, bridge_evidence)
    expected_minimizers = (
        "policy-a1-0-a2-0100", "policy-a1-0-a2-0101",
        "policy-a1-0-a2-0110", "policy-a1-0-a2-0111")
    require(bridge_checked["policies_checked"] == 32 and
            bridge_checked["nodes_checked"] == 21 and
            bridge_checked["minimum_value"] == F(1, 8) and
            bridge_checked["complete_minimizing_set"] == expected_minimizers and
            bridge_evidence.causal_minimizers ==
            bridge_evidence.sequential_minimizers == expected_minimizers,
            "complete causal/Bellman policy equivalence")
    require(len({row.policy for row in bridge_evidence.policy_rows}) == 32,
            "off-root policies were quotiented")
    record("full_subject_all_32_policies_and_minimizers",
           subject_status=bridge_checked["subject_status"],
           policies=32, nodes=21, minimum=F(1, 8),
           complete_minimizers=expected_minimizers)

    # Identical one-stage A2 intervention margins conceal opposite adaptive rules.
    world_one = counterexample_world("same-marginals-world-one")
    world_two = counterexample_world("same-marginals-world-two", reverse=True)
    margins_one = tuple(r.static_second_stage_distribution(world_one, action)
                        for action in (0, 1))
    margins_two = tuple(r.static_second_stage_distribution(world_two, action)
                        for action in (0, 1))
    require(margins_one == margins_two == ((F(1, 2), F(1, 2)),) * 2,
            "one-stage intervention margins must agree exactly")
    match = policy("a2-equals-l1", 0, (0, 1, 0, 1))
    opposite = policy("a2-opposite-l1", 0, (1, 0, 1, 0))
    w1_match = r.consume_policy(policy_request(world_one, match),
                                r.produce_policy(policy_request(world_one, match)))
    w1_opposite = r.consume_policy(policy_request(world_one, opposite),
                                   r.produce_policy(policy_request(world_one, opposite)))
    w2_match = r.consume_policy(policy_request(world_two, match),
                                r.produce_policy(policy_request(world_two, match)))
    w2_opposite = r.consume_policy(policy_request(world_two, opposite),
                                   r.produce_policy(policy_request(world_two, opposite)))
    require((w1_match["value"], w1_opposite["value"],
             w2_match["value"], w2_opposite["value"]) ==
            (F(0), F(1), F(1), F(0)),
            "opposite adaptive-policy optima counterexample")
    w1_bridge = r.consume_bridge(bridge_request(world_one),
                                 r.produce_bridge(bridge_request(world_one)))
    w2_bridge = r.consume_bridge(bridge_request(world_two),
                                 r.produce_bridge(bridge_request(world_two)))
    require(set(w1_bridge["complete_minimizing_set"]).isdisjoint(
            w2_bridge["complete_minimizing_set"]),
            "counterexample needs opposite complete minimizing sets")
    record("one_stage_marginals_do_not_identify_adaptive_policy",
           static_do_A2_bad=(F(1, 2), F(1, 2)),
           world1_values=(F(0), F(1)), world2_values=(F(1), F(0)),
           opposite_minimizing_sets=True)

    # Policy support can hold where the complete subject support does not.
    p_l1 = {0: F(1, 2), 1: F(1, 2)}
    p_a2 = {(a1, l1): F(1, 2)
            for a1, l1 in product((0, 1), repeat=2)}
    p_a2[0, 0] = F(0)
    risk = {(a1, l1, a2): F(1, 4 + a2)
            for a1, l1, a2 in product((0, 1), repeat=3)}
    policy_only_law = observation_from_factors(
        "policy-only-support-law", F(1, 2), p_l1, p_a2, risk)
    supported = policy("supported-policy", 0, (0, 0, 0, 0))
    supported_request = policy_request(policy_only_law, supported)
    supported_result = r.consume_policy(
        supported_request, r.produce_policy(supported_request))
    require(supported_result["status"] == r.POLICY_IDENTIFIED and
            supported_result["full_subject_status"] == r.POLICY_ONLY,
            "policy/full-subject support distinction")
    refused = r.consume_bridge(bridge_request(policy_only_law),
                               r.produce_bridge(bridge_request(policy_only_law)))
    require(refused["status"] == r.POLICY_ONLY,
            "full subject must refuse a missing alternative transition")
    unsupported = policy_request(
        policy_only_law, policy("unsupported-selected-action", 0, (1, 0, 0, 0)))
    unsupported_result = r.consume_policy(unsupported,
                                          r.produce_policy(unsupported))
    require(unsupported_result["status"] == r.SECOND_STAGE_FAILURE and
            unsupported_result["missing_histories"] == ((0, 0, 1),),
            "reachable second-stage positivity failure")
    record("policy_specific_support_is_weaker_than_full_subject_support",
           identified_policy=supported_result["status"],
           full_subject=refused["status"],
           unsupported_policy=unsupported_result["status"])

    # First-stage support and a zero-probability intermediate branch are distinct.
    first_law = observation_from_factors(
        "first-stage-failure-law", F(0), p_l1,
        {(a1, l1): F(1, 2) for a1, l1 in product((0, 1), repeat=2)}, risk)
    first_fail_request = policy_request(first_law, policy("root-one-no-support", 1))
    first_fail = r.consume_policy(first_fail_request,
                                  r.produce_policy(first_fail_request))
    first_ok_request = policy_request(first_law, policy("root-zero-supported", 0,
                                                        (0, 0, 0, 0)))
    first_ok = r.consume_policy(first_ok_request, r.produce_policy(first_ok_request))
    require(first_fail["status"] == r.FIRST_STAGE_FAILURE and
            first_ok["status"] == r.POLICY_IDENTIFIED,
            "first-stage policy-specific positivity")
    zero_l = {0: F(0), 1: F(1, 2)}
    zero_branch_law = observation_from_factors(
        "zero-intermediate-branch-law", F(1, 2), zero_l,
        {(a1, l1): (F(0) if (a1, l1) == (0, 1) else F(1, 2))
         for a1, l1 in product((0, 1), repeat=2)}, risk)
    zero_branch_policy = policy("zero-branch-needs-no-action-support", 0,
                                (0, 1, 0, 0))
    zero_request = policy_request(zero_branch_law, zero_branch_policy)
    zero_result = r.consume_policy(zero_request, r.produce_policy(zero_request))
    require(zero_result["status"] == r.POLICY_IDENTIFIED and
            zero_result["full_subject_status"] == r.POLICY_ONLY,
            "zero-probability L1 branch should not require selected action support")
    record("first_stage_and_zero_intermediate_support_boundaries",
           root1=first_fail["status"], root0=first_ok["status"],
           zero_branch=zero_result["status"],
           zero_branch_full_subject=zero_result["full_subject_status"])

    signed_loss = r.LongitudinalLoss(
        "signed-loss-v1", "utility-adjusted loss units",
        (F(-1, 3), F(1, 7)),
        tuple(F((-1) ** (a1 + l1 + a2), 10)
              for a1, l1, a2 in product((0, 1), repeat=3)),
        tuple(F(-1, 2) if y == 0 else F(3, 2)
              for _a1, _l1, _a2, y in product((0, 1), repeat=4)))
    signed_bridge = bridge_request(observation, signed_loss,
                                   "signed-causal-sequential-equivalence-v1")
    signed_checked = r.consume_bridge(signed_bridge,
                                      r.produce_bridge(signed_bridge))
    require(signed_checked["policies_checked"] == 32 and
            type(signed_checked["minimum_value"]) is F,
            "signed exact costs must remain supported")
    record("signed_costs_and_losses", minimum=signed_checked["minimum_value"])

    # Complete policy shape and exact input discipline fail closed.
    reject(lambda: r.DynamicPolicy("incomplete", 0, (0, 1)))
    reject(lambda: r.DynamicPolicy("boolean-action", True, (0, 1, 0, 1)))
    reject(lambda: r.LongitudinalObservation(
        "float-law", "trial-population-v1", CODING, ORDER,
        (0.0,) + observation.masses[1:]))
    reject(lambda: r.LongitudinalObservation(
        "wrong-order", "trial-population-v1", CODING,
        r.TemporalOrder("wrong-order-id", ("A1", "A2", "L1", "Y")),
        observation.masses))
    reject(lambda: r.PolicyRequest(
        observation, PREMISES, BAD_OUTCOME_LOSS, named,
        "another-population", "support", "query"))
    record("malformed_policy_exactness_temporal_and_transport_controls",
           rejected=5)

    # Every decision-relevant input is part of the receiver's subject binding.
    stale_requests = []
    masses = list(observation.masses)
    masses[0], masses[1] = masses[1], masses[0]
    stale_requests.append(replace(request, observation=replace(
        observation, masses=tuple(masses))))
    stale_requests.append(replace(request, observation=replace(
        observation, population_identity="trial-population-v2"),
        deployment_population_identity="trial-population-v2"))
    changed_y = r.BinaryVariable("Y-v2")
    changed_coding = replace(CODING, outcome=changed_y)
    stale_requests.append(replace(request, observation=replace(
        observation, coding=changed_coding,
        temporal_order=r.TemporalOrder("changed-coding-order",
                                       ("A1", "L1", "A2", "Y-v2")))))
    stale_requests.append(replace(request, observation=replace(
        observation, temporal_order=replace(ORDER, identity="order-v2"))))
    stale_requests.append(replace(request, premises=replace(
        PREMISES, first_stage_exchangeability_identity="first-exchange-v2")))
    stale_requests.append(replace(request, premises=replace(
        PREMISES, second_stage_exchangeability_identity="second-exchange-v2")))
    stale_requests.append(replace(request, premises=replace(
        PREMISES, consistency_identity="consistency-v2")))
    stale_requests.append(replace(request, premises=replace(
        PREMISES, intervention_identity="intervention-v2")))
    stale_requests.append(replace(request, premises=replace(
        PREMISES, adapted_policy_identity="adapted-v2")))
    stale_requests.append(replace(request, premises=replace(
        PREMISES, no_interference_identity="interference-v2")))
    stale_requests.append(replace(request, policy=policy(
        "changed-policy", 0, (0, 0, 0, 0))))
    stale_requests.append(replace(request, loss=replace(
        BAD_OUTCOME_LOSS, first_stage_costs=(1, 0))))
    changed_terminal = list(BAD_OUTCOME_LOSS.terminal_losses)
    changed_terminal[0] = F(-1)
    stale_requests.append(replace(request, loss=replace(
        BAD_OUTCOME_LOSS, terminal_losses=tuple(changed_terminal))))
    stale_requests.append(replace(request, support_query_identity="support-v2"))
    stale_requests.append(replace(request, query_identity="query-v2"))
    for stale in stale_requests:
        reject(lambda stale=stale: r.consume_policy(stale, evidence))
    record("stale_policy_evidence_binding",
           observation_population_coding_order_premises_policy_loss_queries=len(stale_requests))

    bridge_stale = (
        replace(bridge, subject_identity="subject-v2"),
        replace(bridge, policy_catalogue_identity="catalogue-v2"),
        replace(bridge, support_query_identity="support-v2"),
        replace(bridge, query_identity="bridge-query-v2"),
    )
    for stale in bridge_stale:
        reject(lambda stale=stale: r.consume_bridge(stale, bridge_evidence))
    forged_subject = replace(bridge_evidence.subject, name="forged-subject")
    reject(lambda: r.consume_bridge(
        bridge, replace(bridge_evidence, subject=forged_subject)))
    forged_rows = list(bridge_evidence.policy_rows)
    forged_rows[0] = replace(forged_rows[0], distribution=(F(1), F(0)))
    reject(lambda: r.consume_bridge(
        bridge, replace(bridge_evidence, policy_rows=tuple(forged_rows))))
    forged_rows = list(bridge_evidence.policy_rows)
    forged_rows[0] = replace(forged_rows[0], causal_value=F(999))
    reject(lambda: r.consume_bridge(
        bridge, replace(bridge_evidence, policy_rows=tuple(forged_rows))))
    forged_rows = list(bridge_evidence.policy_rows)
    cert = forged_rows[0].sequential_certificate
    forged_rows[0] = replace(
        forged_rows[0], sequential_certificate=replace(
            cert, upper=(cert.upper[0] + 1,) + cert.upper[1:]))
    reject(lambda: r.consume_bridge(
        bridge, replace(bridge_evidence, policy_rows=tuple(forged_rows))))
    reject(lambda: r.consume_policy(
        request, replace(evidence, distribution=(F(1), F(0)))))
    reject(lambda: r.consume_policy(request, replace(evidence, value=F(999))))
    reject(lambda: r.consume_policy(
        request, replace(evidence, status=r.SECOND_STAGE_FAILURE,
                         distribution=(), value=None, stratum_terms=(),
                         missing_histories=((0, 0, 0),),
                         full_subject_status=None)))
    record("stale_bridge_and_forged_claims_reject",
           bridge_revisions=4, forged_subject_distribution_value_certificate=True)

    # Retained evidence must remain consumable with every producer disabled.
    saved_policy = r.produce_policy
    saved_bridge = r.produce_bridge
    saved_sequential = r.sequential.produce

    def disabled(*_args, **_kwargs):
        raise RuntimeError("producer disabled")

    r.produce_policy = disabled
    r.produce_bridge = disabled
    r.sequential.produce = disabled
    r.consume_policy(request, evidence)
    producer_disabled = r.consume_bridge(bridge, bridge_evidence)
    require(producer_disabled["policies_checked"] == 32,
            "receiver called a disabled producer")
    r.produce_policy = saved_policy
    r.produce_bridge = saved_bridge
    r.sequential.produce = saved_sequential
    record("producer_disabled_receiving", policies=32)

    sources = {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
               for name in ("reference.py", "checks.py")}
    output = {
        "python": platform.python_version(),
        "optimized": sys.flags.optimize,
        "passed": len(results),
        "failed": 0,
        "rejections": rejections,
        "results": r.wire(results),
        "source_sha256": sources,
    }
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
