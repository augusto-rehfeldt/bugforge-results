import heapq

def stream():
    values = iter([0])
    class I:
        def __iter__(self):
            return self
        __next__ = staticmethod(lambda: next(values))
    return I()

x = stream()
expected = list(x)
if iter(x) is not x or not all(type(v) is int for v in expected) or expected != sorted(expected):
    print("REFUTATION REJECTED: invalid input")
else:
    try:
        actual = list(heapq.merge(stream()))
    except Exception as e:
        actual = {"exception": type(e).__name__, "message": str(e)}
    if actual != expected:
        print("REFUTATION CONFIRMED:", "input:", expected, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual equals expected")