*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `configparser`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `configparser`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Writing whitespace-padded values silently changes their contents

Target: `configparser.RawConfigParser.write`

Property: For a default RawConfigParser containing section 's' and option 'key' with value L + 'value' + R, where L and R contain only ASCII spaces or tabs and at least one is nonempty, write(io.StringIO()) must either raise InvalidWriteError or produce text that a fresh identically configured parser reads back with exactly the original value.

### Draft issue: configparser.write silently loses surrounding value whitespace instead of raising InvalidWriteError

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `configparser`

**Documented behaviour:** The public API documentation for InvalidWriteError says: "Raised when attempting to write data that the parser would read back differently."

**Expected:** Preserve the exact value ' value' on readback or raise InvalidWriteError.

**Actual:** write() succeeds with '[s]\nkey =  value\n\n'; readback returns 'value'.

**Reproducer:**

```python
import configparser as c
import io

data = {"L": " ", "R": ""}
value = data["L"] + "value" + data["R"]
p = c.RawConfigParser()
try:
    # Documented inputs: a non-DEFAULT section and string option/value.
    p.add_section("s")
    p.set("s", "key", value)
    if p.get("s", "key") != value:
        print("REFUTATION REJECTED:", "input was not stored unchanged")
    else:
        out = io.StringIO()
        try:
            p.write(out)
        except getattr(c, "InvalidWriteError", ()):
            print("REFUTATION REJECTED:", "InvalidWriteError raised as permitted")
        else:
            q = c.RawConfigParser()
            try:
                q.read_string(out.getvalue())
                actual = q.get("s", "key")
            except c.Error as e:
                actual = (type(e).__name__, str(e))
            if actual != value:
                print("REFUTATION CONFIRMED:", data,
                      "actual:", (actual, out.getvalue()),
                      "expected:", (value, "or InvalidWriteError"))
            else:
                print("REFUTATION REJECTED:", "exact value preserved")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: {'L': ' ', 'R': ''} actual: ('value', '[s]\nkey =  value\n\n') expected: (' value', 'or InvalidWriteError')
```

Judge: BUG (medium) -- The reproducer uses valid inputs and verifies that the original value is stored unchanged. write() then silently emits text that loses leading whitespace when read by an identically configured parser, contrary to the documented InvalidWriteError guarantee. Neither listed issue addresses this behaviour, and the upstream changes shown do not fix it.

