"""Fixed family-replanning cases and independent forward complete-path checks."""
from dataclasses import replace
from fractions import Fraction as F
import json
import sys

import replanning as p

f, r, a = p.f, p.r, p.a
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
    raise RuntimeError("invalid replanning claim accepted")


def direct_value(subject, policy, start=()):
    """Forward complete paths; no Bellman backup, certificate or producer call."""
    nodes, chosen = {node.h: node for node in subject.nodes}, dict(policy.choices)
    pending, total, final_mass = [(start, F(1), F(0))], F(0), F(0)
    while pending:
        history, mass, paid = pending.pop()
        node = nodes[history]
        if not node.actions:
            total += mass * (paid + node.terminal)
            final_mass += mass
            continue
        action = next(action for action in node.actions
                      if action.label == chosen[history])
        if not action.outcomes:
            total += mass * (paid + action.cost)
            final_mass += mass
            continue
        for observation, probability in action.outcomes:
            if probability:
                pending.append((history + ((action.label, observation),),
                                mass * probability, paid + action.cost))
    need(final_mass == 1, "direct path mass")
    return total


def mapped_policy(subject, choices):
    return r.Policy(tuple((node.h, choices[node.h]) for node in subject.nodes if node.actions))


def family(identity, rows):
    return f.Family(identity, [f.Member(member_identity, subject)
                               for member_identity, subject in rows])


def request(fam, baseline, event, replacement, cap, threshold,
            baseline_certificates=None, replacement_certificates=None):
    if baseline_certificates is None:
        baseline_certificates = [r.produce(member.subject, baseline)
                                 for member in fam.members]
    if replacement_certificates is None:
        replacement_certificates = [r.produce(member.subject, replacement)
                                    for member in fam.members]
    rows = [p.ModelSources(
        member.identity,
        a.Source(f"baseline-{member.identity}", baseline_certificate),
        a.Source(f"replacement-{member.identity}", replacement_certificate))
        for member, baseline_certificate, replacement_certificate in
        zip(fam.members, baseline_certificates, replacement_certificates)]
    return p.Request(fam, baseline, event, replacement, rows, cap, F(threshold))


def shifted_upper(certificate, amount):
    return replace(certificate,
                   upper=tuple(value + amount for value in certificate.upper))


