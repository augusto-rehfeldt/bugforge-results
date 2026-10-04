*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `heapq`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `heapq`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: merge silently suppresses StopIteration raised by a key function

Target: `heapq.merge`

Property: For finite integer lists sorted in ascending order and a key callable that raises StopIteration on an encountered element, consuming merge(*lists, key=key) must fail rather than terminate successfully with elements silently omitted. Accept StopIteration or RuntimeError caused by StopIteration, accounting for generator exception conversion.

### Draft issue: heapq.merge silently drops an input stream when key raises StopIteration

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `heapq`

**Documented behaviour:** heapq.merge docstring: "Similar to sorted(itertools.chain(*iterables)) but returns a generator" and "If *key* is not None, applies a key function to each element to determine its sort order." sorted propagates an exception from the key function instead of silently discarding input.

**Expected:** Consumption raises StopIteration or RuntimeError caused by StopIteration.

**Actual:** Consumption succeeds with [2, 4], silently omitting 1 and 3.

**Reproducer:**

```python
import heapq
from itertools import chain

data = {"lists": [[1, 3], [2, 4]], "raise_StopIteration_on": 1}
lists = data["lists"]

def key(x):
    if x == data["raise_StopIteration_on"]:
        raise StopIteration
    return x

def outcome(f):
    try:
        return ("result", f())
    except Exception as e:
        if isinstance(e, RuntimeError) and isinstance(e.__cause__, StopIteration):
            e = e.__cause__
        return ("exception", type(e).__name__)

if not all(isinstance(xs, list) and all(type(x) is int for x in xs)
           and xs == sorted(xs) for xs in lists):
    print("REFUTATION REJECTED:", "input is not ascending integer lists")
else:
    actual = outcome(lambda: list(heapq.merge(*lists, key=key)))
    expected = outcome(lambda: sorted(chain.from_iterable(lists), key=key))
    if expected == ("exception", "StopIteration") and actual[0] == "result":
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "no silent successful omission demonstrated",
              data, "actual:", actual, "expected:", expected)
```

**Output:**

```
REFUTATION CONFIRMED: {'lists': [[1, 3], [2, 4]], 'raise_StopIteration_on': 1} actual: ('result', [2, 4]) expected: ('exception', 'StopIteration')
```

Judge: BUG (medium) -- The reproducer uses valid ascending integer lists and correctly distinguishes an exception from successful consumption. heapq.merge catches StopIteration from the key callable as though the input iterator were exhausted, silently discarding the entire [1, 3] stream. A key failure is not iterator exhaustion; this violates the documented merge and key semantics. The listed optimization issue does not establish a duplicate, and the upstream diff does not change merge.

