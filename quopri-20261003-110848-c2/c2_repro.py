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