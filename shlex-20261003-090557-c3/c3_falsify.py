import random
import shlex
import string
import time


def reference_child(parent, child):
    # The pushed stream contains exactly one alphabetic word plus whitespace.
    return child


def run_case(parent, child):
    lexer = shlex.shlex(parent + ";tail", posix=True, punctuation_chars=";")
    first = lexer.get_token()
    if first != parent:
        return ("unexpected parent token", first)
    lexer.push_source(child + " ")
    return lexer.get_token()


def main():
    start = time.monotonic()
    deadline = start + 175.0

    # Ordinary stacked inputs without punctuation immediately after the parent.
    for parent, child in (("parent", "child"), ("A", "Z")):
        lexer = shlex.shlex(parent + " tail", posix=True, punctuation_chars=";")
        first = lexer.get_token()
        lexer.push_source(child + " ")
        actual = lexer.get_token()
        expected = reference_child(parent, child)
        agrees = first == parent and actual == expected
        print("SANITY:", repr((parent, child)), repr(actual), repr(expected), agrees)
        if not agrees:
            print("SANITY FAILED")
            return

    rng = random.Random(20260719)
    alphabet = string.ascii_letters
    edges = [
        ("a", "b"),
        ("A", "Z"),
        ("p", "c"),
        ("parent", "child"),
        ("a", "LongChild"),
        ("LongParent", "x"),
        ("abcXYZ", "XYZabc"),
    ]
    tested = 0

    def check(parent, child):
        nonlocal tested
        expected = reference_child(parent, child)
        try:
            actual = run_case(parent, child)
        except Exception as exc:
            actual = ("exception", type(exc).__name__, str(exc))
        tested += 1
        if actual == expected:
            return False

        try:
            repeated = run_case(parent, child)
        except Exception as exc:
            repeated = ("exception", type(exc).__name__, str(exc))
        if repeated != actual:
            return False

        print("COUNTEREXAMPLE:")
        print(repr((parent, child)))
        print("actual:", repr(actual))
        print("expected:", repr(expected))
        return True

    for parent, child in edges:
        if check(parent, child):
            return

    while time.monotonic() < deadline:
        parent = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 128)))
        child = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 128)))
        if check(parent, child):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()