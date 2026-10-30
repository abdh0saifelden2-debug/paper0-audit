# Dynamic Run Logs

Store one subdirectory per run:

```
RUNS/YYYY-MM-DD-<runner>-<scope>/
  command.txt
  environment.txt
  data.sha256
  pytest.xml
  stdout.log
  stderr.log
  notes.md
```

Required fields:

- audited commit
- runner and hardware
- Python/NumPy/SciPy versions
- data source, version, hash
- seeds
- exact command
- pass/fail/skip counts
- runtime
- comparison to paper/artifact

Completed runs:

- `2026-10-21-k0-probe/` — F-C20 k=0 channel wall probe; Kaggle CPU; cleared for tested scope. See its `README.md` for provenance, results, and caveats.
- `2026-10-22-fc1-fixed-gamma/` — F-C1 proportional vs fixed-gamma sweep; Kaggle CPU. See its `README.md` for the slope/collapse table.
- `2026-10-22-fc2-unitary/` — F-C2 independent-phase vs common-phase/unitary controls; Kaggle CPU. See its `README.md`.
- `2026-10-23-fc15-neon/` — F-C15 raw WREF 2020-01 rerun, `±0.5` vs true `±1.0`, and actual 5–95% ranges; Kaggle CPU. See its `README.md`.
- `2026-10-30-v1.0.2-release/` — released v1.0.2 PDF, hash/size ledger, and `pdftotext` checks. See its `README.md`.
