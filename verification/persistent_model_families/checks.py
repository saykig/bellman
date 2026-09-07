"""Fixed persistent-family cases and a separate direct complete-path oracle."""
from dataclasses import replace
from fractions import Fraction as F
from itertools import product
import json
import sys

import families as f

r, a = f.r, f.a
rejections = 0


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def reject(fn, kind=r.Invalid):
    global rejections
    try:
        fn()
    except kind:
        rejections += 1
        return
    raise RuntimeError("invalid family claim accepted")


def direct_value(subject, policy, start=()):
    """Forward path sums; does not call any reference backup or producer."""
    nodes = {node.h: node for node in subject.nodes}
    chosen = dict(policy.choices)
    pending = [(start, F(1), F(0))]
    total = F(0)
    final_mass = F(0)
    while pending:
        history, mass, paid = pending.pop()
        node = nodes[history]
        if not node.actions:
            total += mass * (paid + node.terminal)
            final_mass += mass
            continue
        action = next(x for x in node.actions if x.label == chosen[history])
        if not action.outcomes:
            total += mass * (paid + action.cost)
            final_mass += mass
        else:
            for observation, probability in action.outcomes:
                if probability:
                    pending.append((history + ((action.label, observation),),
                                    mass * probability, paid + action.cost))
    need(final_mass == 1, "direct path mass")
    return total


def direct_policies(subject):
    nodes = [node for node in subject.nodes if node.actions]
    return tuple(r.Policy(tuple((node.h, label) for node, label in zip(nodes, labels)))
                 for labels in product(*(tuple(x.label for x in node.actions) for node in nodes)))


def one_step(name, costs, labels=("a", "b"), unit="loss"):
    return r.Subject(name, 1, unit, (), [
        r.Node((), actions=[r.Action(label, cost) for label, cost in zip(labels, costs)])
    ])


def policy(subject, labels):
    nodes = [node for node in subject.nodes if node.actions]
    return r.Policy(tuple((node.h, label) for node, label in zip(nodes, labels)))


def family(identity, *subjects):
    return f.Family(identity, [f.Member(f"m{i + 1}", subject)
                               for i, subject in enumerate(subjects)])


def exact_group(member, pi, source_identity="exact"):
    return f.ModelSources(member.identity,
                          [a.Source(source_identity, r.produce(member.subject, pi))])


def exact_named_request(fam, pi):
    return f.NamedPolicyRequest(fam, pi,
                                [exact_group(member, pi) for member in fam.members])


def catalogue(subject, names=None):
    policies = direct_policies(subject)
    if names is None:
        names = [f"p{i}" for i in range(len(policies))]
    return tuple(f.PolicyEntry(name, pi) for name, pi in zip(names, policies))


