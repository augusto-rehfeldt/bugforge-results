import io, json

class D(dict):
    def __bool__(self):
        return False

d = D(a=1)
if not (D.__iter__ is dict.__iter__ and D.items is dict.items
        and all(type(k) is str and type(v) is int for k, v in d.items())
        and not bool(d) and dict(d) == {"a": 1}):
    print("REFUTATION REJECTED: invalid input")
else:
    expected = json.dumps(dict(d))
    fp = io.StringIO()
    json.dump(d, fp)
    actual = fp.getvalue()
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(d),
              "actual:", repr(actual), "expected:", repr(expected))
    else:
        print("REFUTATION REJECTED: dump preserves all entries")