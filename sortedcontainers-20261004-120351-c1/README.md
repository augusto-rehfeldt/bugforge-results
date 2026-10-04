*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `sortedcontainers`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `sortedcontainers` 2.4.0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Interrupted update can desynchronize SortedDict's mapping and sorted keys

Target: `sortedcontainers.SortedDict.update`

Property: For an initially empty SortedDict d, after calling d.update(pairs) and catching an exception raised by pairs after yielding valid integer-keyed pairs, list(d.keys()) must equal sorted(dict.keys(d)). This requires internal consistency, not rollback of partially inserted items.

### Draft issue: SortedDict.update leaves key index inconsistent when an input iterator raises

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `sortedcontainers` 2.4.0

**Documented behaviour:** "Sorted dict keys are maintained in sorted order." — SortedDict class documentation.

**Expected:** After the exception, list(d.keys()) equals sorted(dict.keys(d)); retaining the inserted pair would make both [1].

**Actual:** list(d.keys()) is [], while sorted(dict.keys(d)) is [1].

**Reproducer:**

```python
from sortedcontainers import SortedDict

pairs = [(1, 10)]
if not all(isinstance(p, tuple) and len(p) == 2 and type(p[0]) is int for p in pairs):
    print("REFUTATION REJECTED: invalid integer-keyed pairs")
else:
    error = RuntimeError("iterator failed")

    def source():
        yield from pairs
        raise error

    d = SortedDict()
    caught = None
    try:
        d.update(source())
    except Exception as exc:
        caught = exc

    actual = list(d.keys())
    expected = sorted(dict.keys(d))
    if caught is not error:
        print("REFUTATION REJECTED: expected iterator exception not caught")
    elif actual != expected:
        print("REFUTATION CONFIRMED:", pairs, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: keys remain consistent and sorted")
```

**Output:**

```
REFUTATION CONFIRMED: [(1, 10)] actual: [] expected: [1]
```

Judge: BUG (medium) -- The source yields a valid integer-keyed pair before raising, and the reproducer catches that exact exception. No rollback is required, but SortedDict must keep its sorted-key index consistent with its underlying dictionary. The output shows a stored key missing from the public keys view, violating the documented sorted-key representation. No matching issue or pull request was found.

