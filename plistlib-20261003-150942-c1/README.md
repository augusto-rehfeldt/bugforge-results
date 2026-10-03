*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `plistlib`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `plistlib`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: XML serialization normalizes carriage returns in dictionary keys, silently losing entries

Target: `plistlib.dumps`

Property: For every dictionary d with string keys containing only XML-valid characters and integer values in the supported range, plistlib.loads(plistlib.dumps(d, fmt=plistlib.FMT_XML)) must equal d. In particular, distinct keys differing only by carriage-return versus newline characters must remain distinct.

### Draft issue: plistlib XML serialization normalizes carriage returns in keys, causing silent data loss

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `plistlib`

**Documented behaviour:** The plistlib module documentation states: "Values can be strings, integers, floats, booleans, tuples, lists, dictionaries (but only with string keys), Data, bytes, bytearray, or datetime.datetime objects." Its module introduction describes dump as writing the supplied value and load as returning the unpacked root object.

**Expected:** {'a\rb': 1, 'a\nb': 2}

**Actual:** {'a\nb': 1}

**Reproducer:**

```python
import plistlib

d = {'a\rb': 1, 'a\nb': 2}
valid = all(
    isinstance(k, str)
    and all(ord(c) in (9, 10, 13) or 32 <= ord(c) <= 0xD7FF
            or 0xE000 <= ord(c) <= 0xFFFD
            or 0x10000 <= ord(c) <= 0x10FFFF for c in k)
    and type(v) is int and -(1 << 63) <= v < (1 << 64)
    for k, v in d.items()
)
if not valid:
    print('REFUTATION REJECTED:', 'input outside documented domain')
else:
    expected = d.copy()
    actual = plistlib.loads(plistlib.dumps(d, fmt=plistlib.FMT_XML))
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(d), 'actual:', repr(actual),
              'expected:', repr(expected))
    else:
        print('REFUTATION REJECTED:', 'round-trip equals input')
```

**Output:**

```
REFUTATION CONFIRMED: {'a\rb': 1, 'a\nb': 2} actual: {'a\nb': 1} expected: {'a\rb': 1, 'a\nb': 2}
```

Judge: BUG (medium) -- Both keys contain XML-valid characters and both integer values are supported. Serializing a supported dictionary should preserve its keys and values; silently normalizing carriage returns to newlines merges distinct keys and loses data. XML character references can preserve carriage returns, so this is not an unavoidable format limitation. No listed issue or upstream change addresses this behavior.

