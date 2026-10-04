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