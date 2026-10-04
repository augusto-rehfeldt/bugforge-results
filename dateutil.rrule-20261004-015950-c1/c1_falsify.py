import random
import time
from datetime import datetime, timedelta, timezone
from dateutil.rrule import DAILY, rrule, rrulestr


def start_from(spec):
    return datetime(
        *spec["start"],
        tzinfo=timezone(timedelta(seconds=spec["offset_seconds"]))
    )


def describe(values):
    return [
        {
            "wall": value.replace(tzinfo=None).isoformat(),
            "aware": value.tzinfo is not None and value.utcoffset() is not None,
            "utc": (
                value.astimezone(timezone.utc).isoformat()
                if value.tzinfo is not None and value.utcoffset() is not None
                else None
            ),
        }
        for value in values
    ]


def reference(spec):
    # DAILY with no filters and finite COUNT advances one calendar day
    # per occurrence. Fixed-offset timezones have no DST transitions.
    start = start_from(spec)
    return describe([
        start + timedelta(days=i)
        for i in range(spec["count"])
    ])


def evaluate(spec):
    expected_values = reference(spec)
    expected = {
        "original": expected_values,
        "roundtrip": expected_values,
    }
    try:
        rule = rrule(
            DAILY, dtstart=start_from(spec), count=spec["count"]
        )
        original = describe(list(rule))
        text = str(rule)
        try:
            roundtrip = describe(list(rrulestr(text)))
        except Exception as exc:
            roundtrip = {
                "exception": type(exc).__name__,
                "message": str(exc),
            }
        actual = {"original": original, "roundtrip": roundtrip}
    except Exception as exc:
        actual = {
            "exception": type(exc).__name__,
            "message": str(exc),
        }
    return actual, expected


def main():
    deadline = time.monotonic() + 170

    sanity_cases = [
        {
            "start": (2024, 1, 10, 12, 0, 0),
            "offset_seconds": 0,
            "count": 3,
        },
        {
            "start": (2024, 2, 28, 23, 45, 0),
            "offset_seconds": 19800,
            "count": 4,
        },
    ]
    for index, spec in enumerate(sanity_cases, 1):
        expected = reference(spec)
        actual = describe(list(rrule(
            DAILY, dtstart=start_from(spec), count=spec["count"]
        )))
        agrees = actual == expected
        print("SANITY {}: {}".format(index, "OK" if agrees else "FAILED"))
        if not agrees:
            print("SANITY FAILED")
            return

    handpicked = [
        {"start": (2024, 1, 1, 0, 0, 0),
         "offset_seconds": 0, "count": 1},
        {"start": (2024, 2, 28, 23, 59, 59),
         "offset_seconds": 19800, "count": 5},
        {"start": (2023, 12, 31, 23, 30, 0),
         "offset_seconds": -14400, "count": 3},
    ]

    rng = random.Random(104729)
    tested = 0
    for index in range(100000):
        if time.monotonic() >= deadline:
            break
        if index < len(handpicked):
            spec = handpicked[index]
        else:
            spec = {
                "start": (
                    rng.randint(1990, 2050),
                    rng.randint(1, 12),
                    rng.randint(1, 28),
                    rng.randrange(24),
                    rng.randrange(60),
                    rng.randrange(60),
                ),
                "offset_seconds": rng.choice([0, 19800, -14400]),
                "count": rng.randint(1, 5),
            }
        tested += 1
        actual, expected = evaluate(spec)
        if actual != expected:
            repeated_actual, repeated_expected = evaluate(spec)
            if repeated_actual == actual and repeated_expected == expected:
                print("COUNTEREXAMPLE:")
                print(repr(spec))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()