import base64
import io
import random
import time

ALPHABET = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def reference(payload):
    result = bytearray()
    for offset in range(0, len(payload), 57):
        line = payload[offset:offset + 57]
        for i in range(0, len(line), 3):
            block = line[i:i + 3]
            value = int.from_bytes(block, "big") << (8 * (3 - len(block)))
            result.append(ALPHABET[(value >> 18) & 63])
            result.append(ALPHABET[(value >> 12) & 63])
            result.append(ALPHABET[(value >> 6) & 63] if len(block) >= 2 else 61)
            result.append(ALPHABET[value & 63] if len(block) == 3 else 61)
        result.append(10)
    return bytes(result)


class PrefixWriter(io.RawIOBase):
    def __init__(self, limit):
        super().__init__()
        self.limit = limit
        self.data = bytearray()

    def writable(self):
        return True

    def write(self, b):
        accepted = b[:self.limit]
        self.data.extend(accepted)
        return len(accepted)


def run(payload, limit):
    output = PrefixWriter(limit)
    try:
        base64.encode(io.BytesIO(payload), output)
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc), bytes(output.data))
    return bytes(output.data)


def main():
    sanity_ok = True
    for payload in (b"hello", bytes(range(114))):
        expected = reference(payload)
        output = io.BytesIO()
        base64.encode(io.BytesIO(payload), output)
        actual = output.getvalue()
        agrees = actual == expected == base64.encodebytes(payload)
        print("SANITY:", repr(payload), agrees)
        sanity_ok = sanity_ok and agrees
    if not sanity_ok:
        print("SANITY FAILED")
        return

    deadline = time.monotonic() + 170
    tested = 0

    def check(payload, limit):
        nonlocal tested
        expected = reference(payload)
        actual = run(payload, limit)
        tested += 1
        if actual != expected:
            repeated = run(payload, limit)
            if repeated == actual:
                print("COUNTEREXAMPLE:")
                print(repr((payload, limit)))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return True
        return False

    for length in (1, 56, 57, 58, 114):
        payload = bytes(i % 256 for i in range(length))
        for limit in (1, 2, 75):
            if check(payload, limit):
                return

    rng = random.Random(917234)
    for _ in range(100000):
        if time.monotonic() >= deadline:
            break
        length = rng.choice((0, 1, 56, 57, 58, 114, rng.randrange(4097)))
        payload = bytes(rng.getrandbits(8) for _ in range(length))
        limit = rng.choice((1, 2, 75, rng.randrange(1, 257)))
        if check(payload, limit):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()