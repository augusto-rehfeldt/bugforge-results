import random, math

seed, low, high, mode = inp = (0, -1e308, 1e308, None)
if not (math.isfinite(low) and math.isfinite(high) and low < high and mode is None):
    print("REFUTATION REJECTED:", inp, "invalid input")
else:
    random.seed(seed)
    actual = random.triangular(low, high, mode)
    if not low <= actual <= high:
        print("REFUTATION CONFIRMED:", inp, "actual=", actual, "expected=", (low, high))
    else:
        print("REFUTATION REJECTED:", inp, "sample is within the documented interval")