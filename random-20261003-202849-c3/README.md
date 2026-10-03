*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `random`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Equal positive subnormal weights produce unequal selection probabilities

Target: `random.Random.choices`

Property: For population ['a', 'b'] and equal finite positive weights [w, w], each element must have selection probability 1/2. Test w = 2**-1074 against the equivalent relative weights [1.0, 1.0].

### Draft issue: random.choices produces strongly biased results for equal subnormal weights

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

**Documented behaviour:** Python random documentation, choices(): “If a weights sequence is specified, selections are made according to the relative weights.” Equal relative weights imply equal selection probabilities.

**Expected:** Equal selection probabilities, with approximately 50000 selections per element; scaling to [1.0, 1.0] should preserve the distribution.

**Actual:** 25146 selections of 'a' and 74854 of 'b', consistent with probabilities approximately 1/4 and 3/4.

**Reproducer:**

```python
import random, math
from fractions import Fraction

p, w, k, seed = ['a', 'b'], [2**-1074]*2, 100000, 0
data = dict(population=p, weights=w, k=k, seed=seed)
if not (len(p) == len(w) and all(math.isfinite(x) and x > 0 for x in w)
        and math.isfinite(sum(w)) and sum(w) > 0):
    print("REFUTATION REJECTED:", "invalid input", data)
else:
    q = [Fraction(x) for x in w]
    probabilities = [x / sum(q) for x in q]
    draws = random.Random(seed).choices(p, weights=w, k=k)
    actual = {x: draws.count(x) for x in p}
    expected = {x: dict(probability=str(t), mean=k*float(t),
                       tolerance=10*math.sqrt(k*float(t)*(1-float(t))))
                for x, t in zip(p, probabilities)}
    broken = any(abs(actual[x] - expected[x]['mean']) > expected[x]['tolerance']
                 for x in p)
    if broken:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "counts within 10 standard deviations",
              data, "actual:", actual, "expected:", expected)
```

**Output:**

```
REFUTATION CONFIRMED: {'population': ['a', 'b'], 'weights': [5e-324, 5e-324], 'k': 100000, 'seed': 0} actual: {'a': 25146, 'b': 74854} expected: {'a': {'probability': '1/2', 'mean': 50000.0, 'tolerance': 1581.1388300841897}, 'b': {'probability': '1/2', 'mean': 50000.0, 'tolerance': 1581.1388300841897}}
```

Judge: BUG (medium) -- The inputs are valid finite positive weights, and the exact expected probabilities are correctly computed as 1/2. Multiplying random() by the subnormal total rounds the sampling threshold onto just three values; bisect assigns only the lowest to 'a', producing approximately 1/4 versus 3/4 probabilities. This substantial bias violates relative-weight semantics, rather than being the small round-off bias discussed in the documentation. None of the listed issues describes this behavior, and the upstream diff does not fix choices().

