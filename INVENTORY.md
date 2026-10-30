# Paper0 Inventory

## Repository

- Path: `/home/manem/Downloads/K1-two-clocks-theory`
- Base commit: `e178c55`
- Base tag: `paper0-v1.0`
- Base release: `https://github.com/abdh0saifelden2-debug/K1-two-clocks-theory/releases/tag/paper0-v1.0`
- Released audit target: `239aff9`, tag `paper0-v1.0.2`
- Current release: `https://github.com/abdh0saifelden2-debug/K1-two-clocks-theory/releases/tag/paper0-v1.0.2`
- Working tree at audit start: clean, `main...origin/main`
- Split audit: 451 traced files, 448 byte-identical, 3 modified, 1 new; 78 test files in the split (3 relocated to K2).

## Paper0 Commands

1. `python run_analysis.py`
2. `python run_neon_compare.py`
3. `python asos/fetch_iem.py && python run_asos_ci.py`
4. `python run_rb.py`
5. `python run_rb_ra_sweep.py`
6. `python run_elliptic_demo.py`
7. `python run_stability.py`
8. `python run_compressible.py`
9. `python run_compressible_ns.py`
10. `python run_boussinesq.py`
11. `python run_closure3d.py` (GPU via CuPy)
12. `python run_closure3d_bounded.py`
13. `python run_reanalysis.py`
14. `python run_reanalysis_r2.py`

## Core Test Scope

- 10 files, 54 test functions.
- 19 artifact-only: `test_neon_seasonal.py` (5), `test_asos_ci.py` (5), `test_rb_ra_sweep.py` (5), `test_spde_limit_ensemble.py` (3), `test_reanalysis_crosscheck.py` (1).
- 35 non-artifact: `test_analysis.py` (4), `test_stability.py` (4), `test_compressible.py` (3), `test_closure3d.py` (14), `test_channel3d.py` (10).
- Only `tests/test_channel3d.py` imports a `run_` script among the paper0-critical files.
- No `conftest.py`; tests use module-level fixtures and committed artifacts.
- `run_rb.py` has no direct test; `run_elliptic_demo.py` and `run_compressible_ns.py` have no paper0-critical tests.

## Test Inventory

