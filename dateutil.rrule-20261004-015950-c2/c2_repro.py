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