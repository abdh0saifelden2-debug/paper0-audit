# Paper0 Claim Map

Audited repository: `/home/manem/Downloads/K1-two-clocks-theory`
Base commit: `e178c55` (`paper0-v1.0`)
Released audit target: `3e98346` (`paper0-v1.0.1`), CI-green
Manuscript: `paper0_two_clocks.tex`
Status values describe the base commit unless marked “fixed in v1.0.1”: `OPEN`, `SUPPORTED`, `PARTIAL`, `UNSUPPORTED`, `CONTRADICTED`, `UNVERIFIED`.

Status meaning:
- `SUPPORTED`: claim matches both the committed artifact and an independent/generative check.
- `PARTIAL`: artifact or code supports the claim, but the check is artifact-only, underpowered, or does not cover the full claim.
- `CONTRADICTED`: committed artifact or code directly conflicts with the stated claim.
- `UNVERIFIED`: no test, machine-readable artifact, or reproducible check was found.

## Observation Claims

| ID | Claim | Manuscript | Command | Module/function | Test | Artifact | Status |
|---|---|---|---|---|---|---|---|
| O1 | NEON WREF Jan 2020 has 1488 intervals, 1097 valid pressure, 1180 valid temperature | L59 | `run_analysis.py` | `neon_pt.loader`, `neon_pt.analysis` | `tests/test_neon_seasonal.py::test_winter_matches_paper_headlines` (artifact only) | `figures/01b_neon_seasonal.json` | PARTIAL |
| O2 | Winter temperature has a clean 24 h signal; pressure has a 12 h tide plus multi-day variability | L61-72 | `run_analysis.py` | `neon_pt.analysis` | `tests/test_analysis.py` helpers; no artifact test for the figure | `figures/01_diurnal_composites.png` | PARTIAL |
| O3 | Winter bulk daily P-T correlation is +0.07 | L74 | `run_analysis.py` | `neon_pt.analysis` | `tests/test_neon_seasonal.py::test_winter_matches_paper_headlines` (artifact only) | `figures/01b_neon_seasonal.json` | PARTIAL |
| O4 | Summer semidiurnal/diurnal temperature ratio drops 7.3% to 1.0%; pressure dominant 11.9 h at 8.5%; r=-0.49; pressure dominant 168 h; slope -0.024 vs +0.334 kPa/K | L76 | `run_neon_compare.py` | `neon_pt.analysis`, `neon_pt.stability` | `tests/test_neon_seasonal.py` (artifact only) | `figures/01b_neon_seasonal.json` | PARTIAL |
| O5 | ASOS 8 stations 24.6-47.4 N; semidiurnal pressure amplitude 1.10 to 0.34 hPa, monotonic; Haurwitz trend r=0.98; ratios 0.9-1.4 | L81-107 | `asos/fetch_iem.py && run_asos_ci.py` | `asos/loader.py`, `run_asos_ci.py` | `tests/test_asos_ci.py` (artifact only) | `figures/09b_asos_ci.json`, `figures/11b_tide_vs_latitude_ci.png` | PARTIAL |
| O6 | P-T coherence 0.82-0.98 at 24/12 h; 0.09-0.30 off-line; daily r -0.56 to -0.05 | L87, L111-113 | `run_asos_ci.py` | `run_asos_ci.py` | `tests/test_asos_ci.py` (artifact only; S1 untested) | `figures/09b_asos_ci.json` | CONTRADICTED at v1.0 for S1; S2 supported; fixed in v1.0.1 |
| O7 | RB: L_b=0.195, L_p=0.207, ratio 1.06; lambda_b=0.253, lambda_p=0.607, ratio 2.40; high-k power ratio ~1e4 at k~10 | L129-143 | `run_rb.py` | `run_rb.py` | No direct test; `tests/test_rb_ra_sweep.py` only checks the 2.40 artifact anchor | `figures/13_rb_fields.png`, `15_rb_spectra.png` | UNVERIFIED |
| O8 | Ra sweep: lambda ratio 2.58/2.94/4.45; L ratio 1.02/1.25/1.75; high-k gap widens ~70x | L148-160 | `run_rb_ra_sweep.py` | `run_rb_ra_sweep.py`, `run_rb.py` | `tests/test_rb_ra_sweep.py` (artifact only) | `figures/15b_rb_ra_sweep.json` | PARTIAL |
| O9 | Stability transport ratio swings 4.3x in winter (0.77-3.28) and 5.9x in summer (0.44-2.60); n=602/1030 | L167-181 | `run_stability.py` | `neon_pt.stability` | `tests/test_stability.py` helper tests only | `figures/12_stability_bins.png`, `figures/01b_neon_seasonal.json` | PARTIAL |
| O10 | Elliptic response spreads globally: 79% beyond one source width | L165, L203 | `run_elliptic_demo.py` | `subglacial/elliptic_demo.py` | No paper0 test; adjacent `tests/test_pressure_buoyancy_exchange.py` is unrelated | `figures/39_elliptic_pressure.png` | PARTIAL |

