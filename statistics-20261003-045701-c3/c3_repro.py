import math
import statistics
from fractions import Fraction

a = 1e-200
x = [-a, a]
if not (1e-200 <= a <= 1e-170 and all(map(math.isfinite, x))
        and len(x) >= 2 and len(set(x)) > 1):
    print("REFUTATION REJECTED: invalid input")
else:
    q = list(map(Fraction, x))
    mean = sum(q) / len(q)
    variance = sum((t - mean) ** 2 for t in q)
    expected = float(variance / variance)  # Exact Pearson self-correlation.
    try:
        result = statistics.correlation(x, x)
        actual = ("result", result)
        broken = not math.isclose(result, expected, rel_tol=1e-12)
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", (x, x), "actual =", actual,
              "expected =", expected)
    else:
        print("REFUTATION REJECTED: actual matches exact Pearson self-correlation")