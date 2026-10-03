import datetime
import random
import time


def reference(year, month, day):
    # All generated inputs are Python integers, with month=day=1.
    if not 1 <= year <= 9999:
        return ("exception", "ValueError")
    return ("date", (year, month, day))


def actual(year, month, day):
    try:
        result = datetime.date(year, month, day)
        return ("date", (result.year, result.month, result.day))
    except Exception as exc:
        return ("exception", type(exc).__name__)


def main():
    deadline = time.monotonic() + 175.0

    for args in [(1, 1, 1), (2024, 1, 1)]:
        expected = reference(*args)
        observed = actual(*args)
        print("SANITY:", repr(args), repr(observed), repr(expected))
        if observed != expected:
            print("SANITY FAILED")
            return

    tested = 0

    def check(year):
        nonlocal tested
        args = (year, 1, 1)
        expected = reference(*args)
        observed = actual(*args)
        tested += 1
        if observed != expected:
            repeated = actual(*args)
            if repeated != expected:
                print(
                    "COUNTEREXAMPLE:",
                    repr(args),
                    "actual=" + repr(repeated),
                    "expected=" + repr(expected),
                )
                return True
        return False

    edges = [
        -(2**100),
        -(2**31) - 1,
        0,
        10000,
        2**31,
        2**100,
        -(2**31),
        2**31 - 1,
        -(2**63),
        2**63 - 1,
        2**63,
        -1,
        10001,
    ]

    for year in edges:
        if time.monotonic() >= deadline:
            break
        if check(year):
            return

    rng = random.Random(20240517)
    while time.monotonic() < deadline:
        bits = rng.randint(1, 4096)
        magnitude = rng.getrandbits(bits)
        year = -magnitude if rng.getrandbits(1) else 10000 + magnitude
        if check(year):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()