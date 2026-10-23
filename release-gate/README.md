# Release gate snapshot

Snapshot of the `paper0-v1.0.1` claim-map gate from
`K1-two-clocks-theory` commit `3e98346`.

## Contents

- `CLAIM_MAP.md` — the release map and gate scope (upstream SHA-256
  `6d571e70c00f0d0d9282424be156331636e70c29c7df42fadd69015db5cba8f1`).
- `claims/fc15_winter.json` — verified F-C15 claim data (upstream SHA-256
  `6f2271d46c926820d35a9df267de220e0226df5fdc3e81abed8bc459ac8db7ef`).
- `tools/check_claim_map.py` — vendored copy of the CI lint. Upstream SHA-256:
  `71d09b795a5fcaf00587232b60830ba51cd49e6ccfd1e6a19be6cc563368d418`.
- `tools/run.sh` — convenience runner that points the vendored copy at a target
  checkout.

## Run

```bash
./tools/run.sh /path/to/K1-two-clocks-theory
```

or:

```bash
PAPER0_ROOT=/path/to/K1-two-clocks-theory python3 tools/check_claim_map.py
```

The vendored script differs from upstream only in how it locates the target
checkout: it reads `PAPER0_ROOT` and otherwise defaults to a sibling
`K1-two-clocks-theory` directory. The checks are unchanged.

The target checkout must be at `paper0-v1.0.1` (`3e98346`) or a commit with the
same checked files. The gate reads the target's paper, `REPORT_STABILITY.md`,
`neon_pt/stability.py`, `figures/01b_neon_seasonal.json`,
`figures/09b_asos_ci.json`, `figures/27b_reanalysis_crosscheck.json`, and
`claims/fc15_winter.json`.

## Verified result

The upstream gate ran in CI for PR #4 and on `main`:

- claim-map lint: 3 checks passed;
- pytest: `683 passed, 1 skipped`;
- paper build and PDF check: passed.

The gate is deliberately narrow: F-C15 table/swing/robustness, O6, and R3. F-C1,
F-C2, and F-C4 are reviewed prose, not artifact-gated. See the audit
`CLAIM_MAP.md` for the broader claim statuses.
