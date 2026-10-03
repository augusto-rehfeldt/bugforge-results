*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `email.headerregistry`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.headerregistry`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Address.addr_spec fails to quote local parts with invalid dot placement

Target: `email.headerregistry.Address`

Property: For any nonempty ASCII username containing only letters and dots, and domain='example.com', Address(username=username, domain=domain).addr_spec must be a valid RFC 5322 addr-spec: constructing Address(addr_spec=that_string) must succeed and preserve username and domain, including when the username starts or ends with a dot or contains consecutive dots.

### Draft issue: email.headerregistry.Address fails to quote usernames with leading dots

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `email.headerregistry`

**Documented behaviour:** Address.__init__ docstring: "The addr_spec and the string value of the object are both quoted according to RFC5322 rules, but without any Content Transfer Encoding."

**Expected:** Address(username='.a', domain='example.com').addr_spec returns '".a"@example.com', which parses with username='.a' and domain='example.com'.

**Actual:** addr_spec returns '.a@example.com'; parsing it raises InvalidHeaderDefect.

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: ('.a', 'example.com') actual: ('.a@example.com', 'parse error', 'InvalidHeaderDefect', 'local-part is not dot-atom, quoted-string, or obs-local-part') expected: ('".a"@example.com', '.a', 'example.com')
```

Judge: BUG (medium) -- The username parameter supplies local-part content, not preformatted addr-spec syntax. '.a' is valid quoted-string content but not a valid unquoted local-part. The documented RFC 5322 quoting promise therefore requires quoting it. The reproducer correctly expects '".a"@example.com'; the emitted string instead fails Address's own parser. No duplicate is listed, and the upstream diff does not change this behavior.

