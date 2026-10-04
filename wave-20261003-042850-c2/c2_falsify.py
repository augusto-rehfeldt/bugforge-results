import io
import random
import time
import wave


def reference(case):
    # Documentation forbids all parameter changes after either write method,
    # independently of the number of bytes written.
    return "raises wave.Error"


def check(case):
    writer = wave.open(io.BytesIO(), "wb")
    try:
        writer.setnchannels(case["channels"])
        writer.setsampwidth(case["sample_width"])
        writer.setframerate(case["frame_rate"])
        getattr(writer, case["method"])(case["data"])
        try:
            writer.setnchannels(case["new_channels"])
        except wave.Error:
            return "raises wave.Error"
        except Exception as exc:
            return ("unexpected exception", type(exc).__name__, str(exc))
        return "no exception"
    finally:
        writer.close()


def main():
    deadline = time.monotonic() + 175
    tested = 0

    for index, method in enumerate(("writeframes", "writeframesraw"), 1):
        case = {
            "channels": 1,
            "sample_width": 2,
            "frame_rate": 44100,
            "method": method,
            "data": b"\x00\x00",
            "new_channels": 2,
        }
        expected = reference(case)
        actual = check(case)
        print("SANITY {}: actual={!r}, expected={!r}".format(
            index, actual, expected
        ))
        if actual != expected:
            print("SANITY FAILED")
            return

    def test(case):
        nonlocal tested
        expected = reference(case)
        actual = check(case)
        tested += 1
        if actual != expected:
            repeated = check(case)
            tested += 1
            if repeated == actual:
                print("COUNTEREXAMPLE:", repr(case),
                      "actual:", repr(actual), "expected:", repr(expected))
                return True
        return False

    # Empty writes at every valid boundary combination.
    for method in ("writeframes", "writeframesraw"):
        for channels in (1, 2):
            for sample_width in (1, 4, 2, 3):
                for frame_rate in (8000, 44100):
                    if time.monotonic() >= deadline:
                        print("NO COUNTEREXAMPLE", tested)
                        return
                    case = {
                        "channels": channels,
                        "sample_width": sample_width,
                        "frame_rate": frame_rate,
                        "method": method,
                        "data": b"",
                        "new_channels": 3 - channels,
                    }
                    if test(case):
                        return

    rng = random.Random(20250308)
    for _ in range(10000):
        if time.monotonic() >= deadline:
            break
        channels = rng.choice((1, 2))
        case = {
            "channels": channels,
            "sample_width": rng.randint(1, 4),
            "frame_rate": rng.choice((8000, 44100)),
            "method": rng.choice(("writeframes", "writeframesraw")),
            "data": b"",
            "new_channels": 3 - channels,
        }
        if test(case):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()