import random
import struct
import time


def reference_unpack_b(buffer):
    # 'B' denotes one unsigned byte per chunk.
    return [(value,) for value in buffer]


def check(buffer):
    s = struct.Struct("B")
    iterator = s.iter_unpack(buffer)
    s.__init__("0s")

    yielded = []
    limit = len(buffer) + 1
    for call in range(1, limit + 1):
        try:
            yielded.append(next(iterator))
        except StopIteration:
            return False, {
                "terminated": True,
                "calls": call,
                "yielded": yielded,
            }
        except Exception as exc:
            # An exception ends repeated yielding, so it is not evidence
            # of the specific nontermination property violation.
            return False, {
                "terminated": True,
                "calls": call,
                "exception": (type(exc).__name__, str(exc)),
                "yielded": yielded,
            }

    return True, {
        "terminated": False,
        "calls": limit,
        "yielded": yielded,
    }


def main():
    deadline = time.monotonic() + 175.0

    for buffer in (b"\x00", b"\x00\x01\x7f\x80\xff"):
        expected = reference_unpack_b(buffer)
        actual = list(struct.Struct("B").iter_unpack(buffer))
        print("SANITY:", repr(buffer), "actual:", actual, "expected:", expected)
        if actual != expected:
            print("SANITY FAILED")
            return

    rng = random.Random(8675309)
    tested = 0

    def inputs():
        for length in (1, 32, 2, 31, *range(3, 31)):
            yield bytes(length)
            yield bytes([255]) * length
            yield bytes(range(length))
            yield bytes(255 if i % 2 else 0 for i in range(length))
        for _ in range(100000):
            length = rng.randrange(1, 33)
            yield bytes(rng.randrange(256) for _ in range(length))

    for buffer in inputs():
        if time.monotonic() >= deadline:
            break
        failed, actual = check(buffer)
        tested += 1
        if failed:
            confirmed, repeated = check(buffer)
            if confirmed:
                expected = {
                    "terminated": True,
                    "within_calls": len(buffer) + 1,
                }
                print(
                    "COUNTEREXAMPLE:",
                    repr(buffer),
                    "actual:",
                    repr(repeated),
                    "expected:",
                    repr(expected),
                )
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()