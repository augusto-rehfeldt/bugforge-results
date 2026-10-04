try:
    from more_itertools import all_unique
    data = [set(), frozenset()]
    comparisons = [x == y for x in data for y in data]
    if not all(type(x) is bool for x in comparisons):
        raise ValueError("equality is not Boolean")
    expected = not any(data[i] == data[j]
                       for i in range(len(data)) for j in range(i))
    actual = all_unique(data, key=None)
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: result matches documented expectation")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))