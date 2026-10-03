import math, statistics
from fractions import Fraction

k = j = 600
x, w = 2.0**-k, 2.0**-j
data, weights = [x], [w]
if not (600 <= k <= 900 and 600 <= j <= 900
        and math.isfinite(x) and math.isfinite(w) and x > 0 and w > 0):
    print("REFUTATION REJECTED: invalid input")
else:
    actual = statistics.fmean(data, weights=weights)
    expected = float(Fraction(x) * Fraction(w) / Fraction(w))
    if actual != expected:
        print("REFUTATION CONFIRMED:", dict(data=data, weights=weights),
              "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual equals documented expectation")