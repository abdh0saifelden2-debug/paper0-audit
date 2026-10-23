# F-C2 unitary / cross-spectrum-preserving surrogate

- Run: Kaggle kernel `abduk5/k1-f-c2-unitary`, version 3, `COMPLETE`.
- URL: https://www.kaggle.com/code/abduk5/k1-f-c2-unitary
- Source revision: target at `e178c55`; hashes in `SOURCE_REV.txt`.
- Kernel source dataset: `abduk5/k1-fc2-unitary-src`.
- Environment: Python 3.13.15, NumPy 2.1.3, Linux x86_64, CPU.
- Setup: Boussinesq drift at `n=128`, `t_end=6`; `us,vs = solver.drift_velocity(st, 0.02)`; `ud,vd = helmholtz(us,vs)[2:]`; residual metric is `div(us - surrogate_correction)`.
- `div_star` is `2.7458e-2`; deterministic projection is `2.225e-15`.

## Results

| surrogate | residual div RMS | / div_star | cross-spectrum rel. error |
|---|---:|---:|---:|
| paper independent phase (`seed=11/12`) | 3.7565e-02 | 1.368 | 0.821 |
| **common phase, both components** | **3.6623e-02** | **1.334** | **0.0** |
| global unitary rotation 30 deg | 3.679e-03 | 0.134 | 2.40 |
| global unitary rotation 60 deg | 1.3729e-02 | 0.500 | 2.84 |
| global unitary rotation 90 deg | 2.7458e-02 | 1.000 | 2.00 |
| k-dependent unitary 1 rad | 6.744e-03 | 0.246 | 0.392 |
| k-dependent unitary 2 rad | 2.1942e-02 | 0.799 | 0.827 |

The paper's single-realization surrogate reproduces its reported `3.76e-2` (artifact median `3.69e-2`). The common-phase control applies the **same random phase to both components**; it preserves the scalar spectra and the component cross-spectrum exactly (`rel_err≈2.1e-16`) while randomizing phase relative to the drift. It still leaves residual divergence `3.66e-2`, `1.33x` the uncorrected drift and far above the `2.2e-15` projection.

The global/k-dependent rotations preserve vector energy but **not** the component cross-spectrum (`u v*`); they are reported as unitary controls, not as cross-spectrum-preserving surrogates. A 30-degree rotation can reduce residual divergence because it partially aligns with the removed gradient; this is not evidence that cross-spectrum preservation is sufficient.

## Interpretation

- F-C2's original objection is valid: independent phase randomization destroys the cross-spectrum, so the paper's surrogate failure is partly built in.
- The stronger control removes that objection: a surrogate preserving both scalar and cross-spectra still fails. The missing structure is the phase/alignment of the correction relative to the drift, not only its cross-spectrum.
- The paper's high-level “energy yes, structure no” conclusion survives; §4.2 should report the common-phase control and stop attributing failure solely to lost cross-spectrum.
