from datetime import date, timedelta
from calendar import isleap
from dateutil.relativedelta import relativedelta

d, k = date(2024, 3, 10), 1
if not (isleap(d.year) and 3 <= d.month <= 12 and type(k) is int and 1 <= k <= 28):
    print("REFUTATION REJECTED:", "input outside documented conditions")
else:
    actual = relativedelta(leapdays=k).__rsub__(d)
    expected = d - timedelta(days=k)
    if actual != expected:
        print("REFUTATION CONFIRMED:", (d.year, d.month, d.day, k),
              "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "actual matches documented expectation")