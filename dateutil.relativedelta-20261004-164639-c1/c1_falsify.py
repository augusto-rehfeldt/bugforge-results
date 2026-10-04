import datetime
import random
import time

from dateutil.relativedelta import relativedelta


def reference(d, k):
    leap = d.year % 4 == 0 and (d.year % 100 != 0 or d.year % 400 == 0)
    return d - datetime.timedelta(days=k if leap and d.month >= 3 else 0)


def actual(d, k):
    try:
        return ("result", d - relativedelta(leapdays=k))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def main():
    deadline = time.monotonic() + 175

    for d, k in [
        (datetime.date(2023, 3, 10), 1),
        (datetime.date(2024, 2, 28), 28),
    ]:
        expected = reference(d, k)
        observed = actual(d, k)
        print("SANITY:", repr((d.year, d.month, d.day, k)),
              "actual:", repr(observed), "expected:", repr(expected))
        if observed != ("result", expected):
            print("SANITY FAILED")
            return

    tested = 0

    def check(d, k):
        nonlocal tested
        expected = reference(d, k)
        observed = actual(d, k)
        tested += 1
        if observed != ("result", expected):
            repeated = actual(d, k)
            if repeated == observed:
                value = observed[1] if observed[0] == "result" else observed
                print("COUNTEREXAMPLE:", repr((d.year, d.month, d.day, k)),
                      "actual:", repr(value), "expected:", repr(expected))
                return True
        return False

    for year, month, day in [
        (2024, 3, 10),
        (2024, 3, 1),
        (2000, 3, 1),
        (4, 3, 1),
        (9996, 12, 31),
        (2024, 12, 31),
    ]:
        for k in (1, 28, 2, 14):
            if check(datetime.date(year, month, day), k):
                return

    rng = random.Random(20240310)
    leap_years = [
        y for y in range(1, 10000)
        if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)
    ]

    while time.monotonic() < deadline:
        year = rng.choice(leap_years)
        start = datetime.date(year, 3, 1)
        span = (datetime.date(year, 12, 31) - start).days
        d = start + datetime.timedelta(days=rng.randrange(span + 1))
        if check(d, rng.randint(1, 28)):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()