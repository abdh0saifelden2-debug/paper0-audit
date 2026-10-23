# k=0 channel wall-condition probe

## Purpose

Test F-C20: for horizontal modes with `k_h=0`, `Channel3D.project_wall` replaces
the y=0 Neumann row with the gauge `phi[0]=0`. The static concern was that a
nonzero k=0 wall-normal velocity could survive projection at y=0.

## Provenance

- Target source: `K1-two-clocks-theory` at `e178c55`
- Source file: `closure/channel3d.py`
- Source SHA-256: `9d58e1cbdf72566136c4a5cdab455a590965c899a82f601571656ed199723f51`
- Kaggle kernel: `abduk5/k1-channel-k0-probe`, version 6
- Dataset: `abduk5/k1-channel-probe-src`
- Environment: Python 3.13.15, NumPy 2.1.3, Linux x86_64, CPU
- Grid: `nx=32`, `ny=49`, `nz=32`; grid sweep `ny=33,49,65`
- Command: `kaggle kernels push -p /tmp/opencode/k1-k0-probe`

## Cases

Each field has `u=w=0` and a y-dependent `v`, so only horizontal `k=0` carries
wall-normal velocity:

- `constant_1`
- `cos_pi_y_over_L`
- `linear_y`
- `random_nonzero_walls`
- `pure_bottom_mode`
- `pure_top_mode`

The reference solve imposes both wall conditions plus a zero-mean gauge and
solves the same k=0 pressure equation.

## Result

All values are absolute residuals in grid units.

| Case | Shipped wall max | Interior div ABS RMS | Shipped minus reference RMS |
|---|---:|---:|---:|
| constant_1 | 1.42e-14 | 3.38e-14 | 3.06e-14 |
| cos_pi_y_over_L | 9.99e-15 | 1.40e-14 | 9.56e-15 |
| linear_y | 9.98e-15 | 2.32e-14 | 1.72e-14 |
| random_nonzero_walls | 4.97e-15 | 1.15e-14 | 7.35e-15 |
| pure_bottom_mode | 8.88e-16 | 5.60e-15 | 1.35e-15 |
| pure_top_mode | 6.34e-16 | 1.18e-15 | 1.71e-15 |

Grid sweep (`cos_pi_y_over_L`): wall max `4.44e-16` (ny=33), `9.99e-15`
(ny=49), `1.23e-14` (ny=65).

## Interpretation

- F-C20 is cleared for the tested k=0 scope. The gauge substitution did not
  introduce a detectable bottom-wall residual, including pure bottom and top
  modes and a field with nonzero wall values at both walls.
- Both shipped and reference fields satisfy both walls to about `1e-14`, so
  the artifact's `wall_no_penetration=6.23e-15` is consistent with this path.
- The test gap remains: `test_project_wall_enforces_no_penetration` does not
  isolate k=0, so this behavior is not protected by CI.

## Caveats

- This is a synthetic, single-grid, CPU test; it does not replay the full
  `run_closure3d_bounded.py` artifact field.
- The probe's normalized `no_penetration_rms` and `interior_div_rms` divide by
  a field scale that is ~`1e-14` for the zeroed constant field. Those ratios
  are not physical for that case; use `wall_abs_max` and
  `interior_div_abs_rms` instead.
- Only the declared channel source at `e178c55` was tested.
