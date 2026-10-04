*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `wcwidth`

Python 3.14.6 (Windows-11-10.0.26220-SP0), `wcwidth` 0.9.1

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Wrapping must account for OSC 66 text-scaling width

Target: `wcwidth.wrap`

Property: For integers scale >= 2, 1 <= k, W >= scale*k, and 0 <= p < W, construct sized = TextSizing(TextSizingParams(scale=scale), 'x'*k, '\x07').make_sequence() and text = 'a'*p + ' ' + sized. Every line returned by wrap(text, width=W, break_long_words=True) must satisfy width(line) <= W. The sized segment itself fits within W, so satisfying the width bound does not require splitting that segment.

### Draft issue: wrap exceeds requested width when wrapping an OSC 66 text-sizing segment

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), `wcwidth` 0.9.1

**Documented behaviour:** "Wrap text to fit within given width, returning a list of wrapped lines." — public API documentation for wrap.

**Expected:** Return separate lines for 'a' and the intact sized segment, each no wider than 2 columns.

**Actual:** Returns one line containing 'a' immediately followed by the sized segment, with display width 3.

**Reproducer:**

```python
try:
    import wcwidth

    scale, k, W, p = 2, 1, 2, 1
    sized = f'\x1b]66;s={scale};{"x" * k}\x07'
    text = 'a' * p + ' ' + sized
    case = dict(text=text, width=W, break_long_words=True)

    if not (scale >= 2 and k >= 1 and W >= scale * k and 0 <= p < W):
        raise ValueError("input violates the stated validity constraints")

    lines = wcwidth.wrap(**case)
    widths = []
    for line in lines:
        plain = line.replace(sized, '')
        if any(c not in 'a ' for c in plain):
            raise ValueError("output contains characters this independent oracle cannot measure")
        widths.append(len(plain) + line.count(sized) * scale * k)

    if any(n > W for n in widths):
        print("REFUTATION CONFIRMED:", case,
              {"lines": lines, "reference_widths": widths},
              {"every_line_width_at_most": W})
    else:
        print("REFUTATION REJECTED: every returned line fits", widths)
except Exception as e:
    print("REFUTATION REJECTED:", type(e).__name__, str(e))
```

**Output:**

```
REFUTATION CONFIRMED: {'text': 'a \x1b]66;s=2;x\x07', 'width': 2, 'break_long_words': True} {'lines': ['a\x1b]66;s=2;x\x07'], 'reference_widths': [3]} {'every_line_width_at_most': 2}
```

Judge: BUG (medium) -- The valid input contains one ordinary column followed by a space and an OSC 66 segment occupying two columns. The returned line removes the space but combines both segments, producing three columns at width=2. This violates wrap's documented width bound; the sized segment fits intact on a separate line, so no unsupported splitting is required. No matching issue or pull request was supplied.

