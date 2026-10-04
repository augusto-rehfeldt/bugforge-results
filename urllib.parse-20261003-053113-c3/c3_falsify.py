import random
import string
import time
from urllib.parse import urljoin

BASE = "file://server/share/base"


def main():
    # Expected results are literal applications of URL reference resolution.
    sanity_cases = [
        ("https://example.com/a/b", "c", "https://example.com/a/c"),
        ("file://server/share/base", "/other", "file://server/other"),
    ]
    sane = True
    for base, reference, expected in sanity_cases:
        actual = urljoin(base, reference)
        print("SANITY:", repr((base, reference)), repr(actual), repr(expected))
        if actual != expected:
            sane = False
    if not sane:
        print("SANITY FAILED")
        return

    deadline = time.monotonic() + 175
    tested = 0

    def check(segment):
        nonlocal tested
        reference = "file:///" + segment
        # The reference explicitly supplies the file scheme and empty authority.
        expected = reference
        tested += 1
        try:
            actual = urljoin(BASE, reference)
        except Exception as exc:
            actual = ("EXCEPTION", type(exc).__name__, str(exc))
        if actual != expected:
            try:
                repeated = urljoin(BASE, reference)
            except Exception as exc:
                repeated = ("EXCEPTION", type(exc).__name__, str(exc))
            if repeated != expected:
                print("COUNTEREXAMPLE:", repr((BASE, reference)),
                      repr(repeated), repr(expected))
                return True
        return False

    edges = ["a", "Z", "abc", "ABC", "aZ", "a" * 256, "Z" * 65536]
    for segment in edges:
        if time.monotonic() >= deadline:
            break
        if check(segment):
            return

    rng = random.Random(3986)
    alphabet = string.ascii_letters
    while time.monotonic() < deadline:
        length = rng.choice([1, 2, 3, 16, 256, 4096, rng.randint(1, 8192)])
        segment = "".join(rng.choices(alphabet, k=length))
        if check(segment):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()