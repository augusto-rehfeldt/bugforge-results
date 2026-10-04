import datetime as dt
import random
import time
from dateutil.rrule import rrulestr


def reference(dates):
    return [dt.datetime(y, m, d) for y, m, d in sorted(dates)]


def encode(dates, explicit=True):
    prefix = "RDATE;VALUE=DATE:" if explicit else "RDATE:"
    return prefix + ",".join(f"{y:04d}{m:02d}{d:02d}" for y, m, d in dates)


def evaluate(text):
    try:
        return ("result", list(rrulestr(text)))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def main():
    deadline = time.monotonic() + 175

    # Ordinary RDATE inputs exercise the same independent reference.
    sanity_cases = [
        [(2024, 1, 1)],
        [(2024, 3, 1), (2024, 2, 29), (2023, 12, 31)],
    ]
    for i, dates in enumerate(sanity_cases, 1):
        actual = evaluate(encode(dates, explicit=False))
        expected = ("result", reference(dates))
        print(f"SANITY {i}: actual={actual!r}, expected={expected!r}")
        if actual != expected:
            print("SANITY FAILED")
            return

    tested = 0

    def check(dates):
        nonlocal tested
        text = encode(dates)
        expected = ("result", reference(dates))
        actual = evaluate(text)
        tested += 1
        if actual != expected:
            repeated = evaluate(text)
            if repeated == actual:
                print("COUNTEREXAMPLE:", repr(text))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return True
        return False

    edge_cases = [
        [(2024, 3, 1), (2024, 2, 29), (2023, 12, 31)],
        [(2024, 1, 1)],
        [(1000, 1, 1)],
        [(9999, 12, 31)],
        [(9999, 12, 31), (1000, 1, 1), (2000, 2, 29)],
        [(2400, 2, 29), (2000, 2, 29), (1600, 2, 29)],
        [(1900, 3, 1), (1900, 2, 28), (2000, 2, 29)],
    ]
    for dates in edge_cases:
        if check(dates):
            return

    rng = random.Random(5545)
    low = dt.date(1000, 1, 1).toordinal()
    high = dt.date(9999, 12, 31).toordinal()

    while time.monotonic() < deadline:
        ordinals = rng.sample(range(low, high + 1), rng.randint(1, 64))
        dates = []
        for ordinal in ordinals:
            date = dt.date.fromordinal(ordinal)
            dates.append((date.year, date.month, date.day))
        if check(dates):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()