# Static Findings — Paper0

Status: static sweep complete; dynamic checks F-C20, F-C1, and F-C2 completed (2026-10-21/22); F-C15 raw winter check completed 2026-10-23. Each finding has a code/artifact anchor and, where possible, a per-test ledger row. F-C14–F-C20 are later additions and are numbered by discovery order, not severity; F-C20 was cleared by `RUNS/2026-10-21-k0-probe/`. Release fixes are in `3e98346` / `paper0-v1.0.1`, `239aff9` / `paper0-v1.0.2`, and `a0b6a45` / `paper0-v1.0.3`.

## F-C1 Compressible damping confounds the t90 scaling (reframed in v1.0.1)

- Target: `run_compressible.py:110`
- Observation: `gamma = damp_per_crossing * c / L` with default `damp_per_crossing=1.5`. The damping rate is proportional to `c`, exactly the variable used in `t90 ~ L/c`. The simulation also sets `t_end = n_crossings * L / c`.
- Test: `tests/test_compressible.py:39,57-67` sets `gamma=1.5*c/L` for each `c` and only asserts `t90(16.0) < t90(4.0)`.
- Why it matters: a monotonic decrease of `t90` with `c` is guaranteed by stronger damping even if the acoustic relaxation mechanism is wrong. The claimed slope `2.3` and the `ct/L` collapse are not tested.
- Decisive check: hold `gamma` fixed while varying `c`; fit `t90` vs `L/c`; repeat with `gamma` proportional to `c`; compare slopes and collapse.
- Dynamic result (`RUNS/2026-10-22-fc1-fixed-gamma/`): proportional damping gives `t90=2.2782 L/c` (R² `1.0`, collapse spread `0.0`). Fixed `gamma=12` gives `t90=0.270-0.303` for `c=4-32` (OLS slope `0.158`, intercept `0.264`; through-origin R² negative); fixed `gamma=48` gives `0.071-0.128` (slope `0.267`, intercept `0.061`). The 10% threshold is damping-controlled; the `2.3 L/c` law is not convention-independent.
- Severity: S1 confirmed; the paper must disclose the fixed-damping-per-crossing convention and cannot present the slope as an emergent law.

## F-C2 Boussinesq surrogate destroys vector cross-spectrum by construction (control committed in v1.0.2)

- Target: `run_boussinesq.py:148-149,166-167`; `closure/sgs.py:158`; `closure/sgs3d.py:150`
- Observation: `phase_randomized(sp, ud, seed=11)` and `phase_randomized(sp, vd, seed=12)` use independent random phases for the two velocity components. The docstring says the surrogate matches `E_m(k)` but is not projected, so divergence is nonzero.
- Why it matters: independent per-component phase randomization preserves each component's power spectrum but destroys the cross-spectrum, co-spectrum, vector gradients, and any phase relation between components. A divergence failure is then close to mathematically necessary, not an empirical discovery about "spectrum matching."
- Test: `tests/test_spde_limit_ensemble.py` checks the committed artifact; `tests/test_closure3d.py::test_surrogate_breaks_solenoidality` checks only that divergence is large.
- Decisive check: build a surrogate that preserves the vector cross-spectrum (e.g., randomize a common phase or rotate the vector field coherently) and compare divergence; measure cross-spectrum preservation directly.
- Dynamic result (`RUNS/2026-10-22-fc2-unitary/`): at `n=128,t=6`, `div(u*)=2.7458e-2`; the paper surrogate gives `3.7565e-2` (reproduces the reported `3.76e-2`); a common-phase surrogate preserving scalar spectra and the component cross-spectrum of `(ud,vd)` exactly (`rel_err≈2e-16`) gives `3.6623e-2` (`1.33x` drift); projection is `2.225e-15`. Global/k-dependent unitary rotations preserve vector energy but not the component cross-spectrum and are reported only as controls.
- Interpretation: for the gradient correction the spectral matrix is rank one, so an exact cross-spectrum-preserving randomization is a common phase; the surrogate remains parallel to the gradient and cannot cancel the drift's divergence. The high-level “energy yes, structure no” claim survives; v1.0.2 commits the common-phase control as `figures/24b_spde_common_phase.json`, gates `3.66e-2`/`2.75e-2`/`1.33x`/`2e-16`/`2.2e-15`, and attributes failure to phase alignment with the drift, not cross-spectrum loss alone.
- Severity: S1 for the writeup/interpretation; not a refutation of the high-level claim.

## F-C3 RB high-k ratio is computed from peak-normalized spectra

