import math
import statistics

a = 9.5e307
data = dict(a=a, mu=-a, sigma=a, p=0.975)
if not (9.5e307 <= a <= 1e308 and
        all(math.isfinite(v) for v in data.values()) and
        data["sigma"] > 0 and 0 < data["p"] < 1):
    print("REFUTATION REJECTED:", "invalid input", data)
else:
    lo, hi = 0.0, 10.0
    for _ in range(80):
        z = (lo + hi) / 2
        if math.erfc(-z / math.sqrt(2)) / 2 < data["p"]:
            lo = z
        else:
            hi = z
    expected = a * ((lo + hi) / 2 - 1)
    try:
        actual = statistics.NormalDist(data["mu"], data["sigma"]).inv_cdf(data["p"])
        broken = not math.isfinite(actual) or not math.isclose(
            actual, expected, rel_tol=1e-14, abs_tol=0)
    except Exception as exc:
        actual, broken = repr(exc), True
    if broken:
        print("REFUTATION CONFIRMED:", data, "actual =", actual, "expected =", expected)
    else:
        print("REFUTATION REJECTED:", "finite result agrees within tolerance",
              data, "actual =", actual, "expected =", expected)