*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `cmath`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `cmath`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Overflowing complex magnitudes can make distant finite values compare close

Target: `cmath.isclose`

Property: For finite complex a and b, with rel_tol=1e-9 and abs_tol=0.0, isclose(a, b) must agree with |a-b| <= rel_tol * max(|a|, |b|), evaluated mathematically without intermediate overflow. In particular, it must return False when b=-a and a is nonzero.

### Draft issue: cmath.isclose incorrectly returns True for large finite opposite complex values

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `cmath`

**Documented behaviour:** Python standard-library documentation, cmath.isclose: "If no errors occur, the result will be: abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)."

**Expected:** False

**Actual:** True

**Reproducer:**

```python
import cmath
import math
from fractions import Fraction as F

p = dict(a=complex(1.7e308, 1.7e308), b=complex(-1.7e308, -1.7e308),
         rel_tol=1e-9, abs_tol=0.0)
a, b = p["a"], p["b"]
if not (all(map(math.isfinite, (a.real, a.imag, b.real, b.imag,
                                p["rel_tol"], p["abs_tol"])))
        and p["rel_tol"] >= 0 and p["abs_tol"] >= 0):
    print("REFUTATION REJECTED:", "invalid input", p)
else:
    x, y, u, v = map(F, (a.real, a.imag, b.real, b.imag))
    expected = (x-u)**2 + (y-v)**2 <= max(
        F(p["rel_tol"])**2 * max(x*x+y*y, u*u+v*v),
        F(p["abs_tol"])**2)
    actual = cmath.isclose(**p)
    if actual != expected:
        print("REFUTATION CONFIRMED:", p, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "actual agrees with exact expectation",
              p, "actual:", actual, "expected:", expected)
```

**Output:**

```
REFUTATION CONFIRMED: {'a': (1.7e+308+1.7e+308j), 'b': (-1.7e+308-1.7e+308j), 'rel_tol': 1e-09, 'abs_tol': 0.0} actual: True expected: False
```

Judge: BUG (medium) -- All input components and tolerances are finite and valid. The Fraction calculation correctly tests the documented inequality by squaring its nonnegative sides without overflow. For b=-a, the distance is twice the magnitude of a, so rel_tol=1e-9 cannot make them close. Intermediate magnitude overflow instead produces a spurious True result. The listed math.isclose documentation PR does not report or fix this cmath.isclose behaviour.

