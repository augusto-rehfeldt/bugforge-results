*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `unicodedata`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `unicodedata`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Legacy normalization must treat post-3.2 combining marks as starters

Target: `unicodedata.UCD.is_normalized`

Property: For u = unicodedata.ucd_3_2_0, let m be a character unassigned in Unicode 3.2 with u.category(m) == 'Cn' and u.combining(m) == 0, but unicodedata.combining(m) > 0. The string s = 'A\u0315' + m is already in Unicode 3.2 NFD, so u.is_normalized('NFD', s) must return True: m is a class-zero boundary, not a combining mark that can reorder before U+0315.

### Draft issue: unicodedata.ucd_3_2_0.is_normalized incorrectly rejects NFD with a character unassigned in Unicode 3.2

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `unicodedata`

**Documented behaviour:** Python unicodedata documentation, unicodedata.is_normalized: "Return whether the Unicode string unistr is in the normal form form." The unicodedata.ucd_3_2_0 entry says: "This is an object that has the same methods as the entire module, but uses the Unicode database version 3.2 instead."

**Expected:** ucd_3_2_0.is_normalized('NFD', 'A\u0315\u1ab0') returns True.

**Actual:** Returns False despite the string being NFD under Unicode 3.2.

**Reproducer:**

```python
import unicodedata as ud

u = ud.ucd_3_2_0
m = '\u1ab0'
s = 'A\u0315' + m

if not (u.category(m) == 'Cn' and u.combining(m) == 0
        and ud.combining(m) > 0):
    print('REFUTATION REJECTED: input does not meet the stated premises')
else:
    # These characters are not Hangul syllables. NFD requires no canonical
    # decompositions and nondecreasing combining classes between class-zero boundaries.
    classes = [u.combining(c) for c in s]
    decomps = [u.decomposition(c) for c in s]
    expected = (
        all(not d or d.startswith('<') for d in decomps)
        and all(b == 0 or a <= b for a, b in zip(classes, classes[1:]))
    )
    actual = u.is_normalized('NFD', s)
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), actual, expected)
    else:
        print('REFUTATION REJECTED: actual agrees with independent Unicode 3.2 NFD check')
```

**Output:**

```
REFUTATION CONFIRMED: 'A᪰̕' False True
```

Judge: BUG (medium) -- ucd_3_2_0 explicitly promises Unicode 3.2 database semantics. The valid input has Unicode 3.2 combining classes [0, 232, 0] and no canonical decompositions, so it is NFD: the unassigned U+1AB0 is a class-zero boundary. Returning False violates that promise. The listed issue concerns unrelated regular-expression narrow/wide behavior and is not a duplicate.

