# Paper0 Code and Test Audit

Status: static audit complete; dynamic F-C20, F-C1, F-C2, and F-C15 checks complete; v1.0.3 released at `a0b6a45` / `paper0-v1.0.3`.

## Executive Summary

- Audited base: `/home/manem/Downloads/K1-two-clocks-theory`, commit `e178c55`, tag `paper0-v1.0`.
- Released audit target: commit `a0b6a45`, tag `paper0-v1.0.3`; CI-green at https://github.com/abdh0saifelden2-debug/K1-two-clocks-theory/releases/tag/paper0-v1.0.3. v1.0.3 supersedes v1.0.2 (`239aff9`), which supersedes v1.0.1 (`3e98346`).
- 54/54 core paper0 tests reviewed across 10 test files. The ledger has no `OPEN` rows; 54 test cards exist.
- No project code, test, build, or data job was executed locally. Test verdicts are static code/artifact reviews unless marked as a dynamic probe (F-C20 k=0, F-C1, F-C2, or F-C15); no project pytest was run.
- The suite is green-looking but is not strong validation: 19/54 tests are artifact-only, several central claims have no test, and multiple tests assert properties enforced by construction.
- Three direct claim/text conflicts were found at the base commit; v1.0.1 addresses all three:
  1. **O6** (fixed in v1.0.1): the paper says 24 h and 12 h coherence is 0.82-0.98, but the committed ASOS artifact has 24 h coherence 0.397/0.450/0.465 at CAR/DSM/SEA, below their surrogate thresholds. Fix as “S2 clock shared; S1 weak/below floor at three winter high-latitude stations.”
  2. **F-C15** (fixed in v1.0.1): the paper table labels said `±1.0`, but the values are `±0.5`. A raw WREF `2020-01` rerun reproduces the table exactly at `±0.5` (`95/73/121/153/160`; ratios `0.8680/2.1683/3.2768/1.1275/0.7675`; swing `4.2694`); true `±1.0` gives `51/117/121/228/85` and swing `5.6306`. The printed brackets were also not actual 5–95% ranges; they have been replaced with the measured values. The paper now adds the binning-robustness parenthetical: at coarser `±1.0` boundaries the winter swing is `5.6x` (counts `51/117/121/228/85`). While wiring the gate, the coarse swing was recomputed from `fc15_bins.json` as `5.6306`, correcting the earlier `5.7373` label. See `RUNS/2026-10-23-fc15-neon/`.
  3. **R3** (fixed in v1.0.1): the paper said R1/R2 differences are “15% or less”; `max_rel_diff=0.154581` (15.46%), and the test threshold is 30%. The text now says “approximately 15% (maximum 15.5%).”
- **v1.0.2 submission review** closes seven items: the missing bibliography separator; the off-line coherence contradiction; the Fig. 14 low-pass overclaim; the F-C2 prose-only evidence; F-C9; the reproducibility/SHA/duplicate-word cosmetics; and the coarse `±1.0` swing review. The swing remains `5.6x` because the committed artifact gives `3.2767942481 / 0.5819575731 = 5.6306411318`; `5.74x` is not supported. The claim gate now has 5 checks, including F-C2 and the off-line values.
- **Process note:** F-C15 is the second time a label/prose layer falsified what the code computed correctly (the first was the `0.168/0.480` mapping). The recurring failure mode is the text that describes the numerics, not the numerics; the claim-map lint gate is now in the target and CI and was green for `paper0-v1.0.1`, `paper0-v1.0.2`, and `paper0-v1.0.3`.
- **F-C20 is cleared** for the tested k=0 scope by `RUNS/2026-10-21-k0-probe/`: six pure-k=0 profiles, including pure bottom/top modes and nonzero walls at both ends, give wall residuals at most `1.42e-14`; a dual-wall reference agrees to `3.06e-14`; the ny sweep gives at most `1.23e-14`. The remaining issue is that CI does not isolate k=0.
- **F-C1 is confirmed dynamically**: proportional damping gives `t90 = 2.2782 L/c` with R² `1.0`; holding `gamma` fixed makes `t90` nearly independent of `c` (gamma=12: OLS slope `0.158`, intercept `0.264`; gamma=48: slope `0.267`, intercept `0.061`; both through-origin fits fail). The `2.3 L/c` law is imposed by `gamma=1.5c/L`, not a convention-independent adjustment-time law. See `RUNS/2026-10-22-fc1-fixed-gamma/`.
- **F-C2 is a writeup issue, not a refutation after the control**: the paper surrogate reproduces `3.76e-2`; a common-phase surrogate preserves the scalar spectra and component cross-spectrum of `(ud,vd)` exactly (`rel_err≈2e-16`) and still leaves `3.66e-2` residual divergence vs `2.75e-2` uncorrected (`1.33x`; projection `2.2e-15`). The conclusion survives; v1.0.2 commits the control as `figures/24b_spde_common_phase.json` and gates it, and the text attributes failure to phase alignment, not cross-spectrum alone. See `RUNS/2026-10-22-fc2-unitary/`.
- The highest-risk remaining code/test gap is **F-C17**: the 3D alignment test does not assert the intermediate-eigenvector ordering it headlines, so a permutation or near-isotropic result could pass.
- Major interpretation risks: **F-C1** (the `t90` slope is damping-convention-forced), **F-C2** (the specific surrogate is partly tautological; the v1.0.2 common-phase control supports the conclusion but does not make the test independent), and **F-C4** (reanalysis daily/6-hourly windows differ; only 500 hPa is compared).

