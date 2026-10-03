import math
import random

case = dict(alpha=0.001, beta=0.002, seed_start=0, seed_stop_exclusive=200000)
a, b = case["alpha"], case["beta"]
if not all(math.isfinite(x) and x > 0 for x in (a, b)):
    print("REFUTATION REJECTED:", "parameters must be finite and positive")
else:
    n = case["seed_stop_exclusive"] - case["seed_start"]
    actual = math.fsum(random.Random(s).betavariate(a, b)
                       for s in range(case["seed_start"], case["seed_stop_exclusive"])) / n
    expected = a / (a + b)
    tolerance = 6 * math.sqrt(a * b / ((a + b)**2 * (a + b + 1) * n))
    if abs(actual - expected) > tolerance:
        print("REFUTATION CONFIRMED:", case, "actual =", actual, "expected =", expected)
    else:
        print("REFUTATION REJECTED:", "mean agrees within six standard errors")