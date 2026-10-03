import random
import statistics
import time
from fractions import Fraction


def reference(data, weights):
    numerator = sum(
        (Fraction.from_float(x) * Fraction.from_float(w)
         for x, w in zip(data, weights)),
        Fraction(0),
    )
    denominator = sum(
        (Fraction.from_float(w) for w in weights), Fraction(0)
    )
    return float(numerator / denominator)


def main():
    deadline = time.monotonic() + 175.0
    sanity_ok = True
    for data, weights in [
        ([1.0, 3.0], [1.0, 1.0]),
        ([2.0, 8.0], [2.0, 1.0]),
    ]:
        expected = reference(data, weights)
        actual = statistics.fmean(data, weights=weights)
        print("SANITY:", repr((data, weights)), actual, expected)
        sanity_ok = sanity_ok and actual == expected

    if not sanity_ok:
        print("SANITY FAILED")
        return

    tested = 0

    def check(k, j):
        nonlocal tested
        data = [2.0 ** (-k)]
        weights = [2.0 ** (-j)]
        expected = reference(data, weights)
        tested += 1

        def run():
            try:
                return statistics.fmean(data, weights=weights), False
            except Exception as exc:
                return (type(exc).__name__, str(exc)), True

        actual, raised = run()
        if raised or actual != expected:
            repeated, repeated_raised = run()
            if repeated_raised == raised and repeated == actual:
                print("COUNTEREXAMPLE:")
                print(repr({"k": k, "j": j, "data": data, "weights": weights}))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return True
        return False

    edges = [
        (600, 600),
        (600, 900),
        (900, 600),
        (900, 900),
        (750, 750),
        (601, 600),
        (600, 601),
    ]
    for k, j in edges:
        if time.monotonic() >= deadline:
            break
        if check(k, j):
            return

    rng = random.Random(20250308)
    while time.monotonic() < deadline:
        if check(rng.randint(600, 900), rng.randint(600, 900)):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()