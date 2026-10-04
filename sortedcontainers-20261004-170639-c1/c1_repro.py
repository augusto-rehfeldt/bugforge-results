try:
    from sortedcontainers import SortedDict

    class M(dict):
        def __iter__(self):
            return iter(())

    initial = {i: -i for i in range(100)}
    m = M({100: 1000})
    entries = {k: m[k] for k in m.keys()}
    d = SortedDict(initial)
    if not d or entries != {100: 1000} or list(m) or not all(
        type(k) is type(v) is int for k, v in initial.items()
    ):
        print("REFUTATION REJECTED: invalid input")
    else:
        expected = initial.copy()
        expected.update(m)
        d.update(m)
        actual = dict(d.items())
        if actual != expected:
            print("REFUTATION CONFIRMED:",
                  {"initial": initial, "M_entries": entries},
                  "actual:", actual, "expected:", expected)
        else:
            print("REFUTATION REJECTED: actual matches dict.update")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))