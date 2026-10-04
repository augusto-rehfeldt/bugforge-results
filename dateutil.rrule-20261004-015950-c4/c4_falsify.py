import random
import time
from datetime import datetime, timedelta, timezone
from dateutil.rrule import DAILY, rrule, rrulestr


def make_start(case):
    return datetime(
        case["year"], case["month"], case["day"],
        case["hour"], case["minute"], case["second"],
        tzinfo=timezone(timedelta(seconds=case["offset_seconds"]))
    )


def reference(case):
    start = make_start(case)
    return [start + timedelta(days=i) for i in range(case["count"])]


def aware(value):
    return value.tzinfo is not None and value.utcoffset() is not None


def check(case):
    expected = reference(case)
    try:
        rule = rrule(DAILY, dtstart=make_start(case), count=case["count"])
        actual = list(rrulestr(str(rule)))
        matches = (
            actual == expected
            and [aware(value) for value in actual]
            == [aware(value) for value in expected]
        )
    except Exception as exc:
        actual = {"exception": type(exc).__name__, "message": str(exc)}
        matches = False
    return actual, expected, matches


def main():
    deadline = time.monotonic() + 175
    base = dict(
        year=2025, month=1, day=1,
        hour=0, minute=0, second=0,
        offset_seconds=0, count=1
    )

    # Independently verify the daily reference against ordinary construction.
    sanity_cases = [
        dict(base, count=3),
        dict(base, month=2, day=28, hour=12,
             offset_seconds=19800, count=5)
    ]
    sanity_failed = False
    for number, case in enumerate(sanity_cases, 1):
        expected = reference(case)
        actual = list(rrule(
            DAILY, dtstart=make_start(case), count=case["count"]
        ))
        agrees = (
            actual == expected
            and all(aware(value) for value in actual)
        )
        print("SANITY", number, "agrees =", agrees,
              "actual =", repr(actual), "reference =", repr(expected))
        sanity_failed |= not agrees
    if sanity_failed:
        print("SANITY FAILED")
        return

    edges = [
        base,
        dict(base, count=5),
        dict(base, offset_seconds=19800),
        dict(base, offset_seconds=-43200, count=2),
        dict(base, year=2024, month=2, day=28, count=5),
        dict(base, year=2025, month=12, day=31,
             hour=23, minute=59, second=59, count=5),
        dict(base, offset_seconds=86340, count=2),
        dict(base, offset_seconds=-86340, count=2),
    ]
    rng = random.Random(20250101)
    tested = 0

    while time.monotonic() < deadline:
        if tested < len(edges):
            case = edges[tested]
        else:
            case = dict(
                year=rng.randint(1970, 2090),
                month=rng.randint(1, 12),
                day=rng.randint(1, 28),
                hour=rng.randrange(24),
                minute=rng.randrange(60),
                second=rng.randrange(60),
                offset_seconds=rng.randint(-1439, 1439) * 60,
                count=rng.randint(1, 5)
            )

        actual, expected, matches = check(case)
        tested += 1
        if not matches:
            again, expected_again, matches_again = check(case)
            if not matches_again and repr(again) == repr(actual):
                print("COUNTEREXAMPLE:")
                print(repr(case))
                print("actual:", repr(again))
                print("expected:", repr(expected_again))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()