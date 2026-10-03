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