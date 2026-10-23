# F-C15 raw NEON rerun (2026-10-23)

One-month raw-data check for the stability table (F-C15), using the user's
one-month data limit.

## Source

- Product: `DP4.00200.001` (NEON SAE), site `WREF`
- Month: `2020-01`, package `basic`
- Release: `RELEASE-2026`
- File: `NEON.D16.WREF.DP4.00200.001.nsae.2020-01.basic.20260115T205811Z.h5`
- Size: `153,801,332` bytes
- MD5: `8e7621c78be196cb1991f1dd1eca64c8`
- z-d: `39.73 m` (the site value used by `run_stability.py` and the paper)
- NEON token was mounted from a private ephemeral Kaggle dataset and is not
  stored in this repository.

## Runners

- `abduk5/k1-fc15-winter` v6: full one-month rerun and winter artifact update
- `abduk5/k1-fc15-bins` v4: `±0.5` vs `±1.0` bin comparison, actual percentile
  ranges, and percentile bootstrap of the class medians

## Results

All sets have `602` usable 30-min periods.

| bin set | strongly unstable | unstable | near-neutral | stable | strongly stable |
|---|---:|---:|---:|---:|---:|
| `±0.5` counts | 95 | 73 | 121 | 153 | 160 |
| `±1.0` counts | 51 | 117 | 121 | 228 | 85 |

`±0.5` medians `r_uw`: `0.182 / 0.324 / 0.312 / 0.225 / 0.156`.
`±0.5` medians `|r_wT|`: `0.209 / 0.150 / 0.095 / 0.200 / 0.203`.
`±0.5` ratios: `0.8680 / 2.1683 / 3.2768 / 1.1275 / 0.7675`; swing `4.2694`
(printed `4.3x`).

`±1.0` ratios: `0.6613 / 1.7607 / 3.2768 / 1.1086 / 0.5820`; swing `5.6306` (`5.6x`).

Correction (2026-10-23): the earlier note said `5.7373`; recomputing from the
`pm10` ratios gives `3.276794 / 0.581958 = 5.630641`. The counts and ratios were
unchanged; only the derived swing label was wrong.
The `±1.0` run does **not** reproduce the paper table.

Conclusion: the paper table is a `±0.5` table, not a `±1.0` table. The original
paper row labels and the v1.0.1 Option A code change were wrong. The code is
back at `±0.5`; the row labels and footnote now say `±0.5`.

## Table bracket correction

The paper caption said 5--95% ranges, but the printed brackets were neither
the actual 5--95% data ranges nor the interquartile ranges. Actual 5--95%
ranges at `±0.5`:

| class | `r_uw` 5--95% | `|r_wT|` 5--95% |
|---|---|---|
| strongly unstable | 0.045--0.480 | 0.050--0.640 |
| unstable | 0.100--0.755 | 0.018--0.561 |
| near-neutral | 0.153--0.898 | 0.007--0.358 |
| stable | 0.118--0.560 | 0.058--0.388 |
| strongly stable | 0.044--0.483 | 0.067--0.483 |

The paper table now uses these values rounded to two decimals. The caption's
"5--95% ranges" is therefore literal.

## Artifact

- `01b_neon_seasonal.json`: winter entry replaced with the `±0.5`, z-d=39.73
  rerun (counts `95/73/121/153/160`, ratios above, swing `4.2694`); summer
  entry unchanged.
- The summer entry remains the prior `2020-07` artifact at z-d=39.7. The 0.03 m
  difference moves one winter period from near-neutral to stable; it does not
  affect the seasonal fingerprint. No July rerun was performed, per the user's
  one-month data limit.

## Files

- `download_manifest.json`: source file, size, MD5
- `winter_fc15.json`: table rows, actual percentiles, artifact winter entry
- `fc15_bins.json`: `±0.5`/`±1.0` comparison, exact-boundary checks, bootstrap
- `01b_neon_seasonal.json`: full updated seasonal artifact
- `k1-fc15-winter-v6.log`, `k1-fc15-bins-v4.log`: run logs
