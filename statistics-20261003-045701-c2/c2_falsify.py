import math
import random
import statistics
import time
from fractions import Fraction


def reference(x, y):
    """Compute ordinary least squares using exact rational arithmetic."""
    xs = [Fraction.from_float(v) for v in x]
    ys = [Fraction.from_float(v) for v in y]
    n = len(xs)
    xmean = sum(xs) / n
    ymean = sum(ys) / n
    covariance = sum((u - xmean) * (v - ymean)
                     for u, v in zip(xs, ys))
    variance = sum((u - xmean) ** 2 for u in xs)
    slope = covariance / variance
    intercept = ymean - slope * xmean
    return float(slope), float(intercept)


def actual(x, y):
    try:
        return tuple(statistics.linear_regression(x, y))
    except Exception as exc:
        return {"exception": type(exc).__name__, "message": str(exc)}


def main():
    deadline = time.monotonic() + 175.0

    for x, y in [
        ([0.0, 1.0], [0.0, 1.0]),
        ([0.0, 1.0, 2.0], [1.0, 3.0, 5.0]),
    ]:
        expected = reference(x, y)
        observed = actual(x, y)
        print("SANITY:", repr((x, y)), "actual:", repr(observed),
              "expected:", repr(expected))
        if observed != expected:
            print("SANITY FAILED")
            return

    tested = 0

    def check(a):
        nonlocal tested
        x = [0.0, a]
        y = [0.0, a]
        expected = reference(x, y)
        observed = actual(x, y)
        tested += 1
        if observed != expected:
            repeated = actual(x, y)
            if repeated == observed:
                print("COUNTEREXAMPLE:",
                      repr({"x": x, "y": y, "proportional": False}),
                      "actual:", repr(repeated),
                      "expected:", repr(expected))
                return True
        return False

    edges = [
        1e-200,
        1e-170,
        math.nextafter(1e-200, math.inf),
        math.nextafter(1e-170, 0.0),
    ]
    edges.extend(10.0 ** (-200.0 + i / 10.0) for i in range(301))

    for a in edges:
        if time.monotonic() >= deadline:
            break
        if 1e-200 <= a <= 1e-170 and check(a):
            return

    rng = random.Random(20250308)
    while time.monotonic() < deadline:
        a = 10.0 ** rng.uniform(-200.0, -170.0)
        if 1e-200 <= a <= 1e-170 and check(a):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()