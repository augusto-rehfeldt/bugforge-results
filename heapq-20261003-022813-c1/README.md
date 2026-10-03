*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `heapq`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `heapq`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: merge assumes every iterator's __next__ has __self__

Target: `heapq.merge`

Property: For any finite iterator yielding totally ordered integers in ascending order, list(heapq.merge(iterator)) must equal the sequence yielded by that iterator, without raising an exception. This includes valid iterators whose __next__ is a staticmethod or callable object without a __self__ attribute.

### Draft issue: heapq.merge fails for valid iterators whose __next__ has no __self__

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `heapq`

**Documented behaviour:** heapq.merge docstring: "Merge multiple sorted inputs into a single sorted output." It further states that it "assumes that each of the input streams is already sorted (smallest to largest)."

**Expected:** [0]

**Actual:** AttributeError: 'function' object has no attribute '__self__'

**Reproducer:**

```python
import heapq

def stream():
    values = iter([0])
    class I:
        def __iter__(self):
            return self
        __next__ = staticmethod(lambda: next(values))
    return I()

x = stream()
expected = list(x)
if iter(x) is not x or not all(type(v) is int for v in expected) or expected != sorted(expected):
    print("REFUTATION REJECTED: invalid input")
else:
    try:
        actual = list(heapq.merge(stream()))
    except Exception as e:
        actual = {"exception": type(e).__name__, "message": str(e)}
    if actual != expected:
        print("REFUTATION CONFIRMED:", "input:", expected, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual equals expected")
```

**Output:**

```
REFUTATION CONFIRMED: input: [0] actual: {'exception': 'AttributeError', 'message': "'function' object has no attribute '__self__'"} expected: [0]
```

Judge: BUG (low) -- The reproducer supplies a valid iterator: iter(x) is x, and its staticmethod __next__ yields the sorted integer sequence [0] before raising StopIteration. The expectation is computed correctly from a fresh equivalent iterator. heapq.merge accepts sorted iterables without requiring __next__ to be a bound method, but its remaining-input optimization assumes next.__self__ exists. That undocumented assumption causes the exception. The supplied upstream diff does not change merge, and the listed optimization issue does not establish that this defect is already reported or fixed.

