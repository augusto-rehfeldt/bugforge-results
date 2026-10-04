*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `yarl`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `yarl` 1.25.1

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Removing a query parameter must not corrupt surviving parameter values

Target: `yarl.URL.without_query_params`

Property: For URLs constructed with encoded=True whose query consists of distinct ASCII keys and percent-encoded value octets, removing one key must preserve the percent-decoded octets of every surviving value, including octets that are not valid UTF-8.

### Draft issue: without_query_params corrupts non-UTF-8 bytes in surviving query values

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `yarl` 1.25.1

**Documented behaviour:** “Remove some keys from query part and return new URL.” — public API documentation for URL.without_query_params.

**Expected:** The surviving 'keep' value decodes to b'\xff'.

**Actual:** The surviving 'keep' value decodes to b'\xef\xbf\xbd'.

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: ('https://example.com/?keep=%FF&drop=1', 'drop') actual: {'keep': b'\xef\xbf\xbd'} expected: {'keep': b'\xff'}
```

Judge: BUG (medium) -- The reproducer meets its preconditions and correctly compares percent-decoded bytes. %FF is valid percent-encoding even though its decoded byte is not valid UTF-8. Removing only 'drop' changes the unrelated 'keep' value to a UTF-8 replacement character, exceeding the documented key-removal operation. The listed PR does not establish that this behaviour was reported or fixed.

