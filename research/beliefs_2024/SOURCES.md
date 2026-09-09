# Sources and reuse boundaries

Inspected 9 September 2026 before fitting. This is an additive correction to the earlier
empirical-design checkpoint, whose files remain frozen.

- Aoyagi, Fréchette and Yuksel, *Beliefs in Repeated Games*, AER 114(12), 3944–3975,
  DOI [10.1257/aer.20220639](https://doi.org/10.1257/aer.20220639).
  [Author paper](https://gfrechette.com/print/Aoyagi_2024a.pdf), dated 16 October 2024;
  [online appendix](https://gfrechette.com/print/Aoyagi_2024a_oa.pdf).
  Section 3 supplies payments, timing and random termination. Figure 2 supplies the
  first replication; Figure 11 the changed-payoff comparison. Appendix Table 11
  defines the strategy catalogue. The paper's maintained catalogue and belief-noise
  assumptions do not establish unrestricted identification.
- [Author data](https://gfrechette.com/data/Aoyagi_2024a_data.txt): freshly acquired
  bytes match the earlier checkpoint. This analysis table has own/opponent actions
  and reports but no pair identifier. It is not asserted to be pristine lab logs.
- [Archive v1](https://www.openicpsr.org/openicpsr/project/205541/version/V1/view),
  DOI [10.3886/E205541V1](https://doi.org/10.3886/E205541V1): the rendered public page
  explicitly displays CC BY 4.0. Earlier text extraction omitted this licence.
  The readme preview returned “Plugin not available..”; download redirected to login.
  No login or restricted download was attempted. Archive and author-table byte identity
  remains unverified. Public author access alone is not a redistribution licence:
  keep raw author rows outside Git and provide explicit acquisition and hash checking.
- [stratEst CRAN](https://cran.r-project.org/package=stratEst), version 1.1.8,
  GPL-3; Dvořák (2023), [10.1007/s40881-023-00141-7](https://doi.org/10.1007/s40881-023-00141-7).
  Inspected actual R/stratEst_model.R, R/stratEst_strategy.R and src/stratEst.cpp,
  installed help and strategies.PD objects. Built-in ALLC, ALLD, GRIM, TFT, DTFT,
  GRIM2 and TF2T supply the required automata; construct the three round thresholds.
  Binary emission code uses q as the actual flip probability. Individual mixture
  likelihood multiplies responses across games while states reset each game.
  **Capability correction:** the public model wrapper has no cluster argument and
  initializes cluster internally to a zero matrix. Do not infer session-robust
  uncertainty from package descriptions or use its standard errors for that purpose.
  The package supplies point estimation, not equilibrium or global-optimality proof.
- [SciPy linprog](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html)
  and [minimize](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html)
  supply existing LP and bounded numerical optimization. Their returned success flags
  are numerical diagnostics; exact assurance requires the separately stated witnesses
  or residual bounds. No new solver framework is needed.

The standard finite discounted Markov reward equation is derived explicitly in METHOD.md
rather than borrowing a broader equilibrium theorem. Published treatment patterns were
known before this retrospective specification; target observations still cannot be used
for fitting or model selection. The source manifest binds actual downloaded bytes.
