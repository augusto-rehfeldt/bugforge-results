import math
from statistics import NormalDist

p = ((0.0, 1e150), (0.0, 2e150))
if not all(math.isfinite(m) and math.isfinite(s) and s > 0 for m, s in p):
    print("REFUTATION REJECTED:", "invalid normal-distribution parameters")
else:
    # Integrate the narrower density outside the crossings, wider inside.
    t = math.sqrt(4 * math.log(2) / 3)
    expected = 1 + math.erf(t / 2) - math.erf(t)
    try:
        actual = NormalDist(*p[0]).overlap(NormalDist(*p[1]))
    except Exception as e:
        print("REFUTATION CONFIRMED:", p, "actual =", repr(e), "expected =", expected)
    else:
        if not math.isfinite(actual) or abs(actual - expected) > 1e-12:
            print("REFUTATION CONFIRMED:", p, "actual =", actual, "expected =", expected)
        else:
            print("REFUTATION REJECTED:", "actual agrees with the independent integral")