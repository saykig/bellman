# Public-tag history reduction preserving incentives and consistency

8 September 2026. Additive component on PR #22, based on reviewed head
`eb44e580fe137c50d9c92ea2b284cf0e5d3d90e9`. Earlier mathematical editions and their
source-bound evidence remain unchanged. This is an ordinary finite proof with exact
reference checks, not formal verification or a claim of mathematical novelty.

## 1. A specific history reduction

Let G be a supplied finite perfect-recall game family from the assessed-credibility
and shared-consistency interfaces. Construct a larger game H by a root chance move
Z in a finite tag set (at least two), with rho_m(z)>0 in every model. Both players
observe and remember Z. After tag z, H has a copy G_z of the entire G tree.

The reduction erases that initial public tag and maps each copied history to its
history in G. This removes a chance node and merges multiple copies of every later
node/information set. It is a many-to-one reduction, not merely a renaming.

The input supplies explicit node and information-set bijections from EACH copied
subtree to G. No names are interpreted as mathematical identity. The receiving
conditions are:

1. The source root is chance and its branches partition all other source nodes.
   Within each tag subtree the node map is a tree isomorphism to G, preserving
   roots, player/chance/terminal roles, action labels, and acting players.
2. Each tag has a bijection of its information sets to G's sets. Different tag
   subtrees share no information set: players know the tag. Both complete subjects
   independently satisfy perfect recall and the inherited interface constraints.
3. Models have the same identities. Every copied conditional chance law and terminal
   utility agrees exactly with G. Root tag probabilities may vary across models but
   remain strictly positive. Thus, conditional on a tag, the continuation game is G.
4. The supplied source profile is the same target profile in every copy. The source
   assessment in each copy is the target assessment pulled back through the node map.
   These are conditions on a SPECIFIED assessment, not on every possible strategy.

A failure of these sufficient conditions is `unsupported-reduction`, not proof that
no other reduction could work. This profile does not cover intermediate/private
signals, payoff approximation, endogenous public announcements, arbitrary history
quotients, unobserved tags or changing intervention semantics.

## 2. Exact continuation-value and deviation theorem

For each player i, tag z and target information set I of i, write I_z for its copy.
Every permitted pure continuation plan below I_z corresponds bijectively to a pure
continuation plan below I, by information-set relabelling. The entire source game has
additional tag-contingent global strategies, so there is no claimed bijection between
ALL global source and target strategies. The bijection is local to a queried I_z.

**Theorem 1.** Under conditions 1–4, for each m,I,z and every corresponding continuation
plan tau, the conditional expected utilities in H at I_z and G at I agree. The
proposed-profile values and maximal continuation gains also agree. Consequently
D*_H = D*_G for the common finite model family.

**Proof.** Starting at I_z fixes the known tag. The assessed starting-node masses
agree through the map. Every complete suffix has the same player action probabilities,
fixed conditional chance factors and terminal utility as its image. A finite sum over
suffixes therefore gives equal conditional utilities. The copied information partition
preserves all legal continuation assignments in both directions, so maxima over pure
plans agree. The inherited finite-mixture argument extends the bound to the supported
randomized continuations. Every source information set is a copy of a target set;
taking the maximum over models and information sets gives equality of D*. QED.

For the supplied invariant profile, the ex-ante utility of H is
sum_z rho_m(z) U_m(G)=U_m(G). The law of the ERASED terminal history also agrees.
This is not equality of the raw terminal history laws, which still include the tag.
No root-average utility equality alone is accepted as a substitute for conditions 1–4.

## 3. Shared consistency is preserved in both directions

**Theorem 2.** For the specified assessments satisfying conditions 1–4, existence of
one common completely mixed consistency sequence for G across all supplied models
is equivalent to existence of one for H. This is a statement about the given
assessment, not a characterization of all equilibria of the two games.

**Forward proof.** Copy each completely mixed profile sigma_t in G into every tag
subtree. It is a legal common profile in H, converging to the supplied invariant
profile. For h in I and its copy h_z,

    P^H_m,t(h_z) = rho_m(z) P^G_m,t(h),
    P^H_m,t(I_z) = rho_m(z) P^G_m,t(I).

The strictly positive root factor cancels in Bayes' rule, for every positive t, not
only asymptotically. Thus every copied posterior has the target limit. The same
sequence works across models. Fixed structural zeros in the continuation are handled
by the inherited restriction that each assessed information set be chance-reachable.

**Reverse proof.** Choose one fixed representative tag z0, the same across models.
Restrict a common source sequence to that copied subtree and use the information-set
bijection to obtain a common target sequence. Complete mixing and convergence survive
restriction. The same cancellation proves the target posterior limits. Source profiles
along the perturbation sequence may differ between tag copies; that does not invalidate
restriction to a fixed positive-probability tag. QED.

