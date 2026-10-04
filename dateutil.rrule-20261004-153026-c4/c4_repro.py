from datetime import date, datetime, time
from dateutil.rrule import rrulestr

dates = [date(2024, 3, 1), date(2024, 2, 29), date(2023, 12, 31)]
s = "RDATE;VALUE=DATE:" + ",".join(f"{d.year:04}{d.month:02}{d.day:02}" for d in dates)

# RFC 5545 §3.8.5.2 permits comma-separated DATE values for RDATE.
if not dates or len(set(dates)) != len(dates) or not all(1000 <= d.year <= 9999 for d in dates):
    print("REFUTATION REJECTED: invalid input")
else:
    expected = ("result", [datetime.combine(d, time()) for d in sorted(dates)])
    try:
        actual = ("result", list(rrulestr(s)))
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(s), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual matches documented expectation")