*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `configparser`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `configparser`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Writing values containing inline comments silently loses data

Target: `configparser.RawConfigParser.write`

Property: For RawConfigParser(inline_comment_prefixes=('#',)), with section 's' and option 'key' set to a + ' # ' + b, where a and b are nonempty ASCII alphabetic strings, write(io.StringIO()) must either raise InvalidWriteError or produce text that an identically configured parser reads back with get('s', 'key', raw=True) equal to the original value.

### Draft issue: configparser.write() fails to reject values truncated by inline comments

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `configparser`

**Documented behaviour:** "Raised when attempting to write data that the parser would read back differently." — InvalidWriteError documentation in the supplied public API and source.

**Expected:** write() raises InvalidWriteError or produces text that reads back as 'a # b'.

**Actual:** write() succeeds, and readback returns 'a'.

**Reproducer:**

```python
import configparser as c
import io

a, b = "a", "b"
value = a + " # " + b
expected = ("InvalidWriteError or exact readback", value)

try:
    if not all(x and x.isascii() and x.isalpha() for x in (a, b)):
        raise ValueError("input is outside the claimed domain")
    p = c.RawConfigParser(inline_comment_prefixes=("#",))
    p.add_section("s")
    p.set("s", "key", value)  # Valid string section, option and raw value.
except Exception as e:
    print("REFUTATION REJECTED:", "invalid input:", repr(e))
else:
    out = io.StringIO()
    try:
        p.write(out)
    except Exception as e:
        if isinstance(e, getattr(c, "InvalidWriteError", ())):
            print("REFUTATION REJECTED:", "write raised InvalidWriteError")
        else:
            print("REFUTATION REJECTED:", "unexpected write failure:", repr(e))
    else:
        q = c.RawConfigParser(inline_comment_prefixes=("#",))
        try:
            q.read_string(out.getvalue())
            actual = ("readback", q.get("s", "key", raw=True))
        except Exception as e:
            actual = ("read error", repr(e))
        if actual == ("readback", value):
            print("REFUTATION REJECTED:", "exact readback")
        else:
            print("REFUTATION CONFIRMED:", (a, b),
                  "actual:", actual, "expected:", expected)
```

**Output:**

```
REFUTATION CONFIRMED: ('a', 'b') actual: ('readback', 'a') expected: ('InvalidWriteError or exact readback', 'a # b')
```

Judge: BUG (medium) -- The reproducer uses valid section, option, and raw string values. write() succeeds, but an identically configured parser treats ' # b' as an inline comment and returns 'a'. This violates the documented write/readback protection provided by InvalidWriteError. The lack of comment escaping explains why exact serialization is unavailable, but write() should then reject the value. No listed issue or upstream change addresses this case.

