import pprint

class Key(list):
    __hash__ = object.__hash__

a, b = Key(), Key()
a.append(a)
b.append(b)
d = {a: 1, b: 2}

if not (len(d) == 2 and a is not b and all(
    isinstance(k, list) and type(k).__repr__ is list.__repr__
    and type(k).__hash__ is object.__hash__ and k[0] is k
    for k in d
)):
    print("REFUTATION REJECTED: input does not meet the documented conditions")
else:
    expected = "{" + ", ".join(
        f"[<Recursion on Key with id={id(k)}>]: {v}" for k, v in d.items()
    ) + "}"
    try:
        actual = pprint.saferepr(d)
        broken = not isinstance(actual, str)
    except Exception as e:
        actual = f"{type(e).__name__}: {e}"
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", "input:", repr(d),
              "actual:", repr(actual), "expected:", repr(expected))
    else:
        print("REFUTATION REJECTED: saferepr returned a string without raising")