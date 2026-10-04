*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `dateutil.rrule`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Mixing ordinary and ordinal weekdays should form a union

Target: `dateutil.rrule.TU`

Property: For a naive datetime dtstart at midnight on the first day of a month, a MONTHLY rule bounded by that month's last day with byweekday=(TU, SA(1)) must generate exactly all Tuesdays and the first Saturday of that month, in chronological order.

### Draft issue: MONTHLY rules with mixed ordinal and non-ordinal byweekday entries return no occurrences

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

**Documented behaviour:** The rrule constructor documentation for byweekday says: "a sequence of these constants" and "these variables will define the weekdays where the recurrence will be applied", and specifies that an ordinal means "the nth occurrence of this weekday in the period." RFC 5545 section 3.3.10 defines BYDAY as a comma-separated list of weekday values, each optionally prefixed by an ordinal.

**Expected:** January 2, 6, 9, 16, 23, and 30 of year 1, at midnight, in chronological order.

**Actual:** An empty list.

**Reproducer:**

```python
from datetime import datetime
from calendar import monthrange
from dateutil.rrule import rrule, MONTHLY, TU, SA

start, end = datetime(1, 1, 1), datetime(1, 1, 31)
args = dict(freq=MONTHLY, dtstart=start, until=end, byweekday=(TU, SA(1)))
valid = (
    start.tzinfo is None and start.day == 1 and start.hour == 0
    and end.day == monthrange(start.year, start.month)[1]
    and [(w.weekday, w.n) for w in args["byweekday"]] == [(1, None), (5, 1)]
)
if not valid:
    print("REFUTATION REJECTED: invalid reported input")
else:
    expected = [
        datetime(1, 1, d) for d in range(1, 32)
        if datetime(1, 1, d).weekday() == 1
        or (d <= 7 and datetime(1, 1, d).weekday() == 5)
    ]
    actual = list(rrule(**args))
    if actual != expected:
        print("REFUTATION CONFIRMED:", args, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual matches the documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: {'freq': 1, 'dtstart': datetime.datetime(1, 1, 1, 0, 0), 'until': datetime.datetime(1, 1, 31, 0, 0), 'byweekday': (TU, SA(+1))} actual: [] expected: [datetime.datetime(1, 1, 2, 0, 0), datetime.datetime(1, 1, 6, 0, 0), datetime.datetime(1, 1, 9, 0, 0), datetime.datetime(1, 1, 16, 0, 0), datetime.datetime(1, 1, 23, 0, 0), datetime.datetime(1, 1, 30, 0, 0)]
```

Judge: BUG (medium) -- The input is valid: year 1 is supported by datetime, and MONTHLY permits both ordinal and non-ordinal BYDAY entries. Those entries specify alternative matching weekdays, not an intersection. The expected dates correctly include all Tuesdays and the first Saturday of January 1, within the inclusive bounds. Returning no occurrences violates that documented behavior. No duplicate was supplied; upstream status remains unverified.

