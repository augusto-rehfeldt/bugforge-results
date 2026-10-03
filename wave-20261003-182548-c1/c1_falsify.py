import io
import random
import struct
import time
import wave


class ReadOnlyStream:
    """Binary stream deliberately exposing no seek method."""
    __slots__ = ("_buffer",)

    def __init__(self, data):
        self._buffer = io.BytesIO(data)

    def read(self, size=-1):
        return self._buffer.read(size)

    def tell(self):
        return self._buffer.tell()

    def close(self):
        self._buffer.close()


def make_case(channels, width, rate, frames, rng):
    block_align = channels * width
    assert 1 <= channels <= 65535
    assert width in (1, 2, 3, 4)
    assert block_align <= 65535
    assert 1 <= rate and rate * block_align <= 0xFFFFFFFF

    payload = bytes(rng.randrange(256) for _ in range(frames * block_align))
    assert len(payload) % 2 == 0

    fmt = struct.pack(
        "<HHIIHH", 1, channels, rate, rate * block_align,
        block_align, width * 8
    )
    chunks = b"fmt " + struct.pack("<I", 16) + fmt
    chunks += b"data" + struct.pack("<I", len(payload)) + payload
    wav = b"RIFF" + struct.pack("<I", 4 + len(chunks)) + b"WAVE" + chunks

    requests = (0, 1, 2, frames + 1, 1)
    offset = 0
    reads = []
    for requested in requests:
        end = min(frames, offset + requested)
        reads.append(payload[offset * block_align:end * block_align])
        offset = end

    expected = (
        "ok",
        (channels, width, rate, frames, "NONE", "not compressed"),
        tuple(reads),
    )
    case = {"wav": wav, "read_requests": requests}
    return case, expected


def observe(case, nonseekable=True):
    stream = (
        ReadOnlyStream(case["wav"])
        if nonseekable else io.BytesIO(case["wav"])
    )
    reader = None
    try:
        reader = wave.open(stream, "rb")
        params = tuple(reader.getparams())
        reads = tuple(reader.readframes(n) for n in case["read_requests"])
        return ("ok", params, reads)
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))
    finally:
        if reader is not None:
            reader.close()
        stream.close()


def main():
    rng = random.Random(0x57415645)

    # Check the independent PCM construction and reference using ordinary,
    # seekable in-memory streams before probing the documented edge condition.
    for index, spec in enumerate(((1, 1, 8000, 8), (2, 2, 44100, 5)), 1):
        case, expected = make_case(*spec, rng)
        actual = observe(case, nonseekable=False)
        print("SANITY {}: {}".format(index, actual == expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    started = time.monotonic()
    tested = 0

    def check(spec):
        nonlocal tested
        case, expected = make_case(*spec, rng)
        actual = observe(case)
        tested += 1
        if actual != expected:
            repeated = observe(case)
            if repeated != expected:
                print("COUNTEREXAMPLE:")
                print(repr(case))
                print("actual:", repr(repeated))
                print("expected:", repr(expected))
                return True
        return False

    edges = [
        (1, 1, 8000, 2),
        (1, 1, 1, 0),
        (1, 2, 1, 1),
        (2, 1, 8000, 1),
        (1, 3, 48000, 2),
        (2, 3, 48000, 3),
        (1, 4, 192000, 1),
        (65535, 1, 1, 0),
        (32767, 2, 1, 1),
        (1, 1, 0xFFFFFFFF, 2),
    ]
    for spec in edges:
        if check(spec):
            return

    while tested < 50000 and time.monotonic() - started < 170:
        channels = rng.choice((1, 2, 3, 4, 8, 16, 32, 255))
        width = rng.choice((1, 2, 3, 4))
        align = channels * width
        rate = rng.randint(1, min(384000, 0xFFFFFFFF // align))
        frames = rng.randint(0, 64)
        if align * frames % 2:
            frames += 1
        if check((channels, width, rate, frames)):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()