**Given power-witness corollary.** A supplied target rational power witness lifts by
copying its coefficients and orders. Conversely, a supplied source witness restricts
to the representative tag. Its coefficients and orders remain within the same domain.
The normalization polynomial at each retained information set is unchanged. Source
witness terms need not coincide across copies, provided the supplied source witness
has itself passed shared-consistency receiving. The target positivity radius is freshly
computed: removing other copies can increase the admissible radius.

**Sequential-equilibrium corollary.** Combine Theorems 1–2 with the accepted PR #22
consistency and full-continuation criteria on the identical mapped subjects. At epsilon
zero, modelwise sequential equilibrium with shared consistency transfers in both
directions for this assessment class. At positive epsilon, the same continuation-gain
bound transfers without an exact-equilibrium label. No ambiguity-preference equilibrium,
causal identification or empirical credibility is inferred.

## 4. Two decisive reasons not to generalize the theorem

### Public randomization can coordinate even when payoffs ignore the tag

In a two-player matching game, each chooses L or R and receives 1 for matching, 0
otherwise. The second player does not observe the first action. Add an independent
fair public tag. Both choose L after tag 0 and R after tag 1. This is a source
sequential equilibrium with matching probability 1 and erased outcome law
(LL,RR)=(1/2,1/2). Replacing both players by their marginal half-mixed strategies after
erasure gives matching probability 1/2. Independent target behavior cannot reproduce
the original correlated outcome law: P(LR)=P(RL)=0 together with P(LL)=P(RR)=1/2
has no product-distribution solution. The supplied profile/assessment is not invariant
across tag copies, violating condition 4. The reference rejects that erasure.

This is the familiar strategic role of correlation, not a new impossibility theorem;
see Aumann (1974), *Subjectivity and Correlation in Randomized Strategies*, https://doi.org/10.1016/0304-4068(74)90037-8 . The elementary counterexample
above is fully derived and checked here rather than imported through a solver.

### Root payoff agreement does not preserve off-path likelihood restrictions

Use the earlier exit/entry game: A privately knows g/b, gets 1 for exit and 0 for
entry; B sees entry and has one action and zero payoff. In the target, prior(g)=1/2,
A exits at both types, and B's assessed posterior after entry is 1/2. A unit-rate
witness works. Add two equally likely public tags, but set conditional prior(g) to
3/4 in H and 1/4 in L. The marginal prior is still 1/2 and all proposed root utilities
and continuation incentive maxima remain the same.

In the H copy use entry coefficients (c_g,c_b)=(1,3), and in the L copy use (3,1),
all order one. Both tag-conditional entry posteriors tend to 1/2, so the source
witness is valid. Erasing the tag while restricting the H witness to the target
instead yields posterior (1/2)/(1/2+3/2)=1/4. The target still passes incentive
checking but this restricted witness fails consistency. Condition 3 fails: copied
conditional chance laws are different. Other target witnesses can work; this is a
counterexample to unwarranted witness TRANSPORT, not to target equilibrium existence.

## 5. Established reuse and implementation boundary

The proof specializes exact conditional game isomorphism and Bayes-factor cancellation.
It earns a narrow case of the earlier deviation-covering value-preservation obligation,
plus a consistency obligation that a root value bound alone does not give. Relevant
wider abstraction work includes Kroer and Sandholm's
https://www.cs.cmu.edu/~sandholm/extensiveGameAbstraction.ec14.pdf and
https://papers.nips.cc/paper_files/paper/2018/hash/aa942ab2bfa6ebda4840e7360ce6e7ef-Abstract.html .
Those broader error results are not claimed as a proof of arbitrary assessment transport.
The construction uses the already accepted shared-power witness theorem and independent
SymPy receiver; no new polynomial engine, game solver or language is introduced.

The reference checks an explicitly supplied source, target and reduction map. It
verifies structure and assessment identities, receives source and target consistency
warrants independently with all three candidate producers absent in a control, checks
that the target witness is exactly the representative restriction, and compares all
corresponding continuation values/gains and root expected utilities. Its candidate
constructor reuses existing producers. Independent target receiving is intentionally
retained even though the analytic theorem licenses transport.

The integrated source has two public copies of the 63-node evidence/bond game: 127
nodes and 40 information sets. Erasure gives 63 nodes and 20 information sets, with
four models and query counts 160 -> 80. Model-dependent positive tag probabilities
are included. Negative controls target structure, chance laws, profile invariance,
assessment consistency, witness restriction, missing deviations and stale identities.

The statement is finite but not mathematically capped at two tags or this fixture;
implementation retains the inherited node/depth/continuation limits and 2–4 tags.
No general quotient search, intermediate history reduction or approximate consistency
transfer is earned. A later reduction should relax a concrete restrictive premise
only when there is a specified use and a proof or counterexample.
