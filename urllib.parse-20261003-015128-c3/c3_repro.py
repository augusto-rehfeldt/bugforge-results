import re
import urllib.parse

base, r = "https://example.com/a/", "b//c"
if not re.fullmatch(r"[A-Za-z]+(?:/+[A-Za-z]+)*", r):
    print("REFUTATION REJECTED:", "input is outside the claimed domain")
else:
    actual = urllib.parse.urljoin(base, r)
    # RFC 3986: merge with the base directory; no dot segments to remove.
    expected = base + r
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(r), repr(actual), repr(expected))
    else:
        print("REFUTATION REJECTED:", "actual equals the RFC expectation")