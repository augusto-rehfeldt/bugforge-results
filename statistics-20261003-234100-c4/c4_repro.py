import math
import statistics as s

p = dict(data=[0.0], h=1.0, kernel="sigmoid", cumulative=False)
x = 720.0
inp = dict(p, x=x)
try:
    if not hasattr(s, "kde"):
        raise ValueError("statistics.kde unavailable")
    if "sigmoid" not in (s.kde.__doc__ or ""):
        raise ValueError("sigmoid not documented")
    if not (p["data"] and all(map(math.isfinite, p["data"]))
            and math.isfinite(p["h"]) and p["h"] > 0
            and math.isfinite(x) and 720 <= x <= 1000):
        raise ValueError("invalid input")
    expected = 2 * math.exp(-abs(x)) / (math.pi * (1 + math.exp(-2 * abs(x))))
    try:
        actual = s.kde(**p)(x)
        broken = not (math.isfinite(actual) and actual >= 0
                      and math.isclose(actual, expected, rel_tol=1e-12, abs_tol=0))
    except Exception as e:
        actual = (type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", inp, "actual =", actual, "expected =", expected)
    else:
        print("REFUTATION REJECTED:", "valid input returns the expected density")
except Exception as e:
    print("REFUTATION REJECTED:", str(e))