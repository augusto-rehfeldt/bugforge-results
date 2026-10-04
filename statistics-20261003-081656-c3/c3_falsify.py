import math
import random
import statistics
import time
from fractions import Fraction


def reference(data):
    reciprocals = [1 / Fraction.from_float(x) for x in data]
    return float(Fraction(len(data), 1) / sum(reciprocals, Fraction(0)))


def actual(data):
    try:
        return statistics.harmonic_mean(data), False
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}", True


def main():
    deadline = time.monotonic() + 179.0
    cases_tested = 0

    for data in ([1.0, 1.0], [2.0, 2.0, 2.0]):
        expected = reference(data)
        result, raised = actual(data)
        print(f"SANITY: input={data!r}, actual={result!r}, expected={expected!r}")
        if raised or result != expected:
            print("SANITY FAILED")
            return

    def check(data):
        nonlocal cases_tested
        expected = reference(data)
        result, raised = actual(data)
        cases_tested += 1
        if raised or result != expected:
            repeated, repeated_raised = actual(data)
            if repeated_raised or repeated != expected:
                print(
                    f"COUNTEREXAMPLE: {data!r} "
                    f"actual={repeated!r} expected={expected!r}"
                )
                return True
        return False

    edges = [
        1e-320,
        float.fromhex("0x0.0000000000001p-1022"),
        math.ldexp(2.0, -1074),
        math.ldexp(float((1 << 52) - 1), -1074),
        float.fromhex("0x1p-1022"),
        0.5,
        1.0,
        2.0,
        10.0,
    ]

    for x in edges:
        for n in range(2, 11):
            if time.monotonic() >= deadline:
                print(f"NO COUNTEREXAMPLE {cases_tested}")
                return
            if check([x] * n):
                return

    rng = random.Random(20250308)
    controls = [0.125, 0.5, 1.0, 2.0, 8.0, 100.0]

    for _ in range(100000):
        if time.monotonic() >= deadline:
            break
        if rng.randrange(10) == 0:
            x = rng.choice(controls)
        else:
            significand = rng.randrange(1, 1 << 52)
            x = math.ldexp(float(significand), -1074)
        n = rng.randrange(2, 11)
        if check([x] * n):
            return

    print(f"NO COUNTEREXAMPLE {cases_tested}")


if __name__ == "__main__":
    main()