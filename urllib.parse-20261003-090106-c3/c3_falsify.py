import random
import string
import time
from urllib.parse import urljoin

BASE = "https://example.com/base/"


def remove_dot_segments(path):
    """RFC 3986 section 5.2.4, implemented independently."""
    output = ""
    while path:
        if path.startswith("../"):
            path = path[3:]
        elif path.startswith("./"):
            path = path[2:]
        elif path.startswith("/./"):
            path = path[2:]
        elif path == "/.":
            path = "/"
        elif path.startswith("/../"):
            path = path[3:]
            output = output.rsplit("/", 1)[0]
        elif path == "/..":
            path = "/"
            output = output.rsplit("/", 1)[0]
        elif path in (".", ".."):
            path = ""
        else:
            end = path.find("/", 1 if path.startswith("/") else 0)
            if end == -1:
                output += path
                path = ""
            else:
                output += path[:end]
                path = path[end:]
    return output


def expected(reference):
    # All generated references have this authority and no query or fragment.
    prefix = "//other.example"
    assert reference.startswith(prefix + "/")
    path = reference[len(prefix):]
    return "https://other.example" + remove_dot_segments(path)


def main():
    deadline = time.monotonic() + 180
    for reference in ("//other.example/alpha", "//other.example/alpha/beta"):
        actual = urljoin(BASE, reference)
        wanted = expected(reference)
        print("SANITY:", repr(reference), repr(actual), repr(wanted))
        if actual != wanted:
            print("SANITY FAILED")
            return

    tested = 0

    def check(reference):
        nonlocal tested
        wanted = expected(reference)
        actual = urljoin(BASE, reference)
        tested += 1
        if actual != wanted:
            confirmed = urljoin(BASE, reference)
            if confirmed != wanted:
                print("COUNTEREXAMPLE:")
                print(repr((BASE, reference)))
                print("actual:", repr(confirmed))
                print("expected:", repr(wanted))
                return True
        return False

    edges = [
        "//other.example/a/../b",
        "//other.example/Alpha/../Beta",
        "//other.example/a/./b",
        "//other.example/a/./../b",
        "//other.example/a/b/../../c",
        "//other.example/./a/.././b",
        "//other.example/a/../../b",
        "//other.example/a/../b/./c/../d",
    ]
    for reference in edges:
        if check(reference):
            return

    rng = random.Random(3986)

    def segment():
        return "".join(
            rng.choice(string.ascii_letters)
            for _ in range(rng.randint(1, 64))
        )

    while time.monotonic() < deadline:
        s, t = segment(), segment()
        references = [
            "//other.example/" + s + "/../" + t,
            "//other.example/" + s + "/./" + t,
            "//other.example/" + s + "/./.././" + t,
            "//other.example/" + s + "/" + segment() + "/../../" + t,
        ]
        for reference in references:
            if time.monotonic() >= deadline:
                break
            if check(reference):
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()