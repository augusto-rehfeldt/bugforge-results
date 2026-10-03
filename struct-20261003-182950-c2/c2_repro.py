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