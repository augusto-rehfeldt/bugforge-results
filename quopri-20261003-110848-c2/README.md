*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `quopri`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `quopri`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: decode silently loses bytes on short-writing binary streams

Target: `quopri.decode`

Property: For every nonempty ASCII-letter byte string s and writable binary output stream whose write(b) accepts a positive prefix and returns its length, decode(BytesIO(s), output) must deliver all of s to the output, even when each write accepts fewer bytes than supplied.

### Draft issue: quopri.decode silently truncates output on short writes

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `quopri`

**Documented behaviour:** quopri.decode documentation: "Decode the contents of the input file and write the resulting decoded binary data to the output file. input and output must be binary file objects." The io.RawIOBase.write documentation permits returning fewer bytes than supplied.

**Expected:** Output contains b'AB'.

**Actual:** decode returns normally, but output contains only b'A'.

**Reproducer:**

```python
import io
import quopri

s = b'AB'
limit = 1

class Output(io.RawIOBase):
    def __init__(self):
        super().__init__()
        self.data = bytearray()

    def writable(self):
        return True

    def write(self, b):
        n = min(limit, len(b))
        self.data.extend(b[:n])
        return n

source, output = io.BytesIO(s), Output()
if not (s and all(65 <= c <= 90 or 97 <= c <= 122 for c in s)
        and source.readable() and output.writable() and limit > 0):
    print("REFUTATION REJECTED:", "invalid input or stream")
else:
    expected = s  # ASCII letters are literal quoted-printable data.
    try:
        quopri.decode(source, output)
    except Exception as e:
        print("REFUTATION REJECTED:", repr(e))
    else:
        actual = bytes(output.data)
        if actual != expected:
            print("REFUTATION CONFIRMED:", (s, limit), actual, expected)
        else:
            print("REFUTATION REJECTED:", "actual matches expected")
```

**Output:**

```
REFUTATION CONFIRMED: (b'AB', 1) b'A' b'AB'
```

Judge: BUG (medium) -- The reproducer supplies valid binary file objects and literal quoted-printable input. RawIOBase.write explicitly permits positive short writes, so accepting only one byte is valid stream behavior. decode silently loses the unwritten suffix instead of delivering all decoded data as documented. None of the listed issues reports this output-side short-write problem.

