*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `sortedcontainers`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `sortedcontainers` 2.4.0

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Failed setdefault leaves a key missing from sorted views

Target: `sortedcontainers.SortedDict.setdefault`

Property: For a SortedDict with integer keys and a key function, if setdefault(k, value) raises while evaluating the key function, its underlying dictionary and sorted keys view must remain consistent: list(d.keys()) must equal sorted(dict.keys(d), key=key) after the key function resumes normal operation.

### Draft issue: SortedDict.setdefault leaves keys inconsistent when the key function raises

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `sortedcontainers` 2.4.0

**Documented behaviour:** "Sorted dict keys are maintained in sorted order." — SortedDict class documentation.

**Expected:** After the exception, the dictionary and sorted keys view remain consistent; preferably key 1 is not inserted.

**Actual:** list(d.keys()) is [0], while sorted(dict.keys(d), key=key) is [0, 1].

**Reproducer:**

```python
from sortedcontainers import SortedDict

case = {'initial_keys': [0], 'absent_key': 1, 'value': 'value'}
failing = False

def key(k):
    if failing and k == case['absent_key']:
        raise RuntimeError('key evaluation failed')
    return k

d = SortedDict(key, {k: None for k in case['initial_keys']})
if (not all(type(k) is int for k in case['initial_keys'] + [case['absent_key']])
        or case['absent_key'] in d
        or list(d.keys()) != sorted(dict.keys(d), key=key)):
    print('REFUTATION REJECTED: invalid input or initial ordering')
else:
    failing = True
    raised = False
    try:
        d.setdefault(case['absent_key'], case['value'])
    except RuntimeError:
        raised = True
    finally:
        failing = False
    actual = list(d.keys())
    expected = sorted(dict.keys(d), key=key)
    if raised and actual != expected:
        print('REFUTATION CONFIRMED:', case, 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED:', 'no key-function exception' if not raised
              else 'dictionary and sorted keys remain consistent')
```

**Output:**

```
REFUTATION CONFIRMED: {'initial_keys': [0], 'absent_key': 1, 'value': 'value'} actual: [0] expected: [0, 1]
```

Judge: BUG (medium) -- The reproducer starts with valid integer keys and a consistent SortedDict. The key function raises only for an absent key, so it does not change the ordering of any stored key. After setdefault raises and normal key evaluation resumes, the underlying dictionary contains key 1 but the sorted keys view omits it. This breaks the documented maintained-key invariant, not merely an expectation of exception atomicity. The listed type-annotation PR is unrelated.