## Claim Verdicts

| Claim | Status | Basis |
|---|---|---|
| O1 NEON counts | PARTIAL | Artifact matches exactly; no raw NEON reproduction. |
| O2 winter 24 h signal | PARTIAL | 24 h line exists, but dominant-period artifact is 60.49 h in the 6-240 h band; no figure test. |
| O3 winter P-T r | PARTIAL | Artifact `r=0.07144`; artifact-only. |
| O4 summer fingerprint | PARTIAL | Artifact matches r, slopes, periods, ratios; artifact-only. |
| O5 ASOS ladder | PARTIAL | Artifact matches 8 stations, monotonic S2, Haurwitz `r=0.9837`; artifact-only. |
| O6 coherence | CONTRADICTED for S1; S2 supported | S1 at CAR/DSM/SEA is below surrogate 95%; test never checks S1. Off-line statement corrected and gated in v1.0.2. |
| O7 RB headline | UNVERIFIED | No direct test or machine-readable JSON. |
| O8 Ra sweep | PARTIAL | Artifact matches medians; peak-normalized high-k metric and exact 2.40 anchor. |
| O9 stability swing | PARTIAL | Winter raw-verified at `±0.5` (F-C15): counts `95/73/121/153/160`, swing `4.2694`; coarser `±1.0` gives `5.6306` (`5.6x`), cited as the binning-robustness parenthetical; summer remains artifact-only (`5.9487`); helper tests only. |
| O10 elliptic 79% | PARTIAL | Report/PNG only; `far_fraction` threshold `r>0.6` vs `sigma=0.18`. |
| M1 crossover | PARTIAL | Dynamic: slope `2.2782`, R² `1.0` under `gamma=1.5c/L`; fixed gamma gives no `L/c` scaling; no slope/collapse test. |
| M2 Mach sweep | UNVERIFIED | Report/PNG only; no direct test or JSON. |
| S1 projection | PARTIAL | Dynamic `div(u*)=2.7458e-2`; projected `2.2e-15`; no test. |
| S2 surrogate | PARTIAL | Artifact + common-phase control: `3.66e-2` with exact scalar/cross-spectra; claim survives; lint-gated in v1.0.2, no direct pytest. |
| S3 3D periodic | PARTIAL | Artifact matches headline values; tests are structural; alignment/fixture/sign gaps. |
| S4 channel | PARTIAL | Artifact matches headline values; k=0 gauge cleared dynamically; F-C9 closed as documented limitation (fixed-cutoff ratio, not bandwidth-matched). |
| R1 levels | PARTIAL | Report values match; no direct level test. |
| R2 spectrum | PARTIAL | Figure/report only; no machine-readable spectrum test. |
| R3 15% bound | CONTRADICTED | `max_rel_diff=0.154581`; test threshold 0.30. |
| R4 daily vs 6-hourly | PARTIAL | Only 500 hPa checked; daily 24 days vs 6-hourly 6 days; confirmed static. |
| F1-F4 Lean | PARTIAL | Pinned `553d5c2`, CI `39588479578` green; separate repo, not rechecked locally. |
| E1/E4 | UNVERIFIED | No direct test of the kill condition. |
| E2/E3/E5/E6 | PARTIAL | Artifact/report evidence exists, but not a dedicated falsification test. |

