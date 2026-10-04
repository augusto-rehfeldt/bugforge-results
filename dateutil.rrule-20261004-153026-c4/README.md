*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `dateutil.rrule`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: RDATE with valid VALUE=DATE should parse

Target: `dateutil.rrule.rrulestr`

Property: For a nonempty sequence of distinct Gregorian dates in years 1000–9999, parsing 'RDATE;VALUE=DATE:' followed by their comma-separated YYYYMMDD representations must yield their sorted midnight datetime equivalents, rather than raise an exception.

### Draft issue: rrulestr rejects RFC-valid RDATE;VALUE=DATE entries

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

**Documented behaviour:** The rrulestr documentation says: "Parses a string representation of a recurrence rule or set of recurrence rules." The module describes its implementation as supporting "the recurrence rules documented in the iCalendar RFC". RFC 5545 §3.8.5.2 explicitly permits DATE values for RDATE.

**Expected:** Return midnight datetimes for 2023-12-31, 2024-02-29, and 2024-03-01, in that order.

**Actual:** Raises ValueError: unsupported RDATE parm: VALUE=DATE.

**Reproducer:**

```python
from datetime import date, datetime, time
from dateutil.rrule import rrulestr

dates = [date(2024, 3, 1), date(2024, 2, 29), date(2023, 12, 31)]
s = "RDATE;VALUE=DATE:" + ",".join(f"{d.year:04}{d.month:02}{d.day:02}" for d in dates)

# RFC 5545 §3.8.5.2 permits comma-separated DATE values for RDATE.
if not dates or len(set(dates)) != len(dates) or not all(1000 <= d.year <= 9999 for d in dates):
    print("REFUTATION REJECTED: invalid input")
else:
    expected = ("result", [datetime.combine(d, time()) for d in sorted(dates)])
    try:
        actual = ("result", list(rrulestr(s)))
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(s), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual matches documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: 'RDATE;VALUE=DATE:20240301,20240229,20231231' actual: ('exception', 'ValueError', 'unsupported RDATE parm: VALUE=DATE') expected: ('result', [datetime.datetime(2023, 12, 31, 0, 0), datetime.datetime(2024, 2, 29, 0, 0), datetime.datetime(2024, 3, 1, 0, 0)])
```

Judge: BUG (medium) -- The reproducer supplies distinct, valid Gregorian DATE values using RFC 5545's permitted RDATE;VALUE=DATE syntax. Midnight datetime equivalents in chronological order are consistent with rrulestr's datetime-based recurrence-set interface. Rejecting the explicitly permitted VALUE=DATE parameter conflicts with the documented iCalendar recurrence support. The listed merged PR concerns EXDATE, not this RDATE failure, so it does not establish a duplicate.

