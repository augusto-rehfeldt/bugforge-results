import math
from fractions import Fraction
from statistics import median
import more_itertools

xs = [1e308, 1e308]
if not xs or not all(isinstance(x, float) and math.isfinite(x) and x > 0 for x in xs):
    print("REFUTATION REJECTED: invalid input")
else:
    actual = list(more_itertools.running_median(xs))
    expected = [float(median(list(map(Fraction, xs[:i])))) for i in range(1, len(xs) + 1)]
    if actual != expected:
        print("REFUTATION CONFIRMED:", xs, actual, expected)
    else:
        print("REFUTATION REJECTED: actual matches the documented medians")