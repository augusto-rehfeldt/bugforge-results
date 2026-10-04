import json
import math

class NaN(float):
    def __eq__(self, other): return False
    def __ne__(self, other): return False

x = NaN("nan")
data = [x]
if not (isinstance(x, float) and math.isnan(float(x))):
    print("REFUTATION REJECTED: input is not a NaN float instance")
else:
    expected = ("exception", "ValueError") if not math.isfinite(float(x)) else None
    try:
        actual = ("result", "".join(json.JSONEncoder(allow_nan=False).iterencode(data)))
    except Exception as e:
        actual = ("exception", type(e).__name__)
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, "actual =", actual, "expected =", expected)
    else:
        print("REFUTATION REJECTED: documented ValueError was raised")