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