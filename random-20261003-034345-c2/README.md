*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `random`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: vonmisesvariate divides by zero for valid large concentration

Target: `random.Random.vonmisesvariate`

Property: For finite mu in [0, 2*pi] and finite kappa >= 0, vonmisesvariate(mu, kappa) must return a circular-distribution sample without ZeroDivisionError, including when a supported Random subclass supplies random() values in [0, 1). Test a subclass whose first random() result is 1.0 - 2**-53 with mu=0.0 and kappa=1e20.

### Draft issue: random.vonmisesvariate raises ZeroDivisionError for large finite kappa

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `random`

**Documented behaviour:** Random.vonmisesvariate docstring: "mu is the mean angle, expressed in radians between 0 and 2*pi, and kappa is the concentration parameter, which must be greater than or equal to zero." Random class docstring explicitly permits subclassing to "use a different basic generator of your own devising" by overriding random() and the state methods.

**Expected:** Return a finite circular sample without raising an exception.

**Actual:** ZeroDivisionError: division by zero

**Reproducer:**

```python
import math
import random

mu, kappa = 0.0, 1e20
values = (1.0 - 2**-53, 0.5, 0.5, 0.5)
input_ = dict(mu=mu, kappa=kappa, random_values=values)

class R(random.Random):
    def random(self):
        return next(self.values, 0.5)

valid = (math.isfinite(mu) and 0 <= mu <= math.tau
         and math.isfinite(kappa) and kappa >= 0
         and all(0 <= x < 1 for x in values))
if not valid:
    print("REFUTATION REJECTED:", "input violates documented domain", input_)
else:
    r = R()
    r.values = iter(values)
    expected = f"finite circular sample in [0, {2 * math.pi}] without an exception"
    try:
        actual = r.vonmisesvariate(mu, kappa)
        broken = not (math.isfinite(actual) and 0 <= actual <= 2 * math.pi)
    except Exception as e:
        actual = (type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", input_, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "call returned a valid sample", actual)
```

**Output:**

```
REFUTATION CONFIRMED: {'mu': 0.0, 'kappa': 1e+20, 'random_values': (0.9999999999999999, 0.5, 0.5, 0.5)} actual: ('ZeroDivisionError', 'division by zero') expected: finite circular sample in [0, 6.283185307179586] without an exception
```

Judge: BUG (medium) -- The parameters are within the documented domain, and the subclass supplies valid random() values in [0, 1). For kappa=1e20, the algorithm's r rounds to 1.0; the first supplied value makes cos(pi*u1) round to -1.0, so z/(r+z) divides by zero. This is an unhandled numerical failure, not a documented limitation. The upstream changes shown affect unrelated code, and no duplicate was found.

