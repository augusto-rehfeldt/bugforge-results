*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `configparser`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `configparser`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Multiline value comment lines are silently lost during writing

Target: `configparser.InvalidWriteError`

Property: For RawConfigParser with default settings, section 's', and option 'key' whose value is A + '\n' + P + B, where A and B are nonempty ASCII alphabetic strings and P is '#' or ';', write(io.StringIO()) must raise InvalidWriteError because reading its output with an identically configured parser would discard the second value line.

### Draft issue: configparser fails to reject comment-prefixed multiline values that cannot round-trip

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `configparser`

**Documented behaviour:** The public documentation for InvalidWriteError says: "Raised when attempting to write data that the parser would read back differently."

**Expected:** RawConfigParser.write() raises InvalidWriteError for a value whose continuation line would be discarded as a comment.

**Actual:** write() succeeds, emitting '[s]\nkey = a\n\t#b\n\n'; an identically configured parser reads the value as 'a'.

**Reproducer:**

```python
import configparser as c
import io

data = {"section": "s", "option": "key", "value": "a\n#b"}
p = c.RawConfigParser()
try:
    # Documented input types: string section, option and value.
    p.add_section(data["section"])
    p.set(data["section"], data["option"], data["value"])
except (TypeError, ValueError, c.Error) as e:
    print("REFUTATION REJECTED:", "invalid input:", repr(e))
else:
    out = io.StringIO()
    try:
        p.write(out)
    except Exception as e:
        print("REFUTATION REJECTED:", "write raised", type(e).__name__)
    else:
        text = out.getvalue()
        q = c.RawConfigParser()
        q.read_string(text)
        restored = q.get(data["section"], data["option"])
        actual = ("write succeeded", text, restored)
        # Independently test the documented round-trip promise.
        if restored != data["value"]:
            print("REFUTATION CONFIRMED:", data, "actual:", actual,
                  "expected:", ("exception", "InvalidWriteError"))
        else:
            print("REFUTATION REJECTED:", "round trip preserved the value")
```

**Output:**

```
REFUTATION CONFIRMED: {'section': 's', 'option': 'key', 'value': 'a\n#b'} actual: ('write succeeded', '[s]\nkey = a\n\t#b\n\n', 'a') expected: ('exception', 'InvalidWriteError')
```

Judge: BUG (medium) -- The reproducer uses valid string inputs and demonstrates silent data loss. With default settings, the reader treats the indented '#b' line as a comment, restoring 'a' instead of 'a\n#b'. Successful writing therefore violates the documented InvalidWriteError condition. The supplied upstream changes do not address comment-prefixed continuation lines, and no duplicate is listed.

