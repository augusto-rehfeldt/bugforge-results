import math
import statistics

a = 1e308
mu, sigma, x = -a, a, a
if not (all(map(math.isfinite, (mu, sigma, x))) and 0 < a <= 1.2e308):
    print("REFUTATION REJECTED: invalid input")
else:
    actual = statistics.NormalDist(mu, sigma).cdf(x)
    z = x / sigma - mu / sigma  # Avoid overflow in x - mu.
    expected = (1 + math.erf(z / math.sqrt(2))) / 2
    if not abs(actual - expected) <= 1e-15:
        print("REFUTATION CONFIRMED:", (mu, sigma, x), actual, expected)
    else:
        print("REFUTATION REJECTED: agrees within absolute tolerance 1e-15")