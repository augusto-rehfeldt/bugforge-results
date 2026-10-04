*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `more_itertools`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `more_itertools` 11.1.0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Running mean can overflow when the true mean is finite

Target: `more_itertools.running_mean`

Property: For a two-item list of finite floats [a, b], the second value yielded by running_mean must be finite and agree, within floating-point rounding tolerance, with float((Fraction(a) + Fraction(b)) / 2). The exact average of two finite floats is always within the finite float range.

### Draft issue: running_mean overflows for two identical large finite floats

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `more_itertools` 11.1.0

**Documented behaviour:** The running_mean documentation in more_itertools.more promises: "Yield the running arithmetic mean of the items in iterable."

**Expected:** The second yielded value is finite and approximately 1e308.

**Actual:** The second yielded value is inf.

**Reproducer:**

```python
import math
from fractions import Fraction
from more_itertools.recipes import running_mean

x = [1e308, 1e308]
if len(x) != 2 or not all(isinstance(v, float) and math.isfinite(v) for v in x):
    print("REFUTATION REJECTED: input is not two finite floats")
else:
    expected = float(sum(map(Fraction, x)) / 2)
    try:
        actual = list(running_mean(x))[1]
    except Exception as e:
        print("REFUTATION REJECTED: could not check second value:", repr(e))
    else:
        if not math.isfinite(actual) or not math.isclose(actual, expected, rel_tol=1e-15):
            print("REFUTATION CONFIRMED:", x, "actual:", actual, "expected:", expected)
        else:
            print("REFUTATION REJECTED: second value agrees with the exact mean")
```

**Output:**

```
REFUTATION CONFIRMED: [1e+308, 1e+308] actual: inf expected: 1e+308
```

Judge: BUG (medium) -- The reproducer uses valid finite floats and computes the reference mean exactly with Fraction before converting to float. The documented arithmetic mean of two identical 1e308 values is 1e308; returning infinity is intermediate overflow, not ordinary rounding error. No documented limitation or duplicate was provided.

