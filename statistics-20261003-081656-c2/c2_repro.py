import math
import statistics

a = 1e160
data, mu = [-a, a], 0.0
expected = math.hypot(*data) / math.sqrt(len(data))
if not (all(map(math.isfinite, data)) and math.fsum(data) / len(data) == mu):
    print("REFUTATION REJECTED: invalid input or incorrect mean")
else:
    try:
        actual = statistics.pstdev(data, mu=mu)
    except Exception as e:
        actual = f"{type(e).__name__}: {e}"
    if not isinstance(actual, float) or not math.isclose(actual, expected, rel_tol=1e-15):
        print("REFUTATION CONFIRMED:", {"data": data, "mu": mu},
              "actual=", actual, "expected=", expected)
    else:
        print("REFUTATION REJECTED: result agrees with documented expectation")