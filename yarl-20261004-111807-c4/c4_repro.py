import re
from urllib.parse import unquote_to_bytes
from yarl import URL

s, key = "https://example.com/?keep=%FF&drop=1", "drop"
u = URL(s, encoded=True)
pairs = [p.partition("=")[::2] for p in u.raw_query_string.split("&")]
valid = (
    u.raw_query_string == s.split("?", 1)[1]
    and len({k for k, v in pairs}) == len(pairs)
    and all(re.fullmatch(r"[A-Za-z0-9_]+", k)
            and re.fullmatch(r"(?:%[0-9A-Fa-f]{2}|[A-Za-z0-9])*", v)
            for k, v in pairs)
)
if not valid:
    print("REFUTATION REJECTED:", "input does not meet the stated preconditions")
else:
    expected = {k: unquote_to_bytes(v) for k, v in pairs if k != key}
    result = u.without_query_params(key)
    actual = {
        k: unquote_to_bytes(v)
        for k, v in (p.partition("=")[::2]
                     for p in result.raw_query_string.split("&") if p)
    }
    if actual != expected:
        print("REFUTATION CONFIRMED:", (s, key), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "surviving value octets are preserved")