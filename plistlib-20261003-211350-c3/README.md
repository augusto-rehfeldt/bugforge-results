*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `plistlib`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `plistlib`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: Binary dump requires tell() on a writable binary stream

Target: `plistlib.dump`

Property: For a writable binary stream fp that supports write() but not tell() or seeking, dump(value, fp, fmt=FMT_BINARY) must successfully serialize a supported value, such as an integer, and the captured bytes must load back to that value.

### Draft issue: plistlib.dump fails on non-seekable writable streams with FMT_BINARY

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `plistlib`

**Documented behaviour:** "'fp' should be a writable, binary file object." — plistlib.dump documentation and its source docstring; no positioning capability is required.

**Expected:** dump(0, fp, fmt=FMT_BINARY) succeeds, and the captured bytes load as 0.

**Actual:** dump raises io.UnsupportedOperation('seek') instead of completing serialization.

**Reproducer:**

```python
import io
import plistlib

class Sink(io.RawIOBase):
    def __init__(self):
        super().__init__()
        self.data = bytearray()
    def writable(self):
        return True
    def write(self, data):
        self.data.extend(data)
        return len(data)

value, fp = 0, Sink()
if not (fp.writable() and not fp.seekable() and type(value) is int):
    print("REFUTATION REJECTED: invalid input")
else:
    expected = value
    try:
        plistlib.dump(value, fp, fmt=plistlib.FMT_BINARY)
        actual = plistlib.loads(bytes(fp.data))
    except Exception as e:
        actual = ("exception", type(e).__name__, str(e))
    if actual != expected:
        print("REFUTATION CONFIRMED:", "input:", value,
              "actual:", actual, "expected:", expected)
    else:
        print("REFUTATION REJECTED: serialization and round-trip succeeded")
```

**Output:**

```
REFUTATION CONFIRMED: input: 0 actual: ('exception', 'UnsupportedOperation', 'seek') expected: 0
```

Judge: BUG (medium) -- Sink is a valid writable binary stream, and 0 is a supported plist value. The documented dump contract does not require positioning support, but the binary writer calls tell(), which raises UnsupportedOperation on this non-seekable stream. Serialization can track emitted byte offsets without querying the stream position. None of the listed issues or PRs addresses this failure, and the supplied upstream diff leaves it unchanged.

