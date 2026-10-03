*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `json`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `json`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Streaming and one-shot serialization disagree for false-valued nonempty dictionaries

Target: `json.dumps`

Property: For every dict subclass instance d containing ordinary string keys and JSON-serializable primitive values, whose only override is __bool__ returning False, json.dumps(d) must equal ''.join(json.JSONEncoder().iterencode(d)): both APIs serialize the same dictionary with identical default options.

### Draft issue: json.JSONEncoder.iterencode drops entries from dict subclasses with false truthiness

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `json`

**Documented behaviour:** json.dumps documentation: "Serialize obj to a JSON formatted str." JSONEncoder.iterencode documentation: "Encode the given object, o, and yield each string representation as available." Both describe serialization of the given object.

**Expected:** Both APIs return '{"a": 1}'.

**Actual:** json.dumps returns '{"a": 1}', while joined JSONEncoder.iterencode returns '{}'.

**Reproducer:**

```python
import json

class D(dict):
    def __bool__(self):
        return False

d = D(a=1)
if not all(type(k) is str and type(v) is int for k, v in d.items()):
    print("REFUTATION REJECTED: invalid input")
else:
    actual = json.dumps(d), ''.join(json.JSONEncoder().iterencode(d))
    reference = ''.join(json.JSONEncoder().iterencode(dict(d)))
    expected = reference, reference
    if actual != expected:
        print("REFUTATION CONFIRMED:", d, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: both APIs match the dictionary reference")
```

**Output:**

```
REFUTATION CONFIRMED: {'a': 1} actual: ('{"a": 1}', '{}') expected: ('{"a": 1}', '{"a": 1}')
```

Judge: BUG (medium) -- The input is a nonempty dict subclass with supported keys and values; overriding truthiness does not remove its entries. The reference correctly preserves those entries. The Python encoder treats false truthiness as emptiness and silently drops data, unlike json.dumps' accelerated encoder. The listed issues do not establish a duplicate of this specific truthiness bug, and the __init__.py comparison does not cover the encoder implementation.

