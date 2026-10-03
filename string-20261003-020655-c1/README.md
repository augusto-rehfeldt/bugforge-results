*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `string`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `string`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: capwords ignores an explicitly supplied falsey string separator

Target: `string.capwords`

Property: For every string s and nonempty string separator sep, including str subclasses, capwords(s, sep) must equal sep.join(map(str.capitalize, s.split(sep))).

### Draft issue: string.capwords ignores falsey nonempty str subclasses when joining

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `string`

**Documented behaviour:** The capwords docstring states: "otherwise sep is used to split and join the words." This applies when the optional sep argument is neither absent nor None.

**Expected:** 'A|B'

**Actual:** 'A B'

**Reproducer:**

```python
import string

class FalseySep(str):
    def __bool__(self):
        return False

s, sep = 'a|b', FalseySep('|')
if not (isinstance(s, str) and isinstance(sep, str) and len(sep) > 0):
    print('REFUTATION REJECTED:', 'invalid input')
else:
    actual = string.capwords(s, sep)
    expected = str.join(sep, map(str.capitalize, str.split(s, sep)))
    if actual != expected:
        print('REFUTATION CONFIRMED:', {'s': s, 'sep': sep, 'sep_class': type(sep).__name__},
              'actual:', repr(actual), 'expected:', repr(expected))
    else:
        print('REFUTATION REJECTED:', 'actual matches documented expectation')
```

**Output:**

```
REFUTATION CONFIRMED: {'s': 'a|b', 'sep': '|', 'sep_class': 'FalseySep'} actual: 'A B' expected: 'A|B'
```

Judge: BUG (low) -- The separator is a valid nonempty str subclass. The documentation distinguishes None from a supplied separator, not falsey from truthy separators. The reproducer correctly computes the expected result: splitting uses '|', but capwords substitutes a space when joining because the separator is falsey. The listed issue and PR concern map versus a generator expression, not this behavior; the supplied upstream diff contains no capwords fix.

