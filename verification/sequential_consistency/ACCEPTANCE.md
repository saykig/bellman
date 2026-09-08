# Current acceptance command

This additive orchestration entrypoint supersedes direct current-tree invocation of
the retained `run_checks.py`. The mathematical receiver and its retained evidence are
unchanged. See the [CI replay addendum](../../reviews/SEQUENTIAL_CREDIBILITY_CI_REPLAY_ADDENDUM.md).

From repository root, with the pinned dependencies installed:

```sh
PYTHONDONTWRITEBYTECODE=1 python verification/sequential_consistency/acceptance.py --verify-retained
```

The default runs all three modes. `--strategic`, `--causal` and `--history` select the
individual workflow obligations; each still performs current-tree preservation checks.
Only strategic mode requires SymPy. No inherited job reports success by merely
delegating or skipping its work.

Before replay, the entrypoint compares every file tracked at the retained strategic
head `af7a8fc67cb204b67474eb7749c76c414189a5d5` against today's bytes, except the three
explicitly changed workflow entrypoints. It accepts only the four named additive
acceptance files. It rejects changed mathematical source/evidence and unexpected
release notes; both refusals have mutation controls.
It also directly compares the current merged causal prerequisites against PR #20,
excluding only the three living programme documents and workflow entrypoints.

Strategic receiving runs at that exact head, including the older draft replay. Causal
and version-history acceptance run at exact merged PR #20
`cea4e1a47cb91c1f3917490350deab53d2976908`. The causal runner executes its full inherited
PR #19 -> #17 -> #16 -> #14 -> #12 -> #10 chain. Preserved source bytes justify using
these historical checks for the unchanged current mathematical components. Replay
does not purport to validate revised code: a revision would fail the preliminary
preservation check and require a new warrant.

All clones are temporary local detached snapshots; no remote branch is changed.
The six published version identities and two additional unpublished research-note
identities remain separate. No release/tag is created, no historical manifest is
expanded, and no frozen note is moved or overwritten to satisfy an old glob check.

`acceptance-results.json` binds the additive acceptance sources and observations to a
new commit. `results.json` and the original draft's evidence remain unchanged and
are received at their correct source identities.
