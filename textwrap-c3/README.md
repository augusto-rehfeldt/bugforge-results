*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `textwrap`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `textwrap`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `doc-bug`: Indentation can make filled lines exceed the documented maximum width

Target: `textwrap.TextWrapper.fill`

Property: For positive integer width, break_long_words=True, and nonempty ASCII word input, every line returned by TextWrapper.fill(text) must have length at most width, including any initial_indent or subsequent_indent.

### Draft issue: Clarify TextWrapper width guarantees when indentation leaves no room for text

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `textwrap`

**Documented behaviour:** TextWrapper.fill docstring: "Reformat the single paragraph in 'text' to fit in lines of no more than 'self.width' columns". TextWrapper attribute documentation also says initial_indent "Counts towards the line's width."

**Expected:** Document that lines may exceed width when indentation leaves no room for text.

**Actual:** fill('a') returns ' a', a two-character line with width=1.

**Reproducer:**

```python
import textwrap

case = dict(width=1, initial_indent=" ", subsequent_indent="", text="a")
text = case["text"]
if not (type(case["width"]) is int and case["width"] > 0
        and text and text.isascii() and text.isalpha()
        and all(isinstance(case[k], str) for k in ("initial_indent", "subsequent_indent"))):
    print("REFUTATION REJECTED:", "invalid input")
else:
    # The documentation places no upper bound on indent length.
    wrapper = textwrap.TextWrapper(
        width=case["width"], initial_indent=case["initial_indent"],
        subsequent_indent=case["subsequent_indent"], break_long_words=True)
    actual = wrapper.fill(text)
    expected = {"every_line_length_at_most": case["width"]}
    if any(len(line) > case["width"] for line in actual.split("\n")):
        print("REFUTATION CONFIRMED:", case, "actual:", repr(actual), "expected:", expected)
    else:
        print("REFUTATION REJECTED:", "every line fits the documented width")
```

**Output:**

```
REFUTATION CONFIRMED: {'width': 1, 'initial_indent': ' ', 'subsequent_indent': '', 'text': 'a'} actual: ' a' expected: {'every_line_length_at_most': 1}
```

Judge: DOC_BUG (low) -- The input and length check are valid: ' a' has length 2 despite width=1. However, the indent consumes the entire available width. TextWrapper deliberately consumes at least one character when indentation leaves no room, ensuring progress rather than rejecting the configuration or emitting empty lines. This is a reasonable edge-case policy; the documentation should qualify its width guarantee for indentation that leaves no space for text.

