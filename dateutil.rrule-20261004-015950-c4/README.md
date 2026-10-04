*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `dateutil.rrule`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: String round-trip loses timezone-aware recurrence dates

Target: `dateutil.rrule.rrulestr`

Property: For any finite rrule with a timezone-aware dtstart, positive count, and DAILY frequency, parsing its string representation with rrulestr(str(rule)) must reproduce the same recurrence datetimes, including timezone awareness.

### Draft issue: rrule.__str__ loses UTC DTSTART timezone on rrulestr round-trip

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

**Documented behaviour:** The rrule.__str__ docstring states: "Output a string that would generate this RRULE if passed to rrulestr."

**Expected:** rrulestr(str(rule)) yields datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc).

**Actual:** str(rule) emits DTSTART:20250101T000000 without a UTC marker; rrulestr yields datetime(2025, 1, 1, 0, 0) with no timezone.

**Reproducer:**

```python
from datetime import datetime, timezone, timedelta
from dateutil.rrule import DAILY, rrule, rrulestr

try:
    start, count = datetime(2025, 1, 1, tzinfo=timezone.utc), 1
    if start.utcoffset() is None or count <= 0:
        raise ValueError("Invalid aware DTSTART or positive COUNT")
    rule = rrule(DAILY, dtstart=start, count=count)
    text = str(rule)
    actual = list(rrulestr(text))
    expected = [start + timedelta(days=i) for i in range(count)]
    if actual != expected:
        print("REFUTATION CONFIRMED:", "input =", repr(text),
              "actual =", actual, "expected =", expected)
    else:
        print("REFUTATION REJECTED: documented round-trip agrees")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: input = 'DTSTART:20250101T000000\nRRULE:FREQ=DAILY;COUNT=1' actual = [datetime.datetime(2025, 1, 1, 0, 0)] expected = [datetime.datetime(2025, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)]
```

Judge: BUG (medium) -- The valid UTC-aware DAILY rule with COUNT=1 isolates a loss of timezone information, with no recurrence arithmetic ambiguity. The __str__ docstring explicitly promises a string that regenerates the rule through rrulestr, but serialization omits the UTC marker and parsing consequently produces a naive datetime. None of the listed issues or pull requests reports or fixes this timezone-loss behavior.

