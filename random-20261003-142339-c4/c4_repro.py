import math
import random
from fractions import Fraction

n, p = 2**55, 2**-55
if not (isinstance(n, int) and n >= 0 and math.isfinite(p) and 0 <= p <= 1):
    print("REFUTATION REJECTED:", "invalid input")
else:
    class TrackedRandom(random.Random):
        calls = 0

        def random(self):
            self.calls += 1
            return super().random()

        def getrandbits(self, k):
            self.calls += 1
            return super().getrandbits(k)

    rng = TrackedRandom(0)
    expected = n * Fraction(p)
    actual = rng.binomialvariate(n, p)
    if actual != expected and rng.calls == 0:
        print("REFUTATION CONFIRMED:", (n, p), "actual =", actual,
              "expected mean =", expected, "(no randomness consumed)")
    else:
        print("REFUTATION REJECTED:", "deterministic wrong result not reproduced",
              (n, p), "actual =", actual, "expected mean =", expected)