## Mechanism Claims

| ID | Claim | Manuscript | Command | Module/function | Test | Artifact | Status |
|---|---|---|---|---|---|---|---|
| M1 | Linear crossover: final relative error ~2e-3 for every c; t90 ~ 2.3 L/c; histories collapse in ct/L | L216-223 | `run_compressible.py` | `compressible/solver.py` | `tests/test_compressible.py` (3 tests; no slope test) | `figures/17_crossover.png` | PARTIAL |
| M2 | Mach sweep: KE_dil/KE_sol = 1.5e-4, 5.9e-4, 2.3e-3, 9.3e-3; pressure residual = 8.1e-4, 3.2e-3, 1.4e-2, 1.0e-1; both ~M^2 | L232-250 | `run_compressible_ns.py` | `compressible/ns.py` | No direct paper0 test; adjacent `tests/test_mach_regularity.py` | `figures/21_ns_mach_sweep.png`, `REPORT_NS.md` | UNVERIFIED |

## Surrogate and Beyond-the-Box Claims

| ID | Claim | Manuscript | Command | Module/function | Test | Artifact | Status |
|---|---|---|---|---|---|---|---|
| S1 | Projection: RMS div(u*) = 2.7e-2; projected = 2e-15 | L313, L323-326 | `run_boussinesq.py` | `boussinesq/solver.py` | No direct test for 2.7e-2; `test_spde_limit_ensemble` checks the surrogate artifact only | `figures/23_projection_step.png` | PARTIAL |
| S2 | Spectrum-matched surrogate: median abs(r)=0.07, p95=0.20, n=100; RMS div=3.7e-2 [3.5,3.8]e-2 vs 2.7e-2 uncorrected | L315, L333-338, L348 | `run_boussinesq.py` | `boussinesq/solver.py` | `tests/test_spde_limit_ensemble.py` (artifact only) | `figures/24_spde_limit_ensemble.json` | PARTIAL |
| S3 | 3-D periodic: true projection div=1.05e-14; projected-FDT=8.85e-15; surrogate=9.85; transfer corr ~0.9997 | L370, L385-387 | `run_closure3d.py` | `closure/sgs3d.py`, `closure/spectral3d.py`, `closure/dns3d.py` | `tests/test_closure3d.py` (14 structural tests) | `figures/65_closure3d.json` | PARTIAL |
| S4 | Channel: commutator 3e-16 in box, 2.3e-2 in channel, ratio 7e13, near-wall/bulk 34x; wall-normal velocity 0.513 vs 6e-15 | L372, L393-398 | `run_closure3d_bounded.py` | `closure/channel3d.py` | `tests/test_channel3d.py` (10 tests) | `figures/77_closure3d_bounded.json` | PARTIAL |

## Reanalysis Claims

| ID | Claim | Manuscript | Command | Module/function | Test | Artifact | Status |
|---|---|---|---|---|---|---|---|
| R1 | R1 daily KE_div/KE_rot = 4.0%, 0.7%, 1.0% at 850/500/250 hPa; R2 = 4.5%, 0.8%, 1.1%; minimum at 500 hPa | L417-433 | `run_reanalysis.py` | `reanalysis/ncep.py` | No direct test for levels; `test_reanalysis_crosscheck` only R2 | `figures/27_reanalysis_levels.png`, `figures/27b_reanalysis_crosscheck.json` | PARTIAL |
| R2 | Divergent branch 1-2 decades below rotational for all l <= 35 | L439, L459-461 | `run_reanalysis.py` | `reanalysis/ncep.py` | No direct test | `figures/26_reanalysis_ke_spectrum.png` | PARTIAL |
| R3 | R2 cross-check relative differences 15% or less | L443 | `run_reanalysis_r2.py` | `reanalysis/ncep.py` | `tests/test_reanalysis_crosscheck.py` (artifact only, threshold 0.30) | `figures/27b_reanalysis_crosscheck.json` | CONTRADICTED at v1.0; fixed in v1.0.1 |
| R4 | Daily mean divergent fraction is smaller than 6-hourly at every level; 500 hPa 0.7% vs 1.1% | L445, L468-471 | `run_reanalysis.py` | `reanalysis/ncep.py` | No direct test | `figures/27_reanalysis_levels.png`, `REPORT_REANALYSIS.md` | PARTIAL |

