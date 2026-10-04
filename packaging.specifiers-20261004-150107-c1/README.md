*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `packaging.specifiers`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `packaging` 26.3

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Specifier equality with strings violates the equal-hash invariant

Target: `packaging.specifiers.Specifier.__hash__`

Property: For every valid specifier string text, let s = Specifier(text). If s == text, then hash(s) must equal hash(text), as required for equal hashable objects.

### Draft issue: Specifier string equality violates the equal-hash invariant

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `packaging` 26.3

**Documented behaviour:** Specifier.__eq__ documents string equality with the example `Specifier("==1.2.3") == "==1.2.3"` returning True. Python's data model documentation for object.__hash__ states: "The only required property is that objects which compare equal have the same hash value."

**Expected:** If Specifier("==1.2.3") == "==1.2.3", their hashes must match.

**Actual:** The objects compare equal, but their hashes are -8135646583026934390 and 735621869667386304.

**Reproducer:**

```python
from packaging.specifiers import Specifier, InvalidSpecifier

text = "==1.2.3"  # Documented valid string-equality example.
try:
    s = Specifier(text)
except InvalidSpecifier:
    print("REFUTATION REJECTED: invalid input", repr(text))
else:
    if s != text:
        print("REFUTATION REJECTED: objects do not compare equal")
    else:
        actual, expected = hash(s), hash(text)
        if actual != expected:
            print("REFUTATION CONFIRMED:", repr(text), "actual =", actual, "expected =", expected)
        else:
            print("REFUTATION REJECTED: equal objects have equal hashes")
```

**Output:**

```
REFUTATION CONFIRMED: '==1.2.3' actual = -8135646583026934390 expected = 735621869667386304
```

Judge: BUG (medium) -- The reproducer uses the documented valid string-equality example and compares hashes in the same process. Equality with a hashable string requires equal hashes; the reported output violates that contract and can break mixed string/Specifier dictionary and set lookups. None of the listed issues or pull requests addresses this cross-type inconsistency. Canonical equality also means simply hashing the original spelling is not a general fix.

