from decimal import Decimal
from isodate import Duration, duration_isoformat

years = Decimal(10) ** -7
d = Duration(years=years)
try:
    if not (years.is_finite() and years >= 0 and
            d.years == years and d.months == 0 and
            d.days == d.seconds == d.microseconds == 0):
        print("REFUTATION REJECTED: invalid year-only duration")
    else:
        # ISO 8601 permits a decimal fraction on the lowest-order component.
        expected = "P" + format(years, "f") + "Y"
        actual = duration_isoformat(d)
        if actual != expected:
            print("REFUTATION CONFIRMED:",
                  {"years": str(years), "actual": actual, "expected": expected})
        else:
            print("REFUTATION REJECTED: output matches the ISO 8601 expectation")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))