## Findings by Severity

### S1 — High audit risk

**F-C15. Stability bins, table ranges, and artifact values (resolved in v1.0.1).**
At the base commit `neon_pt/stability.py:80-86` used `±0.5` while the paper table labels said `±1.0`; the committed artifact had near-neutral/stable counts `122/152`, and the printed brackets were not actual 5–95% ranges. The raw WREF `2020-01` rerun in `RUNS/2026-10-23-fc15-neon/` (DP4.00200.001 basic, RELEASE-2026, MD5 `8e7621c78be196cb1991f1dd1eca64c8`, 602 usable periods, z-d `39.73 m`) shows the table is a `±0.5` table: counts `95/73/121/153/160`, medians `0.182/0.324/0.312/0.225/0.156` for `r_uw`, `0.209/0.150/0.095/0.200/0.203` for `|r_wT|`, ratios `0.8680/2.1683/3.2768/1.1275/0.7675`, swing `4.2694`. True `±1.0` bins give `51/117/121/228/85` and swing `5.6306`, so the earlier Option A (`±1.0`) was invalid. The old artifact's `122/152` came from `month_diagnostics`' hard-coded z-d `39.7` vs the paper's `39.73`. v1.0.1 corrects the row labels/footnote to `±0.5`, adds the caption wording “medians with measured 5–95% ranges over usable periods,” replaces the brackets with measured 5–95% values, adds the `±1.0` robustness parenthetical (`5.6x`; counts `51/117/121/228/85`), regenerates the winter artifact at `±0.5`/`39.73`, and makes `run_neon_compare.py` use the site z-d by default. Summer remains the prior `±0.5` artifact (one-month data limit). This is no longer a submission blocker.

**F-C2. Independent phase randomization destroys the vector cross-spectrum.**
`run_boussinesq.py:148-149,166-167` randomizes `ud` and `vd` with independent phases, and `closure/sgs.py:158`/`closure/sgs3d.py:150` do the same per component. This preserves each component's power spectrum but destroys the cross-spectrum and phase relation. The nonzero divergence of the “spectrum-matched” surrogate is therefore partly built in, not evidence that spectrum matching fails. The dynamic control in `RUNS/2026-10-22-fc2-unitary/` reproduces the paper's single-realization `3.76e-2` and adds a **common-phase** surrogate: it applies the same random phase to both components, preserves scalar spectra and the component cross-spectrum of `(ud,vd)` exactly (`rel_err≈2e-16`), and still leaves `3.66e-2` residual divergence vs `2.75e-2` uncorrected (`1.33x`; deterministic projection `2.2e-15`). For the gradient correction the spectral matrix is rank one, so an exact cross-spectrum-preserving randomization reduces to a common phase; the surrogate remains parallel to the gradient and therefore cannot cancel the drift's divergence. The high-level “energy yes, structure no” conclusion survives; the missing structure is phase alignment with the drift, not cross-spectrum alone. The paper now includes this control, commits it as `figures/24b_spde_common_phase.json`, and gates it in the v1.0.2 claim-map lint.

