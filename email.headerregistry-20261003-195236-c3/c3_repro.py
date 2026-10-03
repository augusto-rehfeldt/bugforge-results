import email.headerregistry as hr
import re
from urllib.parse import unquote_to_bytes

s = "attachment; filename*0*=us-ascii''report; FILENAME*1*=.txt"
# Valid RFC 2231: case-insensitive attributes, consecutive segments,
# declared ASCII charset, empty language, and token-safe ASCII values.
m = re.fullmatch(
    r"attachment; filename\*0\*=us-ascii''([A-Za-z]+); filename\*1\*=([A-Za-z.]+)",
    s, re.I | re.ASCII,
)
if not m:
    print("REFUTATION REJECTED: input fails independent validity check")
else:
    expected = b"".join(unquote_to_bytes(v) for v in m.groups()).decode("ascii")
    actual = hr.HeaderRegistry()("Content-Disposition", s).params.get("filename")
    if actual != expected:
        print(f"REFUTATION CONFIRMED: {s!r} actual={actual!r} expected={expected!r}")
    else:
        print("REFUTATION REJECTED: actual matches documented expectation")