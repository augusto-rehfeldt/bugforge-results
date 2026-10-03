import random
import time
from email.headerregistry import HeaderRegistry

registry = HeaderRegistry()
ASCII_DIGITS = "0123456789"
SUPERSCRIPTS = "\u00b2\u00b3\u00b9"
ALPHABET = ASCII_DIGITS + SUPERSCRIPTS


def reference(value):
    # Independent interpretation of the stated property.
    parts = value.split(".")
    assert len(parts) == 2
    assert all(part and all(c in ALPHABET for c in part) for part in parts)

    non_ascii = any(c in SUPERSCRIPTS for c in value)
    expected = {"returned_header": True, "has_defects": non_ascii}
    if not non_ascii:
        numbers = []
        for part in parts:
            number = 0
            for character in part:
                number = number * 10 + ord(character) - ord("0")
            numbers.append(number)
        expected.update(major=numbers[0], minor=numbers[1])
    return expected


def observe(value, expected):
    try:
        header = registry("MIME-Version", value)
        actual = {
            "returned_header": True,
            "has_defects": bool(header.defects),
        }
        if "major" in expected:
            actual.update(major=header.major, minor=header.minor)
        return actual
    except Exception as error:
        return {
            "returned_header": False,
            "exception": type(error).__name__,
            "message": str(error),
        }


def main():
    for value in ("1.0", "12.34"):
        expected = reference(value)
        actual = observe(value, expected)
        print("SANITY:", repr(value), "actual:", actual, "expected:", expected)
        if actual != expected:
            print("SANITY FAILED")
            return

    started = time.monotonic()
    deadline = started + 170
    rng = random.Random(1729)
    tested = 0

    def check(value):
        nonlocal tested
        expected = reference(value)
        actual = observe(value, expected)
        tested += 1
        if actual != expected:
            repeated = observe(value, expected)
            if repeated == actual:
                print(
                    "COUNTEREXAMPLE:",
                    repr(value),
                    "actual:",
                    actual,
                    "expected:",
                    expected,
                )
                return True
        return False

    hand_picked = (
        "².0",
        "1.²",
        "1².0",
        "³.1",
        "0.¹",
        "².³",
        "01.0²",
        "¹0.00",
        "0².1³",
    )
    for value in hand_picked:
        if check(value):
            return

    while time.monotonic() < deadline:
        a = "".join(rng.choice(ALPHABET) for _ in range(rng.randint(1, 8)))
        b = "".join(rng.choice(ALPHABET) for _ in range(rng.randint(1, 8)))
        if not any(c in SUPERSCRIPTS for c in a + b):
            position = rng.randrange(len(a))
            a = a[:position] + rng.choice(SUPERSCRIPTS) + a[position + 1:]
        if check(a + "." + b):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()