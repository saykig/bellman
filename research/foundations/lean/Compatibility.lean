/-
Relational core of DEVELOPMENT T1 (two bags) and T2.
No Mathlib, numerical oracle, axiom declaration, or sorry.
Predicates represent relations; existential quantification is projection.
-/
namespace Bellman

variable {A S B : Type}

def join (R : A → S → Prop) (T : S → B → Prop) : A → S → B → Prop :=
  fun a s b => R a s ∧ T s b

def leftProjection (G : A → S → B → Prop) (a : A) (s : S) : Prop :=
  ∃ b, G a s b

def rightProjection (G : A → S → B → Prop) (s : S) (b : B) : Prop :=
  ∃ a, G a s b

def Extends (G : A → S → B → Prop) (R : A → S → Prop)
    (T : S → B → Prop) : Prop :=
  (∀ a s, leftProjection G a s ↔ R a s) ∧
  (∀ s b, rightProjection G s b ↔ T s b)

-- T1 specialized to two overlapping bags, valid even for infinite types.
theorem extension_iff_join_exact (R : A → S → Prop) (T : S → B → Prop) :
    (∃ G, Extends G R T) ↔ Extends (join R T) R T := by
  constructor
  · intro ⟨G, hL, hR⟩
    constructor
    · intro a s
      constructor
      · intro ⟨b, hr, _⟩
        exact hr
      · intro hr
        obtain ⟨b, hg⟩ := (hL a s).mpr hr
        exact ⟨b, hr, (hR s b).mp ⟨a, hg⟩⟩
    · intro s b
      constructor
      · intro ⟨a, _, ht⟩
        exact ht
      · intro ht
        obtain ⟨a, hg⟩ := (hR s b).mpr ht
        exact ⟨a, (hL a s).mp ⟨b, hg⟩, ht⟩
  · intro h
    exact ⟨join R T, h⟩

-- T2: matching possible separator values implies exact two-bag gluing.
theorem overlap_implies_exact (R : A → S → Prop) (T : S → B → Prop)
    (overlap : ∀ s, (∃ a, R a s) ↔ (∃ b, T s b)) :
    Extends (join R T) R T := by
  constructor
  · intro a s
    constructor
    · intro ⟨b, hr, _⟩
      exact hr
    · intro hr
      obtain ⟨b, ht⟩ := (overlap s).mp ⟨a, hr⟩
      exact ⟨b, hr, ht⟩
  · intro s b
    constructor
    · intro ⟨a, _, ht⟩
      exact ht
    · intro ht
      obtain ⟨a, hr⟩ := (overlap s).mpr ⟨b, ht⟩
      exact ⟨a, hr, ht⟩

-- The parity obstruction X1 is independent of finiteness.
theorem equality_cycle_impossible {α : Type} (a b c : α)
    (ab : a = b) (bc : b = c) (ac : a ≠ c) : False :=
  ac (ab.trans bc)

-- T4's model-set inclusion; projection need not preserve dependence.
theorem relation_in_rectangle (C : A → B → Prop) (a : A) (b : B)
    (h : C a b) : (∃ b', C a b') ∧ (∃ a', C a' b) :=
  ⟨⟨b, h⟩, ⟨a, h⟩⟩

-- T3(b)'s ownership/replacement identity, for arbitrary factor values K.
-- This checks assembly, not stochastic normalization or DAG validity.
def assemble {L R K : Type} (f : L → K) (g : R → K) : Sum L R → K
  | .inl l => f l
  | .inr r => g r

def replace {I K : Type} (f : I → K) (updates : I → Option K) : I → K :=
  fun i => match updates i with
    | none => f i
    | some k => k

theorem replacement_commutes_with_ownership {L R K : Type}
    (f : L → K) (g : R → K) (u : L → Option K) (v : R → Option K) :
    replace (assemble f g) (assemble u v) =
      assemble (replace f u) (replace g v) := by
  funext i
  cases i with
  | inl l => rfl
  | inr r => rfl

#print axioms extension_iff_join_exact
#print axioms overlap_implies_exact
#print axioms equality_cycle_impossible
#print axioms relation_in_rectangle
#print axioms replacement_commutes_with_ownership
end Bellman
