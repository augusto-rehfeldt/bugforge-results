*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `struct`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `struct`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c3 `bug`: pack_into may erase an aliased bytearray string argument before copying it

Target: `struct.pack_into`

Property: For every positive integer n and bytearray b of length n, let expected = struct.pack(f'{n}s', b) before mutation. After struct.pack_into(f'{n}s', b, 0, b), bytes(b) must equal expected. In particular, packing an exactly sized bytearray into itself with an 's' field must preserve its contents.

### Draft issue: struct.pack_into corrupts an 's' value when source and destination are the same bytearray

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `struct`

**Documented behaviour:** Python struct documentation, struct.pack_into: "Pack the values v1, v2, ... according to the format string format and write the packed bytes into the writable buffer buffer starting at position offset." The format-character notes also state: "For the 's' format character, the count is interpreted as the length of the bytes."

**Expected:** b'A'

**Actual:** b'\x00'

**Reproducer:**

```python
import struct

b = bytearray(b'A')
fmt, offset = '1s', 0
given = repr((fmt, b, offset, b))
if not isinstance(b, bytearray) or len(b) != struct.calcsize(fmt):
    print('REFUTATION REJECTED: invalid input')
else:
    expected = bytes(b)  # Exactly one byte: no padding or truncation.
    struct.pack_into(fmt, b, offset, b)
    actual = bytes(b)
    if actual != expected:
        print('REFUTATION CONFIRMED:', given, 'actual=', actual, 'expected=', expected)
    else:
        print('REFUTATION REJECTED: actual equals documented expectation')
```

**Output:**

```
REFUTATION CONFIRMED: ('1s', bytearray(b'A'), 0, bytearray(b'A')) actual= b'\x00' expected= b'A'
```

Judge: BUG (medium) -- The reproducer uses a valid bytearray as both the writable destination and the 's' value. Packing one byte into an exactly sized buffer requires neither padding nor truncation, so the documented packed value is b'A'. Instead, pack_into destroys the source before packing it. No cited documentation excludes aliased inputs, and neither listed issue reports this behavior. The upstream implementation was not compared, so whether it is already fixed there remains unknown.

