*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `quopri`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `quopri`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Trailing-space quoting can exceed the quoted-printable line-length limit

Target: `quopri.encodestring`

Property: For every bytes input containing no CR or LF, encodestring(s, quotetabs=False, header=False) must emit quoted-printable physical lines of at most 76 bytes, excluding their line terminators. This must also hold when the supported pure-Python fallback is selected by setting quopri.b2a_qp to None and restoring it afterward.

### Draft issue: quopri pure-Python fallback exceeds quoted-printable line length limit at a space boundary

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `quopri`

**Documented behaviour:** The Python standard-library quopri documentation describes encodestring as: "Encode the contents of the string s, which contains binary data, and return a bytes object containing the encoded data." Its module introduction identifies the format as "quoted-printable transport encoding, as defined in RFC 1521"; RFC 1521 §5.1 states: "The Quoted-Printable encoding requires that encoded lines be no more than 76 characters long."

**Expected:** Every encoded physical line is at most 76 bytes, excluding its line terminator, including when using the pure-Python fallback.

**Actual:** The fallback emits 74 'A' bytes followed by '=20=' and LF, producing physical line lengths [78, 2].

**Reproducer:**

```python
import quopri

s = b'A' * 74 + b' BB'
saved = quopri.b2a_qp
failure = None
try:
    if not isinstance(s, bytes) or b'\r' in s or b'\n' in s:
        reason = 'input is not bytes without CR/LF'
    else:
        reason = 'all physical lines are at most 76 bytes'
        for encoder in (saved, None):
            quopri.b2a_qp = encoder
            actual = quopri.encodestring(s, quotetabs=False, header=False)
            lengths = list(map(len, actual.splitlines()))
            if any(n > 76 for n in lengths):
                failure = (actual, lengths)
                break
finally:
    quopri.b2a_qp = saved

if failure:
    print('REFUTATION CONFIRMED:', 'input=', repr(s),
          'actual=', repr(failure[0]), 'line lengths=', failure[1],
          'expected=every physical line length <= 76 bytes')
else:
    print('REFUTATION REJECTED:', reason)
```

**Output:**

```
REFUTATION CONFIRMED: input= b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA BB' actual= b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=20=\nBB' line lengths= [78, 2] expected=every physical line length <= 76 bytes
```

Judge: BUG (medium) -- The valid bytes input produces a 78-byte physical line, violating the 76-character limit of the documented quoted-printable format. The pure-Python fallback expands a space at the wrap boundary to '=20' without reserving enough room for that expansion and the soft-break '='. The reproducer measures line lengths correctly and restores the encoder. Neither listed item reports or fixes this wrapping defect.

