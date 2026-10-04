import math, statistics

data = [1e308, 1e308]
if not all(math.isfinite(x) and x > 0 for x in data):
    print("REFUTATION REJECTED: input is not finite positive numeric data")
else:
    actual = statistics.median(data)
    expected = data[0] / 2 + data[1] / 2
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual equals the documented average")