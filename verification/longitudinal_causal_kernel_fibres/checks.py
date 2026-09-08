"""Adversarial exact checks for longitudinal causal kernel fibres."""
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import platform
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from verification.longitudinal_causal_kernel_fibres import reference as r  # noqa: E402


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rejects(call):
    try:
        call()
    except r.Invalid:
        return
    raise RuntimeError("expected invalid claim was accepted")


CODING = r.longitudinal.LongitudinalCoding(
    r.longitudinal.BinaryVariable("A1"),
    r.longitudinal.BinaryVariable("L1"),
    r.longitudinal.BinaryVariable("A2"),
    r.longitudinal.BinaryVariable("Y"))
ORDER = r.longitudinal.TemporalOrder(
    "A1-before-L1-before-A2-before-Y", ("A1", "L1", "A2", "Y"))
PREMISES = r.longitudinal.SequentialCausalPremises(
    "two-stage-sequential-g-formula-premises-v1",
    "consistency-for-A1-A2-and-Y",
    "do-A1-and-adapted-do-A2-meaning",
    "A1-exchangeable-for-L1-and-downstream-counterfactuals",
    "A2-exchangeable-given-A1-L1",
    "A2-policy-measurable-only-in-A1-L1-history",
    "one-population-no-interference-profile")
BAD_OUTCOME_LOSS = r.longitudinal.LongitudinalLoss(
    "bad-outcome-loss-v1", "expected bad-outcome count",
    (0, 0), (0,) * 8,
    tuple(y for _a, _l, _b, y in product((0, 1), repeat=4)))
ONE_GAP_LOSS = replace(BAD_OUTCOME_LOSS,
                       identity="one-gap-dominated-root-loss-v1",
                       first_stage_costs=(0, 2))
PROFILE = r.CompletionProfile("saturated-longitudinal-kernel-profile-v1")


def observation_from_factors(identity, p_a1_1, p_l1_1, p_a2_1, p_y_1,
                             *, population="trial-population-v1"):
    masses = []
    for a, l, b, y in product((0, 1), repeat=4):
        pa = p_a1_1 if a else 1 - p_a1_1
        pl = p_l1_1[a] if l else 1 - p_l1_1[a]
        pb = p_a2_1[a, l] if b else 1 - p_a2_1[a, l]
        py = p_y_1[a, l, b] if y else 1 - p_y_1[a, l, b]
        masses.append(pa * pl * pb * py)
    return r.longitudinal.LongitudinalObservation(
        identity, population, CODING, ORDER, tuple(masses))


def positive_observation():
    p_l = {0: F(1, 4), 1: F(3, 4)}
    p_a2 = {(a, l): (F(9, 10) if l == 0 else F(1, 10))
            for a, l in product((0, 1), repeat=2)}
    risk = {}
    for a in (0, 1):
        risk[a, 0, 0] = F(1, 10)
        risk[a, 0, 1] = F(4, 5)
        risk[a, 1, 0] = F(9, 10)
        risk[a, 1, 1] = F(1, 5)
    return observation_from_factors(
        "positive-16-cell-law-v1", F(1, 2), p_l, p_a2, risk)


def one_gap_observation(identity="one-gap-law-v1"):
    p_l = {0: F(1, 2), 1: F(1, 2)}
    p_a2 = {(a, l): F(1, 2)
            for a, l in product((0, 1), repeat=2)}
    p_a2[0, 0] = F(0)
    risk = {(a, l, b): F(1, 2)
            for a, l, b in product((0, 1), repeat=3)}
    risk[0, 0, 0] = F(1, 2)
    risk[0, 1, 0] = F(0)
    risk[0, 1, 1] = F(1)
    return observation_from_factors(identity, F(1, 2), p_l, p_a2, risk)


def two_gap_observation():
    p_l = {0: F(1, 2), 1: F(1, 2)}
    p_a2 = {(a, l): F(1, 2)
            for a, l in product((0, 1), repeat=2)}
    p_a2[0, 0] = p_a2[0, 1] = F(0)
    risk = {(a, l, b): F(1, 2)
            for a, l, b in product((0, 1), repeat=3)}
    risk[0, 0, 0] = risk[0, 1, 0] = F(1, 2)
    return observation_from_factors(
        "two-gap-law-v1", F(1, 2), p_l, p_a2, risk)


