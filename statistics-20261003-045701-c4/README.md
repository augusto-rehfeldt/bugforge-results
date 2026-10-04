*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `statistics`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Median of two equal finite floats must equal that value

Target: `statistics.median`

Property: For every finite positive float x, median([x, x]) must equal x, the arithmetic average of the two middle values.

### Draft issue: statistics.median overflows for large finite middle values

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `statistics`

**Documented behaviour:** The median() docstring states: "When the number of data points is even, the median is interpolated by taking the average of the two middle values".

**Expected:** statistics.median([1e308, 1e308]) returns 1e308.

**Actual:** Returns inf.

**Reproducer:**

```python
import math, statistics

data = [1e308, 1e308]
if not all(math.isfinite(x) and x > 0 for x in data):
    print("REFUTATION REJECTED: input is not finite positive numeric data")
else:
    actual = statistics.median(data)
    expected = data[0] / 2 + data[1] / 2
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual equals the documented average")
```

**Output:**

```
REFUTATION CONFIRMED: [1e+308, 1e+308] actual: inf expected: 1e+308
```

Judge: BUG (medium) -- The inputs are valid finite positive floats. The average of two identical values is that value, and 1e308 is representable. The reported infinity results from intermediate overflow, not ordinary rounding of the median. The reproducer's expected calculation is correct for these inputs. The supplied upstream diff does not change median, and no duplicate was found.

