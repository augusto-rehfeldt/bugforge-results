import random
import time as clock
from datetime import time, timedelta, timezone


def reference_offset(n):
    # Exact integer arithmetic; no ISO parser is used.
    days, remainder = divmod(n, 86_400_000_000)
    seconds, microseconds = divmod(remainder, 1_000_000)
    return timedelta(days=days, seconds=seconds, microseconds=microseconds)


def actual_offset(text):
    try:
        return time.fromisoformat(text).utcoffset()
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def main():
    deadline = clock.monotonic() + 180

    for n in (3_600_000_000, -19_800_000_000):
        expected = reference_offset(n)
        text = time(
            12, 34, 56, tzinfo=timezone(timedelta(microseconds=n))
        ).isoformat()
        actual = actual_offset(text)
        print("SANITY:", repr(text), "actual =", repr(actual),
              "expected =", repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    rng = random.Random(20250308)
    edges = (1, -1, 10, -10, 500000, -500000, 999999, -999999)
    tested = 0

    def inputs():
        yield from edges
        while True:
            magnitude = rng.randint(1, 999999)
            yield magnitude if rng.getrandbits(1) else -magnitude

    for n in inputs():
        if clock.monotonic() >= deadline:
            break
        expected = reference_offset(n)
        text = time(
            12, 34, 56, tzinfo=timezone(timedelta(microseconds=n))
        ).isoformat()
        actual = actual_offset(text)
        tested += 1
        if actual != expected:
            repeated = actual_offset(text)
            if repeated != expected:
                print("COUNTEREXAMPLE:", repr(text),
                      "actual =", repr(repeated),
                      "expected =", repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()