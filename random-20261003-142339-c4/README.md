*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `random`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Binomial sampling collapses to zero when a positive probability rounds away

Target: `random.binomialvariate`

Property: For integer n >= 0 and finite p in [0, 1], binomialvariate(n, p) must follow the documented binomial distribution, whose expected value is n*p. In particular, for n=2**55 and p=2**-55, the expected value must be 1, rather than the function returning 0 for every generator state.

### Draft issue: random.binomialvariate returns deterministic zero for small positive p with n*p=1

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

**Documented behaviour:** Random.binomialvariate docstring: "The mean (expected value) and variance of the random variable are: E[X] = n * p"; it also specifies "P(X == k) = math.comb(n, k) * p ** k * (1 - p) ** (n - k)".

**Expected:** A nondegenerate binomial sample with mean 1; the probability of zero is approximately exp(-1), not 1.

**Actual:** Returns 0 without consuming randomness for n=2**55 and p=2**-55.

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: (36028797018963968, 2.7755575615628914e-17) actual = 0 expected mean = 1 (no randomness consumed)
```

Judge: BUG (medium) -- The inputs are valid and exactly representable, and n*p is exactly 1. A single sample need not equal its mean, but returning 0 without consuming randomness exposes a deterministic result inconsistent with the promised binomial distribution. Here 1-p rounds to 1.0; treating that numerical cancellation as a genuinely zero success probability is an implementation defect, not a documented input limitation. The upstream changes shown do not address this case, and no duplicate is listed.