- Target: `run_rb.py:141-142`; `run_rb_ra_sweep.py:61-62`
- Observation: the spectra are divided by their own maxima before the high-k ratio is formed. The paper's table lists buoyancy power `1.0` and pressure `1e-4`, i.e. a shape ratio after peak normalization, not an absolute power ratio.
- Artifact: `figures/15b_rb_ra_sweep.json` has `highk_suppression_median` 636 at Ra=1e6 and 46253 at Ra=1e8 (~73x). The paper's `~70x` widening matches the normalized shape ratio; the `~1e4` headline at Ra=1e6 is not the same quantity. `highk_suppression` also averages the top half-decade `k >= kmax/sqrt(10)` (~12.9 for nx=512), not `k ~ 10` as in the paper's RB table, so the two "high-k" numbers are at different bands.
- Why it matters: the claim "buoyancy exceeds pressure by ~1e4" is ambiguous unless the normalization is stated. The physical `1/k^4` argument concerns absolute spectra.
- Decisive check: recompute the raw spectra without peak normalization and report the ratio at the same k; state both raw and normalized values.
- Candidate severity: S1 if the raw ratio is far from 1e4; S2 if it is close but the caption is misleading.

## F-C4 Reanalysis daily vs 6-hourly comparison uses different windows (restricted to 500 hPa in v1.0.1)

- Target: `run_reanalysis.py:105-107,121-130,182`
- Observation: `daily[lev]` is computed from `ncep.ke_ratio_block(u, v, lat)` over `nt=24` daily means, while `inst500` is computed from `fetch_wind(500, year, t0=t0, nt=nt, source="inst")` over `nt=24` six-hourly snapshots (6 days). The branches therefore cover different physical intervals and different averaging operators.
- Paper: `paper0_two_clocks.tex:445` says daily mean is smaller than 6-hourly "at every level"; the code only computes the instantaneous comparison at 500 hPa.
- Why it matters: the claimed low-pass effect is confounded by window length and season; the "every level" claim is not implemented.
- Decisive check: compute daily and 6-hourly ratios on the same start/end and length; compute all three levels; compare.
- Static confirmation: `fig_levels` builds daily 850/500/250 (`run_reanalysis.py:100-113`), but `inst500` is the only instantaneous branch (`:106`); the right bar compares daily 500 against inst 500 (`:121-130`). Daily covers 24 days, instant covers 6 days.
- Severity: S1 for the universal claim; S2 for the 500 hPa comparison. Restrict prose to 500 hPa unless an all-level matched-window run is added.

## F-C5 R2 cross-check exceeds its stated 15% bound (resolved in v1.0.1)

- Target: `figures/27b_reanalysis_crosscheck.json`; `run_reanalysis_r2.py`
- Observation: `max_rel_diff = 0.154581...` (15.46%), while `paper0_two_clocks.tex:443` says "15% or less." The test `tests/test_reanalysis_crosscheck.py` only asserts `< 0.30`.
- Why it matters: the paper's stated bound is false by ~0.46 percentage points under its own artifact. Low severity but concrete.
- Decisive check: recompute from raw R1/R2 or confirm the artifact; report which level drives the max.
- Resolution: v1.0.1 says “approximately 15% (maximum 15.5%)”; the lint checks the exact wording and the artifact maximum.
- Candidate severity: S3.

## F-C6 NumPy minimum version is inconsistent (fixed in v1.0.1)

- Target: `run_rb.py:60`; `requirements.txt:1`
- Observation: `np.trapezoid` was introduced in NumPy 2.0, but the project declares `numpy>=1.24`. A user on 1.24-1.26 gets `AttributeError`.
- Why it matters: reproducibility claim fails on the declared minimum environment. `thermal_tail_amplitude.py:108` has a version-independent helper, but `run_rb.py` does not use it.
- Decisive check: import/run under NumPy 1.26 and 2.x; or inspect the API version.
- Resolution: v1.0.1 sets `numpy>=2.0` in `requirements.txt`.
- Candidate severity: S2 for reproducibility; S3 for scientific claim.

## F-C7 Hardcoded site metadata in seasonal comparison (fixed in v1.0.1)

- Target: `run_neon_compare.py:40`
- Observation: `month_diagnostics(data_dir, z_minus_d: float = 39.7)` hardcodes the WREF displacement height. `run_stability.py:210` uses `meta.z_minus_d`. The seasonal cross-check does not read the file metadata.
- Why it matters: the code is not portable to another site or metadata revision; it silently assumes 39.7 m.
- Decisive check: compare with `meta.z_minus_d`; rerun with metadata.
- Resolution: v1.0.1 makes `z_minus_d` optional and uses `meta.z_minus_d` when no override is passed; the winter artifact was regenerated at `39.73`.
- Candidate severity: S2/S3 depending on whether the hardcoded value matches the data.

