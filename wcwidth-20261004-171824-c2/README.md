*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `wcwidth`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `wcwidth` 0.9.1

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: A leading Indic virama must not join a following consonant

Target: `wcwidth.iter_graphemes`

Property: For every integer k >= 1, let s = '\u094d' * k + '\u0915' (Devanagari viramas followed by KA). list(iter_graphemes(s)) must equal ['\u094d' * k, '\u0915']. Under Unicode extended grapheme rules, GB9c requires an earlier Indic consonant before the linker; leading linkers alone cannot suppress the boundary before KA.

### Draft issue: iter_graphemes incorrectly joins a leading Devanagari virama to a consonant

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `wcwidth` 0.9.1

**Documented behaviour:** The grapheme API describes its units as “grapheme clusters” (public grapheme API documentation; the supplied description of iter_graphemes_reverse likewise says “Iterate over grapheme clusters in reverse order (last to first).”). The Unicode extended grapheme-cluster definition, specifically GB9c, requires an initial InCB=Consonant in the conjunct pattern.

**Expected:** list(iter_graphemes('\u094d\u0915')) == ['\u094d', '\u0915']

**Actual:** list(iter_graphemes('\u094d\u0915')) == ['\u094d\u0915']

**Reproducer:**

```python
from wcwidth import iter_graphemes

s = '\u094d' + '\u0915'
if not isinstance(s, str) or any(0xD800 <= ord(c) <= 0xDFFF for c in s):
    print('REFUTATION REJECTED: input is not a Unicode scalar string')
else:
    # U+094D: Extend, InCB=Linker; U+0915: InCB=Consonant.
    # GB9c cannot apply without an earlier consonant; GB999 splits.
    expected = ['\u094d', '\u0915']
    try:
        actual = list(iter_graphemes(s))
    except Exception as e:
        print('REFUTATION REJECTED: no cluster result:', repr(e))
    else:
        if actual != expected:
            print('REFUTATION CONFIRMED:', repr(s), repr(actual), repr(expected))
        else:
            print('REFUTATION REJECTED: result matches Unicode grapheme rules')
```

**Output:**

```
REFUTATION CONFIRMED: '्क' ['्क'] ['्', 'क']
```

Judge: BUG (medium) -- The reproducer uses valid Unicode scalars and demonstrates incorrect grapheme segmentation. GB9c requires an earlier InCB=Consonant; a leading virama cannot satisfy that requirement. No other no-break rule applies before KA, so GB999 requires a boundary. Returning one cluster violates the documented grapheme-cluster semantics. The supplied issue concerns emoji display widths and is unrelated.

