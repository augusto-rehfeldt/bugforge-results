*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `yarl`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `yarl` 1.25.1

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Scheme replacement must reject a trailing newline

Target: `yarl.URL.with_scheme`

Property: For u = URL('https://example.org/path') and any valid nonempty ASCII URI scheme s, u.with_scheme(s + '\n') must raise ValueError: a newline is not permitted in a URI scheme.

### Draft issue: with_scheme accepts a trailing newline in the scheme

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `yarl` 1.25.1

**Documented behaviour:** The URL.with_scheme documentation in the URL API reference states: “Raises ValueError if scheme is invalid.” URI schemes have the syntax ALPHA *( ALPHA / DIGIT / '+' / '-' / '.' ); a trailing newline makes the scheme invalid.

**Expected:** URL('https://example.org/path').with_scheme('http\n') raises ValueError.

**Actual:** Returns a URL whose string representation is 'http\n://example.org/path'.

**Reproducer:**

```python
import re
from yarl import URL

s = 'http'
scheme = s + '\n'
valid = lambda x: re.fullmatch(r'[A-Za-z][A-Za-z0-9+.-]*', x) is not None

if not valid(s) or valid(scheme):
    print('REFUTATION REJECTED: invalid test setup')
else:
    u = URL('https://example.org/path')
    expected = 'raises ValueError'
    try:
        actual = ('returned', str(u.with_scheme(scheme)))
    except Exception as e:
        actual = 'raises ' + type(e).__name__
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(scheme),
              'actual:', repr(actual), 'expected:', repr(expected))
    else:
        print('REFUTATION REJECTED: ValueError raised as documented')
```

**Output:**

```
REFUTATION CONFIRMED: 'http\n' actual: ('returned', 'http\n://example.org/path') expected: 'raises ValueError'
```

Judge: BUG (medium) -- with_scheme explicitly promises ValueError for an invalid scheme. The reproducer correctly verifies that 'http' is valid and 'http\n' is invalid, then shows the latter is accepted and preserved in the resulting URL. Testing invalid input is appropriate for this documented validation guarantee. The listed PRs concern URL parsing or Windows file URLs; none establishes that this with_scheme validation defect is already handled.

