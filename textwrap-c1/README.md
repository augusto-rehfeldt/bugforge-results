*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `textwrap`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `textwrap`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `doc-bug`: Indentation can violate the documented maximum line width

Target: `textwrap.TextWrapper.wrap`

Property: For every positive integer width, every text string containing only ASCII letters, and initial_indent and subsequent_indent strings containing only spaces, TextWrapper(width=width, initial_indent=initial_indent, subsequent_indent=subsequent_indent, break_long_words=True).wrap(text) must return lines whose lengths are all at most width.

### Draft issue: Clarify TextWrapper width guarantees when indentation consumes the available width

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `textwrap`

**Documented behaviour:** TextWrapper.wrap docstring: "Reformat the single paragraph in 'text' so it fits in lines of no more than 'self.width' columns." TextWrapper class documentation also states that initial_indent "Counts towards the line's width" and subsequent_indent "also counts towards each line's width."

**Expected:** Documentation should qualify the width guarantee when indentation leaves no room for text.

**Actual:** wrap('a') returns [' a'], whose length is 2 despite width=1.

**Reproducer:**

```python
import textwrap

case = dict(width=1, text="a", initial_indent=" ", subsequent_indent="")
w, text = case["width"], case["text"]
valid = (
    type(w) is int and w > 0
    and isinstance(text, str)
    and all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in text)
    and all(isinstance(case[k], str) and not case[k].strip(" ")
            for k in ("initial_indent", "subsequent_indent"))
)
if not valid:
    print("REFUTATION REJECTED:", "input is outside the documented domain")
else:
    wrapper = textwrap.TextWrapper(
        width=w, initial_indent=case["initial_indent"],
        subsequent_indent=case["subsequent_indent"], break_long_words=True)
    actual = wrapper.wrap(text)
    expected = f"Every returned line has length <= {w}"
    if any(len(line) > w for line in actual):
        print("REFUTATION CONFIRMED:", case, "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "all returned lines satisfy", expected)
```

**Output:**

```
REFUTATION CONFIRMED: {'width': 1, 'text': 'a', 'initial_indent': ' ', 'subsequent_indent': ''} actual: [' a'] expected: Every returned line has length <= 1
```

Judge: DOC_BUG (low) -- The reproducer is valid and its length check is correct, but the indent consumes the entire width, leaving no room for even one character. TextWrapper deliberately permits at least one character when indentation leaves no usable width, preserving text and ensuring progress. This is a reasonable fallback for incompatible constraints; the documentation's unqualified width guarantee should explain it. None of the listed issues covers this indentation case.

