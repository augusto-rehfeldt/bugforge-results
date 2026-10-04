*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `more_itertools`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `more_itertools` 11.1.0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: all_unique misses equal values across hashable and unhashable inputs

Target: `more_itertools.all_unique`

Property: For any finite iterable with key=None whose elements have well-defined Boolean equality, all_unique must return False whenever two distinct positions contain equal elements, including when one element is hashable and the other is unhashable.

### Draft issue: all_unique misses equal elements with mixed hashability

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `more_itertools` 11.1.0

**Documented behaviour:** The all_unique docstring states: "Returns ``True`` if all the elements of *iterable* are unique (no two elements are equal)."

**Expected:** all_unique([set(), frozenset()], key=None) returns False.

**Actual:** Returns True despite the two elements comparing equal.

**Reproducer:**

```python
try:
    from more_itertools import all_unique
    data = [set(), frozenset()]
    comparisons = [x == y for x in data for y in data]
    if not all(type(x) is bool for x in comparisons):
        raise ValueError("equality is not Boolean")
    expected = not any(data[i] == data[j]
                       for i in range(len(data)) for j in range(i))
    actual = all_unique(data, key=None)
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: result matches documented expectation")
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: [set(), frozenset()] actual: True expected: False
```

Judge: BUG (medium) -- The docstring explicitly promises that no two elements are equal. set() and frozenset() are valid inputs with Boolean equality and compare equal, despite differing hashability. The reproducer correctly computes False as the expected result, but all_unique returns True. The listed feature request does not report or fix this behaviour. The development branch was not checked.

