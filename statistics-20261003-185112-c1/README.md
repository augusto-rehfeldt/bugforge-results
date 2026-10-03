*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Weighted fmean loses a representable mean through product underflow

Target: `statistics.fmean`

Property: For x = 2.0**(-k) and w = 2.0**(-j), where integers k and j are in [600, 900], fmean([x], weights=[w]) must equal x: the weighted arithmetic mean of a singleton with positive weight is its sole value.

### Draft issue: statistics.fmean returns zero for a singleton with a tiny positive weight

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** "Convert data to floats and compute the arithmetic mean." — statistics.fmean docstring. With weights supplied, the documented operation is the weighted arithmetic mean.

**Expected:** 2.409919865102884e-181

**Actual:** 0.0

**Reproducer:**

```python
import math, statistics
from fractions import Fraction

k = j = 600
x, w = 2.0**-k, 2.0**-j
data, weights = [x], [w]
if not (600 <= k <= 900 and 600 <= j <= 900
        and math.isfinite(x) and math.isfinite(w) and x > 0 and w > 0):
    print("REFUTATION REJECTED: invalid input")
else:
    actual = statistics.fmean(data, weights=weights)
    expected = float(Fraction(x) * Fraction(w) / Fraction(w))
    if actual != expected:
        print("REFUTATION CONFIRMED:", dict(data=data, weights=weights),
              "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual equals documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: {'data': [2.409919865102884e-181], 'weights': [2.409919865102884e-181]} actual: 0.0 expected: 2.409919865102884e-181
```

Judge: BUG (medium) -- The inputs are valid, finite, positive floats, and the exact singleton weighted mean is x, itself exactly representable. The Fraction calculation correctly verifies this. The result loses the entire value because the weighted numerator underflows: x*w = 2**-1200 rounds to zero before division by w. This is avoidable intermediate underflow, not unavoidable rounding of the final mean. None of the listed issues addresses this behaviour, and the supplied upstream diff shows no fix to the weighted path.

