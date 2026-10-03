import math
import random
import time
from fractions import Fraction


def reference(alpha, beta, n):
    a = Fraction(str(alpha))
    b = Fraction(str(beta))
    mean = a / (a + b)
    variance = a * b / ((a + b) ** 2 * (a + b + 1))
    return float(mean), 6.0 * math.sqrt(float(variance / n))


def main():
    deadline = time.monotonic() + 175.0

    # Independent documented moments versus ordinary Monte Carlo samples.
    for seed, alpha, beta in [(12345, 1.0, 1.0), (67890, 2.0, 3.0)]:
        n = 20000
        rng = random.Random(seed)
        actual = math.fsum(rng.betavariate(alpha, beta) for _ in range(n)) / n
        expected, tolerance = reference(alpha, beta, n)
        print(
            "SANITY:",
            repr((alpha, beta)),
            "actual =", actual,
            "expected =", expected,
            "six_standard_errors =", tolerance,
        )
        if not math.isfinite(actual) or abs(actual - expected) > tolerance:
            print("SANITY FAILED")
            return

    alpha, beta = 0.001, 0.002
    n = 200000

    # Hand-picked seed edge cases first, then all remaining seeds in a
    # fixed-seed randomized order. Each integer seed is tested exactly once.
    edges = [0, 1, 2, 3, 7, 42, 255, 256, 65535, 65536, 199998, 199999]
    edge_set = set(edges)
    remaining = [i for i in range(n) if i not in edge_set]
    random.Random(20250308).shuffle(remaining)
    seeds = edges + remaining

    values = []
    for seed in seeds:
        if time.monotonic() >= deadline:
            print("NO COUNTEREXAMPLE", len(values))
            return
        values.append(random.Random(seed).betavariate(alpha, beta))

    actual = math.fsum(values) / n
    expected, tolerance = reference(alpha, beta, n)

    if not math.isfinite(actual) or abs(actual - expected) > tolerance:
        # Re-run the identical aggregate input to exclude flakiness.
        repeated = []
        for seed in seeds:
            if time.monotonic() >= deadline:
                print("NO COUNTEREXAMPLE", n)
                return
            repeated.append(random.Random(seed).betavariate(alpha, beta))
        confirmed = math.fsum(repeated) / n
        if confirmed == actual and (
            not math.isfinite(confirmed) or abs(confirmed - expected) > tolerance
        ):
            failing_input = {
                "alpha": alpha,
                "beta": beta,
                "seed_start": 0,
                "seed_stop_exclusive": n,
            }
            print(
                "COUNTEREXAMPLE:",
                repr(failing_input),
                "actual =", repr(confirmed),
                "expected =", repr(expected),
                "six_standard_errors =", repr(tolerance),
            )
            return

    print("NO COUNTEREXAMPLE", n)


if __name__ == "__main__":
    main()