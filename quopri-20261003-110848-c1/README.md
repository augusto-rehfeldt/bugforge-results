*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `quopri`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `quopri`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: encode silently loses data when a binary output stream performs short writes

Target: `quopri.encode`

Property: For any bytes payload s and any blocking, writable binary output stream whose write(b) accepts a positive prefix of b and returns its length, encode(BytesIO(s), output, quotetabs=False, header=False) must write the same complete byte sequence as encoding s into BytesIO.

### Draft issue: quopri.encode silently truncates output on short writes

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `quopri`

**Documented behaviour:** quopri.encode documentation: "Encode the contents of the input file and write the resulting quoted-printable data to the output file. input and output must be binary file objects." The io.RawIOBase.write documentation permits writing fewer bytes than supplied.

**Expected:** b'AB'

**Actual:** b'A'

**Reproducer:**

```python
import io, quopri

class ShortWriter(io.RawIOBase):
    def __init__(self):
        super().__init__()
        self.data = bytearray()
    def writable(self):
        return True
    def write(self, b):
        n = min(1, len(b))
        self.data.extend(b[:n])
        return n

s = b'AB'
src, dst = io.BytesIO(s), ShortWriter()
if not (isinstance(s, bytes) and src.readable() and dst.writable()
        and all(33 <= c <= 126 and c != 61 for c in s)):
    print("REFUTATION REJECTED: invalid input")
else:
    # These two printable ASCII bytes require neither quoting nor line wrapping.
    expected = s
    quopri.encode(src, dst, quotetabs=False, header=False)
    actual = bytes(dst.data)
    if actual != expected:
        print("REFUTATION CONFIRMED:", (s, 1), actual, expected)
    else:
        print("REFUTATION REJECTED: output matches the documented encoding")
```

**Output:**

```
REFUTATION CONFIRMED: (b'AB', 1) b'A' b'AB'
```

Judge: BUG (medium) -- ShortWriter is a valid writable binary RawIOBase stream, whose write() may legally return a positive short count. The payload b'AB' requires no quoting or wrapping, so the expected encoding is correct. quopri.encode ignores the short write and silently loses the remaining byte, violating its promise to write the encoded contents. No duplicate is listed.

