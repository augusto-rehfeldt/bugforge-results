import base64, binascii, io

data = (None, b'\x00', b'')

class Input(io.RawIOBase):
    def __init__(self):
        super().__init__()
        self.parts = iter(data)
    def readable(self):
        return True
    def readinto(self, buffer):
        part = next(self.parts, b'')
        if part is None:
            return None
        buffer[:len(part)] = part
        return len(part)

probe = Input()
if not probe.readable() or tuple(probe.read(57) for _ in data) != data:
    print("REFUTATION REJECTED: input violates the binary read contract")
else:
    expected = binascii.b2a_base64(b''.join(p for p in data if p is not None))
    output = io.BytesIO()
    try:
        base64.encode(Input(), output)
    except Exception as error:
        print("REFUTATION REJECTED: read did not complete successfully:", repr(error))
    else:
        actual = ("returned", output.getvalue())
        if output.getvalue() != expected:
            print("REFUTATION CONFIRMED:", data, "actual:", actual,
                  "expected:", ("encode", expected, "or signal read unavailable"))
        else:
            print("REFUTATION REJECTED: payload was encoded")