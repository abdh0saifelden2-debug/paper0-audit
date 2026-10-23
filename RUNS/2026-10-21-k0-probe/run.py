"""Kaggle probe: does `Channel3D.project_wall` enforce y=0 no-penetration for k_h=0?

Source is mounted read-only from `abduk5/k1-channel-probe-src` and is pinned by
SHA-256 to `closure/channel3d.py` at commit `e178c55`.

The probe compares the shipped projector with a reference 1-D solve that keeps
BOTH wall Neumann conditions and adds an explicit gauge (`mean(phi)=0`). For a
pure k_h=0 field, divergence is exactly Dy(v), so the two y-wall conditions are
compatible; the question is whether the shipped `phi[0]=0` gauge discards one of
them in practice.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import sys

import numpy as np

EXPECTED_SHA = "9d58e1cbdf72566136c4a5cdab455a590965c899a82f601571656ed199723f51"


def find_source():
    for root, _dirs, files in os.walk("/kaggle/input"):
        if "channel3d.py" in files and os.path.basename(root) == "closure":
            return os.path.dirname(root)
    raise SystemExit("closure/channel3d.py not found under /kaggle/input")


SRC = find_source()
PATH = os.path.join(SRC, "closure", "channel3d.py")
with open(PATH, "rb") as fh:
    sha = hashlib.sha256(fh.read()).hexdigest()
print("source:", PATH)
print("sha256:", sha)
if sha != EXPECTED_SHA:
    raise SystemExit(f"source hash mismatch: {sha} != {EXPECTED_SHA}")
sys.path.insert(0, SRC)

from closure.channel3d import Channel3D  # noqa: E402


def ref_k0(ch, v):
    """Reference k_h=0 projection: both wall BCs + mean(phi)=0 gauge."""
    ny = ch.ny
    v = np.asarray(v, dtype=float).reshape(ny)
    v3 = np.zeros((1, ny, 1), dtype=float)
    v3[0, :, 0] = v
    div = ch._apply_Dy(v3)[0, :, 0]  # exact Dy(v)
    A = []
    b = []
    # interior Poisson equations
    for j in range(1, ny - 1):
        A.append(ch.Dy2[j, :])
        b.append(div[j])
    # both no-penetration conditions
    A.append(ch.Dy[0, :])
    b.append(v[0])
    A.append(ch.Dy[-1, :])
    b.append(v[-1])
    # gauge: additive constant only
    A.append(np.ones(ny))
    b.append(0.0)
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    phi, *_ = np.linalg.lstsq(A, b, rcond=None)
    pv = v - ch.Dy @ phi
    return pv, phi


def make_field(ch, profile, horizontal="mean"):
    """u=w=0; v has only the kx=kz=0 horizontal mode with profile v(y)."""
    if horizontal != "mean":
        raise ValueError(horizontal)
    if len(profile) != ch.ny:
        raise ValueError((len(profile), ch.ny))
    v = np.broadcast_to(profile[None, :, None], (ch.nx, ch.ny, ch.nz)).copy()
    u = np.zeros((ch.nx, ch.ny, ch.nz))
    w = np.zeros((ch.nx, ch.ny, ch.nz))
    return u, v, w


def metrics(ch, v_before, v_after):
    v0b = float(v_before[0, 0, 0])
    vLb = float(v_before[-1, 0, 0])
    v0a = float(v_after[0, 0, 0])
    vLa = float(v_after[-1, 0, 0])
    return {
        "v_bottom_before": v0b,
        "v_top_before": vLb,
        "v_bottom_after": v0a,
        "v_top_after": vLa,
    }


def run_case(name, profile):
    ch = Channel3D(32, 49, 32, xp=np)
    u, v, w = make_field(ch, profile)
    pu, pv, pw = ch.project_wall(u, v, w)
    pv_ref, phi_ref = ref_k0(ch, profile)
    before = np.array([v[0, 0, 0], v[0, -1, 0]], dtype=float)
    after = np.array([pv[0, 0, 0], pv[0, -1, 0]], dtype=float)
    ref_after = np.array([pv_ref[0], pv_ref[-1]], dtype=float)
    wall_abs_max = float(max(np.max(np.abs(pv[:, 0, :])),
                             np.max(np.abs(pv[:, -1, :]))))
    div_abs_interior = float(np.sqrt(np.mean(
        ch.divergence(pu, pv, pw)[:, 1:-1, :] ** 2)))
    q = ch.project_wall(pu, pv, pw)[1]
    idem = float(np.sqrt(np.mean((q - pv) ** 2)) /
                 (np.sqrt(np.mean(pv ** 2)) + 1e-30))
    return {
        "case": name,
        "input_bottom_top": before.tolist(),
        "shipped_bottom_top": after.tolist(),
        "reference_bottom_top": ref_after.tolist(),
        "shipped_minus_reference_rms": float(np.sqrt(np.mean((pv - pv_ref[None, :, None]) ** 2))),
        "shipped_max_abs_wall_residual": float(np.max(np.abs(after))),
        "reference_max_abs_wall_residual": float(np.max(np.abs(ref_after))),
        "interior_div_rms": ch.divergence_rms_interior(pu, pv, pw),
        "interior_div_abs_rms": div_abs_interior,
        "full_div_rms": ch.divergence_rms(pu, pv, pw),
        "no_penetration_rms": ch.no_penetration_rms(pu, pv, pw),
        "wall_abs_max": wall_abs_max,
        "idempotency": idem,
    }


def main():
    y = np.linspace(0.0, 2.0, 49)
    rng = np.random.default_rng(0)
    profiles = {
        "constant_1": np.ones_like(y),
        "cos_pi_y_over_L": np.cos(np.pi * y / 2.0),
        "linear_y": y / 2.0,
        "random_nonzero_walls": rng.standard_normal(y.size),
        "pure_bottom_mode": np.exp(-((y - 0.0) / 0.15) ** 2),
        "pure_top_mode": np.exp(-((y - 2.0) / 0.15) ** 2),
    }
    out = {
        "source_sha256": sha,
        "environment": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "platform": platform.platform(),
            "accelerator": "cpu",
        },
        "grid": [32, 49, 32],
        "cases": [],
    }
    for name, profile in profiles.items():
        out["cases"].append(run_case(name, profile))
        print(json.dumps(out["cases"][-1], sort_keys=True))

    # Also test the artifact grid and a second ny, to rule out a grid accident.
    out["grid_sweep"] = []
    for ny in (33, 49, 65):
        ch = Channel3D(16, ny, 16, xp=np)
        prof = np.cos(np.pi * np.linspace(0.0, 2.0, ny) / 2.0)
        u, v, w = make_field(ch, prof)
        pu, pv, pw = ch.project_wall(u, v, w)
        rec = {
            "ny": ny,
            "before": [float(v[0, 0, 0]), float(v[0, -1, 0])],
            "after": [float(pv[0, 0, 0]), float(pv[0, -1, 0])],
            "max_abs_wall_residual": float(max(abs(pv[0, 0, 0]), abs(pv[0, -1, 0]))),
            "no_penetration_rms": ch.no_penetration_rms(pu, pv, pw),
        }
        out["grid_sweep"].append(rec)
        print(json.dumps(rec, sort_keys=True))

    path = "/kaggle/working/k0_probe.json"
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    print("wrote", path)


if __name__ == "__main__":
    main()
