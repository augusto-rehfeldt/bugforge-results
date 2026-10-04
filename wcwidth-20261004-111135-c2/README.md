*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `wcwidth`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `wcwidth` 0.9.1

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Forward and reverse grapheme iteration must agree

Target: `wcwidth.iter_graphemes`

Property: For every string s composed of Unicode scalar values, list(iter_graphemes(s)) must equal list(reversed(list(iter_graphemes_reverse(s)))) when both functions use their default bounds.

### Draft issue: Forward and reverse grapheme iterators disagree for regional indicators followed by ZWJ

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `wcwidth` 0.9.1

**Documented behaviour:** The supplied public API describes iter_graphemes_reverse as: "Iterate over grapheme clusters in reverse order (last to first)." Reversing traversal must preserve the grapheme clusters yielded by iter_graphemes.

**Expected:** Forward traversal and reversed reverse traversal yield identical grapheme clusters.

**Actual:** Forward traversal ends with '🇩🇪\u200d', while reversed reverse traversal ends with separate '🇩' and '🇪\u200d' clusters.

**Reproducer:**

```python
from wcwidth import iter_graphemes, iter_graphemes_reverse

s = "\r\n" + "".join(chr(0x1F1E6 + i % 26) for i in range(31)) + "\u200d"
if any(0xD800 <= ord(c) <= 0xDFFF for c in s):
    print("REFUTATION REJECTED: input contains non-scalar values")
else:
    actual = list(iter_graphemes(s))
    expected = list(reversed(list(iter_graphemes_reverse(s))))
    if actual != expected:
        print("REFUTATION CONFIRMED:", repr(s), actual, expected)
    else:
        print("REFUTATION REJECTED: forward and reversed reverse traversal agree")
```

**Output:**

```
REFUTATION CONFIRMED: '\r\n🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿🇦🇧🇨🇩🇪\u200d' ['\r\n', '🇦', '🇧🇨', '🇩🇪', '🇫🇬', '🇭🇮', '🇯🇰', '🇱🇲', '🇳🇴', '🇵🇶', '🇷🇸', '🇹🇺', '🇻🇼', '🇽🇾', '🇿🇦', '🇧🇨', '🇩🇪\u200d'] ['\r\n', '🇦', '🇧🇨', '🇩🇪', '🇫🇬', '🇭🇮', '🇯🇰', '🇱🇲', '🇳🇴', '🇵🇶', '🇷🇸', '🇹🇺', '🇻🇼', '🇽🇾', '🇿🇦', '🇧🇨', '🇩', '🇪\u200d']
```

Judge: BUG (medium) -- The input contains only Unicode scalar values, and both iterators use default bounds. Reversing the reverse iterator's output correctly compares cluster boundaries independently of traversal order. The documented reverse traversal promises grapheme clusters in last-to-first order, not different segmentation. The reproduced outputs disagree on the final cluster, violating that promise. No duplicate was supplied.

