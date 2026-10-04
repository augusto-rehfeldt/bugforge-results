import cmath
import math
from fractions import Fraction as F

p = dict(a=complex(1.7e308, 1.7e308), b=complex(-1.7e308, -1.7e308),
         rel_tol=1e-9, abs_tol=0.0)
a, b = p["a"], p["b"]
if not (all(map(math.isfinite, (a.real, a.imag, b.real, b.imag,
                                p["rel_tol"], p["abs_tol"])))
        and p["rel_tol"] >= 0 and p["abs_tol"] >= 0):
    print("REFUTATION REJECTED:", "invalid input", p)
else:
    x, y, u, v = map(F, (a.real, a.imag, b.real, b.imag))
    expected = (x-u)**2 + (y-v)**2 <= max(
        F(p["rel_tol"])**2 * max(x*x+y*y, u*u+v*v),
        F(p["abs_tol"])**2)
    actual = cmath.isclose(**p)
    if actual != expected:
        print("REFUTATION CONFIRMED:", p, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "actual agrees with exact expectation",
              p, "actual:", actual, "expected:", expected)