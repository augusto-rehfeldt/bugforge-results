from sortedcontainers import SortedDict

mapping = {1+0j: 'a', 2+0j: 'b'}
input_ = {'constructor': 'SortedDict(lambda k: k.real, mapping)', 'mapping': mapping}
try:
    expected = set(mapping.items())  # Independently verifies hashability.
    d = SortedDict(lambda k: k.real, mapping)
    if list(d) != sorted(mapping, key=lambda k: k.real) or set(d.items()) != expected:
        raise ValueError("construction did not preserve the mapping and key-function order")
except Exception as e:
    print("REFUTATION REJECTED:", "invalid input:", repr(e))
else:
    try:
        view = d.items()
        result = view & view
        actual = set(result)
        broken = actual != expected
    except Exception as e:
        actual = ('exception', type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", input_, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "self-intersection has exactly the expected members")