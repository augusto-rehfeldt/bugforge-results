*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `dateutil.rrule`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: replace(interval=...) loses originally supplied BYHOUR values

Target: `dateutil.rrule.rrule.replace`

Property: For naive datetime dtstart, positive integer intervals i and j, nonempty byhour subsets of 0..23, and positive count, whenever both constructions are valid, list(rrule(HOURLY, dtstart=dtstart, interval=i, byhour=hours, count=count).replace(interval=j)) must equal list(rrule(HOURLY, dtstart=dtstart, interval=j, byhour=hours, count=count)).

### Draft issue: rrule.replace(interval=...) loses byhour values excluded by the original interval

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

**Documented behaviour:** "Return new rrule with same attributes except for those attributes given new values by whichever keyword arguments are specified." — rrule.replace docstring.

**Expected:** 2024-01-01T00:00:00, 2024-01-01T01:00:00, 2024-01-02T00:00:00

**Actual:** 2024-01-01T00:00:00, 2024-01-02T00:00:00, 2024-01-03T00:00:00

**Reproducer:**

```python
from datetime import datetime, timedelta
from dateutil.rrule import rrule, HOURLY

dtstart, i, j, hours, count = datetime(2024, 1, 1), 2, 1, (0, 1), 3
data = dict(dtstart=dtstart.isoformat(), i=i, j=j, hours=hours, count=count)
try:
    if not (dtstart.tzinfo is None and
            all(type(n) is int and n > 0 for n in (i, j, count)) and
            hours and all(type(h) is int and 0 <= h <= 23 for h in hours)):
        raise ValueError("input outside documented domain")
    original = rrule(HOURLY, dtstart=dtstart, interval=i, byhour=hours, count=count)
    list(original)
    list(rrule(HOURLY, dtstart=dtstart, interval=j, byhour=hours, count=count))
    actual = [d.isoformat() for d in original.replace(interval=j)]
    expected, d = [], dtstart
    while len(expected) < count:
        if d.hour in hours:
            expected.append(d.isoformat())
        d += timedelta(hours=j)
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual equals independent expectation")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: {'dtstart': '2024-01-01T00:00:00', 'i': 2, 'j': 1, 'hours': (0, 1), 'count': 3} actual: ['2024-01-01T00:00:00', '2024-01-02T00:00:00', '2024-01-03T00:00:00'] expected: ['2024-01-01T00:00:00', '2024-01-01T01:00:00', '2024-01-02T00:00:00']
```

Judge: BUG (medium) -- The inputs are valid, and replace explicitly promises to preserve attributes other than those overridden. Changing interval from 2 to 1 must retain byhour=(0, 1), including hour 1 even though it was unreachable under the original interval. The independent expectation correctly enumerates this hourly recurrence. The output shows replace instead retains the original interval's effective hour restriction. No matching issue or pull request was supplied.

