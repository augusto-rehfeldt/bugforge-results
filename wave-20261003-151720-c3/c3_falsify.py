import io
import random
import struct
import time
import wave


class FragmentedIO(io.BytesIO):
    def __init__(self, contents, limit):
        super().__init__(contents)
        self.limit = limit

    def read(self, size=-1):
        if self.tell() >= 44:
            size = self.limit if size < 0 else min(size, self.limit)
        return super().read(size)


def make_wav(channels, width, payload):
    rate = 8000
    frame_width = channels * width
    return (
        b"RIFF"
        + struct.pack("<I", 36 + len(payload))
        + b"WAVEfmt "
        + struct.pack(
            "<IHHIIHH",
            16, 1, channels, rate, rate * frame_width,
            frame_width, width * 8,
        )
        + b"data"
        + struct.pack("<I", len(payload))
        + payload
    )


def observe(case):
    channels, width, frames, limit, payload = case
    stream = FragmentedIO(make_wav(channels, width, payload), limit)
    with wave.open(stream, "rb") as reader:
        pieces = []
        while True:
            piece = reader.readframes(1)
            if not piece:
                break
            pieces.append(piece)
        return b"".join(pieces), reader.tell()


def expected(case):
    channels, width, frames, limit, payload = case
    assert len(payload) == frames * channels * width
    return payload, len(payload) // (channels * width)


def main():
    deadline = time.monotonic() + 175
    rng = random.Random(718293)

    for case in (
        (1, 2, 3, 2, b"\x00\x00\x01\x00\xff\x7f"),
        (2, 2, 2, 4, b"\x00\x00\x01\x00\x02\x00\x03\x00"),
    ):
        actual = observe(case)
        reference = expected(case)
        print("SANITY:", actual, reference, flush=True)
        if actual != reference:
            print("SANITY FAILED")
            return

    tested = 0

    def check(case):
        nonlocal tested
        tested += 1
        reference = expected(case)
        actual = observe(case)
        if actual != reference:
            repeated = observe(case)
            if repeated == actual:
                print("COUNTEREXAMPLE:")
                print(repr({
                    "channels": case[0],
                    "sample_width": case[1],
                    "frames": case[2],
                    "short_read_limit": case[3],
                    "audio_payload": case[4],
                }))
                print("actual:", repr(actual))
                print("expected:", repr(reference))
                return True
        return False

    edges = [
        (1, 2, 1, 1),
        (1, 2, 5, 1),
        (1, 3, 2, 2),
        (2, 2, 3, 3),
        (2, 3, 4, 5),
        (2, 4, 2, 3),
    ]
    for channels, width, frames, limit in edges:
        payload = bytes(i % 256 for i in range(channels * width * frames))
        if check((channels, width, frames, limit, payload)):
            return

    while time.monotonic() < deadline:
        channels = rng.randint(1, 8)
        width = rng.randint(1, 4)
        frame_width = channels * width
        frames = rng.randint(1, 128)
        limit = rng.randint(1, frame_width * 2 + 1)
        payload = bytes(rng.getrandbits(8) for _ in range(frame_width * frames))
        if check((channels, width, frames, limit, payload)):
            return

    print("NO COUNTEREXAMPLE", tested)


if __name__ == "__main__":
    main()