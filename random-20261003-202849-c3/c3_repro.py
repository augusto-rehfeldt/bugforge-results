import random, math
from fractions import Fraction

p, w, k, seed = ['a', 'b'], [2**-1074]*2, 100000, 0
data = dict(population=p, weights=w, k=k, seed=seed)
if not (len(p) == len(w) and all(math.isfinite(x) and x > 0 for x in w)
        and math.isfinite(sum(w)) and sum(w) > 0):
    print("REFUTATION REJECTED:", "invalid input", data)
else:
    q = [Fraction(x) for x in w]
    probabilities = [x / sum(q) for x in q]
    draws = random.Random(seed).choices(p, weights=w, k=k)
    actual = {x: draws.count(x) for x in p}
    expected = {x: dict(probability=str(t), mean=k*float(t),
                       tolerance=10*math.sqrt(k*float(t)*(1-float(t))))
                for x, t in zip(p, probabilities)}
    broken = any(abs(actual[x] - expected[x]['mean']) > expected[x]['tolerance']
                 for x in p)
    if broken:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "counts within 10 standard deviations",
              data, "actual:", actual, "expected:", expected)