*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `quopri`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `quopri`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Fallback encoder splits quoted-printable escape triplets at line boundaries

Target: `quopri.encodestring`

Property: For every bytes input s, encodestring(s, quotetabs=True, header=False) must produce valid quoted-printable: each encoded-byte escape '=HH' must remain contiguous, never split across a soft line break. This must hold for the supported pure-Python fallback as well as the accelerated implementation.

### Draft issue: quopri pure-Python encoder splits hexadecimal escapes at line boundaries

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `quopri`

**Documented behaviour:** Python standard-library documentation, quopri.encodestring: “Encode the contents of s, a bytes object which contains data, and return the encoded data as a bytes object.” The quopri module documentation identifies the encoding as quoted-printable.

**Expected:** 74 ASCII A bytes followed by b'=\n=FFB', preserving the contiguous =FF escape.

**Actual:** 74 ASCII A bytes followed by b'==\nFFB', splitting the =FF escape across a soft line break.

**Reproducer:**

```python
import quopri

s = b'A' * 74 + b'\xffB'
if not isinstance(s, bytes):
    print('REFUTATION REJECTED: input is not bytes')
else:
    lines, line = [], b''
    for c in s:
        token = bytes([c]) if 33 <= c <= 126 and c != 61 else ('=%02X' % c).encode()
        if len(line + token) > 75:
            lines.append(line + b'=\n')
            line = b''
        line += token
    expected = b''.join(lines) + line
    quopri.b2a_qp = None  # Exercise the supported pure-Python fallback.
    actual = quopri.encodestring(s, quotetabs=True, header=False)
    if actual != expected:
        print('REFUTATION CONFIRMED:', s, actual, expected)
    else:
        print('REFUTATION REJECTED: output matches independently encoded expectation')
```

**Output:**

```
REFUTATION CONFIRMED: b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xffB' b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==\nFFB' b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=\n=FFB'
```

Judge: BUG (medium) -- The input is valid bytes, and producing quoted-printable requires keeping =HH escapes intact. The pure-Python fallback wraps within =FF, leaving an invalid escape before the soft line break. The independently constructed expectation is valid. The listed issues concern decoding, newline handling, or incremental codecs, not this encoding defect; main still contains the behavior.

