import urllib.parse as p

s = ""
x = bytearray(s, "ascii")
expected = p.SplitResultBytes(b"", b"", b"", b"", b"")
try:
    valid = isinstance(x, bytearray) and s.isascii() and p.urlsplit(s).encode("ascii") == expected
except Exception as e:
    valid = False

if not valid:
    print("REFUTATION REJECTED:", "input or reference validation failed")
else:
    try:
        actual = p.urlsplit(x)
        broken = not isinstance(actual, p.SplitResultBytes) or actual != expected
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", repr(x), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "actual matches the documented expectation")