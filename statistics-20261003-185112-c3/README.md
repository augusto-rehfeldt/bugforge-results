*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Correlation loses nonconstant integer inputs when centering

Target: `statistics.correlation`

Property: For integers k in [54, 100], let x = [2**k, 2**k + 1]. correlation(x, x) must return approximately 1.0 (absolute tolerance 1e-14), without raising: the input is nonconstant and its Pearson self-correlation is exactly one.

### Draft issue: statistics.correlation misclassifies distinct large integers as constant input

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** The correlation docstring says "Return the Pearson's correlation coefficient for two inputs" and demonstrates "correlation(x, x)" returning "1.0".

**Expected:** Return approximately 1.0 without raising for these nonconstant integer inputs.

**Actual:** StatisticsError: at least one of the inputs is constant

**Reproducer:**

```python
import statistics
from fractions import Fraction
from math import isclose, sqrt

x = [2**54, 2**54 + 1]
if len(x) < 2 or len(set(x)) < 2:
    print("REFUTATION REJECTED: input is too short or constant")
else:
    mean = Fraction(sum(x), len(x))
    deviations = [v - mean for v in x]
    covariance = sum(d * d for d in deviations)
    expected = float(covariance) / sqrt(float(covariance * covariance))
    try:
        actual = statistics.correlation(x, x)
        broken = not isclose(actual, expected, rel_tol=0, abs_tol=1e-14)
    except Exception as e:
        actual = f"{type(e).__name__}: {e}"
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", x, "actual=", actual, "expected=", expected)
    else:
        print("REFUTATION REJECTED: result matches independent Pearson calculation")
```

**Output:**

```
REFUTATION CONFIRMED: [18014398509481984, 18014398509481985] actual= StatisticsError: at least one of the inputs is constant expected= 1.0
```

Judge: BUG (medium) -- The reproducer uses two distinct, exactly represented Python integers. Its independent Fraction calculation correctly gives Pearson self-correlation 1.0. Raising the constant-input error therefore misclassifies valid nonconstant data, rather than merely introducing rounding error in the result. No listed issue duplicates this behaviour, and the supplied upstream diff contains no correlation fix.

