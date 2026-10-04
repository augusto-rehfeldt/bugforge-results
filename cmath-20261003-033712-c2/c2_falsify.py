import cmath
import math
import random
import sys
import time
from fractions import Fraction

REL_TOL = 1e-9
ABS_TOL = 0.0
deadline = time.monotonic() + 175.0
tested = 0


def reference(a, b):
    # Compare squared quantities using exact rational arithmetic.
    ar, ai = Fraction(a.real), Fraction(a.imag)
    br, bi = Fraction(b.real), Fraction(b.imag)
    distance_squared = (ar - br) ** 2 + (ai - bi) ** 2
    magnitude_squared = max(ar * ar + ai * ai, br * br + bi * bi)
    return distance_squared <= max(
        Fraction(REL_TOL) ** 2 * magnitude_squared,
        Fraction(ABS_TOL) ** 2,
    )


def actual(a, b):
    try:
        return cmath.isclose(a, b, rel_tol=REL_TOL, abs_tol=ABS_TOL)
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


for a, b in [
    (complex(3.0, 4.0), complex(3.0 + 1e-10, 4.0)),
    (complex(3.0, 4.0), complex(-3.0, -4.0)),
]:
    expected = reference(a, b)
    result = actual(a, b)
    print("SANITY:", repr((a, b)), "actual:", repr(result),
          "expected:", repr(expected))
    if result != expected:
        print("SANITY FAILED")
        sys.exit(0)


def check(x, y):
    global tested
    a = complex(x, y)
    b = -a
    expected = reference(a, b)
    result = actual(a, b)
    tested += 1
    if result != expected:
        confirmed = actual(a, b)
        if confirmed == result:
            inputs = {
                "a": a,
                "b": b,
                "rel_tol": REL_TOL,
                "abs_tol": ABS_TOL,
            }
            print("COUNTEREXAMPLE:", repr(inputs),
                  "actual:", repr(confirmed), "expected:", repr(expected))
            sys.exit(0)


largest = sys.float_info.max
edge = 1.7e308
nearby = [
    edge,
    math.nextafter(edge, 0.0),
    math.nextafter(edge, math.inf),
    largest,
    math.nextafter(largest, 0.0),
]

# Hand-picked cases first, including the primary overflow candidate.
check(edge, edge)
for x in nearby:
    for y in nearby:
        check(x, y)

for x, y in [
    (1.0, 1.0),
    (3.0, 4.0),
    (1e100, 1e100),
    (1e300, 1e300),
    (1e307, 1e307),
    (largest, 1.0),
]:
    check(x, y)

rng = random.Random(20250308)
while time.monotonic() < deadline:
    if rng.randrange(4):
        # Sample finite floats within roughly one million ULPs of max.
        x = float.fromhex("0x1.%013xp+1023" %
                          ((1 << 52) - 1 - rng.randrange(1 << 20)))
        y = float.fromhex("0x1.%013xp+1023" %
                          ((1 << 52) - 1 - rng.randrange(1 << 20)))
    else:
        # Smaller positive finite controls across a broad exponent range.
        x = math.ldexp(rng.uniform(1.0, 1.999999999999), rng.randrange(-1022, 1024))
        y = math.ldexp(rng.uniform(1.0, 1.999999999999), rng.randrange(-1022, 1024))
    check(x, y)

print("NO COUNTEREXAMPLE", tested)