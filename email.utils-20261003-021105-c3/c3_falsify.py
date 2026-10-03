import datetime
import email.utils
import random
import time


class ZeroOffset(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return "ZeroOffset"

    def __repr__(self):
        return "ZeroOffset()"


def reference(dt):
    assert dt.tzinfo is not None
    assert dt.utcoffset() == datetime.timedelta(0)
    year = dt.year
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    lengths = [31, 29 if leap else 28, 31, 30, 31, 30,
               31, 31, 30, 31, 30, 31]
    previous_year = year - 1
    days = (
        365 * previous_year
        + previous_year // 4
        - previous_year // 100
        + previous_year // 400
        + sum(lengths[:dt.month - 1])
        + dt.day - 1
    )
    weekday = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")[days % 7]
    month = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[dt.month - 1]
    return (
        f"{weekday}, {dt.day:02d} {month} {year:04d} "
        f"{dt.hour:02d}:{dt.minute:02d}:{dt.second:02d} GMT"
    )


def actual(dt):
    try:
        return ("result", email.utils.format_datetime(dt, usegmt=True))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def main():
    start = time.monotonic()
    sanity_inputs = [
        datetime.datetime(2024, 2, 29, 12, 34, 56,
                          tzinfo=datetime.timezone.utc),
        datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc),
    ]
    sanity_failed = False
    for dt in sanity_inputs:
        expected = reference(dt)
        observed = actual(dt)
        agrees = observed == ("result", expected)
        print("SANITY:", repr(dt), repr(observed), repr(expected), agrees)
        sanity_failed |= not agrees
    if sanity_failed:
        print("SANITY FAILED")
        return

    tested = 0

    def check(dt):
        nonlocal tested
        expected = reference(dt)
        observed = actual(dt)
        tested += 1
        if observed != ("result", expected):
            repeated = actual(dt)
            if repeated != ("result", expected):
                print("COUNTEREXAMPLE:")
                print(repr(dt))
                print("actual:", repr(repeated))
                print("expected:", repr(expected))
                return True
        return False

    zones = [
        datetime.timezone.utc,
        datetime.timezone(datetime.timedelta(0), "CustomZero"),
        ZeroOffset(),
    ]
    edges = [
        (1, 1, 1, 0, 0, 0, 0),
        (9999, 12, 31, 23, 59, 59, 999999),
        (2000, 2, 29, 23, 59, 59, 0),
        (2024, 2, 29, 0, 0, 0, 999999),
        (1900, 12, 31, 23, 59, 59, 0),
        (2001, 1, 1, 0, 0, 0, 0),
    ]
    for fields in edges:
        for zone in zones:
            if time.monotonic() - start >= 175:
                print("NO COUNTEREXAMPLE", tested)
                return
            if check(datetime.datetime(*fields, tzinfo=zone)):
                return

    rng = random.Random(8675309)
    while time.monotonic() - start < 175:
        year = rng.randint(1, 9999)
        month = rng.randint(1, 12)
        leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        lengths = [31, 29 if leap else 28, 31, 30, 31, 30,
                   31, 31, 30, 31, 30, 31]
        dt = datetime.datetime(
            year, month, rng.randint(1, lengths[month - 1]),
            rng.randrange(24), rng.randrange(60), rng.randrange(60),
            rng.randrange(1000000), tzinfo=rng.choice(zones),
            fold=rng.randrange(2),
        )
        if check(dt):
            return
    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()