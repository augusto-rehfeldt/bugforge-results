import configparser
import io
import random
import string
import time


def reference(value):
    # With empty_lines_in_values=False, a blank line ends the value.
    # A subsequent indented alphabetic line cannot restore that value.
    lines = value.split("\n")
    if any(not line for line in lines[:-1]):
        return ("write raised", "InvalidWriteError")
    return ("roundtrip", value)


def actual(value):
    parser = configparser.RawConfigParser(empty_lines_in_values=False)
    parser.add_section("s")
    parser.set("s", "key", value)
    output = io.StringIO()
    try:
        parser.write(output)
    except Exception as exc:
        return ("write raised", type(exc).__name__)

    text = output.getvalue()
    fresh = configparser.RawConfigParser(empty_lines_in_values=False)
    try:
        fresh.read_string(text)
        recovered = fresh.get("s", "key", raw=True)
    except Exception as exc:
        return ("write succeeded; read raised",
                type(exc).__name__, str(exc), text)
    if recovered == value:
        return ("roundtrip", recovered)
    return ("write succeeded; value changed", recovered, text)


def main():
    deadline = time.monotonic() + 175

    for value in ("alpha", "Alpha\nBeta"):
        expected = reference(value)
        observed = actual(value)
        print("SANITY:", repr(value), repr(observed), repr(expected))
        if observed != expected:
            print("SANITY FAILED")
            return

    rng = random.Random(482901)
    edges = [
        ("a", "b"),
        ("A", "B"),
        ("key", "s"),
        ("True", "False"),
        ("a" * 1000, "b"),
        ("a", "Z" * 1000),
    ]
    tested = 0

    def check(a, b):
        nonlocal tested
        value = a + "\n\n" + b
        expected = reference(value)
        observed = actual(value)
        tested += 1
        if observed != expected:
            repeated = actual(value)
            if repeated != expected:
                print("COUNTEREXAMPLE:")
                print(repr((a, b)))
                print("actual:", repr(repeated))
                print("expected:", repr(expected))
                return True
        return False

    for a, b in edges:
        if time.monotonic() >= deadline:
            break
        if check(a, b):
            return

    while time.monotonic() < deadline:
        a = "".join(rng.choices(string.ascii_letters,
                              k=rng.randint(1, 256)))
        b = "".join(rng.choices(string.ascii_letters,
                              k=rng.randint(1, 256)))
        if check(a, b):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()