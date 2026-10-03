*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `random`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Beta sampling is biased by underflow of small shape parameters

Target: `random.Random.betavariate`

Property: For finite positive alpha=0.001 and beta=0.002, betavariate(alpha, beta) must produce samples with expected value alpha/(alpha+beta)=1/3. A large deterministic sample across integer seeds should agree with that mean within statistical sampling error.

### Draft issue: random.betavariate produces biased samples for small positive shape parameters

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

**Documented behaviour:** Random.betavariate docstring: "The mean (expected value) and variance of the random variable are: E[X] = alpha / (alpha + beta)"; its parameter conditions are "alpha > 0 and beta > 0."

**Expected:** A sample mean near 0.3333333333333333, within the six-standard-error tolerance of approximately 0.006315.

**Actual:** The 200,000-seed sample mean is 0.2972743605039545, approximately 0.036059 below the expected mean.

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: {'alpha': 0.001, 'beta': 0.002, 'seed_start': 0, 'seed_stop_exclusive': 200000} actual = 0.2972743605039545 expected = 0.3333333333333333
```

Judge: BUG (medium) -- Both parameters are finite and positive, and the expected mean and variance-based tolerance are correct. The observed deviation is about 34 standard errors, far beyond ordinary sampling variation. For these small shape parameters, gamma samples can underflow to zero; betavariate's zero handling then introduces substantial downward bias rather than merely rounding individual results. No listed issue or upstream change addresses this behavior.

