*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `quopri`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `quopri`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Fallback encoder splits hexadecimal escapes at soft line breaks

Target: `quopri.encode`

Property: For every bytes payload s containing no CR or LF, encoding BytesIO(s) into a BytesIO output with quotetabs=True and header=False must produce quoted-printable data that decodes back to s. This must also hold when the optional binascii encoder is unavailable (quopri.b2a_qp is None).

### Draft issue: quopri.encode pure-Python fallback splits hexadecimal escapes at line boundaries

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `quopri`

**Documented behaviour:** The quopri.encode docstring promises: "Read 'input', apply quoted-printable encoding, and write to 'output'." The module docstring identifies the format as "quoted-printable transport encoding as per RFC 1521." Quoted-printable hexadecimal escapes must remain intact across soft line breaks.

**Expected:** Valid quoted-printable output that decodes to 74 ASCII A bytes followed by byte 0xff, with the =FF escape kept intact.

**Actual:** The output is 74 ASCII A bytes followed by b'==\nFF'; decoding yields those A bytes followed by b'=\nFF' instead of byte 0xff.

**Reproducer:**

```python
import binascii, io, quopri

s = b'A' * 74 + b'\xff'
if not isinstance(s, bytes) or b'\r' in s or b'\n' in s:
    print('REFUTATION REJECTED:', 'input is not a newline-free bytes payload')
else:
    quopri.b2a_qp = None
    out = io.BytesIO()
    quopri.encode(io.BytesIO(s), out, quotetabs=True, header=False)
    encoded = out.getvalue()
    actual = binascii.a2b_qp(encoded)
    expected = s
    if actual != expected:
        print('REFUTATION CONFIRMED:', s, (encoded, actual), expected)
    else:
        print('REFUTATION REJECTED:', 'independent decoding recovers the input')
```

**Output:**

```
REFUTATION CONFIRMED: b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xff' (b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==\nFF', b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=\nFF') b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xff'
```

Judge: BUG (medium) -- The valid newline-free bytes input must be preserved by quoted-printable encoding and decoding. Disabling the optional accelerator exercises the pure-Python fallback. It splits the =FF escape after its initial equals sign, then appends a soft-break equals sign, producing invalid quoted-printable data and corrupting the decoded payload. The independent binascii decoder correctly exposes this failure. None of the listed issues identifies this escape-splitting defect.

