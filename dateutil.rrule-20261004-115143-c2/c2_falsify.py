import calendar
import random
import time
from datetime import datetime
from dateutil.rrule import rrule, MONTHLY, TU, SA

deadline = time.monotonic() + 175.0


def bounds(year, month):
    last = calendar.monthrange(year, month)[1]
    return datetime(year, month, 1), datetime(year, month, last)


def reference(year, month, tuesdays=True, first_saturday=True):
    start, end = bounds(year, month)
    result = []
    seen_saturday = False
    for day in range(1, end.day + 1):
        dt = datetime(year, month, day)
        weekday = dt.weekday()
        if weekday == 1 and tuesdays:
            result.append(dt)
        if weekday == 5 and not seen_saturday:
            seen_saturday = True
            if first_saturday:
                result.append(dt)
    return result


# Ordinary inputs exercise each documented weekday form separately.
for label, weekdays, tuesdays, saturday in (
    ("all Tuesdays", (TU,), True, False),
    ("first Saturday", (SA(1),), False, True),
):
    start, end = bounds(2024, 2)
    actual = list(rrule(
        MONTHLY, dtstart=start, until=end, byweekday=weekdays
    ))
    expected = reference(2024, 2, tuesdays, saturday)
    agrees = actual == expected
    print("SANITY:", label, agrees)
    if not agrees:
        print("SANITY FAILED")
        raise SystemExit(0)


def evaluate(year, month):
    start, end = bounds(year, month)
    expected = reference(year, month)
    try:
        actual = list(rrule(
            MONTHLY, dtstart=start, until=end, byweekday=(TU, SA(1))
        ))
        return actual, expected
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc)), expected


tested = 0


def check(year, month):
    global tested
    actual, expected = evaluate(year, month)
    tested += 1
    if actual != expected:
        repeated, repeated_expected = evaluate(year, month)
        if repeated == actual and repeated_expected == expected:
            print("COUNTEREXAMPLE:")
            print(repr({
                "year": year,
                "month": month,
                "dtstart_day": 1,
                "until_day": bounds(year, month)[1].day,
                "hour": 0,
                "frequency": "MONTHLY",
                "byweekday": ("TU", "SA(1)"),
            }))
            print("actual:", repr(actual))
            print("expected:", repr(expected))
            raise SystemExit(0)


edge_cases = [
    (1, 1), (1, 2), (4, 2),
    (1900, 2), (2000, 2),
    (2024, 2), (2024, 6), (2024, 10),
    (9998, 2), (9998, 12),
]

for year, month in edge_cases:
    if time.monotonic() >= deadline:
        break
    check(year, month)

rng = random.Random(0x5545)
while time.monotonic() < deadline:
    check(rng.randint(1, 9998), rng.randint(1, 12))

print("NO COUNTEREXAMPLE", tested)