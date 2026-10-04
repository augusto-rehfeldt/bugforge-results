import math
import random
import statistics
import sys
import time
from fractions import Fraction


def reference(values):
    ordered = sorted(Fraction.from_float(v) for v in values)
    n = len(ordered)
    if n % 2:
        return float(ordered[n // 2])
    return float((ordered[n // 2 - 1] + ordered[n // 2]) / 2)


def actual(values):
    try:
        return statistics.median(values)
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def main():
    deadline = time.monotonic() + 175.0

    for values in ([1.0, 3.0], [2.5, 2.5]):
        expected = reference(values)
        result = actual(values)
        print("SANITY:", repr(values), "actual:", repr(result),
              "expected:", repr(expected))
        if result != expected:
            print("SANITY FAILED")
            return

    maximum = sys.float_info.max
    halfway = maximum / 2.0
    edges = [
        1e308,
        maximum,
        math.nextafter(maximum, 0.0),
        math.nextafter(halfway, math.inf),
        halfway,
        math.nextafter(halfway, 0.0),
        sys.float_info.min,
        math.nextafter(0.0, 1.0),
        1.0,
    ]
    rng = random.Random(20260601)
    tested = 0

    def check(x):
        nonlocal tested
        values = [x, x]
        expected = reference(values)
        result = actual(values)
        tested += 1
        if result != expected:
            repeated = actual(values)
            if repeated == result:
                print("COUNTEREXAMPLE:", repr(values),
                      "actual:", repr(result), "expected:", repr(expected))
                return True
        return False

    for x in edges:
        if check(x):
            return

    while time.monotonic() < deadline:
        if rng.randrange(4):
            # Positive finite IEEE-754 values in the highest exponent binade.
            significand = rng.randrange(1 << 52, 1 << 53)
            x = math.ldexp(float(significand), 971)
        else:
            significand = rng.randrange(1 << 52, 1 << 53)
            exponent = rng.randrange(-1074, 972)
            x = math.ldexp(float(significand), exponent)
        if math.isfinite(x) and x > 0.0 and check(x):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()