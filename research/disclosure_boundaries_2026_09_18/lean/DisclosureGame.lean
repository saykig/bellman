import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Topology.Instances.Real.Lemmas
import Mathlib.Tactic.FunProp

namespace DisclosureGame
noncomputable section

inductive Action | A | B | C deriving DecidableEq
inductive State | one | two | three deriving DecidableEq

/-- A probability distribution on the three named actions (or states in order). -/
structure Mix where
  a : ℝ
  b : ℝ
  c : ℝ
  ha : 0 ≤ a
  hb : 0 ≤ b
  hc : 0 ≤ c
  total : a+b+c=1

structure Values where
  a : ℝ
  b : ℝ
  c : ℝ

def pureA : Mix := ⟨1,0,0,by norm_num,by norm_num,by norm_num,by norm_num⟩
def pureB : Mix := ⟨0,1,0,by norm_num,by norm_num,by norm_num,by norm_num⟩
def pureC : Mix := ⟨0,0,1,by norm_num,by norm_num,by norm_num,by norm_num⟩
def half : Mix := ⟨1/2,1/2,0,by norm_num,by norm_num,by norm_num,by norm_num⟩

def dot (x : Mix) (u : Values) : ℝ := x.a*u.a+x.b*u.b+x.c*u.c

def preferred (player : Bool) : State → Action
  | .one => if player then .B else .A
  | .two => if player then .A else .B
  | .three => .C

/-- Pure policy payoff: coordination, state preference, and a fine for non-C. -/
def utility (b c e : ℝ) (player : Bool) (θ : State) (own other : Action) : ℝ :=
  (if own=other then c else 0)+(if own=preferred player θ then b else 0)
    -(if own=Action.C then 0 else e)

def against (b c e : ℝ) (player : Bool) (θ : State) (own : Action) (q : Mix) : ℝ :=
  q.a*utility b c e player θ own .A + q.b*utility b c e player θ own .B
    + q.c*utility b c e player θ own .C

def expected (b c e : ℝ) (player : Bool) (p q : Mix) (own : Action) : ℝ :=
  p.a*against b c e player .one own q + p.b*against b c e player .two own q
    + p.c*against b c e player .three own q

def values (b c e : ℝ) (player : Bool) (p q : Mix) : Values :=
  ⟨c*q.a+b*(if player then p.b else p.a)-e,
   c*q.b+b*(if player then p.a else p.b)-e,
   c*q.c+b*p.c⟩

/-- The short expected-payoff formulas follow from the pure game and normalization. -/
theorem expected_formula (b c e : ℝ) (player : Bool) (p q : Mix) (own : Action) :
    expected b c e player p q own =
      (match own with
       | .A => (values b c e player p q).a
       | .B => (values b c e player p q).b
       | .C => (values b c e player p q).c) := by
  have hp : p.c=1-p.a-p.b := by linarith [p.total]
  have hq : q.c=1-q.a-q.b := by linarith [q.total]
  cases player <;> cases own <;>
    simp [expected,against,utility,preferred,values] <;> rw [hp,hq] <;> ring

/-- No profitable pure deviation; mixed deviations are derived below. -/
def BR (x : Mix) (u : Values) : Prop :=
  u.a ≤ dot x u ∧ u.b ≤ dot x u ∧ u.c ≤ dot x u

theorem br_all_mixed (x y : Mix) (u : Values) (h : BR x u) : dot y u ≤ dot x u := by
  rcases h with ⟨ha,hb,hc⟩
  have h1 := mul_nonneg y.ha (sub_nonneg.mpr ha)
  have h2 := mul_nonneg y.hb (sub_nonneg.mpr hb)
  have h3 := mul_nonneg y.hc (sub_nonneg.mpr hc)
  have hy := y.total
  have hid : y.a*(dot x u-u.a)+y.b*(dot x u-u.b)+y.c*(dot x u-u.c)
      = dot x u-dot y u := by
    calc
      _ = (y.a+y.b+y.c)*dot x u-dot y u := by unfold dot; ring
      _ = _ := by rw [hy]; ring
  linarith

def Nash (b c e : ℝ) (p x y : Mix) : Prop :=
  BR x (values b c e false p y) ∧ BR y (values b c e true p x)