## F-C8 Projected-FDT residual only fills positive deficits

- Target: `closure/sgs3d.py:209`
- Observation: `resid = max(float(E_true[k]) - float(E_par[k]), 0.0)`. If the parallel/parameterized part overshoots `E_true[k]`, the residual is zero, so the total force spectrum does not match `E_m(k)` as the docstring implies.
- Test: `tests/test_closure3d.py::test_projected_fdt_tracks_true_transfer` only requires transfer correlation > 0.6.
- Why it matters: the construction may be a one-sided spectral patch, not a projection of the full target. The 0.9997 transfer correlation could be a consequence of construction.
- Decisive check: compute total force spectrum vs `E_m(k)` for all k; find overshoot modes; test with a deliberately overshooting parallel part.
- Candidate severity: S2.

## F-C20 k=0 gauge may replace the y=0 no-penetration condition (cleared dynamically)

- Target: `closure/channel3d.py:164-172`; `tests/test_channel3d.py:42-46`.
- Observation: for horizontal modes with `k_h=0`, `project_wall` replaces the wall row at `y=0` with the gauge `phi[0]=0` and sets `rhs[0]=0`. That removes the Neumann condition `Dy phi = v` at `y=0` for those modes. If the k=0 wall-normal velocity is nonzero, the projected field need not satisfy no-penetration at that wall.
- Artifact: `figures/77_closure3d_bounded.json` reports `wall_no_penetration=6.23e-15`, so either the test field's k=0 wall mode vanishes or the artifact came from a different path. The static code does not make that clear.
- Test: `test_project_wall_enforces_no_penetration` checks the same field and reports the artifact-level value; it does not isolate the k=0 mode.
- Dynamic result: `RUNS/2026-10-21-k0-probe/` projects six pure-k=0 fields, including pure bottom/top modes and a random field with nonzero wall values at both walls. Shipped wall absolute residual is at most `1.42e-14`; the dual-wall reference solve agrees to `3.06e-14`; the ny sweep gives at most `1.23e-14`. No bottom-wall leak was detected.
- Why it matters: the headline “machine-zero no-penetration” is not contradicted by this path for the tested k=0 scope. The remaining issue is test coverage, not an observed numerical failure.
- Decisive check: completed in the run above; includes both wall slices separately.
- Candidate severity: no confirmed bug; S3 test gap because CI does not isolate k=0.

## F-C17 3D alignment test does not test the intermediate-eigenvector claim

- Target: `tests/test_closure3d.py:140-145`; `closure/sgs3d.py:267-312`.
- Observation: the test only checks that each mean `|cos|` is in `[0,1]` and `n_points>0`. It does not assert `cos_intermediate > cos_extensional` or `> cos_compressive`, which is the headline Constantin-Fefferman claim.
- Artifact: `figures/65_closure3d.json` has 0.6536 > 0.4786 > 0.3254, so the artifact supports the ordering, but the test would pass if the labels or ordering were wrong.
- Why it matters: a bug that permutes eigenvectors or returns near-isotropic values passes.
- Decisive check: add an analytic strain tensor with known eigenvector ordering; assert the e2 ordering and compare to the artifact.
- Candidate severity: S1 for the test gap; S2 for the claim if the artifact is trusted.

## F-C18 3D physics tests use a small, short fixture against a GPU-scale headline artifact

- Target: `tests/test_closure3d.py:23-29,122-137`; artifact `figures/65_closure3d.json`.
- Observation: the fixture is 32³/300 steps with `nu=3.5e-3`, while the artifact is 128³/2500 steps with `nu=1.2e-3` on CuPy. The tests assert `mean_prod>0`, `norm_prod>1e-3`, and `backscatter_fraction_true>0.05`; the artifact values are 0.1679 and 0.480.
- Why it matters: the test thresholds are weak and run-specific; a short underdeveloped field can be near the sign/threshold boundary. The tests do not vary seed or resolution, so they do not establish that the 32³ fixture is representative of the headline.
- Decisive check: run the fixture across seeds and at 48³/64³; compare the distributions to the artifact.
- Candidate severity: S2.

## F-C19 3D Smagorinsky test checks only the dissipation sign

