*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Weighted harmonic mean rejects valid positive inputs when weighted reciprocals underflow

Target: `statistics.harmonic_mean`

Property: For a = 10.0**k with integer 180 <= k <= 250, harmonic_mean([a, 2*a], weights=[1/a, 1/a]) must return a finite value approximately equal to (4/3)*a, within relative tolerance 1e-14, without raising. Equal positive weights give the ordinary harmonic mean.

### Draft issue: statistics.harmonic_mean raises for positive finite inputs when weighted reciprocals underflow

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** The harmonic_mean docstring states: "The harmonic mean is the reciprocal of the arithmetic mean of the reciprocals of the data." It also documents weighted averaging with the example harmonic_mean([40, 60], weights=[5, 30]).

**Expected:** A finite result approximately equal to 1.3333333333333334e+180.

**Actual:** StatisticsError: Weighted sum must be positive

**Reproducer:**

```python
import math
import statistics
from fractions import Fraction as F

a = 10.0**180
data, weights = [a, 2*a], [1/a, 1/a]
if not all(math.isfinite(x) and x > 0 for x in data + weights):
    print("REFUTATION REJECTED: input is not finite and positive")
else:
    expected = float(sum(map(F, weights)) /
                     sum(F(w) / F(x) for x, w in zip(data, weights)))
    try:
        actual = statistics.harmonic_mean(data, weights=weights)
        broken = not math.isfinite(actual) or not math.isclose(
            actual, expected, rel_tol=1e-14, abs_tol=0)
    except Exception as e:
        actual, broken = (type(e).__name__, str(e)), True
    if broken:
        print("REFUTATION CONFIRMED:", {"data": data, "weights": weights},
              "actual =", actual, "expected =", expected)
    else:
        print("REFUTATION REJECTED: result matches the documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: {'data': [1e+180, 2e+180], 'weights': [1e-180, 1e-180]} actual = ('StatisticsError', 'Weighted sum must be positive') expected = 1.3333333333333334e+180
```

Judge: BUG (medium) -- All inputs are finite and strictly positive, and the exact Fraction calculation correctly computes the weighted harmonic mean. Equal positive weights must cancel. Intermediate w/x values underflow to zero, causing a spurious StatisticsError even though the result is representable. This is not merely a rounded result. No listed issue or upstream change addresses this behavior.

