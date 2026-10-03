*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Normal distribution overlap should be invariant under common positive scaling

Target: `statistics.NormalDist.overlap`

Property: For finite a in [1e100, 1e150], NormalDist(0.0, a).overlap(NormalDist(0.0, 2*a)) must agree with NormalDist(0.0, 1.0).overlap(NormalDist(0.0, 2.0)) within absolute tolerance 1e-12, without raising. Scaling both distributions by the same positive factor preserves the integral of the minimum of their densities.

### Draft issue: statistics.NormalDist.overlap returns incorrect coefficient for large finite standard deviations

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** NormalDist.overlap documentation: "Compute the overlapping coefficient (OVL) between two normal distributions." The overlapping coefficient is the integral of the minimum of the two probability density functions.

**Expected:** Approximately 0.6773254311652314, within absolute tolerance 1e-12, without raising.

**Actual:** 1.0 for NormalDist(0.0, 1e150).overlap(NormalDist(0.0, 2e150)).

**Reproducer:**

```python
import math
from statistics import NormalDist

p = ((0.0, 1e150), (0.0, 2e150))
if not all(math.isfinite(m) and math.isfinite(s) and s > 0 for m, s in p):
    print("REFUTATION REJECTED:", "invalid normal-distribution parameters")
else:
    # Integrate the narrower density outside the crossings, wider inside.
    t = math.sqrt(4 * math.log(2) / 3)
    expected = 1 + math.erf(t / 2) - math.erf(t)
    try:
        actual = NormalDist(*p[0]).overlap(NormalDist(*p[1]))
    except Exception as e:
        print("REFUTATION CONFIRMED:", p, "actual =", repr(e), "expected =", expected)
    else:
        if not math.isfinite(actual) or abs(actual - expected) > 1e-12:
            print("REFUTATION CONFIRMED:", p, "actual =", actual, "expected =", expected)
        else:
            print("REFUTATION REJECTED:", "actual agrees with the independent integral")
```

**Output:**

```
REFUTATION CONFIRMED: ((0.0, 1e+150), (0.0, 2e+150)) actual = 1.0 expected = 0.6773254311652314
```

Judge: BUG (medium) -- The inputs are finite with positive standard deviations. The independent integral is correct: common positive scaling preserves overlap, which is approximately 0.6773254311652314 for a standard-deviation ratio of two. Returning 1.0 is a substantial error, not ordinary floating-point rounding; intermediate overflow in the overlap calculation loses the finite density crossings. The supplied upstream diff does not change overlap, and no duplicate is listed.

