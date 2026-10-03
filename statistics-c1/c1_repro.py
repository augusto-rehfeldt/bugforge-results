import math
import statistics

case = dict(data=[0.0], h=1.0, kernel="logistic", cumulative=True, x=710.0)
data, h, x = case["data"], case["h"], case["x"]
z = [(x - d) / h for d in data]
if not (data and math.isfinite(h) and h > 0 and math.isfinite(x)
        and all(math.isfinite(d) for d in data)
        and all(math.isfinite(t) for t in z)):
    print("REFUTATION REJECTED:", "invalid input", case)
elif not hasattr(statistics, "kde"):
    print("REFUTATION REJECTED:", "statistics.kde unavailable")
else:
    # Logistic CDF, evaluated without overflowing either tail.
    expected = sum(1 / (1 + math.exp(-t)) if t >= 0
                   else math.exp(t) / (1 + math.exp(t)) for t in z) / len(data)
    try:
        actual = statistics.kde(data, h, kernel="logistic", cumulative=True)(x)
        broken = not math.isfinite(actual) or not 0 <= actual <= 1
    except Exception as e:
        actual = (type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", case, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "finite probability returned",
              case, "actual:", actual, "expected:", expected)