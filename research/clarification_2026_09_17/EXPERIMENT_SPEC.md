# Selected next experiment: revision-aware observational completeness

Status: fully specified, runner prepared but NOT executed in this clarification
run. This is one finite test of a research direction, not a launch of the broader
programme. Run later with `python3 research/clarification_2026_09_17/next_experiment.py --run`.

## Question and attainable claim

Which distinctions between partial-knowledge records must survive to reproduce
all declared causal answers after addition, named withdrawal and replacement?
Test whether a source-sensitive operation-stable partition is an exact answer
state, and how much of the complete record it needs. Existence and partition
stability are established theory; the useful output is an explicit instantiation,
its distinguishing revision traces and honest cost, not a new existence theorem.

## Exact finite subject

Eight original models θ=(a,b,c)∈{0,1}³. External input X is a bit. Module M owns
Y=X xor a. Module N owns Z=Y xor b and receives M's one shared output Y. An
independent module owns W=c. No physical random variables, hidden shared noise,
causal discovery, statistical learning or sampling error occur in this test.
Unknown a,b,c are epistemic choices, not randomly reselected settings.

Five immutable source predicates, bound to the original revision:
`coupled`: a=b; `a0`: a=0; `w0`: c=0; `other_a0`: a=0;
`opposite`: a≠b. `a0` and `other_a0` are independently revocable WARRANTS with
the same mathematical content, not two independent data points. A copy of the
same source retains its original key. Provenance tells which case applies.

A state e=(A,v) has A a subset of the five labels and v∈{original,0,1}.
Mode original uses b; mode 0 or 1 physically replaces N's mechanism by Z=Y xor v.
There are 32·3=96 reference records. Original constraints remain about original
θ; no historical constraint is relabelled as an assertion about the replacement.

Queries: jointly attainable tuples

    (Z at X=0, Z at X=1, Z under do(Y=0), Z under do(Y=1), W).

The do operation is a query-specific replacement of M's Y mechanism at its owner;
it does not change A or permanently replace N. The returned tuple contains
single-regime answers of the same model, not a cross-world probability coupling.
Also record inconsistency (empty family). Only Z and W are observed; Y is an
explicitly authorized intervention target. Output-only postprocessing is covered
by equality of complete external output behavior and is not the challenge.

## Allowed operations

For each source key j, add_j and drop_j change membership of A; repeated add is
idempotent and dropping an absent key is a no-op. For b=0,1, replace_N_b changes
v to b and leaves A unchanged. Replacing a hypothesis is drop_old followed by
add_new if both predicates are in the fixed registry. Merging any fixed peer
source subset is composition of additions. Cross-version data joining, arbitrary
new source predicates, new graphs, new interventions and source reliability
updates are unsupported, not silently approximated.

## Reference and retained candidates

Reference: enumerate original θ satisfying every active predicate, then apply v
and evaluate each query by its structural equations. Keep this full labelled
baseline permanently. Compare three PARTITIONS of the 96 records:

1. equal current answer set (`answer_only`);
2. equal current complete model family (`family_only`);
3. the coarsest partition refining equal observations and stable under every
   allowed transition (`operation_stable`).

A partition induces the sound set-of-records saturation described in TRANSLATION.
Refine candidate 3 by repeatedly splitting each block by the vector of successor
block identifiers, until stable. This finite construction terminates in at most
95 strict refinement rounds. It is not a search over all arbitrary abstractions.
Check stability independently after construction. For failed candidates, use
breadth-first search on record pairs to return the shortest separating operation
trace for the reported initial pair and its two final observations. This is not
a globally shortest witness across all initial pairs. A zero-length witness diagnoses loss of
current observations; positive-length witnesses diagnose future-operation loss.

## Candidate property and useful-content requirements

Property: every record and every finite permitted operation sequence have the
same final observation through the quotient as through full reference execution.
A stable partition with observation-homogeneous blocks suffices by induction;
this written argument is available now. The runner checks its hypotheses, not
infinitely many traces. A nontrivial quotient is desirable, not required for
correctness and not presumed to exist with all permissions.

Soundness without exactness may be useful later, but report lost conclusions
explicitly. Reject an indiscriminate “unknown” abstraction as a success: it must
recover the jointly established do(Y=1) answer, preserve W=0 after unrelated
revision, detect `coupled`+`opposite` conflict, and keep unsupported distinct from
negation-supported. Report output-block counts and member records; these are
semantic distinctions, not a compression benchmark for practical databases.

Positive trace: add coupled, a0, w0; infer do(Y=1) gives Z=1. Drop a0: that answer
becomes unresolved while Z=X and W=0 remain. Replace N with flip 1 while a0 is
active: Z=1−X, W=0. Alternative support: with other_a0 also active, dropping a0
must NOT invalidate the first intervention answer. These probes have already run.

Failure: {a0} and {a0,other_a0} have equal current model families but differ after
drop_a0. A source-free state cannot be exact for this operation. One stored proof
of a claim also fails to account for another surviving proof. Mechanism revision
must check version-specific entailment rather than keep an old support blindly.

## Outcomes and stopping rules

- If the quotient passes and preserves useful answers with fewer states, retain
  a worked synthesis of causal semantics, assumption environments and operation-
  relative completeness. Do not market it as a new foundation theorem.
- If it approaches identity, report that the permission menu makes most source
  distinctions necessary. Keep the explicit ledger; do not weaken the menu just
  to obtain attractive compression.
- If failures reflect missing revision/source meaning, repair the concrete
  semantics before any optimization. If labels alone drive the issue, ATMS plus
  exact causal evaluation may already suffice; make that the recommendation.
- If the small exact reference is already adequate, stop. A larger follow-up
  needs a concrete obstacle: e.g. newly admitted post-replacement evidence,
  dependency-preserving stochastic factorization, or cost of exact model sets.
  A new grid alone is not such an obstacle.

No subsequent programme, Lean work, publication, or architecture change is
implicitly authorized by preparing this specification.
