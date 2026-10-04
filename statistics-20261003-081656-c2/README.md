*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Supplying the exact mean makes population standard deviation overflow

Target: `statistics.pstdev`

Property: For every finite float a in [1e160, 1e300], pstdev([-a, a], mu=0.0) must return approximately a (relative tolerance 1e-15), without raising, and agree with pstdev([-a, a]). The supplied mean is exactly correct and the standard deviation is representable.

### Draft issue: statistics.pstdev overflows for large finite values when given the correct mean

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** The pvariance docstring, incorporated by pstdev's sentence "See ``pvariance`` for arguments and other details", states: "The optional argument mu, if given, should be the mean of the data. If it is missing or None, the mean is automatically calculated." pstdev promises: "Return the square root of the population variance."

**Expected:** pstdev([-1e160, 1e160], mu=0.0) returns approximately 1e160, agreeing with the call without mu.

**Actual:** Raises ValueError: inf or nan encountered in data.

**Reproducer:**

```python
import math
import statistics

a = 1e160
data, mu = [-a, a], 0.0
expected = math.hypot(*data) / math.sqrt(len(data))
if not (all(map(math.isfinite, data)) and math.fsum(data) / len(data) == mu):
    print("REFUTATION REJECTED: invalid input or incorrect mean")
else:
    try:
        actual = statistics.pstdev(data, mu=mu)
    except Exception as e:
        actual = f"{type(e).__name__}: {e}"
    if not isinstance(actual, float) or not math.isclose(actual, expected, rel_tol=1e-15):
        print("REFUTATION CONFIRMED:", {"data": data, "mu": mu},
              "actual=", actual, "expected=", expected)
    else:
        print("REFUTATION REJECTED: result agrees with documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: {'data': [-1e+160, 1e+160], 'mu': 0.0} actual= ValueError: inf or nan encountered in data expected= 1e+160
```

Judge: BUG (medium) -- The inputs are finite and mu=0.0 is their exact mean. Their population standard deviation is a, which is representable; the reproducer's scaled hypot calculation correctly gives 1e160. Supplying the correct optional mean should not cause a failure absent when it is calculated automatically. This is intermediate squared-deviation overflow, not ordinary rounding error or invalid data. The supplied upstream diff does not fix this path, and the listed issue titles do not establish a duplicate.

