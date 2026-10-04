import quopri
import random
import time


def reference_short(s):
    """Independent QP encoding for short, non-wrapping sanity inputs."""
    out = bytearray()
    for i, b in enumerate(s):
        literal = (33 <= b <= 60 or 62 <= b <= 126)
        whitespace = b in (9, 32) and i != len(s) - 1
        if literal or whitespace:
            out.append(b)
        else:
            out.extend(("=%02X" % b).encode("ascii"))
    assert len(out) <= 76
    return bytes(out)


def main():
    saved = quopri.b2a_qp
    quopri.b2a_qp = None
    try:
        for s in (b"Hello world", b"cost=\xff"):
            expected = reference_short(s)
            actual = quopri.encodestring(s, quotetabs=False, header=False)
            print("SANITY:", repr(s), repr(actual), repr(expected))
            if actual != expected:
                print("SANITY FAILED")
                return

        deadline = time.monotonic() + 175
        tested = 0

        def check(s):
            nonlocal tested
            assert isinstance(s, bytes) and b"\r" not in s and b"\n" not in s
            tested += 1
            actual = quopri.encodestring(s, quotetabs=False, header=False)
            lengths = [len(line) for line in actual.split(b"\n")]
            # RFC 1521 independently supplies this upper bound.
            if all(length <= 76 for length in lengths):
                return False

            repeated = quopri.encodestring(s, quotetabs=False, header=False)
            repeated_lengths = [len(line) for line in repeated.split(b"\n")]
            if not any(length > 76 for length in repeated_lengths):
                return False

            print("COUNTEREXAMPLE:")
            print(repr(s))
            print("actual:", repr(repeated))
            print("actual line lengths:", repr(repeated_lengths))
            print("expected: every physical line length <= 76 bytes")
            return True

        edges = [
            b"A" * 74 + b" " + b"BB",
            b"A" * 74 + b"\t" + b"BB",
            b"",
            b"A" * 76,
            b"A" * 77,
            b"A" * 73 + b" " + b"BBB",
            b"A" * 75 + b" " + b"BB",
            b" " * 200,
            b"\t" * 200,
            b"=" * 100,
            b"\xff" * 100,
        ]
        for s in edges:
            if check(s):
                return

        rng = random.Random(20260417)
        alphabet = bytes(b for b in range(256) if b not in (10, 13))
        printable = bytes(range(32, 127)) + b"\t"

        while time.monotonic() < deadline:
            if rng.randrange(2):
                s = (
                    bytes(rng.choice(printable) for _ in range(74))
                    + rng.choice((b" ", b"\t"))
                    + bytes(rng.choice(printable)
                            for _ in range(rng.randint(1, 200)))
                )
            else:
                s = bytes(rng.choice(alphabet)
                          for _ in range(rng.randint(0, 1024)))
            if check(s):
                return

        print("NO COUNTEREXAMPLE")
        print(tested)
    finally:
        quopri.b2a_qp = saved


if __name__ == "__main__":
    main()