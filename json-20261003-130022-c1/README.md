*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `json`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `json`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: dump and JSONEncoder.encode disagree for nonempty dictionaries with false truth values

Target: `json.dump`

Property: For every dict subclass instance d with ordinary dictionary iteration and items(), string keys, JSON-serializable primitive values, and __bool__ returning False, json.dump(d, an io.StringIO()) must produce the same JSON representation as json.JSONEncoder().encode(d), preserving all entries.

### Draft issue: json.dump silently drops entries from dict subclasses with false truthiness

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `json`

**Documented behaviour:** json.dump documentation: "Serialize obj as a JSON formatted stream to fp (a .write()-supporting file-like object)." JSONEncoder documentation lists "dict" as supported and maps it to JSON "object".

**Expected:** {"a": 1}

**Actual:** {}

**Reproducer:**

```python
import io, json

class D(dict):
    def __bool__(self):
        return False

d = D(a=1)
if not (D.__iter__ is dict.__iter__ and D.items is dict.items
        and all(type(k) is str and type(v) is int for k, v in d.items())
        and not bool(d) and dict(d) == {"a": 1}):
    print("REFUTATION REJECTED: invalid input")
else:
    expected = json.dumps(dict(d))
    fp = io.StringIO()
    json.dump(d, fp)
    actual = fp.getvalue()
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(d),
              "actual:", repr(actual), "expected:", repr(expected))
    else:
        print("REFUTATION REJECTED: dump preserves all entries")
```

**Output:**

```
REFUTATION CONFIRMED: {'a': 1} actual: '{}' expected: '{"a": 1}'
```

Judge: BUG (medium) -- The input is a supported dict subclass with ordinary iteration and items(); overriding truthiness does not remove its entries. The reproducer correctly establishes that it contains {'a': 1}, yet dump silently serializes an empty object. This violates serialization of a supported dictionary, not merely an undocumented equivalence between APIs. The cited issue concerns an empty iterator with a fake length producing malformed output, not this loss of nonempty dictionary entries. The __init__.py-only comparison cannot establish whether upstream encoder code already fixes this.

