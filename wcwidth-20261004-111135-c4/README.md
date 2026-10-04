*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `wcwidth`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `wcwidth` 0.9.1

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Boundary lookup must preserve regional-indicator pairing context

Target: `wcwidth.grapheme_boundary_before`

Property: For a string consisting of an even number of regional-indicator characters, grapheme clusters are consecutive pairs. For every odd position pos with 1 <= pos < len(text), grapheme_boundary_before(text, pos) must equal pos - 1, the start of the pair containing that position.

### Draft issue: grapheme_boundary_before returns a non-boundary inside a long regional-indicator run

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `wcwidth` 0.9.1

**Documented behaviour:** "Find the grapheme cluster boundary immediately before a position." — public API documentation for grapheme_boundary_before.

**Expected:** grapheme_boundary_before(text, 51) returns 50.

**Actual:** grapheme_boundary_before(text, 51) returns 49.

**Reproducer:**

```python
import unicodedata
from wcwidth import grapheme_boundary_before

text = ''.join(chr(c) for c in range(0x1F1FF, 0x1F1E5, -1)) * 2
pos = 51
if not (0 < pos < len(text) and pos % 2 and len(text) % 2 == 0
        and all(unicodedata.name(c).startswith('REGIONAL INDICATOR SYMBOL LETTER ') for c in text)):
    print('REFUTATION REJECTED:', 'invalid input')
else:
    # Unicode grapheme rule GB12/GB13 pairs consecutive regional indicators.
    expected = max(range(0, pos, 2))
    try:
        actual = grapheme_boundary_before(text, pos)
    except Exception as e:
        print('REFUTATION REJECTED:', 'reported result not reproduced:', repr(e))
    else:
        if actual != expected:
            print('REFUTATION CONFIRMED:', repr((text, pos)), 'actual:', actual, 'expected:', expected)
        else:
            print('REFUTATION REJECTED:', 'actual matches expected:', actual)
```

**Output:**

```
REFUTATION CONFIRMED: ('🇿🇾🇽🇼🇻🇺🇹🇸🇷🇶🇵🇴🇳🇲🇱🇰🇯🇮🇭🇬🇫🇪🇩🇨🇧🇦🇿🇾🇽🇼🇻🇺🇹🇸🇷🇶🇵🇴🇳🇲🇱🇰🇯🇮🇭🇬🇫🇪🇩🇨🇧🇦', 51) actual: 49 expected: 50
```

Judge: BUG (medium) -- The reproducer constructs 52 valid regional-indicator characters. Unicode grapheme rules GB12/GB13 group the uninterrupted run into pairs starting at even indices. Position 51 is inside the final pair, whose preceding boundary is 50; index 49 is not a grapheme boundary. The reported result therefore violates the documented boundary-finding behavior. No duplicate or documented limitation is identified.

