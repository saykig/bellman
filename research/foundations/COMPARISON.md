# Candidate comparison and scope decision

“Partial knowledge” may mean a constraint, an unnormalized likelihood, a known
marginal with missing dependence, or several possible mechanisms. Treating all
four as the same kind of information is the central avoidable mistake.

| Candidate | Objects and supported operations | Guarantee under its premises | What it does not supply |
|---|---|---|---|
| Relational information algebra | Sets of possible assignments; conjunction by natural join; forgetting by projection | Idempotent reuse; exact constraint elimination; contradiction is empty join | Probabilities, causal direction or intervention rules; projection can lose coupling |
| Probability valuation algebra | Scoped nonnegative factors; multiplication and sum elimination | Exact marginal computation for a supplied factorization; elimination respects distributivity | Permission to multiply arbitrary marginal reports or count repeated evidence twice; normalization is not idempotent |
| Local-to-global compatibility | Local relations/distributions with restriction maps; ask for global extensions | Explicit existence questions and witnesses/obstructions; join-tree gluing in the proved relational case | A unique global model, a canonical fusion operation, or causal interpretation of observation contexts |
| Compositional causal model | Typed variables, owned invariant mechanisms, directed wiring; kernel composition, parallel product and replacement | Single-regime intervention laws under causal and randomness assumptions; modular calculation | Automatic identification, hidden-noise coupling, arbitrary feedback, or a prior over unknown mechanisms |

The first two rows are related but should not be collapsed: repeating a logical
constraint adds nothing, while squaring a likelihood usually changes its meaning.
The third row describes a compatibility problem, not a competing universal
arithmetic. The fourth adds meaning to changes of mechanisms. None automatically
represents disputed empirical assumptions or makes a finite sample a population law.

Small separating examples are proved in [DEVELOPMENT](math/DEVELOPMENT.md):
nonuniform separator double-counting; cyclic equality/inequality obstruction;
nonempty join without preservation of every local possibility; observationally
equivalent models with different interventions; coupled flips whose independent
recombination gives a false uncertainty range. These examples discriminate
operations rather than merely display each formalism's notation.

Existing connections (source keys in [NOTES](sources/NOTES.md)):

- **AC/AB:** local compatibility and valuation theory already connect explicitly.
  No new bridge between them is needed for relational knowledge.
- **SS/F:** a causal DAG's numeric evaluation is a product-and-sum calculation,
  but erasing ownership and direction loses the semantics of intervention.
- **P/RW:** finite intervention models already have a precise established meaning.
  Wiring mechanisms and abstracting entire causal models are different uses of
  “compositional”; neither should be passed off as the other.
- **Our representation choice:** relations over whole mechanism choices encode
  uncertainty; causal evaluation maps each admissible realization to its query
  answers. The operations coexist without being the same algebraic operation.

Selected bounded setting: finite acyclic modules, finite catalogues of complete
normalized kernels, shared relational constraints on their choices, and hard
interventions at named owners. This admits exact search and separates knowledge
coupling from physical randomness. It is a smaller domain than Bellman's existing
response-type models with arbitrary latent dependence; it is not a replacement.

Why not select the alternatives for deeper work? Pure compatibility already has
an established bridge and does not address mechanism changes. A universal SCM
composition theorem would require unresolved choices about feedback, shared
noise, abstraction and counterfactuals. The selected setting makes the important
failure visible before adding that machinery. Its chief cost is the explicit
catalogue assumption; catalogue incompleteness remains a substantive limitation.
