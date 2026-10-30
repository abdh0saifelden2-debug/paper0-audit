# Paper0 Audit Workspace

This directory is outside the audited repository. It contains the resumable ledger, claim map, inventory, run logs, and report.

Start here:

1. `AUDIT_STATE.md` — current phase and next test.
2. `AUDIT_LEDGER.tsv` — per-test and per-finding evidence.
3. `CLAIM_MAP.md` — paper claim to code/test/artifact mapping.
4. `INVENTORY.md` — commands, test scope, data map.
5. `notes/static-findings.md` — static findings F-C1–F-C20.
6. `REPORT.md` — audit report; static complete, F-C20/F-C1/F-C2/F-C15 dynamic probes complete, and v1.0.3 released CI-green.
7. `RUNS/2026-10-21-k0-probe/` — F-C20 k=0 probe evidence and reproduction notes.
8. `RUNS/2026-10-22-fc1-fixed-gamma/` — F-C1 proportional/fixed-gamma sweep.
9. `RUNS/2026-10-22-fc2-unitary/` — F-C2 cross-spectrum-preserving surrogate control.
10. `notes/v1.0.1_proposed_changes.md` — final v1.0.1 release changes and F-C15 resolution.
11. `RUNS/2026-10-23-fc15-neon/` — raw WREF 2020-01 F-C15 rerun and `±0.5`/`±1.0` comparison.
12. `notes/v1.0.2_review_fixes.md` — v1.0.2 submission-review fixes and the `5.74x` swing disposition.
13. `RUNS/2026-10-30-v1.0.2-release/` — released v1.0.2 PDF and hash ledger.
14. `notes/v1.0.3_layout_fixes.md` — v1.0.3 read-aloud fixes: clipped table row, split footnote, duplicate coherence text.
15. `RUNS/2026-10-30-v1.0.3-release/` — released v1.0.3 PDF and hash ledger.
16. `release-gate/` — snapshots of the v1.0.3 claim map, claim data, F-C2 artifact, and lint, plus how to run the lint against the tagged target.

Release status: `paper0-v1.0.3` at commit `a0b6a45`, CI-green; release at https://github.com/abdh0saifelden2-debug/K1-two-clocks-theory/releases/tag/paper0-v1.0.3.

Audit repository: https://github.com/abdh0saifelden2-debug/paper0-audit

Rules:

- Target edits are allowed only for the authorized v1.0.3 release surface.
- Do not mark a data-dependent test `PASS` from committed JSON alone.
- Update ledger and state after every test.
- Dynamic runs go to Kaggle/CI, not this laptop.
- Never execute project code/tests locally.
