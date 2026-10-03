*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `configparser`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `configparser`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Writing multiline values with blank lines bypasses round-trip validation

Target: `configparser.RawConfigParser.write`

Property: For RawConfigParser(empty_lines_in_values=False) containing section 's' and option 'key' with value a + '\n\n' + b, where a and b are nonempty ASCII alphabetic strings, write(io.StringIO()) must raise InvalidWriteError because its output cannot be read back by an identically configured parser with the same option value.

### Draft issue: configparser.write() fails to reject blank lines in values when empty_lines_in_values=False

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `configparser`

**Documented behaviour:** The configparser documentation for write() says: "If this method would write a representation which cannot be accurately parsed by a future read() call from this parser, an InvalidWriteError is raised."

**Expected:** write() raises configparser.InvalidWriteError for a value containing an embedded blank line when empty_lines_in_values=False.

**Actual:** write() succeeds and emits '[s]\nkey = a\n\t\n\tb\n\n', which an identically configured parser rejects with ParsingError.

**Reproducer:**

```python
import configparser as c
import io

a, b = "a", "b"
value = a + "\n\n" + b
p = c.RawConfigParser(empty_lines_in_values=False)
p.add_section("s")
try:
    if not all(x and x.isascii() and x.isalpha() for x in (a, b)):
        raise ValueError("invalid claimed input")
    p.set("s", "key", value)  # RawConfigParser accepts string values.
    if p.get("s", "key") != value:
        raise ValueError("input was not stored unchanged")
except Exception as e:
    print("REFUTATION REJECTED:", "invalid input:", repr(e))
else:
    out = io.StringIO()
    try:
        p.write(out)
    except Exception as e:
        print("REFUTATION REJECTED:", "write raised", type(e).__name__, str(e))
    else:
        text = out.getvalue()
        q = c.RawConfigParser(empty_lines_in_values=False)
        try:
            q.read_string(text)
            recovered = q.get("s", "key")
            accurate = recovered == value
            actual = ("write succeeded; roundtrip", recovered, text)
        except Exception as e:
            accurate = False
            actual = ("write succeeded; read raised", type(e).__name__, str(e), text)
        if accurate:
            print("REFUTATION REJECTED:", "output accurately round-trips", repr(value))
        else:
            print("REFUTATION CONFIRMED:", (a, b), "actual:", actual,
                  "expected:", ("write raised", "InvalidWriteError"))
```

**Output:**

```
REFUTATION CONFIRMED: ('a', 'b') actual: ('write succeeded; read raised', 'ParsingError', "Source contains parsing errors: '<string>'\n\t[line  4]: '\\tb\\n'", '[s]\nkey = a\n\t\n\tb\n\n') expected: ('write raised', 'InvalidWriteError')
```

Judge: BUG (medium) -- The reproducer stores a valid string value unchanged. With empty_lines_in_values=False, the emitted blank line terminates the multiline value, so the following indented 'b' produces ParsingError. write() nevertheless succeeds, violating its documented InvalidWriteError guarantee. The listed issue is unrelated, and the upstream changes do not address embedded blank lines.

