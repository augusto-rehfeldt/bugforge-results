*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `random`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Binomial sampling collapses to zero when tiny p rounds 1-p to one

Target: `random.Random.binomialvariate`

Property: For n = 2**60 and p = 2**-60, binomialvariate(n, p) must sample a distribution with expected value n*p = 1, rather than return zero for every seed. Check computationally by sampling across integer seeds and comparing the empirical mean with 1.

### Draft issue: random.binomialvariate returns only zero for large n and tiny p with n*p = 1

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

**Documented behaviour:** Random.binomialvariate docstring: "The mean (expected value) and variance of the random variable are: E[X] = n * p"; it also defines the result as the number of successes in n independent trials with success probability p.

**Expected:** A binomial distribution with mean 1 and zero-success probability approximately 0.367879; the empirical mean should be near 1.

**Actual:** All 4096 integer-seeded samples returned zero; empirical mean 0.0.

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: {'n': 1152921504606846976, 'p': 8.673617379884035e-19, 'integer_seeds': (0, 4096)} actual = 0.0 expected = 1.0
```

Judge: BUG (medium) -- The inputs are valid and n*p is exactly 1. All 4096 samples being zero is a severe distributional failure, not ordinary sampling variation (the mean differs by 64 standard errors). For this p, floating-point subtraction rounds 1-p to 1, making the inverse sampler's initial zero-success probability (1-p)**n equal to 1 instead of approximately exp(-1). This numerical failure is not a documented restriction on valid inputs. The listed PR discusses other numerical risks but does not report or fix this all-zero case; the upstream diff does not address it.

