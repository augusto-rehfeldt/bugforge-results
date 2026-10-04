*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `configparser`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `configparser`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Writing whitespace-prefixed option names silently changes their names

Target: `configparser.InvalidWriteError`

Property: For RawConfigParser() with section 's' and an option named W + K, where W is a nonempty sequence of ASCII spaces or tabs and K is a nonempty ASCII alphabetic string, write(io.StringIO()) must raise InvalidWriteError because reading the serialized text with an identically configured parser changes the option name.

### Draft issue: configparser.write fails to reject whitespace-prefixed option names

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `configparser`

**Documented behaviour:** "Raised when attempting to write data that the parser would read back differently." — InvalidWriteError documentation.

**Expected:** write() raises configparser.InvalidWriteError for the option name ' a'.

**Actual:** write() emits '[s]\n a = value\n\n' without raising; readback changes the option name to 'a'.

**Reproducer:**

```python
import configparser as c
import io

data = {"W": " ", "K": "a", "option": " a", "value": "value"}
p = c.RawConfigParser()
try:
    p.add_section("s")
    p.set("s", data["option"], data["value"])
    if tuple(p.options("s")) != (data["option"],):
        raise ValueError("reported option was not stored unchanged")
except Exception as e:
    print("REFUTATION REJECTED:", "invalid input:", repr(e))
else:
    # Independently check how the default serialization would be read.
    reference = c.RawConfigParser()
    reference.read_string("[s]\n a = value\n\n")
    expected = ("raised", "InvalidWriteError") if tuple(reference.options("s")) != tuple(p.options("s")) else ("write succeeded",)
    out = io.StringIO()
    try:
        p.write(out)
        reread = c.RawConfigParser()
        reread.read_string(out.getvalue())
        actual = ("write succeeded", tuple(reread.options("s")), out.getvalue())
    except Exception as e:
        actual = ("raised", type(e).__name__)
    if expected == ("raised", "InvalidWriteError") and actual[0] == "write succeeded" and actual[1] != tuple(p.options("s")):
        print("REFUTATION CONFIRMED:", data, "actual=", actual, "expected=", expected)
    else:
        print("REFUTATION REJECTED:", "no demonstrated promise violation", data, "actual=", actual, "expected=", expected)
```

**Output:**

```
REFUTATION CONFIRMED: {'W': ' ', 'K': 'a', 'option': ' a', 'value': 'value'} actual= ('write succeeded', ('a',), '[s]\n a = value\n\n') expected= ('raised', 'InvalidWriteError')
```

Judge: BUG (medium) -- The reproducer uses a valid option name accepted and preserved by RawConfigParser.set(). Writing succeeds, but an identically configured parser strips the leading space on readback, violating the documented round-trip guarantee. The listed issues concern comment-prefixed names and multiline values, not whitespace-prefixed option names; the upstream diff does not address this case.

