*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `base64`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `base64`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: File encoder silently loses data on short writes

Target: `base64.encode`

Property: For any finite bytes payload p, encoding io.BytesIO(p) into a writable in-memory binary stream must produce base64.encodebytes(p), including when the output stream's write method legally accepts only a positive prefix of each nonempty buffer and returns the number of bytes accepted.

### Draft issue: base64.encode silently truncates output when the binary stream performs short writes

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `base64`

**Documented behaviour:** "Encode a file; input and output are binary files." — base64.encode documentation. Binary raw streams may return a write count smaller than the supplied buffer.

**Expected:** b'AA==\n'

**Actual:** b'A'

**Reproducer:**

```python
import base64, binascii, io

class PrefixWriter(io.RawIOBase):
    def __init__(self, limit):
        super().__init__()
        self.limit, self.data = limit, bytearray()
    def writable(self):
        return True
    def write(self, b):
        n = min(len(b), self.limit)
        self.data.extend(b[:n])
        return n

p, limit = b'\x00', 1
src, dst = io.BytesIO(p), PrefixWriter(limit)
if not (isinstance(p, bytes) and src.readable() and dst.writable() and limit > 0):
    print("REFUTATION REJECTED: invalid binary stream input")
else:
    base64.encode(src, dst)
    actual = bytes(dst.data)
    expected = binascii.b2a_base64(p)
    if actual != expected:
        print("REFUTATION CONFIRMED:", (p, limit), "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: actual matches expected")
```

**Output:**

```
REFUTATION CONFIRMED: (b'\x00', 1) actual: b'A' expected: b'AA==\n'
```

Judge: BUG (medium) -- PrefixWriter is a valid writable binary raw stream: accepting a positive prefix and returning its length is permitted. base64.encode silently loses the unwritten suffix instead of completing the encoded output. For this one-byte payload, binascii.b2a_base64(p) equals base64.encodebytes(p), so the expectation is correct. None of the listed issues addresses short output writes, and the supplied upstream diff does not fix encode.