/-- A best-response mixture cannot put positive weight on an action strictly
    below the average payoff of two available alternatives. -/
theorem zero_C (x : Mix) (u : Values) (h : BR x u)
    (hbetter : 2*u.c < u.a+u.b) : x.c=0 := by
  rcases h with ⟨ha,hb,hc⟩
  have h1 := mul_nonneg x.ha (sub_nonneg.mpr ha)
  have h2 := mul_nonneg x.hb (sub_nonneg.mpr hb)
  have hid : x.a*(dot x u-u.a)+x.b*(dot x u-u.b)+x.c*(dot x u-u.c)=0 := by
    have ht := x.total
    calc
      _ = (x.a+x.b+x.c)*dot x u-dot x u := by unfold dot; ring
      _ = 0 := by rw [ht]; ring
  have hstrict : 0 < dot x u-u.c := by linarith
  have hnonpos : x.c*(dot x u-u.c) ≤ 0 := by linarith
  have hle : x.c ≤ 0 := by nlinarith
  exact le_antisymm hle x.hc

theorem no_C_after_certificate (b c e : ℝ) (hc : 0 ≤ c)
    (he : e < b/2-c) (p x y : Mix) (hp : p.c=0) (hn : Nash b c e p x y) :
    x.c=0 := by
  have ht := p.total
  have hy := y.total
  have hyc : y.c ≤ 1 := by linarith [y.ha,y.hb]
  apply zero_C x (values b c e false p y) hn.1
  simp only [values, Bool.false_eq_true, ↓reduceIte]
  rw [hp]
  rw [hp] at ht
  have hp_mul := congrArg (fun z : ℝ => b*z) ht
  have hy_mul := congrArg (fun z : ℝ => c*z) hy
  nlinarith [mul_nonneg hc (sub_nonneg.mpr hyc)]

def senderOne (η v : ℝ) (x : Mix) : ℝ := η*x.a+v*x.c
def senderTwo (η v : ℝ) (x : Mix) : ℝ := η*x.b+v*x.c

/-- Algebraic receiver/IC conditions for silence and E12. This predicate alone
    DOES NOT encode prior support and must not be interpreted as a PBE at arbitrary
    priors. The FixedInformationPBE wrapper below supplies the full-support premise. -/
def AlgebraicPooling (b c e η v k : ℝ) (prior : Mix) : Prop :=
  Nash b c e prior pureC pureC ∧
  ∃ p x y : Mix, p.c=0 ∧ Nash b c e p x y ∧
    senderOne η v x-k ≤ v ∧ senderTwo η v x-k ≤ v

/-- The previously checked threshold now follows from best responses in the game. -/
theorem low_fine_necessity (b c e η v k : ℝ) (hc : 0 ≤ c)
    (he : e < b/2-c) (prior : Mix) (h : AlgebraicPooling b c e η v k prior) :
    η/2-v ≤ k := by
  rcases h.2 with ⟨p,x,y,hp,hn,h1,h2⟩
  have hzero := no_C_after_certificate b c e hc he p x y hp hn
  have ht := x.total
  unfold senderOne at h1
  unfold senderTwo at h2
  rw [hzero] at h1 h2 ht
  nlinarith [congrArg (fun z : ℝ => η*z) ht]

/-- Explicit symmetric mixed equilibrium after E12 at low enforcement. -/
theorem half_nash (b c e : ℝ) (hc : 0 ≤ c) (he : e < b/2-c) :
    Nash b c e half half half := by
  dsimp [Nash,BR,values,dot,half]
  repeat' apply And.intro
  all_goals nlinarith

/-- At the higher fine the target itself is a credible continuation. -/
theorem target_nash_after_certificate (b c e : ℝ) (he : b/2-c ≤ e) :
    Nash b c e half pureC pureC := by
  dsimp [Nash,BR,values,dot,half,pureC]
  repeat' apply And.intro
  all_goals nlinarith

def OnPath (b c e : ℝ) (p : Mix) : Prop :=
  b*p.a-e ≤ c+b*p.c ∧ b*p.b-e ≤ c+b*p.c

