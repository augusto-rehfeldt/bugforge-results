import json
import random
import struct
import subprocess
import sys
import time


def check_in_process(case):
    captured = struct.Struct("B")

    class Exporter:
        def __init__(self, token):
            self.token = token

        def __buffer__(self, flags):
            captured.__init__("0s")
            return memoryview(b"")

    # Independently, 0s contains zero bytes per record. No positive
    # fixed-size chunk exists, so iterator creation must raise error.
    expected = "raises struct.error"
    try:
        iterator = captured.iter_unpack(Exporter(case["token"]))
    except struct.error:
        return True, expected, expected
    except Exception as exc:
        return False, ("raises", type(exc).__name__, str(exc)), expected
    else:
        # Creation itself should fail; do not advance a potentially
        # broken zero-sized iterator.
        del iterator
        return False, "returned an iterator", expected


def check(case):
    # Buffer callbacks can trigger a native interpreter crash. Isolate
    # each check so the crash can be reported and independently confirmed.
    result = subprocess.run(
        [sys.executable, __file__, "--worker", json.dumps(case["token"])],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    expected = "raises struct.error"
    if result.returncode != 0:
        return False, ("process exited", result.returncode), expected
    return json.loads(result.stdout)


def main():
    deadline = time.monotonic() + 170.0

    # Independent reference for the ordinary unsigned-byte format.
    for data in (b"", b"\x00\x01\x7f\x80\xff"):
        expected = [(value,) for value in data]
        try:
            actual = list(struct.Struct("B").iter_unpack(data))
        except Exception as exc:
            actual = (type(exc).__name__, str(exc))
        print("SANITY:", repr(data), repr(actual), repr(expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    # Older interpreters do not support Python-defined buffer exporters.
    class Probe:
        def __buffer__(self, flags):
            return memoryview(b"")

    try:
        view = memoryview(Probe())
    except TypeError:
        print("NO COUNTEREXAMPLE", 0)
        return
    else:
        view.release()

    rng = random.Random(0xB00F)
    tested = 0

    def cases():
        for token in (None, 0, 1, -1, 2**64, -(2**64)):
            yield {"initial": "B", "replacement": "0s",
                   "buffer": b"", "token": token}
        for _ in range(10000):
            # The contract fixes the format and payload. Randomize only
            # inert exporter state, keeping every input within that space.
            yield {"initial": "B", "replacement": "0s",
                   "buffer": b"", "token": rng.getrandbits(128)}

    for case in cases():
        if time.monotonic() >= deadline:
            break
        good, actual, expected = check(case)
        tested += 1
        if not good:
            confirmed, repeated_actual, _ = check(case)
            tested += 1
            if not confirmed:
                print("COUNTEREXAMPLE:", repr(case),
                      "actual =", repr((actual, repeated_actual)),
                      "expected =", repr(expected))
                return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--worker":
        print(json.dumps(check_in_process({"token": json.loads(sys.argv[2])})))
    else:
        main()