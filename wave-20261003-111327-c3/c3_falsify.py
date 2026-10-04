import io
import random
import time
import wave


class ShortWriteStream:
    def __init__(self, cap):
        self.buffer = io.BytesIO()
        self.cap = cap

    def write(self, data):
        if self.tell() >= 44:
            data = memoryview(data)[:self.cap]
        return self.buffer.write(data)

    def read(self, size=-1):
        return self.buffer.read(size)

    def tell(self):
        return self.buffer.tell()

    def seek(self, offset, whence=0):
        return self.buffer.seek(offset, whence)

    def flush(self):
        self.buffer.flush()

    def close(self):
        # Keep storage available for inspection after writer closure.
        self.flush()

    def getvalue(self):
        return self.buffer.getvalue()


def reference(payload):
    # Mono PCM with one-byte samples: each supplied byte is one complete frame.
    return bytes(payload)


def run(payload, cap, rate):
    stream = ShortWriteStream(cap)
    try:
        writer = wave.Wave_write(stream)
        writer.setnchannels(1)
        writer.setsampwidth(1)
        writer.setframerate(rate)
        writer.writeframesraw(payload)
        writer.close()
        reader = wave.Wave_read(io.BytesIO(stream.getvalue()))
        try:
            return reader.readframes(-1)
        finally:
            reader.close()
    except Exception as exc:
        return ("EXCEPTION", type(exc).__name__, str(exc))


def main():
    for payload, cap, rate in [
        (b"\x00\x7f\x80\xff", 4, 8000),
        (bytes(range(256)), 1024, 44100),
    ]:
        actual = run(payload, cap, rate)
        expected = reference(payload)
        print("SANITY:", actual == expected)
        if actual != expected:
            print("SANITY FAILED")
            return

    started = time.monotonic()
    rng = random.Random(913746)
    cases = 0

    def check(payload, cap, rate):
        nonlocal cases
        cases += 1
        expected = reference(payload)
        actual = run(payload, cap, rate)
        if actual != expected:
            repeated = run(payload, cap, rate)
            if repeated == actual:
                print("COUNTEREXAMPLE:")
                print(repr({"payload": payload, "cap": cap, "rate": rate}))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return True
        return False

    for length, cap in [
        (2, 1), (3, 1), (3, 2), (45, 1), (45, 44),
        (256, 255), (257, 128), (4096, 7),
    ]:
        payload = bytes((i * 73 + 19) % 256 for i in range(length))
        if check(payload, cap, 8000):
            return

    for _ in range(100000):
        if time.monotonic() - started >= 170:
            break
        length = rng.randint(2, 16384)
        cap = rng.randint(1, length - 1)
        payload = bytes(rng.getrandbits(8) for _ in range(length))
        if check(payload, cap, rng.choice([8000, 11025, 22050, 44100, 48000])):
            return

    print("NO COUNTEREXAMPLE", cases)


if __name__ == "__main__":
    main()