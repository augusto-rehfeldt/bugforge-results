*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Sigmoid KDE density raises OverflowError in finite tails

Target: `statistics.kde`

Property: For every finite float x in [720.0, 1000.0], kde([0.0], 1.0, kernel='sigmoid')(x) must return a finite nonnegative density without raising. Its mathematical value is 2*exp(-abs(x))/(pi*(1+exp(-2*abs(x)))), allowing floating-point underflow to zero.

### Draft issue: statistics.kde sigmoid PDF raises OverflowError for finite tail inputs

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** The statistics.kde docstring says: "Kernel Density Estimation: Create a continuous probability density function or cumulative distribution function from discrete samples." It lists "sigmoid" under "Kernels that give some weight to every sample point".

**Expected:** A finite nonnegative density, approximately 1.29375831084e-313 at x=720; underflow to zero is acceptable for sufficiently distant points.

**Actual:** OverflowError: math range error at x=720.0.

**Reproducer:**

```python
import math
import statistics as s

p = dict(data=[0.0], h=1.0, kernel="sigmoid", cumulative=False)
x = 720.0
inp = dict(p, x=x)
try:
    if not hasattr(s, "kde"):
        raise ValueError("statistics.kde unavailable")
    if "sigmoid" not in (s.kde.__doc__ or ""):
        raise ValueError("sigmoid not documented")
    if not (p["data"] and all(map(math.isfinite, p["data"]))
            and math.isfinite(p["h"]) and p["h"] > 0
            and math.isfinite(x) and 720 <= x <= 1000):
        raise ValueError("invalid input")
    expected = 2 * math.exp(-abs(x)) / (math.pi * (1 + math.exp(-2 * abs(x))))
    try:
        actual = s.kde(**p)(x)
        broken = not (math.isfinite(actual) and actual >= 0
                      and math.isclose(actual, expected, rel_tol=1e-12, abs_tol=0))
    except Exception as e:
        actual = (type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", inp, "actual =", actual, "expected =", expected)
    else:
        print("REFUTATION REJECTED:", "valid input returns the expected density")
except Exception as e:
    print("REFUTATION REJECTED:", str(e))
```

**Output:**

```
REFUTATION CONFIRMED: {'data': [0.0], 'h': 1.0, 'kernel': 'sigmoid', 'cumulative': False, 'x': 720.0} actual = ('OverflowError', 'math range error') expected = 1.29375831084e-313
```

Judge: BUG (medium) -- The reproducer uses valid finite data, positive bandwidth, and a documented unbounded-support kernel. At x=720 the sigmoid density is representable as a positive subnormal float, but computing its reciprocal via cosh(720) overflows. This is avoidable intermediate overflow, not rounding or legitimate density overflow. The upstream implementation retains the same vulnerable formula. The listed feature issue does not report or fix this behaviour.