def gap_count_observation(count):
    need_rows = ((0, 0), (0, 1), (1, 0), (1, 1))[:count]
    p_l = {0: F(1, 2), 1: F(1, 2)}
    p_a2 = {(a, l): (F(0) if (a, l) in need_rows else F(1, 2))
            for a, l in product((0, 1), repeat=2)}
    risk = {(a, l, b): F(a + l + b + 1, 5)
            for a, l, b in product((0, 1), repeat=3)}
    return observation_from_factors(
        f"{count}-gap-law-v1", F(1, 2), p_l, p_a2, risk)


def request(observation, *, loss=BAD_OUTCOME_LOSS, profile=PROFILE,
            query="longitudinal-causal-kernel-fibre-query-v1",
            query_class=r.QUERY_CLASS, rows=None,
            policies=None):
    return r.FibreRequest(
        observation, PREMISES, loss, observation.population_identity, profile,
        r.derive_missing_rows(observation) if rows is None else rows,
        r.longitudinal.complete_policies() if policies is None else policies,
        "identified-two-stage-bellman-subject-v1",
        "all-32-complete-history-policies-v1",
        "second-stage-missing-outcome-row-support-v1",
        "exact-saturated-longitudinal-kernel-fibre-v1",
        "causal-kernel-corner-family-v1", query, query_class)


def policy_result(evidence, identity):
    return next(row for row in evidence.policy_results
                if row.policy.identity == identity)


def named_policy(first, actions):
    return next(policy for policy in r.longitudinal.complete_policies()
                if policy.first_action == first and
                policy.second_actions == tuple(actions))


