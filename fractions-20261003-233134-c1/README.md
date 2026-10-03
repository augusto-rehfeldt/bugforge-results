*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `fractions`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `fractions`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Formatting a bounded rational fails when its components exceed the integer-string limit

Target: `fractions.Fraction.__format__`

Property: For every integer k >= 3, let x = Fraction(10**k + 1, 10**k). Formatting x with '.2e' must return '1.00e+00', including when k exceeds the active integer-string conversion limit.

### Draft issue: Fraction scientific formatting fails for near-unit values with large numerators and denominators

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `fractions`

**Documented behaviour:** “Fraction instances support float-style formatting, with presentation types 'e', 'E', 'f', 'F', 'g', 'G' and '%'.” — Python standard library documentation, fractions module, Fraction formatting.

**Expected:** 1.00e+00

**Actual:** ValueError: Exceeds the limit (4300 digits) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: {'x': 'Fraction(10**4300 + 1, 10**4300)', 'int_max_str_digits': 4300, 'format': '.2e'} actual= ('exception', 'ValueError', 'Exceeds the limit (4300 digits) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit') expected= '1.00e+00'
```

Judge: BUG (medium) -- The input is a valid Fraction and '.2e' is a documented presentation. Exact rounding gives 1.00e+00: the excess over 1 is 10**-4300, far below the rounding threshold. The integer-string limit legitimately restricts large decimal conversions, but the requested formatted result is small; raising it because of an internal conversion of a large numerator or denominator leaks an implementation limitation into float-style formatting. None of the listed issues or PRs covers this behaviour, and the supplied upstream diff does not change formatting.

