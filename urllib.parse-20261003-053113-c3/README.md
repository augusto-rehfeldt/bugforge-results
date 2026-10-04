*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `urllib.parse`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `urllib.parse`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Joining an absolute local file URL incorrectly inherits the base server

Target: `urllib.parse.urljoin`

Property: For base = 'file://server/share/base' and reference = 'file:///' + p, where p is a nonempty ASCII alphabetic path segment, urljoin(base, reference) must equal reference: an absolute local file URL must not acquire the base URL's authority.

### Draft issue: urljoin incorrectly inherits base authority for absolute file URLs with empty authority

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `urllib.parse`

**Documented behaviour:** urljoin's docstring promises: "Join a base URL and a possibly relative URL to form an absolute interpretation of the latter." The module documentation identifies RFC 3986 as the current standard; its section 5.2.2 specifies that a reference with an authority uses that authority, including when it is empty, rather than inheriting the base authority.

**Expected:** file:///a

**Actual:** file://server/a

**Reproducer:**

```python
import urllib.parse as u

base, p = 'file://server/share/base', 'a'
ref = 'file:///' + p
b, r = u.urlsplit(base), u.urlsplit(ref)
if not (p.isascii() and p.isalpha()
        and b.scheme == 'file' and b.netloc == 'server'
        and r.scheme == 'file' and ref[5:7] == '//'
        and r.netloc == '' and r.path == '/' + p):
    print('REFUTATION REJECTED:', 'input is not the documented absolute file URL')
else:
    # RFC 3986 §5.2.2: explicit scheme and authority (even empty) replace base.
    expected = 'file://' + '/' + p
    actual = u.urljoin(base, ref)
    if actual != expected:
        print('REFUTATION CONFIRMED:', (base, ref), repr(actual), repr(expected))
    else:
        print('REFUTATION REJECTED:', 'actual equals documented expectation')
```

**Output:**

```
REFUTATION CONFIRMED: ('file://server/share/base', 'file:///a') 'file://server/a' 'file:///a'
```

Judge: BUG (medium) -- The reproducer uses a valid absolute file URL with an explicitly empty authority. RFC 3986 resolution must not inherit the base authority in this case; the result changes a local file URL into a server-qualified URL. The expected value is correct. None of the supplied issues specifically reports this authority-inheritance defect, and the upstream diff contains no urljoin fix.

