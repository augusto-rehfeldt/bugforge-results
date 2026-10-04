import datetime as dt
import random
import time

from dateutil.easter import easter
from dateutil.rrule import YEARLY, rrule


def reference_easter(year):
    # Gregorian Meeus/Jones/Butcher computus, using exact integer arithmetic.
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, remainder = divmod(h + l - 7 * m + 114, 31)
    return dt.date(year, month, remainder + 1)


def reference_dates(year, offset):
    return [
        dt.datetime.combine(
            reference_easter(y) + dt.timedelta(days=offset),
            dt.time()
        )
        for y in range(year - 2, year + 5)
    ]


def run(year, offset):
    try:
        return list(rrule(
            YEARLY,
            dtstart=dt.datetime(year, 1, 1),
            count=1,
            byeaster=offset,
        ))
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def main():
    deadline = time.monotonic() + 170

    for year, offset in [(2024, 0), (2025, 7)]:
        expected = min(
            value for value in reference_dates(year, offset)
            if value >= dt.datetime(year, 1, 1)
        )
        actual = run(year, offset)
        ok = (
            reference_easter(year) == easter(year)
            and actual == [expected]
        )
        print("SANITY:", repr((year, offset)), repr(actual),
              repr([expected]), "OK" if ok else "FAILED")
        if not ok:
            print("SANITY FAILED")
            return

    tested = 0

    def check(year, offset):
        nonlocal tested
        tested += 1
        candidates = reference_dates(year, offset)
        actual = run(year, offset)
        valid = (
            isinstance(actual, list)
            and len(actual) == 1
            and actual[0] in candidates
        )
        if valid:
            return False

        repeated = run(year, offset)
        if repeated != actual:
            return False

        expected = min(
            value for value in candidates
            if value >= dt.datetime(year, 1, 1)
        )
        print("COUNTEREXAMPLE:")
        print(repr({
            "freq": YEARLY,
            "dtstart": (year, 1, 1, 0, 0, 0),
            "count": 1,
            "byeaster": offset,
        }))
        print("actual:", repr(actual))
        print("expected:", repr([expected]))
        return True

    edges = [
        (2000, -100), (2008, -100), (2016, -100),
        (2024, -100), (2030, -100),
        (2000, -120), (2000, -90), (2030, -120), (2030, -90),
    ]
    for year, offset in edges:
        if check(year, offset):
            return

    rng = random.Random(271828)
    for _ in range(10000):
        if time.monotonic() >= deadline:
            break
        if check(rng.randint(2000, 2030), rng.randint(-120, -90)):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()