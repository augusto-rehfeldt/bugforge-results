import math
from collections.abc import Set
from sortedcontainers import SortedDict

items = {1j: "a", 1 + 2j: "b"}
ranks = {1j: 0, 1 + 2j: 1}
other = set(items)
data = dict(items=items, integer_ranks=ranks, intersection_set=other)

try:
    if not all(isinstance(k, complex) and math.isfinite(k.real)
               and math.isfinite(k.imag) and type(ranks[k]) is int
               for k in items) or len(set(ranks.values())) != len(items):
        raise ValueError("invalid keys or ranks")
    d = SortedDict(ranks.__getitem__, items)
    if dict(d) != items or list(d) != sorted(items, key=ranks.__getitem__):
        raise ValueError("dictionary construction did not preserve input")
except Exception as e:
    print("REFUTATION REJECTED:", "input validation failed:", repr(e))
else:
    expected = set(items).intersection(other)
    try:
        actual = d.keys() & other
        broken = not isinstance(actual, Set) or set(actual) != expected
    except Exception as e:
        actual = f"{type(e).__name__}: {e}"
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "intersection satisfies the documented promise")