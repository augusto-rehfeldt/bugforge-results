*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Linear regression rejects tiny nonconstant inputs with an exact identity fit

Target: `statistics.linear_regression`

Property: For every finite float a with 1e-200 <= a <= 1e-170, linear_regression([0.0, a], [0.0, a]) must return slope 1.0 and intercept 0.0, without raising: the unique ordinary least-squares fit is y = x.

### Draft issue: statistics.linear_regression misclassifies small nonconstant inputs as constant due to underflow

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** The linear_regression docstring states: "Return the slope and intercept of simple linear regression parameters estimated using ordinary least squares."

**Expected:** Slope 1.0 and intercept 0.0.

**Actual:** Raises StatisticsError: x is constant.

**Reproducer:**

```python
import math
import statistics
from fractions import Fraction

x = y = [0.0, 1e-200]
data = {"x": x, "y": y, "proportional": False}
if not (len(x) == len(y) == 2 and x[0] != x[1]
        and all(math.isfinite(v) for v in x + y)):
    print("REFUTATION REJECTED:", "invalid regression input")
else:
    X, Y = list(map(Fraction, x)), list(map(Fraction, y))
    # Two distinct points determine the unique zero-residual OLS line.
    slope = (Y[1] - Y[0]) / (X[1] - X[0])
    expected = (float(slope), float(Y[0] - slope * X[0]))
    try:
        actual = tuple(statistics.linear_regression(x, y))
    except Exception as e:
        actual = {"exception": type(e).__name__, "message": str(e)}
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "actual matches independent OLS expectation")
```

**Output:**

```
REFUTATION CONFIRMED: {'x': [0.0, 1e-200], 'y': [0.0, 1e-200], 'proportional': False} actual: {'exception': 'StatisticsError', 'message': 'x is constant'} expected: (1.0, 0.0)
```

Judge: BUG (medium) -- The inputs are finite, distinct floats and define a unique OLS line. Fraction conversion preserves the actual float values exactly, so the expected result is sound. Underflow of the squared deviations makes the regression denominator zero, incorrectly classifying nonconstant x as constant. This is a spurious rejection of valid input, not merely an inexact fitted coefficient. No listed issue or upstream change handles this behaviour.