| # | Test | Line | Initial oracle |
|---|---|---|---|
| 1 | `tests/test_analysis.py::test_lagged_xcorr_recovers_known_lag` | 19 | analytic |
| 2 | `tests/test_analysis.py::test_spectrum_finds_diurnal_and_semidiurnal` | 30 | analytic |
| 3 | `tests/test_analysis.py::test_coupling_decoupled_when_density_varies` | 42 | analytic/invariant |
| 4 | `tests/test_analysis.py::test_qc_drops_out_of_range` | 56 | invariant |
| 5 | `tests/test_neon_seasonal.py::test_two_months_same_site` | 17 | artifact |
| 6 | `tests/test_neon_seasonal.py::test_winter_matches_paper_headlines` | 22 | artifact |
| 7 | `tests/test_neon_seasonal.py::test_fingerprint_persists_both_seasons` | 28 | artifact |
| 8 | `tests/test_neon_seasonal.py::test_coupling_regime_dependent_never_locked` | 43 | artifact |
| 9 | `tests/test_neon_seasonal.py::test_transport_ratio_swing_both_seasons` | 53 | artifact |
| 10 | `tests/test_asos_ci.py::test_ladder_size_and_span` | 18 | artifact |
| 11 | `tests/test_asos_ci.py::test_s2_declines_monotonically_with_cis` | 25 | artifact |
| 12 | `tests/test_asos_ci.py::test_haurwitz_protocol_validation` | 34 | artifact |
| 13 | `tests/test_asos_ci.py::test_coherence_split` | 40 | artifact |
| 14 | `tests/test_asos_ci.py::test_no_tight_positive_daily_lock` | 48 | artifact |
| 15 | `tests/test_rb_ra_sweep.py::test_three_ra_at_pr1` | 17 | artifact |
| 16 | `tests/test_rb_ra_sweep.py::test_taylor_ratio_above_one_and_widening` | 23 | artifact |
| 17 | `tests/test_rb_ra_sweep.py::test_paper_headline_anchor` | 31 | artifact/regression |
| 18 | `tests/test_rb_ra_sweep.py::test_integral_ratio_stays_order_one` | 39 | artifact |
| 19 | `tests/test_rb_ra_sweep.py::test_highk_suppression_grows` | 44 | artifact |
| 20 | `tests/test_stability.py::test_air_density_ideal_gas` | 9 | analytic |
| 21 | `tests/test_stability.py::test_derive_sign_of_stability` | 17 | analytic |
| 22 | `tests/test_stability.py::test_transport_efficiency_formula` | 36 | analytic |
| 23 | `tests/test_stability.py::test_summary_ratio_varies_with_made_up_classes` | 54 | synthetic/invariant |
| 24 | `tests/test_compressible.py::test_poisson_fft_recovers_known_field` | 13 | analytic |
| 25 | `tests/test_compressible.py::test_acoustic_steady_state_matches_elliptic` | 26 | analytic |
| 26 | `tests/test_compressible.py::test_higher_c_relaxes_faster` | 45 | weak monotonic |
| 27 | `tests/test_spde_limit_ensemble.py::test_ensemble_size_and_schema` | 22 | artifact |
| 28 | `tests/test_spde_limit_ensemble.py::test_correlation_small_but_honestly_scattered` | 29 | artifact |
| 29 | `tests/test_spde_limit_ensemble.py::test_divergence_ceiling_is_structural` | 38 | artifact |
| 30 | `tests/test_reanalysis_crosscheck.py::test_crosscheck_artifact` | 9 | artifact |
| 31 | `tests/test_closure3d.py::test_dns_produces_nonzero_field` | 32 | structural |
| 32 | `tests/test_closure3d.py::test_dns_field_is_nearly_divergence_free` | 38 | invariant |
| 33 | `tests/test_closure3d.py::test_exact_sgs_force_is_solenoidal` | 44 | invariant |
| 34 | `tests/test_closure3d.py::test_smagorinsky_is_solenoidal` | 50 | invariant |
| 35 | `tests/test_closure3d.py::test_surrogate_breaks_solenoidality` | 57 | structural |
| 36 | `tests/test_closure3d.py::test_projected_fdt_is_solenoidal` | 64 | invariant |
| 37 | `tests/test_closure3d.py::test_smagorinsky_is_purely_dissipative` | 71 | structural |
| 38 | `tests/test_closure3d.py::test_projected_fdt_tracks_true_transfer` | 79 | weak correlation |
| 39 | `tests/test_closure3d.py::test_sharp_filter_removes_high_modes` | 90 | invariant |
| 40 | `tests/test_closure3d.py::test_force_spectrum_parseval` | 97 | invariant |
| 41 | `tests/test_closure3d.py::test_vortex_stretching_zero_for_2d_flow` | 110 | analytic |
| 42 | `tests/test_closure3d.py::test_vortex_stretching_nonzero_and_positive_in_3d` | 122 | structural |
| 43 | `tests/test_closure3d.py::test_smagorinsky_has_zero_backscatter_fraction` | 131 | structural |
| 44 | `tests/test_closure3d.py::test_strain_vorticity_alignment_valid` | 140 | invariant |
| 45 | `tests/test_channel3d.py::test_project_wall_is_divergence_free_interior` | 35 | invariant |
| 46 | `tests/test_channel3d.py::test_project_wall_enforces_no_penetration` | 42 | invariant |
| 47 | `tests/test_channel3d.py::test_project_wall_is_idempotent` | 49 | invariant |
| 48 | `tests/test_channel3d.py::test_project_wall_actually_changes_a_divergent_field` | 57 | structural |
| 49 | `tests/test_channel3d.py::test_naive_projector_violates_no_penetration` | 66 | structural |
| 50 | `tests/test_channel3d.py::test_periodic_commutator_vanishes` | 78 | invariant |
| 51 | `tests/test_channel3d.py::test_wall_breaks_filter_projector_commutation` | 85 | structural |
| 52 | `tests/test_channel3d.py::test_commutator_is_wall_localized` | 95 | structural |
| 53 | `tests/test_channel3d.py::test_sharp_filter_band_limits_horizontally` | 110 | invariant |
| 54 | `tests/test_channel3d.py::test_reproducible` | 120 | regression |

