import base64
import io
import random
import time


ALPHABET = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def reference(payload):
    result = bytearray()
    for offset in range(0, len(payload), 57):
        line = payload[offset:offset + 57]
        for start in range(0, len(line), 3):
            chunk = line[start:start + 3]
            value = int.from_bytes(chunk, "big") << (8 * (3 - len(chunk)))
            result.append(ALPHABET[(value >> 18) & 63])
            result.append(ALPHABET[(value >> 12) & 63])
            result.append(ALPHABET[(value >> 6) & 63] if len(chunk) >= 2 else 61)
            result.append(ALPHABET[value & 63] if len(chunk) == 3 else 61)
        result.append(10)
    return bytes(result)


class TemporarilyUnavailable(io.RawIOBase):
    def __init__(self, payload):
        super().__init__()
        self.payload = payload
        self.step = 0

    def readable(self):
        return True

    def read(self, size=-1):
        if self.step == 0:
            self.step = 1
            return None
        if self.step == 1:
            if size == 0:
                return b""
            count = len(self.payload) if size is None or size < 0 else size
            result = self.payload[:count]
            self.payload = self.payload[count:]
            if not self.payload:
                self.step = 2
            return result
        return b""


def run(payload):
    source = TemporarilyUnavailable(payload)
    output = io.BytesIO()
    try:
        base64.encode(source, output)
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc), output.getvalue())
    return ("returned", output.getvalue())


def main():
    for payload in (b"f", bytes(range(58))):
        output = io.BytesIO()
        base64.encode(io.BytesIO(payload), output)
        expected = reference(payload)
        actual = output.getvalue()
        print("SANITY:", repr(payload), repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 175
    rng = random.Random(90210)
    tested = 0
    edges = [
        b"\x00",
        b"\xff",
        bytes(range(57)),
        b"\xff" * 57,
        bytes(range(58)),
        b"\x00" * 58,
    ]

    def check(payload):
        nonlocal tested
        tested += 1
        expected = reference(payload)
        actual = run(payload)
        if actual[0] == "returned" and actual[1] != expected:
            repeated = run(payload)
            if repeated[0] == "returned" and repeated[1] != expected:
                print("COUNTEREXAMPLE:")
                print(repr((None, payload, b"")))
                print("actual:", repr(repeated))
                print("expected:", repr(("encode", expected, "or signal read unavailable")))
                return True
        return False

    for payload in edges:
        if check(payload):
            return

    while time.monotonic() < deadline:
        length = rng.choice((1, 57, 58))
        payload = bytes(rng.randrange(256) for _ in range(length))
        if check(payload):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()