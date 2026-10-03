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