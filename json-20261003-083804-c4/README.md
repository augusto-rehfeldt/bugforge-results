*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `json`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `json`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Overridden float comparisons can bypass NaN rejection

Target: `json.JSONEncoder.iterencode`

Property: For every float instance x whose underlying floating-point value is NaN, including float subclasses overriding equality comparisons, consuming JSONEncoder(allow_nan=False).iterencode([x]) must raise ValueError.

### Draft issue: json.JSONEncoder.iterencode allows NaN float subclasses with allow_nan=False

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `json`

**Documented behaviour:** json.JSONEncoder documentation: "If allow_nan is false (default: True), then it will be a ValueError to serialize out of range float values (nan, inf, -inf) in strict compliance of the JSON specification."

**Expected:** Consuming iterencode([x]) raises ValueError.

**Actual:** Iteration completes and produces '[nan]', which is invalid JSON.

**Reproducer:**

```python
import json
import math

class NaN(float):
    def __eq__(self, other): return False
    def __ne__(self, other): return False

x = NaN("nan")
data = [x]
if not (isinstance(x, float) and math.isnan(float(x))):
    print("REFUTATION REJECTED: input is not a NaN float instance")
else:
    expected = ("exception", "ValueError") if not math.isfinite(float(x)) else None
    try:
        actual = ("result", "".join(json.JSONEncoder(allow_nan=False).iterencode(data)))
    except Exception as e:
        actual = ("exception", type(e).__name__)
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, "actual =", actual, "expected =", expected)
    else:
        print("REFUTATION REJECTED: documented ValueError was raised")
```

**Output:**

```
REFUTATION CONFIRMED: [nan] actual = ('result', '[nan]') expected = ('exception', 'ValueError')
```

Judge: BUG (medium) -- The input is a valid float subclass with an underlying NaN value, and the expected ValueError follows directly from allow_nan=False. The Python encoder's NaN check relies on x != x, which this subclass overrides to return False, allowing NaN to fall through to float representation and bypass strict validation. The supplied issue concerns unrelated default/cls handling; the upstream diff does not address this behavior.

