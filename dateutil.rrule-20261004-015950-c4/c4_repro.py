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