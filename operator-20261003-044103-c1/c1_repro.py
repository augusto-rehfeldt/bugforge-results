import operator

class L(list):
    def __iadd__(self, other):
        return [99]

a, ref, b, rb = L([1]), L([1]), [2], [2]
data = {"mode": "fresh99", "initial": list(a), "rhs": list(b)}

def snapshot(result, original, rhs):
    return {
        "result": list(result),
        "result_type": type(result).__name__,
        "original_after": list(original),
        "rhs_after": list(rhs),
        "result_is_original": result is original,
    }

if not (isinstance(a, list) and type(b) is list
        and type(a.__iadd__(b)) is list and a == [1] and b == [2]):
    print("REFUTATION REJECTED:", "input does not satisfy the claimed domain")
else:
    actual = snapshot(operator.iconcat(a, b), a, b)
    original = ref
    ref += rb
    expected = snapshot(ref, original, rb)
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, actual, expected)
    else:
        print("REFUTATION REJECTED:", "iconcat agrees with independently executed +=")