def main():
    results = []
    rejections = 0

    def record(case, **values):
        results.append(dict(case=case, status="PASS", **values))

    def reject(call):
        nonlocal rejections
        rejects(call)
        rejections += 1

    # k=0 is not a lookalike: it is the exact preceding PR20 subject/result.
    zero_request = request(positive_observation())
    zero_evidence = r.produce(zero_request)
    zero = r.consume(zero_request, zero_evidence)
    expected_pr20 = (
        "policy-a1-0-a2-0100", "policy-a1-0-a2-0101",
        "policy-a1-0-a2-0110", "policy-a1-0-a2-0111")
    require(zero["dimension"] == 0 and zero["corners_checked"] == 1 and
            zero["common_minimizers"] == expected_pr20 and
            zero["minimax_loss_winners"] == expected_pr20 and
            zero_evidence.corner_family.members[0].subject ==
            zero_evidence.pr20_bridge.subject and
            zero_evidence.corner_family.equals_continuous_fibre is True and
            tuple(row.expected_loss.lower for row in zero_evidence.policy_results) ==
            tuple(row.causal_value for row in zero_evidence.pr20_bridge.policy_rows),
            "zero-gap fibre must collapse exactly to PR20")
    record("zero_gap_exact_pr20_collapse", dimension=0, corners=1,
           policies=32, minimizing_set=expected_pr20,
           subject_byte_identity=True)

    # Mandatory one-gap example: policy S is constant 1/4, U is q/2.
    one_request = request(one_gap_observation(), loss=ONE_GAP_LOSS)
    one_evidence = r.produce(one_request)
    one = r.consume(one_request, one_evidence)
    safe = named_policy(0, (0, 0, 0, 0))
    uncertain = named_policy(0, (1, 0, 0, 0))
    safe_result = policy_result(one_evidence, safe.identity)
    uncertain_result = policy_result(one_evidence, uncertain.identity)
    require((safe_result.expected_loss.lower, safe_result.expected_loss.upper,
             uncertain_result.expected_loss.lower,
             uncertain_result.expected_loss.upper) ==
            (F(1, 4), F(1, 4), F(0), F(1, 2)) and
            safe_result.status == r.POINT_POLICY and
            uncertain_result.status == r.PARTIAL_POLICY and
            one["decision_status"] == r.DECISION_MODEL_DEPENDENT and
            not one["common_minimizers"] and
            safe.identity in one["minimax_loss_winners"],
            "mandatory one-gap policy and decision fibre")
    q0, q1 = one_evidence.decision.corner_decisions
    require(uncertain.identity in q0.minimizers and
            safe.identity in q1.minimizers and
            set(q0.minimizers).isdisjoint(q1.minimizers),
            "opposite completion-specific optima required")
    robust_u = dict(one_evidence.robust.same_model_worst_regrets)[uncertain.identity]
    invalid_cross_shortcut = uncertain_result.expected_loss.upper - \
        min(row.minimum_loss for row in one_evidence.decision.corner_decisions)
    require(robust_u == F(1, 4) and invalid_cross_shortcut == F(1, 2),
            "same-completion regret must differ from cross-completion shortcut")
    reject(lambda: r.same_model_regret(
        q0.corner_identity, q1.corner_identity, F(1, 2), F(0)))
    record("one_gap_partial_policy_model_dependent_decision_and_regret",
           S_interval=(F(1, 4), F(1, 4)), U_interval=(F(0), F(1, 2)),
           common_minimizers=0, U_same_model_worst_regret=robust_u,
           rejected_cross_model_shortcut=invalid_cross_shortcut)

    # Uncertainty remains real while a changed cost makes the decision common.
    second_costs = [F(0)] * 8
    second_costs[1] = F(1)
    decision_loss = replace(ONE_GAP_LOSS,
                            identity="missing-action-cost-loss-v1",
                            second_stage_costs=tuple(second_costs))
    identified_request = request(one_gap_observation(), loss=decision_loss,
                                 query="decision-identified-with-live-fibre-v1")
    identified_evidence = r.produce(identified_request)
    identified = r.consume(identified_request, identified_evidence)
    identified_uncertain = policy_result(identified_evidence, uncertain.identity)
    require(identified["dimension"] == 1 and
            identified_uncertain.status == r.PARTIAL_POLICY and
            identified_uncertain.expected_loss.lower == F(1, 2) and
            identified_uncertain.expected_loss.upper == F(1) and
            identified["decision_status"] == r.DECISION_IDENTIFIED and
            safe.identity in identified["common_minimizers"],
            "decision may identify although a policy remains partial")
    record("decision_identified_despite_nontrivial_fibre",
           dimension=1, partial_policy_interval=(F(1, 2), F(1)),
           common_minimizers=identified["common_minimizers"])

    # Two independent missing rows: exact rectangle corners and interior audit.
    two_request = request(two_gap_observation(), loss=ONE_GAP_LOSS)
    two_evidence = r.produce(two_request)
    two = r.consume(two_request, two_evidence)
    selects_both = named_policy(0, (1, 1, 0, 0))
    both_result = policy_result(two_evidence, selects_both.identity)
    corner_values = tuple(
        cell.expected_loss for cell in two_evidence.cells
        if cell.policy_identity == selects_both.identity)
    interior_distribution, interior_value = r.policy_at_completion(
        two_request, selects_both, (F(1, 3), F(2, 5)))
    require(corner_values == (F(0), F(1, 2), F(1, 2), F(1)) and
            interior_value == interior_distribution[1] == F(11, 30) and
            (both_result.expected_loss.lower,
             both_result.expected_loss.upper) == (F(0), F(1)) and
            two["persistent_composition"] == r.PERSISTENT_REUSED,
            "two-gap multi-affine corner and interior audit")
    require(two_evidence.corner_family.equals_continuous_fibre is False,
            "positive-dimensional corner family cannot equal the fibre")
    record("two_gap_continuous_rectangle_exact_query_corners",
           dimension=2, corners=4,
           corner_values=corner_values, interior_point=(F(1, 3), F(2, 5)),
           interior_value=interior_value,
           finite_corners_equal_fibre=False)

    # Corner reduction is query-specific: the nonlinear g(q)=q(1-q) is zero
    # at both corners and 1/4 at the interior midpoint.
    nonlinear_corner_values = tuple(q * (1 - q) for q in (F(0), F(1)))
    nonlinear_interior = F(1, 2) * (1 - F(1, 2))
    require(nonlinear_corner_values == (F(0), F(0)) and
            nonlinear_interior == F(1, 4),
            "nonlinear corner insufficiency control")
    record("finite_corners_not_valid_for_arbitrary_nonlinear_queries",
           corner_values=nonlinear_corner_values,
           midpoint_value=nonlinear_interior)

    # The entire bounded dimension 0..4 is supported; 8/16 corners expose,
    # rather than mutate, the frozen four-model persistent checker limit.
    counts = []
    for k in range(1, 5):
        bounded_request = request(gap_count_observation(k),
                                  query=f"bounded-{k}-gap-query-v1")
        bounded_evidence = r.produce(bounded_request)
        bounded = r.consume(bounded_request, bounded_evidence)
        expected_persistent = (r.PERSISTENT_REUSED if k <= 2
                               else r.PERSISTENT_LOCAL)
        require((bounded["dimension"], bounded["corners_checked"],
                 bounded["cells_checked"], bounded["persistent_composition"]) ==
                (k, 2 ** k, 32 * 2 ** k, expected_persistent),
                f"bounded k={k} profile")
        counts.append((k, 2 ** k, 32 * 2 ** k, expected_persistent))
    record("all_bounded_dimensions_and_persistent_limit", counts=counts,
           existing_family_limit=r.families.MAX_MODELS,
           max_reference_cells=512)

    # Earlier-stage gaps are outside this construction, not incompatibility.
    p_l = {0: F(1, 2), 1: F(1, 2)}
    p_a2 = {(a, l): F(1, 2)
            for a, l in product((0, 1), repeat=2)}
    risk = {(a, l, b): F(1, 2)
            for a, l, b in product((0, 1), repeat=3)}
    first_gap = observation_from_factors(
        "first-stage-gap-law", F(0), p_l, p_a2, risk)
    first_boundary = r.consume(request(first_gap), r.produce(request(first_gap)))
    intermediate_gap = observation_from_factors(
        "intermediate-gap-law", F(1, 2), {0: F(0), 1: F(1, 2)},
        p_a2, risk)
    intermediate_boundary = r.consume(
        request(intermediate_gap), r.produce(request(intermediate_gap)))
    narrower_policy = r.longitudinal.DynamicPolicy(
        "narrower-supported-policy", 0, (0, 1, 0, 0))
    narrower_request = r.longitudinal.PolicyRequest(
        intermediate_gap, PREMISES, BAD_OUTCOME_LOSS, narrower_policy,
        intermediate_gap.population_identity, "policy-support", "policy-query")
    narrower = r.longitudinal.consume_policy(
        narrower_request, r.longitudinal.produce_policy(narrower_request))
    require(first_boundary["status"] == intermediate_boundary["status"] ==
            r.OUTSIDE_PROFILE and
            narrower["status"] == r.longitudinal.POLICY_IDENTIFIED,
            "earlier support boundary must preserve narrower prior result")
    record("earlier_stage_gaps_outside_profile_not_impossible",
           first_stage=first_boundary["status"],
           intermediate=intermediate_boundary["status"],
           narrower_pr20_policy=narrower["status"])

    # Stronger restrictions and arbitrary nonlinear queries are not dropped.
    stronger_profile = r.CompletionProfile(
        "monotone-profile-request", r.SATURATED_PROFILE,
        ("monotonicity-across-second-stage-actions",))
    stronger_request = request(one_gap_observation(), profile=stronger_profile,
                               query="stronger-cross-row-query")
    stronger = r.consume(stronger_request, r.produce(stronger_request))
    nonlinear_request = request(
        one_gap_observation(), query="nonlinear-fibre-shape-query",
        query_class="arbitrary-nonlinear-functional")
    nonlinear = r.consume(nonlinear_request, r.produce(nonlinear_request))
    require(stronger["status"] == r.UNSUPPORTED_RESTRICTION and
            nonlinear["status"] == r.UNSUPPORTED_QUERY,
            "unsupported assumptions and queries require explicit status")
    record("stronger_scm_restriction_and_nonlinear_query_refuse",
           restriction_status=stronger["status"],
           query_status=nonlinear["status"])

    # Exact input/map/policy shape and hidden completion-indexed policies fail.
    row = r.derive_missing_rows(one_request.observation)[0]
    reject(lambda: r.FibreRequest(
        one_request.observation, PREMISES, BAD_OUTCOME_LOSS,
        one_request.deployment_population_identity, PROFILE, (row, row),
        one_request.policies, one_request.subject_identity,
        one_request.policy_catalogue_identity, one_request.support_query_identity,
        one_request.fibre_identity, one_request.corner_family_identity,
        one_request.query_identity))
    reject(lambda: r.produce(request(one_request.observation, rows=())))
    renamed = replace(row, identity=row.identity + ":renamed")
    reject(lambda: r.produce(request(one_request.observation, rows=(renamed,))))
    reverse_policies = tuple(reversed(one_request.policies))
    reject(lambda: request(one_request.observation, policies=reverse_policies))
    changed_policies = (replace(one_request.policies[0],
                                identity="changed-policy"),) + \
        one_request.policies[1:]
    reject(lambda: request(one_request.observation, policies=changed_policies))
    reject(lambda: request(one_request.observation,
                           policies=tuple({"corner": policy}
                                          for policy in one_request.policies)))
    reject(lambda: r.policy_at_completion(
        one_request, uncertain, (F(1, 2), F(1, 2))))
    record("missing_row_map_catalogue_and_hidden_policy_controls",
           duplicate_missing=True, omitted_missing=True, renamed_missing=True,
           reordered_catalogue=True, changed_policy=True,
           model_indexed_policy_vector=True,
           extra_assignment=True)

    # Every decision-relevant request component is bound before recomputation.
    stale_requests = []
    obs = one_request.observation
    masses = list(obs.masses)
    masses[4], masses[5] = masses[5], masses[4]
    stale_requests.append(replace(one_request,
                                  observation=replace(obs, masses=tuple(masses))))
    support_masses = list(obs.masses)
    support_masses[0:4] = (F(1, 16), F(1, 16), F(1, 16), F(1, 16))
    stale_requests.append(replace(
        one_request, observation=replace(obs, masses=tuple(support_masses))))
    stale_requests.append(replace(
        one_request,
        observation=replace(obs, population_identity="trial-population-v2"),
        deployment_population_identity="trial-population-v2"))
    changed_coding = replace(CODING,
                             outcome=r.longitudinal.BinaryVariable("Y-v2"))
    stale_requests.append(replace(
        one_request,
        observation=replace(
            obs, coding=changed_coding,
            temporal_order=r.longitudinal.TemporalOrder(
                "changed-order", ("A1", "L1", "A2", "Y-v2")))))
    stale_requests.append(replace(
        one_request,
        observation=replace(obs, temporal_order=replace(
            ORDER, identity="temporal-order-v2"))))
    stale_requests.append(replace(one_request, premises=replace(
        PREMISES, second_stage_exchangeability_identity="second-stage-v2")))
    stale_requests.append(replace(one_request, completion_profile=replace(
        PROFILE, identity="profile-v2")))
    stale_requests.append(replace(one_request, loss=replace(
        BAD_OUTCOME_LOSS, first_stage_costs=(1, 0))))
    stale_requests.append(replace(one_request, subject_identity="subject-v2"))
    stale_requests.append(replace(one_request,
                                  policy_catalogue_identity="catalogue-v2"))
    stale_requests.append(replace(one_request,
                                  support_query_identity="support-v2"))
    stale_requests.append(replace(one_request, fibre_identity="fibre-v2"))
    stale_requests.append(replace(one_request,
                                  corner_family_identity="corners-v2"))
    stale_requests.append(replace(one_request, query_identity="query-v2"))
    stale_requests.append(replace(
        two_request, missing_rows=tuple(reversed(two_request.missing_rows))))
    for stale in stale_requests:
        retained = two_evidence if stale.observation == two_request.observation else one_evidence
        reject(lambda stale=stale, retained=retained: r.consume(stale, retained))
    record("stale_observation_premises_profile_loss_and_identity_binding",
           rejected=len(stale_requests), changed_support_pattern=True,
           changed_missing_row_order=True)

    # Forged support/corners/transitions/cells/intervals/decision/robust claims.
    forged_member = one_evidence.corner_family.members[0]
    forged_assignment = replace(forged_member.assignment,
                                identity=forged_member.assignment.identity + ":forged")
    forged_family = replace(
        one_evidence.corner_family,
        members=(replace(forged_member, assignment=forged_assignment),) +
        one_evidence.corner_family.members[1:])
    reject(lambda: r.consume(one_request,
                             replace(one_evidence, corner_family=forged_family)))
    omitted_family = replace(
        one_evidence.corner_family,
        members=one_evidence.corner_family.members[:1])
    reject(lambda: r.consume(one_request,
                             replace(one_evidence,
                                     corner_family=omitted_family)))
    supported_member = one_evidence.corner_family.members[0]
    supported_subject = supported_member.subject
    supported_node = supported_subject.nodes[1]
    supported_action = replace(
        supported_node.actions[0],
        outcomes=(("Y=0", F(1, 4)), ("Y=1", F(3, 4))))
    changed_node = replace(
        supported_node,
        actions=(supported_action,) + supported_node.actions[1:])
    changed_subject = replace(
        supported_subject,
        nodes=(supported_subject.nodes[0], changed_node) +
        supported_subject.nodes[2:])
    changed_member = replace(supported_member, subject=changed_subject)
    changed_family = replace(
        one_evidence.corner_family,
        members=(changed_member,) + one_evidence.corner_family.members[1:])
    reject(lambda: r.consume(one_request, replace(
        one_evidence, corner_family=changed_family)))
    forged_parameter = object.__new__(r.ParameterInterval)
    object.__setattr__(forged_parameter, "row",
                       one_evidence.fibre.parameters[0].row)
    object.__setattr__(forged_parameter, "lower", F(0))
    object.__setattr__(forged_parameter, "upper", F(1, 2))
    forged_fibre = replace(one_evidence.fibre,
                           parameters=(forged_parameter,))
    reject(lambda: r.consume(one_request, replace(
        one_evidence, fibre=forged_fibre)))
    reject(lambda: r.consume(one_request,
                             replace(one_evidence,
                                     cells=one_evidence.cells[:-1])))
    cell = one_evidence.cells[0]
    forged_cells = (replace(cell, distribution=(F(0), F(1))),) + \
        one_evidence.cells[1:]
    reject(lambda: r.consume(one_request,
                             replace(one_evidence, cells=forged_cells)))
    cert = cell.certificate
    forged_cells = (replace(cell, certificate=replace(
        cert, upper=(cert.upper[0] + 1,) + cert.upper[1:])),) + \
        one_evidence.cells[1:]
    reject(lambda: r.consume(one_request,
                             replace(one_evidence, cells=forged_cells)))
    first_result = one_evidence.policy_results[0]
    forged_results = (replace(
        first_result, expected_loss=replace(first_result.expected_loss,
                                            upper=F(999))),) + \
        one_evidence.policy_results[1:]
    reject(lambda: r.consume(one_request, replace(
        one_evidence, policy_results=forged_results)))
    reject(lambda: r.consume(one_request, replace(
        one_evidence, decision=replace(one_evidence.decision,
                                       common_minimizers=(safe.identity,)))))
    robust = one_evidence.robust
    reject(lambda: r.consume(one_request, replace(
        one_evidence, robust=replace(robust,
                                     minimax_loss_winners=(uncertain.identity,)))))
    reject(lambda: replace(
        one_evidence.corner_family,
        members=(one_evidence.corner_family.members[0],) * 2))
    record("forged_corner_transition_certificate_interval_and_decision_reject",
           forged_controls=11)

    # Retained evidence remains checkable with every candidate producer off.
    saved = (r.produce, r.sequential.produce, r.families.choose,
             r.longitudinal.produce_bridge)

    def disabled(*_args, **_kwargs):
        raise RuntimeError("producer disabled")

    r.produce = disabled
    r.sequential.produce = disabled
    r.families.choose = disabled
    r.longitudinal.produce_bridge = disabled
    disabled_result = r.consume(two_request, two_evidence)
    zero_disabled = r.consume(zero_request, zero_evidence)
    require(disabled_result["cells_checked"] == 128 and
            zero_disabled["cells_checked"] == 32,
            "receiver called a disabled producer")
    (r.produce, r.sequential.produce, r.families.choose,
     r.longitudinal.produce_bridge) = saved
    record("producer_disabled_receiving",
           fibre_cells=128, pr20_collapse_cells=32,
           persistent_producer_disabled=True)

    sources = {
        name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
        for name in ("reference.py", "checks.py")
    }
    print(json.dumps({
        "python": platform.python_version(),
        "optimized": sys.flags.optimize,
        "passed": len(results),
        "failed": 0,
        "rejections": rejections,
        "results": r.wire(results),
        "source_sha256": sources,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
