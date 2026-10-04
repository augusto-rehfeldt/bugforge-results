from sortedcontainers import SortedDict

pairs = [(1, 10)]
if not all(isinstance(p, tuple) and len(p) == 2 and type(p[0]) is int for p in pairs):
    print("REFUTATION REJECTED: invalid integer-keyed pairs")
else:
    error = RuntimeError("iterator failed")

    def source():
        yield from pairs
        raise error

    d = SortedDict()
    caught = None
    try:
        d.update(source())
    except Exception as exc:
        caught = exc

    actual = list(d.keys())
    expected = sorted(dict.keys(d))
    if caught is not error:
        print("REFUTATION REJECTED: expected iterator exception not caught")
    elif actual != expected:
        print("REFUTATION CONFIRMED:", pairs, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: keys remain consistent and sorted")