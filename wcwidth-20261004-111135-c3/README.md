*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `wcwidth`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `wcwidth` 0.9.1

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Reverse grapheme iteration must reverse the forward cluster sequence

Target: `wcwidth.iter_graphemes_reverse`

Property: For every Unicode string s, list(wcwidth.iter_graphemes_reverse(s)) must equal list(reversed(list(wcwidth.iter_graphemes(s)))) when both functions use their default bounds.

### Draft issue: iter_graphemes_reverse missegments a 31-regional-indicator run followed by a combining mark

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `wcwidth` 0.9.1

**Documented behaviour:** "Iterate over grapheme clusters in reverse order (last to first)." — public API documentation for iter_graphemes_reverse.

**Expected:** 17 clusters: the final '🇪́', followed by the 15 left-paired regional-indicator clusters in reverse order, then '\r\n'.

**Actual:** 18 clusters: after '🇪́', an erroneous standalone '🇩' and shifted regional-indicator pairs, ending with standalone '🇦' and '\r\n'.

**Reproducer:**

```python
import wcwidth

r = ''.join(chr(0x1F1E6 + i % 26) for i in range(31))
s = '\r\n' + r + '\u0301'
if not isinstance(s, str) or any(0xD800 <= ord(c) <= 0xDFFF for c in s):
    print('REFUTATION REJECTED: input is not a Unicode scalar string')
else:
    # CRLF is one cluster; regional indicators pair from the left;
    # the combining acute joins the final cluster.
    clusters = ['\r\n'] + [r[i:i+2] for i in range(0, len(r), 2)]
    clusters[-1] += '\u0301'
    expected = clusters[::-1]
    try:
        actual = list(wcwidth.iter_graphemes_reverse(s))
    except Exception as e:
        actual = f'{type(e).__name__}: {e}'
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), repr(actual), repr(expected))
    else:
        print('REFUTATION REJECTED: reverse iteration matches independent grapheme segmentation')
```

**Output:**

```
REFUTATION CONFIRMED: '\r\n🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿🇦🇧🇨🇩🇪́' ['🇪́', '🇩', '🇧🇨', '🇿🇦', '🇽🇾', '🇻🇼', '🇹🇺', '🇷🇸', '🇵🇶', '🇳🇴', '🇱🇲', '🇯🇰', '🇭🇮', '🇫🇬', '🇩🇪', '🇧🇨', '🇦', '\r\n'] ['🇪́', '🇨🇩', '🇦🇧', '🇾🇿', '🇼🇽', '🇺🇻', '🇸🇹', '🇶🇷', '🇴🇵', '🇲🇳', '🇰🇱', '🇮🇯', '🇬🇭', '🇪🇫', '🇨🇩', '🇦🇧', '\r\n']
```

Judge: BUG (medium) -- The input is a valid Unicode scalar string. CRLF forms one cluster, regional indicators pair from the left, and the combining acute attaches to the final unpaired indicator. The expected segmentation is correct. Reverse iteration instead introduces incorrect regional-indicator boundaries, violating the documented promise to iterate grapheme clusters from last to first. No duplicate or documented limitation is provided.

