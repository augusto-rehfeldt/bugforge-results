*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: fmean overflows for a finite, representable arithmetic mean

Target: `statistics.fmean`

Property: For every finite float x in [1e308, 1.7e308] and integer n in [2, 10], fmean([x] * n) must return approximately x (relative tolerance 1e-15), without raising an exception.

### Draft issue: statistics.fmean raises OverflowError for finite inputs with a representable mean

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** "Convert data to floats and compute the arithmetic mean." — statistics.fmean docstring.

**Expected:** Return approximately 1e308 without raising.

**Actual:** OverflowError: intermediate overflow in fsum

**Reproducer:**

```python
import statistics, math
from fractions import Fraction

data = [1e308, 1e308]
if not data or not all(isinstance(x, float) and math.isfinite(x) for x in data):
    print("REFUTATION REJECTED: input is not nonempty finite float data")
else:
    expected = float(sum(map(Fraction, data), Fraction()) / len(data))
    try:
        actual = statistics.fmean(data)
        broken = not math.isclose(actual, expected, rel_tol=1e-15)
    except Exception as e:
        actual = f"{type(e).__name__}: {e}"
        broken = True
    if broken:
        print(f"REFUTATION CONFIRMED: input={data!r}, actual={actual!r}, expected={expected!r}")
    else:
        print("REFUTATION REJECTED: result matches the independently computed arithmetic mean")
```

**Output:**

```
REFUTATION CONFIRMED: input=[1e+308, 1e+308], actual='OverflowError: intermediate overflow in fsum', expected=1e+308
```

Judge: BUG (medium) -- The input contains valid finite floats, and the exact-rational reference correctly yields the representable mean 1e308. fmean raises because its intermediate sum overflows, not because the mean is unrepresentable or rounding exceeds the tolerance. This defeats its documented arithmetic-mean operation. None of the listed issues addresses this behaviour, and the upstream diff retains fsum(data).

