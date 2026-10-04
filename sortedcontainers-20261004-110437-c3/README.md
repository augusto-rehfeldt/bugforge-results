*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `sortedcontainers`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `sortedcontainers` 2.4.0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Items-view intersection fails for valid keys sorted by a custom key function

Target: `sortedcontainers.SortedItemsView`

Property: For a SortedDict whose keys and values are hashable, including keys ordered through a supplied key function rather than native comparison, intersecting its items view with itself must succeed and produce exactly the same members as set(d.items()).

### Draft issue: SortedItemsView intersection fails for keys ordered by a custom key function

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `sortedcontainers` 2.4.0

**Documented behaviour:** "Sorted items views are set-like and support set operations." — SortedItemsView documentation.

**Expected:** Self-intersection succeeds with exactly the members {((1+0j), 'a'), ((2+0j), 'b')}.

**Actual:** view & view raises TypeError: '<' not supported between instances of 'complex' and 'complex'.

**Reproducer:**

```python
from sortedcontainers import SortedDict

mapping = {1+0j: 'a', 2+0j: 'b'}
input_ = {'constructor': 'SortedDict(lambda k: k.real, mapping)', 'mapping': mapping}
try:
    expected = set(mapping.items())  # Independently verifies hashability.
    d = SortedDict(lambda k: k.real, mapping)
    if list(d) != sorted(mapping, key=lambda k: k.real) or set(d.items()) != expected:
        raise ValueError("construction did not preserve the mapping and key-function order")
except Exception as e:
    print("REFUTATION REJECTED:", "invalid input:", repr(e))
else:
    try:
        view = d.items()
        result = view & view
        actual = set(result)
        broken = actual != expected
    except Exception as e:
        actual = ('exception', type(e).__name__, str(e))
        broken = True
    if broken:
        print("REFUTATION CONFIRMED:", input_, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "self-intersection has exactly the expected members")
```

**Output:**

```
REFUTATION CONFIRMED: {'constructor': 'SortedDict(lambda k: k.real, mapping)', 'mapping': {(1+0j): 'a', (2+0j): 'b'}} actual: ('exception', 'TypeError', "'<' not supported between instances of 'complex' and 'complex'") expected: {((1+0j), 'a'), ((2+0j), 'b')}
```

Judge: BUG (medium) -- The input is valid: the supplied key function orders the complex keys, and all item pairs are hashable. The reproducer verifies construction and computes the expected members independently. Documented set-like intersection should preserve these members, but self-intersection attempts native comparison of complex keys and raises TypeError. No matching issue or pull request was found.