def run():
    results = []

    def record(name, **values):
        results.append(dict(case=name, status="PASS", **values))

    # R1: the conditionally preferred action destroys both original root caps.
    H, O = (("observe", "h"),), (("observe", "other"),)

    def r1_subject(name, probability, a_cost):
        return r.Subject(name, 2, "loss", ("fixed whole-episode model",), [
            r.Node((), actions=[r.Action("observe", 0,
                                         [("h", probability),
                                          ("other", 1 - probability)])]),
            r.Node(H, actions=[r.Action("a", a_cost), r.Action("b", 2)]),
            r.Node(O, terminal=0),
        ])

    r1a, r1b = r1_subject("R1 A", F(9, 10), 0), r1_subject("R1 B", F(1, 10), 10)
    fam1 = family("R1 family", (("A", r1a), ("B", r1b)))
    base1 = mapped_policy(r1a, {(): "observe", H: "a"})
    replacement1 = mapped_policy(r1a, {(): "observe", H: "b"})
    cost1q = request(fam1, base1, H, replacement1, p.EXPECTED_COST_CAP, 1)
    cost1e = p.splice(cost1q)
    final1 = cost1e.final_policy
    cost1 = p.consume(cost1q, final1, cost1e)
    need(cost1["baseline_values"] == (F(0), F(1)) and
         cost1["spliced_values"] == (F(9, 5), F(1, 5)) and
         cost1["allowances"] == (F(10, 9), F(10)) and
         cost1["continuation_within_allowance"] == (False, True) and
         cost1["disposition"] == p.NOT_ESTABLISHED, "R1 root cost cap")
    regret1q = request(fam1, base1, H, replacement1, p.REGRET_CAP, F(4, 5))
    regret1e = p.splice(regret1q)
    regret1 = p.consume(regret1q, regret1e.final_policy, regret1e)
    need(regret1["baseline_values"] == (F(0), F(4, 5)) and
         regret1["spliced_values"] == (F(9, 5), F(0)) and
         regret1["allowances"] == (F(8, 9), F(10)) and
         regret1["continuation_within_allowance"] == (False, True) and
         regret1["disposition"] == p.NOT_ESTABLISHED, "R1 root regret cap")
    exact1e = p.exact_evidence(cost1q)
    exact1 = p.consume_exact(cost1q, final1, exact1e)
    need(exact1["cap_disposition"] == p.VIOLATION and
         exact1["final_metrics"] == (F(9, 5), F(1, 5)), "R1 exact violation")

    baseline_conditional = f.ContinuationRequest(fam1, base1, base1, H)
    replacement_conditional = f.ContinuationRequest(fam1, base1, replacement1, H)
    bc = f.consume_condition(baseline_conditional, f.condition(baseline_conditional))
    rc = f.consume_condition(replacement_conditional, f.condition(replacement_conditional))
    need(max(row[3] for row in bc["modelwise"]) == 10 and
         max(row[4] for row in bc["modelwise"]) == 8 and
         max(row[3] for row in rc["modelwise"]) == 2 and
         max(row[4] for row in rc["modelwise"]) == 2, "R1 conditional comparison")
    entries1 = tuple(f.PolicyEntry(dict(pi.choices)[H], pi)
                     for pi in r.enumerate_policies(r1a))
    loss1q = f.ChoiceRequest(fam1, entries1, f.FULL, f.MINIMAX_LOSS)
    choice_regret1q = f.ChoiceRequest(fam1, entries1, f.FULL, f.MINIMAX_REGRET)
    loss1 = f.consume_choice(loss1q, f.choose(loss1q))
    choice_regret1 = f.consume_choice(choice_regret1q, f.choose(choice_regret1q))
    direct1 = tuple(tuple(direct_value(member.subject, entry.policy) for entry in entries1)
                    for member in fam1.members)
    need(loss1["matrix"] == direct1 and loss1["winners"] == ("a",) and
         choice_regret1["winners"] == ("a",), "R1 independent complete policy choice")
    record("R1_conditional_improvement_root_deterioration",
           baseline_root=(F(0), F(1)), replacement_root=(F(9, 5), F(1, 5)),
           conditional_worst_loss=(10, 2), conditional_worst_regret=(8, 2),
           preserved_cost_cap=False, preserved_regret_cap=False)

    # R2: a shared continuation improves both fixed models and preserves both caps.
    def r2_subject(name, root_cost, probability, other_terminal, a_cost, b_cost):
        return r.Subject(name, 2, "loss", ("signed exact costs",), [
            r.Node((), actions=[r.Action("stop", 4),
                                r.Action("probe", root_cost,
                                         [("h", probability),
                                          ("other", 1 - probability)])]),
            r.Node((("probe", "h"),),
                   actions=[r.Action("a", a_cost), r.Action("b", b_cost)]),
            r.Node((("probe", "other"),), terminal=other_terminal),
        ])

    H2 = (("probe", "h"),)
    r2a = r2_subject("R2 A", -1, F(1, 2), 2, 3, -1)
    r2b = r2_subject("R2 B", F(1, 4), F(1, 3), -2, 2, 1)
    fam2 = family("R2 family", (("A", r2a), ("B", r2b)))
    base2 = mapped_policy(r2a, {(): "probe", H2: "a"})
    replacement2 = mapped_policy(r2a, {(): "probe", H2: "b"})
    cost2q = request(fam2, base2, H2, replacement2, p.EXPECTED_COST_CAP, F(3, 2))
    cost2e = p.splice(cost2q)
    final2 = cost2e.final_policy
    cost2 = p.consume(cost2q, final2, cost2e)
    need(cost2["baseline_values"] == (F(3, 2), F(-5, 12)) and
         cost2["spliced_values"] == (F(-1, 2), F(-3, 4)) and
         cost2["disposition"] == p.PRESERVED and
         cost2["member_masses"] == (F(1, 2), F(1, 3)), "R2 preserved cost")
    regret2q = request(fam2, base2, H2, replacement2, p.REGRET_CAP, 2)
    regret2e = p.splice(regret2q)
    regret2 = p.consume(regret2q, regret2e.final_policy, regret2e)
    need(regret2["baseline_values"] == (F(2), F(1, 3)) and
         regret2["spliced_values"] == (F(0), F(0)) and
         regret2["disposition"] == p.PRESERVED, "R2 preserved regret")
    exact2e = p.exact_evidence(cost2q)
    exact2 = p.consume_exact(cost2q, final2, exact2e)
    need(exact2["all_members_nonworsening"] and exact2["aggregate_nonworsening"],
         "R2 actual improvement")
    named2q = f.NamedPolicyRequest(fam2, final2, [
        f.ModelSources(row.member_identity, [a.Source("checked-splice", row.certificate)])
        for row in cost2e.rows
    ])
    named2 = f.consume_named_policy(named2q, f.bound_named_policy(named2q))
    need(named2["worst_policy_upper"] == F(-1, 2) and
         named2["worst_regret_upper"] == 0, "R2 inherited named-family route")
    record("R2_genuine_preserved_improvement", positive_masses=(F(1, 2), F(1, 3)),
           baseline_worst=F(3, 2), final_worst=F(-1, 2),
           cost_cap_preserved=True, regret_cap_preserved=True)

    # R3: a -99 change between two upper tables is not actual improvement.
    r3s = r.Subject("R3", 1, "loss", (), [
        r.Node((), actions=[r.Action("a", 0), r.Action("b", 1)])
    ])
    fam3 = family("R3 family", (("only", r3s),))
    base3 = mapped_policy(r3s, {(): "a"})
    replacement3 = mapped_policy(r3s, {(): "b"})
    loose3 = r.Certificate(r3s, base3, (F(0),), (F(100),))
    exact_b3 = r.produce(r3s, replacement3)
    q3 = request(fam3, base3, (), replacement3, p.EXPECTED_COST_CAP, 100,
                 [loose3], [exact_b3])
    e3 = p.splice(q3)
    x3 = p.consume(q3, e3.final_policy, e3)
    exact3e = p.exact_evidence(q3)
    exact3 = p.consume_exact(q3, e3.final_policy, exact3e)
    need(x3["spliced_values"] == (F(1),) and
         exact3["modelwise"][0][5] == 1 and 1 - 100 == -99, "R3 distinctions")
    reject(lambda: p.consume_exact(q3, e3.final_policy,
                                    replace(exact3e, claimed_root_deltas=(F(-99),))))
    record("R3_certificate_tightening_not_actual_improvement",
           certificate_upper_change=-99, actual_policy_change=1,
           valid_spliced_upper=1)

    # R4: loose evidence is insufficient, while exact evidence establishes no violation.
    r4s = r.Subject("R4", 1, "loss", (), [r.Node((), actions=[r.Action("a", 0)])])
    fam4 = family("R4 family", (("only", r4s),))
    pi4 = mapped_policy(r4s, {(): "a"})
    exact4 = r.produce(r4s, pi4)
    loose4 = shifted_upper(exact4, F(2))
    cost4q = request(fam4, pi4, (), pi4, p.EXPECTED_COST_CAP, 1, [exact4], [loose4])
    cost4e = p.splice(cost4q)
    need(p.consume(cost4q, cost4e.final_policy, cost4e)["disposition"] ==
         p.NOT_ESTABLISHED, "R4 loose cost bound")
    need(p.consume_exact(cost4q, cost4e.final_policy,
                         p.exact_evidence(cost4q))["cap_disposition"] == p.EXACT_SATISFIED,
         "R4 exact cost resolution")
    regret4q = request(fam4, pi4, (), pi4, p.REGRET_CAP, 1, [exact4], [loose4])
    regret4e = p.splice(regret4q)
    need(p.consume(regret4q, regret4e.final_policy, regret4e)["disposition"] ==
         p.NOT_ESTABLISHED, "R4 loose regret bound")
    tight4q = request(fam4, pi4, (), pi4, p.EXPECTED_COST_CAP, 1, [exact4], [exact4])
    tight4e = p.splice(tight4q)
    need(p.consume(tight4q, tight4e.final_policy, tight4e)["disposition"] == p.PRESERVED,
         "R4 tightened certificate")
    absent_premise4q = request(fam4, pi4, (), pi4, p.EXPECTED_COST_CAP, 1,
                               [loose4], [exact4])
    absent_premise4e = p.splice(absent_premise4q)
    need(p.consume(absent_premise4q, absent_premise4e.final_policy,
                   absent_premise4e)["disposition"] == p.BASELINE_NOT_ESTABLISHED,
         "R4 baseline preservation premise")
    record("R4_failure_to_certify_not_violation", true_cost=0, loose_upper=2,
           cost_disposition=p.NOT_ESTABLISHED, regret_disposition=p.NOT_ESTABLISHED,
           tightened_disposition=p.PRESERVED,
           absent_baseline_premise=p.BASELINE_NOT_ESTABLISHED)

    # R5: zero-mass conditional exclusion never removes a member from the root cap.
    def r5_subject(name, probability):
        return r.Subject(name, 2, "loss", (), [
            r.Node((), actions=[r.Action("observe", 0,
                                         [("h", probability),
                                          ("other", 1 - probability)])]),
            r.Node(H, actions=[r.Action("a", 0), r.Action("b", 1)]),
            r.Node(O, terminal=10),
        ])

    r5a, r5b = r5_subject("R5 A", F(0)), r5_subject("R5 B", F(1))
    fam5 = family("R5 family", (("A", r5a), ("B", r5b)))
    base5 = mapped_policy(r5a, {(): "observe", H: "a"})
    replacement5 = mapped_policy(r5a, {(): "observe", H: "b"})
    q5 = request(fam5, base5, H, replacement5, p.EXPECTED_COST_CAP, 10)
    e5 = p.splice(q5)
    x5 = p.consume(q5, e5.final_policy, e5)
    need(x5["member_masses"] == (F(0), F(1)) and
         x5["spliced_values"] == (F(10), F(1)) and
         x5["allowances"][0] is None and x5["disposition"] == p.PRESERVED,
         "R5 ex-ante member retention")
    conditional5q = f.ContinuationRequest(fam5, base5, replacement5, H)
    conditional5 = f.consume_condition(conditional5q, f.condition(conditional5q))
    need(conditional5["retained"] == ("B",) and
         conditional5["excluded_zero_mass"] == ("A",), "R5 conditional partition")
    r5c = r5_subject("R5 C", F(0))
    all_zero5 = family("R5 all zero", (("A", r5a), ("C", r5c)))
    all_zero_q = request(all_zero5, base5, H, replacement5, p.EXPECTED_COST_CAP, 10)
    all_zero_e = p.splice(all_zero_q)
    p.consume(all_zero_q, all_zero_e.final_policy, all_zero_e)
    impossible5q = f.ContinuationRequest(all_zero5, base5, replacement5, H)
    reject(lambda: f.consume_condition(impossible5q, f.condition(impossible5q)),
           f.ImpossibleConditioning)
    reject(lambda: f.Family("empty", []))
    record("R5_conditional_exclusion_preserves_root_family", root_worst=10,
           conditional_retained=("B",), all_zero_algebraic=True,
           all_zero_conditional="impossible")

    # R6: bind the whole prefix, subtree, family, sources, comparator and claim.
    O6 = (("observe", "other"),)
    r6s = r.Subject("R6", 2, "loss", (), [
        r.Node((), actions=[r.Action("stop", 3),
                            r.Action("observe", 0, [("h", F(1, 2)),
                                                     ("other", F(1, 2))])]),
        r.Node(H, actions=[r.Action("a", 2), r.Action("b", 1)]),
        r.Node(O6, actions=[r.Action("a", 0), r.Action("b", 4)]),
    ])
    fam6 = family("R6 family", (("only", r6s),))
    base6 = mapped_policy(r6s, {(): "observe", H: "a", O6: "a"})
    replacement6 = mapped_policy(r6s, {(): "observe", H: "b", O6: "b"})
    q6 = request(fam6, base6, H, replacement6, p.EXPECTED_COST_CAP, 3)
    e6 = p.splice(q6)
    final6 = e6.final_policy
    p.consume(q6, final6, e6)
    wrong_prefix6 = mapped_policy(r6s, {(): "stop", H: "b", O6: "a"})
    wrong_outside6 = mapped_policy(r6s, {(): "observe", H: "b", O6: "b"})
    reject(lambda: p.consume(q6, wrong_prefix6, e6))
    reject(lambda: p.consume(q6, wrong_outside6, e6))
    reject(lambda: p.Request(fam6, base6, H, [replacement6], q6.sources,
                               p.EXPECTED_COST_CAP, F(3)))
    incomplete6 = r.Policy((((), "observe"), (H, "b")))
    reject(lambda: request(fam6, base6, H, incomplete6,
                           p.EXPECTED_COST_CAP, 3))
    reject(lambda: replace(q6, event=(("observe", "absent"),)))
    other_event6q = request(fam6, base6, O6, replacement6,
                            p.EXPECTED_COST_CAP, 3)
    reject(lambda: p.consume(other_event6q, p._receiver_policy(other_event6q), e6))
    reject(lambda: replace(cost1q, sources=tuple(reversed(cost1q.sources))))
    wrong_old6 = p.ModelSources("only", a.Source("wrong-old", r.produce(r6s, replacement6)),
                                q6.sources[0].replacement)
    reject(lambda: replace(q6, sources=(wrong_old6,)))
    reject(lambda: replace(q6, criterion="tail-risk"))
    reject(lambda: replace(q6, cap="changed-cap"))
    reject(lambda: p.Request(fam6, base6, H, replacement6, q6.sources,
                             p.EXPECTED_COST_CAP, F(3), criterion="changed"))
    reject(lambda: p.Request(fam6, base6, H, replacement6, q6.sources,
                             p.EXPECTED_COST_CAP, 3.0))
    forged_factors6 = replace(e6.rows[0], path_factors=tuple(
        F(0) for _ in e6.rows[0].path_factors))
    reject(lambda: p.consume(q6, final6, replace(e6, rows=(forged_factors6,))))
    lower6 = tuple(value - 1 for value in e6.rows[0].certificate.lower)
    changed_comparator6 = replace(e6.rows[0], certificate=replace(
        e6.rows[0].certificate, lower=lower6))
    r.consume(r6s, final6, changed_comparator6.certificate)
    reject(lambda: p.consume(q6, final6, replace(e6, rows=(changed_comparator6,))))
    exact_target4 = r.produce(r4s, pi4)
    r.consume(r4s, pi4, exact_target4)
    false_provenance4 = replace(cost4e.rows[0], certificate=exact_target4)
    reject(lambda: p.consume(cost4q, cost4e.final_policy,
                             replace(cost4e, rows=(false_provenance4,))))
    wrong_cap6 = request(fam6, base6, H, replacement6, p.REGRET_CAP, 3)
    reject(lambda: p.consume(wrong_cap6, p._receiver_policy(wrong_cap6), e6))
    different_unit6 = replace(r6s, unit="utility")
    reject(lambda: f.Family("mixed unit", [f.Member("a", r6s),
                                            f.Member("b", different_unit6)]))
    wrong_member1 = p.ModelSources("A", cost1q.sources[0].baseline,
                                   cost1q.sources[1].replacement)
    reject(lambda: replace(cost1q, sources=(wrong_member1, cost1q.sources[1])))
    record("R6_complete_prefix_splice_and_claim_binding", matched_control=True)

    # R7: overlapping edits need correct predecessors, not old-plan delta addition.
    C7 = (("go", "child"),)
    r7s = r.Subject("R7", 2, "loss", (), [
        r.Node((), actions=[r.Action("stop", 2),
                            r.Action("go", 0, [("child", 1)])]),
        r.Node(C7, actions=[r.Action("a", 0), r.Action("b", 1)]),
    ])
    fam7 = family("R7 family", (("only", r7s),))
    old7 = mapped_policy(r7s, {(): "stop", C7: "a"})
    root7 = mapped_policy(r7s, {(): "go", C7: "a"})
    child7 = mapped_policy(r7s, {(): "stop", C7: "b"})
    final7 = mapped_policy(r7s, {(): "go", C7: "b"})
    root7q = request(fam7, old7, (), root7, p.EXPECTED_COST_CAP, 3)
    child7q = request(fam7, old7, C7, child7, p.EXPECTED_COST_CAP, 3)
    root7x = p.consume_exact(root7q, root7, p.exact_evidence(root7q))
    child7x = p.consume_exact(child7q, child7, p.exact_evidence(child7q))
    final_delta7 = direct_value(r7s, final7) - direct_value(r7s, old7)
    need(root7x["modelwise"][0][5] == -2 and child7x["modelwise"][0][5] == 0 and
         final_delta7 == -1 and -2 + 0 != final_delta7, "R7 overlapping old deltas")
    second7q = request(fam7, root7, C7, final7, p.EXPECTED_COST_CAP, 3)
    second7x = p.consume_exact(second7q, final7, p.exact_evidence(second7q))
    need(root7x["modelwise"][0][5] + second7x["modelwise"][0][5] == final_delta7,
         "R7 consecutive telescoping")
    reject(lambda: p.Request(fam7, old7, ((), C7), final7, root7q.sources,
                             p.EXPECTED_COST_CAP, F(3)))
    record("R7_overlapping_replacements", independent_old_deltas=(-2, 0),
           actual_final_delta=-1, consecutive_deltas=(-2, 1))

    # R8: deeper non-topological tree, support differences and trust boundaries.
    L8, R8 = (("probe", "L"),), (("probe", "R"),)
    LX8 = L8 + (("advance", "x"),)
    LY8 = L8 + (("advance", "y"),)
    LXZ8 = LX8 + (("finish", "z"),)

    def r8_subject(name, root_probabilities, branch_probabilities, costs):
        return r.Subject(name, 3, "loss", ("non-topological signed tree",), [
            r.Node((), actions=[r.Action("stop", costs[0]),
                                r.Action("probe", costs[1], root_probabilities)]),
            r.Node(LXZ8, terminal=costs[8]),
            r.Node(R8, actions=[r.Action("c", costs[2]), r.Action("d", costs[3])]),
            r.Node(LY8, terminal=costs[7]),
            r.Node(L8, actions=[r.Action("halt", costs[4]),
                                r.Action("advance", costs[5], branch_probabilities)]),
            r.Node(LX8, actions=[r.Action("quit", costs[6]),
                                 r.Action("finish", costs[9], [("z", 1)])]),
        ])

    r8a = r8_subject("R8 A", [("L", 1), ("R", 0)],
                     [("x", 1), ("y", 0)],
                     (2, F(-1, 3), -2, 1, 1, F(1, 2), 4, -1, -3, F(-1, 4)))
    r8b = r8_subject("R8 B", [("L", F(1, 3)), ("R", F(2, 3))],
                     [("x", F(1, 2)), ("y", F(1, 2))],
                     (3, F(1, 5), 1, -1, 2, F(-1, 2), 2, 2, 1, F(1, 3)))
    fam8 = family("R8 family", (("A", r8a), ("B", r8b)))
    base8 = mapped_policy(r8a, {(): "probe", R8: "c", L8: "advance", LX8: "finish"})
    replacement8 = mapped_policy(r8a, {(): "stop", R8: "d", L8: "halt", LX8: "quit"})
    cut_answers = {}
    cut_evidence = {}
    for name, event in (("root", ()), ("terminal", LXZ8),
                        ("support-varying", R8), ("deep", LX8)):
        query = request(fam8, base8, event, replacement8,
                        p.EXPECTED_COST_CAP, 10)
        evidence = p.splice(query)
        answer = p.consume(query, evidence.final_policy, evidence)
        exact = p.consume_exact(query, evidence.final_policy, p.exact_evidence(query))
        paths = tuple(direct_value(member.subject, evidence.final_policy)
                      for member in fam8.members)
        need(answer["spliced_values"] == paths and exact["final_metrics"] == paths,
             f"R8 {name} direct paths")
        cut_answers[name] = answer
        cut_evidence[name] = (query, evidence)
    need(cut_answers["support-varying"]["member_masses"] == (F(0), F(2, 3)),
         "R8 differing supports")
    need(cut_evidence["terminal"][1].final_policy == base8,
         "R8 terminal splice leaves policy unchanged")

    loose_terminal8 = [shifted_upper(r.produce(member.subject, replacement8), F(2))
                       for member in fam8.members]
    loose_terminal8q = request(fam8, base8, LXZ8, replacement8,
                               p.EXPECTED_COST_CAP, 10,
                               replacement_certificates=loose_terminal8)
    loose_terminal8e = p.splice(loose_terminal8q)
    loose_terminal8x = p.consume(loose_terminal8q, loose_terminal8e.final_policy,
                                 loose_terminal8e)
    need(loose_terminal8x["spliced_values"] == (F(-13, 12), F(143, 90)) and
         tuple(direct_value(member.subject, loose_terminal8e.final_policy)
               for member in fam8.members) == (F(-37, 12), F(113, 90)),
         "R8 terminal cut with signed slack")

    zero8 = r.Subject("R8 signed terminal only", 0, "loss", (),
                      [r.Node((), terminal=-2)])
    zero8_family = family("R8 terminal family", (("only", zero8),))
    zero8_policy = r.Policy(())
    zero8q = request(zero8_family, zero8_policy, (), zero8_policy,
                     p.EXPECTED_COST_CAP, -2)
    zero8e = p.splice(zero8q)
    need(p.consume(zero8q, zero8e.final_policy, zero8e)["disposition"] == p.PRESERVED,
         "R8 signed terminal-only root")

    huge = F(2 ** 1024, 3)
    loose8 = [shifted_upper(r.produce(member.subject, replacement8), huge)
              for member in fam8.members]
    huge8q = request(fam8, base8, LX8, replacement8, p.EXPECTED_COST_CAP,
                     huge + 10, replacement_certificates=loose8)
    huge8e = p.splice(huge8q)
    huge8 = p.consume(huge8q, huge8e.final_policy, huge8e)
    need(max(value.numerator.bit_length() for row in huge8e.rows
             for value in row.certificate.upper) > 1000, "R8 large derived fractions")
    reject(lambda: r.Certificate(r8a, base8,
                                 r.produce(r8a, base8).lower,
                                 tuple(True for _ in r8a.nodes)))
    reject(lambda: r.Certificate(r8a, base8,
                                 r.produce(r8a, base8).lower,
                                 tuple(0.0 for _ in r8a.nodes)))
    reject(lambda: p.Request(fam8, base8, LX8, replacement8, huge8q.sources,
                             p.EXPECTED_COST_CAP, True))

    members8 = [f.Member("A", r8a), f.Member("B", r8b)]
    detached_family8 = f.Family("detached R8", members8)
    members8.clear()
    sources8 = list(huge8q.sources)
    detached8q = p.Request(detached_family8, base8, LX8, replacement8,
                           sources8, p.EXPECTED_COST_CAP, huge + 10)
    sources8.clear()
    detached8e = p.splice(detached8q)
    p.consume(detached8q, detached8e.final_policy, detached8e)
    record("R8_deep_exact_controls", cuts=("root", "terminal", "support-varying", "deep"),
           support_masses=(F(0), F(2, 3)), derived_bits=max(
               value.numerator.bit_length() for row in huge8e.rows
               for value in row.certificate.upper),
           root_values=cut_answers["root"]["spliced_values"],
           terminal_values=cut_answers["terminal"]["spliced_values"],
           support_varying_values=cut_answers["support-varying"]["spliced_values"],
           deep_values=cut_answers["deep"]["spliced_values"],
           loose_terminal_values=loose_terminal8x["spliced_values"],
           terminal_only_value=-2, caller_containers_detached=True,
           huge_disposition=huge8["disposition"])

    # Receiving still works when all new and inherited candidate producers are disabled.
    saved = (p.splice, p.exact_evidence, p._producer_policy, p._producer_factor,
             f.bound_named_policy, f.choose, f.condition, a.combine, a._produce, r.produce)

    def disabled(*args, **kwargs):
        raise RuntimeError("candidate producer invoked")

    try:
        p.splice = p.exact_evidence = p._producer_policy = p._producer_factor = disabled
        f.bound_named_policy = f.choose = f.condition = disabled
        a.combine = a._produce = r.produce = disabled
        p.consume(cost2q, final2, cost2e)
        p.consume_exact(cost1q, final1, exact1e)
        p.consume(q5, e5.final_policy, e5)
        p.consume(cut_evidence["deep"][0], cut_evidence["deep"][1].final_policy,
                  cut_evidence["deep"][1])
        reject(lambda: p.consume(q6, final6, replace(e6, rows=(forged_factors6,))))
    finally:
        (p.splice, p.exact_evidence, p._producer_policy, p._producer_factor,
         f.bound_named_policy, f.choose, f.condition, a.combine, a._produce, r.produce) = saved
    record("receivers_run_with_new_and_inherited_producers_disabled")

    print(json.dumps(r.wire({"passed": len(results), "failed": 0,
                             "rejections": rejections, "results": results,
                             "optimized": sys.flags.optimize}), sort_keys=True))


if __name__ == "__main__":
    run()
