#!/usr/bin/env python3
"""Targeted public-subject and revision controls for PR #14 hardening."""
from dataclasses import replace
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from verification.multistream_collection import reference as ref  # noqa: E402
from verification.history_migration.checks import verify_moved_records  # noqa: E402


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def rejected(operation, message):
    try:
        operation()
    except (ref.Invalid, TypeError, KeyError):
        return
    raise AssertionError(message)


def subjects():
    streams = (
        ref.make_stream("A", "population-A", "protocol-A"),
        ref.make_stream("B", "population-B", "protocol-B"),
    )
    collection = ref.make_collection(
        streams, F(1, 20), (("A", F(1, 40)), ("B", F(1, 40))),
        record="collection-record", revision="revision-1")
    return streams, collection


def r1_collection_constructor():
    streams, collection = subjects()
    rejected(lambda: ref.make_collection(
        streams, F(1, 20), (("A", F(1, 40)), ("B", F(1, 40)),
                            ("ghost", F(9, 10)))),
        "public collection helper discarded an extra allocation")
    reordered = ref.make_collection(
        streams, F(1, 20), (("B", F(1, 40)), ("A", F(1, 40))))
    check(reordered.allocations == (("A", F(1, 40)), ("B", F(1, 40))),
          "complete reordered allocation was not canonicalized")
    rejected(lambda: ref.make_collection(
        streams, F(1, 20), (("A", F(1, 40)),)),
        "public collection helper accepted a missing allocation")
    rejected(lambda: ref.make_collection(
        streams, F(1, 20), (("A", F(1, 80)), ("A", F(1, 80)),
                            ("B", F(1, 40)))),
        "public collection helper accepted a duplicate allocation")

    direct_extra = replace(
        collection,
        allocations=(("A", F(1, 40)), ("B", F(1, 40)),
                     ("ghost", F(9, 10))))
    rejected(direct_extra.validate,
             "direct collection dataclass accepted an extra allocation")
    direct_reordered = replace(
        collection, allocations=(("B", F(1, 40)), ("A", F(1, 40))))
    check(direct_reordered.validate() == direct_reordered,
          "direct collection validation rejected complete reordered allocation")
    return {
        "ghost_allocation": "rejected-through-public-helper",
        "caller_allocation_sum": F(19, 20),
        "registered_reordering": "accepted-and-canonicalized",
        "missing_and_duplicate": "rejected",
        "direct_and_helper_subject_coverage": "aligned",
    }


def r2_decision_constructor():
    _, collection = subjects()
    safe = ref.make_affine_action("safe", 0, (("A", 0), ("B", 0)))
    risky = ref.make_affine_action(
        "risky", -1, (("A", 0), ("B", 0), ("ghost", 2)))
    rejected(lambda: ref.make_decision(
        collection, (safe, risky), intended_action="risky"),
        "public decision helper discarded an extra affine weight")
    reordered = ref.make_affine_action(
        "reordered", F(-1, 3), (("B", F(-2, 5)), ("A", F(7, 6))))
    decision = ref.make_decision(
        collection, (safe, reordered), intended_action="reordered")
    check(decision.actions[1].weights ==
          (("A", F(7, 6)), ("B", F(-2, 5))),
          "complete reordered weights were not canonicalized")

    direct = ref.DecisionRequest(
        collection, (safe, risky), "loss", "risky")
    rejected(direct.validate,
             "direct decision dataclass accepted an extra affine weight")
    collection_evidence = ref.produce_collection(collection)
    coverage = ref.produce_coverage(collection, collection_evidence)
    rejected(lambda: ref.produce_decision(direct, coverage),
             "material ghost-weight subject became a decision certificate")
    check(risky.intercept + dict(risky.weights)["ghost"] == 1,
          "material ghost-weight control changed meaning")
    return {
        "ghost_weight": "rejected-through-public-helper",
        "silently_truncated_risk": F(-1),
        "caller_risk_when_ghost_is_one": F(1),
        "opposite_decision_certificate_prevented": True,
        "registered_reordering": "accepted-and-canonicalized",
        "direct_and_helper_subject_coverage": "aligned",
    }


