import random
import string
import time
from urllib.parse import urljoin

BASE = "https://example.com/a/"


def reference(relative):
    # Every generated reference is a relative path with no dot segments.
    # RFC path merging therefore appends it without removing empty segments.
    return BASE + relative


def main():
    deadline = time.monotonic() + 180.0

    for relative in ("b/c", "Alpha/Beta/Gamma"):
        expected = reference(relative)
        actual = urljoin(BASE, relative)
        print("SANITY:", repr(relative), repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    tested = 0

    def check(relative):
        nonlocal tested
        expected = reference(relative)
        actual = urljoin(BASE, relative)
        tested += 1
        if actual != expected:
            repeated = urljoin(BASE, relative)
            if repeated == actual:
                print("COUNTEREXAMPLE:", repr(relative), repr(actual), repr(expected))
                return True
        return False

    edges = (
        "b//c",
        "b///c",
        "b//c//d",
        "b////c",
        "A/B",
        "Alpha////Beta///Gamma//Delta",
    )
    for relative in edges:
        if time.monotonic() >= deadline:
            break
        if check(relative):
            return

    rng = random.Random(3986)
    while time.monotonic() < deadline:
        segments = [
            "".join(rng.choice(string.ascii_letters)
                    for _ in range(rng.randint(1, 16)))
            for _ in range(rng.randint(2, 10))
        ]
        relative = segments[0]
        for segment in segments[1:]:
            relative += "/" * rng.randint(1, 4) + segment
        if check(relative):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()