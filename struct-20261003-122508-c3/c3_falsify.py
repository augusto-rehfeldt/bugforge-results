import random
import struct
import time


def reference(data):
    # An exactly sized 's' field contains all input bytes unchanged.
    return bytes(data)


def main():
    for data in (b"A", b"\x00\x7f\xffB"):
        expected = reference(data)
        actual = struct.pack(f"{len(data)}s", data)
        print(f"SANITY: input={data!r} actual={actual!r} expected={expected!r}")
        if actual != expected:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 175.0
    tested = 0

    def run(data):
        b = bytearray(data)
        expected = reference(b)
        try:
            struct.pack_into(f"{len(b)}s", b, 0, b)
            actual = bytes(b)
        except Exception as exc:
            actual = ("EXCEPTION", type(exc).__name__, str(exc))
        return actual, expected

    def check(data):
        nonlocal tested
        tested += 1
        actual, expected = run(data)
        if actual != expected:
            repeated, repeated_expected = run(data)
            if repeated != repeated_expected:
                print("COUNTEREXAMPLE:")
                print(repr((f"{len(data)}s", bytearray(data), 0, bytearray(data))))
                print(f"actual={repeated!r}")
                print(f"expected={repeated_expected!r}")
                return True
        return False

    edges = [
        b"A",
        b"\xff",
        b"\x00A",
        b"A\x00",
        b"AB",
        b"\x00" * 31 + b"\x01",
        b"\x01" + b"\x00" * 31,
        bytes(range(256)),
        b"\xff" * 1024,
        b"A" * 65536,
    ]
    for data in edges:
        if time.monotonic() >= deadline:
            break
        if check(data):
            return

    rng = random.Random(0x5E1F)
    while time.monotonic() < deadline:
        n = rng.choice((1, 2, 3, 7, 8, 15, 16, 255, 256, 4096))
        if rng.randrange(2):
            n = rng.randint(1, 16384)
        data = bytearray(rng.getrandbits(8) for _ in range(n))
        if not any(data):
            data[rng.randrange(n)] = rng.randint(1, 255)
        if check(data):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()