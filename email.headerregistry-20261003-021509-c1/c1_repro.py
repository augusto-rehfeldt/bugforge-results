import re
from email.headerregistry import Address

u, d = ".a", "example.com"
try:
    if not re.fullmatch(r"[A-Za-z.]+", u) or d != "example.com":
        raise ValueError("input is outside the documented test case")
    # username is supplied unquoted, not as an addr_spec; dots are legal
    # quoted-string content. Only dot-atoms may remain unquoted here.
    local = u if re.fullmatch(r"[A-Za-z]+(?:\.[A-Za-z]+)*", u) else f'"{u}"'
    expected = (local + "@" + d, u, d)
    a = Address(username=u, domain=d)
    if (a.username, a.domain) != (u, d):
        raise ValueError("constructor did not accept the input unchanged")
    s = a.addr_spec
    try:
        b = Address(addr_spec=s)
        actual = (s, b.username, b.domain)
    except Exception as e:
        actual = (s, "parse error", type(e).__name__, str(e))
    if actual != expected:
        print("REFUTATION CONFIRMED:", (u, d), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: output is correctly quoted and round-trips")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))