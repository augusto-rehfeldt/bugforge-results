import fractions
import sys

if sys.version_info < (3, 12):
    print("REFUTATION REJECTED: float-style Fraction formatting requires Python 3.12+")
    sys.exit(0)

sys.set_int_max_str_digits(4300)
k = 4300
d = 10**k
n = d + 1
x = fractions.Fraction(n, d)
spec = ".2e"  # Valid Fraction and documented float-style presentation.

# Independent exact rounding to two decimal places; x has exponent zero.
q, r = divmod(100 * n, d)
q += 2 * r > d or (2 * r == d and q % 2)
expected = f"{q // 100}.{q % 100:02d}e+00"

try:
    actual = format(x, spec)
except Exception as e:
    actual = ("exception", type(e).__name__, str(e))

if actual != expected:
    print("REFUTATION CONFIRMED:",
          {"x": "Fraction(10**4300 + 1, 10**4300)",
           "int_max_str_digits": sys.get_int_max_str_digits(), "format": spec},
          "actual=", repr(actual), "expected=", repr(expected))
else:
    print("REFUTATION REJECTED: actual matches the exact rounding reference")