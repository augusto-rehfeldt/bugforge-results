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