## Adjacent Tests Not in Paper0 Core

- `tests/test_temporal_clocks.py` (3): temporal-clock diagnostics, not in the paper0 command table.
- `tests/test_mach_regularity.py`: Mach-to-zero bridge; adjacent to M2 but not `run_compressible_ns.py`.
- `tests/test_pressure_buoyancy_exchange.py`: paper2 pressure-mediated buoyancy; unrelated to O10.
- 68+ other split tests: out of scope unless a paper0 claim depends on them.

## Data Map

| Script | Input | Availability | Notes |
|---|---|---|---|
| `run_analysis.py` | NEON DP4.00200.001 `.h5` under `data/` | Missing | `data/` has 14 unrelated JSON caches, 2.6 MB |
| `run_neon_compare.py` | `/home/data_neon_jan2020`, `/home/data_neon_jul2020` | Missing | Defaults are absolute paths |
| `run_asos_ci.py` | IEM ASOS cache from `asos/fetch_iem.py` | Fetchable | 8 stations, Q1 2020 |
| `run_rb.py` | `data_rb/rb_Ra1e6_Pr1.hdf5` | Missing | The Well 2D RB, 512x128, 200 steps; each file ~8.4 GB |
| `run_rb_ra_sweep.py` | The Well Ra 1e6/1e7/1e8 Pr=1 | Missing | 5 trajectories x 6 snapshots; full ensemble 342 GB |
| `run_elliptic_demo.py` | none | Available | CPU |
| `run_stability.py` | NEON WREF | Raw used remotely; not retained | F-C15 winter rerun from `DP4.00200.001` 2020-01 basic (RELEASE-2026), 153.8 MB, in `RUNS/2026-10-23-fc15-neon/` |
| `run_compressible.py` | none | Available | CPU |
| `run_compressible_ns.py` | none | Available | CPU |
| `run_boussinesq.py` | none | Available | CPU |
| `run_closure3d.py` | none | Available | GPU/CuPy |
| `run_closure3d_bounded.py` | none | Available | CPU |
| `run_reanalysis.py` | NOAA PSL OPeNDAP | Fetchable | R1 2021, `nt=24` |
| `run_reanalysis_r2.py` | NOAA PSL OPeNDAP | Fetchable | R2 cross-check |

## Environment

- `requires-python = ">=3.10"`.
- Base `requirements.txt`: `numpy>=1.24`, unpinned upper bounds; v1.0.1 sets `numpy>=2.0` and `pytest==8.3.5`.
- Base CI installed `requirements.txt` with `|| true`, then unpinned `pytest numpy scipy matplotlib`; v1.0.1 installs only `requirements.txt`.
- No `conftest.py`; test paths via `pyproject.toml`.
- `np.trapezoid` in `run_rb.py:60` requires NumPy >= 2.0, above the declared minimum.

## Artifact Anchors

- `figures/01b_neon_seasonal.json`: winter `n_valid_pressure=1097`, `n_valid_temperature=1180`, `pearson_r=0.07`; v1.0.1 winter counts `95/73/121/153/160`, swing `4.2694`; summer unchanged.
- `figures/09b_asos_ci.json`: 8-station amplitude ladder and CIs.
- `figures/15b_rb_ra_sweep.json`: `lambda_ratio_median` 2.40 at Ra=1e6; high-k medians 636 / 21809 / 46253.
- `figures/24_spde_limit_ensemble.json`: n=100; rms_proj=2.26e-15; rms_surr_median=0.03692; corr_abs_median=0.0697.
- `figures/24b_spde_common_phase.json`: common-phase F-C2 control; `div_star_rms=0.0274581`, `div_surrogate_rms=0.0366233`, ratio `1.33379`, cross-spectrum error `2.1393e-16`, projection `2.2245e-15`; lint-gated in v1.0.2.
- `figures/27b_reanalysis_crosscheck.json`: max_rel_diff=0.15458.
- `figures/65_closure3d.json`: div truth=1.05e-14, surrogate=9.85; transfer corr projected-FDT=0.999722.
- `figures/77_closure3d_bounded.json`: commutator periodic=3.06e-16, channel=0.02256; wall_div_full=0.00971.
