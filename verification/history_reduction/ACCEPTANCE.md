# Current PR #22 reproduction

This is the current entrypoint for shared sequential consistency and its specified
public-tag history reduction. It fixes the live reproduction link while leaving earlier
README commands and frozen results intact at their own historical source identities.

From repository root, in a Python environment with the pinned dependencies installed:

```sh
python -m pip install -r verification/sequential_consistency/requirements.txt
PYTHONDONTWRITEBYTECODE=1 python verification/history_reduction/acceptance.py --verify-retained
```

The default executes the new normal/optimized checks and all inherited strategic,
causal and history obligations. `--strategic`, `--causal` or `--history` selects a
workflow obligation. Only strategic/default mode needs SymPy. The receiver can also
be imported as `transfer_receiver.receive(source, target, warrant, epsilon='0')`.
`example_transfer.json` contains all three retained arguments; the receiving control
checks those retained bytes in a temporary deployment without any candidate producer.

The [theorem](../../foundations/BELLMAN_PUBLIC_TAG_HISTORY_REDUCTION.md) erases a
positive initial public tag from copies of an identical continuation game with an
invariant specified profile and assessment. It proves equality of all conditional
continuation values/gains, equality of the erased outcome law, and common consistency
in both directions. An explicitly supplied map is checked; no quotient search is
implemented. A supplied power witness restricts to one fixed tag across all models.
Target positivity and all target belief/incentive claims are independently received.

The main fixture has 127 -> 63 nodes, 40 -> 20 information sets and 160 -> 80 model/set
queries. Controls preserve profitable deviations and tolerance statuses, exercise
model-dependent positive tag probabilities and unequal perturbation coefficients,
and reject stale identities, invalid maps, altered premises and invalid transport.
The two substantive counterexamples concern public coordination and off-path
likelihoods. They refute broader shortcuts, not this conditional theorem.

Before any historical replay, `acceptance.py` compares all existing bytes with
`eb44e580fe137c50d9c92ea2b284cf0e5d3d90e9`, except the three living programme documents
and three workflow entrypoints listed in its source. New files have an explicit
allowlist. Mutated inherited evidence and unregistered release notes must be rejected.
The old acceptance then runs at that exact detached temporary snapshot, recursively
replaying its original strategic and merged causal/history sources. Changed earlier
mathematics would fail preservation rather than gain an inherited passing label.

`results.json` binds every new source, the retained example, living guidance and
workflow source to an exact commit, and records the fresh observations. It is excluded
from its own manifest to avoid circular hashing. The historical release manifests and
source identities are not expanded or overwritten; this extension has a separate
research note, not a GitHub release. The causal branch, Writ and Decision Lab are
outside this work.

This is analytical proof plus exact executable conformance evidence. It does not
claim external peer acceptance, Lean verification, empirical truth of the supplied
premises, preservation of all equilibria, or general strategic history compression.
