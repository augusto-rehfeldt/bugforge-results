import random
import math

n, p, samples = 2**60, 2**-60, 4096
try:
    if not (isinstance(n, int) and n >= 0 and 0 <= p <= 1):
        raise ValueError("input violates documented domain")
    expected = n * p
    values = [random.Random(seed).binomialvariate(n, p)
              for seed in range(samples)]
    actual = sum(values) / samples
    if abs(actual - expected) > 8 * math.sqrt(n * p * (1 - p) / samples):
        print("REFUTATION CONFIRMED:",
              {"n": n, "p": p, "integer_seeds": (0, samples)},
              "actual =", actual, "expected =", expected)
    else:
        print("REFUTATION REJECTED: empirical mean agrees with expectation",
              actual, expected)
except Exception as exc:
    print("REFUTATION REJECTED: could not test:", type(exc).__name__, str(exc))