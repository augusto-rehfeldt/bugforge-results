import io
import random
import time
import wave


class MemoryStream:
    def __init__(self, frame_size, accepted_frames=None):
        self.buffer = io.BytesIO()
        self.frame_size = frame_size
        self.accepted_frames = accepted_frames
        self.payload_bytes = 0

    def read(self, size=-1):
        return self.buffer.read(size)

    def write(self, data):
        data = bytes(data)
        position = self.buffer.tell()
        header_bytes = min(len(data), max(0, 44 - position))
        payload = len(data) - header_bytes
        accepted = payload
        if payload and self.accepted_frames is not None:
            accepted = min(payload, self.accepted_frames * self.frame_size)
        count = header_bytes + accepted
        written = self.buffer.write(data[:count])
        self.payload_bytes += max(0, written - header_bytes)
        return written

    def seek(self, offset, whence=0):
        return self.buffer.seek(offset, whence)

    def tell(self):
        return self.buffer.tell()

    def flush(self):
        return self.buffer.flush()

    def close(self):
        return self.buffer.close()


def run(case):
    frame_size = case["channels"] * case["sample_width"]
    assert len(case["data"]) % frame_size == 0
    stream = MemoryStream(frame_size, case["accepted_frames"])
    writer = wave.open(stream, "wb")
    try:
        writer.setnchannels(case["channels"])
        writer.setsampwidth(case["sample_width"])
        writer.setframerate(case["rate"])
        writer.writeframesraw(case["data"])
        actual = writer.tell()
        # Independent definition: stored audio bytes / bytes per PCM frame.
        expected = stream.payload_bytes // frame_size
        assert stream.payload_bytes % frame_size == 0
        return actual, expected
    finally:
        writer.close()
        stream.close()


def main():
    sanity_cases = [
        dict(channels=1, sample_width=1, rate=8000,
             data=b"\x00\x01\x02\x03", accepted_frames=None),
        dict(channels=2, sample_width=2, rate=44100,
             data=b"\x00\x01\x02\x03" * 7, accepted_frames=None),
    ]
    for index, case in enumerate(sanity_cases, 1):
        actual, expected = run(case)
        print("SANITY {}: actual={!r}, expected={!r}".format(
            index, actual, expected))
        if actual != expected:
            print("SANITY FAILED")
            return

    start = time.monotonic()
    tested = 0

    def check(case):
        nonlocal tested
        actual, expected = run(case)
        tested += 1
        if actual != expected:
            repeated_actual, repeated_expected = run(case)
            if (actual, expected) == (repeated_actual, repeated_expected):
                print("COUNTEREXAMPLE:")
                print(repr(case))
                print("actual:", repr(actual))
                print("expected:", repr(expected))
                return True
        return False

    edges = [
        dict(channels=1, sample_width=1, rate=8000,
             data=b"\x00\x01\x02\x03", accepted_frames=2),
        dict(channels=2, sample_width=2, rate=44100,
             data=b"\x00" * 12, accepted_frames=1),
        dict(channels=1, sample_width=3, rate=8000,
             data=b"\xff" * 6, accepted_frames=1),
    ]
    for case in edges:
        if check(case):
            return

    rng = random.Random(20260123)
    while tested < 100000 and time.monotonic() - start < 170:
        channels = rng.randint(1, 8)
        width = rng.randint(1, 4)
        frames = rng.randint(2, 256)
        case = dict(
            channels=channels,
            sample_width=width,
            rate=rng.choice([8000, 16000, 22050, 44100, 48000]),
            data=bytes(rng.randrange(256)
                       for _ in range(frames * channels * width)),
            accepted_frames=rng.randint(1, frames - 1),
        )
        if check(case):
            return

    print("NO COUNTEREXAMPLE")
    print(tested)


if __name__ == "__main__":
    main()