import statistics, math
from fractions import Fraction

x = [-7e153, -7e153, 7e153, 7e153]
y = x.copy()
if len(x) != len(y) or len(x) < 2 or not all(map(math.isfinite, x + y)):
    print("REFUTATION REJECTED: invalid input")
else:
    n = len(x)
    u, v = list(map(Fraction, x)), list(map(Fraction, y))
    expected = float((sum(a*b for a, b in zip(u, v)) - sum(u)*sum(v)/n)/(n-1))
    try:
        actual = statistics.covariance(x, y)
        broken = not math.isfinite(actual) or not math.isclose(actual, expected, rel_tol=1e-14)
    except Exception as e:
        actual, broken = repr(e), True
    if broken:
        print("REFUTATION CONFIRMED:", (x, y), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: sample covariance agrees with exact reference")