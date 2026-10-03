import math
import random
import statistics
import time
from fractions import Fraction


def reference(a):
    exact = Fraction.from_float(a)
    side = float(exact * Fraction(3, 2))
    return [-side, 0.0, side]


def agrees(actual, expected):
    return (
        len(actual) == 3
        and all(math.isfinite(x) for x in actual)
        and math.isclose(actual[0], expected[0], rel_tol=1e-14, abs_tol=0.0)
        and actual[1] == expected[1]
        and math.isclose(actual[2], expected[2], rel_tol=1e-14, abs_tol=0.0)
    )


def evaluate(a):
    try:
        return statistics.quantiles([-a, a], n=4, method="exclusive")
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def passes(actual, expected):
    return isinstance(actual, list) and agrees(actual, expected)


def main():
    for a in (1.0, 10.0):
        expected = reference(a)
        actual = evaluate(a)
        print("SANITY:", repr([-a, a]), "actual:", repr(actual),
              "expected:", repr(expected))
        if not passes(actual, expected):
            print("SANITY FAILED")
            return

    low, high = 6e307, 1e308
    edges = [
        low,
        high,
        math.nextafter(low, high),
        math.nextafter(high, low),
        low + (high - low) / 2,
    ]
    rng = random.Random(20250308)
    deadline = time.monotonic() + 175.0
    tested = 0

    def check(a):
        nonlocal tested
        expected = reference(a)
        actual = evaluate(a)
        tested += 1
        if not passes(actual, expected):
            repeated = evaluate(a)
            if not passes(repeated, expected):
                print("COUNTEREXAMPLE:", repr([-a, a]),
                      "actual:", repr(repeated), "expected:", repr(expected))
                return True
        return False

    for a in edges:
        if check(a):
            return

    while time.monotonic() < deadline:
        a = rng.uniform(low, high)
        if check(a):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()