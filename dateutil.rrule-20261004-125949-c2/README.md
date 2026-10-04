*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `dateutil.rrule`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Replacing frequency loses an explicitly supplied ordinal weekday

Target: `dateutil.rrule.rrule.replace`

Property: For naive datetime dtstart, positive count, and n in {-4,-3,-2,-1,1,2,3,4}, let r = rrule(DAILY, dtstart=dtstart, count=count, byweekday=TU(n)). Then list(r.replace(freq=MONTHLY)) must equal list(rrule(MONTHLY, dtstart=dtstart, count=count, byweekday=TU(n))), preserving the explicitly supplied weekday parameter while changing only frequency.

### Draft issue: rrule.replace loses ordinal byweekday when changing DAILY frequency to MONTHLY

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

**Documented behaviour:** rrule.replace docstring: "Return new rrule with same attributes except for those attributes given new values by whichever keyword arguments are specified." The byweekday parameter documentation describes n as "the nth occurrence of this weekday in the period."

**Expected:** 2024-01-02, 2024-02-06, 2024-03-05, matching a directly constructed MONTHLY rule with byweekday=TU(+1).

**Actual:** 2024-01-02, 2024-01-09, 2024-01-16: every Tuesday rather than the first Tuesday of each month.

**Reproducer:**

```python
from datetime import datetime, timedelta
from dateutil.rrule import rrule, DAILY, MONTHLY, TU

dtstart, count, n = datetime(2024, 1, 1), 3, 1
data = dict(dtstart=dtstart, count=count, byweekday=TU(n),
            freq=DAILY, replace=dict(freq=MONTHLY))

# Naive start, positive count, documented ordinal weekday.
if dtstart.tzinfo is not None or count <= 0 or n not in (-4, -3, -2, -1, 1, 2, 3, 4):
    print("REFUTATION REJECTED: invalid input", data)
else:
    r = rrule(DAILY, dtstart=dtstart, count=count, byweekday=TU(n))
    actual = list(r.replace(freq=MONTHLY))
    # Independently compute the first Tuesday of each month.
    expected = []
    year, month = dtstart.year, dtstart.month
    while len(expected) < count:
        first = datetime(year, month, 1)
        tuesday = first + timedelta(days=(1 - first.weekday()) % 7)
        if tuesday >= dtstart:
            expected.append(tuesday)
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, "actual =", actual, "expected =", expected)
    else:
        print("REFUTATION REJECTED: actual equals documented expectation", data)
```

**Output:**

```
REFUTATION CONFIRMED: {'dtstart': datetime.datetime(2024, 1, 1, 0, 0), 'count': 3, 'byweekday': TU(+1), 'freq': 3, 'replace': {'freq': 1}} actual = [datetime.datetime(2024, 1, 2, 0, 0), datetime.datetime(2024, 1, 9, 0, 0), datetime.datetime(2024, 1, 16, 0, 0)] expected = [datetime.datetime(2024, 1, 2, 0, 0), datetime.datetime(2024, 2, 6, 0, 0), datetime.datetime(2024, 3, 5, 0, 0)]
```

Judge: BUG (medium) -- replace promises to preserve attributes not explicitly changed. The valid DAILY rule accepts TU(+1), but replacing only freq loses the supplied ordinal and behaves as though byweekday were TU. The reproducer correctly calculates the first Tuesday of each month for n=1. The listed time-zone PR is unrelated; upstream status was not checked.

