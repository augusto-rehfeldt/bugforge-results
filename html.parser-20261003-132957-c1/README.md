*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `html.parser`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `html.parser`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Long numeric character references in attributes raise ValueError instead of decoding

Target: `html.parser.HTMLParser.parse_starttag`

Property: With the default integer-string conversion limit, for every n >= 4300, feeding '<div title="&#' + '0'*n + '65;">' to HTMLParser(convert_charrefs=True) must call handle_starttag('div', [('title', 'A')]) without raising an exception: the decimal character reference denotes Unicode code point 65 regardless of leading zeros.

### Draft issue: HTMLParser raises ValueError for numeric character references with many leading zeros

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `html.parser`

**Documented behaviour:** HTMLParser documentation, constructor: "If convert_charrefs is True (the default), all character references (except the ones in script/style elements) are automatically converted to the corresponding Unicode characters."

**Expected:** handle_starttag('div', [('title', 'A')]) without an exception

**Actual:** ValueError: integer string conversion exceeds the 4300-digit limit; handle_starttag is not called.

**Reproducer:**

```python
import html.parser
import re
import sys

if not hasattr(sys, "set_int_max_str_digits"):
    print("REFUTATION REJECTED: integer-string conversion limit unavailable")
else:
    sys.set_int_max_str_digits(4300)
    text = '<div title="&#' + '0' * 4300 + '65;">'
    match = re.fullmatch(r'<div title="&#([0-9]+);">', text)
    if not match or match[1].lstrip("0") != "65":
        print("REFUTATION REJECTED: input is not a valid decimal reference to U+0041")
    else:
        expected = ("OK", [("div", [("title", chr(65))])])
        events = []

        class Parser(html.parser.HTMLParser):
            def handle_starttag(self, tag, attrs):
                events.append((tag, attrs))

        try:
            Parser(convert_charrefs=True).feed(text)
            actual = ("OK", events)
        except Exception as e:
            actual = ("EXCEPTION", type(e).__name__, str(e))

        if actual != expected:
            print("REFUTATION CONFIRMED:", repr(text),
                  "actual:", actual, "expected:", expected)
        else:
            print("REFUTATION REJECTED: actual matches documented expectation")
```

**Output:**

```
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000065;">' actual: ('EXCEPTION', 'ValueError', 'Exceeds the limit (4300 digits) for integer string conversion: value has 4302 digits; use sys.set_int_max_str_digits() to increase the limit') expected: ('OK', [('div', [('title', 'A')])])
```

Judge: BUG (medium) -- The input contains a valid decimal character reference to U+0041; leading zeros do not change its value. Attribute character-reference conversion instead raises ValueError because all 4302 digits are passed to integer conversion. The integer conversion limit is documented, but it is not a documented restriction on HTML character references and does not justify failing to decode this small code point. Neither listed issue nor the supplied upstream changes address this behaviour.

