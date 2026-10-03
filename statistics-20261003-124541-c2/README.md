*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Inverse normal CDF overflows before a finite location shift

Target: `statistics.NormalDist.inv_cdf`

Property: For finite a in [9.5e307, 1e308], NormalDist(-a, a).inv_cdf(0.975) must be finite and agree with a * (NormalDist().inv_cdf(0.975) - 1.0) to relative tolerance 1e-14.

### Draft issue: NormalDist.inv_cdf returns infinity from intermediate overflow for a finite quantile

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** The supplied public API documents inv_cdf as "Inverse cumulative distribution function. x : P(X <= x) = p". For a normal distribution, the specified quantile is mu + sigma times the standard-normal quantile.

**Expected:** A finite quantile approximately 9.119657853130516e307, agreeing with a * (NormalDist().inv_cdf(0.975) - 1) within relative tolerance 1e-14.

**Actual:** inf

**Reproducer:**

```python
import math
import statistics

a = 9.5e307
data = dict(a=a, mu=-a, sigma=a, p=0.975)
if not (9.5e307 <= a <= 1e308 and
        all(math.isfinite(v) for v in data.values()) and
        data["sigma"] > 0 and 0 < data["p"] < 1):
    print("REFUTATION REJECTED:", "invalid input", data)
else:
    lo, hi = 0.0, 10.0
    for _ in range(80):
        z = (lo + hi) / 2
        if math.erfc(-z / math.sqrt(2)) / 2 < data["p"]:
            lo = z
        else:
            hi = z
    expected = a * ((lo + hi) / 2 - 1)
    try:
        actual = statistics.NormalDist(data["mu"], data["sigma"]).inv_cdf(data["p"])
        broken = not math.isfinite(actual) or not math.isclose(
            actual, expected, rel_tol=1e-14, abs_tol=0)
    except Exception as exc:
        actual, broken = repr(exc), True
    if broken:
        print("REFUTATION CONFIRMED:", data, "actual =", actual, "expected =", expected)
    else:
        print("REFUTATION REJECTED:", "finite result agrees within tolerance",
              data, "actual =", actual, "expected =", expected)
```

**Output:**

```
REFUTATION CONFIRMED: {'a': 9.5e+307, 'mu': -9.5e+307, 'sigma': 9.5e+307, 'p': 0.975} actual = inf expected = 9.119657853130516e+307
```

Judge: BUG (medium) -- The inputs are valid and finite, with positive sigma and p strictly between zero and one. The reproducer independently computes the standard-normal quantile using erfc and bisection; its expected result is finite and consistent with the documented inverse CDF. Multiplying sigma by the standard quantile overflows before adding the negative mean, although the final mathematical result is representable. This is avoidable intermediate overflow, not ordinary rounding error. No listed issue duplicates it, and the supplied upstream diff does not fix inv_cdf.

