import io
import json
import random
import time


class FalseDict(dict):
    def __bool__(self):
        return False


def quote(s):
    escapes = {
        '"': '\\"', '\\': '\\\\', '\b': '\\b', '\f': '\\f',
        '\n': '\\n', '\r': '\\r', '\t': '\\t',
    }
    parts = ['"']
    for c in s:
        n = ord(c)
        if c in escapes:
            parts.append(escapes[c])
        elif n < 32 or n > 126:
            if n <= 0xFFFF:
                parts.append("\\u%04x" % n)
            else:
                n -= 0x10000
                parts.append("\\u%04x\\u%04x" %
                             (0xD800 + (n >> 10), 0xDC00 + (n & 1023)))
        else:
            parts.append(c)
    parts.append('"')
    return "".join(parts)


def reference_value(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return quote(v)
    raise TypeError("Unsupported reference input")


def reference(d):
    return "{" + ", ".join(
        quote(k) + ": " + reference_value(v) for k, v in d.items()
    ) + "}"


def observe(d):
    stream = io.StringIO()
    try:
        json.dump(d, stream)
        dumped = stream.getvalue()
    except Exception as exc:
        dumped = ("EXCEPTION", type(exc).__name__, str(exc))
    try:
        encoded = json.JSONEncoder().encode(d)
    except Exception as exc:
        encoded = ("EXCEPTION", type(exc).__name__, str(exc))
    return {"dump": dumped, "encode": encoded}


def agrees(d, actual, expected):
    if actual["dump"] != expected or actual["encode"] != expected:
        return False
    return (
        json.loads(actual["dump"]) == dict(d.items())
        and json.loads(actual["encode"]) == dict(d.items())
    )


def main():
    start = time.monotonic()
    for i, ordinary in enumerate([
        {"a": 1},
        {"text": 'é😀\n"\\', "flag": False, "empty": None, "number": -123},
    ], 1):
        expected = reference(ordinary)
        actual = observe(ordinary)
        ok = agrees(ordinary, actual, expected)
        print("SANITY %d: %s" % (i, "PASS" if ok else "FAIL"))
        if not ok:
            print("SANITY FAILED")
            return

    rng = random.Random(271828)
    tested = 0

    def check(d):
        nonlocal tested
        tested += 1
        expected = reference(d)
        actual = observe(d)
        if agrees(d, actual, expected):
            return False
        repeated = observe(d)
        if agrees(d, repeated, expected):
            return False
        print("COUNTEREXAMPLE:")
        print(repr(d))
        print("actual:", repr(repeated))
        print("expected:", repr(expected))
        return True

    edges = [
        {"a": 1},
        {"": None},
        {"a": False, "b": True},
        {"quote\"": "backslash\\", "unicode😀": "é\n"},
        {"zero": 0, "negative": -1, "large": 10**100},
    ]
    for entries in edges:
        if check(FalseDict(entries)):
            return

    alphabet = 'ab09"\\\n\té😀'
    values = [None, False, True, 0, 1, -1, 10**100, "", "é😀", "\x00"]
    while time.monotonic() - start < 170 and tested < 100000:
        d = FalseDict()
        for _ in range(rng.randint(1, 20)):
            key = "".join(rng.choice(alphabet)
                          for _ in range(rng.randint(0, 15)))
            value = (rng.choice(values) if rng.randrange(2)
                     else rng.randint(-10**30, 10**30))
            d[key] = value
        if check(d):
            return
    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()