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