def run():
    results = []

    def record(name, **values):
        results.append(dict(case=name, status="PASS", **values))

    # F1: subtraction occurs before the maximum over persistent models.
    f1a = one_step("F1 low", (2, 0))
    f1b = one_step("F1 high", (100, 100))
    fam1 = family("F1 family", f1a, f1b)
    pa = policy(f1a, ("a",))
    q1 = exact_named_request(fam1, pa)
    e1 = f.bound_named_policy(q1)
    x1 = f.consume_named_policy(q1, e1)
    need(x1["modelwise"] == (("m1", F(0), F(2), F(2)),
                              ("m2", F(100), F(100), F(0))), "F1 pairs")
    need(x1["worst_policy_upper"] == 100 and x1["worst_regret_upper"] == 2,
         "F1 aggregate")
    false_subtraction = max(F(2), F(100)) - max(F(0), F(100))
    need(false_subtraction == 0, "F1 false cross-model subtraction")
    reject(lambda: f.consume_named_policy(q1, replace(e1, worst_regret_upper=F(0))))
    record("F1_pair_before_aggregation", actual_worst_regret=2,
           rejected_cross_model_bound=false_subtraction)

    # F2: minimum worst loss and minimum worst regret select different actions.
    f2a = one_step("F2 A", (0, 2))
    f2b = one_step("F2 B", (10, 9))
    fam2 = family("F2 family", f2a, f2b)
    entries2 = catalogue(f2a, ("a", "b"))
    loss_request = f.ChoiceRequest(fam2, entries2, f.FULL, f.MINIMAX_LOSS)
    regret_request = f.ChoiceRequest(fam2, entries2, f.FULL, f.MINIMAX_REGRET)
    loss_evidence = f.choose(loss_request)
    regret_evidence = f.choose(regret_request)
    loss_answer = f.consume_choice(loss_request, loss_evidence)
    regret_answer = f.consume_choice(regret_request, regret_evidence)
    need(loss_answer["matrix"] == ((F(0), F(2)), (F(10), F(9))), "F2 matrix")
    need(loss_answer["worst_costs"] == (F(10), F(9)) and
         regret_answer["worst_regrets"] == (F(1), F(2)), "F2 criteria")
    need(loss_answer["winners"] == ("b",) and regret_answer["winners"] == ("a",),
         "F2 choices")
    reject(lambda: f.consume_choice(regret_request, loss_evidence))
    record("F2_explicit_criteria_choose_differently", worst_loss_winner="b",
           worst_regret_winner="a")

    # F3: a hidden model oracle is not a common implementable policy.
    f3a = one_step("F3 A", (0, 1))
    f3b = one_step("F3 B", (1, 0))
    fam3 = family("F3 family", f3a, f3b)
    entries3 = catalogue(f3a, ("a", "b"))
    q3 = f.ChoiceRequest(fam3, entries3, f.FULL, f.MINIMAX_LOSS)
    x3 = f.consume_choice(q3, f.choose(q3))
    common3 = f.ChoiceRequest(fam3, entries3, f.FULL, f.COMMON_OPTIMAL)
    need(x3["worst_costs"] == (F(1), F(1)) and
         x3["worst_regrets"] == (F(1), F(1)), "F3 deterministic values")
    need(f.consume_choice(common3, f.choose(common3))["winners"] == (),
         "F3 no common optimizer")
    reject(lambda: f.NamedPolicyRequest(fam3, [entries3[0].policy, entries3[1].policy], []))
    need((F(0) + F(1)) / 2 == F(1, 2), "F3 mixture arithmetic")
    record("F3_hidden_model_oracle_rejected", deterministic_value=1,
           separate_randomized_context_value=F(1, 2))

    # F4: real observations, unlike hidden model labels, may select later actions.
    L, R = (("observe", "L"),), (("observe", "R"),)
    f4a = r.Subject("F4 A", 2, "loss", (), [
        r.Node((), actions=[r.Action("observe", 0, [("L", 1), ("R", 0)])]),
        r.Node(L, actions=[r.Action("a", 0), r.Action("b", 1)]),
        r.Node(R, actions=[r.Action("a", 0), r.Action("b", 1)]),
    ])
    f4b = r.Subject("F4 B", 2, "loss", (), [
        r.Node((), actions=[r.Action("observe", 0, [("L", 0), ("R", 1)])]),
        r.Node(L, actions=[r.Action("a", 1), r.Action("b", 0)]),
        r.Node(R, actions=[r.Action("a", 1), r.Action("b", 0)]),
    ])
    fam4 = family("F4 family", f4a, f4b)
    entries4 = catalogue(f4a, ("aa", "ab", "ba", "bb"))
    common4 = f.ChoiceRequest(fam4, entries4, f.FULL, f.COMMON_OPTIMAL)
    common_answer = f.consume_choice(common4, f.choose(common4))
    need(common_answer["winners"] == ("ab",), "F4 observed-history policy")
    shared4 = next(x.policy for x in entries4 if x.identity == "ab")
    c4q = f.ContinuationRequest(fam4, shared4, shared4, L)
    c4e = f.condition(c4q)
    c4a = f.consume_condition(c4q, c4e)
    need(c4a["retained"] == ("m1",) and c4a["excluded_zero_mass"] == ("m2",),
         "F4 support filter")
    reject(lambda: f.consume_condition(c4q, replace(c4e, retained=("m1", "m2"), excluded=())))
    record("F4_observed_signal_support_filter", shared_policy_costs=(0, 0),
           retained_at_L=("m1",), excluded_at_L=("m2",))

    # F5: one model is held fixed over both dates.
    T = (("continue", "next"),)
    f5a = r.Subject("F5 A", 2, "loss", (), [
        r.Node((), actions=[r.Action("continue", 0, [("next", 1)])]),
        r.Node(T, actions=[r.Action("end", 1)]),
    ])
    f5b = r.Subject("F5 B", 2, "loss", (), [
        r.Node((), actions=[r.Action("continue", 1, [("next", 1)])]),
        r.Node(T, actions=[r.Action("end", 0)]),
    ])
    fam5 = family("F5 family", f5a, f5b)
    entries5 = catalogue(f5a, ("only",))
    q5 = f.ChoiceRequest(fam5, entries5, f.FULL, f.MINIMAX_LOSS)
    e5 = f.choose(q5)
    x5 = f.consume_choice(q5, e5)
    need(x5["matrix"] == ((F(1),), (F(1),)) and x5["worst_costs"] == (F(1),),
         "F5 fixed model values")
    reject(lambda: f.consume_choice(q5, replace(e5, matrix=((F(2),), (F(1),)))))
    record("F5_model_fixed_between_dates", whole_episode_worst=1,
           rowwise_rectangularized_value=2)

    # F6: full-class coverage is recomputed, while subset claims remain available.
    f6 = one_step("F6", (0, 1, 2), ("a", "b", "c"))
    fam6 = family("F6 family", f6)
    pa6, pb6, pc6 = direct_policies(f6)
    subset6 = (f.PolicyEntry("b", pb6), f.PolicyEntry("c", pc6))
    subset_request = f.ChoiceRequest(fam6, subset6, f.SUBSET, f.MINIMAX_LOSS)
    subset_evidence = f.choose(subset_request)
    subset_answer = f.consume_choice(subset_request, subset_evidence)
    need(subset_answer["winners"] == ("b",) and subset_answer["worst_costs"] == (F(1), F(2)),
         "F6 subset")
    reject(lambda: f.ChoiceRequest(fam6, subset6, f.FULL, f.MINIMAX_LOSS))
    reject(lambda: f.ChoiceRequest(fam6,
                                   (f.PolicyEntry("b1", pb6), f.PolicyEntry("b2", pb6)),
                                   f.SUBSET, f.MINIMAX_LOSS))
    reject(lambda: f.consume_choice(subset_request,
                                    replace(subset_evidence, policy_count=3)))
    full6 = (f.PolicyEntry("a", pa6),) + subset6
    full_request6 = f.ChoiceRequest(fam6, full6, f.FULL, f.MINIMAX_LOSS)
    need(f.consume_choice(full_request6, f.choose(full_request6))["winners"] == ("a",),
         "F6 full optimum")
    record("F6_coverage_and_subset_scope", subset_optimum=1, full_optimum=0)

    # F7: PR7 accumulation is applied inside, never across, exact model identities.
    groups7 = []
    exact7 = []
    for member in fam1.members:
        certificate = r.produce(member.subject, pa)
        exact7.append(certificate)
        upper_loose = replace(certificate, upper=tuple(x + 1 for x in certificate.upper))
        lower_loose = replace(certificate, lower=tuple(x - 1 for x in certificate.lower))
        groups7.append(f.ModelSources(member.identity,
                                      [a.Source("upper-loose", upper_loose),
                                       a.Source("lower-loose", lower_loose)]))
    q7 = f.NamedPolicyRequest(fam1, pa, groups7)
    e7 = f.bound_named_policy(q7)
    x7 = f.consume_named_policy(q7, e7)
    need(tuple(row.evidence.certificate for row in e7.combined) == tuple(exact7),
         "F7 within-model accumulation")
    need(x7["worst_regret_upper"] == 2, "F7 family aggregate")
    cross = r.Certificate(f1a, pa, (F(100),), (F(2),))
    forged = a.Evidence(e7.combined[0].evidence.request, cross)
    reject(lambda: f.consume_named_policy(q7, replace(
        e7, combined=(f.ModelAccumulation("m1", forged), e7.combined[1]))))
    reject(lambda: f.NamedPolicyRequest(fam1, pa,
        (replace(groups7[0], member_identity="m2"), groups7[1])))
    reject(lambda: f.NamedPolicyRequest(fam1, pa,
        (groups7[0], f.ModelSources("m2", [a.Source("wrong", exact7[0])]))))
    record("F7_accumulate_only_within_models", modelwise_gaps=(2, 0),
           family_worst_regret=2)

    # F8: signed, early-stop, three-observation, union-support sequential family.
    L8, M8, R8 = (("probe", "L"),), (("probe", "M"),), (("probe", "R"),)
    f8a = r.Subject("F8 A", 2, "loss", ("observable probe",), [
        r.Node((), actions=[r.Action("stop", 2),
                            r.Action("probe", F(-1, 2),
                                     [("L", F(1, 2)), ("M", F(1, 2)), ("R", 0)])]),
        r.Node(R8, actions=[r.Action("x", 3), r.Action("y", 0)]),
        r.Node(L8, actions=[r.Action("x", 0), r.Action("y", 2)]),
        r.Node(M8, actions=[r.Action("x", 1), r.Action("y", -1)]),
    ])
    f8b = r.Subject("F8 B", 2, "loss", ("observable probe",), [
        r.Node((), actions=[r.Action("stop", 1),
                            r.Action("probe", F(1, 4),
                                     [("L", 0), ("M", F(1, 2)), ("R", F(1, 2))])]),
        r.Node(R8, actions=[r.Action("x", 2), r.Action("y", 0)]),
        r.Node(L8, actions=[r.Action("x", 0), r.Action("y", 2)]),
        r.Node(M8, actions=[r.Action("x", -1), r.Action("y", 1)]),
    ])
    fam8 = family("F8 family", f8a, f8b)
    policies8 = direct_policies(f8a)
    entries8 = tuple(f.PolicyEntry(f"p{i:02d}", pi) for i, pi in enumerate(policies8))
    need(len(entries8) == 16, "F8 complete deterministic count")
    matrix8 = tuple(tuple(direct_value(member.subject, entry.policy)
                          for entry in entries8) for member in fam8.members)
    loss8q = f.ChoiceRequest(fam8, entries8, f.FULL, f.MINIMAX_LOSS)
    regret8q = f.ChoiceRequest(fam8, entries8, f.FULL, f.MINIMAX_REGRET)
    common8q = f.ChoiceRequest(fam8, entries8, f.FULL, f.COMMON_OPTIMAL)
    loss8e, regret8e = f.choose(loss8q), f.choose(regret8q)
    loss8, regret8 = f.consume_choice(loss8q, loss8e), f.consume_choice(regret8q, regret8e)
    need(loss8["matrix"] == matrix8 and regret8["matrix"] == matrix8,
         "F8 direct full paths versus exact matrix")
    need(min(loss8["worst_costs"]) == 0 and len(loss8["winners"]) == 1,
         "F8 minimum worst loss")
    need(min(regret8["worst_regrets"]) == 1 and len(regret8["winners"]) == 4,
         "F8 regret ties")
    need(f.consume_choice(common8q, f.choose(common8q))["winners"] == (),
         "F8 competing modelwise actions")
    winner8 = next(x.policy for x in entries8 if x.identity == loss8["winners"][0])
    named8q = exact_named_request(fam8, winner8)
    named8e = f.bound_named_policy(named8q)
    named8 = f.consume_named_policy(named8q, named8e)
    need(named8["worst_policy_upper"] == 0 and named8["worst_regret_upper"] == 1,
         "F8 named policy")
    l8q = f.ContinuationRequest(fam8, winner8, winner8, L8)
    l8e = f.condition(l8q)
    l8 = f.consume_condition(l8q, l8e)
    need(l8["retained"] == ("m1",) and l8["excluded_zero_mass"] == ("m2",) and
         l8["modelwise"][0][3] == direct_value(f8a, winner8, L8), "F8 L continuation")
    m8q = f.ContinuationRequest(fam8, winner8, winner8, M8)
    m8 = f.consume_condition(m8q, f.condition(m8q))
    need(m8["retained"] == ("m1", "m2") and
         tuple(row[1] for row in m8["modelwise"]) == (F(1, 2), F(1, 2)),
         "F8 positive family prefix")
    stop8 = next(entry.policy for entry in entries8 if dict(entry.policy.choices)[()] == "stop")
    impossible8q = f.ContinuationRequest(fam8, stop8, winner8, L8)
    reject(lambda: f.consume_condition(impossible8q, f.condition(impossible8q)),
           f.ImpossibleConditioning)
    record("F8_nontrivial_sequential_family", policies=16,
           minimum_worst_loss=0, minimum_worst_regret=1, regret_ties=4,
           L_retained=("m1",), M_retained=("m1", "m2"))

    # Cross-cutting input, exactness, resource, and mutation controls.
    reject(lambda: f.Family("bad unit", [f.Member("a", f1a),
                                          f.Member("b", replace(f1b, unit="utility"))]))
    reject(lambda: replace(fam1, criterion="tail-risk"))
    missing8 = r.Policy(tuple(winner8.choices[:-1]))
    reject(lambda: exact_named_request(fam8, missing8))
    reject(lambda: r.Certificate(f1a, pa, (True,), (F(2),)))
    reject(lambda: r.Certificate(f1a, pa, (F(0),), (0.0,)))
    huge = F(2 ** 1024)
    huge_certificate = r.Certificate(f1a, pa, (-huge,), (huge,))
    huge_family = family("large exact proof", f1a)
    huge_request = f.NamedPolicyRequest(huge_family, pa, [
        f.ModelSources("m1", [a.Source("large", huge_certificate)])
    ])
    huge_answer = f.consume_named_policy(huge_request, f.bound_named_policy(huge_request))
    need(huge_answer["worst_regret_upper"] == 2 * huge, "large derived rational")

    wide_children = tuple((("probe", f"o{i}"),) for i in range(4))
    wide = r.Subject("coverage budget", 2, "loss", (), [
        r.Node((), actions=[r.Action("probe", 0,
                                    [(f"o{i}", F(1, 4)) for i in range(4)])]),
        *(r.Node(h, actions=[r.Action(f"a{j}", j) for j in range(4)])
          for h in wide_children),
    ])
    wide_family = family("coverage budget family", wide)
    wide_policy = policy(wide, ("probe", "a0", "a0", "a0", "a0"))
    reject(lambda: f.ChoiceRequest(wide_family,
                                   (f.PolicyEntry("candidate", wide_policy),),
                                   f.FULL, f.MINIMAX_LOSS), f.Unfinished)
    wide_named = exact_named_request(wide_family, wide_policy)
    f.consume_named_policy(wide_named, f.bound_named_policy(wide_named))

    members = [f.Member("m1", f1a)]
    detached_family = f.Family("detached", members)
    members.clear()
    sources = [a.Source("exact", r.produce(f1a, pa))]
    detached_group = f.ModelSources("m1", sources)
    sources.clear()
    groups = [detached_group]
    detached_request = f.NamedPolicyRequest(detached_family, pa, groups)
    groups.clear()
    detached_evidence = f.bound_named_policy(detached_request)
    need(f.consume_named_policy(detached_request, detached_evidence)["worst_regret_upper"] == 2,
         "detached caller containers")
    record("exact_inputs_limits_and_immutable_requests",
           derived_bits=(2 * huge).numerator.bit_length(),
           refused_full_policy_count=256, named_policy_bound_preserved=True)

    # Zero horizon and one-model reduction retain inherited exact meanings.
    zero = r.Subject("zero horizon", 0, "loss", (), [r.Node((), terminal=-2)])
    zero_family = family("zero family", zero)
    zero_policy = r.Policy([])
    zero_entries = (f.PolicyEntry("terminal", zero_policy),)
    zero_choice = f.ChoiceRequest(zero_family, zero_entries, f.FULL, f.MINIMAX_REGRET)
    zero_answer = f.consume_choice(zero_choice, f.choose(zero_choice))
    zero_named_request = exact_named_request(zero_family, zero_policy)
    zero_named = f.consume_named_policy(zero_named_request,
                                        f.bound_named_policy(zero_named_request))
    inherited = r.consume(zero, zero_policy, r.produce(zero, zero_policy))
    need(zero_answer["matrix"] == ((F(-2),),) and zero_answer["winners"] == ("terminal",),
         "zero-horizon matrix")
    need((zero_named["worst_policy_upper"], zero_named["worst_regret_upper"]) ==
         (inherited["policy_upper"], inherited["regret_upper"]), "one-model reduction")
    need(len(entries5) == 1, "singleton policy class")
    record("zero_horizon_singleton_and_one_model_reduction", terminal_value=-2)

    # All receiving remains operational with every relevant candidate producer disabled.
    saved = (f.bound_named_policy, f.choose, f.condition, a.combine, a._produce, r.produce)

    def disabled(*args, **kwargs):
        raise RuntimeError("candidate producer invoked")

    try:
        f.bound_named_policy = f.choose = f.condition = disabled
        a.combine = a._produce = r.produce = disabled
        f.consume_named_policy(q1, e1)
        f.consume_choice(loss_request, loss_evidence)
        f.consume_choice(regret8q, regret8e)
        f.consume_condition(c4q, c4e)
        reject(lambda: f.consume_named_policy(q1, replace(e1, worst_regret_upper=F(0))))
    finally:
        f.bound_named_policy, f.choose, f.condition, a.combine, a._produce, r.produce = saved
    record("receivers_run_with_candidate_producers_disabled")

    print(json.dumps(r.wire({"passed": len(results), "failed": 0,
                             "rejections": rejections, "results": results,
                             "optimized": sys.flags.optimize}), sort_keys=True))


if __name__ == "__main__":
    run()