**F-C1. Compressible damping confounds t90 scaling.**
`run_compressible.py:110` sets `gamma = damp_per_crossing * c / L`; the damping rate grows with the same `c` used in `t90 ~ L/c`, and the run length also scales as `L/c`. `tests/test_compressible.py:39,57-67` only asserts `t90(16)<t90(4)`. A monotonic t90 decrease is guaranteed by stronger damping; the claimed 2.3 slope and `ct/L` collapse are not tested. The dynamic sweep in `RUNS/2026-10-22-fc1-fixed-gamma/` confirms the confound: proportional damping gives exactly `t90 = 2.2782 L/c` (R² `1.0`), but fixed `gamma=12` gives `t90=0.270-0.303` across `c=4-32` (OLS slope `0.158`, intercept `0.264`), and fixed `gamma=48` gives `0.071-0.128` (slope `0.267`, intercept `0.061`); both through-origin fits fail. The 10% threshold is controlled by the damping time, not the wave-crossing time. The slope should be presented as conditional on a fixed damping-per-crossing convention, not as an emergent `L/c` law.

**F-C4. Reanalysis daily/6-hourly comparison is not controlled.**
`run_reanalysis.py:105-107,121-130` compares 24 daily means against 24 six-hourly snapshots (6 days), so the windows and averaging operators differ. The daily branch builds `fig_levels` for 850/500/250 hPa; the instantaneous branch computes only 500 hPa, then the right-hand bar compares `daily[500]` against `inst[500]`. The paper says daily is smaller than 6-hourly “at every level,” but no level comparison exists. The low-pass interpretation is therefore confounded by window length and season. This is a confirmed static finding; no dynamic run is needed if the prose is restricted, but an all-level matched-window run is required to defend the stronger statement.

**F-C16. O6 is contradicted by its own ASOS artifact.**
`figures/09b_asos_ci.json` gives `coh_S1=0.3971` (CAR), `0.4504` (DSM), `0.4645` (SEA), below their surrogate thresholds. `tests/test_asos_ci.py:40-45` only checks `coh_S2` and off-line coherence. The S2 latitude fingerprint is supported; the 24 h coherence sentence is not.

**F-C17. The 3D alignment test does not test intermediate-eigenvector ordering.**
`tests/test_closure3d.py:140-145` only checks that each mean `|cos|` lies in `[0,1]` and `n_points>0`. It does not assert `cos_intermediate > cos_extensional` or `> cos_compressive`, which is the headline ordering. The artifact has `0.6536 > 0.4786 > 0.3254`, but a permuted or near-isotropic implementation would still pass. This is a high-value test gap, not a proof that the artifact is wrong.

### S2 — Moderate audit risk

**F-C5. R3 exceeds its stated 15% bound.**
Artifact `max_rel_diff=0.154581` (15.46%); per-level `11.84/15.46/8.19%`. The paper says 15% or less; the test asserts `<0.30`. Concrete text/test mismatch, low scientific magnitude.

**F-C8. Projected-FDT residual only fills positive deficits.**
`closure/sgs3d.py:209` uses `resid = max(E_true[k]-E_par[k], 0)`. If the parallel part overshoots, the residual is zero and the total force spectrum need not match `E_m(k)`. The 0.9997 transfer correlation may be a construction artifact; the test only requires `>0.6`.

**F-C9. Channel filter cutoff units are inconsistent (closed as documented limitation).**
`sharp_filter` uses a DCT mode count `ny_keep`; `fourier_filter` uses `kc_y=float(ny_keep)` as a Fourier wavenumber, so the commutator comparison uses different cutoff conventions. The qualitative wall effect is independently supported by the near-wall localization (near/bulk `33.81`, peak `0`), but the exact ratio is not a bandwidth-matched calibration. The paper now discloses this in the text (v1.0.3 moved it out of a footnote that split across pages); the audit records it as a documented limitation rather than a resolved numerical check. No matched-bandwidth sweep was run.

**F-C3. RB high-k ratio is peak-normalized and measured at a different band.**
`run_rb.py:141-142` and `run_rb_ra_sweep.py:61-62` divide each spectrum by its own maximum. The paper's `~1e4` and `~70x` widening are shape ratios, not absolute power ratios; the sweep averages `k >= kmax/sqrt(10)` (~12.9 for `nx=512`), not `k~10`. State both raw and normalized ratios.

**F-C6. NumPy minimum version is inconsistent.**
`run_rb.py:60` uses `np.trapezoid` (NumPy ≥2.0), while `requirements.txt` declares `numpy>=1.24`. The declared minimum environment fails with `AttributeError`. CI's unpinned install may hide this.

