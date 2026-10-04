import math
import random
import statistics
import time
from fractions import Fraction


def reference(x, y):
    # Compute centered sums exactly from the floats' binary values.
    fx = [Fraction(v) for v in x]
    fy = [Fraction(v) for v in y]
    n = len(fx)
    mx, my = sum(fx) / n, sum(fy) / n
    dx = [v - mx for v in fx]
    dy = [v - my for v in fy]
    covariance = sum(u * v for u, v in zip(dx, dy))
    vx = sum(u * u for u in dx)
    vy = sum(v * v for v in dy)
    if not vx or not vy:
        raise ValueError("Constant input")
    # Avoid converting tiny variances to floats before taking their ratio.
    magnitude = math.sqrt(float(covariance * covariance / (vx * vy)))
    return -magnitude if covariance < 0 else magnitude


def observe(x, y):
    try:
        return ("result", statistics.correlation(x, y))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def agrees(actual, expected):
    return (
        actual[0] == "result"
        and math.isfinite(actual[1])
        and math.isclose(actual[1], expected, rel_tol=1e-12, abs_tol=1e-12)
    )


def main():
    for x, y in [
        ([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]),
        ([1.0, 2.0, 3.0], [3.0, 2.0, 1.0]),
    ]:
        expected = reference(x, y)
        actual = observe(x, y)
        print("SANITY:", repr((x, y)), "actual =", repr(actual),
              "expected =", repr(expected))
        if not agrees(actual, expected):
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 175.0
    rng = random.Random(20260719)
    edges = [
        1e-200,
        math.nextafter(1e-200, math.inf),
        1e-190,
        1e-180,
        math.nextafter(1e-170, 0.0),
        1e-170,
    ]
    tested = 0

    def check(a):
        nonlocal tested
        x = [-a, a]
        expected = reference(x, x)
        actual = observe(x, x)
        tested += 1
        if not agrees(actual, expected):
            repeated = observe(x, x)
            if not agrees(repeated, expected):
                print("COUNTEREXAMPLE:", repr((x, x)),
                      "actual =", repr(repeated),
                      "expected =", repr(expected))
                return True
        return False

    for a in edges:
        if check(a):
            return

    while time.monotonic() < deadline:
        a = 10.0 ** rng.uniform(-200.0, -170.0)
        if math.isfinite(a) and 1e-200 <= a <= 1e-170:
            if check(a):
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()