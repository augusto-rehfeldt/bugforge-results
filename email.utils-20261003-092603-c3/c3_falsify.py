import email.utils
import random
import re
import string
import time


COMPLETE = re.compile(
    r"([A-Za-z]+) <([A-Za-z]+@[A-Za-z]+(?:\.[A-Za-z]+)+)>",
    re.ASCII,
)
UNCLOSED = re.compile(
    r"([A-Za-z]+) <([A-Za-z]+@[A-Za-z]+(?:\.[A-Za-z]+)+)",
    re.ASCII,
)


def reference(text):
    match = COMPLETE.fullmatch(text)
    if match:
        return match.group(1), match.group(2)
    if UNCLOSED.fullmatch(text):
        # The required closing angle bracket is absent.
        return "", ""
    raise ValueError("Input outside the test grammar")


def actual(text):
    try:
        return email.utils.parseaddr(text, strict=True)
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def main():
    sanity_failed = False
    for text in (
        "Alice <alice@example.com>",
        "Z <a@b.co>",
    ):
        expected = reference(text)
        result = actual(text)
        print("SANITY:", repr(text), repr(result), repr(expected))
        sanity_failed |= result != expected

    if sanity_failed:
        print("SANITY FAILED")
        return

    deadline = time.monotonic() + 179.0
    tested = 0

    def check(text):
        nonlocal tested
        expected = reference(text)
        result = actual(text)
        tested += 1
        if result != expected:
            repeated = actual(text)
            if repeated == result:
                print(
                    "COUNTEREXAMPLE:",
                    repr(text),
                    "actual=" + repr(result),
                    "expected=" + repr(expected),
                )
                return True
        return False

    edge_cases = (
        "Alice <alice@example.com",
        "A <a@b.co",
        "Z <Z@Z.Z",
        "ALICE <ALICE@EXAMPLE.COM",
        "a <b@c.d.e",
        "AbCd <EfGh@IjKl.MnOp",
        ("N" * 256) + " <a@example.com",
        "Alice <" + ("a" * 64) + "@example.com",
        "Alice <a@" + ("b" * 63) + ".com",
        "Alice <a@b." + ("c" * 63),
    )
    for text in edge_cases:
        if time.monotonic() >= deadline:
            break
        if check(text):
            return

    rng = random.Random(1729)
    alphabet = string.ascii_letters

    def word(length):
        return "".join(rng.choice(alphabet) for _ in range(length))

    while time.monotonic() < deadline:
        name = word(rng.randint(1, 80))
        local = word(rng.randint(1, 64))
        labels = [
            word(rng.randint(1, 20))
            for _ in range(rng.randint(2, 6))
        ]
        text = name + " <" + local + "@" + ".".join(labels)
        if check(text):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()