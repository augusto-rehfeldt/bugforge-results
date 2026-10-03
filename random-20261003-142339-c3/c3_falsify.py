import random
import time
from fractions import Fraction
from math import sqrt

DEADLINE = time.monotonic() + 175.0
SAMPLES = 4096
cases_tested = 0


def reference(n, p):
    # Exact moments from the sum of n independent Bernoulli trials.
    probability = Fraction.from_float(p)
    mean = n * probability
    variance = n * probability * (1 - probability)
    return mean, variance


def sample(n, p, seed_start, count):
    total = 0
    nonzero = 0
    for seed in range(seed_start, seed_start + count):
        if time.monotonic() >= DEADLINE:
            return None
        value = random.Random(seed).binomialvariate(n, p)
        total += value
        nonzero += value != 0
    return {
        "empirical_mean": total / count,
        "nonzero_samples": nonzero,
        "samples": count,
    }


def disagrees(actual, mean, variance, count):
    # A conservative statistical check, not a demand for exact sample equality.
    tolerance = max(0.25, 10 * sqrt(float(variance) / count))
    return abs(actual["empirical_mean"] - float(mean)) > tolerance


def main():
    global cases_tested

    sanity_failed = False
    for n, p in ((10, 0.5), (20, 0.25)):
        mean, variance = reference(n, p)
        actual = sample(n, p, 0, SAMPLES)
        agrees = (
            actual is not None
            and not disagrees(actual, mean, variance, SAMPLES)
        )
        print(
            "SANITY:",
            repr((n, p)),
            "actual =", repr(actual),
            "reference_mean =", float(mean),
            "agrees =", agrees,
        )
        sanity_failed |= not agrees

    if sanity_failed:
        print("SANITY FAILED")
        return

    chooser = random.Random(20250308)
    hand_picked = iter((60, 54, 55, 56, 64, 80, 100))

    while time.monotonic() < DEADLINE:
        try:
            m = next(hand_picked)
            seed_start = 0
        except StopIteration:
            m = chooser.randrange(54, 101)
            seed_start = chooser.randrange(0, 1_000_000)

        n = 2 ** m
        p = 2.0 ** (-m)
        mean, variance = reference(n, p)
        assert mean == 1 and 0 < p < 1

        actual = sample(n, p, seed_start, SAMPLES)
        if actual is None:
            break
        cases_tested += 1

        if disagrees(actual, mean, variance, SAMPLES):
            repeated = sample(n, p, seed_start, SAMPLES)
            if repeated is None:
                break
            if repeated == actual and disagrees(
                repeated, mean, variance, SAMPLES
            ):
                failing_input = {
                    "n": n,
                    "p": p,
                    "integer_seeds": (seed_start, seed_start + SAMPLES),
                }
                print(
                    "COUNTEREXAMPLE:",
                    repr(failing_input),
                    "actual =", repr(actual),
                    "expected =", repr({"mean": float(mean)}),
                )
                return

    print("NO COUNTEREXAMPLE", cases_tested)


if __name__ == "__main__":
    main()