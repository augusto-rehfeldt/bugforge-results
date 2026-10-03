import statistics
import math

a = 6e307
data = [-a, a]
if len(data) < 2 or not all(math.isfinite(x) for x in data):
    print("REFUTATION REJECTED: invalid input")
else:
    actual = statistics.quantiles(data, n=4, method="exclusive")
    # Interpolate/extrapolate between (-a, 1/3) and (a, 2/3).
    expected = [a * (3 * i / 2 - 3) for i in range(1, 4)]
    if len(actual) != 3 or any(
        not math.isfinite(x) or not math.isclose(x, y, rel_tol=1e-14, abs_tol=0.0)
        for x, y in zip(actual, expected)
    ):
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual matches documented expectation")