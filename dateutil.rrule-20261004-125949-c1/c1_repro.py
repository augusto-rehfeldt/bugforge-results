from datetime import datetime, timedelta
from dateutil.rrule import rrule, YEARLY

def easter(y):  # Independent Gregorian computus
    a = y % 19
    b, c = divmod(y, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    n = h + l - 7*m + 114
    return datetime(y, n // 31, n % 31 + 1)

p = dict(freq=YEARLY, dtstart=datetime(2008, 1, 1),
         count=1, byeaster=-100)
s, k = p["dtstart"], p["byeaster"]
# Documentation permits negative integer offsets, without a lower bound.
if not (type(k) is int and s.tzinfo is None
        and s == datetime(s.year, s.month, s.day)
        and p["freq"] == YEARLY and p["count"] == 1):
    print("REFUTATION REJECTED: input does not satisfy the stated conditions")
else:
    actual = list(rrule(**p))
    expected = [min(easter(y) + timedelta(days=k)
                    for y in range(2008, 2011)
                    if easter(y) + timedelta(days=k) >= s)]
    if actual != expected:
        print("REFUTATION CONFIRMED:", p, "actual:", actual,
              "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual matches documented expectation",
              p, actual)