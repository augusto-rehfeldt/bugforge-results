import math
import random
import statistics
import time
from fractions import Fraction


def reference(x, y):
    n = len(x)
    if n != len(y) or n < 2:
        raise ValueError("Invalid lengths")
    x = [Fraction(v) for v in x]
    y = [Fraction(v) for v in y]
    mx = sum(x) / n
    my = sum(y) / n
    xx = sum((v - mx) ** 2 for v in x)
    yy = sum((v - my) ** 2 for v in y)
    xy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    if not xx or not yy:
        raise ValueError("Constant input")
    magnitude = math.sqrt(float(xy * xy / (xx * yy)))
    return -magnitude if xy < 0 else magnitude


def evaluate(x, expected):
    try:
        actual = statistics.correlation(x, x)
        failed = not math.isclose(
            actual, expected, rel_tol=0.0, abs_tol=1e-14
        )
        return failed, repr(actual)
    except Exception as exc:
        return True, repr(f"{type(exc).__name__}: {exc}")


def main():
    for x, y in [
        ([1, 2, 3], [1, 2, 3]),
        ([1, 2, 3], [3, 2, 1]),
    ]:
        expected = reference(x, y)
        try:
            actual = statistics.correlation(x, y)
            agrees = math.isclose(
                actual, expected, rel_tol=0.0, abs_tol=1e-14
            )
        except Exception as exc:
            actual = f"{type(exc).__name__}: {exc}"
            agrees = False
        print("SANITY:", repr((x, y)), repr(actual), repr(expected))
        if not agrees:
            print("SANITY FAILED")
            return

    rng = random.Random(20250308)
    deadline = time.monotonic() + 175
    tested = 0
    edges = [54, 55, 56, 100, 99, 64, 80]

    for index in range(100000):
        if time.monotonic() >= deadline:
            break
        k = edges[index] if index < len(edges) else rng.randint(54, 100)
        x = [2**k, 2**k + 1]
        expected = reference(x, x)
        failed, actual = evaluate(x, expected)
        tested += 1
        if failed:
            failed_again, actual_again = evaluate(x, expected)
            if failed_again:
                print(
                    "COUNTEREXAMPLE:",
                    repr(x),
                    "actual=" + actual_again,
                    "expected=" + repr(expected),
                )
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()