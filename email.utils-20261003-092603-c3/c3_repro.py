import re
from email.utils import parseaddr

n, a = "Alice", "alice@example.com"
s = n + " <" + a
if not (re.fullmatch(r"[A-Za-z]+", n, re.ASCII) and
        re.fullmatch(r"[A-Za-z]+@[A-Za-z]+\.[A-Za-z]+", a, re.ASCII)):
    print("REFUTATION REJECTED: invalid display-name atom or addr-spec")
else:
    # This valid name and addr-spec lack the angle address's required '>'.
    expected = ("", "") if s.count("<") != s.count(">") else None
    try:
        actual = parseaddr(s, strict=True)
    except Exception as e:
        print(f"REFUTATION REJECTED: {type(e).__name__}: {e}")
    else:
        if expected is not None and actual != expected:
            print(f"REFUTATION CONFIRMED: {s!r} actual={actual!r} expected={expected!r}")
        else:
            print("REFUTATION REJECTED: malformed input was rejected")