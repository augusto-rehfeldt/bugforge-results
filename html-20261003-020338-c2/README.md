*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `html`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `html`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Long decimal character references obey HTML5 decoding without raising

Target: `html.unescape`

Property: For every nonempty ASCII decimal digit string d, html.unescape('&#' + d + ';') must return the HTML5 numeric-character-reference decoding. In particular, if d represents an integer greater than 0x10FFFF, the result must be '\uFFFD', regardless of the number of digits.

### Draft issue: html.unescape raises ValueError for decimal character references exceeding the integer conversion digit limit

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `html`

**Documented behaviour:** The unescape docstring states: "This function uses the rules defined by the HTML 5 standard for both valid and invalid character references, and the list of HTML 5 named character references defined in html.entities.html5." HTML5 numeric-reference rules replace values above 0x10FFFF with U+FFFD.

**Expected:** A single U+FFFD replacement character.

**Actual:** ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 4301 digits.

**Reproducer:**

```python
import html

d = '9' * 4301
s = '&#' + d + ';'
n = d.lstrip('0') or '0'
if not d or any(c not in '0123456789' for c in d):
    print('REFUTATION REJECTED: invalid decimal reference')
elif (len(n), n) <= (7, '1114111'):
    print('REFUTATION REJECTED: value is not above 0x10FFFF')
else:
    expected = '\uFFFD'
    try:
        actual = html.unescape(s)
    except Exception as e:
        actual = ('exception', type(e).__name__, str(e))
    if actual != expected:
        print('REFUTATION CONFIRMED:', repr(s), 'actual =', repr(actual),
              'expected =', repr(expected))
    else:
        print('REFUTATION REJECTED: result matches HTML5')
```

**Output:**

```
999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999;' actual = ('exception', 'ValueError', 'Exceeds the limit (4300 digits) for integer string conversion: value has 4301 digits; use sys.set_int_max_str_digits() to increase the limit') expected = '�'
```

Judge: BUG (medium) -- The reproducer uses a nonempty ASCII decimal reference whose value exceeds 0x10FFFF. HTML5 requires U+FFFD for that value, and html.unescape explicitly promises HTML5 handling of invalid references. Instead, decimal integer conversion raises ValueError at Python's digit limit. The documented integer-conversion limit does not justify violating unescape's decoding contract; this reference can be classified as out of range without converting the entire number. No duplicate is listed.

