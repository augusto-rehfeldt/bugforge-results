*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `configparser`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `configparser`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Writing comment-prefixed option names must reject silent data loss

Target: `configparser.RawConfigParser.write`

Property: For a RawConfigParser with default settings, a section named 's', and one option whose name is '#' or ';' followed by nonempty ASCII letters and whose value is 'v', write(io.StringIO()) must raise InvalidWriteError if its output, read by a fresh identically configured parser, would omit that option.

### Draft issue: configparser.write fails to reject comment-prefixed option names

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `configparser`

**Documented behaviour:** The configparser.InvalidWriteError documentation says: "Raised when attempting to write data that the parser would read back differently."

**Expected:** RawConfigParser.write() raises InvalidWriteError for an option name such as '#a' or ';a' that would be omitted on readback.

**Actual:** write() succeeds and emits '[s]\n#a = v\n\n'; a fresh default parser reads section 's' with no options.

**Reproducer:**

```python
import configparser as c
import io

inp = {"section": "s", "option": "#a", "value": "v"}
try:
    # Documented API: string section/option/value; no forbidden option names.
    p = c.RawConfigParser()
    p.add_section(inp["section"])
    p.set(inp["section"], inp["option"], inp["value"])
    original = p.items("s", raw=True)
    if original != [("#a", "v")]:
        raise ValueError("input was not stored as reported")

    out = io.StringIO()
    try:
        p.write(out)
    except Exception as e:
        if isinstance(e, getattr(c, "InvalidWriteError", ())):
            print("REFUTATION REJECTED:", "write raised InvalidWriteError")
        else:
            print("REFUTATION REJECTED:", repr(e))
    else:
        q = c.RawConfigParser()
        q.read_string(out.getvalue())
        readback = q.items("s", raw=True) if q.has_section("s") else []
        actual = {
            "status": "written",
            "output": out.getvalue(),
            "readback_items": readback,
        }
        expected = {
            "must_raise_InvalidWriteError": readback != original,
            "original_items": original,
            "readback_items": readback,
        }
        if expected["must_raise_InvalidWriteError"]:
            print("REFUTATION CONFIRMED:", inp, actual, expected)
        else:
            print("REFUTATION REJECTED:", "output preserves the input", actual)
except Exception as e:
    print("REFUTATION REJECTED:", "validation/readback failed:", repr(e))
```

**Output:**

```
REFUTATION CONFIRMED: {'section': 's', 'option': '#a', 'value': 'v'} {'status': 'written', 'output': '[s]\n#a = v\n\n', 'readback_items': []} {'must_raise_InvalidWriteError': True, 'original_items': [('#a', 'v')], 'readback_items': []}
```

Judge: BUG (medium) -- The reproducer stores a valid string option through the documented API. With default comment prefixes, the emitted '#a = v' line is treated as a comment on readback, silently losing the option. Successful writing therefore contradicts the documented InvalidWriteError round-trip guarantee. The listed issue is unrelated, and the supplied upstream changes do not address comment-prefixed option names.

