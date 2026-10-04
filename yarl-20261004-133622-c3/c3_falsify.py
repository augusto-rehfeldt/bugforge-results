import random
import string
import time

from yarl import URL


LETTERS = string.ascii_letters
CONTINUATION = LETTERS + string.digits + "+-."


def valid_scheme(s):
    return (
        bool(s)
        and s[0] in LETTERS
        and all(c in CONTINUATION for c in s[1:])
    )


def observe(url, scheme):
    try:
        return ("returned", str(url.with_scheme(scheme)))
    except Exception as exc:
        return ("raised", type(exc).__name__, str(exc))


def main():
    start = time.monotonic()
    url = URL("https://example.org/path")

    sanity_failed = False
    for scheme in ("http", "https"):
        expected = ("returned", scheme + "://example.org/path")
        actual = observe(url, scheme)
        agrees = valid_scheme(scheme) and actual == expected
        print("SANITY:", repr(scheme), "PASS" if agrees else "FAIL")
        sanity_failed |= not agrees

    if sanity_failed:
        print("SANITY FAILED")
        return

    rng = random.Random(20260817)
    edges = [
        "http", "https", "a", "A", "z", "Z",
        "a0", "a+", "a-", "a.", "HTTP", "HTTPS",
        "a+-.", "a" + "0" * 1024, "a" + "." * 1024,
    ]
    tested = 0

    def check(base):
        nonlocal tested
        assert valid_scheme(base)
        scheme = base + "\n"
        # Derive the expected behavior from the URI scheme grammar.
        assert not valid_scheme(scheme)
        expected = "raises ValueError"
        actual = observe(url, scheme)
        tested += 1
        if actual[:2] == ("raised", "ValueError"):
            return False

        repeated = observe(url, scheme)
        if repeated != actual:
            return False

        print(
            "COUNTEREXAMPLE:", repr(scheme),
            "actual:", repr(actual),
            "expected:", repr(expected),
        )
        return True

    for base in edges:
        if time.monotonic() - start >= 175:
            break
        if check(base):
            return

    for _ in range(100000):
        if time.monotonic() - start >= 175:
            break
        length = rng.choice((1, 2, 3, 8, 32, 128, 1024))
        base = rng.choice(LETTERS) + "".join(
            rng.choice(CONTINUATION) for _ in range(length - 1)
        )
        if check(base):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()