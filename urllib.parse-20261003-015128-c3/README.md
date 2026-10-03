*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `urllib.parse`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `urllib.parse`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: urljoin must preserve empty interior path segments

Target: `urllib.parse.urljoin`

Property: For a base URL 'https://example.com/a/' and a relative reference r consisting of nonempty ASCII alphabetic path segments separated by one or more '/' characters, with no query, fragment, or dot segments, urljoin(base, r) must equal base + r. In particular, repeated interior slashes must be preserved.

### Draft issue: urllib.parse.urljoin incorrectly collapses repeated slashes in relative paths

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `urllib.parse`

**Documented behaviour:** urljoin's docstring promises: "Join a base URL and a possibly relative URL to form an absolute interpretation of the latter." The module documentation states: "RFC 3986 is considered the current standard and any future changes to urllib.parse module should conform with it." RFC 3986 sections 5.2.3–5.2.4 specify path merging and dot-segment removal; empty interior segments are not dot segments.

**Expected:** https://example.com/a/b//c

**Actual:** https://example.com/a/b/c

**Reproducer:**

```python
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
```

**Output:**

```
REFUTATION CONFIRMED: 'b//c' 'https://example.com/a/b/c' 'https://example.com/a/b//c'
```

Judge: BUG (medium) -- The reference 'b//c' is valid and satisfies the claimed domain. RFC 3986 path merging yields '/a/b//c', and dot-segment removal does not remove empty interior segments. Collapsing these slashes changes the path and violates the documented RFC-based resolution semantics. The listed issue concerns argument types, not slash preservation.

