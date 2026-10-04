*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `sortedcontainers`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `sortedcontainers` 2.4.0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Keys-view intersection fails for valid key-ordered, non-orderable keys

Target: `sortedcontainers.SortedKeysView`

Property: For a SortedDict d whose keys are finite complex numbers and whose supplied key function returns distinct integer ranks, d.keys() & set(d) must succeed and return a set-like collection containing exactly the keys of d.

### Draft issue: SortedKeysView intersection fails for keys ordered by a custom key function

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `sortedcontainers` 2.4.0

**Documented behaviour:** “Sorted keys views also support set-like operations.” — SortedKeysView class documentation. Intersection is a supported set operation on the dictionary's valid, hashable keys.

**Expected:** Intersection succeeds and returns a set-like collection containing 1j and (1+2j).

**Actual:** TypeError: '<' not supported between instances of 'complex' and 'complex'

**Reproducer:**

```python
import math
from collections.abc import Set
from sortedcontainers import SortedDict

items = {1j: "a", 1 + 2j: "b"}
ranks = {1j: 0, 1 + 2j: 1}
other = set(items)
data = dict(items=items, integer_ranks=ranks, intersection_set=other)

try:
    if not all(isinstance(k, complex) and math.isfinite(k.real)
               and math.isfinite(k.imag) and type(ranks[k]) is int
               for k in items) or len(set(ranks.values())) != len(items):
        raise ValueError("invalid keys or ranks")
    d = SortedDict(ranks.__getitem__, items)
    if dict(d) != items or list(d) != sorted(items, key=ranks.__getitem__):
        raise ValueError("dictionary construction did not preserve input")
except Exception as e:
    print("REFUTATION REJECTED:", "input validation failed:", repr(e))
else:
    expected = set(items).intersection(other)
    try:
        actual = d.keys() & other
        broken = not isinstance(actual, Set) or set(actual) != expected
    except Exception as e:
        actual = f"{type(e).__name__}: {e}"
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "intersection satisfies the documented promise")
```

**Output:**

```
REFUTATION CONFIRMED: {'items': {1j: 'a', (1+2j): 'b'}, 'integer_ranks': {1j: 0, (1+2j): 1}, 'intersection_set': {1j, (1+2j)}} actual: TypeError: '<' not supported between instances of 'complex' and 'complex' expected: {1j, (1+2j)}
```

Judge: BUG (medium) -- The reproducer uses valid, hashable complex keys with distinct integer sorting ranks and verifies successful SortedDict construction. The documented set-like intersection should work on those keys; instead, it attempts to compare complex keys directly, failing despite the supplied ordering function. The expected membership is correctly computed, and no duplicate is listed.

