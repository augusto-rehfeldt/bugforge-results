import json
import random
import time


class FalseDict(dict):
    def __bool__(self):
        return False


def reference_string(s):
    escapes = {
        '"': '\\"', '\\': '\\\\', '\b': '\\b', '\f': '\\f',
        '\n': '\\n', '\r': '\\r', '\t': '\\t',
    }
    parts = ['"']
    for ch in s:
        n = ord(ch)
        if ch in escapes:
            parts.append(escapes[ch])
        elif n < 32 or n > 126:
            if n <= 0xffff:
                parts.append("\\u%04x" % n)
            else:
                n -= 0x10000
                parts.append("\\u%04x\\u%04x" %
                             (0xd800 + (n >> 10), 0xdc00 + (n & 1023)))
        else:
            parts.append(ch)
    parts.append('"')
    return ''.join(parts)


def reference_value(value):
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return reference_string(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return repr(value)
    raise TypeError("Unsupported reference value")


def reference(d):
    # Use the actual entries, never the subclass's truth value.
    return "{" + ", ".join(
        reference_string(k) + ": " + reference_value(v)
        for k, v in dict.items(d)
    ) + "}"


def observe(d):
    return json.dumps(d), ''.join(json.JSONEncoder().iterencode(d))


def main():
    for ordinary in [
        {"a": 1},
        {"quote\n": '"\\', "unicode": "é😀", "null": None,
         "bool": False, "float": -0.0},
    ]:
        expected = reference(ordinary)
        actual = observe(ordinary)
        print("SANITY:", repr(ordinary), repr(actual), repr(expected))
        if actual != (expected, expected):
            print("SANITY FAILED")
            return

    count = 0

    def check(d):
        nonlocal count
        count += 1
        expected_text = reference(d)
        expected = (expected_text, expected_text)
        actual = observe(d)
        if actual != expected:
            # Repeat the exact same input before reporting.
            repeated = observe(d)
            if repeated == actual:
                print("COUNTEREXAMPLE:")
                print(repr(d))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return True
        return False

    # Empty control, followed by the requested starting nonempty case.
    edges = [
        FalseDict(),
        FalseDict({"a": 1}),
        FalseDict({"": None}),
        FalseDict({"a": False, "b": True}),
        FalseDict({"é😀": "line\nbreak"}),
        FalseDict({"zero": -0.0, "large": 10**100}),
    ]
    for d in edges:
        if check(d):
            return

    rng = random.Random(1729)
    deadline = time.monotonic() + 175
    alphabet = 'abc"\\\n\té😀'
    values = [None, True, False, 0, 1, -1, 10**100,
              0.0, -0.0, 1.25, "", "hello", "é😀"]

    while time.monotonic() < deadline:
        d = FalseDict()
        for _ in range(rng.randint(1, 12)):
            key = ''.join(rng.choice(alphabet)
                          for _ in range(rng.randint(0, 12)))
            d[key] = rng.choice(values)
        if check(d):
            return

    print("NO COUNTEREXAMPLE", count)


if __name__ == "__main__":
    main()