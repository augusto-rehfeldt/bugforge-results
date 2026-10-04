import math
import random
import sys
import time
from fractions import Fraction

from more_itertools import running_mean


def reference(pair):
    a, b = pair
    return float((Fraction(a) + Fraction(b)) / 2)


def actual(pair):
    try:
        values = iter(running_mean(pair))
        next(values)
        return next(values)
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def agrees(value, expected):
    return (
        isinstance(value, (int, float))
        and math.isfinite(value)
        and math.isclose(
            value,
            expected,
            rel_tol=1e-14,
            abs_tol=4 * math.ulp(expected),
        )
    )


def main():
    deadline = time.monotonic() + 175.0

    for pair in ([2.0, 4.0], [-3.0, 7.0]):
        expected = reference(pair)
        observed = actual(pair)
        print("SANITY:", repr(pair), "actual:", repr(observed),
              "expected:", repr(expected))
        if not agrees(observed, expected):
            print("SANITY FAILED")
            return

    tested = 0

    def check(pair):
        nonlocal tested
        expected = reference(pair)
        observed = actual(pair)
        tested += 1
        if not agrees(observed, expected):
            repeated = actual(pair)
            if not agrees(repeated, expected):
                print("COUNTEREXAMPLE:", repr(pair),
                      "actual:", repr(repeated),
                      "expected:", repr(expected))
                return True
        return False

    maximum = sys.float_info.max
    below_maximum = math.nextafter(maximum, 0.0)
    edges = [
        [1e308, -1e308],
        [-1e308, 1e308],
        [1e308, 1e308],
        [-1e308, -1e308],
        [maximum, maximum],
        [-maximum, -maximum],
        [maximum, -maximum],
        [-maximum, maximum],
        [maximum, -below_maximum],
        [-maximum, below_maximum],
        [maximum, below_maximum],
        [-maximum, -below_maximum],
    ]

    for pair in edges:
        if check(pair):
            return

    rng = random.Random(20260717)
    while time.monotonic() < deadline:
        a = math.ldexp(rng.uniform(0.5, 1.0), rng.choice((1023, 1024)))
        b = math.ldexp(rng.uniform(0.5, 1.0), rng.choice((1023, 1024)))
        if not (math.isfinite(a) and math.isfinite(b)):
            continue
        if rng.getrandbits(1):
            a = -a
        if rng.getrandbits(1):
            b = -b
        if check([a, b]):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()