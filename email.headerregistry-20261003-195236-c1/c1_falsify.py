import random
import string
import time
from email.headerregistry import HeaderRegistry

registry = HeaderRegistry()


def reference(a, b):
    return a + b


def make_header(a, b, name0="filename", name1="filename"):
    return "attachment; " + name0 + "*0*=us-ascii''" + a + "; " + name1 + "*1*=" + b


def evaluate(value):
    try:
        return registry("Content-Disposition", value).params["filename"]
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def main():
    start = time.monotonic()
    for a, b in [("hello", "world"), ("A", "z")]:
        value = make_header(a, b)
        actual = evaluate(value)
        expected = reference(a, b)
        print("SANITY:", repr(value), repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    tested = 0

    def check(a, b, name0, name1):
        nonlocal tested
        value = make_header(a, b, name0, name1)
        expected = reference(a, b)
        actual = evaluate(value)
        tested += 1
        if actual != expected:
            repeated = evaluate(value)
            if repeated != expected:
                print("COUNTEREXAMPLE:", repr(value),
                      "actual =", repr(repeated), "expected =", repr(expected))
                return True
        return False

    edges = [
        ("hello", "world", "filename", "FILENAME"),
        ("hello", "world", "filename", "filename"),
        ("A", "B", "FILENAME", "filename"),
        ("a", "Z", "FileName", "fIlEnAmE"),
        ("ABC", "xyz", "FILENAME", "FILENAME"),
        ("a" * 256, "Z" * 256, "filename", "Filename"),
    ]
    for case in edges:
        if check(*case):
            return

    rng = random.Random(2231)

    def random_name():
        return "".join(
            c.upper() if rng.getrandbits(1) else c
            for c in "filename"
        )

    while time.monotonic() - start < 175:
        a = "".join(rng.choice(string.ascii_letters)
                    for _ in range(rng.randint(1, 128)))
        b = "".join(rng.choice(string.ascii_letters)
                    for _ in range(rng.randint(1, 128)))
        if check(a, b, random_name(), random_name()):
            return
        if check(a, b, "filename", "filename"):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()