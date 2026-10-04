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