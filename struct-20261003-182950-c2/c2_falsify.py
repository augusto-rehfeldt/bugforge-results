import random
import struct
import time


def reference(buffer, offset, count, value):
    result = bytearray(buffer)
    if count:
        payload = value[:count - 1]
        encoded = bytes([min(len(payload), 255)]) + payload
        encoded += b"\x00" * (count - len(encoded))
        result[offset:offset + count] = encoded
    return bytes(result)


def main():
    for count, initial, offset, value in (
        (5, b"abcdefgh", 1, b"xy"),
        (4, b"abcdefgh", 2, b"abcdef"),
    ):
        expected = reference(initial, offset, count, value)
        buffer = bytearray(initial)
        struct.Struct(f"{count}p").pack_into(buffer, offset, value)
        actual = bytes(buffer)
        print("SANITY:", repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    target = struct.Struct("0p")
    deadline = time.monotonic() + 175
    tested = 0

    def run(initial, offset, value):
        buffer = bytearray(initial)
        try:
            target.pack_into(buffer, offset, value)
        except Exception as exc:
            return ("exception", type(exc).__name__, str(exc), bytes(buffer))
        return bytes(buffer)

    def check(initial, offset, value):
        nonlocal tested
        expected = reference(initial, offset, 0, value)
        actual = run(initial, offset, value)
        tested += 1
        if actual != expected:
            repeated = run(initial, offset, value)
            if repeated != expected:
                print("COUNTEREXAMPLE:")
                print(repr((bytearray(initial), offset, value)))
                print("actual:", repr(repeated))
                print("expected:", repr(expected))
                return True
        return False

    values = (b"", b"a", b"a" * 256, b"b" * 1024)
    for length in range(1, 33):
        for initial in (
            bytes(length),
            b"\xfe" * length,
            bytes(i % 255 for i in range(length)),
        ):
            for offset in range(length):
                for value in values:
                    if time.monotonic() >= deadline:
                        print("NO COUNTEREXAMPLE", tested)
                        return
                    if check(initial, offset, value):
                        return

    rng = random.Random(20260309)
    while time.monotonic() < deadline:
        length = rng.randint(1, 32)
        initial = bytes(rng.randrange(255) for _ in range(length))
        offset = rng.randrange(length)
        choice = rng.randrange(4)
        if choice == 0:
            value = b""
        elif choice == 1:
            value = b"a"
        else:
            size = rng.randint(256, 2048) if choice == 2 else rng.randint(0, 255)
            value = bytes(rng.randrange(256) for _ in range(size))
        if check(initial, offset, value):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()