*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `dateutil.rrule`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Negative Easter offsets can wrap to unrelated dates

Target: `dateutil.rrule.rrule`

Property: For YEARLY rules with a naive midnight dtstart, count=1, and an integer byeaster offset k, every emitted date must equal Easter Sunday of some Gregorian year plus timedelta(days=k). Test especially k=-100, where the intended offset crosses into the preceding calendar year.

### Draft issue: YEARLY byeaster produces incorrect dates for negative offsets crossing a year boundary

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

**Documented behaviour:** The rrule constructor documentation for byeaster states: "Each integer will define an offset from the Easter Sunday." It explicitly allows integers "positive or negative."

**Expected:** [datetime.datetime(2009, 1, 2, 0, 0)]

**Actual:** [datetime.datetime(2008, 12, 21, 0, 0)]

**Reproducer:**

```python
from datetime import datetime, timedelta
from dateutil.rrule import rrule, YEARLY

def easter(y):  # Independent Gregorian computus
    a = y % 19
    b, c = divmod(y, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    n = h + l - 7*m + 114
    return datetime(y, n // 31, n % 31 + 1)

p = dict(freq=YEARLY, dtstart=datetime(2008, 1, 1),
         count=1, byeaster=-100)
s, k = p["dtstart"], p["byeaster"]
# Documentation permits negative integer offsets, without a lower bound.
if not (type(k) is int and s.tzinfo is None
        and s == datetime(s.year, s.month, s.day)
        and p["freq"] == YEARLY and p["count"] == 1):
    print("REFUTATION REJECTED: input does not satisfy the stated conditions")
else:
    actual = list(rrule(**p))
    expected = [min(easter(y) + timedelta(days=k)
                    for y in range(2008, 2011)
                    if easter(y) + timedelta(days=k) >= s)]
    if actual != expected:
        print("REFUTATION CONFIRMED:", p, "actual:", actual,
              "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual matches documented expectation",
              p, actual)
```

**Output:**

```
REFUTATION CONFIRMED: {'freq': 0, 'dtstart': datetime.datetime(2008, 1, 1, 0, 0), 'count': 1, 'byeaster': -100} actual: [datetime.datetime(2008, 12, 21, 0, 0)] expected: [datetime.datetime(2009, 1, 2, 0, 0)]
```

Judge: BUG (medium) -- The documentation explicitly permits negative integer offsets from Easter Sunday. The input is valid, and the independent computus gives Easter 2009 as April 12, making its -100-day offset January 2, 2009—the first qualifying occurrence after dtstart. The emitted December 21, 2008 is not Easter Sunday minus 100 days for any Gregorian year: adding 100 days gives March 31, 2009, not Easter. No duplicate was identified.

