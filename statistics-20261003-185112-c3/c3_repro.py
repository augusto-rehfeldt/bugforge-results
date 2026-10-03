import statistics
from fractions import Fraction
from math import isclose, sqrt

x = [2**54, 2**54 + 1]
if len(x) < 2 or len(set(x)) < 2:
    print("REFUTATION REJECTED: input is too short or constant")
else:
    mean = Fraction(sum(x), len(x))
    deviations = [v - mean for v in x]
    covariance = sum(d * d for d in deviations)
    expected = float(covariance) / sqrt(float(covariance * covariance))
    try:
        actual = statistics.correlation(x, x)
        broken = not isclose(actual, expected, rel_tol=0, abs_tol=1e-14)
    except Exception as e:
        actual = f"{type(e).__name__}: {e}"
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", x, "actual=", actual, "expected=", expected)
    else:
        print("REFUTATION REJECTED: result matches independent Pearson calculation")