**F-C11. Artifact-only tests and exact anchors dominate.**
19/54 tests read committed JSON. Exact counts (`1097/1180`) and the exact `2.40` anchor can pass with a wrong generator. `test_reanalysis_crosscheck` uses 0.30 for a 15% claim. These are consistency checks, not independent validation.

**F-C12. CI hides dependency failures.**
`.github/workflows/ci.yml` uses `pip install -r requirements.txt || true`, then installs unpinned `pytest numpy scipy matplotlib`. A broken or missing declared dependency can be silently replaced. This undermines the reproducibility claim.

**F-C18. 3D physics tests use a small, short fixture against a GPU-scale artifact.**
Fixture `32³/300`, `nu=3.5e-3`; artifact `128³/2500`, `nu=1.2e-3` on CuPy. Tests assert `mean_prod>0`, `norm_prod>1e-3`, `backscatter_fraction_true>0.05`; artifact values are `0.1679` and `0.480`. No seed/resolution ensemble, so the fixture's representativeness is unknown.

**F-C19. Smagorinsky test checks only the dissipation sign.**
`tests/test_closure3d.py:71-76` requires `T_smag<=1e-9` but not magnitude, shape, or anti-correlation with the true transfer. Artifact `transfer_corrs.Smagorinsky=-0.6415`. A wrong-amplitude model with the right sign passes.

**F-C7. Hardcoded NEON displacement height.**
`run_neon_compare.py:40` hardcodes `z_minus_d=39.7`; `run_stability.py:210` reads metadata. The seasonal comparison silently assumes WREF metadata and is not portable across sites/revisions.

**F-C13. Taylor microscale convention is unstated.**
`run_rb.py` uses `sqrt(<phi²>/<(dphi/dx)²>)`; another common convention has `sqrt(2)`. Ratios are invariant, but absolute `0.607/0.253` depend on the convention.

### S3 — Low audit risk / wording and coverage

**F-C10. Elliptic “one source width” label is imprecise.**
`far_fraction` uses `r>0.6` while `sigma=0.18`; 0.6 is ~3.3 sigma. The 79% number may be correct for the stated threshold, but the caption's “beyond one source-width” needs a definition.

**F-C14. Winter dominant period needs claim qualification.**
Artifact `temp_dominant_period_h=60.49` in the 6-240 h band; the paper says “clean 24-hour signal.” The 24 h line is present, but “dominant” depends on the band. State the band or check the 24 h peak directly.

### Cleared by dynamic check

**F-C20. k=0 gauge and the y=0 no-penetration condition.**
The static concern was that `closure/channel3d.py:164-172` replaces the y=0 Neumann row with `phi[0]=0`, so a nonzero k=0 wall mode could survive projection at the bottom wall. The k=0 probe in `RUNS/2026-10-21-k0-probe/` tested six profiles with nonzero wall-normal velocity, including pure bottom/top modes and a random field with nonzero values at both walls. Shipped wall absolute residual is at most `1.42e-14`; the dual-wall reference solve agrees to `3.06e-14`; the ny sweep gives at most `1.23e-14`. No bottom-wall leak was detected, so the artifact's `wall_no_penetration=6.23e-15` is consistent with this path. The remaining issue is a test gap: `test_project_wall_enforces_no_penetration` does not isolate k=0, so CI does not protect this behavior. See `notes/static-findings.md` F-C20 for the full caveat.

## Test Quality

- The ledger contains 54 reviewed rows, no `OPEN`, and 54 cards. This is a static review completion, not a pytest run.
- 19 tests are artifact-only and cannot detect a wrong generator, only artifact drift.
- Several tests assert properties enforced by construction: projection tests end in `project3d`/`project_wall`; transfer tests build the model from the truth; backscatter tests use a positive-definite Smagorinsky model.
- Several thresholds are weak or fixture-specific: `corr>0.6`, `div<0.1`, `mean_prod>0`, `backscatter_true>0.05`, exact `2.40` anchor, 30% cross-check threshold.
- No test covers O7, M2, O10, the M1 slope/collapse, or the full S1 input divergence.
- No test runs under the declared minimum NumPy version or across CPU/CuPy/seed ensembles.

