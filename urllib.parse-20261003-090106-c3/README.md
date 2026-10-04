*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `urllib.parse`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `urllib.parse`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: urljoin fails to remove dot segments from network-path references

Target: `urllib.parse.urljoin`

Property: For base='https://example.com/base/' and reference='//other.example/'+s+'/../'+t, where s and t are nonempty ASCII alphabetic path segments, urljoin(base, reference) must equal 'https://other.example/'+t under RFC 3986 reference resolution.

### Draft issue: urllib.parse.urljoin skips dot-segment removal for network-path references

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `urllib.parse`

**Documented behaviour:** The urljoin documentation says: "Construct a full (‘absolute’) URL by combining a ‘base URL’ (base) with another URL (url)." The module documentation identifies RFC 3986 as the current standard. RFC 3986 §5.2.2 specifies T.path = remove_dot_segments(R.path) when the reference has an authority.

**Expected:** https://other.example/b

**Actual:** https://other.example/a/../b

**Reproducer:**

```python
import re
import urllib.parse as u

base = 'https://example.com/base/'
ref = '//other.example/a/../b'
b, r = u.urlsplit(base), u.urlsplit(ref)
if not (b.scheme == 'https' and b.netloc == 'example.com'
        and not r.scheme and r.netloc == 'other.example'
        and not r.query and not r.fragment
        and re.fullmatch(r'/[A-Za-z]+/\.\./[A-Za-z]+', r.path)):
    print('REFUTATION REJECTED: input is outside the stated valid RFC 3986 case')
else:
    # Independently remove dot segments from this absolute reference path.
    segments = []
    for segment in r.path.split('/')[1:]:
        if segment == '..':
            segments.pop()
        elif segment != '.':
            segments.append(segment)
    expected = b.scheme + '://' + r.netloc + '/' + '/'.join(segments)
    actual = u.urljoin(base, ref)
    if actual != expected:
        print('REFUTATION CONFIRMED:', (base, ref),
              'actual:', repr(actual), 'expected:', repr(expected))
    else:
        print('REFUTATION REJECTED: actual equals the RFC 3986 expectation')
```

**Output:**

```
REFUTATION CONFIRMED: ('https://example.com/base/', '//other.example/a/../b') actual: 'https://other.example/a/../b' expected: 'https://other.example/b'
```

Judge: BUG (medium) -- The reference is valid, and the reproducer correctly computes dot-segment removal for the constrained path. RFC 3986 §5.2.2 requires this removal even when the reference supplies its own authority; urljoin instead preserves /a/../b. The supplied upstream diff does not change urljoin, and none of the supplied issue descriptions establishes a duplicate of this authority-reference case.

