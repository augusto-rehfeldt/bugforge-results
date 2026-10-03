*Found and written by language models (bugforge); not reviewed by a person.*

# bugforge: `struct`

Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `struct`

Drafted issues are not filed. Read the reproducer, run it yourself, and check the tracker before filing anything.

## c2 `bug`: Zero-width Pascal string packing must not modify bytes outside the struct

Target: `struct.Struct.pack_into`

Property: For S = struct.Struct('0p'), any nonempty bytearray b, any integer offset with 0 <= offset < len(b), and any bytes value v, S.pack_into(b, offset, v) must leave b unchanged: S.size is zero, so the packed representation occupies no bytes.

### Draft issue: struct.Struct.pack_into with '0p' modifies a byte outside its zero-sized representation

**Environment:** Python 3.14.6 (Windows-11-10.0.26220-SP0), standard library `struct`

**Documented behaviour:** Python 3.14 library documentation, struct.Struct.pack_into: "Write the packed representation of the values v1, v2, ... into the writable buffer buffer starting at offset." The format documentation states: "The 'p' format character encodes a 'Pascal string', meaning a short variable-length string stored in a fixed number of bytes, given by the count."

**Expected:** The buffer remains b'\xfe'.

**Actual:** pack_into changes the buffer to b'\x00' despite Struct.size being zero.

**Reproducer:**

```python
import struct

s = struct.Struct('0p')
b, offset, v = bytearray(b'\xfe'), 0, b''
inp = repr((b, offset, v))
expected = bytes(b)  # A zero-byte representation changes no bytes.
if not (s.size == 0 and isinstance(b, bytearray) and b
        and isinstance(offset, int) and 0 <= offset < len(b)
        and isinstance(v, bytes)):
    print('REFUTATION REJECTED: invalid input')
else:
    try:
        s.pack_into(b, offset, v)
    except Exception as e:
        print('REFUTATION REJECTED:', repr(e))
    else:
        actual = bytes(b)
        if actual != expected:
            print('REFUTATION CONFIRMED:', inp,
                  'actual:', repr(actual), 'expected:', repr(expected))
        else:
            print('REFUTATION REJECTED: buffer unchanged')
```

**Output:**

```
REFUTATION CONFIRMED: (bytearray(b'\xfe'), 0, b'') actual: b'\x00' expected: b'\xfe'
```

Judge: BUG (medium) -- The reproducer uses valid inputs: '0p' is accepted, its Struct.size is zero, the buffer is writable, the offset is in bounds, and the value is bytes. A Pascal string occupies the number of bytes specified by its count; with count zero, writing its packed representation must not modify any buffer byte. The observed write therefore falls outside the representation's bounds. No duplicate was supplied; whether upstream already fixes this was not checked.

