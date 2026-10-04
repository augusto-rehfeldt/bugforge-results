import json
import math
import random
import time


class BadFloat(float):
    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return False


def reference(value):
    # float() extracts the underlying value without using overridden equality.
    if not math.isfinite(float(value)):
        return ("exception", "ValueError")
    return ("result", "[" + repr(float(value)) + "]")


def actual(value):
    try:
        result = "".join(json.JSONEncoder(allow_nan=False).iterencode([value]))
        return ("result", result)
    except Exception as exc:
        return ("exception", type(exc).__name__)


def main():
    start = time.monotonic()
    for value in (1.25, float("nan")):
        expected = reference(value)
        observed = actual(value)
        print("SANITY:", repr([value]), observed, expected)
        if observed != expected:
            print("SANITY FAILED")
            return

    rng = random.Random(1729)
    tested = 0

    def check(value):
        nonlocal tested
        expected = reference(value)
        observed = actual(value)
        tested += 1
        if observed != expected:
            repeated = actual(value)
            if repeated == observed:
                print("COUNTEREXAMPLE:", repr([value]),
                      "actual =", repr(observed),
                      "expected =", repr(expected))
                return True
        return False

    for value in (
        BadFloat(float("nan")),
        BadFloat(-float("nan")),
    ):
        if check(value):
            return

    while time.monotonic() - start < 175:
        # Randomize the NaN sign and payload using IEEE-754 binary64 bits.
        import struct
        payload = rng.randrange(1, 1 << 52)
        bits = (rng.getrandbits(1) << 63) | (0x7FF << 52) | payload
        value = BadFloat(struct.unpack(">d", struct.pack(">Q", bits))[0])
        if check(value):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()