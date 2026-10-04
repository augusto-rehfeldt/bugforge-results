*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Self-correlation fails for tiny nonconstant inputs

Target: `statistics.correlation`

Property: For x = [-a, a], where a is a positive finite float in [1e-200, 1e-170], correlation(x, x) must return approximately 1.0, without raising an exception: x is nonconstant and its Pearson self-correlation is exactly 1.

### Draft issue: statistics.correlation misclassifies tiny nonconstant inputs as constant

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** The correlation() docstring states: "Return the Pearson's correlation coefficient for two inputs." It also demonstrates "correlation(x, x)" returning "1.0".

**Expected:** Return approximately 1.0 without raising an exception.

**Actual:** Raises StatisticsError: at least one of the inputs is constant.

**Reproducer:**

```python
import math
import statistics
from fractions import Fraction

a = 1e-200
x = [-a, a]
if not (1e-200 <= a <= 1e-170 and all(map(math.isfinite, x))
        and len(x) >= 2 and len(set(x)) > 1):
    print("REFUTATION REJECTED: invalid input")
else:
    q = list(map(Fraction, x))
    mean = sum(q) / len(q)
    variance = sum((t - mean) ** 2 for t in q)
    expected = float(variance / variance)  # Exact Pearson self-correlation.
    try:
        result = statistics.correlation(x, x)
        actual = ("result", result)
        broken = not math.isclose(result, expected, rel_tol=1e-12)
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", (x, x), "actual =", actual,
              "expected =", expected)
    else:
        print("REFUTATION REJECTED: actual matches exact Pearson self-correlation")
```

**Output:**

```
REFUTATION CONFIRMED: ([-1e-200, 1e-200], [-1e-200, 1e-200]) actual = ('exception', 'StatisticsError', 'at least one of the inputs is constant') expected = 1.0
```

Judge: BUG (medium) -- The inputs are finite, nonconstant, and have sufficient length. Fraction computes the exact variance of the supplied floats, which is positive, so the expected self-correlation of 1.0 is correct. Underflow in intermediate squared deviations incorrectly classifies these inputs as constant; this is not merely a small rounding error. The listed PR introduces correlation but does not report or fix this behaviour, and the supplied upstream diff shows no relevant fix.

