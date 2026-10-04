*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Normal CDF should be invariant under positive rescaling

Target: `statistics.NormalDist.cdf`

Property: For every finite float a with 0 < a <= 1.2e308, NormalDist(-a, a).cdf(a) must agree with NormalDist(0.0, 1.0).cdf(2.0) within absolute tolerance 1e-15: the evaluation point is exactly two standard deviations above the mean.

### Draft issue: statistics.NormalDist.cdf returns incorrect probability when x - mu overflows

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** Public API documentation for NormalDist.cdf: "Cumulative distribution function. P(X <= x)"; NormalDist describes mu and sigma as the mean and standard deviation.

**Expected:** 0.9772498680518209, within absolute tolerance 1e-15

**Actual:** 1.0

**Reproducer:**

```python
import math
import statistics

a = 1e308
mu, sigma, x = -a, a, a
if not (all(map(math.isfinite, (mu, sigma, x))) and 0 < a <= 1.2e308):
    print("REFUTATION REJECTED: invalid input")
else:
    actual = statistics.NormalDist(mu, sigma).cdf(x)
    z = x / sigma - mu / sigma  # Avoid overflow in x - mu.
    expected = (1 + math.erf(z / math.sqrt(2))) / 2
    if not abs(actual - expected) <= 1e-15:
        print("REFUTATION CONFIRMED:", (mu, sigma, x), actual, expected)
    else:
        print("REFUTATION REJECTED: agrees within absolute tolerance 1e-15")
```

**Output:**

```
REFUTATION CONFIRMED: (-1e+308, 1e+308, 1e+308) 1.0 0.9772498680518209
```

Judge: BUG (medium) -- The reproducer uses finite inputs and a positive standard deviation. Its overflow-safe reference correctly gives z = 2. The returned 1.0 differs by about 0.02275, not ordinary floating-point rounding: subtraction overflows even though the standardized argument is representable. This violates the documented CDF meaning. Neither listed issue addresses this behavior, and the supplied upstream diff leaves cdf unchanged.

