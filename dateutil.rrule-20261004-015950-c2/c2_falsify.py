from datetime import datetime, timedelta
from math import gcd
import random
import time

from dateutil.rrule import rrule, HOURLY


def reference(start, interval, hours, count):
    """Advance on the hourly interval grid, retaining allowed hours."""
    result = []
    current = start.replace(microsecond=0)
    allowed = set(hours)
    step = timedelta(hours=interval)
    while len(result) < count:
        if current.hour in allowed:
            result.append(current)
        current += step
    return result


def encode(values):
    return [value.isoformat() for value in values]


def evaluate(case):
    start = datetime(*case["dtstart"])
    original = rrule(
        HOURLY,
        dtstart=start,
        interval=case["i"],
        byhour=case["hours"],
        count=case["count"],
    )
    actual = list(original.replace(interval=case["j"]))
    expected = reference(start, case["j"], case["hours"], case["count"])
    return actual, expected


def main():
    deadline = time.monotonic() + 170

    sanity_cases = [
        (datetime(2024, 1, 1), 1, (0, 1, 2), 5),
        (datetime(2024, 2, 28, 22, 17, 9), 3, (1, 7, 22), 6),
    ]
    for number, (start, interval, hours, count) in enumerate(sanity_cases, 1):
        expected = reference(start, interval, hours, count)
        actual = list(rrule(
            HOURLY, dtstart=start, interval=interval,
            byhour=hours, count=count,
        ))
        print("SANITY", number, "actual =", encode(actual),
              "reference =", encode(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    hand_picked = [
        dict(dtstart=(2024, 1, 1), i=2, j=1, hours=(0, 1), count=3),
        dict(dtstart=(2024, 1, 1, 23), i=2, j=1,
             hours=(0, 23), count=4),
        dict(dtstart=(2024, 2, 28, 22, 17, 9), i=6, j=1,
             hours=(0, 4, 22), count=5),
        dict(dtstart=(2024, 12, 31), i=24, j=1,
             hours=(0, 23), count=3),
    ]

    rng = random.Random(20240101)
    tested = 0

    def check(case):
        nonlocal tested
        actual, expected = evaluate(case)
        tested += 1
        if actual != expected:
            repeated_actual, repeated_expected = evaluate(case)
            if (actual, expected) == (repeated_actual, repeated_expected):
                print("COUNTEREXAMPLE:", repr(case))
                print("actual:", repr(encode(actual)))
                print("expected:", repr(encode(expected)))
                return True
        return False

    for case in hand_picked:
        if time.monotonic() >= deadline:
            break
        if check(case):
            return

    while time.monotonic() < deadline and tested < 100000:
        interval = rng.choice((2, 3, 4, 6, 8, 12, 24, 48))
        hour = rng.randrange(24)
        divisor = gcd(interval, 24)
        reachable = [h for h in range(24) if (h - hour) % divisor == 0]
        unreachable = [h for h in range(24) if (h - hour) % divisor != 0]
        hours = {rng.choice(reachable), rng.choice(unreachable)}
        hours.update(rng.sample(range(24), rng.randrange(25)))
        case = dict(
            dtstart=(2024, rng.randrange(1, 13), rng.randrange(1, 29),
                     hour, rng.randrange(60), rng.randrange(60)),
            i=interval,
            j=1,
            hours=tuple(sorted(hours)),
            count=rng.randrange(1, 9),
        )
        if check(case):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()