import email.utils
import random
import re
import time

ATOM = r"[A-Za-z0-9]+"
ADDRESS = re.compile(
    rf"{ATOM}(?:\.{ATOM})*@[a-z]+(?:\.[a-z]+)+", re.ASCII
)


def reference(field):
    """Validate this restricted RFC-valid grammar independently."""
    address, separator, tail = field.partition(" ")
    assert ADDRESS.fullmatch(address)
    if not separator:
        return [("", address)]
    assert tail.startswith("(") and tail.endswith(")")
    comment = tail[1:-1]
    assert all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ," for c in comment)
    return [(comment, address)]


def call(field):
    try:
        return email.utils.getaddresses([field], strict=True)
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def satisfies(actual, expected):
    # The property constrains cardinality and email, not the display name.
    return (
        isinstance(actual, list)
        and len(actual) == 1
        and isinstance(actual[0], tuple)
        and len(actual[0]) == 2
        and actual[0][1] == expected[0][1]
    )


def main():
    start = time.monotonic()
    deadline = start + 170

    for field in ("alice@example.com", "bob.smith@mail.example.org"):
        expected = reference(field)
        actual = call(field)
        print("SANITY:", repr(field), repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    tested = 0

    def check(field):
        nonlocal tested
        expected = reference(field)
        actual = call(field)
        tested += 1
        if not satisfies(actual, expected):
            repeated = call(field)
            if repeated == actual and not satisfies(repeated, expected):
                print("COUNTEREXAMPLE:", repr(field), repr(actual), repr(expected))
                return True
        return False

    comments = [
        "team, west",
        "team,west",
        ",",
        ",,",
        ",,,",
        ",team",
        "team,",
        ",team,",
        "team,,west",
        "team, west, north",
        "team , west",
        "team, ,west",
        "team" + "," * 100 + "west",
    ]
    for address in ("alice@example.com", "a.b@sub.example.org"):
        for comment in comments:
            if check(address + " (" + comment + ")"):
                return

    rng = random.Random(2822)

    def word():
        return "".join(rng.choice("abcdefghijklmnopqrstuvwxyz")
                       for _ in range(rng.randint(1, 12)))

    for _ in range(100000):
        if time.monotonic() >= deadline:
            break
        local = ".".join(word() for _ in range(rng.randint(1, 3)))
        domain = ".".join(word() for _ in range(rng.randint(2, 4)))
        pieces = [word() for _ in range(rng.randint(1, 8))]
        comment = pieces[0]
        for piece in pieces[1:]:
            comment += (
                " " * rng.randint(0, 2)
                + "," * rng.randint(1, 8)
                + " " * rng.randint(0, 2)
                + piece
            )
        comment = "," * rng.randint(0, 4) + comment + "," * rng.randint(0, 4)
        if "," not in comment:
            comment += ","
        if check(local + "@" + domain + " (" + comment + ")"):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()