# Release gate snapshot

Snapshot of the `paper0-v1.0.3` claim-map gate from
`K1-two-clocks-theory` commit `a0b6a45`. The gate files are unchanged from
v1.0.2; v1.0.3 is a layout-only release.

## Contents

- `CLAIM_MAP.md` — the release map and gate scope (upstream SHA-256
  `14060f0ec445dc8b11d4b7a7f67fd8f4721a077521130b2968f676b9507a5bb5`).
- `claims/fc15_winter.json` — verified F-C15 claim data (upstream SHA-256
  `6f2271d46c926820d35a9df267de220e0226df5fdc3e81abed8bc459ac8db7ef`;
  unchanged from v1.0.1).
- `figures/24b_spde_common_phase.json` — F-C2 common-phase control artifact
  (upstream SHA-256
  `49e6aa9a3f8927ea41321c303c9f50739002ec129094d073c6669f8f14fefe55`).
- `tools/check_claim_map.py` — vendored copy of the CI lint. Upstream SHA-256:
  `2299f4df921766ea867a8b9ff9e50f66e1d6900fa0fec49d1f4479bf52c273fc`.
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

The target checkout must be at `paper0-v1.0.3` (`a0b6a45`) or a commit with the
same checked files. The gate reads the target's paper, `REPORT_STABILITY.md`,
`neon_pt/stability.py`, `figures/01b_neon_seasonal.json`,
`figures/09b_asos_ci.json`, `figures/24b_spde_common_phase.json`,
`figures/27b_reanalysis_crosscheck.json`, and `claims/fc15_winter.json`.

## Verified result

The upstream gate ran in CI for PR #5, PR #6, and PR #7 and on `main`:

- claim-map lint: 5 checks passed;
- pytest: `683 passed, 1 skipped`;
- paper build and PDF check: passed;
- v1.0.3 adds a PDF text gate: `final state` and the full archive SHA-256 must
  survive `pdftotext`;
- released PDF SHA-256:
  `03e629b145dd6fbbf47b98488fbcd25fd1f3ca2f400691998149bbdc6865e9e4`
  (`2,357,555` bytes, 24 pages).

The gate covers F-C15 table/swing/robustness, O6 (including off-line coherence),
F-C2 common-phase control, manuscript disclosures, and R3. F-C1 and F-C4 are
reviewed prose, not artifact-gated. See the audit `CLAIM_MAP.md` for the broader
claim statuses.
