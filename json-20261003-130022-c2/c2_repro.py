import json

class D(dict):
    def __bool__(self):
        return False

d = D(a=1)
if not all(type(k) is str and type(v) is int for k, v in d.items()):
    print("REFUTATION REJECTED: invalid input")
else:
    actual = json.dumps(d), ''.join(json.JSONEncoder().iterencode(d))
    reference = ''.join(json.JSONEncoder().iterencode(dict(d)))
    expected = reference, reference
    if actual != expected:
        print("REFUTATION CONFIRMED:", d, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: both APIs match the dictionary reference")