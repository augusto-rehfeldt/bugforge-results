*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `dateutil.relativedelta`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Subtracting leapdays adds them instead

Target: `dateutil.relativedelta.relativedelta.__rsub__`

Property: For a date d in March through December of a leap year and an integer k with 1 <= k <= 28, d - relativedelta(leapdays=k) must equal d - datetime.timedelta(days=k).

### Draft issue: Subtracting relativedelta fails to negate the leapdays adjustment

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

**Documented behaviour:** The relativedelta class documentation says relative information "may be negative" and that "adding or subtracting a relativedelta with relative information performs the corresponding arithmetic operation"; its leapdays entry says "Will add given days to the date found, if year is a leap year, and the date found is post 28 of february."

**Expected:** 2024-03-09

**Actual:** 2024-03-11

**Reproducer:**

```python
from datetime import date, timedelta
from calendar import isleap
from dateutil.relativedelta import relativedelta

d, k = date(2024, 3, 10), 1
if not (isleap(d.year) and 3 <= d.month <= 12 and type(k) is int and 1 <= k <= 28):
    print("REFUTATION REJECTED:", "input outside documented conditions")
else:
    actual = relativedelta(leapdays=k).__rsub__(d)
    expected = d - timedelta(days=k)
    if actual != expected:
        print("REFUTATION CONFIRMED:", (d.year, d.month, d.day, k),
              "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "actual matches documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: (2024, 3, 10, 1) actual: 2024-03-11 expected: 2024-03-09
```

Judge: BUG (medium) -- The input is valid and satisfies the documented leapdays condition. Subtracting relative information should reverse its arithmetic effect; instead, __rsub__ applies the positive leapdays adjustment and moves the date forward. The timedelta expectation is correct for this case, and no duplicate was supplied.

