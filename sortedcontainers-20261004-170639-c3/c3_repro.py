try:
    from sortedcontainers import SortedSet

    failing = False

    class V(int):
        __slots__ = ()

        def __hash__(self):
            if failing:
                raise ValueError("temporary hash failure")
            return int.__hash__(self)

    v = V(0)  # Immutable and totally ordered; successful hashes are stable integers.
    data = {"values": [0], "pop_index": 0}
    s = SortedSet([v])
    if not (type(hash(v)) is int and hash(v) == hash(v)
            and list(s) == [v] and v in s and v <= v):
        raise RuntimeError("invalid initial input")

    failing = True
    raised = False
    try:
        s.pop(0)
    except ValueError:
        raised = True
    finally:
        failing = False

    items = list(s)
    comparisons = [(int(v), v in s, any(v == x for x in items))]
    actual = {
        "raised_ValueError": raised,
        "iteration": list(map(int, items)),
        "membership_equals_iteration": [(n, a == b) for n, a, b in comparisons],
        "comparisons": comparisons,
    }
    # Independently require the set and list representations to agree.
    expected = {"membership_equals_iteration": [(int(v), True)]}
    if raised and actual["membership_equals_iteration"] != expected["membership_equals_iteration"]:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "no ValueError or representations agree", actual)
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))