# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Logistic KDE CDF must remain defined for finite tail queries

Target: `statistics.kde`

Property: For any nonempty list of finite floats data and positive finite bandwidth h, with finite standardized differences (x - datum) / h, kde(data, h, kernel='logistic', cumulative=True)(x) must return a finite probability between 0.0 and 1.0 for every finite float x.

### Draft issue: statistics.kde logistic CDF overflows for large finite arguments

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** The statistics.kde docstring says: "Create a continuous probability density function or cumulative distribution function from discrete samples." It also lists logistic under "Kernels that give some weight to every sample point".

**Expected:** Return 1.0 without raising an exception.

**Actual:** Raises OverflowError: math range error.

**Reproducer:**

```python
import math
import statistics

case = dict(data=[0.0], h=1.0, kernel="logistic", cumulative=True, x=710.0)
data, h, x = case["data"], case["h"], case["x"]
z = [(x - d) / h for d in data]
if not (data and math.isfinite(h) and h > 0 and math.isfinite(x)
        and all(math.isfinite(d) for d in data)
        and all(math.isfinite(t) for t in z)):
    print("REFUTATION REJECTED:", "invalid input", case)
elif not hasattr(statistics, "kde"):
    print("REFUTATION REJECTED:", "statistics.kde unavailable")
else:
    # Logistic CDF, evaluated without overflowing either tail.
    expected = sum(1 / (1 + math.exp(-t)) if t >= 0
                   else math.exp(t) / (1 + math.exp(t)) for t in z) / len(data)
    try:
        actual = statistics.kde(data, h, kernel="logistic", cumulative=True)(x)
        broken = not math.isfinite(actual) or not 0 <= actual <= 1
    except Exception as e:
        actual = (type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", case, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "finite probability returned",
              case, "actual:", actual, "expected:", expected)
```

**Output:**

```
REFUTATION CONFIRMED: {'data': [0.0], 'h': 1.0, 'kernel': 'logistic', 'cumulative': True, 'x': 710.0} actual: ('OverflowError', 'math range error') expected: 1.0
```

Judge: BUG (medium) -- The reproducer uses valid finite inputs and a finite standardized difference of 710. A logistic cumulative distribution function is defined at this point and must return a probability; its correctly rounded value here is 1.0. Raising OverflowError is avoidable with a numerically stable logistic CDF evaluation, not an ordinary rounding limitation. The listed issue concerns adding KDE, not this overflow defect.