theorem on_path_from_game (b c e : ℝ) (p : Mix) :
    Nash b c e p pureC pureC ↔ OnPath b c e p := by
  simp [Nash,BR,values,dot,pureC,OnPath]
  intro h1 h2
  exact ⟨h2,h1⟩

/-- Complete fixed-information policy-pooling characterization, derived from
    pure utilities, receiver deviations, and the two sender payoff functions. -/
theorem pooling_iff (b c e η v k : ℝ) (hc : 0 ≤ c) (hk : 0 ≤ k) (prior : Mix) :
    AlgebraicPooling b c e η v k prior ↔
      OnPath b c e prior ∧ (b/2-c ≤ e ∨ η/2-v ≤ k) := by
  constructor
  · intro h
    refine ⟨(on_path_from_game b c e prior).mp h.1,?_⟩
    by_cases he : b/2-c ≤ e
    · exact Or.inl he
    · exact Or.inr (low_fine_necessity b c e η v k hc (lt_of_not_ge he) prior h)
  · rintro ⟨hon,hcut⟩
    refine ⟨(on_path_from_game b c e prior).mpr hon,?_⟩
    by_cases he : b/2-c ≤ e
    · refine ⟨half,pureC,pureC,by rfl,target_nash_after_certificate b c e he,?_,?_⟩
      · dsimp [senderOne,pureC]; linarith
      · dsimp [senderTwo,pureC]; linarith
    · have he' : e < b/2-c := lt_of_not_ge he
      have hcost : η/2-v ≤ k := hcut.resolve_left he
      refine ⟨half,half,half,by rfl,half_nash b c e hc he',?_,?_⟩
      · dsimp [senderOne,half]; linarith
      · dsimp [senderTwo,half]; linarith

/-- The boundary certificate belief is not an unsupported punishment:
    positive eligible prior masses can yield the equal posterior by trembles. -/
theorem equal_posterior_tremble (p1 p2 ε : ℝ) (h1 : 0 < p1) (h2 : 0 < p2)
    (hε : 0 < ε) (hε1 : ε ≤ 2*p1) (hε2 : ε ≤ 2*p2) :
    0 < ε/(2*p1) ∧ ε/(2*p1) ≤ 1 ∧
    0 < ε/(2*p2) ∧ ε/(2*p2) ≤ 1 ∧
    p1*(ε/(2*p1))/(p1*(ε/(2*p1))+p2*(ε/(2*p2)))=1/2 := by
  have h1' : 0 < 2*p1 := by linarith
  have h2' : 0 < 2*p2 := by linarith
  refine ⟨div_pos hε h1',(div_le_one h1').mpr hε1,
          div_pos hε h2',(div_le_one h2').mpr hε2,?_⟩
  have ha : p1*(ε/(2*p1))=ε/2 := by field_simp
  have hb : p2*(ε/(2*p2))=ε/2 := by field_simp
  rw [ha,hb]
  field_simp
  ring

/-- Source-state marginal probability of a positive operational outcome. -/
def sourceMatch (s : ℝ) (y : Bool) : ℝ := if y then s else 1-s

def opUtility (L w s : ℝ) (own other : Bool) : ℝ :=
  (if own=other then L else 0)+w*sourceMatch s own

def OpBR (L w s : ℝ) (y : Bool) : Prop :=
  ∀ z : Bool, opUtility L w s z y ≤ opUtility L w s y y

/-- After a certificate a common source-majority action is always an equilibrium. -/
theorem operational_exists (L w s : ℝ) (hL : 0 ≤ L) (hw : 0 ≤ w) :
    ∃ y : Bool, OpBR L w s y := by
  by_cases hs : 1/2 ≤ s
  · refine ⟨true,?_⟩
    intro z
    cases z <;> simp [opUtility,sourceMatch]
    all_goals nlinarith
  · refine ⟨false,?_⟩
    intro z
    cases z <;> simp [opUtility,sourceMatch]
    all_goals nlinarith

/-- All mixed policy deviations and either operational action. -/
def JointBR (x : Mix) (u : Values) (L w s : ℝ) (target : Bool) : Prop :=
  ∀ y : Mix, ∀ z : Bool,
    dot y u+opUtility L w s z target ≤ dot x u+opUtility L w s target target

