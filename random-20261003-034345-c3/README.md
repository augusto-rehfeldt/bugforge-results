*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `random`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Triangular samples escape finite bounds when interval subtraction overflows

Target: `random.triangular`

Property: For finite float bounds low < high and mode=None, every returned sample must satisfy low <= sample <= high.

### Draft issue: random.triangular returns infinity for finite bounds when their difference overflows

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

**Documented behaviour:** "Continuous distribution bounded by given lower and upper limits, and having a given mode value in-between." — Random.triangular docstring.

**Expected:** A finite sample in [-1e308, 1e308].

**Actual:** random.triangular(-1e308, 1e308, None) returns -inf after random.seed(0).

**Reproducer:**

```python
import random, math

seed, low, high, mode = inp = (0, -1e308, 1e308, None)
if not (math.isfinite(low) and math.isfinite(high) and low < high and mode is None):
    print("REFUTATION REJECTED:", inp, "invalid input")
else:
    random.seed(seed)
    actual = random.triangular(low, high, mode)
    if not low <= actual <= high:
        print("REFUTATION CONFIRMED:", inp, "actual=", actual, "expected=", (low, high))
    else:
        print("REFUTATION REJECTED:", inp, "sample is within the documented interval")
```

**Output:**

```
REFUTATION CONFIRMED: (0, -1e+308, 1e+308, None) actual= -inf expected= (-1e+308, 1e+308)
```

Judge: BUG (medium) -- The reproducer uses finite, strictly ordered bounds and the supported default mode. The documented bounded distribution excludes infinite results. Computing high - low overflows to infinity; with seed 0, the reflected branch then produces -inf. This is not ordinary rounding error. The listed issue concerns equal bounds, and the upstream diff does not fix triangular.

