import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

namespace JointFeasibility

/-- Two attained scalar fibre minima exactly answer a shared additive budget.
    Weights may be absorbed into c and d. Shared interfaces must already be fixed. -/
theorem scalar_profile {X Y A B : Type*} (f : X → A) (g : Y → B)
    (c : X → ℝ) (d : Y → ℝ) (a : A) (b : B) (j k budget : ℝ)
    (hx : ∃ x, f x = a ∧ c x = j) (hy : ∃ y, g y = b ∧ d y = k)
    (hj : ∀ x, f x = a → j ≤ c x) (hk : ∀ y, g y = b → k ≤ d y) :
    (∃ x y, f x = a ∧ g y = b ∧ c x + d y ≤ budget) ↔ j+k ≤ budget := by
  constructor
  · rintro ⟨x,y,hfx,hgy,hbudget⟩
    have h1 := hj x hfx
    have h2 := hk y hgy
    linarith
  · intro hbudget
    rcases hx with ⟨x,hfx,hcx⟩
    rcases hy with ⟨y,hgy,hdy⟩
    exact ⟨x,y,hfx,hgy,by rw [hcx,hdy]; exact hbudget⟩

def Upper {I : Type*} (K : (I → ℝ) → Prop) (b : I → ℝ) : Prop :=
  ∃ x, K x ∧ ∀ i, x i ≤ b i

/-- No convexity or closure is silently inserted. -/
theorem upper_sum {I : Type*} (K L : (I → ℝ) → Prop) (b : I → ℝ) :
    (∃ x y, K x ∧ L y ∧ ∀ i, x i+y i ≤ b i) ↔
    (∃ a c, Upper K a ∧ Upper L c ∧ ∀ i, a i+c i=b i) := by
  constructor
  · rintro ⟨x,y,hx,hy,hbound⟩
    refine ⟨x,(fun i => b i-x i),⟨x,hx,fun _ => le_rfl⟩,?_,?_⟩
    · refine ⟨y,hy,?_⟩
      intro i
      have hh := hbound i
      linarith
    · intro i
      ring
  · rintro ⟨a,c,⟨x,hx,hxa⟩,⟨y,hy,hyc⟩,hsum⟩
    refine ⟨x,y,hx,hy,?_⟩
    intro i
    have h1 := hxa i
    have h2 := hyc i
    have h3 := hsum i
    linarith

/-- All upper-threshold answers characterize the upper image exactly. -/
theorem upper_query_equivalence {I : Type*} (K L : (I → ℝ) → Prop) :
    (∀ b, Upper K b ↔ Upper L b) ↔ Upper K = Upper L := by
  constructor
  · intro h
    funext b
    exact propext (h b)
  · intro h b
    rw [h]

/-- Joint sender inequalities, with arbitrary real scale eta (the game assumes positivity). -/
theorem certificate_cost (eta v k : ℝ) :
    (∃ q : ℝ, 0 ≤ q ∧ q ≤ 1 ∧ eta*q-k ≤ v ∧ eta*(1-q)-k ≤ v)
      ↔ eta/2-v ≤ k := by
  constructor
  · rintro ⟨q,_,_,h1,h2⟩
    nlinarith
  · intro hk
    refine ⟨(1:ℝ)/2,by norm_num,by norm_num,?_,?_⟩ <;> nlinarith

/-- The inequality excluding C below the partial-certificate fine. -/
theorem exclude_C (b c e r : ℝ) (hc : 0 ≤ c) (hr : r ≤ 1)
    (he : e < b/2-c) : 0 < b/2-e+c*(1-r)/2-c*r := by
  nlinarith

/-- The unnormalized likelihood matrix of two independent sender trembles has rank ≤1. -/
theorem product_likelihood_determinant (a b c d : ℝ) :
    (a*c)*(b*d)-(a*d)*(b*c)=0 := by ring

#print axioms scalar_profile
#print axioms upper_sum
#print axioms upper_query_equivalence
#print axioms certificate_cost
#print axioms exclude_C
#print axioms product_likelihood_determinant
end JointFeasibility
