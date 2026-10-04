*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `unicodedata`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `unicodedata`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Legacy UCD numeric values may leak modern Unihan additions

Target: `unicodedata.UCD.numeric`

Property: For u = unicodedata.ucd_3_2_0 and every character assigned in Unicode 3.2 but lacking a Numeric_Value in that database, u.numeric(character) must raise ValueError, and u.numeric(character, sentinel) must return sentinel by identity—even if the current Unicode database assigns that character a numeric value.

### Draft issue: unicodedata.ucd_3_2_0.numeric returns newer numeric value for U+4EAC

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `unicodedata`

**Documented behaviour:** The unicodedata documentation describes ucd_3_2_0 as “An object that has the same methods as the entire module, but uses the Unicode database version 3.2 instead”. The numeric() entry says: “If no such value is defined, default is returned, or, if not given, ValueError is raised.”

**Expected:** u.numeric('京') raises ValueError; u.numeric('京', sentinel) returns sentinel by identity.

**Actual:** Both calls return 1e+16.

**Reproducer:**

```python
import unicodedata as ud

c = chr(0x4EAC)
u = ud.ucd_3_2_0
sentinel = object()

# Independent reference: U+4EAC has no numeric field in Unicode 3.2's
# UnicodeData.txt or numeric entry in its Unihan data.
reference = {0x4EAC: None}

def call(*args):
    try:
        value = u.numeric(*args)
        return ("returned", "sentinel by identity" if value is sentinel else value)
    except Exception as e:
        return ("raised", type(e).__name__)

if u.unidata_version != "3.2.0" or len(c) != 1 or u.category(c) == "Cn":
    print("REFUTATION REJECTED:", "input is not an assigned Unicode 3.2 character")
elif reference[ord(c)] is not None:
    print("REFUTATION REJECTED:", "reference defines a numeric value")
else:
    expected = (("raised", "ValueError"), ("returned", "sentinel by identity"))
    actual = (call(c), call(c, sentinel))
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(c), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "documented behavior holds for", repr(c))
```

**Output:**

```
REFUTATION CONFIRMED: '京' actual: (('returned', 1e+16), ('returned', 1e+16)) expected: (('raised', 'ValueError'), ('returned', 'sentinel by identity'))
```

Judge: BUG (medium) -- ucd_3_2_0 explicitly promises Unicode 3.2 database semantics. U+4EAC is assigned in that version but has no Numeric_Value there, so returning its newer numeric value violates that promise. Both the exception and default-return paths fail. None of the listed issues addresses this behavior.

