*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `dateutil.rrule`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: String round trip preserves timezone-aware recurrences

Target: `dateutil.rrule.rrule.__str__`

Property: For an rrule with timezone-aware dtstart and finite count, parsing str(rule) with dateutil.rrule.rrulestr must reproduce the same recurrence datetimes, including their timezone awareness and represented instants.

### Draft issue: rrule.__str__ round-trip loses timezone-aware DTSTART

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `dateutil` 2.9.0.post0

**Documented behaviour:** The rrule.__str__ docstring states: "Output a string that would generate this RRULE if passed to rrulestr."

**Expected:** One occurrence at 2024-01-01 00:00:00+00:00, preserving UTC awareness and the represented instant.

**Actual:** One naive occurrence at 2024-01-01 00:00:00, with no timezone or unambiguous represented instant.

**Reproducer:**

```python
from datetime import datetime, timezone, timedelta
from dateutil.rrule import rrule, rrulestr, DAILY

data = {"start": (2024, 1, 1, 0, 0, 0), "offset_seconds": 0, "count": 1}
try:
    start = datetime(*data["start"], tzinfo=timezone(timedelta(seconds=data["offset_seconds"])))
    if not isinstance(data["count"], int) or data["count"] <= 0:
        raise ValueError("count must be a positive integer")
    # Aware DTSTART is supported; DAILY with COUNT=1 yields DTSTART itself.
    rule = rrule(DAILY, dtstart=start, count=data["count"])
    expected = [start]
    actual = list(rrulestr(str(rule)))
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: round-trip preserves the expected datetime")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: {'start': (2024, 1, 1, 0, 0, 0), 'offset_seconds': 0, 'count': 1} actual: [datetime.datetime(2024, 1, 1, 0, 0)] expected: [datetime.datetime(2024, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)]
```

Judge: BUG (medium) -- The docstring explicitly promises reconstruction through rrulestr. A UTC-aware DTSTART with DAILY and COUNT=1 is valid, and the expected occurrence is correctly computed as DTSTART itself. The output shows that serialization and parsing lose timezone awareness, so the reconstructed rule is not equivalent. PR #62 concerns general string serialization and does not specifically report or fix this timezone-loss behaviour.

