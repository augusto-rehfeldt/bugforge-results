*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `pprint`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `pprint`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: saferepr can recurse indefinitely while sorting recursive dictionary keys

Target: `pprint.saferepr`

Property: For dictionaries whose keys are identity-hashable list subclasses inheriting list.__repr__, including distinct self-referential keys, saferepr must return a string without raising RecursionError.

### Draft issue: pprint.saferepr raises RecursionError when sorting self-referential list-subclass dictionary keys

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `pprint`

**Documented behaviour:** The pprint.saferepr documentation states: "Return a string representation of object, protected against recursive data structures." It further specifies: "This only handles recursive instances of dict, list and tuple or subclasses whose __repr__ is not overridden."

**Expected:** Return a string representing the dictionary, with recursion markers for its self-referential keys.

**Actual:** RecursionError: Stack overflow (used 2912 kB) in comparison

**Reproducer:**

```python
import pprint

class Key(list):
    __hash__ = object.__hash__

a, b = Key(), Key()
a.append(a)
b.append(b)
d = {a: 1, b: 2}

if not (len(d) == 2 and a is not b and all(
    isinstance(k, list) and type(k).__repr__ is list.__repr__
    and type(k).__hash__ is object.__hash__ and k[0] is k
    for k in d
)):
    print("REFUTATION REJECTED: input does not meet the documented conditions")
else:
    expected = "{" + ", ".join(
        f"[<Recursion on Key with id={id(k)}>]: {v}" for k, v in d.items()
    ) + "}"
    try:
        actual = pprint.saferepr(d)
        broken = not isinstance(actual, str)
    except Exception as e:
        actual = f"{type(e).__name__}: {e}"
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", "input:", repr(d),
              "actual:", repr(actual), "expected:", repr(expected))
    else:
        print("REFUTATION REJECTED: saferepr returned a string without raising")
```

**Output:**

```
REFUTATION CONFIRMED: input: {[[...]]: 1, [[...]]: 2} actual: 'RecursionError: Stack overflow (used 2912 kB) in comparison' expected: '{[<Recursion on Key with id=1278655537488>]: 1, [<Recursion on Key with id=1278655537136>]: 2}'
```

Judge: BUG (medium) -- The input meets the documented conditions: both keys are list subclasses inheriting list.__repr__, and the dictionary contains two distinct self-referential keys. saferepr's dictionary-key sorting invokes recursive list comparison before recursion-safe formatting, raising RecursionError. The test requires only a string, not the exact illustrative output. None of the listed issues reports or fixes this sorting failure, and the supplied upstream diff leaves the relevant dictionary sorting unchanged.

