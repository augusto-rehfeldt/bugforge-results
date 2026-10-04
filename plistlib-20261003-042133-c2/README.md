*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `plistlib`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `plistlib`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: XML loading fails with a non-dict mapping factory

Target: `plistlib.load`

Property: For any nonempty dictionary with string keys and string values, loading its XML plist from io.BytesIO with dict_type=collections.UserDict must return a UserDict with the same contents.

### Draft issue: plistlib.load rejects XML dictionary keys when dict_type is collections.UserDict

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `plistlib`

**Documented behaviour:** Python plistlib documentation, load(): "The dict_type is the type of the dictionaries that are returned (by default, dict)."

**Expected:** Return a collections.UserDict containing {'a': 'b'}.

**Actual:** Raises ValueError: unexpected key at line 5.

**Reproducer:**

```python
import plistlib
from io import BytesIO
from collections import UserDict

data = {'a': 'b'}
try:
    if not data or not all(isinstance(k, str) and isinstance(v, str)
                           for k, v in data.items()):
        raise ValueError("input is not a nonempty string-to-string dictionary")
    xml = plistlib.dumps(data, fmt=plistlib.FMT_XML)
    if plistlib.load(BytesIO(xml)) != data:
        raise ValueError("XML does not represent the reported input")
except Exception as e:
    print("REFUTATION REJECTED:", "invalid input:", repr(e))
else:
    expected = UserDict(data)
    try:
        actual = plistlib.load(BytesIO(xml), dict_type=UserDict)
        broken = not isinstance(actual, UserDict) or actual != expected
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", "input:", data,
              "actual:", repr(actual), "expected:", repr(expected))
    else:
        print("REFUTATION REJECTED:", "returned the expected UserDict")
```

**Output:**

```
REFUTATION CONFIRMED: input: {'a': 'b'} actual: ('exception', 'ValueError', 'unexpected key at line 5') expected: {'a': 'b'}
```

Judge: BUG (medium) -- The reproducer generates valid XML and verifies it loads correctly with the default dictionary type. UserDict is a mutable dictionary implementation suitable for dict_type, which is documented as selecting the type of returned dictionaries. Raising an unexpected-key error instead violates that promise. None of the listed issues addresses this behavior, and the upstream diff does not fix XML dictionary parsing.

