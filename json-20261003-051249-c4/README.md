*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `json`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `json`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Falsey callable parse_float is silently ignored

Target: `json.loads`

Property: For every valid JSON document consisting of a single finite floating-point number and every callable parse_float object supplied explicitly, loads must call that object with the number's exact textual representation and return its result, even when bool(parse_float) is False.

### Draft issue: json.loads ignores explicitly supplied false-valued parse_float callables

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `json`

**Documented behaviour:** json.loads docstring: "``parse_float``, if specified, will be called with the string of every JSON float to be decoded."

**Expected:** Call hook('1.5') exactly once and return '<sentinel>'.

**Actual:** Returns 1.5 without calling the hook.

**Reproducer:**

```python
import json, math, re

class FalseBool:
    def __init__(self):
        self.calls = []
    def __bool__(self):
        return False
    def __call__(self, text):
        self.calls.append(text)
        return "<sentinel>"

document, hook = "1.5", FalseBool()
if not (re.fullmatch(r"-?(?:0|[1-9][0-9]*)\.[0-9]+", document)
        and math.isfinite(float(document)) and callable(hook) and not bool(hook)):
    print("REFUTATION REJECTED:", "invalid input or hook")
else:
    expected = {"result": "<sentinel>", "calls": [document]}
    try:
        result = json.loads(document, parse_float=hook)
        actual = {"result": result, "calls": hook.calls}
    except Exception as error:
        actual = {"exception": repr(error), "calls": hook.calls}
    if actual != expected:
        print("REFUTATION CONFIRMED:",
              {"document": document, "parse_float": "FalseBool"},
              "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "actual matches documented expectation")
```

**Output:**

```
REFUTATION CONFIRMED: {'document': '1.5', 'parse_float': 'FalseBool'} actual: {'result': 1.5, 'calls': []} expected: {'result': '<sentinel>', 'calls': ['1.5']}
```

Judge: BUG (medium) -- The reproducer uses valid JSON and an explicitly supplied callable. The documented hook contract does not require the callable to be truthy. The output shows the hook was silently ignored, violating that contract. None of the listed issues addresses false-valued parse_float callables, and the supplied upstream diff does not demonstrate a fix.

