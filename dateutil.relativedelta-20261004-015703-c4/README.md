*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `dateutil.relativedelta`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Equivalent Tuesday weekday specifications violate hash consistency

Target: `dateutil.relativedelta.TU`

Property: For arbitrary valid integer relative offsets, let a = relativedelta(weekday=TU, **offsets) and b = relativedelta(weekday=TU(1), **offsets). The documented equivalence requires a == b and hash(a) == hash(b), so the two equivalent specifications remain interchangeable as dictionary keys.

### Draft issue: Equal relativedelta objects with default and explicit +1 weekdays have different hashes

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

**Documented behaviour:** The relativedelta class documentation, under weekday, states: "Not specifying it is the same as specifying +1."

**Expected:** relativedelta(weekday=TU) and relativedelta(weekday=TU(1)) compare equal and have equal hashes.

**Actual:** They compare equal but have unequal hashes: (True, False).

**Reproducer:**

```python
from dateutil.relativedelta import relativedelta, TU

offsets = {}
w = TU(1)
data = {"offsets": offsets, "left_weekday": ("TU", TU.n),
        "right_weekday": ("TU", w.n)}
if TU.weekday != 1 or TU.n is not None or w.weekday != 1 or w.n != 1:
    print("REFUTATION REJECTED: input is not the documented Tuesday/default/+1 case")
else:
    a = relativedelta(weekday=TU, **offsets)
    b = relativedelta(weekday=w, **offsets)
    actual = (a == b, hash(a) == hash(b))
    # Empty offsets are valid; documented default +1 makes both specifications
    # equivalent, and equal hashable objects must have equal hashes.
    expected = (True, True)
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: equality and hashes match the documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: {'offsets': {}, 'left_weekday': ('TU', None), 'right_weekday': ('TU', 1)} actual: (True, False) expected: (True, True)
```

Judge: BUG (medium) -- The reproducer uses valid inputs and directly checks the documented default weekday equivalence. The objects actually compare equal, so Python's hash contract requires equal hashes regardless of whether the documentation explicitly promises dictionary-key interchangeability. Unequal hashes violate that contract and can prevent lookup using an equivalent key. No duplicate was provided; upstream fix status is unverified.

