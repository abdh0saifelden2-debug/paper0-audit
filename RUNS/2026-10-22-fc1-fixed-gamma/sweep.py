"""F-C1: fixed-gamma vs gamma proportional to c for the acoustic crossover.

Read-only audit probe. Uses the target solver at e178c55 without editing it.
"""
from __future__ import annotations

import glob
import json
import platform
import sys
import zipfile
from pathlib import Path

import numpy as np

for cand in glob.glob("/kaggle/input/**/compressible", recursive=True):
    sys.path.insert(0, str(Path(cand).parent))
    break
for zpath in glob.glob("/kaggle/input/**/compressible.zip", recursive=True):
    with zipfile.ZipFile(zpath) as zf:
        zf.extractall("/kaggle/working/src")
    break
for solver in glob.glob("/kaggle/working/src/**/solver.py", recursive=True):
    sys.path.insert(0, str(Path(solver).parent.parent))
    break

from compressible.solver import (  # noqa: E402
    LinearAcoustics2D,
    gaussian_bump,
    gradient_forcing,
    poisson_fft,
)

SOURCE_SHA = "027e1f3dcba8bc0dd9992f239076232c46dc40adb65c9a192ee8509e3ac18dfb"
N = 128
L = 1.0
C_VALUES = [4.0, 8.0, 16.0, 32.0]
CROSSINGS = 20.0
THRESH = 0.10
CONVENTIONS = [
    ("proportional_1.5c_L", None),
    ("fixed_gamma_12", 12.0),
    ("fixed_gamma_48", 48.0),
]


def make_problem(n: int, L: float):
    dx = L / n
    psi = gaussian_bump(n, L, x0=L / 2, y0=L / 2, sigma=0.10, amp=1.0)
    fx, fy = gradient_forcing(psi, dx)
    div_f = (np.roll(fx, -1, 0) - np.roll(fx, 1, 0)) / (2 * dx) \
        + (np.roll(fy, -1, 1) - np.roll(fy, 1, 1)) / (2 * dx)
    p_ell = poisson_fft(div_f, dx)
    p_ell -= p_ell.mean()
    return fx, fy, p_ell, float(np.linalg.norm(p_ell))


def run_case(c: float, gamma: float, fx, fy, p_ell, norm_ell):
    sim = LinearAcoustics2D(N, L, c, rho0=1.0, gamma=gamma, cfl=0.4)
    t_end = CROSSINGS * L / c
    t_hist = []
    e_hist = []
    while sim.state.t < t_end - 1e-12:
        p = sim.state.p - sim.state.p.mean()
        t_hist.append(sim.state.t)
        e_hist.append(float(np.linalg.norm(p - p_ell) / norm_ell))
        sim.step(fx=fx, fy=fy)
    t = np.asarray(t_hist)
    e = np.asarray(e_hist)
    below = np.where(e < THRESH)[0]
    t90 = float(t[below[0]]) if below.size else None
    idx = np.linspace(0, len(t) - 1, min(400, len(t))).astype(int)
    return {
        "c": c,
        "gamma": gamma,
        "dt": float(sim.dt),
        "steps": int(len(t)),
        "t_end": float(t_end),
        "t90": t90,
        "final_error": float(e[-1]),
        "error_at_crossings": {
            str(x): float(np.interp(x, t * c / L, e)) for x in [1, 2, 4, 8, 16]
        },
        "t": t[idx].tolist(),
        "err": e[idx].tolist(),
    }


def fit_scaling(cases):
    finite = [r for r in cases if r["t90"] is not None]
    if len(finite) < 2:
        return None
    x = np.array([1.0 / r["c"] for r in finite])
    y = np.array([r["t90"] for r in finite])
    slope0 = float(np.sum(x * y) / np.sum(x * x))
    pred0 = slope0 * x
    r2_0 = float(1.0 - np.sum((y - pred0) ** 2) / np.sum((y - y.mean()) ** 2))
    slope, intercept = np.polyfit(x, y, 1)
    pred = slope * x + intercept
    r2 = float(1.0 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2))
    return {
        "n": len(finite),
        "slope_origin": slope0,
        "r2_origin": r2_0,
        "slope_ls": float(slope),
        "intercept_ls": float(intercept),
        "r2_ls": r2,
    }


def collapse_metric(cases):
    grid = np.linspace(0.5, 16.0, 63)
    curves = []
    for r in cases:
        t = np.asarray(r["t"])
        e = np.asarray(r["err"])
        s = t * r["c"] / L
        curves.append(np.interp(grid, s, e))
    arr = np.asarray(curves)
    mean = arr.mean(axis=0)
    spread = np.sqrt(np.mean((arr - mean) ** 2, axis=0))
    rel = spread / np.maximum(mean, 1e-12)
    return {
        "grid": grid.tolist(),
        "rms_relative_spread": float(np.sqrt(np.mean(rel ** 2))),
        "max_relative_spread": float(rel.max()),
    }


def main():
    fx, fy, p_ell, norm_ell = make_problem(N, L)
    out = {
        "probe": "F-C1 fixed-gamma crossover",
        "source_sha256": SOURCE_SHA,
        "environment": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "platform": platform.platform(),
            "accelerator": "cpu",
        },
        "grid": [N, N],
        "L": L,
        "crossings": CROSSINGS,
        "threshold": THRESH,
        "c_values": C_VALUES,
        "conventions": [],
    }
    for label, fixed_gamma in CONVENTIONS:
        cases = []
        for c in C_VALUES:
            gamma = 1.5 * c / L if fixed_gamma is None else fixed_gamma
            r = run_case(c, gamma, fx, fy, p_ell, norm_ell)
            cases.append(r)
            print(f"{label:22s} c={c:5g} gamma={gamma:8.3f} "
                  f"t90={r['t90']} final={r['final_error']:.3e}")
        out["conventions"].append({
            "label": label,
            "fixed_gamma": fixed_gamma,
            "cases": cases,
            "fit": fit_scaling(cases),
            "collapse": collapse_metric(cases),
        })
    print(json.dumps(out, indent=2)[:1500])
    Path("/kaggle/working/fc1_sweep.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
