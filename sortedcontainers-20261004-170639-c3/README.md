*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `sortedcontainers`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `sortedcontainers` 2.4.0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: SortedSet.pop can leave a removed value in its membership set

Target: `sortedcontainers.SortedSet.pop`

Property: For a SortedSet of immutable, totally ordered objects whose hashes are stable integers whenever hashing succeeds, if pop() raises because the selected object's __hash__ temporarily raises ValueError, then, after hashing is restored, membership and iteration must still agree: for every original value v, (v in s) == any(v == x for x in s).

### Draft issue: SortedSet.pop leaves set and list inconsistent when hashing raises

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `sortedcontainers` 2.4.0

**Documented behaviour:** “Sorted set uses a set for set-operations and maintains a sorted list of values.” — SortedSet class documentation. These representations must describe the same set.

**Expected:** After pop raises and hashing is restored, membership and iteration describe the same set, preferably with the failed removal leaving the value present in both representations.

**Actual:** pop raises ValueError; iteration is empty, but the original value remains a member.

**Reproducer:**

```python
try:
    from sortedcontainers import SortedSet

    failing = False

    class V(int):
        __slots__ = ()

        def __hash__(self):
            if failing:
                raise ValueError("temporary hash failure")
            return int.__hash__(self)

    v = V(0)  # Immutable and totally ordered; successful hashes are stable integers.
    data = {"values": [0], "pop_index": 0}
    s = SortedSet([v])
    if not (type(hash(v)) is int and hash(v) == hash(v)
            and list(s) == [v] and v in s and v <= v):
        raise RuntimeError("invalid initial input")

    failing = True
    raised = False
    try:
        s.pop(0)
    except ValueError:
        raised = True
    finally:
        failing = False

    items = list(s)
    comparisons = [(int(v), v in s, any(v == x for x in items))]
    actual = {
        "raised_ValueError": raised,
        "iteration": list(map(int, items)),
        "membership_equals_iteration": [(n, a == b) for n, a, b in comparisons],
        "comparisons": comparisons,
    }
    # Independently require the set and list representations to agree.
    expected = {"membership_equals_iteration": [(int(v), True)]}
    if raised and actual["membership_equals_iteration"] != expected["membership_equals_iteration"]:
        print("REFUTATION CONFIRMED:", data, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "no ValueError or representations agree", actual)
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: {'values': [0], 'pop_index': 0} actual: {'raised_ValueError': True, 'iteration': [], 'membership_equals_iteration': [(0, False)], 'comparisons': [(0, True, False)]} expected: {'membership_equals_iteration': [(0, True)]}
```

Judge: BUG (medium) -- The input is immutable and totally ordered, and every successful hash is stable. A temporary hashing exception does not change its hash value. The output demonstrates corruption of the documented set/list representation invariant: pop removes the value from the sorted list before set removal fails, leaving membership and iteration inconsistent after hashing is restored. This is an exception-safety bug, not merely an expectation that pop must succeed. No duplicate was supplied.

