*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `html.parser`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `html.parser`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c4 `bug`: Valid out-of-range numeric references can raise instead of converting

Target: `html.parser.HTMLParser.goahead`

Property: With convert_charrefs=True, for every n >= 4301, feeding '&#' + '9'*n + ';' and then closing must produce U+FFFD through handle_data without raising: the numeric reference denotes a value outside the Unicode range.

### Draft issue: HTMLParser raises ValueError for oversized decimal character references

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `html.parser`

**Documented behaviour:** HTMLParser documentation, constructor: "If convert_charrefs is True (the default), all character references (except the ones in script/style elements) are automatically converted to the corresponding Unicode characters." HTML character-reference conversion maps out-of-range numeric values to U+FFFD.

**Expected:** handle_data receives U+FFFD, with feed() and close() completing without exceptions.

**Actual:** ValueError: integer string conversion exceeds the 4300-digit limit for the 4301-digit reference.

**Reproducer:**

```python
import html.parser
import re

s = '&#' + '9' * 4301 + ';'
digits = s[2:-1]
if not re.fullmatch(r'&#[0-9]+;', s):
    print('REFUTATION REJECTED: invalid decimal character reference')
else:
    d = digits.lstrip('0') or '0'
    expected = ('data', '\ufffd' if (len(d), d) > (7, '1114111') else chr(int(d)))

    class Parser(html.parser.HTMLParser):
        def handle_data(self, data):
            chunks.append(data)

    chunks = []
    try:
        p = Parser(convert_charrefs=True)
        p.feed(s)
        p.close()
        actual = ('data', ''.join(chunks))
    except Exception as e:
        actual = ('exception', type(e).__name__, str(e))

    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), 'actual:', actual, 'expected:', expected)
    else:
        print('REFUTATION REJECTED: actual matches documented expectation')
```

**Output:**

```
9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999;' actual: ('exception', 'ValueError', 'Exceeds the limit (4300 digits) for integer string conversion: value has 4301 digits; use sys.set_int_max_str_digits() to increase the limit') expected: ('data', '�')
```

Judge: BUG (medium) -- The input is a valid decimal character reference whose value exceeds the Unicode range, so automatic HTML character-reference conversion should yield U+FFFD. The reproducer computes that expectation without converting the oversized decimal string to an integer. Instead, parsing exposes the integer-conversion digit limit as a ValueError. That limit does not justify failing HTML conversion when the value can be classified as out of range without integer conversion. The supplied issue is unrelated, and the upstream diff does not fix character-reference conversion.

