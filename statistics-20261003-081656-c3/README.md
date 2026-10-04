*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Harmonic mean of identical tiny positive floats becomes zero

Target: `statistics.harmonic_mean`

Property: For every finite positive float x and integer n >= 2, harmonic_mean([x] * n) must equal x, as required by the mathematical definition of the harmonic mean.

### Draft issue: statistics.harmonic_mean returns zero for identical positive subnormal floats

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** The harmonic_mean docstring states: "The harmonic mean is the reciprocal of the arithmetic mean of the reciprocals of the data." For identical positive observations, this is the observation itself.

**Expected:** 1e-320

**Actual:** 0.0

**Reproducer:**

```python
import math
import statistics
from fractions import Fraction

data = [1e-320, 1e-320]
if len(data) < 2 or not all(math.isfinite(x) and x > 0 for x in data):
    print("REFUTATION REJECTED: invalid input")
else:
    expected = float(len(data) / sum(1 / Fraction(x) for x in data))
    actual = statistics.harmonic_mean(data)
    if actual != expected:
        print(f"REFUTATION CONFIRMED: input={data!r}, actual={actual!r}, expected={expected!r}")
    else:
        print("REFUTATION REJECTED: actual equals documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: input=[1e-320, 1e-320], actual=0.0, expected=1e-320
```

Judge: BUG (medium) -- The inputs are valid finite positive floats. Fraction(x) preserves each float's exact value, so the expected result is correctly computed: the harmonic mean of these identical observations is exactly the representable input. Returning zero is not ordinary rounding error; intermediate floating-point reciprocals overflow to infinity even though the final result is representable. The supplied upstream diff does not fix harmonic_mean, and no duplicate is listed.

