import configparser
import io
import random
import string
import time


def roundtrip(value):
    parser = configparser.RawConfigParser(inline_comment_prefixes=("#",))
    parser.add_section("s")
    parser.set("s", "key", value)
    output = io.StringIO()
    try:
        parser.write(output)
    except Exception as exc:
        invalid_write = getattr(configparser, "InvalidWriteError", None)
        if invalid_write is not None and isinstance(exc, invalid_write):
            return ("InvalidWriteError",)
        return ("write exception", type(exc).__name__, str(exc))
    text = output.getvalue()
    reader = configparser.RawConfigParser(inline_comment_prefixes=("#",))
    try:
        reader.read_string(text)
        return ("readback", reader.get("s", "key", raw=True))
    except Exception as exc:
        return ("read exception", type(exc).__name__, str(exc))


def main():
    start = time.monotonic()
    for value in ("alpha", "BetaGamma"):
        expected = ("readback", value)
        actual = roundtrip(value)
        print("SANITY:", repr(value), "actual:", repr(actual),
              "expected:", repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    rng = random.Random(1729)
    alphabet = string.ascii_letters
    edges = [
        ("a", "b"),
        ("A", "B"),
        ("z", "Z"),
        ("alpha", "beta"),
        ("a" * 1024, "b"),
        ("a", "B" * 1024),
    ]
    cases = 0

    def check(a, b):
        nonlocal cases
        # The documented expectation is preservation of the exact set value,
        # unless write rejects it with InvalidWriteError.
        value = a + " # " + b
        expected = ("readback", value)
        actual = roundtrip(value)
        cases += 1
        if actual == ("InvalidWriteError",) or actual == expected:
            return False
        repeated = roundtrip(value)
        if repeated == ("InvalidWriteError",) or repeated == expected:
            return False
        print("COUNTEREXAMPLE:", repr((a, b)),
              "actual:", repr(repeated),
              "expected:", repr(("InvalidWriteError or exact readback", value)))
        return True

    for a, b in edges:
        if check(a, b):
            return

    while time.monotonic() - start < 175:
        a = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 256)))
        b = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 256)))
        if check(a, b):
            return
    print("NO COUNTEREXAMPLE", cases)


if __name__ == "__main__":
    main()