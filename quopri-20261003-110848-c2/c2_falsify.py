import io
import quopri
import random
import time


class PrefixOutput(io.RawIOBase):
    def __init__(self, limit):
        super().__init__()
        self.limit = limit
        self.data = bytearray()

    def writable(self):
        return True

    def write(self, b):
        self._checkClosed()
        prefix = bytes(b[:self.limit])
        self.data.extend(prefix)
        return len(prefix)


def reference(s):
    # ASCII letters have no quoted-printable escapes or line structure.
    assert s and all(65 <= c <= 90 or 97 <= c <= 122 for c in s)
    return bytes(s)


def ordinary(s):
    output = io.BytesIO()
    quopri.decode(io.BytesIO(s), output)
    return output.getvalue()


def run(s, limit):
    output = PrefixOutput(limit)
    try:
        quopri.decode(io.BytesIO(s), output)
        return bytes(output.data)
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc), bytes(output.data))


def main():
    for s in (b"AB", b"HelloWorld"):
        expected = reference(s)
        actual = ordinary(s)
        print("SANITY:", repr(s), repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 180
    rng = random.Random(20260719)
    alphabet = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    edges = [
        (b"AB", 1),
        (b"abc", 1),
        (b"abc", 2),
        (b"A" * 64, 1),
        (b"Z" * 64, 63),
        (alphabet, 7),
    ]
    tested = 0

    def check(s, limit):
        nonlocal tested
        tested += 1
        expected = reference(s)
        actual = run(s, limit)
        if actual != expected:
            repeated = run(s, limit)
            if repeated == actual:
                print("COUNTEREXAMPLE:")
                print(repr((s, limit)))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return True
        return False

    for s, limit in edges:
        if time.monotonic() >= deadline:
            break
        if check(s, limit):
            return

    while time.monotonic() < deadline:
        length = rng.randint(2, 4096)
        s = bytes(rng.choice(alphabet) for _ in range(length))
        limit = rng.randint(1, length - 1)
        if check(s, limit):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()