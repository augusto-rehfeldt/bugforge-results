import collections
import io
import plistlib
import random
import time


def reference(data):
    result = collections.UserDict()
    for key, value in data.items():
        result[key] = value
    return result


def load_target(xml):
    try:
        result = plistlib.load(
            io.BytesIO(xml), dict_type=collections.UserDict
        )
        return result, None
    except Exception as exc:
        return None, (type(exc).__name__, str(exc))


def matches(result, error, expected):
    return (
        error is None
        and isinstance(result, collections.UserDict)
        and result == expected
    )


def describe(result, error):
    if error is not None:
        return "exception " + repr(error)
    return type(result).__name__ + "(" + repr(result) + ")"


def main():
    deadline = time.monotonic() + 170.0

    # Check the independent reference against ordinary, default-dict loads.
    for number, data in enumerate(
        ({"a": "b"}, {"name": "Alice", "city": "Paris"}), 1
    ):
        expected = reference(data)
        try:
            actual = plistlib.load(
                io.BytesIO(plistlib.dumps(data, fmt=plistlib.FMT_XML))
            )
            agrees = isinstance(actual, dict) and actual == expected
        except Exception:
            agrees = False
        print("SANITY {}: {}".format(number, "OK" if agrees else "FAILED"))
        if not agrees:
            print("SANITY FAILED")
            return

    tested = 0

    def check(data):
        nonlocal tested
        expected = reference(data)
        xml = plistlib.dumps(data, fmt=plistlib.FMT_XML)
        actual, error = load_target(xml)
        tested += 1
        if matches(actual, error, expected):
            return False

        repeated, repeated_error = load_target(xml)
        if matches(repeated, repeated_error, expected):
            return False
        if describe(actual, error) != describe(repeated, repeated_error):
            return False

        print("COUNTEREXAMPLE:")
        print(repr(data))
        print("actual:", describe(repeated, repeated_error))
        print("expected: UserDict(" + repr(dict(expected.items())) + ")")
        return True

    edges = [
        {"a": "b"},
        {"": ""},
        {"": "value"},
        {"key": ""},
        {"é": "雪"},
        {"😀": "𝄞"},
        {"a": "b", "": "empty key"},
        {"<&>\"'": "<&>\"'"},
        {"tab\tkey": "line\nvalue"},
        {"a": "\r"},
        {"\r": "b"},
        {"a": "\r\n"},
    ]

    for data in edges:
        if time.monotonic() >= deadline:
            break
        if check(data):
            return

    rng = random.Random(20260319)
    # All characters are permitted by XML 1.0.
    alphabet = list("abcXYZ012 <>&\"'\t\n\r") + [
        "é", "雪", "Ω", "😀", "𝄞", "\u0301", "\u2028"
    ]

    def random_string():
        return "".join(
            rng.choice(alphabet) for _ in range(rng.randrange(25))
        )

    for _ in range(100000):
        if time.monotonic() >= deadline:
            break
        data = {}
        for _ in range(rng.randint(1, 10)):
            data[random_string()] = random_string()
        if check(data):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()