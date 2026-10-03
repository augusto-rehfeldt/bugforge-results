import statistics, math
from fractions import Fraction

data = [1e308, 1e308]
if not data or not all(isinstance(x, float) and math.isfinite(x) for x in data):
    print("REFUTATION REJECTED: input is not nonempty finite float data")
else:
    expected = float(sum(map(Fraction, data), Fraction()) / len(data))
    try:
        actual = statistics.fmean(data)
        broken = not math.isclose(actual, expected, rel_tol=1e-15)
    except Exception as e:
        actual = f"{type(e).__name__}: {e}"
        broken = True
    if broken:
        print(f"REFUTATION CONFIRMED: input={data!r}, actual={actual!r}, expected={expected!r}")
    else:
        print("REFUTATION REJECTED: result matches the independently computed arithmetic mean")