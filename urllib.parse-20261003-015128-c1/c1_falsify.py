import random
import time
from urllib.parse import urlsplit, SplitResultBytes


def reference(s):
    """Independent implementation for the ASCII URL input space used here."""
    s = s.lstrip("".join(chr(i) for i in range(33)))
    s = s.replace("\t", "").replace("\r", "").replace("\n", "")

    scheme = ""
    colon = s.find(":")
    if colon > 0:
        candidate = s[:colon]
        if (
            candidate[0] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            and all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-."
                    for c in candidate)
        ):
            scheme = candidate.lower()
            s = s[colon + 1:]

    netloc = ""
    if s.startswith("//"):
        end = len(s)
        for delimiter in "/?#":
            pos = s.find(delimiter, 2)
            if pos >= 0:
                end = min(end, pos)
        netloc, s = s[2:end], s[end:]

    fragment = ""
    if "#" in s:
        s, fragment = s.split("#", 1)

    query = ""
    if "?" in s:
        s, query = s.split("?", 1)

    return SplitResultBytes(
        *(part.encode("ascii") for part in (scheme, netloc, s, query, fragment))
    )


def observe(value):
    try:
        result = urlsplit(value)
        return ("result", result)
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


def matches(actual, expected):
    return (
        actual[0] == "result"
        and isinstance(actual[1], SplitResultBytes)
        and actual[1] == expected
    )


def main():
    start = time.monotonic()
    deadline = start + 175

    for s in ("http://example.com/a?x=1#top", "relative/path?q=%20#part"):
        expected = reference(s)
        observed = urlsplit(s).encode("ascii")
        print("SANITY:", repr(s), repr(observed), repr(expected))
        if observed != expected:
            print("SANITY FAILED")
            return

    handpicked = [
        "",
        "/",
        "relative/path",
        "../a",
        "?",
        "#",
        "?x=1#frag",
        "http://example.com",
        "HTTP://example.com/a?x=%2F#fragment",
        "/a%20b/%FF",
        "//example.com/path",
        "http://[::1]/",
        "http://[2001:db8::1]:8080/a?q=1#f",
        "https://user:pass@example.com:443/",
    ]

    rng = random.Random(736281)
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~%"
    tested = 0

    def check(s):
        nonlocal tested
        # This call is solely the eligibility filter, not the expected oracle.
        try:
            urlsplit(s)
        except Exception:
            return False

        expected = reference(s)
        value = bytearray(s, "ascii")
        actual = observe(value)
        tested += 1

        if not matches(actual, expected):
            confirmed = observe(bytearray(s, "ascii"))
            if not matches(confirmed, expected):
                print("COUNTEREXAMPLE:")
                print(repr(value))
                print("actual:", repr(confirmed))
                print("expected:", repr(expected))
                return True
        return False

    for s in handpicked:
        if time.monotonic() >= deadline:
            break
        if check(s):
            return

    while time.monotonic() < deadline:
        path = "/".join(
            "".join(rng.choice(alphabet) for _ in range(rng.randrange(16)))
            for _ in range(rng.randrange(1, 5))
        )
        prefix = rng.choice([
            "", "/", "../", "http://example.com/",
            "https://example.com:443/", "http://[::1]/",
            "http://[2001:db8::1]:8080/", "//example.com/",
        ])
        s = prefix + path
        if rng.randrange(2):
            s += "?" + rng.choice(["", "a=1", "q=%20", "x=a/b?c", "a=&b=2"])
        if rng.randrange(2):
            s += "#" + rng.choice(["", "top", "%23", "a?b", "a#b"])
        if check(s):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()