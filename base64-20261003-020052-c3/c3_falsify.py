import base64
import random
import time


def reference(data, wrapcol):
    """Encode Adobe ASCII85 from scratch, then apply the documented bound."""
    pieces = []
    for offset in range(0, len(data), 4):
        block = data[offset:offset + 4]
        value = int.from_bytes(block.ljust(4, b"\0"), "big")
        if len(block) == 4 and value == 0:
            pieces.append(b"z")
            continue
        digits = bytearray(5)
        for index in range(4, -1, -1):
            value, remainder = divmod(value, 85)
            digits[index] = remainder + 33
        pieces.append(bytes(digits[:len(block) + 1]))
    encoded = b"<~" + b"".join(pieces) + b"~>"
    return b"\n".join(
        encoded[index:index + wrapcol]
        for index in range(0, len(encoded), wrapcol)
    )


def main():
    for data, wrapcol in [(b"hello", 80), (b"\0\0\0\0abcd", 80)]:
        expected = reference(data, wrapcol)
        actual = base64.a85encode(data, wrapcol=wrapcol, adobe=True)
        print("SANITY:", repr((data, wrapcol)), repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 175
    tested = 0

    def check(data, wrapcol):
        nonlocal tested
        actual = base64.a85encode(data, wrapcol=wrapcol, adobe=True)
        tested += 1
        if all(len(line) <= wrapcol for line in actual.split(b"\n")):
            return False
        repeated = base64.a85encode(data, wrapcol=wrapcol, adobe=True)
        if repeated != actual or all(
            len(line) <= wrapcol for line in repeated.split(b"\n")
        ):
            return False
        expected = reference(data, wrapcol)
        print("COUNTEREXAMPLE:")
        print(repr((data, wrapcol)))
        print("actual:", repr(actual))
        print("expected:", repr(expected))
        return True

    edge_inputs = [
        b"", b"\0", b"a", b"\xff", b"\0" * 4, b"abcd",
        b"abcde", bytes(range(256)), b"\0" * 1024, b"x" * 1024,
    ]
    for data in edge_inputs:
        for wrapcol in [1, 2, 3, 4, 5, 6, 7, 10, 80]:
            if time.monotonic() >= deadline:
                print("NO COUNTEREXAMPLE", tested)
                return
            if check(data, wrapcol):
                return

    rng = random.Random(20260301)
    while time.monotonic() < deadline:
        size = rng.randrange(4097)
        data = bytes(rng.getrandbits(8) for _ in range(size))
        wrapcol = rng.choice([1, 1, 2, 3, 4, 5, rng.randrange(1, 257)])
        if check(data, wrapcol):
            return
    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()