import math
from fractions import Fraction
from more_itertools.recipes import running_mean

x = [1e308, 1e308]
if len(x) != 2 or not all(isinstance(v, float) and math.isfinite(v) for v in x):
    print("REFUTATION REJECTED: input is not two finite floats")
else:
    expected = float(sum(map(Fraction, x)) / 2)
    try:
        actual = list(running_mean(x))[1]
    except Exception as e:
        print("REFUTATION REJECTED: could not check second value:", repr(e))
    else:
        if not math.isfinite(actual) or not math.isclose(actual, expected, rel_tol=1e-15):
            print("REFUTATION CONFIRMED:", x, "actual:", actual, "expected:", expected)
        else:
            print("REFUTATION REJECTED: second value agrees with the exact mean")