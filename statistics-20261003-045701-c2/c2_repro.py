import math
import statistics
from fractions import Fraction

x = y = [0.0, 1e-200]
data = {"x": x, "y": y, "proportional": False}
if not (len(x) == len(y) == 2 and x[0] != x[1]
        and all(math.isfinite(v) for v in x + y)):
    print("REFUTATION REJECTED:", "invalid regression input")
else:
    X, Y = list(map(Fraction, x)), list(map(Fraction, y))
    # Two distinct points determine the unique zero-residual OLS line.
    slope = (Y[1] - Y[0]) / (X[1] - X[0])
    expected = (float(slope), float(Y[0] - slope * X[0]))
    try:
        actual = tuple(statistics.linear_regression(x, y))
    except Exception as e:
        actual = {"exception": type(e).__name__, "message": str(e)}
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "actual matches independent OLS expectation")