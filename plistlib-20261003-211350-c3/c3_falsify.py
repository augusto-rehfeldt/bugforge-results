import io
import plistlib
import random
import time


class WriteOnly(io.RawIOBase):
    def __init__(self):
        super().__init__()
        self.data = bytearray()

    def writable(self):
        return True

    def write(self, data):
        self.data.extend(data)
        return len(data)


def check(value):
    fp = WriteOnly()
    try:
        plistlib.dump(value, fp, fmt=plistlib.FMT_BINARY)
        actual = plistlib.loads(bytes(fp.data))
        if type(actual) is int and actual == value:
            return True, actual
        return False, actual
    except Exception as exc:
        return False, ("exception", type(exc).__name__, str(exc))
    finally:
        fp.close()


def main():
    # The documented round-trip definition independently requires that an
    # integer deserialize to exactly the original integer.
    for value in (0, -1):
        fp = io.BytesIO()
        try:
            plistlib.dump(value, fp, fmt=plistlib.FMT_BINARY)
            actual = plistlib.loads(fp.getvalue())
        except Exception as exc:
            print("SANITY FAILED", repr(value), type(exc).__name__, str(exc))
            return
        print("SANITY:", repr(value), "actual:", repr(actual),
              "expected:", repr(value))
        if type(actual) is not int or actual != value:
            print("SANITY FAILED")
            return

    deadline = time.monotonic() + 175
    rng = random.Random(20260217)
    edges = [
        0, 1, -1, -(1 << 63), (1 << 63) - 1,
        1 << 63, (1 << 64) - 1,
        255, 256, 65535, 65536, -128, -129,
    ]
    tested = 0

    def inputs():
        yield from edges
        while time.monotonic() < deadline:
            yield rng.randrange(-(1 << 63), 1 << 64)

    for value in inputs():
        if time.monotonic() >= deadline:
            break
        tested += 1
        passed, actual = check(value)
        if not passed:
            passed_again, actual_again = check(value)
            if not passed_again and actual_again == actual:
                print("COUNTEREXAMPLE:", repr(value),
                      "actual:", repr(actual_again),
                      "expected:", repr(value))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()