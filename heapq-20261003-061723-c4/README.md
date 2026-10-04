*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `heapq`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `heapq`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: nsmallest may violate sorted() stability for ordering-equivalent objects

Target: `heapq.nsmallest`

Property: For a finite list xs of objects whose __lt__ compares integer priorities and whose equality is identity-based, and integer n with 0 < n < len(xs), nsmallest(n, xs) must return the same object identities in the same order as sorted(xs)[:n], including stable selection among equal priorities.

### Draft issue: heapq.nsmallest violates sorted equivalence for ordering-equivalent objects with identity equality

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `heapq`

**Documented behaviour:** The nsmallest docstring states: "Equivalent to: sorted(iterable, key=key)[:n]". Python's sorting documentation guarantees that sorts are stable.

**Expected:** ['e', 'a', 'b', 'c'], with exactly those object identities in that order

**Actual:** ['e', 'a', 'd', 'b']

**Reproducer:**

```python
import heapq

class Item:
    def __init__(self, name, priority):
        self.name, self.priority = name, priority
    def __lt__(self, other):
        return self.priority < other.priority

data = [('a', 1), ('b', 1), ('c', 1), ('d', 1), ('e', 0)]
xs = [Item(*pair) for pair in data]
n = 4

if not (type(n) is int and 0 < n < len(xs)
        and all(type(x.priority) is int for x in xs)
        and all((x == y) == (x is y)
                and (x < y) == (x.priority < y.priority)
                for x in xs for y in xs)):
    print("REFUTATION REJECTED: invalid input")
else:
    actual = heapq.nsmallest(n, xs)
    expected = sorted(xs)[:n]
    if len(actual) != len(expected) or any(
            a is not e for a, e in zip(actual, expected)):
        print("REFUTATION CONFIRMED:",
              {'n': n, 'xs': data},
              "actual:", [x.name for x in actual],
              "expected:", [x.name for x in expected])
    else:
        print("REFUTATION REJECTED: actual matches sorted(xs)[:n] by identity and order")
```

**Output:**

```
REFUTATION CONFIRMED: {'n': 4, 'xs': [('a', 1), ('b', 1), ('c', 1), ('d', 1), ('e', 0)]} actual: ['e', 'a', 'd', 'b'] expected: ['e', 'a', 'b', 'c']
```

Judge: BUG (medium) -- The input is valid: __lt__ consistently orders integer priorities, and sorting does not require equality to agree with ordering equivalence. The documented equivalence to sorted(xs)[:n] promises stable tie selection. nsmallest decorates elements with tuple tie-breakers, but identity-based equality prevents those tie-breakers from being used for distinct equal-priority objects. It consequently selects and orders the wrong tied objects. Neither listed report covers this behaviour, and the upstream changes leave the cause intact.