## Dynamic Verification

Completed:

- **F-C20 pure wall mode:** `RUNS/2026-10-21-k0-probe/`; six pure-k=0 profiles at `32x49x32` plus `ny=33/49/65`; wall residual at most `1.42e-14`; dual-wall reference agrees to `3.06e-14`. Cleared for the tested scope.
- **F-C1 fixed-gamma sweep:** `RUNS/2026-10-22-fc1-fixed-gamma/`; `c=[4,8,16,32]`, `n=128`, `20 L/c`; proportional `t90=2.2782 L/c` (R² `1.0`); fixed gamma 12/48 gives OLS slopes `0.158/0.267` with nonzero intercepts and no through-origin `L/c` law; relative collapse spread `0/1.19/0.71`.
- **F-C2 unitary control:** `RUNS/2026-10-22-fc2-unitary/`; `n=128`, `t=6`; paper surrogate `3.7565e-2` (reproduces `3.76e-2`); common-phase surrogate `3.6623e-2` with exact scalar/component cross-spectrum (`rel_err≈2e-16`); drift `2.7458e-2`; projection `2.225e-15`.
- **F-C15 NEON rerun:** `RUNS/2026-10-23-fc15-neon/`; WREF `2020-01` `DP4.00200.001` basic `RELEASE-2026`, MD5 `8e7621c78be196cb1991f1dd1eca64c8`; 602 usable periods; `±0.5` reproduces paper counts/medians/ratios (swing `4.2694`); true `±1.0` gives `51/117/121/228/85` and swing `5.6306`; actual 5–95% ranges measured.

Pending, in priority order; all execution belongs on Kaggle/CI, not this laptop:

1. **F-C17/F-C18/F-C19:** add analytic eigenvector-ordering test; run 3D fixture across seeds and resolutions; check Smagorinsky transfer magnitude/shape.
2. **F-C3:** recompute RB absolute spectra and the same-`k` ratio, without peak normalization.
3. **Data-backed O1–O9 beyond F-C15:** fetch ASOS/RB subsets and rerun the artifacts; compare coherence and headline values. The winter NEON stability table is done; summer remains artifact-only.
4. **Optional R3/R4/F-C4:** if the paper keeps the “at every level” claim, recompute R1/R2 ratios on identical windows at 850/500/250 hPa and compare daily vs 6-hourly at all levels.

## What Was Not Audited

- Dynamic behavior outside the completed k=0, F-C1, F-C2, and F-C15 probes and under the paper's exact environment.
- Data-backed recomputation for NEON, ASOS, RB, and reanalysis.
- Full Lean proof audit; only pinned statement-scope mapping and CI status were checked.
- Paper1 and non-paper0 claims.
- The v1.0.1 release commit was CI-built and tagged; no project pytest was run locally. The audit did not independently rerun the full suite or rebuild the PDF. The same applies to v1.0.2 and v1.0.3: CI built the PDF, and the released asset was only read and hashed locally.
- No matched-bandwidth channel sweep; F-C9 is disclosed, not resolved.

## Release Outcome

