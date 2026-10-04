*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `operator`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `operator`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: iconcat may bypass a list subclass's overridden __iadd__

Target: `operator.iconcat`

Property: For list subclasses whose __iadd__ deterministically returns a list, operator.iconcat(a, b) must produce the same result and mutations as executing a += b on an independently constructed equivalent operand, with b a plain list.

### Draft issue: operator.iconcat ignores list subclass __iadd__ override

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `operator`

**Documented behaviour:** "Same as a += b, for a and b sequences." — supplied public API and iconcat docstring.

**Expected:** Return the fresh plain list [99], leaving both original operands unchanged.

**Actual:** Returns the fresh plain list [1, 2], leaving both original operands unchanged.

**Reproducer:**

```python
import operator

class L(list):
    def __iadd__(self, other):
        return [99]

a, ref, b, rb = L([1]), L([1]), [2], [2]
data = {"mode": "fresh99", "initial": list(a), "rhs": list(b)}

def snapshot(result, original, rhs):
    return {
        "result": list(result),
        "result_type": type(result).__name__,
        "original_after": list(original),
        "rhs_after": list(rhs),
        "result_is_original": result is original,
    }

if not (isinstance(a, list) and type(b) is list
        and type(a.__iadd__(b)) is list and a == [1] and b == [2]):
    print("REFUTATION REJECTED:", "input does not satisfy the claimed domain")
else:
    actual = snapshot(operator.iconcat(a, b), a, b)
    original = ref
    ref += rb
    expected = snapshot(ref, original, rb)
    if actual != expected:
        print("REFUTATION CONFIRMED:", data, actual, expected)
    else:
        print("REFUTATION REJECTED:", "iconcat agrees with independently executed +=")
```

**Output:**

```
REFUTATION CONFIRMED: {'mode': 'fresh99', 'initial': [1], 'rhs': [2]} {'result': [1, 2], 'result_type': 'list', 'original_after': [1], 'rhs_after': [2], 'result_is_original': False} {'result': [99], 'result_type': 'list', 'original_after': [1], 'rhs_after': [2], 'result_is_original': False}
```

Judge: BUG (medium) -- The documented equivalence to += applies to these valid sequence operands. The deterministic __iadd__ returns a plain list, and the independently constructed reference correctly captures both the result and operand mutations. operator.iconcat instead bypasses the override and concatenates the underlying list contents. No duplicate or existing fix was identified.

