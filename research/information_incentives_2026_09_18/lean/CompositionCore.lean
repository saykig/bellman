import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/- New narrow algebraic checks. These do not formalize probability semantics,
   entropy duality, Bayesian equilibrium, or historical novelty. -/
namespace InformationIncentives

theorem max_plus (a b c : ℝ) : max a b + c = max (a+c) (b+c) := by
  rcases le_total a b with h | h
  · rw [max_eq_right h, max_eq_right (show a+c ≤ b+c from by linarith)]
  · rw [max_eq_left h, max_eq_left (show b+c ≤ a+c from by linarith)]

theorem plus_max (a b c : ℝ) : a + max b c = max (a+b) (a+c) := by
  rcases le_total b c with h | h
  · rw [max_eq_right h, max_eq_right (show a+b ≤ a+c from by linarith)]
  · rw [max_eq_left h, max_eq_left (show a+c ≤ a+b from by linarith)]

/-- The six common-law affine branches, before optimizing over admissible laws. -/
theorem six_branch_reduction (p0 p1 p2 o : ℝ) :
    max (max p0 p1) p2 + max 0 o =
    max (max (max p0 (p0+o)) (max p1 (p1+o))) (max p2 (p2+o)) := by
  simp only [max_plus, plus_max, add_zero]
  ac_rfl

/-- G's sharp partial-certificate cost threshold, for all real mixed probabilities. -/
theorem certificate_threshold (k : ℝ) :
    (∃ q : ℝ, 0 ≤ q ∧ q ≤ 1 ∧ q-k ≤ (1:ℝ)/5 ∧ 1-q-k ≤ (1:ℝ)/5)
    ↔ (3:ℝ)/10 ≤ k := by
  constructor
  · rintro ⟨q, _, _, h1, h2⟩
    linarith
  · intro hk
    refine ⟨(1:ℝ)/2, by norm_num, by norm_num, ?_, ?_⟩ <;> linarith

/-- Each type can be separately deterred without cost. -/
theorem separate_deterrents :
    (∃ q : ℝ, 0 ≤ q ∧ q ≤ 1 ∧ q ≤ (1:ℝ)/5) ∧
    (∃ q : ℝ, 0 ≤ q ∧ q ≤ 1 ∧ 1-q ≤ (1:ℝ)/5) := by
  constructor
  · exact ⟨0, by norm_num, by norm_num, by norm_num⟩
  · exact ⟨1, by norm_num, by norm_num, by norm_num⟩

/-- But no common continuation can deter both at zero cost. -/
theorem no_common_zero_cost_deterrent :
    ¬ (∃ q : ℝ, 0 ≤ q ∧ q ≤ 1 ∧ q ≤ (1:ℝ)/5 ∧ 1-q ≤ (1:ℝ)/5) := by
  rintro ⟨q, _, _, h1, h2⟩
  linarith

#print axioms six_branch_reduction
#print axioms certificate_threshold
#print axioms separate_deterrents
#print axioms no_common_zero_cost_deterrent
end InformationIncentives
