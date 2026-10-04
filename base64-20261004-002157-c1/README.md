*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `base64`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `base64`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c1 `bug`: Temporary read unavailability is mistaken for EOF

Target: `base64.encode`

Property: For a binary input stream whose read() returns None when temporarily unavailable, then supplies a nonempty bytes payload p before returning b'' at EOF, encode(input, output) must not return successfully with an encoding that omits p; it must encode the data or signal that the read cannot currently complete.

### Draft issue: base64.encode silently treats non-blocking read returning None as EOF

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `base64`

**Documented behaviour:** base64.encode documentation: "Encode a file; input and output are binary files." io.RawIOBase.read documentation: "If the object is in non-blocking mode and no bytes are available, None is returned."

**Expected:** Encode the payload as b'AA==\n', or raise an exception indicating that reading cannot currently complete.

**Actual:** Returns successfully with empty output, omitting b'\x00'.

**Reproducer:**

```python
import base64, binascii, io

data = (None, b'\x00', b'')

class Input(io.RawIOBase):
    def __init__(self):
        super().__init__()
        self.parts = iter(data)
    def readable(self):
        return True
    def readinto(self, buffer):
        part = next(self.parts, b'')
        if part is None:
            return None
        buffer[:len(part)] = part
        return len(part)

probe = Input()
if not probe.readable() or tuple(probe.read(57) for _ in data) != data:
    print("REFUTATION REJECTED: input violates the binary read contract")
else:
    expected = binascii.b2a_base64(b''.join(p for p in data if p is not None))
    output = io.BytesIO()
    try:
        base64.encode(Input(), output)
    except Exception as error:
        print("REFUTATION REJECTED: read did not complete successfully:", repr(error))
    else:
        actual = ("returned", output.getvalue())
        if output.getvalue() != expected:
            print("REFUTATION CONFIRMED:", data, "actual:", actual,
                  "expected:", ("encode", expected, "or signal read unavailable"))
        else:
            print("REFUTATION REJECTED: payload was encoded")
```

**Output:**

```
REFUTATION CONFIRMED: (None, b'\x00', b'') actual: ('returned', b'') expected: ('encode', b'AA==\n', 'or signal read unavailable')
```

Judge: BUG (medium) -- The reproducer supplies a valid readable binary RawIOBase stream: None means temporarily unavailable, whereas b'' means EOF. encode treats the initial None as EOF and returns successfully without reading the subsequent payload, silently truncating its documented file encoding operation. The expected encoding is correct. Neither listed issue reports or fixes this behavior, and the supplied upstream diff leaves encode unchanged.

