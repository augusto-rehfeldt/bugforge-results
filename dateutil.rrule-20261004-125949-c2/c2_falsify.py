import calendar
import random
import time
from datetime import datetime
from dateutil.rrule import rrule, DAILY, MONTHLY, TU


def reference(start, count, ordinal):
    """Nth Tuesday of each month, excluding occurrences before start."""
    result = []
    year, month = start.year, start.month
    while len(result) < count:
        last_day = calendar.monthrange(year, month)[1]
        if ordinal > 0:
            first_weekday = datetime(year, month, 1).weekday()
            day = 1 + (1 - first_weekday) % 7 + 7 * (ordinal - 1)
        else:
            last_weekday = datetime(year, month, last_day).weekday()
            day = last_day - (last_weekday - 1) % 7 + 7 * (ordinal + 1)

        if 1 <= day <= last_day:
            candidate = datetime(year, month, day)
            if candidate >= start:
                result.append(candidate)

        month += 1
        if month == 13:
            year += 1
            month = 1
    return result


def actual(start, count, ordinal):
    try:
        rule = rrule(
            DAILY, dtstart=start, count=count, byweekday=TU(ordinal)
        )
        return list(rule.replace(freq=MONTHLY))
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def main():
    deadline = time.monotonic() + 175

    sanity_cases = [
        (datetime(2024, 1, 1), 3, 1),
        (datetime(2023, 2, 1), 4, -4),
    ]
    for index, (start, count, ordinal) in enumerate(sanity_cases, 1):
        expected = reference(start, count, ordinal)
        observed = list(rrule(
            MONTHLY, dtstart=start, count=count, byweekday=TU(ordinal)
        ))
        print("SANITY", index, "module =", repr(observed),
              "reference =", repr(expected))
        if observed != expected:
            print("SANITY FAILED")
            return

    edge_cases = [
        (datetime(2024, 1, 1), 3, 1),
        (datetime(2024, 2, 1), 1, -1),
        (datetime(2023, 2, 1), 4, -4),
    ]
    for year, month in [(2024, 2), (2023, 2), (2000, 2), (1900, 2),
                        (2024, 12), (2024, 10)]:
        for ordinal in (-4, -3, -2, -1, 1, 2, 3, 4):
            edge_cases.append((datetime(year, month, 1), 5, ordinal))

    rng = random.Random(20240101)
    tested = 0
    iterator = iter(edge_cases)

    while time.monotonic() < deadline:
        try:
            start, count, ordinal = next(iterator)
        except StopIteration:
            start = datetime(rng.randint(1900, 2099), rng.randint(1, 12), 1)
            count = rng.randint(1, 8)
            ordinal = rng.choice((-4, -3, -2, -1, 1, 2, 3, 4))

        expected = reference(start, count, ordinal)
        observed = actual(start, count, ordinal)
        tested += 1

        if observed != expected:
            repeated = actual(start, count, ordinal)
            repeated_expected = reference(start, count, ordinal)
            if repeated == observed and repeated_expected == expected:
                input_literal = {
                    "dtstart": (start.year, start.month, start.day),
                    "count": count,
                    "byweekday": ("TU", ordinal),
                    "freq": "DAILY",
                    "replace": {"freq": "MONTHLY"},
                }
                print("COUNTEREXAMPLE:")
                print(repr(input_literal))
                print("actual =", repr(observed))
                print("expected =", repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()