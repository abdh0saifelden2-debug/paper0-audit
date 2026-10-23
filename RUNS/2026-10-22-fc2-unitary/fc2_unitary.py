"""F-C2: does a cross-spectrum-preserving unitary surrogate enforce div=0?

Read-only audit probe against the Boussinesq drift at e178c55. Compares:
  * independent component phase randomization (paper's surrogate);
  * a global rotation of the gradient correction (unitary, exact cross-spectrum);
  * a k-dependent unitary rotation (unitary, exact per-mode cross-spectrum).
The residual is div(us - surrogate correction), the quantity in Fig. 24.
"""
from __future__ import annotations

import glob
import json
import platform
import sys
from pathlib import Path

import numpy as np

for cand in glob.glob("/kaggle/input/**/compressible", recursive=True):
    sys.path.insert(0, str(Path(cand).parent))
    break
from compressible.ns import Spectral2D, helmholtz  # noqa: E402
from boussinesq.solver import (  # noqa: E402
    BoussinesqProjection, BoussinesqState, divergence, project, warm_blobs,
)

NU = 2e-3
KAPPA = 2e-3
DT_CAP = 0.02
N = 128
T_END = 6.0


def _rms(a):
    return float(np.sqrt(np.mean(np.asarray(a) ** 2)))


def simulate(n, t_end):
    solver = BoussinesqProjection(n, NU, KAPPA, cfl=0.4)
    u, v, b = warm_blobs(solver.sp)
    u, v = project(solver.sp, u, v)
    st = BoussinesqState(u, v, b, 0.0)
    while st.t < t_end:
        dt = min(solver.dt_cfl(st), DT_CAP)
        solver.step(st, dt)
        if not np.isfinite(st.u).all():
            raise RuntimeError(f"diverged at t={st.t}")
    return solver, st


def phase_randomized(sp, f, seed):
    amp = np.abs(sp.fft(f))
    rng = np.random.default_rng(seed)
    rand_phase = np.angle(sp.fft(rng.standard_normal(f.shape)))
    return sp.ifft(amp * np.exp(1j * rand_phase))


def phase_common(sp, ud, vd, seed):
    """Apply the SAME random phase to both components: exact scalar and cross-spectrum."""
    rng = np.random.default_rng(seed)
    phase = np.angle(sp.fft(rng.standard_normal(ud.shape)))
    return (sp.ifft(sp.fft(ud) * np.exp(1j * phase)),
            sp.ifft(sp.fft(vd) * np.exp(1j * phase)))


def rotate_global(ud, vd, theta):
    c, s = np.cos(theta), np.sin(theta)
    return c * ud - s * vd, s * ud + c * vd


def rotate_kdep(sp, ud, vd, theta0):
    udh, vdh = sp.fft(ud), sp.fft(vd)
    kr = np.sqrt(sp.k2)
    safe = np.where(kr > 0, kr, 1.0)
    theta = theta0 * sp.kx / safe
    theta[0, 0] = 0.0
    c, s = np.cos(theta), np.sin(theta)
    xuh = c * udh - s * vdh
    xvh = s * udh + c * vdh
    return sp.ifft(xuh), sp.ifft(xvh)


def cross_spectrum(sp, u, v):
    return np.real(sp.fft(u) * np.conj(sp.fft(v)))


def metrics(sp, us, vs, ud, vd, xu, xv):
    div_star = divergence(sp, us, vs)
    div_surr = divergence(sp, us - xu, vs - xv)
    div_corr = divergence(sp, xu, xv)
    ref = cross_spectrum(sp, ud, vd)
    got = cross_spectrum(sp, xu, xv)
    return {
        "div_star_rms": _rms(div_star),
        "div_surrogate_rms": _rms(div_surr),
        "div_correction_rms": _rms(div_corr),
        "surrogate_div_ratio": _rms(div_surr) / _rms(div_star),
        "cross_spectrum_rel_err": float(
            np.linalg.norm(got - ref) / max(np.linalg.norm(ref), 1e-30)
        ),
        "corr_ud_xu": float(np.corrcoef(ud.ravel(), xu.ravel())[0, 1]),
        "corr_vd_xv": float(np.corrcoef(vd.ravel(), xv.ravel())[0, 1]),
    }


def main():
    solver, st = simulate(N, T_END)
    sp = solver.sp
    us, vs = solver.drift_velocity(st, DT_CAP)
    up, vp = project(sp, us, vs)
    ud, vd = helmholtz(sp, us, vs)[2:]

    out = {
        "probe": "F-C2 unitary surrogate",
        "environment": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "platform": platform.platform(),
            "accelerator": "cpu",
        },
        "n": N,
        "t_end": T_END,
        "t_final": float(st.t),
        "correction_norm": float(np.linalg.norm(ud)),
        "div_proj_rms": _rms(divergence(sp, up, vp)),
        "checks": {},
    }
    xu, xv = phase_common(sp, ud, vd, 11)
    out["checks"]["common_phase_cross_spectrum_preserving"] = metrics(
        sp, us, vs, ud, vd, xu, xv
    )
    out["checks"]["paper_independent_phase"] = metrics(
        sp, us, vs, ud, vd,
        phase_randomized(sp, ud, 11), phase_randomized(sp, vd, 12),
    )
    for deg in (30.0, 60.0, 90.0):
        th = np.deg2rad(deg)
        xu, xv = rotate_global(ud, vd, th)
        out["checks"][f"unitary_global_{deg:g}deg"] = metrics(
            sp, us, vs, ud, vd, xu, xv
        )
    xu, xv = rotate_kdep(sp, ud, vd, 1.0)
    out["checks"]["unitary_kdep_1rad"] = metrics(
        sp, us, vs, ud, vd, xu, xv
    )
    xu, xv = rotate_kdep(sp, ud, vd, 2.0)
    out["checks"]["unitary_kdep_2rad"] = metrics(
        sp, us, vs, ud, vd, xu, xv
    )
    print(json.dumps(out, indent=2))
    Path("/kaggle/working/fc2_unitary.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
