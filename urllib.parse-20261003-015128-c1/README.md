# bugforge: `urllib.parse`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `urllib.parse`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: urlsplit rejects documented bytearray inputs before parsing

Target: `urllib.parse.urlsplit`

Property: For every ASCII URL string s that urlsplit(s) successfully parses, urlsplit(bytearray(s, 'ascii')) must also successfully parse and return the corresponding SplitResultBytes, equal to urlsplit(s).encode('ascii'), with default scheme and allow_fragments arguments.

### Draft issue: urllib.parse.urlsplit rejects documented bytearray inputs as unhashable

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `urllib.parse`

**Documented behaviour:** The urllib.parse documentation, section 'Parsing ASCII Encoded Bytes', states: "Accordingly, the URL parsing functions in this module all operate on bytes and bytearray objects in addition to str objects."

**Expected:** SplitResultBytes(scheme=b'', netloc=b'', path=b'', query=b'', fragment=b'')

**Actual:** TypeError: unhashable type: 'bytearray'

**Reproducer:**

```python
import urllib.parse as p

s = ""
x = bytearray(s, "ascii")
expected = p.SplitResultBytes(b"", b"", b"", b"", b"")
try:
    valid = isinstance(x, bytearray) and s.isascii() and p.urlsplit(s).encode("ascii") == expected
except Exception as e:
    valid = False

if not valid:
    print("REFUTATION REJECTED:", "input or reference validation failed")
else:
    try:
        actual = p.urlsplit(x)
        broken = not isinstance(actual, p.SplitResultBytes) or actual != expected
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", repr(x), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "actual matches the documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: bytearray(b'') actual: ('exception', 'TypeError', "unhashable type: 'bytearray'") expected: SplitResultBytes(scheme=b'', netloc=b'', path=b'', query=b'', fragment=b'')
```

Judge: BUG (medium) -- The documentation explicitly supports bytearray inputs. The reproducer uses valid ASCII input and correctly derives the expected bytes result from urlsplit(''). Instead, urlsplit rejects the bytearray as unhashable, breaking that promise. Neither listed issue reports this behaviour; accepting arbitrary falsy values is a different problem.