- `paper0-v1.0.1` was released from commit `3e98346` (squashed PR #4) on 2026-10-23. The audit is published at https://github.com/abdh0saifelden2-debug/paper0-audit.
- Claim-map lint: 3 checks passed. Pytest: `683 passed, 1 skipped`. Paper build/PDF check: passed.
- Main CI run `40021028585` green in `6m36s`; tag workflow `40021921986` built and attached `paper0_two_clocks.pdf` (SHA-256 `f06630066e9c6d6e514e0f41c0b845c3cdac977c48ae7c4b5303117391c63d31`).
- The first CI run failed because CI's Python formatted O6 `0.4645` as `0.464` at three decimals while the paper prints `0.465`; the checker now compares the printed values numerically. The fix was squashed into `3e98346`.
- The release notes name the superseded v1.0 items: O6, F-C15 (labels/ranges/robustness), R3, F-C1, F-C2, F-C4, and CI/dependency fixes.

### v1.0.2

- `paper0-v1.0.2` was released from `239aff9` on 2026-10-30, superseding v1.0.1 (`3e98346`; tag left unmoved). PR #5 (`1fab285`) closed the seven submission-review items; PR #6 (`239aff9`) moved the archive SHA-256 to a copyable line after the first v1.0.2 PDF clipped it.
- Claim-map lint: 5 checks passed. Pytest: `683 passed, 1 skipped`. Paper build/PDF check: passed.
- PR #5 CI `40027964422` / `40027964234`; PR #6 CI `41037093654` / `41037093652`; main CI `41037934023` green in `6m33s`; Paper main `41037934080` green; tag workflow `41038812908` green.
- Released asset: `2,358,357` bytes, 24 pages, SHA-256 `1b336d631bcf92ea896718d2882782f3a81cb58db3374fb3b09cc9dde794616a` (identical to the GitHub asset digest). `pdftotext` recovers the full 64-character archive digest on one line.
- Off-line coherence is stated as `0.09–0.30`, at or below the surrogate floor at four of eight stations and within `0.12` elsewhere; Fig. 14 is a same-level consistency check; F-C9 is a disclosed limitation. The coarse `±1.0` swing stays `5.6×`; `5.74×` is not supported by `fc15_bins.json`.
- Release: https://github.com/abdh0saifelden2-debug/K1-two-clocks-theory/releases/tag/paper0-v1.0.2

### v1.0.3

- `paper0-v1.0.3` was released from `a0b6a45` on 2026-10-30, superseding v1.0.2 (`239aff9`; older tags left unmoved). A read-aloud of the released v1.0.2 PDF found three defects that the source lint could not see.
- Table 8's E4 row was clipped: the `ll` tabular ran 150.6 pt past the margin and `pdftotext` recovered only `... converges with a c-depen`. The second column is now `p{0.60\linewidth}`; the row reads `... c-dependent final state`.
- The F-C9 footnote split across pages and stranded “calibration.” alone at the bottom of page 17. The caveat is now in the body.
- The pre-table coherence paragraph duplicated the band-resolved paragraph and said coherence “collapses to the surrogate noise floor”; it was removed, and the band-resolved paragraph now carries the exact gated `0.09–0.30` sentence.
- The Paper workflow now installs `poppler-utils` and gates the built PDF for `final state` and the full 64-character archive SHA-256.
- PR #7 CI `41040231759` / `41040231804`; main CI `41040989300` green in `6m23s`; Paper main `41040989285` green; tag workflow `41041824992` green.
- Released asset: `2,357,555` bytes, 24 pages, SHA-256 `03e629b145dd6fbbf47b98488fbcd25fd1f3ca2f400691998149bbdc6865e9e4` (identical to the GitHub asset digest). `pdftotext -bbox` finds no word reaching the 612 pt page edge.
- Release: https://github.com/abdh0saifelden2-debug/K1-two-clocks-theory/releases/tag/paper0-v1.0.3

## Appendices

- `AUDIT_LEDGER.tsv` — 54 per-test rows.
- `CLAIM_MAP.md` — claim-by-claim status and evidence notes.
- `INVENTORY.md` — test/data/artifact inventory and coverage gaps.
- `notes/test-cards.md` — 54 detailed cards.
- `notes/static-findings.md` — F-C1–F-C20.
- `notes/v1.0.1_proposed_changes.md` — applied v1.0.1 fixes for O6/F-C15/R3/F-C1/F-C2/F-C4/CI.
- `RUNS/2026-10-21-k0-probe/` — F-C20 k=0 probe: JSON, kernel log, source revision, run code, and result summary.
- `RUNS/2026-10-22-fc1-fixed-gamma/` — F-C1 proportional/fixed-gamma sweep and collapse metrics.
- `RUNS/2026-10-22-fc2-unitary/` — F-C2 independent-phase, common-phase, and unitary controls.
- `RUNS/2026-10-23-fc15-neon/` — F-C15 raw WREF 2020-01 rerun, `±0.5`/`±1.0` comparison, actual percentiles, and updated winter artifact.
- `release-gate/` — snapshot of the v1.0.1 claim-map gate (`CLAIM_MAP.md`, `claims/fc15_winter.json`, lint, runner) with upstream hashes and CI result.
