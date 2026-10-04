import math
import statistics
from fractions import Fraction

data = [1e-320, 1e-320]
if len(data) < 2 or not all(math.isfinite(x) and x > 0 for x in data):
    print("REFUTATION REJECTED: invalid input")
else:
    expected = float(len(data) / sum(1 / Fraction(x) for x in data))
    actual = statistics.harmonic_mean(data)
    if actual != expected:
        print(f"REFUTATION CONFIRMED: input={data!r}, actual={actual!r}, expected={expected!r}")
    else:
        print("REFUTATION REJECTED: actual equals documented expectation")