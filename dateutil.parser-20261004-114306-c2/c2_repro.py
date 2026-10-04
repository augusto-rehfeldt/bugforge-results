from datetime import date
from dateutil.parser.isoparser import isoparser

y, d = 2021, 1
s = f"{y:04d}-W53-{d}"
if not (1 <= y <= 9998 and 1 <= d <= 7
        and date(y, 12, 28).isocalendar().week == 52):
    print("REFUTATION REJECTED: invalid test premise")
else:
    # Documented YYYY-Www-D syntax; independently check ISO validity.
    try:
        expected = date.fromisocalendar(y, 53, d)
    except ValueError:
        expected = ValueError
    try:
        actual = isoparser().parse_isodate(s)
    except Exception as e:
        actual = type(e)
    if expected is ValueError and actual is not ValueError:
        print("REFUTATION CONFIRMED:", repr(s),
              "actual=", actual, "expected=ValueError")
    else:
        print("REFUTATION REJECTED:", repr(s),
              "actual=", actual, "expected=", expected)