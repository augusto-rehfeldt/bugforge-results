import math
import statistics
from fractions import Fraction as F

a = 10.0**180
data, weights = [a, 2*a], [1/a, 1/a]
if not all(math.isfinite(x) and x > 0 for x in data + weights):
    print("REFUTATION REJECTED: input is not finite and positive")
else:
    expected = float(sum(map(F, weights)) /
                     sum(F(w) / F(x) for x, w in zip(data, weights)))
    try:
        actual = statistics.harmonic_mean(data, weights=weights)
        broken = not math.isfinite(actual) or not math.isclose(
            actual, expected, rel_tol=1e-14, abs_tol=0)
    except Exception as e:
        actual, broken = (type(e).__name__, str(e)), True
    if broken:
        print("REFUTATION CONFIRMED:", {"data": data, "weights": weights},
              "actual =", actual, "expected =", expected)
    else:
        print("REFUTATION REJECTED: result matches the documented expectation")