- Target: `tests/test_closure3d.py:71-76`; artifact `transfer_corrs.Smagorinsky=-0.6415`.
- Observation: the test requires `T_smag(k)<=1e-9` but does not check the magnitude, the transfer shape, or the anti-correlation with the true transfer.
- Why it matters: the paper’s claim that Smagorinsky carries the right magnitude but wrong shape is not tested; a model with the wrong amplitude but the right sign passes.
- Decisive check: compare `T_smag` to `-2<nu_t |S|²>` and to `T_true`; report the correlation and amplitude ratio.
- Candidate severity: S3 for coverage.

## F-C9 Channel filter cutoff units are inconsistent (closed as documented limitation)

- Target: `closure/channel3d.py`
- Observation: `_dct_lowpass_y` uses a mode count (`ny_keep`), while `fourier_filter` uses `kc_y=ny_keep` as a wavenumber cutoff. The commutator comparison may compare filters with different effective cutoffs.
- Why it matters: the headline commutator ratio and near-wall localization could depend on the cutoff convention. The qualitative wall effect may survive.
- Decisive check: sweep cutoff definitions at matched effective bandwidth; compare commutator and localization.
- Disposition (v1.0.2, 2026-10-30): **CLOSED as a documented limitation, not numerically resolved.** No matched-bandwidth sweep was run. The paper now states in the text that the channel ratio uses the test's fixed cutoffs and is an order-of-magnitude contrast, not a bandwidth-matched calibration (v1.0.3 moved this out of a footnote that split across pages). The qualitative near-wall localization (`near/bulk=33.81`, `peak=0`) remains the supported feature.
- Severity: S2; disclosed limitation, not a submission blocker.

## F-C10 Elliptic far-field label is imprecise

- Target: `subglacial/elliptic_demo.py`
- Observation: `far_fraction` uses `r > 0.6` while the bump scale is `sigma=0.18`; 0.6 is ~3.3 sigma, not "one source-width." The 79% claim may still hold, but the caption's "beyond one source-width" needs a definition.
- Candidate severity: S3.

## F-C11 Artifact-only tests and exact anchors

- Targets: `tests/test_neon_seasonal.py:24`, `tests/test_rb_ra_sweep.py:35`, `tests/test_asos_ci.py`, `tests/test_spde_limit_ensemble.py`, `tests/test_reanalysis_crosscheck.py`
- Observation: 19/54 tests read committed JSON. Exact counts (1097/1180) and exact 2.40 anchors can pass with a wrong generator. `test_reanalysis_crosscheck` uses a 0.30 threshold for a 15% claim.
- Why it matters: green suite is not evidence of correct generation. These tests are consistency checks, not independent validation.
- Candidate severity: S2 for coverage; S3 for individual anchors.

## F-C12 CI hides dependency failures (fixed in v1.0.1)

- Target: `.github/workflows/ci.yml`
- Observation: `pip install -r requirements.txt || true`, followed by unpinned `pytest numpy scipy matplotlib`.
- Why it matters: a missing declared dependency can be silently installed at latest version, or a broken install can be ignored. The environment is not pinned.
- Resolution: v1.0.1 removes `|| true`, installs only `requirements.txt`, and pins `pytest==8.3.5`.
- Candidate severity: S2/S3.

## F-C13 Taylor microscale convention is not stated

- Target: `run_rb.py` `taylor_microscale`
- Observation: `lambda = sqrt(<phi^2>/<(dphi/dx)^2>)`. Another common convention has a factor `sqrt(2)`. The ratio is unaffected, but absolute values 0.607/0.253 depend on the convention.
- Candidate severity: S3.

## F-C16 Paper claims high 24 h and 12 h coherence; artifact's 24 h coherence is low at three stations (resolved in v1.0.1)

- Target: `paper0_two_clocks.tex:87,113`; `figures/09b_asos_ci.json`; `tests/test_asos_ci.py:40-45`
- Observation: the paper says coherence at the solar harmonic lines (24 and 12 h) is high, 0.82-0.98. The artifact's `coh_S2` (12 h) is 0.8203-0.9837, matching. But `coh_S1` (24 h) is 0.3971 at CAR, 0.4504 at DSM, and 0.4645 at SEA. Those three are below their own `coh_S1_surr95` values (0.5323, 0.6130, 0.5966).
- Test: `test_coherence_split` only checks `coh_S2` and off-line coherence; it never checks `coh_S1`.
- Why it matters: the paper's statement about both solar lines is contradicted by its own artifact at 3 of 8 stations. The S2 latitude fingerprint remains supported.
- Decisive check: recompute S1/S2 coherence from IEM data; verify the artifact; correct the text to distinguish S1 and S2, or explain why 24 h coherence is not expected to be high at those sites.
- Resolution: v1.0.1 reports S2 `0.82–0.98` and S1 at CAR/DSM/SEA (`0.397/0.450/0.465`) below their surrogate thresholds; the lint checks these values.
- Candidate severity: S2.

