*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `unicodedata`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `unicodedata`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Unicode 3.2 normalization must treat subsequently assigned combining marks as unassigned starters

Target: `unicodedata.UCD.normalize`

Property: For u = unicodedata.ucd_3_2_0, choose characters x and y such that u.category(x) == 'Cn', u.combining(x) == 0, u.decomposition(x) == '', u.combining(y) > 0, and u.decomposition(y) == ''. Then u.normalize('NFD', 'a' + x + y) must equal 'a' + x + y: in Unicode 3.2, x is a starter, so canonical ordering cannot move y across it.

### Draft issue: unicodedata.ucd_3_2_0.normalize incorrectly reorders marks across Unicode 3.2 unassigned characters

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `unicodedata`

**Documented behaviour:** The unicodedata documentation states: "Return the normal form form for the Unicode string unistr." Its ucd_3_2_0 entry states: "This is an object that has the same methods as the entire module, but uses the Unicode database version 3.2 instead". Unicode canonical ordering, referenced by the normalization documentation, does not reorder combining characters across a character with canonical combining class zero.

**Expected:** u.normalize('NFD', 'a\u1ab0\u0316') returns 'a\u1ab0\u0316'.

**Actual:** Returns 'a\u0316\u1ab0', moving U+0316 across a Unicode 3.2 starter.

**Reproducer:**

```python
import unicodedata as ud

u = ud.ucd_3_2_0
x, y = '\u1ab0', '\u0316'
s = 'a' + x + y
if not (u.category(x) == 'Cn' and u.combining(x) == 0
        and u.decomposition(x) == '' and u.combining(y) > 0
        and u.decomposition(y) == '' and u.decomposition('a') == ''
        and u.combining('a') == 0):
    print('REFUTATION REJECTED: input does not satisfy the premises')
else:
    ref = []
    for c in s:
        ref.append(c)
        i = len(ref) - 1
        while i and 0 < u.combining(ref[i]) < u.combining(ref[i - 1]):
            ref[i - 1], ref[i] = ref[i], ref[i - 1]
            i -= 1
    expected = ''.join(ref)
    actual = u.normalize('NFD', s)
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), 'actual =', repr(actual),
              'expected =', repr(expected))
    else:
        print('REFUTATION REJECTED: actual matches documented expectation')
```

**Output:**

```
REFUTATION CONFIRMED: 'a̖᪰' actual = 'a̖᪰' expected = 'a̖᪰'
```

Judge: BUG (medium) -- The premises are satisfied: U+1AB0 is unassigned with combining class zero in Unicode 3.2, while U+0316 has a positive combining class. Neither character requires decomposition. Canonical ordering must not move U+0316 across that zero-class boundary. The reported result violates the documented use of the Unicode 3.2 database and is consistent with normalization incorrectly using a newer combining class for U+1AB0. Neither listed issue reports or fixes this behaviour.

