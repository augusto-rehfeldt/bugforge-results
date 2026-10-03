import math
import random
import statistics
import time
from fractions import Fraction


def reference(data):
    total = Fraction(0)
    for value in data:
        numerator, denominator = value.as_integer_ratio()
        total += Fraction(numerator, denominator)
    return float(total / len(data))


def evaluate(data, expected):
    try:
        actual = statistics.fmean(data)
    except Exception as exc:
        return True, f"{type(exc).__name__}: {exc}"
    failed = not math.isclose(actual, expected, rel_tol=1e-15, abs_tol=0.0)
    return failed, actual


def main():
    for data in ([1.0, 2.0, 3.0], [0.25, 0.5, 0.75, 1.0]):
        expected = reference(data)
        failed, actual = evaluate(data, expected)
        print(f"SANITY: input={data!r}, actual={actual!r}, expected={expected!r}")
        if failed:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 170.0
    cases = 0

    def check(x, n):
        nonlocal cases
        data = [x] * n
        expected = reference(data)
        cases += 1
        failed, actual = evaluate(data, expected)
        if failed:
            failed_again, actual_again = evaluate(data, expected)
            if failed_again:
                print("COUNTEREXAMPLE:")
                print(repr(data))
                print(f"actual: {actual_again!r}")
                print(f"expected: {expected!r}")
                return True
        return False

    edges = (
        1e308,
        math.nextafter(1e308, math.inf),
        1.35e308,
        math.nextafter(1.7e308, -math.inf),
        1.7e308,
    )
    for x in edges:
        for n in range(2, 11):
            if time.monotonic() >= deadline:
                print(f"NO COUNTEREXAMPLE {cases}")
                return
            if check(x, n):
                return

    rng = random.Random(20260601)
    while time.monotonic() < deadline:
        x = rng.uniform(1e308, 1.7e308)
        if not (math.isfinite(x) and 1e308 <= x <= 1.7e308):
            continue
        for n in range(2, 11):
            if time.monotonic() >= deadline:
                print(f"NO COUNTEREXAMPLE {cases}")
                return
            if check(x, n):
                return

    print(f"NO COUNTEREXAMPLE {cases}")


if __name__ == "__main__":
    main()