import quopri
import random
import time

HEX = b"0123456789ABCDEF"


def reference(s):
    """Encode whole tokens; never split an =HH escape."""
    tokens = []
    for b in s:
        if 33 <= b <= 126 and b != 61:
            tokens.append(bytes((b,)))
        else:
            tokens.append(bytes((61, HEX[b >> 4], HEX[b & 15])))

    lines = []
    line = bytearray()
    for token in tokens:
        if len(line) + len(token) > 75:
            lines.append(bytes(line) + b"=\n")
            line.clear()
        line.extend(token)
    lines.append(bytes(line))
    return b"".join(lines)


def contiguous_escapes(encoded):
    """Every non-soft-break '=' must introduce two hex digits on its line."""
    for line in encoded.split(b"\n"):
        i = 0
        while i < len(line):
            if line[i] != 61:
                i += 1
            elif i == len(line) - 1:
                # Terminal '=' is a soft line break.
                i += 1
            elif (
                i + 2 < len(line)
                and line[i + 1] in HEX
                and line[i + 2] in HEX
            ):
                i += 3
            else:
                return False
    return True


def main():
    original = quopri.b2a_qp
    count = 0
    deadline = time.monotonic() + 175
    try:
        quopri.b2a_qp = None
        for s in (b"Hello world!", b"plain\ttext=\xff"):
            expected = reference(s)
            actual = quopri.encodestring(s, quotetabs=True, header=False)
            print("SANITY:", repr(s), actual == expected)
            if actual != expected:
                print("SANITY FAILED")
                return

        implementations = [None]
        if original is not None:
            implementations.append(original)

        def check(s):
            nonlocal count
            expected = reference(s)
            for implementation in implementations:
                quopri.b2a_qp = implementation
                actual = quopri.encodestring(s, quotetabs=True, header=False)
                count += 1
                if not contiguous_escapes(actual):
                    repeated = quopri.encodestring(
                        s, quotetabs=True, header=False
                    )
                    if repeated == actual and not contiguous_escapes(repeated):
                        print("COUNTEREXAMPLE:")
                        print(repr(s))
                        print("actual:", repr(actual))
                        print("expected:", repr(expected))
                        return True
            return False

        cases = [b"A" * 74 + b"\xff" + b"B"]
        for n in range(73, 77):
            for escaped in (0, 9, 32, 61, 127, 128, 255):
                cases.append(b"A" * n + bytes((escaped,)) + b"B")

        for s in cases:
            if check(s):
                return

        rng = random.Random(20260517)
        printable = bytes(b for b in range(33, 127) if b != 61)
        escaping = (0, 9, 32, 61, 127, 128, 200, 255)
        for _ in range(100000):
            if time.monotonic() >= deadline:
                break
            prefix = bytes(rng.choice(printable) for _ in range(rng.randrange(73, 77)))
            suffix = bytes(rng.choice(printable) for _ in range(rng.randrange(1, 20)))
            s = prefix + bytes((rng.choice(escaping),)) + suffix
            if check(s):
                return

        print("NO COUNTEREXAMPLE", count)
    finally:
        quopri.b2a_qp = original


if __name__ == "__main__":
    main()