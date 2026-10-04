*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `more_itertools`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `more_itertools` 11.1.0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Running median overflows for finite, equal observations

Target: `more_itertools.running_median`

Property: For every finite positive float x and integer n >= 1, running_median([x] * n) must yield n values equal to x: the median of every nonempty prefix of identical observations is x.

### Draft issue: running_median overflows for identical large finite floats

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `more_itertools` 11.1.0

**Documented behaviour:** The running_median docstring promises: "Yield the median of the elements seen so far."

**Expected:** [1e308, 1e308]

**Actual:** [1e308, inf]

**Reproducer:**

```python
import math
from fractions import Fraction
from statistics import median
import more_itertools

xs = [1e308, 1e308]
if not xs or not all(isinstance(x, float) and math.isfinite(x) and x > 0 for x in xs):
    print("REFUTATION REJECTED: invalid input")
else:
    actual = list(more_itertools.running_median(xs))
    expected = [float(median(list(map(Fraction, xs[:i])))) for i in range(1, len(xs) + 1)]
    if actual != expected:
        print("REFUTATION CONFIRMED:", xs, actual, expected)
    else:
        print("REFUTATION REJECTED: actual matches the documented medians")
```

**Output:**

```
REFUTATION CONFIRMED: [1e+308, 1e+308] [1e+308, inf] [1e+308, 1e+308]
```

Judge: BUG (medium) -- The input contains valid finite positive floats. Every prefix consists of identical observations, so its median is exactly 1e308; the Fraction-based reference correctly avoids intermediate overflow. Returning infinity breaks the documented promise, rather than merely introducing rounding error. The listed pull request concerns windowed data, not this overflow behaviour.