theorem joint_br_iff (x : Mix) (u : Values) (L w s : ℝ) (target : Bool) :
    JointBR x u L w s target ↔ BR x u ∧ OpBR L w s target := by
  constructor
  · intro h
    have ha := h pureA target
    have hb := h pureB target
    have hc := h pureC target
    simp only [dot,pureA,pureB,pureC,one_mul,zero_mul,zero_add,add_zero] at ha hb hc
    refine ⟨⟨by dsimp [dot]; linarith,by dsimp [dot]; linarith,by dsimp [dot]; linarith⟩,?_⟩
    intro z
    have hz := h x z
    linarith
  · rintro ⟨hpol,hop⟩ y z
    have h1 := br_all_mixed x y u hpol
    have h2 := hop z
    linarith

/-- source records P(S=positive | state); the advocate sees only the state,
    so evidence changes its weights p, not these conditional source probabilities. -/
def FullNash (b c e L w : ℝ) (source : Values) (p x y : Mix) (op : Bool) : Prop :=
  JointBR x (values b c e false p y) L w (dot p source) op ∧
  JointBR y (values b c e true p x) L w (dot p source) op

theorem full_nash_iff (b c e L w : ℝ) (source : Values) (p x y : Mix) (op : Bool) :
    FullNash b c e L w source p x y op ↔
      Nash b c e p x y ∧ OpBR L w (dot p source) op := by
  unfold FullNash Nash
  rw [joint_br_iff,joint_br_iff]
  constructor
  · rintro ⟨⟨h1,ho⟩,⟨h2,_⟩⟩
    exact ⟨⟨h1,h2⟩,ho⟩
  · rintro ⟨⟨h1,h2⟩,ho⟩
    exact ⟨⟨h1,ho⟩,⟨h2,ho⟩⟩

def SourceValid (source : Values) : Prop :=
  0 ≤ source.a ∧ source.a ≤ 1 ∧ 0 ≤ source.b ∧ source.b ≤ 1 ∧
    0 ≤ source.c ∧ source.c ≤ 1

theorem source_marginal_valid (p : Mix) (s : Values) (hs : SourceValid s) :
    0 ≤ dot p s ∧ dot p s ≤ 1 := by
  rcases hs with ⟨ha,ha1,hb,hb1,hc,hc1⟩
  have h1 := mul_nonneg p.ha ha
  have h2 := mul_nonneg p.hb hb
  have h3 := mul_nonneg p.hc hc
  have h4 := mul_nonneg p.ha (sub_nonneg.mpr ha1)
  have h5 := mul_nonneg p.hb (sub_nonneg.mpr hb1)
  have h6 := mul_nonneg p.hc (sub_nonneg.mpr hc1)
  have ht := p.total
  dsimp [dot]
  constructor <;> nlinarith

def FullAlgebraicPooling (b c e η v k L w : ℝ) (source : Values)
    (prior : Mix) (target : Bool) : Prop :=
  FullNash b c e L w source prior pureC pureC target ∧
  ∃ p x y : Mix, ∃ op : Bool, p.c=0 ∧ FullNash b c e L w source p x y op ∧
    senderOne η v x-k ≤ v ∧ senderTwo η v x-k ≤ v

theorem full_pooling_iff_policy (b c e η v k L w : ℝ) (source : Values)
    (prior : Mix) (target : Bool) (hL : 0 ≤ L) (hw : 0 ≤ w) :
    FullAlgebraicPooling b c e η v k L w source prior target ↔
      AlgebraicPooling b c e η v k prior ∧ OpBR L w (dot prior source) target := by
  constructor
  · rintro ⟨hon,⟨p,x,y,op,hp,hn,h1,h2⟩⟩
    have h0 := (full_nash_iff b c e L w source prior pureC pureC target).mp hon
    have hcont := (full_nash_iff b c e L w source p x y op).mp hn
    exact ⟨⟨h0.1,⟨p,x,y,hp,hcont.1,h1,h2⟩⟩,h0.2⟩
  · rintro ⟨⟨hon,⟨p,x,y,hp,hn,h1,h2⟩⟩,hop⟩
    rcases operational_exists L w (dot p source) hL hw with ⟨op,ho⟩
    exact ⟨(full_nash_iff b c e L w source prior pureC pureC target).mpr ⟨hon,hop⟩,
      ⟨p,x,y,op,hp,(full_nash_iff b c e L w source p x y op).mpr ⟨hn,ho⟩,h1,h2⟩⟩

