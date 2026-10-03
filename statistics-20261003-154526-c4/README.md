*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Exclusive quartiles overflow despite finite, representable results

Target: `statistics.quantiles`

Property: For every finite float a in [6e307, 1e308], quantiles([-a, a], n=4, method='exclusive') must return three finite cut points approximately equal to [-1.5*a, 0.0, 1.5*a], with relative tolerance 1e-14 for the nonzero values and absolute tolerance 0.0 for the middle value.

### Draft issue: statistics.quantiles produces infinite cut points from finite inputs with representable results

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** The statistics.quantiles documentation states: "The cut points are linearly interpolated from the two nearest data points." For method='exclusive', it states: "The portion of the population falling below the i-th of m sorted data points is computed as i / (m + 1)." With two observations, these rules place them at probabilities 1/3 and 2/3 and determine the stated quartiles.

**Expected:** For a=6e307, approximately [-9e307, 0.0, 9e307], all finite.

**Actual:** [-inf, 0.0, inf]

**Reproducer:**

```python
import statistics
import math

a = 6e307
data = [-a, a]
if len(data) < 2 or not all(math.isfinite(x) for x in data):
    print("REFUTATION REJECTED: invalid input")
else:
    actual = statistics.quantiles(data, n=4, method="exclusive")
    # Interpolate/extrapolate between (-a, 1/3) and (a, 2/3).
    expected = [a * (3 * i / 2 - 3) for i in range(1, 4)]
    if len(actual) != 3 or any(
        not math.isfinite(x) or not math.isclose(x, y, rel_tol=1e-14, abs_tol=0.0)
        for x, y in zip(actual, expected)
    ):
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual matches documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: [-6e+307, 6e+307] actual: [-inf, 0.0, inf] expected: [-8.999999999999999e+307, 0.0, 8.999999999999999e+307]
```

Judge: BUG (medium) -- The input is valid, and the expected quartiles follow from the documented exclusive probability positions and linear interpolation/extrapolation. All expected results are representable finite floats throughout the stated range. The reported infinities therefore reflect avoidable intermediate overflow, not ordinary rounding or overflow of the mathematical result. The supplied upstream diff does not change quantiles, and the Decimal issue does not report this behaviour.

