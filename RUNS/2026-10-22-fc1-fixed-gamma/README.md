# F-C1 fixed-gamma sweep

- Run: Kaggle kernel `abduk5/k1-f-c1-fixed-gamma`, version 2, `COMPLETE`.
- URL: https://www.kaggle.com/code/abduk5/k1-f-c1-fixed-gamma
- Source revision: `/home/manem/Downloads/K1-two-clocks-theory` at `e178c55`; solver SHA-256 in `SOURCE_REV.txt`.
- Environment: Python 3.13.15, NumPy 2.1.3, Linux x86_64, CPU.
- Grid: `128x128` periodic; `L=1`; `c=[4,8,16,32]`; run length `20 L/c`.
- `t90` is the first time `||p-p_ell||/||p_ell|| < 0.10`; errors recorded every step.

| convention | c | gamma | t90 | t90*c/L | final error |
|---|---:|---:|---:|---:|---:|
| proportional | 4 | 6 | 0.569552 | 2.2782 | 2.3749e-03 |
| proportional | 8 | 12 | 0.284776 | 2.2782 | 2.3749e-03 |
| proportional | 16 | 24 | 0.142388 | 2.2782 | 2.3749e-03 |
| proportional | 32 | 48 | 0.071194 | 2.2782 | 2.3749e-03 |
| fixed_12 | 4 | 12 | 0.303283 | 1.2131 | 2.3750e-03 |
| fixed_12 | 8 | 12 | 0.284776 | 1.1391 | 2.3749e-03 |
| fixed_12 | 16 | 12 | 0.271932 | 1.0877 | 2.2882e-03 |
| fixed_12 | 32 | 12 | 0.269861 | 1.0794 | 1.7430e-02 |
| fixed_48 | 4 | 48 | 0.128163 | 0.5127 | 2.3750e-03 |
| fixed_48 | 8 | 48 | 0.093360 | 0.3734 | 2.3750e-03 |
| fixed_48 | 16 | 48 | 0.075821 | 0.3033 | 2.3750e-03 |
| fixed_48 | 32 | 48 | 0.071194 | 0.2848 | 2.3749e-03 |

## Fit and collapse

- Proportional: through-origin slope `2.27820966`, R² `1.0`, collapse spread `0.0`.
- Fixed gamma 12: through-origin slope invalid (R² `-132.0`); ordinary least-squares slope `0.1582` with intercept `0.2639` (R² `0.9919`). `t90` is nearly constant in physical time (`0.270-0.303`), not proportional to `L/c`.
- Fixed gamma 48: through-origin R² `-1.51`; OLS slope `0.2666`, intercept `0.0609` (R² `0.9960`). `t90` ranges `0.071-0.128`.
- Relative collapse spread: proportional `0.0`; fixed 12 `1.1866`; fixed 48 `0.7089`.

## Interpretation

The clean `t90 = 2.278 L/c` law is recovered only when damping is imposed **per acoustic crossing** (`gamma=1.5c/L`). Holding `gamma` fixed makes `t90` nearly independent of `c` at gamma=12 and only weakly dependent at gamma=48; the damping time, not the wave-crossing time, controls the 10% threshold. Thus the paper's slope is a property of the damping convention, not a convention-independent adjustment-time law. This confirms F-C1 dynamically and strengthens it from a disclosure issue to a construction/confound issue.

The fixed values are the paper's damping rates at `c=8` and `c=32`; they are deliberately within the paper's own range, not extreme choices.
