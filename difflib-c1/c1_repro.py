import difflib
from collections import Counter

data = dict(word=[0j, 3j], possibilities=[[0j, 1j], [0j, 2j]], n=3, cutoff=0.5)
w, ps, n, cutoff = data.values()

def matches(a, b):
    best, i, j = 0, 0, 0
    for x in range(len(a)):
        for y in range(len(b)):
            k = 0
            while x+k < len(a) and y+k < len(b) and a[x+k] == b[y+k]:
                k += 1
            if k > best:
                best, i, j = k, x, y
    return (best + matches(a[:i], b[:j]) + matches(a[i+best:], b[j+best:])
            if best else 0)

def score(p):
    return 2 * matches(w, p) / (len(w) + len(p))

valid = (
    isinstance(ps, list)
    and all(isinstance(s, list) and all(isinstance(x, complex) for x in s)
            for s in [w] + ps)
    and isinstance(n, int) and n > 0 and 0 <= cutoff <= 1
)
if not valid:
    print("REFUTATION REJECTED:", "input violates documented requirements")
else:
    expected = sorted((p for p in ps if score(p) >= cutoff),
                      key=score, reverse=True)[:n]
    try:
        actual = difflib.get_close_matches(**data)
        # Both reported candidates tie, so accept either ordering.
        ok = (isinstance(actual, list)
              and Counter(map(tuple, actual)) == Counter(map(tuple, expected)))
    except Exception as e:
        actual = (type(e).__name__, str(e))
        ok = False
    if ok:
        print("REFUTATION REJECTED:", "actual matches the documented expectation")
    else:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)