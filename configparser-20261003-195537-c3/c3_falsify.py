import configparser
import io
import random
import string
import time


def run(value):
    parser = configparser.RawConfigParser()
    parser.add_section("s")
    parser.set("s", "key", value)
    output = io.StringIO()
    try:
        parser.write(output)
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))
    text = output.getvalue()
    fresh = configparser.RawConfigParser()
    try:
        fresh.read_string(text)
        restored = fresh.get("s", "key", raw=True)
    except Exception as exc:
        return ("write succeeded", text, "read exception",
                type(exc).__name__, str(exc))
    return ("write succeeded", text, restored)


def reference(a, b, prefix=None):
    # Alphabetic continuation lines survive; default full-line comment
    # prefixes are discarded even when indented. Thus a prefixed second
    # line cannot round-trip and must cause InvalidWriteError.
    if prefix is None:
        return a if b is None else a + "\n" + b
    return ("exception", "InvalidWriteError")


def main():
    deadline = time.monotonic() + 175.0

    for index, (a, b) in enumerate(
        [("Alpha", None), ("Alpha", "Beta")], 1
    ):
        expected = reference(a, b)
        actual = run(expected)
        agrees = actual[0] == "write succeeded" and actual[2] == expected
        print("SANITY {}: reference={!r}, actual={!r}, agrees={}".format(
            index, expected, actual, agrees
        ))
        if not agrees:
            print("SANITY FAILED")
            return

    cases = 0

    def check(a, b, prefix):
        nonlocal cases
        value = a + "\n" + prefix + b
        expected = reference(a, b, prefix)
        actual = run(value)
        cases += 1
        if actual[:2] == expected:
            return False
        repeated = run(value)
        if repeated[:2] == expected:
            return False
        print("COUNTEREXAMPLE:")
        print(repr({"section": "s", "option": "key", "value": value}))
        print("actual:", repr(repeated))
        print("expected:", repr(expected))
        return True

    hand_picked = [
        ("a", "b"),
        ("A", "Z"),
        ("Alpha", "Beta"),
        ("z", "A" * 1024),
        ("a" * 1024, "B"),
        ("AbCdEf", "xYz"),
    ]
    for a, b in hand_picked:
        for prefix in ("#", ";"):
            if time.monotonic() >= deadline:
                print("NO COUNTEREXAMPLE", cases)
                return
            if check(a, b, prefix):
                return

    rng = random.Random(731904)
    alphabet = string.ascii_letters
    while time.monotonic() < deadline:
        a = "".join(rng.choices(alphabet, k=rng.randint(1, 256)))
        b = "".join(rng.choices(alphabet, k=rng.randint(1, 256)))
        if check(a, b, rng.choice(("#", ";"))):
            return

    print("NO COUNTEREXAMPLE", cases)


if __name__ == "__main__":
    main()