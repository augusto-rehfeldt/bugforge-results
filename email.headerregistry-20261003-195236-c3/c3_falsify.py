import random
import string
import time
from email.headerregistry import HeaderRegistry

registry = HeaderRegistry()


def reference(first, second):
    # us-ascii segments here contain only literal ASCII characters.
    return first + second


def actual(value):
    try:
        return registry("Content-Disposition", value).params["filename"]
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def make_value(first, second, name0="filename", name1="filename"):
    return (
        "attachment; " + name0 + "*0*=us-ascii''" + first
        + "; " + name1 + "*1*=" + second
    )


for first, second in [("report", ".txt"), ("Alpha", "Beta")]:
    value = make_value(first, second)
    expected = reference(first, second)
    result = actual(value)
    print("SANITY:", repr(value), "actual =", repr(result),
          "expected =", repr(expected))
    if result != expected:
        print("SANITY FAILED")
        raise SystemExit(0)

tested = 0
deadline = time.monotonic() + 175


def check(value, expected):
    global tested
    tested += 1
    result = actual(value)
    if result != expected:
        repeated = actual(value)
        if repeated != expected:
            print("COUNTEREXAMPLE:", repr(value),
                  "actual =", repr(repeated), "expected =", repr(expected))
            raise SystemExit(0)


edges = [
    ("report", ".txt", "filename", "FILENAME"),
    ("report", ".txt", "FILENAME", "filename"),
    ("a", "b", "filename", "FILENAME"),
    ("a", "b", "FILENAME", "filename"),
    ("Alpha", "Beta", "FiLeNaMe", "fIlEnAmE"),
    ("X", "Y", "FILENAME", "FILENAME"),
    ("LongAlphabeticSegment", "AnotherSegment", "fileName", "Filename"),
]

for first, second, name0, name1 in edges:
    expected = reference(first, second)
    check(make_value(first, second), expected)
    check(make_value(first, second, name0, name1), expected)

rng = random.Random(2231)


def varied_name():
    return "".join(
        char.upper() if rng.getrandbits(1) else char
        for char in "filename"
    )


while time.monotonic() < deadline:
    first = "".join(rng.choice(string.ascii_letters)
                    for _ in range(rng.randint(1, 64)))
    second = "".join(rng.choice(string.ascii_letters)
                     for _ in range(rng.randint(1, 64)))
    name0, name1 = varied_name(), varied_name()
    expected = reference(first, second)
    check(make_value(first, second), expected)
    check(make_value(first, second, name0, name1), expected)

print("NO COUNTEREXAMPLE", tested)