def FullSupport (p : Mix) : Prop := 0 < p.a ∧ 0 < p.b ∧ 0 < p.c

def SupportConsistent (prior posterior : Mix) : Prop :=
  (0 < posterior.a → 0 < prior.a) ∧
  (0 < posterior.b → 0 < prior.b) ∧
  (0 < posterior.c → 0 < prior.c)

theorem full_support_allows (prior posterior : Mix) (h : FullSupport prior) :
    SupportConsistent prior posterior :=
  ⟨fun _ => h.1,fun _ => h.2.1,fun _ => h.2.2⟩

/-- Actual fixed-information game interpretation: positivity is explicitly part
    of this predicate, preventing reuse at histories where an eligible type is
    impossible. The algebraic criterion is intentionally separate. -/
def FixedInformationPBE (b c e η v k L w : ℝ) (source : Values)
    (prior : Mix) (target : Bool) : Prop :=
  FullSupport prior ∧ SourceValid source ∧
    FullAlgebraicPooling b c e η v k L w source prior target

theorem fixed_information_pbe_iff (b c e η v k L w : ℝ) (source : Values)
    (prior : Mix) (target : Bool) (hc : 0 ≤ c) (hk : 0 ≤ k)
    (hL : 0 ≤ L) (hw : 0 ≤ w) :
    FixedInformationPBE b c e η v k L w source prior target ↔
      FullSupport prior ∧ SourceValid source ∧ OnPath b c e prior ∧
      (b/2-c ≤ e ∨ η/2-v ≤ k) ∧ OpBR L w (dot prior source) target := by
  unfold FixedInformationPBE
  rw [full_pooling_iff_policy b c e η v k L w source prior target hL hw,
      pooling_iff b c e η v k hc hk prior]
  constructor
  · rintro ⟨hf,hs,⟨⟨hon,hcut⟩,hop⟩⟩
    exact ⟨hf,hs,hon,hcut,hop⟩
  · rintro ⟨hf,hs,hon,hcut,hop⟩
    exact ⟨hf,hs,⟨⟨hon,hcut⟩,hop⟩⟩

/-- Bayes after silence for types one/two tends to the prior under the canonical
    half-posterior trembles, whose total certificate probability is epsilon. -/
theorem silence_belief_limit (p : ℝ) :
    Filter.Tendsto (fun ε : ℝ => (p-ε/2)/(1-ε)) (nhds 0) (nhds p) := by
  have h : ContinuousAt (fun ε : ℝ => (p-ε/2)/(1-ε)) 0 := by fun_prop (disch := norm_num)
  simpa using h.tendsto

theorem third_silence_belief_limit (p : ℝ) :
    Filter.Tendsto (fun ε : ℝ => p/(1-ε)) (nhds 0) (nhds p) := by
  have h : ContinuousAt (fun ε : ℝ => p/(1-ε)) 0 := by fun_prop (disch := norm_num)
  simpa using h.tendsto

/-- A support-loss history cannot reuse the verified full-support wrapper. -/
theorem zero_eligible_prior_rejected (prior : Mix) (h : prior.a=0) :
    ¬ FullSupport prior := by
  intro hp
  have hpos := hp.1
  rw [h] at hpos
  linarith

#print axioms expected_formula
#print axioms br_all_mixed
#print axioms no_C_after_certificate
#print axioms pooling_iff
#print axioms equal_posterior_tremble
#print axioms operational_exists
#print axioms joint_br_iff
#print axioms source_marginal_valid
#print axioms full_pooling_iff_policy
#print axioms full_support_allows
#print axioms fixed_information_pbe_iff
#print axioms silence_belief_limit
#print axioms third_silence_belief_limit
#print axioms zero_eligible_prior_rejected
end
end DisclosureGame
