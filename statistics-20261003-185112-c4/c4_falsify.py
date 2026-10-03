import math
import random
import statistics
import time
from fractions import Fraction

def reference_covariance(x, y):
    n = len(x)
    fx = [Fraction(v) for v in x]
    fy = [Fraction(v) for v in y]
    mx = sum(fx) / n
    my = sum(fy) / n
    return float(sum((u - mx) * (v - my) for u, v in zip(fx, fy)) / (n - 1))

def evaluate(x, y, expected):
    try:
        actual = statistics.covariance(x, y)
        failed = not (
            math.isfinite(actual)
            and math.isclose(actual, expected, rel_tol=1e-14, abs_tol=0.0)
        )
        return failed, repr(actual)
    except Exception as exc:
        return True, f"{type(exc).__name__}({str(exc)!r})"

def main():
    start = time.monotonic()
    sanity_ok = True
    for x, y in [
        ([1.0, 2.0, 3.0], [2.0, 4.0, 6.0]),
        ([-3.0, -3.0, 3.0, 3.0], [-3.0, -3.0, 3.0, 3.0]),
    ]:
        expected = reference_covariance(x, y)
        failed, actual = evaluate(x, y, expected)
        print(f"SANITY: input={repr((x, y))} actual={actual} expected={expected!r}")
        sanity_ok = sanity_ok and not failed
    if not sanity_ok:
        print("SANITY FAILED")
        return

    low, high = 7e153, 1e154
    edges = [
        low, high,
        math.nextafter(low, high),
        math.nextafter(high, low),
        8e153, 9e153,
        (low + high) / 2,
    ]
    rng = random.Random(20260221)
    tested = 0

    def candidates():
        yield from edges
        while True:
            yield rng.uniform(low, high)

    for a in candidates():
        if time.monotonic() - start >= 175.0:
            break
        if not low <= a <= high:
            continue
        x = [-a, -a, a, a]
        expected = reference_covariance(x, x)
        tested += 1
        failed, actual = evaluate(x, x, expected)
        if failed:
            failed_again, actual_again = evaluate(x, x, expected)
            if failed_again:
                print("COUNTEREXAMPLE:", repr((x, x)))
                print("actual:", actual_again)
                print("expected:", repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)

if __name__ == "__main__":
    main()