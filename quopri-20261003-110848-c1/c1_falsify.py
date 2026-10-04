import io
import quopri
import random
import time


class PrefixWriter(io.RawIOBase):
    def __init__(self, k):
        super().__init__()
        self.k = k
        self.data = bytearray()

    def writable(self):
        return True

    def write(self, b):
        n = min(self.k, len(b))
        self.data.extend(b[:n])
        return n


def reference(s):
    # Inputs contain only ASCII 33..126, have length 2..24, and
    # therefore need neither whitespace escaping nor line wrapping.
    return b"".join(
        b"=3D" if byte == 61 else bytes([byte])
        for byte in s
    )


def ordinary_encode(s):
    out = io.BytesIO()
    quopri.encode(io.BytesIO(s), out, quotetabs=False, header=False)
    return out.getvalue()


def run(s, k):
    out = PrefixWriter(k)
    try:
        quopri.encode(io.BytesIO(s), out, quotetabs=False, header=False)
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc), bytes(out.data))
    return bytes(out.data)


def main():
    for s in (b"HelloWorld!", b"A=B"):
        expected = reference(s)
        actual = ordinary_encode(s)
        print("SANITY:", repr(s), repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 170
    rng = random.Random(20260317)
    tested = 0

    edges = [
        (b"AB", 1),
        (b"AB", 2),
        (b"A=B", 1),
        (b"==", 2),
        (b"..", 1),
        (b"!~", 1),
        (b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:24], 3),
    ]

    def cases():
        yield from edges
        for _ in range(100000):
            n = rng.randint(2, 24)
            s = bytes(rng.randint(33, 126) for _ in range(n))
            k = rng.randint(1, n - 1)
            yield s, k

    for s, k in cases():
        if time.monotonic() >= deadline:
            break
        expected = reference(s)
        actual = run(s, k)
        tested += 1
        if actual != expected:
            repeated = run(s, k)
            if repeated == actual:
                print("COUNTEREXAMPLE:", repr((s, k)),
                      repr(actual), repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()