import binascii
import io
import quopri
import random
import time


def reference_encode(s):
    """Token-preserving quoted-printable encoding for CR/LF-free bytes."""
    tokens = [
        bytes([b]) if 33 <= b <= 126 and b != 61
        else ("=%02X" % b).encode("ascii")
        for b in s
    ]
    lines = []
    line = b""
    for token in tokens:
        if len(line) + len(token) > 75:
            lines.append(line + b"=\n")
            line = b""
        line += token
    return b"".join(lines) + line


original_encoder = quopri.b2a_qp


def run(s, fallback):
    previous = quopri.b2a_qp
    try:
        quopri.b2a_qp = None if fallback else original_encoder
        output = io.BytesIO()
        quopri.encode(io.BytesIO(s), output, quotetabs=True, header=False)
        encoded = output.getvalue()
        return ("result", encoded, binascii.a2b_qp(encoded))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))
    finally:
        quopri.b2a_qp = previous


def main():
    for index, s in enumerate((b"Hello world!", b"tab\t=\xff"), 1):
        expected_encoding = reference_encode(s)
        results = [run(s, fallback) for fallback in (False, True)]
        if any(
            result != ("result", expected_encoding, s)
            for result in results
        ):
            print("SANITY FAILED")
            return
        print("SANITY %d: reference agrees" % index)

    started = time.monotonic()
    tested = 0

    def check(s):
        nonlocal tested
        assert 10 not in s and 13 not in s
        # Independently, the documented round-trip result is the input itself.
        expected = bytes(s)
        for fallback in (True, False):
            if time.monotonic() - started >= 175:
                return "timeout"
            actual = run(s, fallback)
            tested += 1
            failed = actual[0] != "result" or actual[2] != expected
            if failed:
                repeated = run(s, fallback)
                if repeated == actual:
                    print("COUNTEREXAMPLE:")
                    print(repr(s))
                    print("actual:", repr(actual))
                    print("expected:", repr(expected))
                    print("fallback:", fallback)
                    return "failure"
        return None

    edges = [b"A" * 74 + b"\xff"]
    for length in range(73, 77):
        for escaped in (b"\xff", b"=", b"\t", b" ", b"\x00"):
            for suffix in (b"", b"B", b"B" * 80):
                edges.append(b"A" * length + escaped + suffix)
    edges.extend((b"", b"\xff" * 100, b" " * 100, b"A" * 200))

    for s in edges:
        status = check(s)
        if status == "failure":
            return
        if status == "timeout":
            print("NO COUNTEREXAMPLE", tested)
            return

    rng = random.Random(20250308)
    alphabet = [b for b in range(256) if b not in (10, 13)]
    escaping = [b for b in alphabet if not (33 <= b <= 126 and b != 61)]
    while time.monotonic() - started < 175:
        if rng.randrange(2):
            s = (
                b"A" * rng.randrange(73, 77)
                + bytes([rng.choice(escaping)])
                + bytes(rng.choice(alphabet) for _ in range(rng.randrange(200)))
            )
        else:
            s = bytes(
                rng.choice(alphabet) for _ in range(rng.randrange(1025))
            )
        status = check(s)
        if status == "failure":
            return
        if status == "timeout":
            break

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()