## F-C15 Stability bin boundaries, table ranges, and artifact values (resolved in v1.0.1)

- Target: `paper0_two_clocks.tex:177-187`; `neon_pt/stability.py:80-86`; `figures/01b_neon_seasonal.json`
- Original observation: the paper table labels were `<-1.0`, `-1.0` to `-0.1`, `-0.1` to `0.1`, `0.1` to `1.0`, `>1.0`, while the code used `±0.5`. The committed artifact had near-neutral/stable counts `122/152` and ratios `3.3388/1.1202/0.7675`; the paper printed `121/153` and `3.28/1.13/0.77`.
- Raw check (`RUNS/2026-10-23-fc15-neon/`; WREF `2020-01`, `DP4.00200.001` basic `RELEASE-2026`, MD5 `8e7621c78be196cb1991f1dd1eca64c8`, 602 usable periods, z-d `39.73 m`): the `±0.5` bins reproduce the paper exactly: counts `95/73/121/153/160`; medians `0.182/0.324/0.312/0.225/0.156` for `r_uw`, `0.209/0.150/0.095/0.200/0.203` for `|r_wT|`; ratios `0.8680/2.1683/3.2768/1.1275/0.7675`; swing `4.2694`.
- The true `±1.0` bins give counts `51/117/121/228/85`, ratios `0.6613/1.7607/3.2768/1.1086/0.5820`, swing `5.6306`; they do **not** reproduce the paper. The v1.0.1 Option A assumption (paper is `±1.0`) was therefore wrong.
- The old artifact's `122/152` came from `month_diagnostics`' hard-coded z-d `39.7`; the paper/`run_stability.py` use the site value `39.73`. The 0.03 m shift moves one period from near-neutral to stable.
- The printed brackets were not actual 5--95% data ranges. Actual values are `0.045--0.480` / `0.050--0.640` (strongly unstable), `0.100--0.755` / `0.018--0.561` (unstable), `0.153--0.898` / `0.007--0.358` (near-neutral), `0.118--0.560` / `0.058--0.388` (stable), and `0.044--0.483` / `0.067--0.483` (strongly stable).
- Resolution: code remains at `±0.5`; paper row labels and footnote now say `±0.5`; brackets now use the actual 5--95% values; winter artifact regenerated at `±0.5`/`39.73` (counts `95/73/121/153/160`, swing `4.2694`); summer artifact unchanged. `REPORT_NEON_SEASONS.md` winter swing corrected `4.4x` -> `4.3x`. The caption now says “medians with measured 5--95% ranges over usable periods.”
- Robustness parenthetical added in `paper0_two_clocks.tex:167`: at coarser `±1.0` boundaries the winter swing is `5.6x` (counts `51/117/121/228/85`), explicitly answering the binning-artifact objection. This makes E3 binning-robust rather than weakening it.
- Process note: this is the second time a label/prose layer falsified correct code (the first was the `0.168/0.480` mapping). The recurring failure mode is the text that describes the numerics, not the numerics; the claim-map lint gate is therefore a release gate, not a post-release nicety; it was green for v1.0.1.
- Residual: the summer artifact was not raw-rerun because of the one-month data limit; it remains the prior `±0.5` artifact at z-d `39.7`. This does not affect the winter table or the paper's rounded summer swing `5.9x`.
- Candidate severity: S1 table/reproducibility, resolved; qualitative `4.3x` statement survives.

## F-C14 Winter temperature dominant period needs claim check

- Target: `figures/01b_neon_seasonal.json`
- Observation: winter `temp_dominant_period_h` is 60.49 h in the 6-240 h band; the paper says temperature is a "clean 24-hour signal." `tests/test_neon_seasonal.py` only asserts summer 20-28 h.
- Why it matters: "dominant period" depends on the band; a synoptic peak can dominate a wide band while the diurnal line remains clean. The caption should state the band or the test should check it.
- Candidate severity: S3.

## Cleared in Triage

- Taylor ratio 2.40 is invariant to the `sqrt(2)` convention; only absolute values change.
- ASOS `harmonic_amplitudes` uses time since the first sample; amplitude is shift-invariant, so the arbitrary origin is not a bug.
- `test_asos_ci.py` path resolution points at the repo root `figures/`, not `tests/figures/`; correct.
- `test_analysis.py` and `test_stability.py` are genuine synthetic unit tests, not artifact checks.
- The 3-D artifact `65_closure3d.json` matches the paper's headline divergence values; the issue is the construction/test oracle, not the stored numbers.