def r3_revision_classification():
    streams, base = subjects()
    same = replace(base)
    check(ref.classify_collection_revision(base, same) ==
          "same-transcript-recalculation-no-new-evidence",
          "unchanged subject/transcript/lineage was not a recalculation")

    for changed in (
        replace(base, record_identity="other-record"),
        replace(base, revision_identity="revision-2"),
        replace(base, predecessor_digest="0" * 64),
    ):
        check(ref.classify_collection_revision(base, changed) ==
              "provenance-changed-new-claim",
              "same transcript with changed provenance was treated as unchanged")

    event = ref.make_observation(1, "A", 1, 0, "event-1")
    correct = replace(
        base, transcript=(event,), revision_identity="revision-2",
        predecessor_digest=ref.collection_digest(base))
    check(ref.classify_collection_revision(base, correct) ==
          "append-only-transcript-extension", "valid append was not recognized")
    reused_revision = replace(correct, revision_identity=base.revision_identity)
    wrong_predecessor = replace(correct, predecessor_digest="0" * 64)
    changed_record = replace(correct, record_identity="other-record")
    for changed in (reused_revision, wrong_predecessor, changed_record):
        check(ref.classify_collection_revision(base, changed) ==
              "provenance-changed-new-claim",
              "unlinked growth was mislabeled append-only")

    changed_coverage = replace(
        base, allocations=(("A", F(1, 80)), ("B", F(3, 80))))
    check(ref.classify_collection_revision(base, changed_coverage) ==
          "new-coverage-specification", "changed allocation was misclassified")
    changed_rule = replace(base, rule_identity=ref.RULE_ROUND_ROBIN_SIX)
    check(ref.classify_collection_revision(base, changed_rule) ==
          "new-collection-subject", "changed rule was misclassified")
    changed_registry = replace(
        base, registry=(replace(streams[0], population_identity="new-population"),
                        streams[1]))
    check(ref.classify_collection_revision(base, changed_registry) ==
          "new-collection-subject", "changed registry was misclassified")

    prior = correct
    retroselected = replace(
        prior, transcript=(replace(event, value=1),))
    check(ref.classify_collection_revision(prior, retroselected) ==
          "corrected-or-retroselected-transcript-new-claim",
          "retroselected history was mislabeled append-only")
    return {
        "unchanged": "same-transcript-recalculation-no-new-evidence",
        "correct_append": "append-only-transcript-extension",
        "changed_lineage": "provenance-changed-new-claim",
        "same_revision_growth": "provenance-changed-new-claim",
        "wrong_predecessor": "provenance-changed-new-claim",
        "changed_record": "provenance-changed-new-claim",
        "changed_coverage": "new-coverage-specification",
        "changed_rule_or_registry": "new-collection-subject",
        "retroselected": "corrected-or-retroselected-transcript-new-claim",
    }


def r4_stopping_state_revision_classification():
    streams, base = subjects()
    same = replace(base)
    check(ref.classify_collection_revision(base, same) ==
          "same-transcript-recalculation-no-new-evidence",
          "identical stopping state was not an ordinary recalculation")

    toggled = replace(base, stopped=True)
    check(toggled.validate() == toggled,
          "structurally valid stopping-state control did not validate")
    check(ref.collection_digest(toggled) != ref.collection_digest(base),
          "stopping state was absent from the collection digest")
    check(ref.classify_collection_revision(base, toggled) ==
          "provenance-changed-new-claim",
          "changed stopping state was treated as an ordinary recalculation")
    rejected(lambda: ref.produce_collection(toggled),
             "producer accepted a rule-inconsistent stopping state")
    base_evidence = ref.produce_collection(base)
    toggled_evidence = replace(
        base_evidence, subject=toggled,
        subject_digest=ref.collection_digest(toggled))
    rejected(lambda: ref.consume_collection(toggled, toggled_evidence),
             "receiver accepted a rule-inconsistent stopping state")

    def event(index):
        stream = streams[(index - 1) % len(streams)].stream_identity
        local = (index + len(streams) - 1) // len(streams)
        return ref.make_observation(
            index, stream, local, index % 2, f"stopping-event-{index}")

    prefix = ref.make_collection(
        streams, base.total_alpha, base.allocations,
        rule=ref.RULE_ROUND_ROBIN_SIX,
        transcript=tuple(event(index) for index in range(1, 6)),
        stopped=False, record="stopping-record", revision="revision-1")
    successor = ref.make_collection(
        streams, base.total_alpha, base.allocations,
        rule=ref.RULE_ROUND_ROBIN_SIX,
        transcript=tuple(event(index) for index in range(1, 7)),
        stopped=True, record=prefix.record_identity, revision="revision-2",
        predecessor_digest=ref.collection_digest(prefix))
    check(ref.produce_collection(prefix).disposition == "observe",
          "valid append prefix did not remain open")
    successor_evidence = ref.produce_collection(successor)
    check(ref.consume_collection(successor, successor_evidence)["disposition"] == "stop",
          "valid terminal successor did not pass full receiving")
    check(ref.classify_collection_revision(prefix, successor) ==
          "append-only-transcript-extension",
          "valid not-stopped to stopped append was not recognized")
    return {
        "unchanged_stopping_state":
            "same-transcript-recalculation-no-new-evidence",
        "toggled_stopping_state": "provenance-changed-new-claim",
        "toggled_subject_digest_changed": True,
        "inconsistent_state_producer": "rejected-by-full-replay",
        "inconsistent_state_receiver": "rejected-by-full-replay",
        "valid_false_to_true_append": "append-only-transcript-extension",
        "valid_successor_replay_disposition": "stop",
    }


def main():
    moved = verify_moved_records()
    result = {
        "status": "passed",
        "groups": {
            "R1": r1_collection_constructor(),
            "R2": r2_decision_constructor(),
            "R3": r3_revision_classification(),
            "R4": r4_stopping_state_revision_classification(),
            "PR13": {
                "canonical_history_records": sorted(moved),
                "obsolete_root_ledgers_absent": all(
                    not (ROOT / name).exists() for name in (
                        "FINDINGS_LEDGER.md", "MATH_ARCHIVE_LEDGER.md",
                        "SUBSTRATE_LEDGER.md", "LEGACY_ARCHIVE_STATUS.md")),
            },
        },
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    check(result["groups"]["PR13"]["obsolete_root_ledgers_absent"],
          "obsolete root ledger was resurrected")
    print(json.dumps(ref.wire(result), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
