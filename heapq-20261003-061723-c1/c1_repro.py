import heapq
from itertools import chain

data = {"lists": [[1, 3], [2, 4]], "raise_StopIteration_on": 1}
lists = data["lists"]

def key(x):
    if x == data["raise_StopIteration_on"]:
        raise StopIteration
    return x

def outcome(f):
    try:
        return ("result", f())
    except Exception as e:
        if isinstance(e, RuntimeError) and isinstance(e.__cause__, StopIteration):
            e = e.__cause__
        return ("exception", type(e).__name__)

if not all(isinstance(xs, list) and all(type(x) is int for x in xs)
           and xs == sorted(xs) for xs in lists):
    print("REFUTATION REJECTED:", "input is not ascending integer lists")
else:
    actual = outcome(lambda: list(heapq.merge(*lists, key=key)))
    expected = outcome(lambda: sorted(chain.from_iterable(lists), key=key))
    if expected == ("exception", "StopIteration") and actual[0] == "result":
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "no silent successful omission demonstrated",
              data, "actual:", actual, "expected:", expected)