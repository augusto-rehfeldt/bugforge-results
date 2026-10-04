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