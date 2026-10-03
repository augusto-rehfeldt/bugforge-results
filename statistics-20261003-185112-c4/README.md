*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Covariance overflows although the sample covariance is representable

Target: `statistics.covariance`

Property: For every finite float a in [7e153, 1e154], let x = [-a, -a, a, a]. covariance(x, x) must return a finite value agreeing with (a * a) * (4.0 / 3.0) within relative tolerance 1e-14, without raising an exception.

### Draft issue: statistics.covariance overflows when the final covariance is representable

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** "Return the sample covariance of two inputs *x* and *y*." — statistics.covariance docstring.

**Expected:** A finite sample covariance approximately equal to 6.533333333333333e+307 for the reproduced input.

**Actual:** statistics.covariance(x, x) returns inf.

**Reproducer:**

```python
import statistics, math
from fractions import Fraction

x = [-7e153, -7e153, 7e153, 7e153]
y = x.copy()
if len(x) != len(y) or len(x) < 2 or not all(map(math.isfinite, x + y)):
    print("REFUTATION REJECTED: invalid input")
else:
    n = len(x)
    u, v = list(map(Fraction, x)), list(map(Fraction, y))
    expected = float((sum(a*b for a, b in zip(u, v)) - sum(u)*sum(v)/n)/(n-1))
    try:
        actual = statistics.covariance(x, y)
        broken = not math.isfinite(actual) or not math.isclose(actual, expected, rel_tol=1e-14)
    except Exception as e:
        actual, broken = repr(e), True
    if broken:
        print("REFUTATION CONFIRMED:", (x, y), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: sample covariance agrees with exact reference")
```

**Output:**

```
REFUTATION CONFIRMED: ([-7e+153, -7e+153, 7e+153, 7e+153], [-7e+153, -7e+153, 7e+153, 7e+153]) actual: inf expected: 6.533333333333333e+307
```

Judge: BUG (medium) -- The reproducer supplies valid finite inputs and computes the sample covariance correctly using exact Fraction arithmetic. Each product and the final covariance are representable as floats, but the unnormalized sum of products exceeds the float range. Returning infinity reflects avoidable intermediate overflow, not ordinary rounding error. The supplied upstream diff contains no covariance fix, and no duplicates were found.