## Formal Claims

| ID | Claim | Manuscript | Formal target | Status |
|---|---|---|---|---|
| F1 | Finite cyclic-grid DFT inverse, Hermitian spectrum, admissible phase yields real field, Parseval, shell sums | L355 | `Parseval.lean` | PARTIAL |
| F2 | Antipodal phase gives -f, maximum L2 distance `2‖f‖` | L357 | `Antipodal.lean` | PARTIAL |
| F3 | Discrete Leray symbol kills its wavevector, symmetric, idempotent, even; P^2=P; spectral divergence ledger zero; zero-mode convention; Nyquist excluded | L359 | `Leray.lean`, `LerayBox.lean` | PARTIAL |
| F4 | Formal development pinned to `553d5c2`; exact over R/C; no floating-point/continuum claim | L361-363 | `STATEMENT_MATCH.md` | PARTIAL |

## Falsification Criteria

| ID | Claim | Kill condition | Status |
|---|---|---|---|
| E1 | Temporal split | Pressure and temperature show identical diurnal power ratios | UNVERIFIED |
| E2 | Spatial split | Taylor microscale ratio approaches unity at high Ra | PARTIAL |
| E3 | Transport efficiency | Momentum-to-heat ratio is constant across stability classes | PARTIAL |
| E4 | Crossover scaling | t90 does not scale as L/c in the compressible solver | PARTIAL — paper's `gamma∝c` gives `t90=2.2782 L/c`; fixed gamma gives no `L/c` law |
| E5 | Spectrum matching | Phase-randomized surrogate achieves machine-zero divergence | PARTIAL |
| E6 | Reanalysis split | Divergent kinetic energy exceeds 10% at any level | PARTIAL |

## Release Resolution

- `paper0-v1.0.1` (`3e98346`) fixes O6, F-C15, and R3; adds the F-C1/F-C2/F-C4 wording restrictions; and pins the CI dependencies.
- Claim-map lint: 3 checks passed. Pytest: `683 passed, 1 skipped`. Main CI `40021028585` green; tag workflow `40021921986` published the PDF.
- The gate is deliberately narrow: it covers the F-C15 table/swing/robustness, O6, and R3. F-C1, F-C2, and F-C4 are reviewed prose, not artifact-gated.
- The first CI run failed on O6 `0.4645` formatting (`0.464` vs paper `0.465`); the final checker compares printed values numerically.

## Evidence Notes

- O1/O3/O4/O8/O9: the committed artifacts match the quoted numbers. O1: `n_intervals=1488`, `n_valid_pressure=1097`, `n_valid_temperature=1180`, `pearson_r=0.07144`. O3/O4: winter `r=+0.0714`, summer `r=-0.4894`; slopes `+0.01416/-0.02438` vs gas-law `+0.35268/+0.33374 kPa/K`; summer pressure dominant `168.20 h`; summer S2 period `11.946 h`, power ratio `0.08486`; summer/winter temperature S2/S1 power ratio `0.00988/0.07273`. O8: medians `2.5816/2.9398/4.454`; L medians `1.0241/1.2497/1.747`; high-k medians `636.9/21809/46253`. O9: winter raw rerun (`RUNS/2026-10-23-fc15-neon/`) reproduces the `±0.5` table: counts `95/73/121/153/160`, ratios `0.8680/2.1683/3.2768/1.1275/0.7675`, swing `4.2694`; true `±1.0` gives `51/117/121/228/85`, swing `5.6306`. Summer remains the prior artifact (`5.9487`, counts total `1030`). Tables now use actual 5–95% ranges and `±0.5` labels; the paper adds the `±1.0` robustness parenthetical (`5.6306`, counts `51/117/121/228/85`).
- O2: artifact `temp_diurnal_period_h=23.64`, `temp_dominant_period_h=60.49` in the 6-240 h band. The 24 h line is present, but “clean 24 h” depends on the band; no artifact test of the figure.
- O5: artifact has 8 stations, strict S2 decay, `trend_corr=0.98366`, ratios `0.9386-1.3944`; latitude span `24.5561-47.4447`.
- O6: artifact `coh_S2=0.8203-0.9837`; `coh_S1=0.3971` (CAR), `0.4504` (DSM), `0.4645` (SEA), all below their `coh_S1_surr95` values (`0.5323`, `0.6130`, `0.5966`). `test_coherence_split` never checks S1.
- O7/M2: no machine-readable JSON and no direct paper0 test; values are report/PNG-level only.
- O10: `REPORT_ELLIPTIC_PRESSURE.md:23` reports 79%; `far_fraction` uses `r>0.6` while `sigma=0.18`, so “one source width” is not the literal threshold (F-C10).
- M1: `tests/test_compressible.py:39,57-67` sets `gamma=1.5*c/L` for every `c`; the test only asserts `t90(16)<t90(4)`. Dynamic F-C1 (`RUNS/2026-10-22-fc1-fixed-gamma/`): proportional `t90=2.2782 L/c`, R² `1.0`; fixed gamma 12/48 gives OLS slopes `0.158/0.267` with nonzero intercepts and no through-origin scaling. The claimed slope/collapse are imposed by the damping convention (F-C1).
- S1/S2: `rms_proj=2.26e-15`, surrogate `rms=0.03692` `[0.03479,0.03839]`, `median|r|=0.06972`, `p95=0.19814`, `n=100`; the input divergence is dynamically `2.7458e-2`, projection `2.225e-15`. The paper surrogate reproduces `3.7565e-2`; a common-phase surrogate preserving scalar and cross-spectra exactly (`rel_err=0.0`) still gives `3.6623e-2` (`1.33x` drift). The claim survives, but the paper should add this control and attribute failure to phase alignment, not cross-spectrum alone (F-C2).
- S3: artifact `true_projected_div`/`projected_fdt_div` are machine-small; `transfer_corrs.Smagorinsky=-0.6415`; alignment `0.47855/0.65358/0.32543`; backscatter `0.48015`; structural tests do not read the artifact. Alignment test lacks the e2-ordering assertion (F-C17); fixture is 32³/300 vs 128³/2500 artifact (F-C18); Smagorinsky test is sign-only (F-C19).
- S4: artifact `wall_div_interior=8.5356e-15`, `wall_div_full=0.0097097`, `wall_no_penetration=6.233e-15`, `wall_idempotency=5.137e-15`, `fourier_no_penetration=0.51318`, `input_div=1.9248`, `input_no_pen=0.79324`; commutator `periodic=3.0596e-16`, `channel=0.022558`, ratio `7.37e13`; near/bulk `33.81`, peak `0`. The k=0 gauge bottom-wall concern (F-C20) was cleared dynamically: six pure-k=0 profiles give wall residual at most `1.42e-14`, and a dual-wall reference agrees to `3.06e-14` (`RUNS/2026-10-21-k0-probe/`). The filter cutoffs remain in different units (F-C9), and the CI test still does not isolate k=0.
- R1/R2/R4: `REPORT_REANALYSIS.md` gives R1 `3.99/0.67/1.04%`, R2 `4.47/0.77/1.13%`, minimum at 500 hPa; R4 only checks 500 hPa (`0.67%` daily vs `1.12%` 6-hourly). No direct level/spectrum test. Confirmed static: daily is 24 daily means (24 days), inst is 24 six-hourly snapshots (6 days), and only 500 hPa is compared; “at every level” is unsupported (F-C4).
- R3: artifact `max_rel_diff=0.154581` (15.46%), with per-level `11.84/15.46/8.19%`; paper says 15% or less; test asserts `<0.30` (F-C5).
- F1-F4: pinned Lean stamp `553d5c2`; CI run `39588479578` succeeded; `STATEMENT_MATCH.md:346-356` maps §2b. This is a separate formal repo; no local recheck and no Python-test coverage.

## Coverage Gaps

- O1/O3/O4: only artifact consistency; no end-to-end NEON data test.
- O2: no artifact test for the figure; dominant-period band ambiguity.
- O5/O6: only artifact consistency; no end-to-end ASOS fetch/test.
- O7: no direct test of `run_rb.py`; only the sweep artifact anchor; no machine-readable headline artifact.
- O8: artifact-only; exact 2.40 anchor is a regression, not independent validation.
- O9: winter raw-verified; summer still artifact-level; helper unit tests only, no NEON stability artifact test.
- O10: no paper0 test for the 79% claim; far-field threshold label imprecise.
- M1: no test of the 2.3 slope or collapse in CI; dynamic F-C1 shows the slope is forced by `gamma∝c`; damping confound.
- M2: no direct paper0 test and no JSON artifact.
- S1: no test of the 2.7e-2 divergence or 2e-15 projection.
- S2: artifact-only; no test that the surrogate generator preserves the claimed spectrum or cross-spectrum.
- S3/S4: structural tests; do not read the committed headline artifacts; fixture-scale gaps. S4 k=0 is not isolated in CI, but the dynamic probe found wall residual <=1.42e-14, so this is a test gap rather than an observed bug.
- R1/R2/R4: no direct tests; R3 artifact-only and threshold-mismatched.
- F1-F4: separate Lean repository; not covered by Python tests.
